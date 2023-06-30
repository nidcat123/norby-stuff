import kaitaistruct


class NorbyBinary(kaitaistruct.KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = NorbyBinary.HeaderStruct(self._io, self, self._root)
        self.payload = NorbyBinary.Tmi0Struct(self._io, self, self._root)

    class HeaderStruct(kaitaistruct.KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length = self._io.read_u8le()
            self.receiver_address = self._io.read_u32le()
            self.transmitter_address = self._io.read_u32le()
            self.transaction_number = self._io.read_u16le()
            self.reserved = [self._io.read_u8le() for _ in range(2)]
            self.msg_type_id = self._io.read_s16le()

    class Tmi0Struct(kaitaistruct.KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.frame_start_mark = [self._io.read_u8le() for _ in range(2)]
            self.frame_definition = self._io.read_u16le()
            self.frame_number = self._io.read_u16le()
            self.frame_generation_time = self._io.read_u32le()
            self.brk_title = self._io.read_bytes(24).decode('ASCII')
            self.brk_number_active = self._io.read_u8le()
            self.brk_restarts_count_active = self._io.read_s32le()
            self.brk_current_mode_id = self._io.read_u8le()
            self.brk_transmitter_power_active = self._io.read_s8()
            self.brk_temp_active = self._io.read_s8()
            self.brk_module_state_active = [self._io.read_u8le() for _ in range(2)]
            self.brk_voltage_offset_amplifier_active = self._io.read_u16le()
            self.brk_last_received_packet_rssi_active = self._io.read_s8()
            self.brk_last_received_packet_snr_active = self._io.read_s8()
            self.brk_archive_record_pointer = self._io.read_u16le()
            self.brk_last_received_packet_snr_inactive = self._io.read_s8()
            self.ms_module_state = [self._io.read_u8le() for _ in range(2)]
            self.ms_payload_state = [self._io.read_u8le() for _ in range(2)]
            self.ms_temp = self._io.read_s8()
            self.ms_pn_supply_state = self._io.read_u8le()
            self.sop_altitude_glonass = self._io.read_s32le()
            self.sop_latitude_glonass = self._io.read_s32le()
            self.sop_longitude_glonass = self._io.read_s32le()
            self.sop_date_time_glonass = self._io.read_u32le()
            self.sop_magnetic_induction_module = self._io.read_u16le()
            self.sop_angular_velocity_vector = [self._io.read_u8le() for _ in range(6)]
            self.sop_angle_priority1 = self._io.read_u16le()
            self.sop_angle_priority2 = self._io.read_u16le()
            self.sop_mk_temp_dsg1 = self._io.read_s8()
            self.sop_mk_temp_dsg6 = self._io.read_s8()
            self.sop_board_temp = self._io.read_s8()
            self.sop_state = [self._io.read_u8le() for _ in range(2)]
            self.sop_state_dsg = [self._io.read_u8le() for _ in range(6)]
            self.sop_orientation_number = self._io.read_u8le()
            self.ses_median_panel_x_temp_positive = self._io.read_s8()
            self.ses_median_panel_x_temp_negative = self._io.read_s8()
            self.ses_solar_panels_state = [self._io.read_u8le() for _ in range(5)]
            self.ses_charge_level_m_ah = self._io.read_u16le()
            self.ses_battery_state = [self._io.read_u8le() for _ in range(3)]
            self.ses_charging_keys_state = [self._io.read_u8le() for _ in range(2)]
            self.ses_power_line_state = self._io.read_u8le()
            self.ses_total_charging_power = self._io.read_s16le()
            self.ses_total_generated_power = self._io.read_u16le()
            self.ses_total_power_load = self._io.read_u16le()
            self.ses_median_pmm_temp = self._io.read_s8()
            self.ses_median_pam_temp = self._io.read_s8()
            self.ses_median_pdm_temp = self._io.read_s8()
            self.ses_module_state = [self._io.read_u8le() for _ in range(3)]
            self.ses_voltage = self._io.read_u16le()
            self.crc16 = self._io.read_u16le()



#You can use this code to parse Norby binary files by creating an instance of the NorbyBinary class and providing a file-like object to its constructor. For example:


with open('your_file.norby', 'rb') as f:
    norby = NorbyBinary(f)
    # Access the parsed data
    header = norby.header
    payload = norby.payload
