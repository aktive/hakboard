# HAKboard Entity Schema

This document describes all entities created by the HAKboard integration.

> **Note**: All entity IDs use the pattern `sensor.hakboard_{instance_key}_*` where `{instance_key}` is the unique identifier configured for each Kanboard instance (e.g., `hl` for "Homelab").

---

## Table of Contents

- [Summary Sensors](#summary-sensors)
  - [Projects Total](#projects-total)
  - [Projects Synced](#projects-synced)
  - [Users Summary](#users-summary)
- [System Status Sensor](#system-status-sensor)
- [Project Sensors](#project-sensors)
- [Entity Naming Convention](#entity-naming-convention)
- [Device Grouping](#device-grouping)

---

## Summary Sensors

### Projects Total
| Property | Value |
|----------|-------|
| **Entity ID** | `sensor.hakboard_{instance_key}_summary_projects_total` |
| **Name** | `{Instance Name} • Summary: Projects Total` |
| **State** | Total number of projects in Kanboard instance |
| **State Class** | `measurement` |

**Attributes**: None

---

### Projects Synced
| Property | Value |
|----------|-------|
| **Entity ID** | `sensor.hakboard_{instance_key}_summary_projects_synced` |
| **Name** | `{Instance Name} • Summary: Projects Synced` |
| **State** | Number of projects matching the configured project filter |
| **State Class** | `measurement` |

**Attributes**: None

---

### Users Summary
| Property | Value |
|----------|-------|
| **Entity ID** | `sensor.hakboard_{instance_key}_summary_users` |
| **Name** | `{Instance Name} • Summary: Users` |
| **State** | Total number of users in Kanboard instance |
| **State Class** | `measurement` |

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `active_count` | int | Number of active users |
| `admin_count` | int | Number of users with `app-admin` role |
| `user_list` | list | Array of user objects (max 20) |

**`user_list` item structure**:
```json
{
  "username": "john_doe",
  "role": "app-admin",
  "open_tasks": 5
}
```

**Possible `role` values**:
- `app-admin` - Administrator
- `app-manager` - Manager
- `app-user` - Standard user

---

## System Status Sensor

| Property | Value |
|----------|-------|
| **Entity ID** | `sensor.hakboard_{instance_key}_system_status` |
| **Name** | `{Instance Name} • System Status` |
| **State** | Total task count across all projects |
| **Unit** | `tasks` |
| **State Class** | `measurement` |
| **Entity Category** | `diagnostic` |
| **Icon** | `mdi:pulse` |

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `instance_url` | string | Base URL of the Kanboard instance |
| `poll_interval` | string | Human-readable polling interval (e.g., `5m`, `1h 30m`) |
| `api_endpoint` | string | Full JSON-RPC API endpoint URL |
| `config_entry_id` | string | Home Assistant config entry ID |
| `project_filter` | string | Configured project filter (e.g., `1-10, 15`) |
| `synced_project_count` | int | Number of projects being synced |
| `last_success_timestamp` | string | ISO timestamp of last successful update |
| `instance_name` | string | Friendly name of the instance |

---

## Project Sensors

One sensor is created for each project matching the configured project filter.

| Property | Value |
|----------|-------|
| **Entity ID** | `sensor.hakboard_{instance_key}_project_{project_id}` |
| **Name** | `{Instance Name} • Project {ID}: {Project Name}` |
| **State** | Total active task count for this project |
| **State Class** | `measurement` |

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Kanboard project ID |
| `project_name` | string | Project name |
| `identifier` | string | Project identifier/code |
| `description` | string | Project description |
| `project_url` | string | Direct URL to project board |
| `owner` | string | Project owner name |
| `project_email` | string | Project email (if configured) |
| `last_activity` | string | ISO timestamp of last modification |
| `overdue_count` | int | Number of overdue tasks |
| `{Column Name}` | int | Task count per column (dynamic) |

**Dynamic Column Attributes**:

The project sensor includes a task count for each column in the project. Column names are used as attribute keys.

Example for a project with columns "Backlog", "In Progress", "Done":
```json
{
  "id": 1,
  "project_name": "My Project",
  "Backlog": 5,
  "In Progress": 3,
  "Done": 12,
  "overdue_count": 1
}
```

---

## Entity Naming Convention

All entities follow this naming pattern:

```
sensor.hakboard_{instance_key}_{entity_type}_{identifier}
```

| Component | Description | Example |
|-----------|-------------|---------|
| `hakboard` | Integration domain | `hakboard` |
| `{instance_key}` | Unique instance identifier | `hl`, `work`, `personal` |
| `{entity_type}` | Type of entity | `summary`, `system`, `project` |
| `{identifier}` | Specific identifier | `projects_total`, `status`, `1` |

**Examples**:
- `sensor.hakboard_hl_summary_projects_total`
- `sensor.hakboard_hl_system_status`
- `sensor.hakboard_hl_project_1`
- `sensor.hakboard_work_summary_users`

---

## Device Grouping

All sensors for a single Kanboard instance are grouped under one device with the identifier:

```
(hakboard, {instance_key})
```

This allows you to view all entities for an instance together in the Home Assistant UI.
