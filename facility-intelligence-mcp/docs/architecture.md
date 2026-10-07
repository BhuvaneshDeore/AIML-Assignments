# Facility Intelligence MCP Server Architecture

## Overview
The **Facility Intelligence MCP Server** is an independent educational prototype designed to demonstrate how Large Language Model (LLM) agents can analyze simulated facility infrastructure, detect energy anomalies, prioritize maintenance work orders, and model control actions safely using the Model Context Protocol (MCP).

---

## Architectural Layers

```
User (Facility Manager)
        │
        ▼
   AI Agent (Claude / LLM Host)
        │
        ▼  [MCP JSON-RPC / Stdio Protocol]
┌─────────────────────────────────────────────────────────┐
│              Facility Intelligence MCP Server           │
│                                                         │
│   ├── MCP Tools (6 Tools)                               │
│   │   ├── get_facility_status()                         │
│   │   ├── analyze_energy_usage()                        │
│   │   ├── detect_anomalies()                            │
│   │   ├── get_equipment_health()                        │
│   │   ├── prioritize_maintenance()                      │
│   │   └── simulate_action()                             │
│   │                                                     │
│   ├── MCP Resource (1 Resource)                         │
│   │   └── facility://summary                            │
│   │                                                     │
│   └── MCP Prompt (1 Prompt)                             │
│       └── facility_analysis                             │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌─────────────────┐   ┌──────────────┐
│  Data Layer  │   │ Analysis Engine │   │ Simulation   │
│ (data/*.json)│   │ (Rule-Based)    │   │ Layer (Virtual)
└──────────────┘   └─────────────────┘   └──────────────┘
```

---

## Core Components

### 1. AI Agent
The reasoning and interaction engine (e.g., Claude Desktop, FastMCP Inspector). The agent processes human requests, decides which MCP primitives to invoke, interprets returned JSON structures, and presents recommendations to the facility manager.

### 2. MCP Server (`server.py`)
The communication gateway exposing MCP tools, resources, and prompts over standard input/output (Stdio) via JSON-RPC. It translates incoming tool calls into internal Python service calls.

### 3. MCP Tools (6 Primitives)
- **`get_facility_status()`**: Aggregates facility-wide summary indicators.
- **`analyze_energy_usage()`**: Evaluates baseline vs. actual energy consumption and calculates percentage deviations.
- **`detect_anomalies()`**: Runs transparent rule checks for energy spikes, sensor vibration thresholds, and hardware faults.
- **`get_equipment_health()`**: Ranks equipment by health risk indices.
- **`prioritize_maintenance()`**: Applies a multi-factor formula to rank open maintenance work orders.
- **`simulate_action()`**: Mathematically models the thermal and energy impact of proposed actions without touching physical hardware.

### 4. MCP Resource (`facility://summary`)
A passive, read-only endpoint providing an instant text snapshot of facility health metrics.

### 5. MCP Prompt (`facility_analysis`)
A standardized 8-step operating procedure instructing the AI agent on systematic facility diagnosis and safety constraints.

### 6. Facility Data Layer (`data/*.json`)
Simulated facility state stored in structured JSON files:
- `energy.json`: Building energy consumption, baselines, and peak loads.
- `equipment.json`: Equipment inventory, status, runtime hours, and criticality.
- `maintenance.json`: Work order tickets with safety, reliability, and energy scores.
- `sensors.json`: Real-time telemetry (temperature, vibration, power draw).

### 7. Analysis Layer (`energy_service.py`, `equipment_service.py`, `maintenance_service.py`)
Encapsulates transparent rule-based logic to process data, calculate variance, evaluate risk scores, and compute maintenance priorities.

### 8. Simulation Layer (`simulation_service.py`)
Virtual modeling engine that estimates energy savings (e.g., Fan Affinity Laws, Chilled Water Reset, Setpoint adjustments) without modifying physical hardware.

### 9. Safety Layer (Human-in-the-Loop)
Guarantees that the AI agent operates strictly in a decision-support role. The system intentionally **omits** any `execute_action()` tool to prevent autonomous physical control.

---

## Example Request Flow

1. **User Request**: *"Why did Building A use more electricity today?"*
2. **AI Reasoning**: Agent calls `analyze_energy_usage(building="Building-A")`.
3. **MCP Tool Invocation**: `server.py` dispatches request to `energy_service.py`.
4. **Data Retrieval & Analysis**: `energy_service.py` reads `energy.json` and `equipment.json`, calculates a `+24.2%` deviation from baseline, and identifies degraded equipment (`RTU-3` compressor short cycling).
5. **JSON Response**: Server returns structured JSON payload to the AI Agent.
6. **Follow-up Simulation**: User asks: *"What if we increase RTU-3 cooling setpoint by 1°C?"*
7. **Simulation Tool**: Agent calls `simulate_action(equipment_id="RTU-3", action="increase_cooling_setpoint", value=1.0)`.
8. **Virtual Estimate**: `simulation_service.py` calculates an estimated 4.2% cooling reduction (1.63 kW savings) and cautions that compressor maintenance is required first.
9. **Final Recommendation**: AI presents analysis and recommendation to the facility manager for human review and sign-off.
