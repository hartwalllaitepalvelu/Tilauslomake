import re

print("DEBUG: Python start OK")

# --- LUE SAP-RAPORTTI ---
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

# --- LUE DATA.TXT (nimikelista) ---
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        valid_materials = {line.strip() for line in f if line.strip()}
except FileNotFoundError:
    print("ERROR: data.txt puuttuu!")
    valid_materials = set()

print(f"DEBUG: data.txt sisältää {len(valid_materials)} nimikettä")

stocks = {}
current_material = None

# Regex nimikeriveille
material_line_regex = re.compile(r"^\|[TV]?\d{5}\s{2,}")

# Regex määräriville
qty_line_regex = re.compile(r"^\|01\s+([\d\.,]+)\s+ST")

for line in lines:
    line = line.rstrip("\n")

    # Ohita Total-rivit
    if "Total" in line:
        current_material = None
        continue

    # Nimikerivi
    if material_line_regex.match(line):
        current_material = line[1:7].strip()
        continue

    # Määrärivi
    qty_match = qty_line_regex.match(line)
    if qty_match and current_material:
        qty = qty_match.group(1).replace(",", ".")
        try:
            stocks[current_material] = float(qty)
        except ValueError:
            print(f"WARNING: Ei voitu muuntaa määrää numeroksi: {qty} (materiaalille {current_material})")
        current_material = None

# --- SUODATA VAIN DATA.TXT:N NIMIKKEET ---
filtered_stocks = {m: q for m, q in stocks.items() if m in valid_materials}

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
print("DEBUG: SAP materials:", list(stocks.keys()))
print("DEBUG: data.txt materials:", valid_materials)
