#include <Wire.h>
#include <MPU6050.h>
MPU6050 mpu;
const float accel_scale = 9.80665 / 16384.0; // m/s² por LSB
const float gyro_scale = 1.0 / 131.0; // °/s por LSB
void setup() {
Serial.begin(9600);
Wire.begin();
Serial.println("Inicializando MPU6050...");
mpu.initialize();
if (!mpu.testConnection()) {
Serial.println("Error: MPU6050 no conectado.");
while (1);
}
Serial.println("Calibrando, no mover el sensor...");
const int N = 1000;
long ax_sum = 0, ay_sum = 0, az_sum = 0;
long gx_sum = 0, gy_sum = 0, gz_sum = 0;
for (int i = 0; i < N; i++) {
int16_t ax, ay, az, gx, gy, gz;
mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
ax_sum += ax;
ay_sum += ay;
az_sum += (az - 16384); // restar 1g en Z
gx_sum += gx;
gy_sum += gy;
gz_sum += gz;
delay(2);
}
float ax_offset_si = (ax_sum / (float)N) * accel_scale;
float ay_offset_si = (ay_sum / (float)N) * accel_scale;
float az_offset_si = (az_sum / (float)N) * accel_scale;
float gx_offset_si = (gx_sum / (float)N) * gyro_scale;
float gy_offset_si = (gy_sum / (float)N) * gyro_scale;
float gz_offset_si = (gz_sum / (float)N) * gyro_scale;
Serial.println("Offsets en unidades SI (m/s² y °/s):");
Serial.println("Copia y pega estos valores en tu código de adquisición:");
Serial.print("const float ax_offset = "); Serial.print(ax_offset_si, 6); Serial.println(";");
Serial.print("const float ay_offset = "); Serial.print(ay_offset_si, 6); Serial.println(";");
Serial.print("const float az_offset = "); Serial.print(az_offset_si, 6); Serial.println(";");
Serial.print("const float gx_offset = "); Serial.print(gx_offset_si, 6); Serial.println(";");
Serial.print("const float gy_offset = "); Serial.print(gy_offset_si, 6); Serial.println(";");
Serial.print("const float gz_offset = "); Serial.print(gz_offset_si, 6); Serial.println(";");
}
void loop() {
// No hace nada, calibración solo en setup
}
