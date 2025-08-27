#include <Wire.h>
#include <MPU6050.h>
MPU6050 mpu;
// Offsets obtenidos tras calibración previa (en unidades del SI)
const float ax_offset = -0.766880;
const float ay_offset = 0.035183;
const float az_offset = 0.468066;
const float gx_offset = -1.437863;
const float gy_offset = 0.676000;
const float gz_offset = -1.447885;
// Sensibilidades del MPU6050 por defecto:
// Acelerómetro: 16384 LSB/g (±2g)
// Giroscopio: 131 LSB/(°/s) (±250 °/s)
const float accel_scale = 9.80665 / 16384.0; // m/s² por LSB
const float gyro_scale = 1.0 / 131.0; // °/s por LSB
void setup() {
Serial.begin(9600);
Wire.begin();
Serial.println("Inicializando MPU6050...");
mpu.initialize();
if (mpu.testConnection()) {
Serial.println("MPU6050 conectado correctamente.");
} else {
Serial.println("Error: no se detecta el MPU6050.");
while (1);
}
Serial.println("Tiempo[ms],Ax[m/s²],Ay[m/s²],Az[m/s²],Gx[°/s],Gy[°/s],Gz[°/s]");
}
void loop() {
int16_t ax_raw, ay_raw, az_raw;
int16_t gx_raw, gy_raw, gz_raw;
mpu.getMotion6(&ax_raw, &ay_raw, &az_raw, &gx_raw, &gy_raw, &gz_raw);
// Convertir a unidades del SI
float ax = ax_raw * accel_scale - ax_offset;
float ay = ay_raw * accel_scale - ay_offset;
float az = az_raw * accel_scale - az_offset;
float gx = gx_raw * gyro_scale - gx_offset;
float gy = gy_raw * gyro_scale - gy_offset;
float gz = gz_raw * gyro_scale - gz_offset;
// Obtener tiempo actual
unsigned long t_ms = millis();
// Imprimir datos como CSV
Serial.print(t_ms); Serial.print(",");
Serial.print(ax, 3); Serial.print(",");
Serial.print(ay, 3); Serial.print(",");
Serial.print(az, 3); Serial.print(",");
Serial.print(gx, 3); Serial.print(",");
Serial.print(gy, 3); Serial.print(",");
Serial.println(gz, 3);
delay(100); // Ajusta si quieres otra frecuencia de muestreo (e.g., 10 Hz)
}