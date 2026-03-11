import re

print("DEBUG: Python start OK")

# --- FUNKTIO: PUHDISTA KOODI ---
def clean_code(code):
    return re.sub(r"[^A-Za-z0-9]", "", code)

# --- LUE DATA.TXT JA POIMI SALLITUT MATERIAALINUMEROT ---
valid_materials = set()

with open("data.txt", "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        first = line.split()[0]
        cleaned = clean_code(first)

        if cleaned:
            valid_materials.add(cleaned)

print(f"DEBUG: data.txt materiaalinumeroita: {len(valid_materials)}")

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

# Materiaalinumero: sisennetty, 5–6 numeroa tai kirjain+numeroita
material_regex = re.compile(r"^\s*([A-Za-z]?\d{5,6})\s+")

# Määrä: sisennetty, numero + ST/SHT
qty_regex = re.compile(r"^\s*([\d\.]+)\s+(ST|SHT)\s*$")

with open("sap_report.txt", "r", encoding="latin-1") as f:
    for raw in f:
        line = raw.rstrip("\n")

        if not line.strip():
            continue

        # Etsi materiaalinumero
        mat = material_regex.match(line)
        if mat:
            current_material = clean_code(mat.group(1))
            continue

        # Etsi määrä
        qty = qty_regex.match(line)
        if qty and current_material:
            amount = float(qty.group(1))
            stocks[current_material] = amount
            current_material = None

print(f"DEBUG: SAP:sta löytyi nimikkeitä: {len(stocks)}")

# --- SUODATA ---
filtered_stocks = {m: q for m, q in stocks.items() if m in valid_materials}

print(f"DEBUG: Suodatettuja nimikkeitä: {len(filtered_stocks)}")

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
