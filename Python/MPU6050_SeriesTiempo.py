"""
==============================================================
   CAPTURA Y ETIQUETADO DE DATOS MPU6050 (SIN GRÁFICAS)
==============================================================

AUTOR:
   Código educativo para adquisición y etiquetado
   de datos del MPU6050 usando Arduino + Python.

==============================================================
   ¿QUÉ HACE ESTE PROGRAMA?
==============================================================

Este programa:

1. Lee datos enviados desde Arduino
2. Recibe acelerómetro y giroscopio
3. Permite etiquetar movimientos usando teclado
4. Guarda datos en un archivo CSV
5. NO genera gráficas (más ligero y rápido)

==============================================================
   ¿CUÁNDO USAR ESTA VERSIÓN?
==============================================================

Usar esta versión cuando:

 Solo quieres guardar datos
 Quieres máxima velocidad
 No necesitas visualizar señales
 Vas a procesar datos después
 Quieres evitar lag por gráficas

==============================================================
   FLUJO GENERAL
==============================================================

MPU6050
   ↓
Arduino
   ↓ (USB Serial)
Python
   ↓
CSV etiquetado

==============================================================
   SOFTWARE NECESARIO
==============================================================

ANTES DE EJECUTAR:

 Python instalado
 VS Code instalado
 Extensión Python instalada
 Entorno virtual (venv)
 Librerías instaladas

==============================================================
   INSTALAR LIBRERÍAS
==============================================================

Con el entorno virtual activo:

   pip install pyserial pandas keyboard

==============================================================
   ¿PARA QUÉ SIRVE CADA LIBRERÍA?
==============================================================

serial
   Comunicación serial con Arduino

pandas
   Guardar archivos CSV

time
   Manejo de tiempo

os
   Manejo de carpetas

keyboard
   Detectar teclas del teclado

==============================================================
   IMPORTANTE SOBRE EL PUERTO COM
==============================================================

Verificar en Arduino IDE:

   Herramientas → Puerto

Ejemplos:

   COM3
   COM5
   COM8

Actualizar:

   PORT = "COM5"

==============================================================
   IMPORTANTE SOBRE BAUDRATE
==============================================================

Debe coincidir EXACTAMENTE con Arduino.

Si Arduino usa:

   Serial.begin(9600);

Aquí debe ser:

   BAUD = 9600

==============================================================
   CONTROLES
==============================================================

1 -> Clase 1
2 -> Clase 2
3 -> Clase 3

ESPACIO -> terminar captura

==============================================================
   EJEMPLO DE ETIQUETADO
==============================================================

Clase 1 -> caminar
Clase 2 -> sentado
Clase 3 -> correr

Mientras el sujeto realiza movimientos:

   presionar 1, 2 o 3

para etiquetar los datos.

==============================================================
   FORMATO DEL CSV
==============================================================

Tiempo[ms],Ax,Ay,Az,Gx,Gy,Gz,Clase

==============================================================
"""

# ==========================================================
# IMPORTAR LIBRERÍAS
# ==========================================================

import serial
import pandas as pd
import time
import os
import keyboard


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

# ----------------------------------------------------------
# PUERTO COM DEL ARDUINO
# ----------------------------------------------------------
#
# Verificar en:
#
# Arduino IDE → Herramientas → Puerto
#
#  CAMBIAR SI ES NECESARIO
# ----------------------------------------------------------

PORT = "COM5"


# ----------------------------------------------------------
# BAUDRATE
# ----------------------------------------------------------
#
# Debe coincidir con:
#
# Serial.begin(9600);
#
# del código Arduino
# ----------------------------------------------------------

BAUD = 9600


# ----------------------------------------------------------
# CARPETA DONDE SE GUARDARÁN LOS DATOS
# ----------------------------------------------------------
#
#  IMPORTANTE:
#
# La ruta debe existir.
#
# Ejemplo válido:
#
#   D:\Cursos\FunBio\Datos_MPU6050
#
# ----------------------------------------------------------

OUTPUT_DIR = r"D:\Cursos\FunBio\Datos_MPU6050"


# Crear carpeta automáticamente si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CREAR NOMBRE AUTOMÁTICO DEL ARCHIVO
# ==========================================================

timestamp = time.strftime("%Y%m%d_%H%M%S")

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    f"mpu_datos_{timestamp}.csv"
)


# ==========================================================
# INICIAR COMUNICACIÓN SERIAL
# ==========================================================

print("==============================================")
print("Inicializando comunicación serial...")
print("==============================================")


# Abrir puerto serial
ser = serial.Serial(PORT, BAUD, timeout=1)


# Esperar reinicio de Arduino
time.sleep(2)

print("Conexión serial iniciada correctamente.")
print()

print("==============================================")
print("CONTROLES")
print("==============================================")
print("1 -> Clase 1")
print("2 -> Clase 2")
print("3 -> Clase 3")
print("ESPACIO -> finalizar captura")
print("==============================================")


# ==========================================================
# VARIABLES PRINCIPALES
# ==========================================================

# Lista donde se guardarán TODOS los datos
data = []


# Clase inicial
current_class = "Clase 1"


# ==========================================================
# LOOP PRINCIPAL
# ==========================================================

while True:

    # ======================================================
    # DETECTAR TECLAS
    # ======================================================

    # ------------------------------------------------------
    # FINALIZAR PROGRAMA
    # ------------------------------------------------------

    if keyboard.is_pressed("space"):

        print()
        print("Captura finalizada por el usuario.")
        break


    # ------------------------------------------------------
    # CLASE 1
    # ------------------------------------------------------

    elif keyboard.is_pressed("1"):

        current_class = "Clase 1"

        print("Clase cambiada a 1")

        # Evitar múltiples detecciones
        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 2
    # ------------------------------------------------------

    elif keyboard.is_pressed("2"):

        current_class = "Clase 2"

        print("Clase cambiada a 2")

        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 3
    # ------------------------------------------------------

    elif keyboard.is_pressed("3"):

        current_class = "Clase 3"

        print("Clase cambiada a 3")

        time.sleep(0.3)


    # ======================================================
    # LEER DATOS DEL SERIAL
    # ======================================================

    # Leer línea enviada por Arduino
    line = ser.readline().decode(
        "utf-8",
        errors="ignore"
    ).strip()


    # Ignorar encabezado CSV
    if line and not line.startswith("Tiempo"):

        try:

            # ==================================================
            # SEPARAR DATOS CSV
            # ==================================================

            valores = line.split(",")


            # Verificar número correcto de columnas
            if len(valores) == 7:

                # Extraer variables
                t, ax, ay, az, gx, gy, gz = valores


                # ==================================================
                # CONVERTIR DATOS
                # ==================================================

                t = int(t)

                ax = float(ax)
                ay = float(ay)
                az = float(az)

                gx = float(gx)
                gy = float(gy)
                gz = float(gz)


                # ==================================================
                # GUARDAR DATOS
                # ==================================================

                data.append([
                    t,
                    ax,
                    ay,
                    az,
                    gx,
                    gy,
                    gz,
                    current_class
                ])


                # ==================================================
                # MOSTRAR EN TERMINAL
                # ==================================================
                #
                # Opcional:
                # comentar estas líneas si quieres
                # máxima velocidad
                # ==================================================

                print(
                    f"T={t} ms | "
                    f"Ax={ax:.2f} | "
                    f"Ay={ay:.2f} | "
                    f"Az={az:.2f} | "
                    f"Clase={current_class}"
                )


        except Exception as e:

            # Mostrar error sin detener programa
            print(f"Error de lectura: {e}")


# ==========================================================
# CERRAR SERIAL
# ==========================================================

ser.close()

print()
print("Puerto serial cerrado.")


# ==========================================================
# CONVERTIR A DATAFRAME
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
        "Gz",
        "Clase"
    ]
)


# ==========================================================
# GUARDAR CSV
# ==========================================================

df.to_csv(OUTPUT_FILE, index=False)

print()
print("==============================================")
print("DATOS GUARDADOS CORRECTAMENTE")
print("==============================================")
print(OUTPUT_FILE)


# ==========================================================
# RESUMEN FINAL
# ==========================================================

print()
print("==============================================")
print("RESUMEN")
print("==============================================")
print(f"Muestras capturadas: {len(df)}")
print(f"Archivo generado: {OUTPUT_FILE}")
print("==============================================")
