import re

print("DEBUG: Python start OK")

# --- LUE SAP-RAPORTTI ---
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

# --- LUE DATA.TXT JA RAKENNA KATEGORIAT ---
categories = {}
current_category = None

try:
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Jos rivi EI ala materiaalinumerolla → se on kategoria
            if not re.match(r"^[A-Z]?\d{5}", line):
                current_category = line
                categories[current_category] = []
                continue

            # Muuten rivi on nimike → lisää se nykyiseen kategoriaan
            material = line.split()[0]
            if current_category:
                categories[current_category].append(material)

except FileNotFoundError:
    print("ERROR: data.txt puuttuu!")

# Luo lista kaikista sallituista materiaaleista
valid_materials = {m for mats in categories.values() for m in mats}

print(f"DEBUG: Kategorioita: {len(categories)}")
print(f"DEBUG: Sallittuja nimikkeitä: {len(valid_materials)}")

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

material_line_regex = re.compile(r"^\|(\w{5,6})\s{2,}")
qty_line_regex = re.compile(r"^\|\s*([\d\.]+)\s+ST")

for line in lines:
    line = line.rstrip("\n")

    if line.startswith("-"):
        current_material = None
        continue

    mat_match = material_line_regex.match(line)
    if mat_match:
        current_material = mat_match.group(1)
        continue

    qty_match = qty_line_regex.match(line)
    if qty_match and current_material:
        qty = qty_match.group(1)
        try:
            stocks[current_material] = float(qty)
        except ValueError:
            print(f"WARNING: Ei voitu muuntaa määrää numeroksi: {qty}")
        current_material = None

# --- SUODATA VAIN KATEGORIOIDEN NIMIKKEET ---
filtered_stocks = {m: q for m, q in stocks.items() if m in valid_materials}

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
