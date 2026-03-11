import re

print("DEBUG: start")

# --- LUE DATA.TXT: POIMI MATERIAALINUMEROT (ENSIMMÄINEN SANA, JOS NUMEROIN ALKAVA) ---
valid_materials = set()

with open("data.txt", "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        first = line.split()[0]
        # jos ensimmäinen merkki on numero → materiaalirivi
        if first[0].isdigit():
            valid_materials.add(first)

print("DEBUG: data.txt nimikkeitä:", len(valid_materials))

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

# rivi, jossa on materiaalinumero + kuvaus
material_re = re.compile(r"^\s*(\d{5})\s+")
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

# --- SUODATUS: VAIN NE, JOTKA OVAT data.txt:SSÄ ---
filtered_stocks = {
    m: q for m, q in stocks.items()
    if m in valid_materials
}

print("DEBUG: Suodatettuja nimikkeitä:", len(filtered_stocks))

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: done")
