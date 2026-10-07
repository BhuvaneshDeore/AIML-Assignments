"""
Maintenance Service Layer Module
Ranks and prioritizes open maintenance issues using a multi-factor risk scoring formula.
"""

from typing import Dict, List, Any
from facility_service import load_json_data


class MaintenanceService:
    """Calculates maintenance priorities based on safety, reliability, energy, and criticality."""

    def prioritize_maintenance(self) -> Dict[str, Any]:
        """
        Ranks maintenance issues by calculating a transparent priority score.

        Priority Score Formula:
            priority_score = (safety_risk * 0.35) + (reliability_risk * 0.25) +
                             (energy_impact * 0.25) + ((criticality * 2) * 0.15)

        Score Range: 1.0 (Lowest Priority) to 10.0 (Highest Priority)

        Returns:
            Dict[str, Any]: Ranked maintenance work orders with priority ranks and scores.
        """
        maintenance_data = load_json_data("maintenance.json")
        equipment_data = load_json_data("equipment.json")

        eq_map = {eq.get("equipment_id"): eq for eq in equipment_data}

        ranked_issues = []
        for issue in maintenance_data:
            if issue.get("status") not in ["OPEN", "IN_PROGRESS"]:
                continue

            eq_id = issue.get("equipment_id")
            eq_info = eq_map.get(eq_id, {})

            safety_risk = float(issue.get("safety_risk", 5))
            reliability_risk = float(issue.get("reliability_risk", 5))
            energy_impact = float(issue.get("energy_impact", 5))
            criticality = float(issue.get("criticality", eq_info.get("criticality", 3)))
            normalized_criticality = criticality * 2.0  # Convert 1-5 scale to 1-10 scale

            # Calculate multi-factor weighted priority score
            priority_score = round(
                (safety_risk * 0.35) +
                (reliability_risk * 0.25) +
                (energy_impact * 0.25) +
                (normalized_criticality * 0.15),
                2
            )

            # Generate justification reason
            reasons = []
            if safety_risk >= 7:
                reasons.append(f"High Safety Risk ({safety_risk}/10)")
            if reliability_risk >= 8:
                reasons.append(f"High Equipment Failure Risk ({reliability_risk}/10)")
            if energy_impact >= 8:
                reasons.append(f"High Energy Waste ({energy_impact}/10)")
            if not reasons:
                reasons.append("Routine maintenance inspection and service required.")

            ranked_issues.append({
                "issue_id": issue.get("issue_id"),
                "equipment_id": eq_id,
                "building": issue.get("building", eq_info.get("building")),
                "description": issue.get("description"),
                "severity": issue.get("severity"),
                "status": issue.get("status"),
                "estimated_cost_usd": issue.get("estimated_cost"),
                "priority_score": priority_score,
                "score_breakdown": {
                    "safety_risk_score": safety_risk,
                    "reliability_risk_score": reliability_risk,
                    "energy_impact_score": energy_impact,
                    "criticality_score": criticality
                },
                "priority_reason": "; ".join(reasons)
            })

        # Sort from highest priority score to lowest
        ranked_issues.sort(key=lambda x: x["priority_score"], reverse=True)

        # Assign ordinal ranks (Rank 1, Rank 2, ...)
        for index, item in enumerate(ranked_issues, start=1):
            item["priority_rank"] = index

        return {
            "status": "success",
            "scoring_formula": "Priority Score = (Safety * 0.35) + (Reliability * 0.25) + (Energy * 0.25) + ((Criticality * 2) * 0.15)",
            "total_open_issues": len(ranked_issues),
            "prioritized_maintenance_list": ranked_issues
        }
