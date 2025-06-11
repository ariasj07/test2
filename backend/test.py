import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('ejemplo.db')
cursor = conn.cursor()

# Crear tabla (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    created_in TEXT -- formato YYYY-MM-DD
)
''')

# Insertar algunos datos de ejemplo
datos = [
    ("Evento A", "2025-06-05"),
    ("Evento B", "2025-06-06"),
    ("Evento C", "2025-06-06"),
    ("Evento D", "2025-06-07")
]

cursor.executemany('INSERT INTO eventos (nombre, created_in) VALUES (?, ?)', datos)
conn.commit()

# === Consulta por fecha exacta ===
print("Eventos del 2025-06-06:")
cursor.execute("SELECT * FROM eventos WHERE created_in = '2025-06-06'")
for fila in cursor.fetchall():
    print(fila)

# === Consulta por rango de fechas ===
print("\nEventos del 2025-06-05 al 2025-06-06:")
cursor.execute("""
SELECT * FROM eventos
WHERE created_in BETWEEN '2025-03-05' AND '2025-06-06'
""")
for fila in cursor.fetchall():
    print(fila)

# Cerrar conexión
conn.close()
