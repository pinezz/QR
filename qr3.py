import cv2
from pyzbar.pyzbar import decode
import mysql.connector
import qrcode

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

# Inicializar la cámara
cap = cv2.VideoCapture(0)

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()
    
    # Decodifica los objetos (códigos QR) en el frame
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            # Decodifica el contenido del QR en formato UTF-8
            data = obj.data.decode('utf-8')
            
            # Obtiene los datos asociados al ID del QR
            record_data = get_data_from_db(data)

            if record_data:
                print("Datos asociados:", record_data)
            else:
                print(f"No se encontraron datos asociados para el ID {data}")

            # Crea un objeto QRCode
            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # Agrega el código al objeto QRCode
            qr.add_data(data)
            qr.make(fit=True)

            # Crea una imagen QR
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Guarda la imagen QR en un archivo
            qr_image.save(f"codigoqr.png")

    # Muestra el frame con el contenido de la cámara
    cv2.imshow("QR Code Reader", frame)

    # Espera a que se presione la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()