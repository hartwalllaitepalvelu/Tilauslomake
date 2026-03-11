import re

print("DEBUG: Python start OK")

# --- LUE SAP-RAPORTTI ---
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

# --- LUE DATA.TXT JA RAKENNA KATEGORIAT ---
categories = {}
current_category = None

# Regex materiaalinumerolle:
# 10029
# T49212
# V02387
# 272229
material_number_regex = re.compile(r"^[A-Z]?\d{5,6}$")

try:
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            first = parts[0]

            # Jos ensimmäinen sana on materiaalinumero → nimike
            if material_number_regex.match(first):
                material = first
                if current_category:
                    categories[current_category].append(material)
                continue

            # Muuten → kategoria
            current_category = line
            categories[current_category] = []

except FileNotFoundError:
    print("ERROR: data.txt puuttuu!")

# Luo lista kaikista sallituista materiaaleista
valid_materials = {m for mats in categories.values() for m in mats}

print(f"DEBUG: Kategorioita: {len(categories)}")
print(f"DEBUG: Sallittuja nimikkeitä: {len(valid_materials)}")

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

# Nimikerivi: |10029  POST-MIX...
material_line_regex = re.compile(r"^\|(\w{5,6})\s{2,}")

# Määrärivi: |      2  ST
qty_line_regex = re.compile(r"^\|\s*([\d\.]+)\s+ST")

for line in lines:
    line = line.rstrip("\n")

    # Ohita viivarivit
    if line.startswith("-"):
        current_material = None
        continue

    # Nimikerivi
    mat_match = material_line_regex.match(line)
    if mat_match:
        current_material = mat_match.group(1)
        continue

    # Määrärivi
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
