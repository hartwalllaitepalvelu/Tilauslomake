import re

print("DEBUG: Python start OK")

# Lue SAP-raportti
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

stocks = {}
current_material = None

# Nimikerivi: |10029  POST-MIX...
material_line_regex = re.compile(r"^\|(\d{5})\s{2,}")

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

# Tulosta tulos
print("=== PARSED STOCKS ===")
for material, qty in stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
