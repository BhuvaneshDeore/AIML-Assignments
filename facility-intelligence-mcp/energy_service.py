"""
Energy Service Layer Module
Analyzes energy consumption metrics against baseline standards.
"""

from typing import Dict, List, Any, Optional
from facility_service import load_json_data


class EnergyService:
    """Provides energy analysis and baseline deviation calculations."""

    def analyze_energy_usage(self, building: Optional[str] = None) -> Dict[str, Any]:
        """
        Compares actual energy consumption against baseline expectations.

        Calculates:
            difference = actual - baseline
            percentage_change = ((actual - baseline) / baseline) * 100

        Args:
            building (Optional[str]): Target building filter (e.g. 'Building-A').

        Returns:
            Dict[str, Any]: Energy analysis breakdown per building.
        """
        energy_data = load_json_data("energy.json")
        equipment_data = load_json_data("equipment.json")

        if building:
            filtered = [e for e in energy_data if e.get("building").lower() == building.lower()]
            if not filtered:
                return {
                    "status": "error",
                    "message": f"Building '{building}' not found in energy records. Available buildings: " +
                               ", ".join(list({e.get('building') for e in energy_data}))
                }
            energy_records = filtered
        else:
            energy_records = energy_data

        analysis_results = []
        total_actual = 0.0
        total_baseline = 0.0

        for record in energy_records:
            bld = record.get("building")
            actual = record.get("energy_kwh", 0.0)
            baseline = record.get("baseline_kwh", 1.0)  # Avoid division by zero
            peak = record.get("peak_kwh", 0.0)

            difference = round(actual - baseline, 2)
            percentage_change = round(((actual - baseline) / baseline) * 100, 2)

            total_actual += actual
            total_baseline += baseline

            # Identify contributing factors from equipment status
            bld_equipment = [eq for eq in equipment_data if eq.get("building") == bld]
            faulty_equipment = [
                f"{eq.get('equipment_id')} ({eq.get('issue')})"
                for eq in bld_equipment if eq.get("risk") in ["HIGH", "MEDIUM"]
            ]

            status = "OPTIMAL"
            reasons = []
            if percentage_change > 15.0:
                status = "CRITICAL_EXCESS"
                reasons.append(f"Consumption exceeds baseline by {percentage_change}%.")
                if faulty_equipment:
                    reasons.append(f"Potential equipment faults: {', '.join(faulty_equipment)}")
            elif percentage_change > 5.0:
                status = "MODERATE_EXCESS"
                reasons.append(f"Consumption is {percentage_change}% above baseline.")
                if faulty_equipment:
                    reasons.append(f"Degraded equipment detected: {', '.join(faulty_equipment)}")
            elif percentage_change < -5.0:
                status = "HIGH_EFFICIENCY"
                reasons.append(f"Consumption is {abs(percentage_change)}% below baseline threshold.")
            else:
                status = "ON_PAR"
                reasons.append("Energy consumption matches expected baseline expectations.")

            analysis_results.append({
                "building": bld,
                "actual_energy_kwh": actual,
                "baseline_energy_kwh": baseline,
                "peak_energy_kwh": peak,
                "difference_kwh": difference,
                "percentage_change": percentage_change,
                "status": status,
                "possible_reasons": reasons
            })

        overall_diff = round(total_actual - total_baseline, 2)
        overall_pct = round(((total_actual - total_baseline) / total_baseline) * 100, 2) if total_baseline > 0 else 0.0

        return {
            "status": "success",
            "filter_building": building,
            "overall_summary": {
                "total_actual_kwh": round(total_actual, 2),
                "total_baseline_kwh": round(total_baseline, 2),
                "overall_difference_kwh": overall_diff,
                "overall_percentage_change": overall_pct
            },
            "building_analysis": analysis_results
        }
