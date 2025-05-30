from config.db import get_connection

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Conexión exitosa a la base de datos SQL Server.")
        conn.close()
    else:
        print("Fallo en la conexión a la base de datos.")
