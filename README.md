FLOW:

1. **First the arduino ide takes a reading from all the sensors and uploads the telemetry data into a binary file.**

2. **The binary file format is stored in a yaml document that adheres to the kataistruct format.**

3. **Next the binary file is parsed to read the header and other fields.**

4. **(The original code is written in python using the kataistruct library but the arduino ide doesnt support this and so, if the code has to be written in c, it will be using a basic parser.) (so ive written two documents to exhibit this)**

5. **Last, the document is decoded and displayed (python)**

MEANING OF ALL THE INPUT FIELDS:
Norby binary file format and what each field means:

struct NorbyHeader {
  uint8_t length;                    // Length of the header and payload in bytes
  uint32_t receiver_address;         // Receiver address
  uint32_t transmitter_address;      // Transmitter address
  uint16_t transaction_number;       // Transaction number
  uint8_t reserved[2];               // Reserved bytes (set to 0)
  int16_t msg_type_id;               // Message type ID
};


struct NorbyTmi0 {
  uint8_t frame_start_mark[2];                   // Frame start mark (set to 0)
  uint16_t frame_definition;                     // Frame definition
  uint16_t frame_number;                         // Frame number
  uint32_t frame_generation_time;                // Frame generation time
  char brk_title[24];                            // Title (24 characters)
  uint8_t brk_number_active;                     // Number of active elements
  int32_t brk_restarts_count_active;             // Restart count for active elements
  uint8_t brk_current_mode_id;                   // Current mode ID
  int8_t brk_transmitter_power_active;           // Transmitter power for active elements
  int8_t brk_temp_active;                         // Temperature for active elements
  uint8_t brk_module_state_active[2];            // Module state for active elements (2 bytes)
  uint16_t brk_voltage_offset_amplifier_active;  // Voltage offset amplifier for active elements
  int8_t brk_last_received_packet_rssi_active;   // Last received packet RSSI for active elements
  int8_t brk_last_received_packet_snr_active;    // Last received packet SNR for active elements
  uint16_t brk_archive_record_pointer;           // Archive record pointer
  int8_t brk_last_received_packet_snr_inactive;  // Last received packet SNR for inactive elements
  uint8_t ms_module_state[2];                    // Module state for MS elements (2 bytes)
  uint8_t ms_payload_state[2];                   // Payload state for MS elements (2 bytes)
  int8_t ms_temp;                                // Temperature for MS elements
  uint8_t ms_pn_supply_state;                    // PN supply state for MS elements
  int32_t sop_altitude_glonass;                  // Altitude for SOP elements (GLONASS)
  int32_t sop_latitude_glonass;                  // Latitude for SOP elements (GLONASS)
  int32_t sop_longitude_glonass;                 // Longitude for SOP elements (GLONASS)
  uint32_t sop_date_time_glonass;                // Date and time for SOP elements (GLONASS)
  uint16_t sop_magnetic_induction_module;        // Magnetic induction module for SOP elements
  



uint8_t sop_angular_velocity_vector[6];        // Angular velocity vector for SOP elements (6 bytes)
  uint16_t sop_angle_priority1;                  // Angle priority 1 for SOP elements
 

 uint16_t sop_angle_priority2;                  // Angle priority 2 for SOP elements
  int8_t sop_mk_temp_dsg1;                       // MK temperature for DSG1 element
  int8_t sop_mk_temp_dsg6;                       // MK temperature for DSG6 element
  int8_t sop_board_temp;                         // Board temperature for SOP elements
  uint8_t sop_state[2];                          // State for SOP elements (2 bytes)
  uint8_t sop_state_dsg[6];                      // State for SOP DSG elements (6 bytes)
  uint8_t sop_orientation_number;                // Orientation number for SOP elements
  int8_t ses_median_panel_x_temp_positive;       // Median panel X temperature (positive) for SES elements
  int8_t ses_median_panel_x_temp_negative;       // Median panel X temperature (negative) for SES elements
  uint8_t ses_solar_panels_state[5];             // Solar panels state for SES elements (5 bytes)
  uint16_t ses_charge_level_m_ah;                // Charge level in milliampere-hours for SES elements
  uint8_t ses_battery_state[3];                  // Battery state for SES elements (3 bytes)
  uint8_t ses_charging_keys_state[2];            // Charging keys state for SES elements (2 bytes)
  uint8_t ses_power_line_state;                  // Power line state for SES elements
  int16_t ses_total_charging_power;              // Total charging power for SES elements
  uint16_t ses_total_generated_power;            // Total generated power for SES elements
  uint16_t ses_total_power_load;                 // Total power load for SES elements
  int8_t ses_median_pmm_temp;                    // Median PMM temperature for SES elements
  int8_t ses_median_pam_temp;                    // Median PAM temperature for SES elements
  int8_t ses_median_pdm_temp;                    // Median PDM temperature for SES elements
  uint8_t ses_module_state[3];                   // Module state for SES elements (3 bytes)
  uint16_t ses_voltage;                          // Voltage for SES elements
  uint16_t crc16;                                // CRC16 checksum
};
