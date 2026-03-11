import re

print("DEBUG: start")

# --- LUE DATA.TXT: POIMI MATERIAALINUMEROT ---
valid_materials = set()

with open("data.txt", "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        first = line.split()[0]
        if first[0].isdigit():
            valid_materials.add(first)

print("DEBUG: data.txt nimikkeitä:", len(valid_materials))

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

# rivi, jossa on materiaalinumero + kuvaus (materiaalinumero = ensimmäinen "sana", jossa on numeroita)
material_re = re.compile(r"^\s*(\d+)\s+")
# rivi, jossa on määrä + yksikkö (ST tai SHT)
qty_re = re.compile(r"^\s*([\d.,]+)\s+(ST|SHT)\s*$")

with open("sap_report.txt", "r", encoding="latin-1") as f:
    for raw in f:
        line = raw.rstrip("\n")

        if not line.strip():
            continue

        m_mat = material_re.match(line)
        if m_mat:
            current_material = m_mat.group(1)
            continue

        m_qty = qty_re.match(line)
        if m_qty and current_material:
            qty_str = m_qty.group(1).replace(",", ".")
            try:
                qty = float(qty_str)
                stocks[current_material] = qty
            except ValueError:
                pass
            current_material = None

print("DEBUG: SAP:sta parsittuja nimikkeitä:", len(stocks))

# --- LEIKKAUS: MITKÄ OVAT MOLEMMISSA? ---
common = set(stocks.keys()) & valid_materials
print("DEBUG: Yhteisiä nimikkeitä:", len(common))

# --- TULOSTA VAIN YHTEISET ---
print("=== FILTERED (vain molemmissa olevat) ===")
for material in sorted(common):
    print(material, stocks[material])

print("DEBUG: done")
