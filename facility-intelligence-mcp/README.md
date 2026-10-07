# Facility Intelligence MCP: AI-Powered Energy Infrastructure Intelligence and Safe Action Framework

> ⚠️ **EDUCATIONAL DISCLAIMER**: This project is an independent educational prototype created for learning Model Context Protocol (MCP) concepts inspired by modern facility and energy operations. It is **not** an official product of Edviro and does **not** connect to any proprietary Edviro systems, real Building Management Systems (BMS), or live physical equipment. All data and simulations are 100% synthetic and local.

---

## 1. Project Title
**Facility Intelligence MCP: AI-Powered Energy Infrastructure Intelligence and Safe Action Framework**

---

## 2. Project Overview
The **Facility Intelligence MCP Server** enables Large Language Model (LLM) agents to analyze simulated commercial facility data—such as energy consumption baselines, HVAC equipment health, telemetry sensor streams, and maintenance work orders—and propose safe facility optimization actions without directly controlling physical hardware.

---

## 3. Problem Statement
Commercial buildings consume over 30% of global electricity, with significant energy wasted due to undetected equipment degradation, improper setpoints, and reactive maintenance. While AI agents possess the reasoning capability to spot energy anomalies and recommend setpoint adjustments, giving AI agents direct autonomous control over real physical HVAC equipment, boilers, or electrical systems introduces major safety, security, and liability risks.

---

## 4. Proposed Solution
This framework introduces a **Safe Action Framework** using the Model Context Protocol (MCP):
- **AI Agent**: Analyzes data, reasons about facility conditions, and evaluates options.
- **MCP Server**: Exposes standardized tools, resources, and prompts to the AI agent.
- **Virtual Simulation**: Estimates energy and thermal impacts safely in software.
- **Human-in-the-Loop**: Requires human facility manager approval for any physical execution.

---

## 5. Why MCP is Used
The Model Context Protocol (MCP) provides a standardized, open protocol for connecting AI models to domain-specific tools and data sources. Rather than writing custom ad-hoc prompt logic or proprietary integrations, MCP allows an AI assistant (like Claude Desktop) to discover tools, inspect read-only resources, and execute standardized analysis protocols over a clean JSON-RPC protocol.

---

## 6. Architecture

```text
User (Facility Manager)
        ↓
    AI Agent
        ↓
    MCP Server (server.py)
        ↓
Facility Intelligence Tools (6 Tools)
        ↓
Simulated Facility Data (data/*.json)
        ↓
  Analysis / Simulation Layer
        ↓
   Safety Evaluation
        ↓
 Human Recommendation (Human-in-the-Loop)
```

---

## 7. Features
- 📊 **Facility Status Aggregation**: High-level summary of buildings, energy variance, anomalies, and maintenance.
- ⚡ **Energy Baseline Analysis**: Calculates energy variance (`difference = actual - baseline`) and percentage changes.
- 🔍 **Transparent Rule-Based Anomaly Detection**: Identifies energy spikes, sensor vibration anomalies, and equipment faults without black-box claims.
- 🛠️ **Risk-Ranked Equipment Health**: Ranks facility equipment from highest to lowest failure risk.
- 📋 **Multi-Factor Maintenance Prioritization**: Uses a weighted scoring formula considering safety risk, reliability risk, energy impact, and equipment criticality.
- 🧪 **Safe Virtual Action Simulation**: Models energy savings for setpoint and fan speed adjustments safely in software.

---

## 8. MCP Tools (6 Tools Implemented)

1. `get_facility_status()`: Summary of buildings, energy totals, anomalies, and maintenance tickets.
2. `analyze_energy_usage(building=None)`: Compares actual consumption against baseline expectations.
3. `detect_anomalies()`: Rule-based detection of energy spikes, vibration anomalies, and equipment faults.
4. `get_equipment_health(building=None)`: Equipment health inventory ranked by risk score.
5. `prioritize_maintenance()`: Work order prioritization using a multi-factor risk formula.
6. `simulate_action(equipment_id, action, value=1.0)`: Safely simulates the energy and risk impact of proposed actions.

---

## 9. MCP Resource

### `facility://summary`
- **Type**: Read-Only Resource
- **URI**: `facility://summary`
- **Description**: Returns a clean text snapshot summarizing building counts, energy consumption today, baseline expectations, active anomalies, open maintenance issues, and overall facility health index.

---

## 10. MCP Prompt

### `facility_analysis`
- **Type**: Prompt Template
- **Name**: `facility_analysis`
- **Description**: Standardized 8-step operating procedure guiding AI assistants to systematically check status, analyze energy, detect anomalies, check equipment health, prioritize maintenance, simulate safe actions, and deliver clear human-in-the-loop recommendations.

---

## 11. Data Structure

Simulated facility state resides in `data/`:
- `energy.json`: Building energy readings, baseline kWh, peak kWh, and status.
- `equipment.json`: Equipment inventory (`RTU-1` through `RTU-3`, `Boiler-1`, `Chiller-1`, etc.), risk levels, issues, and criticality ratings.
- `maintenance.json`: Work order tickets (`WO-101` through `WO-107`) with safety, reliability, and energy ratings.
- `sensors.json`: Real-time sensor telemetry (temperature, humidity, power draw, vibration).

---

## 12. Safety / Human-in-the-Loop

```text
AI → MCP → Analysis/Simulation → Safety Check → Recommendation → Human Approval
```

The system intentionally **omits** any physical execution tools (e.g., `execute_action()`). The simulation tool explicitly sets `"hardware_modified": false` and returns clear safety recommendations for human facility managers.

---

## 13. Installation

### Prerequisites
- Python 3.10+
- `pip` package manager

### Clone & Setup
```powershell
cd facility-intelligence-mcp
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

---

## 14. How to Run

Run the MCP server locally over stdio:
```powershell
python server.py
```

---

## 15. MCP Inspector Testing

Test the tools, resource, and prompt interactively using the official MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector python server.py
```

Open `http://localhost:5173` in your browser to inspect tools, resource `facility://summary`, and prompt `facility_analysis`.

---

## 16. Example Questions & Demonstration Flow

1. **Facility Overview**: *"What is the current facility status?"*
   - Uses `get_facility_status()`.
2. **Energy Spike Investigation**: *"Why did Building A consume more electricity?"*
   - Uses `analyze_energy_usage(building="Building-A")` and `detect_anomalies()`.
3. **Equipment Inspection**: *"Which equipment should we inspect first?"*
   - Uses `get_equipment_health()` and `prioritize_maintenance()`.
4. **Safe Action Simulation**: *"What happens if we increase the cooling setpoint of RTU-3 by 1°C?"*
   - Uses `simulate_action(equipment_id="RTU-3", action="increase_cooling_setpoint", value=1.0)`.

---

## 17. Sample Outputs

### Maintenance Prioritization Output
```json
{
  "status": "success",
  "scoring_formula": "Priority Score = (Safety * 0.35) + (Reliability * 0.25) + (Energy * 0.25) + ((Criticality * 2) * 0.15)",
  "total_open_issues": 7,
  "prioritized_maintenance_list": [
    {
      "priority_rank": 1,
      "issue_id": "WO-101",
      "equipment_id": "RTU-3",
      "building": "Building-A",
      "priority_score": 8.45,
      "description": "Compressor short-cycling rapidly causing 35% excess peak electrical power draw.",
      "priority_reason": "High Safety Risk (7.0/10); High Equipment Failure Risk (9.0/10); High Energy Waste (9.0/10)"
    }
  ]
}
```

### Action Simulation Output
```json
{
  "status": "success",
  "simulation_type": "SAFE_VIRTUAL_ESTIMATE",
  "hardware_modified": false,
  "target_equipment": "RTU-3",
  "proposed_action": "Increase cooling setpoint by 1.0°C",
  "expected_energy_impact": "-4.2% building cooling load",
  "estimated_power_savings_kw": 1.63,
  "estimated_risk": "HIGH",
  "safety_recommendation": "CAUTION REQUIRED: Equipment has active critical fault. Repair compressor before adjusting setpoints."
}
```

---

## 18. Limitations
- **Simulated Data Only**: Uses static JSON data snapshots rather than live BACnet/Modbus BAS feeds.
- **Simplified Thermodynamics**: Physics equations use simplified linear and affinity models for educational clarity.

---

## 19. Future Scope
- **BACnet/Modbus Telemetry Connectors**: Read live sensor telemetry from BACnet/IP gateways in read-only mode.
- **Time-Series Forecasting**: Incorporate Prophet or ARIMA models for predictive baseline forecasting.
- **Multi-Building Portfolio Optimization**: Expand heuristics to handle regional building campuses.

---

## 20. Conclusion
The **Facility Intelligence MCP Server** demonstrates how the Model Context Protocol enables AI agents to serve as powerful, safe, human-in-the-loop energy intelligence assistants.
