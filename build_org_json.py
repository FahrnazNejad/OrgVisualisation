import json
from collections import defaultdict


INPUT_FILE = "employees_raw.json"
OUTPUT_FILE = "employees_hierarchy.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    employees = json.load(f)

# lookup: userId -> raw employee (for manager email, etc.)
emp_by_id = {e.get("userId"): e for e in employees}

root = {
    "name": "Company Organization",
    "level": "company",
    "children": []
}

# group structure:
# portfolio -> value_stream -> art -> team -> list[employees]
grouped = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(list)
        )
    )
)

for emp in employees:
    portfolio = emp.get("custom_66bb4781e4736654749e352d") or "Unassigned Portfolio"
    vs        = emp.get("custom_66bb4829e4736654749f2e55") or "Unassigned Value Stream"
    art       = emp.get("custom_66bb489ee4736654749fc6b4") or "Unassigned ART"
    team      = emp.get("custom_66c5ce5d8f12f9a7dd0c4f95") or "Unassigned Team"

    grouped[portfolio][vs][art][team].append(emp)

for portfolio, vs_dict in grouped.items():
    portfolio_node = {
        "name": portfolio,
        "level": "portfolio",
        "children": []
    }

    for vs, art_dict in vs_dict.items():
        vs_node = {
            "name": vs,
            "level": "value_stream",
            "children": []
        }

        for art, team_dict in art_dict.items():
            art_node = {
                "name": art,
                "level": "art",
                "children": []
            }

            for team, people in team_dict.items():
                team_node = {
                    "name": team,
                    "level": "product_team",
                    "children": []
                }

                for emp in people:
                    manager_id = emp.get("manager_id")
                    manager = emp_by_id.get(manager_id) if manager_id else None

                    person_node = {
                        "name": emp.get("displayName"),
                        "level": "person",
                        "userId": emp.get("userId"),
                        "manager_id": manager_id,
                        "title": emp.get("title"),
                        "role": emp.get("custom_672b20f1eb514012f7443658"),
                        "department": emp.get("department"),
                        "location": emp.get("workLocation"),
                        "productTeam": team,
                        "managerEmail": manager.get("email") if manager else None,
                    }
                    team_node["children"].append(person_node)

                art_node["children"].append(team_node)
            vs_node["children"].append(art_node)
        portfolio_node["children"].append(vs_node)

    root["children"].append(portfolio_node)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(root, f, ensure_ascii=False, indent=2)
