import json
import pandas as pd

# 1. Load HRIS-style flat JSON
with open("employees_hris.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 2. Rename columns to simpler internal names
df = df.rename(columns={
    "employee_id": "pnumber",
    "first_name": "first_name",
    "last_name": "last_name",
    "work_email": "email",
    "work_phone": "phone",
    "manager_id": "manager_pnumber",
    "department": "portfolio",
    "job_title": "role"
})

# 3. Build node dict for each employee
employees = {
    row.pnumber: {
        "name": f"{row.first_name} {row.last_name}",
        "PNumber": row.pnumber,
        "email": row.email,
        "phone": row.phone,
        "location": row.location,
        "portfolio": row.portfolio,
        "role": row.role,
        "children": []
    }
    for _, row in df.iterrows()
}

# 4. Link managers to their direct reports and find roots
roots = []
for _, row in df.iterrows():
    emp_id = row.pnumber
    mgr_id = row.manager_pnumber

    if pd.isna(mgr_id) or mgr_id is None or str(mgr_id) not in employees:
        roots.append(employees[emp_id])
    else:
        employees[str(mgr_id)]["children"].append(employees[emp_id])

# 5. Compute "value" (size) for circle packing
def add_values(node):
    if not node["children"]:
        node["value"] = 1
        return 1
    total = 0
    for child in node["children"]:
        total += add_values(child)
    node["value"] = total
    return total

org_tree = {"name": "Organization", "children": roots}
add_values(org_tree)

# 6. Save hierarchy JSON for D3
with open("employees_hierarchy.json", "w", encoding="utf-8") as f:
    json.dump(org_tree, f, ensure_ascii=False, indent=2)
