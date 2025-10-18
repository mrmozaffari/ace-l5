import yaml
import pyeapi

interface_dict = dict()
with open('interfaces.yml', 'r') as f:
    interface_dict = yaml.safe_load(f)
print(interface_dict)

config = pyeapi.load_config('eapi.conf')

for switch in interface_dict['devices']:
    print(switch)
    print(f"Connecting to {switch}")
    connect = pyeapi.connect_to(switch)
    int_api = connect.api('ipinterfaces')
    for interface in interface_dict['devices'][switch]['interfaces']:
        ip = interface_dict['devices'][switch]['interfaces'][interface]['ip']
        mask = interface_dict['devices'][switch]['interfaces'][interface]['mask']
        ip_mask = f'{ip}/{mask}'
        int_api.create(interface)
        int_api.set_address(interface, ip_mask)
