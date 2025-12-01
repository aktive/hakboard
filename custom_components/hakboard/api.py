import aiohttp
import async_timeout
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)


class HakboardAPI:
    """Kanboard JSON-RPC API client."""

    def __init__(self, endpoint: str, token: str):
        self._endpoint = endpoint.rstrip("/")
        self._token = token

    async def _rpc_call(self, session, method, params=None, req_id=1):
        """Helper to perform a single JSON-RPC call."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": req_id,
        }
        if params:
            payload["params"] = params

        async with session.post(
            self._endpoint,
            json=payload,
            auth=aiohttp.BasicAuth("jsonrpc", self._token),
            ssl=False,
        ) as resp:
            if resp.status != 200:
                _LOGGER.error("Kanboard API HTTP error %s", resp.status)
                return None
            data = await resp.json()
            if "error" in data:
                _LOGGER.error("Kanboard API RPC error: %s", data["error"])
                return None
            return data.get("result")

    async def async_validate_credentials(self) -> bool:
        """Soft-check whether the API token appears valid.

        Uses a cheap RPC call (e.g., system.getVersion).
        Returns:
            True if the call succeeds and returns a result.
            False on HTTP error, RPC error, or exception.
        """
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    result = await self._rpc_call(session, "getVersion")
                    if result is None:
                        _LOGGER.warning(
                            "Kanboard API credential validation failed (no result from getVersion)."
                        )
                        return False
                    return True
        except Exception as err:
            _LOGGER.error("Kanboard API credential validation error: %s", err)
            return False

    async def async_fetch_data(self, allowed_ids=None):
        """Fetches Projects, Users, Overdue items, Column stats, and Workloads."""
        if allowed_ids is None:
            allowed_ids = []

        allowed_ids_str = [str(i) for i in allowed_ids]

        try:
            async with async_timeout.timeout(45):
                async with aiohttp.ClientSession() as session:
                    # 1. PARALLEL FETCH: Projects, Users, AND Overdue Tasks
                    # Fetch overdue globally (1 call) instead of per-project (N calls)
                    f_projects = self._rpc_call(session, "getAllProjects")
                    f_users = self._rpc_call(session, "getAllUsers")
                    f_overdue = self._rpc_call(session, "getOverdueTasks")

                    results = await asyncio.gather(f_projects, f_users, f_overdue)

                    all_projects = results[0] or []
                    all_users = results[1] or []
                    all_overdue = results[2] or []

                    # --- MAP OVERDUE COUNTS ---
                    overdue_map = {}
                    for task in all_overdue:
                        p_id = str(task.get("project_id"))
                        overdue_map[p_id] = overdue_map.get(p_id, 0) + 1

                    # --- USER MAP ---
                    user_map = {str(u["id"]): u for u in all_users}

                    # 2. ENRICH PROJECTS
                    tasks_reqs = []
                    cols_reqs = []
                    projects_to_enrich = []

                    for project in all_projects:
                        p_id = str(project["id"])

                        # A. Map Owner Data
                        owner_id = str(project.get("owner_id", 0))
                        if owner_id in user_map:
                            owner_data = user_map[owner_id]
                            project["owner_name"] = (
                                owner_data.get("name") or owner_data.get("username")
                            )
                        else:
                            project["owner_name"] = "Unassigned"

                        # B. Map Overdue Count
                        project["overdue_count"] = overdue_map.get(p_id, 0)

                        # C. Prepare Deep Fetch
                        if p_id in allowed_ids_str:
                            projects_to_enrich.append(project)
                            tasks_reqs.append(
                                self._rpc_call(
                                    session,
                                    "getAllTasks",
                                    {"project_id": project["id"], "status_id": 1},
                                )
                            )
                            cols_reqs.append(
                                self._rpc_call(
                                    session,
                                    "getColumns",
                                    {"project_id": project["id"]},
                                )
                            )
                        else:
                            project["task_count"] = 0
                            project["column_counts"] = {}

                    # 3. Fire parallel requests
                    if tasks_reqs:
                        all_task_results = await asyncio.gather(*tasks_reqs)
                        all_col_results = await asyncio.gather(*cols_reqs)

                        user_workload = {}

                        # 4. Process the data
                        for i, project in enumerate(projects_to_enrich):
                            tasks = all_task_results[i] or []
                            columns = all_col_results[i] or []

                            project["task_count"] = len(tasks)

                            col_breakdown = {col["title"]: 0 for col in columns}
                            col_id_to_name = {
                                col["id"]: col["title"] for col in columns
                            }

                            for task in tasks:
                                c_id = task.get("column_id")
                                c_name = col_id_to_name.get(c_id)
                                if c_name:
                                    col_breakdown[c_name] += 1

                                assignee = task.get("owner_id")
                                if assignee and str(assignee) != "0":
                                    assignee = str(assignee)
                                    user_workload[assignee] = (
                                        user_workload.get(assignee, 0) + 1
                                    )

                            project["column_counts"] = col_breakdown

                        # 5. Attach Workload to User Objects
                        for u in all_users:
                            u_id = str(u.get("id"))
                            u["open_tasks"] = user_workload.get(u_id, 0)

                    return {
                        "projects": all_projects,
                        "users": all_users,
                    }

        except Exception as err:
            _LOGGER.error("Kanboard API error: %s", err)
            return {"projects": [], "users": []}
