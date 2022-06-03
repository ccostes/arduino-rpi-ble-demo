# imports
import os
import subprocess
from gatt_server import BleApplication, DataServiceAdvertisement, DataService

### params
DATA_SERVICE_INDEX = 0

# execution
ble_app = BleApplication()
ble_app.add_service(DataService(DATA_SERVICE_INDEX))
ble_app.register()

ble_adv = DataServiceAdvertisement(0)
ble_adv.register()

try:
    print('GATT application running')
    ble_app.run()
except KeyboardInterrupt:
    ble_app.quit()
    pass
