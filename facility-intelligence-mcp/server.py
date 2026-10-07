"""
Facility Intelligence MCP Server
AI-Powered Energy Infrastructure Intelligence and Safe Action Framework

Exposes 6 Tools, 1 Resource, and 1 Prompt for simulated facility management.
"""

import json
from typing import Dict, Any, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    from mcp.server.mcpserver import MCPServer as FastMCP

from facility_service import FacilityService
from energy_service import EnergyService
from equipment_service import EquipmentService
from maintenance_service import MaintenanceService
from simulation_service import SimulationService

# Initialize MCP Server instance
mcp = FastMCP("Facility Intelligence MCP Server")

# Instantiate Service Layers
facility_service = FacilityService()
energy_service = EnergyService()
equipment_service = EquipmentService()
maintenance_service = MaintenanceService()
simulation_service = SimulationService()


# ==============================================================================
# 1. MCP TOOLS (6 Tools)
# ==============================================================================

@mcp.tool()
def get_facility_status() -> str:
    """
    Returns a high-level summary of the overall facility status.

    Includes total buildings, total monitored equipment, today's energy usage,
    energy variance from baseline, count of active anomalies, and open maintenance tickets.

    Example Question: "What is the current facility status?"
    """
    try:
        data = facility_service.get_summary()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Failed to fetch facility status: {str(e)}"}, indent=2)


@mcp.tool()
def analyze_energy_usage(building: Optional[str] = None) -> str:
    """
    Compares actual energy consumption against baseline metrics.

    Calculates baseline difference (actual - baseline) and percentage change.
    Provides diagnostic reasons for energy spikes.

    Args:
        building (Optional[str]): Optional building identifier filter (e.g. 'Building-A').

    Example Question: "Why did Building A use more electricity?"
    """
    try:
        data = energy_service.analyze_energy_usage(building=building)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Energy analysis failed: {str(e)}"}, indent=2)


@mcp.tool()
def detect_anomalies() -> str:
    """
    Identifies unusual facility conditions using transparent rule-based detection.

    Checks energy deviations (>15%), sensor vibration spikes (>4.0 mm/s),
    abnormal power draw, and high equipment runtime hours.

    Example Question: "Are there any active anomalies in the facility?"
    """
    try:
        data = equipment_service.detect_anomalies()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Anomaly detection failed: {str(e)}"}, indent=2)


@mcp.tool()
def get_equipment_health(building: Optional[str] = None) -> str:
    """
    Provides equipment health records ranked from highest to lowest risk.

    Args:
        building (Optional[str]): Optional building filter (e.g. 'Building-C').

    Example Question: "Which equipment has the highest risk of failure?"
    """
    try:
        data = equipment_service.get_equipment_health(building=building)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Equipment health check failed: {str(e)}"}, indent=2)


@mcp.tool()
def prioritize_maintenance() -> str:
    """
    Ranks open maintenance work orders using a multi-factor risk scoring formula:
    Priority Score = (Safety Risk * 0.35) + (Reliability Risk * 0.25) +
                     (Energy Impact * 0.25) + ((Criticality * 2) * 0.15)

    Example Question: "Which equipment should we inspect first?"
    """
    try:
        data = maintenance_service.prioritize_maintenance()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Maintenance prioritization failed: {str(e)}"}, indent=2)


@mcp.tool()
def simulate_action(equipment_id: str, action: str, value: float = 1.0) -> str:
    """
    Simulates the estimated energy reduction and risk of a proposed facility action.

    IMPORTANT SAFETY GUARANTEE:
    This tool NEVER modifies real physical hardware. It performs virtual mathematical estimates only.

    Args:
        equipment_id (str): Target equipment ID (e.g. 'RTU-3', 'Chiller-1').
        action (str): Action name (e.g. 'increase_cooling_setpoint', 'reduce_fan_speed', 'reset_chiller_temp').
        value (float): Adjustment magnitude (default: 1.0).

    Example Question: "What happens if we increase the cooling setpoint of RTU-3 by 1°C?"
    """
    try:
        data = simulation_service.simulate_action(equipment_id=equipment_id, action=action, value=value)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Simulation failed: {str(e)}"}, indent=2)


# ==============================================================================
# 2. MCP RESOURCE (1 Resource)
# ==============================================================================

@mcp.resource("facility://summary")
def get_facility_summary_resource() -> str:
    """
    Read-only resource providing a concise facility summary snapshot.

    URI: facility://summary
    """
    try:
        summary = facility_service.get_summary()
        output = (
            "Facility Summary Snapshot\n"
            "-------------------------\n"
            f"Buildings Monitored: {summary.get('total_buildings')}\n"
            f"Equipment Records: {summary.get('total_equipment_monitored')}\n"
            f"Energy Today: {summary.get('total_energy_today_kwh'):,} kWh\n"
            f"Baseline Expected: {summary.get('total_baseline_today_kwh'):,} kWh\n"
            f"Active Anomalies: {summary.get('active_anomalies_count')}\n"
            f"Open Maintenance Issues: {summary.get('open_maintenance_issues_count')}\n"
            f"Equipment Warnings: {summary.get('equipment_warnings_count')}\n"
            f"Facility Health Index: {summary.get('facility_health_index')}\n"
        )
        return output
    except Exception as e:
        return f"Error loading facility summary resource: {str(e)}"


# ==============================================================================
# 3. MCP PROMPT (1 Prompt)
# ==============================================================================

@mcp.prompt("facility_analysis")
def facility_analysis_prompt() -> str:
    """
    Standardized system instructions guiding AI assistants through safe facility intelligence workflows.
    """
    return """
You are an expert AI Facility Intelligence & Energy Operations Assistant.
Follow this 8-step protocol to analyze facility conditions and provide safe optimization recommendations:

1. **Check Facility Status**: Call `get_facility_status()` or read `facility://summary` to review overall metrics.
2. **Analyze Energy Usage**: Call `analyze_energy_usage()` to identify energy spikes and baseline deviations.
3. **Detect Anomalies**: Call `detect_anomalies()` to pinpoint equipment faults, sensor spikes, and runtime anomalies.
4. **Check Equipment Health**: Call `get_equipment_health()` to inspect equipment ranked by failure risk.
5. **Prioritize Maintenance**: Call `prioritize_maintenance()` to review open maintenance work orders ordered by priority score.
6. **Simulate Safe Actions**: When optimization opportunities are identified, call `simulate_action()` to estimate energy savings and risk.
7. **Give Clear Recommendations**: Synthesize your analysis into clear, human-readable insights for facility managers.
8. **NEVER Directly Control Hardware**: Remember that the system provides virtual simulations and decision support only. All physical control actions require explicit human approval and execution.
"""


def main():
    """Server main entrypoint."""
    print("Starting Facility Intelligence MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
