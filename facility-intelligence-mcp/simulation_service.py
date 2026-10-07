"""
Simulation Service Layer Module
Simulates facility control actions in a safe virtual environment without affecting physical hardware.
"""

from typing import Dict, Any, Optional
from facility_service import load_json_data


class SimulationService:
    """Provides safe virtual simulation of proposed facility optimization actions."""

    def simulate_action(self, equipment_id: str, action: str, value: float = 1.0) -> Dict[str, Any]:
        """
        Simulates the estimated thermal, energy, and risk impact of a proposed facility action.

        IMPORTANT SAFETY GUARANTEE:
        This tool NEVER communicates with or alters physical BMS/BAS hardware.
        All calculations are mathematical model estimates for decision support only.

        Args:
            equipment_id (str): Equipment identifier (e.g. 'RTU-3', 'Chiller-1', 'Boiler-2').
            action (str): Proposed action name (e.g. 'increase_cooling_setpoint', 'reduce_fan_speed',
                          'reset_chiller_temp', 'cycle_boiler_standby').
            value (float): Adjustment magnitude (e.g. +1.0°C, -10% fan speed).

        Returns:
            Dict[str, Any]: Simulated energy impact, risk assessment, confidence rating, and safety recommendation.
        """
        equipment_data = load_json_data("equipment.json")
        sensor_data = load_json_data("sensors.json")

        # Find target equipment
        equipment = next((eq for eq in equipment_data if eq.get("equipment_id").lower() == equipment_id.lower()), None)

        if not equipment:
            available_equipment = [eq.get("equipment_id") for eq in equipment_data]
            return {
                "status": "error",
                "message": f"Equipment '{equipment_id}' not found. Available equipment IDs: " + ", ".join(available_equipment)
            }

        sensor = next((s for s in sensor_data if s.get("equipment_id").lower() == equipment_id.lower()), {})
        building = equipment.get("building")
        eq_type = equipment.get("type")
        current_status = equipment.get("status")

        # Action 1: Increase Cooling Setpoint (e.g. +1.0°C or +2.0°C)
        if action.lower() in ["increase_cooling_setpoint", "adjust_setpoint"]:
            energy_reduction_pct = round(value * 4.2, 1)  # ~4.2% energy savings per °C setpoint increase
            
            if current_status == "CRITICAL_FAULT":
                estimated_risk = "HIGH"
                confidence = "82%"
                recommendation = "CAUTION REQUIRED: Equipment has active critical fault. Repair compressor before adjusting setpoints."
            else:
                estimated_risk = "LOW"
                confidence = "92%"
                recommendation = "SAFE TO PROPOSE: Setpoint adjustment reduces compressor load with minimal occupant impact."

            return {
                "status": "success",
                "simulation_type": "SAFE_VIRTUAL_ESTIMATE",
                "hardware_modified": False,
                "target_equipment": equipment_id,
                "building": building,
                "proposed_action": f"Increase cooling setpoint by {value}°C",
                "expected_energy_impact": f"-{energy_reduction_pct}% building cooling load",
                "estimated_power_savings_kw": round((sensor.get("power_kw", 20.0) * (energy_reduction_pct / 100.0)), 2),
                "estimated_risk": estimated_risk,
                "confidence_score": confidence,
                "safety_recommendation": recommendation,
                "notes": "Simulated estimate. Requires facility manager sign-off prior to BAS execution."
            }

        # Action 2: Reduce Fan Speed (e.g. -10% or -15%)
        elif action.lower() in ["reduce_fan_speed", "vfd_fan_reduction"]:
            # Fan Affinity Law: Power proportional to cube of speed ratio
            energy_reduction_pct = round((1 - ((100 - value) / 100.0) ** 3) * 100, 1)
            
            estimated_risk = "MEDIUM" if value > 20 else "LOW"
            confidence = "89%"
            recommendation = "SAFE TO PROPOSE: VFD fan reduction yields exponential power savings."

            return {
                "status": "success",
                "simulation_type": "SAFE_VIRTUAL_ESTIMATE",
                "hardware_modified": False,
                "target_equipment": equipment_id,
                "building": building,
                "proposed_action": f"Reduce fan VFD speed by {value}%",
                "expected_energy_impact": f"-{energy_reduction_pct}% fan power consumption",
                "estimated_power_savings_kw": round((sensor.get("power_kw", 15.0) * (energy_reduction_pct / 100.0)), 2),
                "estimated_risk": estimated_risk,
                "confidence_score": confidence,
                "safety_recommendation": recommendation,
                "notes": "Simulated affinity law calculation. Check duct static pressure."
            }

        # Action 3: Reset Chiller Water Temperature
        elif action.lower() in ["reset_chiller_temp", "chiller_reset"]:
            energy_reduction_pct = round(value * 2.5, 1)
            estimated_risk = "LOW" if current_status == "OPERATIONAL" else "MEDIUM"
            confidence = "94%"
            recommendation = "SAFE TO PROPOSE: Chilled water reset improves chiller efficiency."

            return {
                "status": "success",
                "simulation_type": "SAFE_VIRTUAL_ESTIMATE",
                "hardware_modified": False,
                "target_equipment": equipment_id,
                "building": building,
                "proposed_action": f"Reset chilled water supply temperature by +{value}°C",
                "expected_energy_impact": f"-{energy_reduction_pct}% chiller power draw",
                "estimated_power_savings_kw": round((sensor.get("power_kw", 100.0) * (energy_reduction_pct / 100.0)), 2),
                "estimated_risk": estimated_risk,
                "confidence_score": confidence,
                "safety_recommendation": recommendation,
                "notes": "Simulated estimate. Verify space humidity limits."
            }

        # Fallback / General Action
        else:
            return {
                "status": "success",
                "simulation_type": "SAFE_VIRTUAL_ESTIMATE",
                "hardware_modified": False,
                "target_equipment": equipment_id,
                "building": building,
                "proposed_action": f"{action} (value={value})",
                "expected_energy_impact": f"-{round(value * 3.0, 1)}% estimated energy reduction",
                "estimated_risk": "LOW",
                "confidence_score": "85%",
                "safety_recommendation": "SAFE TO PROPOSE: Standard operational optimization proposal.",
                "notes": "Generic simulated estimate."
            }
