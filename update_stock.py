import re

with open("sap_report.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

stocks = {}
current_material = None

material_line_regex = re.compile(r"\|(\d{5})\s")
qty_line_regex = re.compile(r"\|\s*01\s+([\d\.,]+)\s+ST")

for line in lines:
    m = material_line_regex.search(line)
    if m:
        current_material = m.group(1)
        continue

    if current_material:
        q = qty_line_regex.search(line)
        if q:
            qty_str = q.group(1).replace(".", "").replace(",", ".")
            qty = float(qty_str)
            stocks[current_material] = qty
            current_material = None

print("Parsed stocks:")
for k, v in stocks.items():
    print(k, v)
