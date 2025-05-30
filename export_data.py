# export_data.py
import pandas as pd
import numpy as np
from config.db import get_connection
import os

# Crear carpeta de salida si no existe
os.makedirs("data/output", exist_ok=True)

def export_table(table_name, file_prefix):
    conn = get_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)

    # Exportar a CSV
    csv_path = f"data/output/{file_prefix}.csv"
    df.to_csv(csv_path, index=False)

    # Exportar a .npy
    npy_path = f"data/output/{file_prefix}.npy"
    np.save(npy_path, df.to_records(index=False))

    print(f"✅ Exportado: {file_prefix} → CSV y NPY")

if __name__ == "__main__":
    tablas = {
        "production.subsidiary": "subsidiary",
        "production.chickenAreas": "chicken_areas",
        "production.chickenBreed": "chicken_breeds",
        "production.product": "products",
        "production.collectionOperator": "operators"
    }

    for tabla, nombre in tablas.items():
        export_table(tabla, nombre)
