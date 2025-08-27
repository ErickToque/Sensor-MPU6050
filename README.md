# Proyecto MPU6050 con Arduino y Python

Este proyecto permite leer datos del sensor MPU6050 usando Arduino, exportarlos a CSV y graficarlos en Python.

## Contenido
- **Arduino/**
  - `MPU6050.ino`: Código principal para leer datos del sensor.
  - `Calibrar_MPU.ino`: Código para calibrar el sensor.
- **Python/**
  - `MPU6050_Exportar.py`: Script para leer datos enviados por Arduino y guardarlos en CSV/PNG.
- **Datos_MPU6050/**: Carpeta donde se guardan las mediciones (`.csv` y `.png`).

## Requisitos
- Arduino IDE
- Librería `Wire.h` y `MPU6050.h`
- Python 3.x con librerías:
  - `pandas`
  - `matplotlib`
  - `pyserial`

## Uso
1. Conectar el **MPU6050** al Arduino (SDA → A4, SCL → A5 en Arduino UNO).
2. Subir el código `MPU6050.ino`.
3. Ejecutar el script en Python para guardar los datos:
   ```bash
   python Python/MPU6050_Exportar.py
Autor
Erick Toque
