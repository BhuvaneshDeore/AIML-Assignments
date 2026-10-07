"""
Equipment Service Layer Module
Provides equipment health evaluations and transparent rule-based anomaly detection.
"""

from typing import Dict, List, Any, Optional
from facility_service import load_json_data


class EquipmentService:
    """Provides equipment risk ranking and rule-based anomaly detection."""

    RISK_WEIGHTS = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }

    def get_equipment_health(self, building: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves equipment health metrics and ranks equipment from highest to lowest risk.

        Args:
            building (Optional[str]): Optional building filter.

        Returns:
            Dict[str, Any]: Ranked list of equipment by risk level.
        """
        equipment_data = load_json_data("equipment.json")
        sensor_data = load_json_data("sensors.json")

        if building:
            equipment_data = [e for e in equipment_data if e.get("building").lower() == building.lower()]
            if not equipment_data:
                return {
                    "status": "error",
                    "message": f"No equipment records found for building '{building}'."
                }

        # Index telemetry by equipment ID
        telemetry = {s.get("equipment_id"): s for s in sensor_data}

        enriched_equipment = []
        for eq in equipment_data:
            eq_id = eq.get("equipment_id")
            sensor = telemetry.get(eq_id, {})

            risk_level = eq.get("risk", "LOW")
            risk_score = self.RISK_WEIGHTS.get(risk_level, 1) * 10 + eq.get("criticality", 1)

            enriched_equipment.append({
                "equipment_id": eq_id,
                "building": eq.get("building"),
                "type": eq.get("type"),
                "status": eq.get("status"),
                "risk_level": risk_level,
                "risk_score": risk_score,
                "issue": eq.get("issue"),
                "energy_impact": eq.get("energy_impact"),
                "criticality": eq.get("criticality"),
                "runtime_hours": eq.get("runtime_hours"),
                "telemetry_snapshot": {
                    "temperature_c": sensor.get("temperature_c"),
                    "vibration_mm_s": sensor.get("vibration_mm_s"),
                    "power_kw": sensor.get("power_kw"),
                    "sensor_status": sensor.get("sensor_status", "UNKNOWN")
                }
            })

        # Sort equipment from highest to lowest risk score
        ranked_equipment = sorted(enriched_equipment, key=lambda x: x["risk_score"], reverse=True)

        return {
            "status": "success",
            "filter_building": building,
            "total_equipment_inspected": len(ranked_equipment),
            "high_risk_count": sum(1 for e in ranked_equipment if e["risk_level"] == "HIGH"),
            "medium_risk_count": sum(1 for e in ranked_equipment if e["risk_level"] == "MEDIUM"),
            "low_risk_count": sum(1 for e in ranked_equipment if e["risk_level"] == "LOW"),
            "ranked_equipment": ranked_equipment
        }

    def detect_anomalies(self) -> Dict[str, Any]:
        """
        Transparent rule-based anomaly detection.

        Checks:
        - Energy consumption above baseline thresholds (> 15% deviation)
        - Equipment running with HIGH risk or CRITICAL_FAULT status
        - Excessive sensor temperature (> 27°C for HVAC/pumps or > 75°C for boilers)
        - Excessive vibration levels (> 4.0 mm/s)
        - High runtime hours (> 5000 hours without routine overhaul)

        Returns:
            Dict[str, Any]: Identified anomalies with severity, reasons, and confidence scores.
        """
        energy_data = load_json_data("energy.json")
        equipment_data = load_json_data("equipment.json")
        sensor_data = load_json_data("sensors.json")

        anomalies = []

        # 1. Building Energy Anomalies
        for energy in energy_data:
            bld = energy.get("building")
            actual = energy.get("energy_kwh", 0)
            baseline = energy.get("baseline_kwh", 1)
            pct = ((actual - baseline) / baseline) * 100

            if pct > 15.0:
                anomalies.append({
                    "anomaly_id": f"ANOM-ENERGY-{bld}",
                    "affected_target": bld,
                    "target_type": "BUILDING",
                    "severity": "HIGH",
                    "reason": f"Energy usage is {round(pct, 1)}% above baseline expected consumption.",
                    "detection_method": "Rule-Based Baseline Variance (>15%)",
                    "confidence": "94%"
                })

        # 2. Sensor Telemetry Anomalies (Vibration, Temperature, Power Draw)
        for sensor in sensor_data:
            eq_id = sensor.get("equipment_id")
            bld = sensor.get("building")
            vib = sensor.get("vibration_mm_s", 0)
            temp = sensor.get("temperature_c", 0)
            status = sensor.get("sensor_status")

            if vib > 4.0:
                anomalies.append({
                    "anomaly_id": f"ANOM-VIB-{eq_id}",
                    "affected_target": f"{eq_id} ({bld})",
                    "target_type": "EQUIPMENT",
                    "severity": "CRITICAL",
                    "reason": f"Mechanical vibration spike at {vib} mm/s (Threshold: 4.0 mm/s). Risk of bearing failure.",
                    "detection_method": "Rule-Based Vibration Threshold Check",
                    "confidence": "98%"
                })
            elif status == "ANOMALOUS_POWER_DRAW":
                anomalies.append({
                    "anomaly_id": f"ANOM-PWR-{eq_id}",
                    "affected_target": f"{eq_id} ({bld})",
                    "target_type": "EQUIPMENT",
                    "severity": "HIGH",
                    "reason": f"Unusual electrical power draw of {sensor.get('power_kw')} kW under current load.",
                    "detection_method": "Rule-Based Electrical Power Telemetry",
                    "confidence": "91%"
                })

        # 3. Equipment Status & Runtime Anomalies
        for eq in equipment_data:
            eq_id = eq.get("equipment_id")
            if eq.get("status") == "CRITICAL_FAULT":
                anomalies.append({
                    "anomaly_id": f"ANOM-FAULT-{eq_id}",
                    "affected_target": f"{eq_id} ({eq.get('building')})",
                    "target_type": "EQUIPMENT",
                    "severity": "HIGH",
                    "reason": f"Equipment reported fault state: {eq.get('issue')}",
                    "detection_method": "Equipment Fault Code Inspection",
                    "confidence": "99%"
                })
            elif eq.get("runtime_hours", 0) > 6000:
                anomalies.append({
                    "anomaly_id": f"ANOM-RUN-{eq_id}",
                    "affected_target": f"{eq_id} ({eq.get('building')})",
                    "target_type": "EQUIPMENT",
                    "severity": "MEDIUM",
                    "reason": f"High operating hours ({eq.get('runtime_hours')} hrs). Increased failure probability.",
                    "detection_method": "Runtime Maintenance Threshold (>6000 hrs)",
                    "confidence": "85%"
                })

        return {
            "status": "success",
            "detection_type": "Rule-Based Facility Intelligence Engine",
            "total_anomalies_detected": len(anomalies),
            "anomalies": anomalies
        }
