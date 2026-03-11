import re

print("DEBUG: Python start OK")

# --- LUE SAP-RAPORTTI JA SIIVOA SE ---
clean_lines = []

with open("sap_report.txt", "r", encoding="latin-1") as f:
    for raw in f:
        line = raw.strip()

        # Poista viivarivit
        if set(line) == {"-"}:
            continue

        # Poista pystyviivat
        line = line.replace("|", "").strip()

        if not line:
            continue

        clean_lines.append(line)

print(f"DEBUG: Siivottuja rivejä: {len(clean_lines)}")

# --- LUE DATA.TXT JA POIMI SALLITUT MATERIAALINUMEROT ---
valid_materials = set()
material_number_regex = re.compile(r"^[A-Z]?\d{5,6}$")

with open("data.txt", "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        first = line.split()[0].strip()

        # Poista näkymättömät merkit
        first = first.replace("\u200b", "").replace("\ufeff", "").strip()

        if material_number_regex.match(first):
            valid_materials.add(first)

print(f"DEBUG: data.txt materiaalinumeroita: {len(valid_materials)}")

# --- PARSE SIIVOTTU SAP-RAPORTTI ---
stocks = {}
current_material = None

material_line_regex = re.compile(r"^([A-Z]?\d{5,6})\s+")
qty_line_regex = re.compile(r"^(\d+[\.\d]*)\s+ST")

for line in clean_lines:

    # Nimikerivi
    mat_match = material_line_regex.match(line)
    if mat_match:
        current_material = mat_match.group(1)
        continue

    # Määrärivi
    qty_match = qty_line_regex.match(line)
    if qty_match and current_material:
        qty = qty_match.group(1)
        stocks[current_material] = float(qty)
        current_material = None

print(f"DEBUG: SAP:sta löytyi nimikkeitä: {len(stocks)}")

# --- SUODATA VAIN DATA.TXT:N NIMIKKEET ---
filtered_stocks = {m: q for m, q in stocks.items() if m in valid_materials}

print(f"DEBUG: Suodatettuja nimikkeitä: {len(filtered_stocks)}")

print("=== PARSED & FILTERED STOCKS ===")
for material, qty in filtered_stocks.items():
    print(material, qty)

print("DEBUG: Parser finished OK")
