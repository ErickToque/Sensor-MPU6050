import serial
import pandas as pd
import time
import os
import keyboard
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
PORT = "COM5"
BAUD = 9600

# Carpeta donde quieres guardar
OUTPUT_DIR = r"E:\PUCP\Biomecatronica\Sensor_MPU6050\Datos_MPU6050"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
# Nombre del archivo final con timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"mpu_datos_{timestamp}.csv")

# --- INICIO SERIAL ---
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("📡 Capturando datos del MPU6050...")
print("👉 Presiona '1', '2' o '3' para cambiar de clase. Presiona 'ESPACIO' para terminar.")

# --- LISTA PARA GUARDAR DATOS ---
data = []
current_class = "Clase 1"
class_numeric = 1  # para graficar como número

# --- CONFIGURAR PLOTEO ---
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,7), sharex=True,
                               gridspec_kw={'height_ratios':[3,1]})

ax1.set_title("Acelerómetro en tiempo real (Ax, Ay, Az)")
ax1.set_ylabel("Aceleración [m/s²]")

ax2.set_title("Clase en el tiempo")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Clase")
ax2.set_yticks([1,2,3])
ax2.set_yticklabels(["Clase 1","Clase 2","Clase 3"])

class_lines = []  # marcas verticales cuando cambia de clase

x_vals, ax_vals, ay_vals, az_vals, class_vals = [], [], [], [], []

# --- LOOP ---
while True:
    if keyboard.is_pressed("space"):  # terminar
        print("⏹ Captura finalizada por el usuario.")
        break
    elif keyboard.is_pressed("1"):
        current_class = "Clase 1"
        class_numeric = 1
        print("🔖 Clase cambiada a 1")
        class_lines.append(len(x_vals))
        time.sleep(0.3)
    elif keyboard.is_pressed("2"):
        current_class = "Clase 2"
        class_numeric = 2
        print("🔖 Clase cambiada a 2")
        class_lines.append(len(x_vals))
        time.sleep(0.3)
    elif keyboard.is_pressed("3"):
        current_class = "Clase 3"
        class_numeric = 3
        print("🔖 Clase cambiada a 3")
        class_lines.append(len(x_vals))
        time.sleep(0.3)

    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if line and not line.startswith("Tiempo"):
        try:
            valores = line.split(",")
            if len(valores) == 7:
                t, ax_val, ay_val, az_val, gx, gy, gz = valores
                ax_val, ay_val, az_val = float(ax_val), float(ay_val), float(az_val)

                data.append([int(t), ax_val, ay_val, az_val,
                             float(gx), float(gy), float(gz), current_class])

                # --- actualizar datos ---
                x_vals.append(len(x_vals))
                ax_vals.append(ax_val)
                ay_vals.append(ay_val)
                az_vals.append(az_val)
                class_vals.append(class_numeric)

                # --- actualizar gráfica ---
                ax1.clear()
                ax1.plot(x_vals, ax_vals, label="Ax")
                ax1.plot(x_vals, ay_vals, label="Ay")
                ax1.plot(x_vals, az_vals, label="Az")

                for c in class_lines:
                    ax1.axvline(c, color="red", linestyle="--")
                ax1.set_ylabel("Aceleración [m/s²]")
                ax1.set_title(f"Acelerómetro (Ax, Ay, Az) - Clase actual: {current_class}")
                ax1.legend()

                ax2.clear()
                ax2.step(x_vals, class_vals, where="post", label="Clase", color="black")
                for c in class_lines:
                    ax2.axvline(c, color="red", linestyle="--")
                ax2.set_yticks([1,2,3])
                ax2.set_yticklabels(["Clase 1","Clase 2","Clase 3"])
                ax2.set_xlabel("Muestras")
                ax2.set_ylabel("Clase")

                plt.pause(0.01)
        except:
            pass

ser.close()

# --- CONVERTIR A DATAFRAME ---
df = pd.DataFrame(data, columns=["Tiempo[ms]", "Ax", "Ay", "Az", "Gx", "Gy", "Gz", "Clase"])

# --- GUARDAR CSV ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Datos guardados en {OUTPUT_FILE}")

# --- GUARDAR FIGURA ---
FIG_FILE = os.path.splitext(OUTPUT_FILE)[0] + ".png"
plt.ioff()
fig.savefig(FIG_FILE, dpi=300)
print(f"🖼️ Figura guardada en {FIG_FILE}")

plt.show() 