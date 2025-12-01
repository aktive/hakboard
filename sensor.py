from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util
from datetime import datetime

from .const import (
    DOMAIN,
    CONF_PROJECT_FILTER,
    CONF_INSTANCE_KEY,
    CONF_API_ENDPOINT,
)
from .utils import parse_text_into_ids


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]

    merged = {**entry.data, **entry.options}
    display_name = merged.get("display_name", merged.get("instance_key"))
    instance_key = merged.get(CONF_INSTANCE_KEY)

    coordinator = data["coordinator"]

    filter_text = merged.get(CONF_PROJECT_FILTER, "")
    api_endpoint = merged.get(CONF_API_ENDPOINT, "")

    allowed_ids = parse_text_into_ids(filter_text)

    valid_unique_ids = set()
    sensors = []

    # --- SUMMARY: PROJECTS TOTAL ---
    uid_total = f"hakboard_{instance_key}_summary_projects_total"
    valid_unique_ids.add(uid_total)
    sensors.append(HakboardProjectsTotalSensor(coordinator, instance_key))

    # --- SUMMARY: PROJECTS SYNCED ---
    uid_synced = f"hakboard_{instance_key}_summary_projects_synced"
    valid_unique_ids.add(uid_synced)
    sensors.append(HakboardProjectsSyncedSensor(coordinator, instance_key, allowed_ids))

    # --- SUMMARY: USERS ---
    uid_users = f"hakboard_{instance_key}_summary_users"
    valid_unique_ids.add(uid_users)
    sensors.append(HakboardUsersSensor(coordinator, instance_key))

    # -------------------------------------------------------------------
    # NEW STANDARD NAME: SYSTEM STATUS
    # -------------------------------------------------------------------
    uid_status = f"hakboard_{instance_key}_system_status"
    valid_unique_ids.add(uid_status)
    sensors.append(
        HakboardSystemStatusSensor(
            coordinator,
            instance_key,
            api_endpoint,
            entry.entry_id,
            filter_text,
            allowed_ids,
        )
    )

    # --- PROJECT SENSORS ---
    projects = coordinator.data.get("projects", [])
    for project in projects:
        p_id = project["id"]
        if p_id in allowed_ids:
            p_uid = f"hakboard_{instance_key}_project_{p_id}"
            valid_unique_ids.add(p_uid)
            sensors.append(
                HakboardProjectSensor(
                    coordinator,
                    instance_key,
                    project,
                    api_endpoint,
                )
            )

    async_add_entities(sensors)

    # --- ORPHAN CLEANUP ---
    entity_registry = er.async_get(hass)
    entries = entity_registry.entities.get_entries_for_config_entry_id(entry.entry_id)

    for entity in entries:
        if entity.unique_id not in valid_unique_ids and entity.domain == "sensor":
            entity_registry.async_remove(entity.entity_id)


# ============================================================================
# BASE SENSOR
# ============================================================================
class HakboardBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, instance_key):
        super().__init__(coordinator)
        self.instance_key = instance_key

    @property
    def display_name_dynamic(self):
        merged = {
            **self.coordinator.config_entry.data,
            **self.coordinator.config_entry.options,
        }
        return merged.get("display_name", merged.get("instance_key"))

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.instance_key)},
            "name": f"HAKboard ({self.display_name_dynamic})",
            "manufacturer": "HAKboard",
            "entry_type": "service",
        }


# ============================================================================
# SUMMARY: PROJECTS TOTAL
# ============================================================================
class HakboardProjectsTotalSensor(HakboardBaseSensor):
    def __init__(self, coordinator, instance_key):
        super().__init__(coordinator, instance_key)
        self._attr_unique_id = f"hakboard_{instance_key}_summary_projects_total"
        self.entity_id = f"sensor.hakboard_{instance_key}_summary_projects_total"

    @property
    def name(self):
        return f"{self.display_name_dynamic} • Summary: Projects Total"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("projects", []))


# ============================================================================
# SUMMARY: PROJECTS SYNCED
# ============================================================================
class HakboardProjectsSyncedSensor(HakboardBaseSensor):
    def __init__(self, coordinator, instance_key, allowed_ids):
        super().__init__(coordinator, instance_key)
        self.allowed_ids = allowed_ids
        self._attr_unique_id = f"hakboard_{instance_key}_summary_projects_synced"
        self.entity_id = f"sensor.hakboard_{instance_key}_summary_projects_synced"

    @property
    def name(self):
        return f"{self.display_name_dynamic} • Summary: Projects Synced"

    @property
    def native_value(self):
        projects = self.coordinator.data.get("projects", [])
        return len([p for p in projects if p["id"] in self.allowed_ids])


# ============================================================================
# SUMMARY: USERS
# ============================================================================
class HakboardUsersSensor(HakboardBaseSensor):
    def __init__(self, coordinator, instance_key):
        super().__init__(coordinator, instance_key)
        self._attr_unique_id = f"hakboard_{instance_key}_summary_users"
        self.entity_id = f"sensor.hakboard_{instance_key}_summary_users"

    @property
    def name(self):
        return f"{self.display_name_dynamic} • Summary: Users"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("users", []))

    @property
    def extra_state_attributes(self):
        users = self.coordinator.data.get("users", [])

        active = len([u for u in users if u.get("is_active") == 1])
        admin = len([u for u in users if u.get("role") == "app-admin"])

        user_list = [
            {
                "name": u.get("username"),
                "role": u.get("role"),
                "open_tasks": u.get("open_tasks", 0),
            }
            for u in users
        ][:20]

        return {
            "active_count": active,
            "admin_count": admin,
            "user_list": user_list,
        }


# ============================================================================
# NEW: SYSTEM STATUS SENSOR (formerly summary_status)
# ============================================================================
class HakboardSystemStatusSensor(HakboardBaseSensor):
    _attr_icon = "mdi:pulse"

    def __init__(
        self,
        coordinator,
        instance_key,
        api_endpoint,
        config_entry_id,
        filter_text,
        allowed_ids,
    ):
        super().__init__(coordinator, instance_key)
        self.api_endpoint = api_endpoint
        self.config_entry_id = config_entry_id
        self.filter_text = filter_text
        self.allowed_ids = allowed_ids

        # NEW NAMES
        self._attr_unique_id = f"hakboard_{instance_key}_system_status"
        self.entity_id = f"sensor.hakboard_{instance_key}_system_status"

    @property
    def name(self):
        return f"{self.display_name_dynamic} • System Status"

    @property
    def native_value(self):
        projects = self.coordinator.data.get("projects", [])
        return sum(p.get("task_count", 0) for p in projects)

    @property
    def unit_of_measurement(self):
        return "tasks"

    @property
    def extra_state_attributes(self):
        interval = self.coordinator.update_interval
        seconds = int(interval.total_seconds()) if interval else 0

        if seconds < 60:
            interval_str = f"{seconds}s"
        elif seconds < 3600:
            m = seconds // 60
            s = seconds % 60
            interval_str = f"{m}m" if s == 0 else f"{m}m {s}s"
        else:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            interval_str = f"{h}h" if m == 0 else f"{h}h {m}m"

        projects = self.coordinator.data.get("projects", [])
        synced = len([p for p in projects if p["id"] in self.allowed_ids])

        return {
            "poll_interval": interval_str,
            "api_endpoint": self.api_endpoint,
            "config_entry_id": self.config_entry_id,
            "project_filter": self.filter_text,
            "synced_project_count": synced,
            "last_success_timestamp": dt_util.now().isoformat()
            if self.coordinator.last_update_success
            else None,
            "display_name": self.display_name_dynamic,
        }


# ============================================================================
# PROJECT SENSOR
# ============================================================================
class HakboardProjectSensor(HakboardBaseSensor):
    def __init__(self, coordinator, instance_key, project_data, api_endpoint):
        super().__init__(coordinator, instance_key)

        self.project_id = project_data["id"]
        self.project_name = project_data.get("name", "Unknown")

        self._attr_unique_id = f"hakboard_{instance_key}_project_{self.project_id}"
        self.entity_id = f"sensor.hakboard_{instance_key}_project_{self.project_id}"

        base = api_endpoint.replace("jsonrpc.php", "").rstrip("/")
        self.project_url = f"{base}/board/{self.project_id}"

    @property
    def name(self):
        return (
            f"{self.display_name_dynamic} • Project {self.project_id}: "
            f"{self.project_name}"
        )

    @property
    def native_value(self):
        projects = self.coordinator.data.get("projects", [])
        p = next((x for x in projects if x["id"] == self.project_id), None)
        return p.get("task_count", 0) if p else 0

    @property
    def extra_state_attributes(self):
        projects = self.coordinator.data.get("projects", [])
        p = next((x for x in projects if x["id"] == self.project_id), None)

        if not p:
            return {}

        ts = int(p.get("last_modified", 0))
        last_activity = datetime.fromtimestamp(ts).isoformat() if ts > 0 else None

        attrs = {
            "id": p.get("id"),
            "name": p.get("name"),
            "identifier": p.get("identifier"),
            "description": p.get("description"),
            "project_url": self.project_url,
            "owner": p.get("owner_name", "Unassigned"),
            "project_email": p.get("email") or "",
            "last_activity": last_activity,
            "overdue_count": p.get("overdue_count", 0),
        }

        attrs.update(p.get("column_counts", {}))
        return attrs
