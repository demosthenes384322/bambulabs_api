###################################################
###############  NOTICE  ##########################
###################################################
###  MUST BE LOCATED IN THE ROOT DIR TO WORK  #####
###  AKA THE SAME DIR AS "README.MD"  #############
###################################################

from bambulabs_api import * # imports from files in dir instead of through pip
# ^ everything is in the subfolder of the same name
import time
import logging

####### CONFIG  ---  MUST EDIT ###############
config = ["192.168.0.111", "01S00C000000000", "00000000"]
#                              AC12309BH109
##  ^ I noted a difference in the example serial
# [ip : str, serial number for printer : str, access code for printer : str]
path = "yourpath/yourfile.3mf" # path to find file on your machine
filename = "yourfile.3mf" # path to put file on printer
ams = False
plate_type = "smooth"
####### END CONFIG ################

printer = Printer(config[0], config[2], config[1])

print("Object created, connecting to printer")
time.sleep(3)
printer.connect()
print("Connected")
time.sleep(3)
mqtt_status = printer.get_mqtt_status()
print(f"MQTT Status: {mqtt_status}, checking state")
#time.sleep(1)
state = printer.get_state()
print(f"Got state: {printer.get_current_state()}")
#time.sleep(3)
print(f"Got bed temp: {printer.get_bed_temperature()}")
#time.sleep(3)
print(f"Got light state: {printer.get_light_state()}")
#time.sleep(3)
print(f"Got time remaining: {printer.get_time()}")
#time.sleep(3)
#print("Attempting to turn off the light")
#printer.turn_light_off()
#time.sleep(3)
#print(f"Light state: {printer.get_light_state()}")
#time.sleep(7)
#print("Attempting to turn on the light")
#printer.turn_light_on()
#time.sleep(7)
#print(f"Light state: {printer.get_light_state()}")
#print("Attempting to home the toolhead")
#printer.home_printer()
#print("\nmqtt dump pre cali\n")
#print(f"{printer.mqtt_dump()}\n")
#printer.calibrate_printer(True, False, True)
#time.sleep(27*60) # wait 27 min for cali to compl
#print("\nmqtt dump pre file\n")
#print(f"{printer.mqtt_dump()}\n")
#prtrFilename = 'test.gcode'
# Open the file and pass the file object to upload_file
try:
    with open(path, 'rb') as file:  # Open file in binary mode
        result = printer.upload_file(file, filename)
        if result == "226" or result == 226:
            print("Upload sucessful, connection closed")
        else:
            print(f"Possible error, ftp result code {result}")

#except FileNotFoundError:
#    print(f"Error: File not found at {prtrFilename}")
except Exception as e:
    print(f"Error during file upload: {e}")
print("File uploaded, starting print")
time.sleep(3)
print("\nmqtt dump between upload and start\n")
print(f"{printer.mqtt_dump()}\n")
time.sleep(2)
outcome = printer.start_print(filename, 1, "smooth", False) # filename to start, plate_num, plate_type, use_ams
if outcome:
    print("MQTT message posted")
else:
    print("Failed to post MQTT message")
#time.sleep(10)
time.sleep(3)
print("\nmqtt dump post\n")
print(f"{printer.mqtt_dump()}\n")
time.sleep(3)
print("end of script")


### AN EXAMPLE OF WHAT AN MQTT DUMP WILL LOOK LIKE
###
###
mqtt_dump={
'upgrade_state': {'cur_state_code': 0},

'ipcam': {'ipcam_dev': '1', 'ipcam_record': 'enable', 'timelapse': 'disable', 'resolution': '', 'tutk_server': 'enable', 'mode_bits': 3},

'upload': {'status': 'idle', 'progress': 0, 'message': ''},

'net': {'conf': 0, 'info': [{'ip': 2566957248, 'mask': 16777215}]},

'nozzle_temper': 36.5,
'nozzle_target_temper': 0, 'bed_temper': 60.75,
'bed_target_temper': 0,
'chamber_temper': 5,
'mc_print_stage': '1',
'heatbreak_fan_speed': '0',
'cooling_fan_speed': '0',
'big_fan1_speed': '0',
'big_fan2_speed': '0',
'mc_percent': 100,
'mc_remaining_time': 0,
'ams_status': 0,
'ams_rfid_status': 6,
'hw_switch_state': 1,
'spd_mag': 100,
'spd_lvl': 2,
'print_error': 83935249,
'lifecycle': 'product',
'wifi_signal': '-35dBm',
'gcode_state': 'IDLE',
'gcode_file_prepare_percent': '100',
'queue_number': 0,
'queue_total': 0,
'queue_est': 0, 
'queue_sts': 0,
'project_id': '212400474',
'profile_id': '199159726',
'task_id': '427775271',
'subtask_id': '0',
'subtask_name': '',
'gcode_file': 'ftp_upload.gcode',
'stg': [],
'stg_cur': 255,
'print_type': 'idle',
'home_flag': 140723735,
'mc_print_line_number': '0',
'mc_print_sub_stage': 0,
'sdcard': True, 
'force_upgrade': False,
'mess_production_state': 'active',
'layer_num': 59,
'total_layer_num': 59, 's_obj': [],
'filam_bak': [], 'fan_gear': 0, 
'nozzle_diameter': '0.4', 
'nozzle_type': 'hardened_steel', 
'cali_version': 0, 'k': '0.0200',
'flag3': 15,
'hms': [], 
'online': {'ahb': False, 'rfid': False, 'version': 225464073},

'ams': {'ams': [], 'ams_exist_bits': '0', 'tray_exist_bits': '0', 'tray_is_bbl_bits': '0', 'tray_tar': '255', 'tray_now': '254',
'tray_pre': '254', 'tray_read_done_bits': '0', 'tray_reading_bits': '0', 'version': 13, 'insert_flag': True, 'power_on_flag': False},

'vt_tray': {'id': '254', 'tag_uid': '0000000000000000', 'tray_id_name': '', 'tray_info_idx': '', 'tray_type': '', 'tray_sub_brands': '', 'tray_color': '00000000',
'tray_weight': '0', 'tray_diameter': '0.00', 'tray_temp': '0', 'tray_time': '0', 'bed_temp_type': '0', 'bed_temp': '0', 'nozzle_temp_max': '0', 'nozzle_temp_min': '0',
'xcam_info': '000000000000000000000000', 'tray_uuid': '00000000000000000000000000000000', 'remain': 0, 'k': 0.019999999552965164, 'n': 1, 'cali_idx': -1},

'lights_report': [{'node': 'chamber_light', 'mode': 'on'}],
'command': 'push_status',
'msg': 1,
'sequence_id': '19568',
'param': 'Metadata/plate_1.gcode',
'file': 'ftp_upload.gcode',
'bed_leveling': True,
'bed_type': 'textured_plate',
'flow_cali': True,
'vibration_cali': True,
'url': 'ftp:///ftp_upload.gcode',
'layer_inspect': False,
'use_ams': True,
'ams_mapping': [0],
'skip_objects': None,
'reason': 'success',
'result': 'success'
}
