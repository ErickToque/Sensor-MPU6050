/*
 ==========================================================
   CALIBRACIÓN DEL SENSOR MPU6050
   ==========================================================
   IMPORTANTE: INSTALACIÓN CORRECTA DE LA LIBRERÍA
   ----------------------------------------------------------
   Este código fue probado con la librería:

   "MPU6050 by Electronic Cats"

   Instalar desde:
      Arduino IDE -> Herramientas -> Administrar bibliotecas

   Buscar:
      MPU6050 Electronic Cats
   ----------------------------------------------------------
   PROBLEMA COMÚN:
   Existen muchas librerías llamadas "MPU6050" y pueden
   entrar en conflicto entre sí.

   Si aparecen errores como:
      - "MPU6050.h: No such file"
      - errores de compilación
      - funciones no reconocidas
      - conflicto de clases

   entonces probablemente tienes varias librerías instaladas.
   ----------------------------------------------------------
   RECOMENDACIÓN:
   Eliminar manualmente TODAS las librerías MPU6050
   que NO sean de Electronic Cats.

   En Windows normalmente están en:

      Documentos/Arduino/libraries

   Revisar y eliminar carpetas como:
      MPU6050
      i2cdevlib
      MPU6050-master
      MPU6050_tockn
      etc.

   Dejando únicamente la librería:
      MPU6050 by Electronic Cats
   ----------------------------------------------------------
   ¿QUÉ HACE ESTE PROGRAMA?
   ----------------------------------------------------------
   1. Inicializa el sensor MPU6050
   2. Toma 1000 muestras del acelerómetro y giroscopio
   3. Calcula offsets (errores de reposo)
   4. Convierte los offsets a unidades SI:
         - m/s² para aceleración
         - °/s para velocidad angular
   5. Imprime constantes listas para copiar y pegar
      en el código principal de adquisición.

   ----------------------------------------------------------
   IMPORTANTE DURANTE LA CALIBRACIÓN
   ----------------------------------------------------------
   - NO mover el sensor
   - Colocarlo sobre una superficie estable
   - Esperar a que termine el proceso
 ==========================================================
*/

#include <Wire.h>
#include <MPU6050.h>

// Crear objeto del sensor
MPU6050 mpu;

// Factores de conversión:
// 16384 LSB = 1g  (configuración ±2g)
// 131 LSB = 1 °/s (configuración ±250 °/s)

const float accel_scale = 9.80665 / 16384.0; // Conversión a m/s²
const float gyro_scale  = 1.0 / 131.0;       // Conversión a °/s

void setup() {

  // Inicializar comunicación serial
  Serial.begin(9600);

  // Inicializar bus I2C
  Wire.begin();

  Serial.println("Inicializando MPU6050...");

  // Inicializar sensor
  mpu.initialize();

  // Verificar conexión del sensor
  if (!mpu.testConnection()) {

    Serial.println("Error: MPU6050 no conectado.");

    // Detener ejecución si no hay conexión
    while (1);
  }

  Serial.println("MPU6050 conectado correctamente.");
  Serial.println("Calibrando, NO mover el sensor...");

  // Número de muestras para promediar
  const int N = 1000;

  // Variables acumuladoras
  long ax_sum = 0;
  long ay_sum = 0;
  long az_sum = 0;

  long gx_sum = 0;
  long gy_sum = 0;
  long gz_sum = 0;

  // Tomar N muestras
  for (int i = 0; i < N; i++) {

    int16_t ax, ay, az;
    int16_t gx, gy, gz;

    // Leer acelerómetro y giroscopio
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Acumular lecturas
    ax_sum += ax;
    ay_sum += ay;

    /*
       En reposo, el eje Z mide aproximadamente +1g.
       Se resta 16384 para eliminar la gravedad y obtener
       únicamente el offset real del sensor.
    */
    az_sum += (az - 16384);

    gx_sum += gx;
    gy_sum += gy;
    gz_sum += gz;

    delay(2);
  }

  // Calcular offsets promedio en unidades SI
  float ax_offset_si = (ax_sum / (float)N) * accel_scale;
  float ay_offset_si = (ay_sum / (float)N) * accel_scale;
  float az_offset_si = (az_sum / (float)N) * accel_scale;

  float gx_offset_si = (gx_sum / (float)N) * gyro_scale;
  float gy_offset_si = (gy_sum / (float)N) * gyro_scale;
  float gz_offset_si = (gz_sum / (float)N) * gyro_scale;

  // Mostrar resultados
  Serial.println();
  Serial.println("======================================");
  Serial.println("Offsets en unidades SI");
  Serial.println("(m/s² y °/s)");
  Serial.println("======================================");

  Serial.println("Copiar y pegar en el código principal:");
  Serial.println();

  Serial.print("const float ax_offset = ");
  Serial.print(ax_offset_si, 6);
  Serial.println(";");

  Serial.print("const float ay_offset = ");
  Serial.print(ay_offset_si, 6);
  Serial.println(";");

  Serial.print("const float az_offset = ");
  Serial.print(az_offset_si, 6);
  Serial.println(";");

  Serial.print("const float gx_offset = ");
  Serial.print(gx_offset_si, 6);
  Serial.println(";");

  Serial.print("const float gy_offset = ");
  Serial.print(gy_offset_si, 6);
  Serial.println(";");

  Serial.print("const float gz_offset = ");
  Serial.print(gz_offset_si, 6);
  Serial.println(";");

  Serial.println();
  Serial.println("Calibración finalizada.");
}

void loop() {

  // No se ejecuta nada aquí
  // La calibración ocurre solo una vez en setup()

}
