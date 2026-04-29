"""
==========================================================
   EXPORTAR DATOS SERIAL DEL MPU6050 A CSV
==========================================================

¿QUÉ HACE ESTE PROGRAMA?
----------------------------------------------------------

Este script:

1. Lee datos enviados por Arduino
2. Guarda automáticamente las series de tiempo
3. Exporta los datos a un archivo CSV

NO:
    grafica
    etiqueta clases
    usa teclado

Es la versión más simple para capturar datos.

==========================================================
   REQUISITOS
==========================================================

Instalar librerías:

   pip install pyserial pandas

==========================================================
   IMPORTANTE
==========================================================

El código Arduino debe enviar datos en formato CSV.

Ejemplo:

   Tiempo,Ax,Ay,Az,Gx,Gy,Gz

==========================================================
   PUERTO COM
==========================================================

Verificar en Arduino IDE:

   Herramientas → Puerto

Ejemplo:

   COM5

==========================================================
   BAUDRATE
==========================================================

Debe coincidir con Arduino.

Si Arduino tiene:

   Serial.begin(9600);

Aquí debe ser:

   BAUD = 9600

==========================================================
"""

# ==========================================================
# IMPORTAR LIBRERÍAS
# ==========================================================

import serial
import pandas as pd
import time
import os


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

# Puerto COM del Arduino
PORT = "COM5"

# Baudrate
BAUD = 9600


# ==========================================================
# CARPETA DE SALIDA
# ==========================================================

# CAMBIAR SEGÚN TU PC

OUTPUT_DIR = r"D:\Cursos\FunBio\Datos_MPU6050"

# Crear carpeta si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CREAR NOMBRE AUTOMÁTICO DEL CSV
# ==========================================================

timestamp = time.strftime("%Y%m%d_%H%M%S")

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    f"mpu_datos_{timestamp}.csv"
)


# ==========================================================
# INICIAR SERIAL
# ==========================================================

print("======================================")
print("Iniciando captura serial...")
print("======================================")

# Abrir puerto serial
ser = serial.Serial(PORT, BAUD, timeout=1)

# Esperar reinicio Arduino
time.sleep(2)

print("Conexión establecida.")
print()
print("Presiona CTRL + C para terminar.")
print()


# ==========================================================
# LISTA PARA DATOS
# ==========================================================

data = []


# ==========================================================
# CAPTURA PRINCIPAL
# ==========================================================

try:

    while True:

        # Leer línea serial
        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()


        # Ignorar encabezado
        if line and not line.startswith("Tiempo"):

            try:

                # Separar CSV
                valores = line.split(",")


                # Verificar cantidad correcta
                if len(valores) == 7:

                    # Extraer variables
                    t, ax, ay, az, gx, gy, gz = valores


                    # Convertir tipos
                    fila = [
                        int(t),
                        float(ax),
                        float(ay),
                        float(az),
                        float(gx),
                        float(gy),
                        float(gz)
                    ]


                    # Guardar fila
                    data.append(fila)


                    # Mostrar en pantalla
                    print(fila)

            except Exception as e:

                print(f"Error: {e}")


# ==========================================================
# DETENER CON CTRL + C
# ==========================================================

except KeyboardInterrupt:

    print()
    print("Captura finalizada por el usuario.")


# ==========================================================
# CERRAR SERIAL
# ==========================================================

ser.close()

print("Puerto serial cerrado.")


# ==========================================================
# CREAR DATAFRAME
# ==========================================================

df = pd.DataFrame(
    data,
    columns=[
        "Tiempo[ms]",
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz"
    ]
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

df.to_csv(OUTPUT_FILE, index=False)

print()
print("======================================")
print("CSV GUARDADO CORRECTAMENTE")
print("======================================")
print(OUTPUT_FILE)

print()
print(f"Muestras guardadas: {len(df)}")
