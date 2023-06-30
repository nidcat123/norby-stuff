#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <SPIFFS.h>
#include <MPU6050.h>

// Norby header structure
struct NorbyHeader {
  uint8_t length;
  uint32_t receiver_address;
  uint32_t transmitter_address;
  uint16_t transaction_number;
  uint8_t reserved[2];
  int16_t msg_type_id;
};

// Norby Tmi0 payload structure
struct NorbyTmi0 {
  uint8_t frame_start_mark[2];
  uint16_t frame_definition;
  uint16_t frame_number;
  uint32_t frame_generation_time;
  char brk_title[24];
  uint8_t brk_number_active;
  int32_t brk_restarts_count_active;
  uint8_t brk_current_mode_id;
  int8_t brk_transmitter_power_active;
  int8_t brk_temp_active;
  uint8_t brk_module_state_active[2];
  uint16_t brk_voltage_offset_amplifier_active;
  int8_t brk_last_received_packet_rssi_active;
  int8_t brk_last_received_packet_snr_active;
  uint16_t brk_archive_record_pointer;
  int8_t brk_last_received_packet_snr_inactive;
  uint8_t ms_module_state[2];
  uint8_t ms_payload_state[2];
  int8_t ms_temp;
  uint8_t ms_pn_supply_state;
  int32_t sop_altitude_glonass;
  int32_t sop_latitude_glonass;
  int32_t sop_longitude_glonass;
  uint32_t sop_date_time_glonass;
  uint16_t sop_magnetic_induction_module;
  uint8_t sop_angular_velocity_vector[6];
  uint16_t sop_angle_priority1;
  uint16_t sop_angle_priority2;
  int8_t sop_mk_temp_dsg1;
  int8_t sop_mk_temp_dsg6;
  int8_t sop_board_temp;
  uint8_t sop_state[2];
  uint8_t sop_state_dsg[6];
  uint8_t sop_orientation_number;
  int8_t ses_median_panel_x_temp_positive;
  int8_t ses_median_panel_x_temp_negative;
  uint8_t ses_solar_panels_state[5];
  uint16_t ses_charge_level_m_ah;
  uint8_t ses_battery_state[3];
  uint8_t ses_charging_keys_state[2];
  uint8_t ses_power_line_state;
  int16_t ses_total_charging_power;
  uint16_t ses_total_generated_power;
  uint16_t ses_total_power_load;
  int8_t ses_median_pmm_temp;
  int8_t ses_median_pam_temp;
  int8_t ses_median_pdm_temp;
  uint8_t ses_module_state[3];
  uint16_t ses_voltage;
  uint16_t crc16;
};

// BMP280 sensor instance
Adafruit_BMP280 bmp;

// MPU6050 sensor instance
MPU6050 mpu;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize BMP280 sensor
  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 sensor initialization failed!");
    while (1);
  }

  // Initialize MPU6050 sensor
  Wire.begin();
  mpu.initialize();

  // Initialize SPIFFS
  if (!SPIFFS.begin()) {
    Serial.println("SPIFFS initialization failed!");
    while (1);
  }

  // Create and populate the Norby Tmi0 payload
  NorbyTmi0 tmi0;
  memset(&tmi0, 0, sizeof(NorbyTmi0));

  // Read BMP280 sensor data
  tmi0.brk_temp_active = bmp.readTemperature();
  tmi0.brk_module_state_active[0] = bmp.readPressure() / 1000;

  // Read MPU6050 sensor data
  int16_t accelerometerX, accelerometerY, accelerometerZ;
  int16_t gyroX, gyroY, gyroZ;
  mpu.getMotion6(&accelerometerX, &accelerometerY, &accelerometerZ, &gyroX, &gyroY, &gyroZ);
  tmi0.sop_angular_velocity_vector[0] = gyroX >> 8;
  tmi0.sop_angular_velocity_vector[1] = gyroX & 0xFF;
  tmi0.sop_angular_velocity_vector[2] = gyroY >> 8;
  tmi0.sop_angular_velocity_vector[3] = gyroY & 0xFF;
  tmi0.sop_angular_velocity_vector[4] = gyroZ >> 8;
  tmi0.sop_angular_velocity_vector[5] = gyroZ & 0xFF;
  // Populate the remaining fields of the Tmi0 payload as needed

  // Create the Norby binary file
  File norbyFile = SPIFFS.open("/example.norby", "w+");
  if (!norbyFile) {
    Serial.println("Failed to create Norby binary file!");
    while (1);
  }

  // Create and populate the Norby header
  NorbyHeader header;
  header.length = sizeof(NorbyHeader) + sizeof(NorbyTmi0);
  header.receiver_address = 12345678;
  header.transmitter_address = 87654321;
  header.transaction_number = 1234;
  memset(header.reserved, 0, sizeof(header.reserved));
  header.msg_type_id = 0;

  // Write the header to the file
  norbyFile.write(reinterpret_cast<const uint8_t*>(&header), sizeof(NorbyHeader));

  // Write the Tmi0 payload to the file
  norbyFile.write(reinterpret_cast<const uint8_t*>(&tmi0), sizeof(NorbyTmi0));

  // Close the Norby binary file
  norbyFile.close();

  Serial.println("Norby binary file created successfully!");
}

void loop() {
  // Empty loop
}
