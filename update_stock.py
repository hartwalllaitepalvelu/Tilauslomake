import pandas as pd

print("DEBUG: start")

# Lue Excel ja ohita ensimmäiset 4 riviä
df = pd.read_excel("Book1.xlsx", header=None, skiprows=4)

# Ota vain sarakkeet B, C ja D (eli indeksit 1, 2, 3)
df = df[[1, 2, 3]]

# Nimeä sarakkeet
df.columns = ["Material", "Material Description", "Unrestricted", "Unit"]

# Poista tyhjät rivit
df = df.dropna().reset_index(drop=True)

print("DEBUG: Excel-rivejä:", len(df))

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
filtered = df[df["Material"].astype(str).isin(valid_materials)]

print("DEBUG: Suodatettuja rivejä:", len(filtered))

# Tulosta
print("=== FILTERED RESULTS ===")
for _, row in filtered.iterrows():
    print(row["Material"], row["Unrestricted"], row["Unit"])

print("DEBUG: done")
