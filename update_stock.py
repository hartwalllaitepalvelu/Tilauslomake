import pandas as pd

print("DEBUG: start")

# Lue Excel yhtenä sarakkeena
raw = pd.read_excel("Book1.xlsx", header=None)

# Poista tyhjät rivit
raw = raw.dropna().reset_index(drop=True)

print("DEBUG: Excel-rivejä:", len(raw))

# Joka 4 rivi muodostaa yhden tuotteen
materials = []
descriptions = []
quantities = []
units = []

for i in range(0, len(raw), 4):
    try:
        materials.append(str(raw.iloc[i, 0]).strip())
        descriptions.append(str(raw.iloc[i+1, 0]).strip())
        quantities.append(str(raw.iloc[i+2, 0]).strip())
        units.append(str(raw.iloc[i+3, 0]).strip())
    except:
        pass

df = pd.DataFrame({
    "Material": materials,
    "Material Description": descriptions,
    "Unrestricted": quantities,
    "Unit": units
})

print("DEBUG: Muodostettuja rivejä:", len(df))

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
filtered = df[df["Material"].isin(valid_materials)]

print("DEBUG: Suodatettuja rivejä:", len(filtered))

# Tulosta
print("=== FILTERED RESULTS ===")
for _, row in filtered.iterrows():
    print(row["Material"], row["Unrestricted"], row["Unit"])

print("DEBUG: done")
