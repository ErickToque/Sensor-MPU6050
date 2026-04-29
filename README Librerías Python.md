# README — Instalación Completa de Python, VS Code, Entornos Virtuales y Librerías para MPU6050

---

# Tabla de Contenidos

1. Introducción
2. Requisitos del sistema
3. Instalación de Python
4. Problemas comunes durante instalación de Python
5. Verificar instalación de Python
6. Instalar Visual Studio Code
7. Instalar extensión Python en VS Code
8. Abrir proyecto en VS Code
9. Crear entorno virtual (venv)
10. Problemas comunes con venv
11. Activar entorno virtual
12. Problemas de PowerShell y ExecutionPolicy
13. Instalar librerías Python
14. Problemas comunes instalando librerías
15. Verificar librerías instaladas
16. Seleccionar intérprete Python correcto en VS Code
17. Ejecutar scripts Python
18. Problemas comunes de serial y COM
19. Problemas comunes con Arduino
20. Problemas comunes con rutas y carpetas
21. Estructura recomendada del proyecto
22. Comandos importantes
23. Solución rápida de errores frecuentes
24. Recomendaciones finales

---

# 1. Introducción

Esta guía explica paso a paso cómo configurar correctamente:

* Python
* Visual Studio Code
* Entornos virtuales (venv)
* Librerías necesarias
* Comunicación serial con Arduino
* Captura de datos MPU6050

Además incluye soluciones a los errores más comunes encontrados por estudiantes y usuarios principiantes.

---

# 2. Requisitos del sistema

Recomendado:

* Windows 10 u 11
* Arduino IDE instalado
* VS Code instalado
* Conexión USB funcional
* Arduino UNO/Nano/ESP32
* Sensor MPU6050

---

# 3. Instalación de Python

## Paso 1 — Descargar Python

Ir a:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

Descargar:

* Python 3.12
* Python 3.13

Preferiblemente versión 64 bits.

---

## Paso 2 — Ejecutar instalador

MUY IMPORTANTE:

Antes de instalar marcar:

```text
☑ Add Python to PATH
```

Esto es CRÍTICO.

Si no se marca, aparecerán errores como:

```text
python no se reconoce como un comando interno o externo
```

Luego presionar:

```text
Install Now
```

---

## Paso 3 — Opciones recomendadas

También marcar:

```text
☑ Install launcher for all users
☑ Disable path length limit
```

---

# 4. Problemas comunes durante instalación de Python

---

## Error:

```text
python no se reconoce como un comando interno o externo
```

## Causa:

Python no está agregado al PATH.

## Solución:

Reinstalar Python marcando:

```text
☑ Add Python to PATH
```

O agregar PATH manualmente.

---

## Error:

```text
Python was not found
```

## Causa:

Python no está instalado correctamente.

## Solución:

Reinstalar Python.

---

## Error:

```text
Microsoft Store alias
```

## Causa:

Windows intenta abrir Python desde Microsoft Store.

## Solución:

Ir a:

```text
Configuración → Apps → Advanced App Settings → App Execution Aliases
```

Desactivar:

* python.exe
* python3.exe

---

# 5. Verificar instalación de Python

Abrir CMD o PowerShell.

Ejecutar:

```bash
python --version
```

Debe mostrar algo como:

```text
Python 3.13.0
```

También probar:

```bash
pip --version
```

---

# 6. Instalar Visual Studio Code

Descargar desde:

[https://code.visualstudio.com/](https://code.visualstudio.com/)

Instalar normalmente.

---

# 7. Instalar extensión Python en VS Code

Abrir VS Code.

Ir a:

```text
Extensions
```

Buscar:

```text
Python
```

Instalar:

```text
Python (Microsoft)
```

---

# 8. Abrir proyecto en VS Code

Ir a:

```text
File → Open Folder
```

Abrir carpeta del proyecto.

Ejemplo:

```text
D:\Cursos\FunBio\Sensor-MPU6050-main
```

---

# 9. Crear entorno virtual (venv)

---

## ¿Qué es un entorno virtual?

Un entorno virtual permite:

* aislar librerías
* evitar conflictos
* mantener proyectos independientes
* evitar errores globales

---

## Crear entorno virtual

Abrir terminal en VS Code:

```text
Terminal → New Terminal
```

Ejecutar:

```bash
python -m venv venv
```

Esto crea:

```text
venv/
```

---

# 10. Problemas comunes con venv

---

## Error:

```text
Python was not found
```

## Solución:

Usar ruta completa:

```powershell
& "C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python313\python.exe" -m venv venv
```

---

## Error:

```text
No module named venv
```

## Solución:

Reinstalar Python.

---

# 11. Activar entorno virtual

En PowerShell:

```powershell
.\venv\Scripts\Activate
```

Si funciona aparecerá:

```text
(venv)
```

al inicio de la terminal.

---

# 12. Problemas de PowerShell y ExecutionPolicy

---

## Error:

```text
running scripts is disabled on this system
```

## Causa:

Windows bloquea scripts por seguridad.

---

## Solución:

Ejecutar UNA SOLA VEZ:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Luego responder:

```text
Y
```

y Enter.

Luego activar nuevamente:

```powershell
.\venv\Scripts\Activate
```

---

# 13. Instalar librerías Python

Con el venv activo:

```bash
pip install pyserial pandas matplotlib keyboard
```

---

## Librerías usadas

### pyserial

Comunicación serial con Arduino.

---

### pandas

Guardar CSV y manejar datos.

---

### matplotlib

Graficar señales.

---

### keyboard

Detectar teclas.

---

# 14. Problemas comunes instalando librerías

---

## Error:

```text
pip no se reconoce
```

## Solución:

Usar:

```bash
python -m pip install paquete
```

---

## Error:

```text
No module named serial
```

## Causa:

pyserial no está instalado.

## Solución:

```bash
pip install pyserial
```

---

## Error:

```text
No module named pandas
```

## Solución:

```bash
pip install pandas
```

---

## Error:

```text
No module named matplotlib
```

## Solución:

```bash
pip install matplotlib
```

---

## Error:

```text
No module named keyboard
```

## Solución:

```bash
pip install keyboard
```

---

## Error:

```text
Permission denied
```

## Solución:

Abrir VS Code como administrador.

---

# 15. Verificar librerías instaladas

Ejecutar:

```bash
pip list
```

Deben aparecer:

* pyserial
* pandas
* matplotlib
* keyboard

---

# 16. Seleccionar intérprete Python correcto en VS Code

MUY IMPORTANTE.

VS Code puede usar otro Python incorrecto.

---

## Seleccionar intérprete

Presionar:

```text
Ctrl + Shift + P
```

Buscar:

```text
Python: Select Interpreter
```

Elegir:

```text
.\venv\Scripts\python.exe
```

---

# 17. Ejecutar scripts Python

Ejemplo:

```bash
python archivo.py
```

O desde VS Code:

```text
▶ Run Python File
```

---

# 18. Problemas comunes de serial y COM

---

## Error:

```text
could not open port COM5
```

## Posibles causas:

* Puerto incorrecto
* Arduino desconectado
* Arduino IDE abierto
* Driver no instalado

---

## Solución:

### Paso 1

Verificar puerto en:

```text
Arduino IDE → Herramientas → Puerto
```

---

### Paso 2

Cerrar Arduino IDE.

Arduino IDE bloquea el puerto serial.

---

### Paso 3

Verificar cable USB.

Muchos cables solo cargan y NO transmiten datos.

---

# 19. Problemas comunes con Arduino

---

## Error:

```text
No data received
```

## Solución:

Verificar:

```cpp
Serial.begin(9600);
```

Debe coincidir con:

```python
BAUD = 9600
```

---

## Error:

```text
datos extraños o símbolos raros
```

## Causa:

Baudrate incorrecto.

---

# 20. Problemas comunes con rutas y carpetas

---

## Error:

```text
FileNotFoundError
```

## Causa:

Ruta inválida.

Ejemplo incorrecto:

```python
OUTPUT_DIR = r"E:\Datos"
```

cuando no existe unidad E:

---

## Solución:

Usar rutas válidas.

Ejemplo:

```python
OUTPUT_DIR = r"D:\Cursos\Datos"
```

---

# 21. Estructura recomendada del proyecto

```text
Proyecto/
│
├── Arduino/
│   └── MPU6050.ino
│
├── Python/
│   └── captura.py
│
├── Datos/
│   └── archivos CSV
│
├── venv/
│
└── README.md
```

---

# 22. Comandos importantes

---

## Crear venv

```bash
python -m venv venv
```

---

## Activar venv

```powershell
.\venv\Scripts\Activate
```

---

## Instalar librerías

```bash
pip install pyserial pandas matplotlib keyboard
```

---

## Ver librerías instaladas

```bash
pip list
```

---

## Ejecutar programa

```bash
python archivo.py
```

---

# 23. Solución rápida de errores frecuentes

| Error                   | Solución                   |
| ----------------------- | -------------------------- |
| python no reconocido    | Reinstalar Python con PATH |
| pip no reconocido       | usar python -m pip         |
| scripts disabled        | Set-ExecutionPolicy        |
| No module named serial  | pip install pyserial       |
| COM no abre             | cerrar Arduino IDE         |
| símbolos raros serial   | baudrate incorrecto        |
| FileNotFoundError       | ruta inválida              |
| VS Code usa otro Python | Select Interpreter         |

---

# 24. Recomendaciones finales

---

## Recomendación 1

Usar SIEMPRE entornos virtuales.

---

## Recomendación 2

No instalar librerías globalmente.

---

## Recomendación 3

Mantener Arduino IDE cerrado durante captura serial.

---

## Recomendación 4

Usar rutas simples.

Ejemplo:

```text
D:\Datos_MPU6050
```

---

## Recomendación 5

Verificar siempre:

* COM correcto
* baudrate correcto
* venv activo
* intérprete correcto

---

# FIN DEL README
