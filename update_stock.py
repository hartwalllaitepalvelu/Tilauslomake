import re

print("DEBUG: Python start OK")

# Lue SAP-raportti
with open("sap_report.txt", "r", encoding="latin-1") as f:
    lines = f.readlines()

stocks = {}
current_material = None

# Regex nimikeriveille:
# |T00736 ...
# |V48923 ...
# |10029 ...
material_line_regex = re.compile(r"^\|[TV]?\d{5}\s{2,}")

# Regex määräriville:
# |01        3  ST
qty_line_regex = re.compile(r"^\|01\s+([\d\.,]+)\s+ST")

for line in lines:
    line = line.rstrip("\n")

    # Ohita Total-rivit ja muut yhteenvedot
    if "Total" in line:
        current_material = None
        continue

    # Tunnista nimikerivi
    if material_line_regex.match(line):
        # Ota materiaalinumero (esim. T00736 tai 10029)
        current_material = line[1:7].strip()
        continue

    # Tunnista määrärivi
    qty_match = qty_line_regex.match(line)
    if qty_match and current_material:
        qty = qty_match.group(1).replace(",", ".")
        try:
            stocks[current_material] = float(qty)
        except ValueError:
            print(f"WARNING: Ei voitu muuntaa määrää numeroksi: {qty} (materiaalille {current_material})")
        current_material = None

# Tulosta lopputulos
print("=== PARSED STOCKS ===")
for material, qty in stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
