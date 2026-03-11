import pandas as pd

print("DEBUG: start")

# --- LUE EXCEL JUURESTA ---
df = pd.read_excel("Book1.xlsx")

# Varmistetaan, että materiaalinumero on merkkijono
df["Material"] = df["Material"].astype(str).str.strip()

print("DEBUG: Excel-rivejä:", len(df))

# --- LUE DATA.TXT JUURESTA ---
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

# --- SUODATA EXCELIN RIVIT ---
filtered = df[df["Material"].isin(valid_materials)]

print("DEBUG: Suodatettuja rivejä:", len(filtered))

# --- TULOSTA TULOS ---
print("=== FILTERED RESULTS ===")
for _, row in filtered.iterrows():
    print(row["Material"], row["Unrestricted"], row["Unit"])

print("DEBUG: done")
