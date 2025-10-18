import yaml
import pyeapi

vlan_dict = dict()
with open('vlans.yml', 'r') as f:
    vlan_dict = yaml.safe_load(f)

config = pyeapi.load_config('eapi.conf')

for switch in vlan_dict['switches']:
    print(f"Connecting to {switch}")
    connect = pyeapi.connect_to(switch)
    vlan_api = connect.api('vlans')
    for vlan in vlan_dict['vlans']:
        vlan_id=vlan['id']
        vlan_name=vlan['name']
        print(f'Adding vlan {vlan_id} to switch {switch}')
        vlan_api.create(vlan_id)
        vlan_api.set_name(vlan_id,vlan_name)