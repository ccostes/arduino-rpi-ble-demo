import dbus

from ble_gatt_server.advertisement import Advertisement
from ble_gatt_server.service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class BleApplication(Application):
    pass

class DataServiceAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("DataServiceBLE")
        self.include_tx_power = True

class DataService(Service):
    DATA_SVC_UUID = "00000000-8cb1-44ce-9a66-001dca0941a6"

    def __init__(self, index):
        Service.__init__(self, index, self.DATA_SVC_UUID, True)
        self.add_characteristic(DataCharacteristic(self))
        
    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class DataCharacteristic(Characteristic):
    DATA_CHARACTERISTIC_UUID = "00000001-8cb1-44ce-9a66-001dca0941a6"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.DATA_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(DataDescriptor(self))

    def WriteValue(self, value, options):
        int_val = int.from_bytes(value, "little", signed="True")
        print(f'Value received: {int_val}', flush=True)
        val = "".join(map(chr, int_val))
        print('New data value:', val, flush=True)

        self.service.set_data(val)

    def ReadValue(self, options):
        value = []

        val = self.service.get_data()
        value.append(dbus.Byte(val.encode()))

        return value

class DataDescriptor(Descriptor):
    DATA_DESCRIPTOR_UUID = "0001"
    DATA_DESCRIPTOR_VALUE = "Data"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.DATA_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.DATA_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value
