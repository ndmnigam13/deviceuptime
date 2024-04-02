import json
import datetime
from openpyxl import Workbook

with open("outputv2.json", "r") as json_file:
    my_bgp_config = json.load(json_file)
    get_data = my_bgp_config.get("devices", {})

    # Create a new Workbook
    wb = Workbook()
    # Select the active worksheet
    ws = wb.active
    # Define the column headers
    ws.append(["HOST IP", "UPTIME", "DEVICE NAME", "LOCATION", "TYPE", "VENDOR", "CODE VERSION"])

    for device_id, device_info in get_data.items():
        # device_id is saving actually all key like "400" or "401"
        # device_info will save all values inside key "400" or "401"

        hostname = device_info['ip']
        if device_info['uptime'] is not None:
            seconds_uptime = int(device_info['uptime'])
            uptime = str(datetime.timedelta(seconds=seconds_uptime))
        else:
            uptime = str(device_info['uptime'])
        sysName = str(device_info['sysName'])
        location = str(device_info['location'])

        type = str(device_info['type'])
        vendor = str(device_info['vendor'])
        version = str(device_info['version'])
        # Insert data into rows
        ws.append([hostname, uptime, sysName, location, type, vendor, version])

# Save the workbook
wb.save("output.xlsx")
