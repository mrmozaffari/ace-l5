# %%
import pyeapi

pyeapi.load_config('./eapi.conf')

# %%
switches = ['leaf1', 'leaf2', 'leaf3', 'leaf4', 'spine1', 'spine2', 'spine3', 'spine4', 'borderleaf1', 'borderleaf2']

# %%
mac_table_set = set()
for switch in switches:
    connect = pyeapi.connect_to(switch)
    cmd_result = connect.enable('show mac address-table')
    unicast_table = cmd_result[0]['result']
    mac_table_dict = cmd_result[0]['result']['unicastTable']['tableEntries']
    for mac in mac_table_dict:
        mac_table_set.add(mac['macAddress'])


# %%
    for mac_entry in mac_table_set:
        print(mac_entry)