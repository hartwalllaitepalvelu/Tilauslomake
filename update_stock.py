import re

print("DEBUG: Python start OK")

# --- PUHDISTA KOODI ---
def clean_code(code):
    # Poista kaikki merkit, jotka eivät ole A-Z tai 0-9
    return re.sub(r"[^A-Za-z0-9]", "", code)

# --- LUE DATA.TXT JA POIMI MATERIAALINUMEROT ---
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

print("DEBUG: data.txt materiaalinumeroita:", len(valid_materials))

# --- PARSE SAP-RAPORTTI ---
stocks = {}
current_material = None

with open("sap_report.txt", "r", encoding="latin-1") as f:
    for raw in f:
        line = raw.rstrip("\n")

        if not line.strip():
            continue

        parts = line.split()

        # Jos rivin ensimmäinen "sana" sisältää numeroita → se on materiaalinumero
        if len(parts) >= 1 and any(c.isdigit() for c in parts[0]):
            cleaned = clean_code(parts[0])
            if cleaned:
                current_material = cleaned
            continue

        # Jos rivillä on määrä + yksikkö
        if len(parts) >= 2 and (parts[-1] in ("ST", "SHT")):
            try:
                qty = float(parts[-2].replace(",", "."))
                if current_material:
                    stocks[current_material] = qty
                current_material = None
            except:
                pass

print("DEBUG: SAP:sta löytyi nimikkeitä:", len(stocks))

# --- SUODATA ---
filtered_stocks = {m: q for m, q in stocks.items() if m in valid_materials}

print("DEBUG: Suodatettuja nimikkeitä:", len(filtered_stocks))

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
