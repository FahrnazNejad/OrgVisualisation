import json
import random

OUTPUT_FILE = "employees_raw.json"

random.seed(42)

first_names = [
    "Liam","Emma","Noah","Mia","Finn","Sophia","Leon","Hannah","Elias","Lina",
    "Gabriel","Chloé","Lucas","Camille","Louis","Manon","Hugo","Léa","Nathan","Zoé",
    "Hugo","Lucía","Mateo","Sofía","Alejandro","María","Pablo","Carmen","Diego","Elena"
]

last_names = [
    "Becker","Wagner","Fischer","Keller","Schneider","Vogel","Hoffmann","Meier","Richter","Brandt",
    "Martin","Bernard","Laurent","Dubois","Moreau","Simon","Fournier","Rousseau","Blanc","Garnier",
    "Lopez","Ramos","Alonso","Cruz","Ruiz","Ortega","Navarro","Santos","Molina","Vega"
]

locations = ["Berlin, Germany", "Paris, France", "Madrid, Spain"]

portfolios = ["Portfolio Customer", "Portfolio Vehicles", "Backbone"]

records = []
next_user_num = 1

def new_user_id():
    global next_user_num
    uid = f"u{next_user_num:04d}"
    next_user_num += 1
    return uid

def random_name():
    return random.choice(first_names), random.choice(last_names)

def make_person(portfolio, value_stream, art, team, dept, role, manager_user_id=None):
    user_id = new_user_id()
    first, last = random_name()
    location = random.choice(locations)

    rec = {
        "userId": user_id,                          # primary employee id
        "externalId": f"EMP-{user_id[1:]}",         # keep externalId for realism
        "active": True,
        "displayName": f"{first} {last}",
        "firstName": first,
        "lastName": last,
        "title": "Engineer" if "Lead" not in role and "Manager" not in role and "Head" not in role and "Architect" not in role else role,
        "department": dept,
        "manager_id": manager_user_id,              # references another userId
        "workLocation": location,
        "custom_672b20f1eb514012f7443658": role,           # Main Role
        "custom_66bb4781e4736654749e352d": portfolio,      # Portfolio
        "custom_66bb4829e4736654749f2e55": value_stream,   # Value Stream
        "custom_66bb489ee4736654749fc6b4": art,            # ART
        "custom_66c5ce5d8f12f9a7dd0c4f95": team            # Product Team
    }
    records.append(rec)
    return user_id

for p_idx, portfolio in enumerate(portfolios):
    dept = portfolio.split()[-1]

    # portfolio head, top of hierarchy (no manager)
    head_uid = make_person(portfolio, None, None, None,
                           dept, role="Portfolio Head", manager_user_id=None)

    # 2–4 value streams
    n_vs = random.randint(2, 4)
    for vs_idx in range(n_vs):
        vs = f"VS {p_idx+1}.{vs_idx+1}"

        # VS lead → portfolio head
        vs_lead_uid = make_person(portfolio, vs, None, None,
                                  dept, role="Value Stream Lead", manager_user_id=head_uid)

        # 2–3 ARTs per value stream
        n_arts = random.randint(2, 3)
        for art_idx in range(n_arts):
            art = f"ART {p_idx+1}.{vs_idx+1}.{art_idx+1}"

            # ART manager → VS lead
            art_manager_uid = make_person(portfolio, vs, art, None,
                                          dept, role="ART Manager", manager_user_id=vs_lead_uid)

            # 2–4 product teams per ART
            n_teams = random.randint(2, 4)
            for team_idx in range(n_teams):
                team = f"Team {p_idx+1}.{vs_idx+1}.{art_idx+1}.{team_idx+1}"

                # team lead → ART manager
                team_lead_uid = make_person(portfolio, vs, art, team,
                                            dept, role="Team Lead", manager_user_id=art_manager_uid)

                # 3–5 members → team lead
                n_people = random.randint(3, 5)
                for _ in range(n_people):
                    make_person(portfolio, vs, art, team,
                                dept, role="Developer", manager_user_id=team_lead_uid)

print(f"Generated {len(records)} employees")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
