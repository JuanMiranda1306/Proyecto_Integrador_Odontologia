from database import crear_conexion
from mysql.connector import Error

def ver_clientes():
    """Obtiene todos los clientes registrados."""
    conexion = crear_conexion()
    if not conexion:
        return []
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        return clientes
    except Error as e:
        print(f"Error al obtener clientes: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def agregar_cliente(nombre_completo, edad, tratamiento_previo, recordatorio_contacto,
                    presupuesto_tratamiento, abierto_costo, dra_encargada,
                    fecha_entrada, fecha_salida):
    """Agrega un nuevo cliente (paciente) a la base de datos."""
    conexion = crear_conexion()
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO clientes (
                nombre_completo, edad, tratamiento_previo, recordatorio_contacto,
                presupuesto_tratamiento, abierto_costo, dra_encargada,
                fecha_entrada, fecha_salida
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre_completo, edad, tratamiento_previo, recordatorio_contacto,
                   presupuesto_tratamiento, abierto_costo, dra_encargada,
                   fecha_entrada, fecha_salida)
        cursor.execute(query, valores)
        conexion.commit()
        return True
    except Error as e:
        print(f"Error al agregar cliente: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def eliminar_cliente(cliente_id):
    """Elimina un cliente por su ID."""
    conexion = crear_conexion()
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        conexion.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al eliminar cliente: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
