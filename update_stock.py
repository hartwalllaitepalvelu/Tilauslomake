import re

print("DEBUG: Python start OK")

# --- LUE SAP-RAPORTTI ---
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

# --- LUE DATA.TXT JA POIMI SALLITUT MATERIAALINUMEROT ---
valid_materials = set()

material_number_regex = re.compile(r"^[A-Z]?\d{5,6}$")

try:
    with open("data.txt", "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                continue

            # Ota ensimmäinen sana
            first = line.split()[0].strip()

            # Poista kaikki näkymättömät merkit
            first = first.replace("\u200b", "").replace("\ufeff", "").strip()

            # Jos näyttää materiaalinumerolta → lisää sallittuihin
            if material_number_regex.match(first):
                valid_materials.add(first)

except FileNotFoundError:
    print("ERROR: data.txt puuttuu!")

print(f"DEBUG: data.txt materiaalinumeroita: {len(valid_materials)}")
print(f"DEBUG: valid_materials: {sorted(valid_materials)}")

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

material_line_regex = re.compile(r"^\|(\w{5,6})\s{2,}")
qty_line_regex = re.compile(r"^\|\s*([\d\.]+)\s+ST")

for raw in lines:
    line = raw.rstrip("\n")

    # Ohita viivarivit
    if line.startswith("-"):
        current_material = None
        continue

    # Nimikerivi
    mat_match = material_line_regex.match(line)
    if mat_match:
        current_material = mat_match.group(1).strip()
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

print(f"DEBUG: SAP:sta löytyi nimikkeitä: {len(stocks)}")

# --- SUODATA VAIN DATA.TXT:N MATERIAALIT ---
filtered_stocks = {}

for material, qty in stocks.items():
    if material.strip() in valid_materials:
        filtered_stocks[material] = qty

print(f"DEBUG: Suodatettuja nimikkeitä: {len(filtered_stocks)}")

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
