import re

print("DEBUG: start")

def extract_digits(s):
    return "".join(c for c in s if c.isdigit())

# --- LUE DATA.TXT ---
valid_materials = set()

with open("data.txt", "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        first = line.split()[0]
        code = extract_digits(first)

        if code:
            valid_materials.add(code)

print("DEBUG: data.txt materiaalinumeroita:", len(valid_materials))

# --- PARSE SAP ---
stocks = {}
current_material = None

with open("sap_report.txt", "r", encoding="latin-1") as f:
    for raw in f:
        line = raw.rstrip("\n")

        if not line.strip():
            continue

        parts = line.split()

        # Materiaalinumero = ensimmäinen sana, jossa on numeroita
        if parts and any(ch.isdigit() for ch in parts[0]):
            current_material = extract_digits(parts[0])
            continue

        # Määrärivi
        if len(parts) >= 2 and parts[-1] in ("ST", "SHT"):
            qty_str = parts[-2].replace(",", ".")
            try:
                qty = float(qty_str)
                if current_material:
                    stocks[current_material] = qty
            except:
                pass
            current_material = None

print("DEBUG: SAP:sta parsittuja nimikkeitä:", len(stocks))

# --- SUODATA ---
filtered = {m: q for m, q in stocks.items() if m in valid_materials}

print("DEBUG: Suodatettuja nimikkeitä:", len(filtered))

print("=== FILTERED ===")
for m, q in filtered.items():
    print(m, q)

print("DEBUG: done")
