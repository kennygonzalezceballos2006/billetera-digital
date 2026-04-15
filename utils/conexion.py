import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
            return conexion

    except Error as e:
        print(f"❌ Error al conectar: {e}")
        return None


if __name__ == "__main__":
    con = conectar_db()
    if con:
        con.close()
        print("🔌 Prueba terminada, conexión cerrada.")