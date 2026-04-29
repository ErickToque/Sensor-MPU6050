```python
"""
==============================================================
   CAPTURA, ETIQUETADO Y EXPORTACIÓN DE DATOS MPU6050
==============================================================

AUTOR:
   Código educativo para adquisición de datos del MPU6050
   usando Arduino + Python + VS Code.

==============================================================
   ¿QUÉ HACE ESTE PROGRAMA?
==============================================================

Este programa:

1. Lee datos enviados desde Arduino por puerto serial
2. Visualiza Ax, Ay y Az en tiempo real
3. Permite etiquetar movimientos usando teclado
4. Guarda datos en formato CSV
5. Guarda la gráfica final en PNG

==============================================================
   FLUJO GENERAL DEL SISTEMA
==============================================================

MPU6050
   ↓
Arduino
   ↓ (Serial USB)
Python
   ↓
CSV + Gráficas

==============================================================
   SOFTWARE NECESARIO
==============================================================

ANTES DE EJECUTAR ESTE SCRIPT DEBES TENER:

✅ Python instalado
✅ VS Code instalado
✅ Extensión Python de VS Code
✅ Entorno virtual (venv)
✅ Librerías instaladas

==============================================================
   INSTALACIÓN DE PYTHON
==============================================================

Descargar Python desde:

   https://www.python.org/downloads/

⚠️ IMPORTANTE DURANTE LA INSTALACIÓN:

MARCAR:

   ☑ Add Python to PATH

antes de presionar:

   Install Now

==============================================================
   INSTALACIÓN DE VS CODE
==============================================================

Instalar:

   Visual Studio Code

Luego instalar la extensión:

   Python (Microsoft)

en:

   Extensions → buscar "Python"

==============================================================
   CREAR ENTORNO VIRTUAL (venv)
==============================================================

Abrir terminal en VS Code:

   Terminal → New Terminal

Ir a carpeta del proyecto:

   cd ruta_de_tu_proyecto

Crear entorno virtual:

   python -m venv venv

Si python no funciona:

   usar la ruta completa del python.exe

==============================================================
   ACTIVAR EL ENTORNO VIRTUAL
==============================================================

En PowerShell:

   .\venv\Scripts\Activate

Si aparece error de permisos:

   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Luego volver a activar.

==============================================================
   INSTALAR LIBRERÍAS NECESARIAS
==============================================================

Con (venv) activo:

   pip install pyserial pandas matplotlib keyboard

==============================================================
   ¿PARA QUÉ SIRVE CADA LIBRERÍA?
==============================================================

serial
   Comunicación serial con Arduino

pandas
   Guardar datos como tablas CSV

time
   Manejo de tiempos

os
   Manejo de carpetas y archivos

keyboard
   Detectar teclas del teclado

matplotlib
   Gráficas en tiempo real

==============================================================
   IMPORTANTE SOBRE EL PUERTO COM
==============================================================

Debes verificar el puerto COM del Arduino.

En Arduino IDE:

   Herramientas → Puerto

Ejemplos:

   COM3
   COM5
   COM8

Luego actualizar:

   PORT = "COM5"

==============================================================
   IMPORTANTE SOBRE BAUDRATE
==============================================================

Debe coincidir EXACTAMENTE con Arduino.

Si en Arduino tienes:

   Serial.begin(9600);

Aquí debe ser:

   BAUD = 9600

==============================================================
   CONTROLES DEL TECLADO
==============================================================

Tecla 1
   Cambia a Clase 1

Tecla 2
   Cambia a Clase 2

Tecla 3
   Cambia a Clase 3

ESPACIO
   Finaliza captura

==============================================================
   EJEMPLO DE ETIQUETADO
==============================================================

Clase 1 → caminar
Clase 2 → sentado
Clase 3 → correr

Mientras el sujeto realiza movimientos:

   Presionar 1, 2 o 3

para etiquetar los datos.

==============================================================
   SALIDAS GENERADAS
==============================================================

Se generan automáticamente:

1. Archivo CSV
2. Imagen PNG de las gráficas

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
import matplotlib.pyplot as plt


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

# ----------------------------------------------------------
# PUERTO SERIAL DEL ARDUINO
# ----------------------------------------------------------
#
# Verificar en:
#
# Arduino IDE → Herramientas → Puerto
#
# Ejemplo:
#   COM5
#
# ⚠️ CAMBIAR SI ES NECESARIO
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
# ⚠️ IMPORTANTE:
#
# La unidad debe existir.
#
# Ejemplos válidos:
#
#   D:\Datos
#   C:\Users\TuUsuario\Documents\Datos
#
# Si usas una ruta inexistente:
#
#   FileNotFoundError
#
# ----------------------------------------------------------

OUTPUT_DIR = r"D:\Cursos\FunBio\Datos_MPU6050"


# Crear carpeta automáticamente si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CREAR NOMBRE AUTOMÁTICO DEL ARCHIVO
# ==========================================================

# Fecha y hora actual
#
# Ejemplo:
#   20260428_154510

timestamp = time.strftime("%Y%m%d_%H%M%S")


# Archivo CSV final
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
# VARIABLES PARA ALMACENAR DATOS
# ==========================================================

# Lista principal
data = []


# Clase inicial
current_class = "Clase 1"


# Valor numérico de clase
#
# útil para gráficas
class_numeric = 1


# ==========================================================
# CONFIGURACIÓN DE GRÁFICAS
# ==========================================================

# Activar modo interactivo
plt.ion()


# Crear figura con dos subgráficas
fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(12, 8),
    sharex=True,
    gridspec_kw={'height_ratios':[3,1]}
)


# ==========================================================
# GRÁFICA SUPERIOR
# ==========================================================

ax1.set_title("Acelerómetro en tiempo real")
ax1.set_ylabel("Aceleración [m/s²]")


# ==========================================================
# GRÁFICA INFERIOR
# ==========================================================

ax2.set_title("Etiquetado de clases")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Clase")

ax2.set_yticks([1,2,3])

ax2.set_yticklabels([
    "Clase 1",
    "Clase 2",
    "Clase 3"
])


# ==========================================================
# VARIABLES AUXILIARES PARA GRÁFICAS
# ==========================================================

# Posiciones donde cambia la clase
class_lines = []


# Datos eje X
x_vals = []


# Señales acelerómetro
ax_vals = []
ay_vals = []
az_vals = []


# Etiquetas de clase
class_vals = []


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
        class_numeric = 1

        print("Clase cambiada a 1")

        # Guardar punto de cambio
        class_lines.append(len(x_vals))

        # Evitar múltiples pulsaciones
        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 2
    # ------------------------------------------------------

    elif keyboard.is_pressed("2"):

        current_class = "Clase 2"
        class_numeric = 2

        print("Clase cambiada a 2")

        class_lines.append(len(x_vals))

        time.sleep(0.3)


    # ------------------------------------------------------
    # CLASE 3
    # ------------------------------------------------------

    elif keyboard.is_pressed("3"):

        current_class = "Clase 3"
        class_numeric = 3

        print("Clase cambiada a 3")

        class_lines.append(len(x_vals))

        time.sleep(0.3)


    # ======================================================
    # LEER DATOS DEL PUERTO SERIAL
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


            # Verificar que lleguen 7 columnas
            if len(valores) == 7:

                # Extraer variables
                t, ax_val, ay_val, az_val, gx, gy, gz = valores


                # ==================================================
                # CONVERTIR A FLOAT
                # ==================================================

                ax_val = float(ax_val)
                ay_val = float(ay_val)
                az_val = float(az_val)

                gx = float(gx)
                gy = float(gy)
                gz = float(gz)


                # ==================================================
                # GUARDAR DATOS
                # ==================================================

                data.append([
                    int(t),
                    ax_val,
                    ay_val,
                    az_val,
                    gx,
                    gy,
                    gz,
                    current_class
                ])


                # ==================================================
                # ACTUALIZAR VARIABLES DE GRÁFICAS
                # ==================================================

                x_vals.append(len(x_vals))

                ax_vals.append(ax_val)
                ay_vals.append(ay_val)
                az_vals.append(az_val)

                class_vals.append(class_numeric)


                # ==================================================
                # ACTUALIZAR GRÁFICA SUPERIOR
                # ==================================================

                ax1.clear()

                ax1.plot(x_vals, ax_vals, label="Ax")
                ax1.plot(x_vals, ay_vals, label="Ay")
                ax1.plot(x_vals, az_vals, label="Az")


                # Líneas verticales de cambio de clase
                for c in class_lines:

                    ax1.axvline(
                        c,
                        color="red",
                        linestyle="--"
                    )


                ax1.set_ylabel("Aceleración [m/s²]")

                ax1.set_title(
                    f"Acelerómetro - Clase actual: {current_class}"
                )

                ax1.legend()


                # ==================================================
                # ACTUALIZAR GRÁFICA INFERIOR
                # ==================================================

                ax2.clear()

                ax2.step(
                    x_vals,
                    class_vals,
                    where="post",
                    color="black"
                )


                for c in class_lines:

                    ax2.axvline(
                        c,
                        color="red",
                        linestyle="--"
                    )


                ax2.set_yticks([1,2,3])

                ax2.set_yticklabels([
                    "Clase 1",
                    "Clase 2",
                    "Clase 3"
                ])

                ax2.set_xlabel("Muestras")
                ax2.set_ylabel("Clase")


                # ==================================================
                # ACTUALIZAR VENTANA
                # ==================================================

                plt.pause(0.01)


        except Exception as e:

            # Ignorar errores menores
            print(f"Error de lectura: {e}")


# ==========================================================
# CERRAR PUERTO SERIAL
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
print("CSV GUARDADO")
print("==============================================")
print(OUTPUT_FILE)


# ==========================================================
# GUARDAR FIGURA
# ==========================================================

# Crear nombre PNG
FIG_FILE = os.path.splitext(OUTPUT_FILE)[0] + ".png"


# Desactivar modo interactivo
plt.ioff()


# Guardar imagen
fig.savefig(FIG_FILE, dpi=300)

print()
print("==============================================")
print("FIGURA GUARDADA")
print("==============================================")
print(FIG_FILE)


# ==========================================================
# MOSTRAR GRÁFICA FINAL
# ==========================================================

plt.show()
```
