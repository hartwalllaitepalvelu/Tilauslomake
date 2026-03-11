import pandas as pd

print("DEBUG: start")

# Lue Excel ja ohita ensimmäiset 4 riviä
df = pd.read_excel("Book1.xlsx", header=None, skiprows=4)

# Poista tyhjät rivit
df = df.dropna().reset_index(drop=True)

materials = []
descriptions = []
quantities = []
units = []

i = 0
while i < len(df):
    material = str(df.iloc[i, 1]).strip()      # Sarake B
    description = str(df.iloc[i, 2]).strip()   # Sarake C

    qty_unit = str(df.iloc[i+1, 1]).strip()    # Sarake B seuraavalta riviltä
    parts = qty_unit.split()

    quantity = parts[0]
    unit = parts[1] if len(parts) > 1 else ""

    materials.append(material)
    descriptions.append(description)
    quantities.append(quantity)
    units.append(unit)

    i += 2  # Hypätään seuraavaan tuotteeseen

df2 = pd.DataFrame({
    "Material": materials,
    "Material Description": descriptions,
    "Unrestricted": quantities,
    "Unit": units
})

print("DEBUG: Muodostettuja rivejä:", len(df2))

# Lue data.txt
valid_materials = set()
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        first = line.split()[0]
        if first.isdigit():
            valid_materials.add(first)

print("DEBUG: data.txt nimikkeitä:", len(valid_materials))

# Suodata
filtered = df2[df2["Material"].astype(str).isin(valid_materials)]

print("DEBUG: Suodatettuja rivejä:", len(filtered))

# Tulosta
print("=== FILTERED RESULTS ===")
for _, row in filtered.iterrows():
    print(row["Material"], row["Unrestricted"], row["Unit"])

print("DEBUG: done")
