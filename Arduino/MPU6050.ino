/*
 ==========================================================
   ADQUISICIÓN DE DATOS CON MPU6050
   ==========================================================

   IMPORTANTE: LIBRERÍA RECOMENDADA
   ----------------------------------------------------------
   Este código utiliza la librería:

      "MPU6050 by Electronic Cats"

   Instalar desde:
      Arduino IDE -> Herramientas -> Administrar bibliotecas

   Buscar:
      MPU6050 Electronic Cats

   ----------------------------------------------------------
   IMPORTANTE SOBRE CONFLICTOS DE LIBRERÍAS
   ----------------------------------------------------------
   Existen múltiples librerías MPU6050 y pueden generar:
      - errores de compilación
      - métodos no encontrados
      - conflictos de clases
      - lecturas incorrectas

   Se recomienda eliminar TODAS las librerías MPU6050
   que NO sean de Electronic Cats.

   En Windows normalmente están en:

      Documentos/Arduino/libraries

   Mantener únicamente:
      MPU6050 by Electronic Cats

   ----------------------------------------------------------
   ¿QUÉ HACE ESTE PROGRAMA?
   ----------------------------------------------------------
   1. Inicializa el sensor MPU6050
   2. Lee acelerómetro y giroscopio
   3. Convierte datos a unidades SI
   4. Aplica offsets de calibración
   5. Envía datos por Serial en formato CSV

   ----------------------------------------------------------
   FORMATO DE SALIDA
   ----------------------------------------------------------

   Tiempo[ms],Ax,Ay,Az,Gx,Gy,Gz

   Donde:
      Ax, Ay, Az -> aceleración en m/s²
      Gx, Gy, Gz -> velocidad angular en °/s

   ----------------------------------------------------------
   IMPORTANTE SOBRE LOS OFFSETS
   ----------------------------------------------------------
   Los offsets usados en este código:

      ax_offset
      ay_offset
      az_offset
      gx_offset
      gy_offset
      gz_offset

   fueron obtenidos mediante una calibración previa.

   ----------------------------------------------------------
   MUY IMPORTANTE:
   ----------------------------------------------------------
   Cada MPU6050 posee errores internos diferentes.

   Por ello:
      ✔ NO debes reutilizar offsets de otro sensor
      ✔ Debes recalibrar SIEMPRE cuando:
            - uses un nuevo MPU6050
            - cambies de módulo
            - reemplaces hardware
            - quieras mayor precisión

   En otras palabras:
      Cada sensor necesita SU PROPIA calibración.

   ----------------------------------------------------------
   RECOMENDACIÓN
   ----------------------------------------------------------
   Antes de usar este programa:

   1. Ejecutar primero el código de calibración
   2. Copiar los offsets generados
   3. Reemplazar los valores de abajo

 ==========================================================
*/

#include <Wire.h>
#include <MPU6050.h>

// Crear objeto del sensor
MPU6050 mpu;

/*
 ==========================================================
   OFFSETS DE CALIBRACIÓN
   ==========================================================

   Estos valores fueron calculados previamente usando
   el programa de calibración.

   Deben cambiarse para cada nuevo MPU6050.
*/

// Offsets del acelerómetro (m/s²)
const float ax_offset = -0.766880;
const float ay_offset =  0.035183;
const float az_offset =  0.468066;

// Offsets del giroscopio (°/s)
const float gx_offset = -1.437863;
const float gy_offset =  0.676000;
const float gz_offset = -1.447885;

/*
 ==========================================================
   FACTORES DE CONVERSIÓN
   ==========================================================

   Configuración por defecto del MPU6050:

      Acelerómetro: ±2g
      Giroscopio:   ±250 °/s

   Sensibilidades correspondientes:

      16384 LSB = 1g
      131 LSB   = 1 °/s
*/

// Conversión de acelerómetro a m/s²
const float accel_scale = 9.80665 / 16384.0;

// Conversión de giroscopio a °/s
const float gyro_scale = 1.0 / 131.0;

void setup() {

  // Inicializar comunicación serial
  Serial.begin(9600);

  // Inicializar comunicación I2C
  Wire.begin();

  Serial.println("Inicializando MPU6050...");

  // Inicializar sensor
  mpu.initialize();

  // Verificar conexión
  if (mpu.testConnection()) {

    Serial.println("MPU6050 conectado correctamente.");

  } else {

    Serial.println("Error: no se detecta el MPU6050.");

    // Detener ejecución
    while (1);
  }

  /*
     Encabezado CSV

     Facilita importar los datos a:
        - Excel
        - MATLAB
        - Python
        - Arduino Serial Plotter
        - herramientas de análisis
  */

  Serial.println(
    "Tiempo[ms],Ax[m/s²],Ay[m/s²],Az[m/s²],Gx[°/s],Gy[°/s],Gz[°/s]"
  );
}

void loop() {

  // Variables RAW del sensor
  int16_t ax_raw, ay_raw, az_raw;
  int16_t gx_raw, gy_raw, gz_raw;

  // Leer acelerómetro y giroscopio
  mpu.getMotion6(
    &ax_raw, &ay_raw, &az_raw,
    &gx_raw, &gy_raw, &gz_raw
  );

  /*
   ==========================================================
      CONVERSIÓN A UNIDADES SI
   ==========================================================

      Primero:
         RAW -> unidades físicas

      Luego:
         corrección con offsets
  */

  // Aceleración en m/s²
  float ax = ax_raw * accel_scale - ax_offset;
  float ay = ay_raw * accel_scale - ay_offset;
  float az = az_raw * accel_scale - az_offset;

  // Velocidad angular en °/s
  float gx = gx_raw * gyro_scale - gx_offset;
  float gy = gy_raw * gyro_scale - gy_offset;
  float gz = gz_raw * gyro_scale - gz_offset;

  // Tiempo desde inicio del programa
  unsigned long t_ms = millis();

  /*
   ==========================================================
      SALIDA CSV
   ==========================================================

      Formato:
      tiempo,ax,ay,az,gx,gy,gz
  */

  Serial.print(t_ms);
  Serial.print(",");

  Serial.print(ax, 3);
  Serial.print(",");

  Serial.print(ay, 3);
  Serial.print(",");

  Serial.print(az, 3);
  Serial.print(",");

  Serial.print(gx, 3);
  Serial.print(",");

  Serial.print(gy, 3);
  Serial.print(",");

  Serial.println(gz, 3);

  /*
     Frecuencia de muestreo

     delay(100) ≈ 10 Hz

     Ejemplos:
        delay(10)  ≈ 100 Hz
        delay(20)  ≈ 50 Hz
        delay(50)  ≈ 20 Hz
        delay(100) ≈ 10 Hz
  */

  delay(100);
}
