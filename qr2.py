import cv2
import qrcode
from pyzbar.pyzbar import decode
import mysql.connector

# Función para conectar a la base de datos y obtener registros
def get_records_from_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prueba"
    )

    cursor = db.cursor()

    query = "SELECT id FROM datos"
    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    db.close()

    return records

# Función para conectar a la base de datos y obtener datos asociados al ID
def get_data_from_db(record_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prueba"
    )

    cursor = db.cursor()

    query = "SELECT * FROM datos WHERE id = %s"
    cursor.execute(query, (record_id,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

# Obtén los registros de la base de datos
records = get_records_from_db()

for record in records:
    record_id = record[0]
    record_data = get_data_from_db(record_id)

    if record_data:
        # Aquí puedes acceder a los campos de record_data y mostrarlos si es necesario
        print("Datos asociados:", record_data)

        # Crea un objeto QRCode
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Agrega el código al objeto QRCode
        qr.add_data(record_id)
        qr.make(fit=True)

        # Crea una imagen QR
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Guarda la imagen QR en un archivo
        qr_image.save(f"codigoqr.png")

    else:
        print(f"No se encontraron datos asociados para el ID {record_id}")