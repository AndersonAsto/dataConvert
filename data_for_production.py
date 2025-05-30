import pandas as pd
import numpy as np
from datetime import datetime

# Cargar archivos exportados
subsidiary_df = pd.read_csv("data/output/subsidiary.csv")
areas_df = pd.read_csv("data/output/chicken_areas.csv")
breeds_df = pd.read_csv("data/output/chicken_breeds.csv")
products_df = pd.read_csv("data/output/products.csv")
operators_df = pd.read_csv("data/output/operators.csv")

# Crear mapeo raza → prefijo de producto
breed_prefix_map = {
    "Cobb 500": "CBB",
    "Ross 308": "RSS",
    "Hubbard Flex": "HBF",
    "Hubbard JA57": "HBJ",
    "ISA Brown": "ISB",
    "Lohmann Brown": "LHB",
    "Hy-Line Brown": "HLB",
    "Rhode Island Red": "RID",
    "Plymouth Rock": "PLR",
    "Gallina Criolla Peruana": "GCP"
}

# Crear mapeo prefijo → lista de productos
product_mapping = {}
for _, row in products_df.iterrows():
    code_prefix = row['productCode'].split('-')[0]
    product_mapping.setdefault(code_prefix, []).append(row['productId'])

# Crear mapeo área → filial
area_subsidiary_map = {}
current_index = 0
for _, row in subsidiary_df.iterrows():
    count = row['areaCapacity']
    for i in range(count):
        area_id = areas_df.iloc[current_index + i]['areasId']
        area_subsidiary_map[area_id] = row['subsidiaryId']
    current_index += count

# Fechas desde 30-01-2019 hasta 30-12-2024
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 12, 31)

# Generar fechas con día 30 cuando sea posible
date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
date_list = []

for d in date_range:
    try:
        date_list.append(d.replace(day=30))
    except ValueError:
        # Si el mes no tiene día 30 (febrero), usar el último día disponible
        date_list.append(d)

# Convertimos a tipo datetime.date
date_list = [d.date() for d in date_list]

# Generar registros
records = []
operator_count = len(operators_df)

for date in date_list:
    for i, area in areas_df.iterrows():
        area_id = area['areasId']
        capacity = area['currentQuantity']
        subsidiary_id = area_subsidiary_map[area_id]
        operator_id = operators_df.iloc[i % operator_count]['operatorId']

        breed = breeds_df.sample(1).iloc[0]
        breed_id = breed['breedId']
        breed_name = breed['breed']

        breed_prefix = breed_prefix_map.get(breed_name)
        if not breed_prefix:
            continue  # Saltar si no hay prefijo mapeado

        available_products = product_mapping.get(breed_prefix, [])
        if not available_products:
            continue

        product_id = np.random.choice(available_products)
        quantity = int(capacity * np.random.uniform(0.7, 0.95))
        weight = round(quantity * np.random.uniform(1.2, 2.5), 2)
        status = np.random.randint(1, 4)

        records.append([
            subsidiary_id, area_id, breed_id, product_id,
            operator_id, date, quantity, status, weight
        ])

# Crear DataFrame final
columns = [
    "subsidiaryId", "areasId", "breedId", "productId",
    "operatorId", "pickUpDate", "quantityProduced",
    "processStatus", "totalWeight"
]
production_df = pd.DataFrame(records, columns=columns)
production_df["pickUpDate"] = production_df["pickUpDate"].apply(lambda x: f"'{x}'")

###production_df["created_at"] = datetime.now()

# Guardar archivos
csv_path = "data/output/production_events.csv"
npy_path = "data/output/production_events.npy"

production_df.to_csv(csv_path, index=False)
np.save(npy_path, production_df.to_records(index=False))

print(f"✅ Exportación completada: {len(production_df)} registros → CSV y NPY")
