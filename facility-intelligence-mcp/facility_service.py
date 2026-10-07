"""
Facility Service Layer Module
Handles loading simulated facility JSON data files and providing high-level facility summary aggregations.
"""

import os
import json
from typing import Dict, List, Any


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_json_data(filename: str) -> List[Dict[str, Any]]:
    """
    Safely loads JSON data from the data/ directory.

    Args:
        filename (str): Name of the JSON file inside data/ (e.g. 'energy.json').

    Returns:
        List[Dict[str, Any]]: Parsed JSON list or empty list if file not found or invalid.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        print(f"[FacilityService Warning] Data file '{file_path}' not found.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[FacilityService Error] Failed to parse '{file_path}': {e}")
        return []


class FacilityService:
    """Provides high-level facility summary metrics and data access."""

    def __init__(self):
        self.data_dir = DATA_DIR

    def get_summary(self) -> Dict[str, Any]:
        """
        Calculates high-level summary statistics across all simulated buildings,
        equipment, energy usage, active anomalies, and open maintenance tickets.

        Returns:
            Dict[str, Any]: Facility status summary dictionary.
        """
        energy_data = load_json_data("energy.json")
        equipment_data = load_json_data("equipment.json")
        maintenance_data = load_json_data("maintenance.json")
        sensor_data = load_json_data("sensors.json")

        # Unique buildings
        buildings = sorted(list({item.get("building") for item in energy_data if item.get("building")}))
        
        # Total energy calculation
        total_energy_kwh = sum(item.get("energy_kwh", 0) for item in energy_data)
        total_baseline_kwh = sum(item.get("baseline_kwh", 0) for item in energy_data)

        # Equipment health counts
        critical_faults = [eq for eq in equipment_data if eq.get("status") in ["CRITICAL_FAULT", "WARNING", "DEGRADED"]]
        
        # Open maintenance tickets
        open_maintenance = [m for m in maintenance_data if m.get("status") in ["OPEN", "IN_PROGRESS"]]

        # Sensor anomalies
        anomalous_sensors = [s for s in sensor_data if s.get("sensor_status") not in ["NORMAL"]]

        return {
            "status": "success",
            "total_buildings": len(buildings),
            "buildings": buildings,
            "total_equipment_monitored": len(equipment_data),
            "total_energy_today_kwh": round(total_energy_kwh, 2),
            "total_baseline_today_kwh": round(total_baseline_kwh, 2),
            "energy_variance_kwh": round(total_energy_kwh - total_baseline_kwh, 2),
            "active_anomalies_count": len(anomalous_sensors),
            "open_maintenance_issues_count": len(open_maintenance),
            "equipment_warnings_count": len(critical_faults),
            "facility_health_index": "DEGRADED" if len(critical_faults) > 3 else "OPTIMAL"
        }
