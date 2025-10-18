import pyeapi
import yaml

pyeapi.load_config('./eapi.conf')

vlans_dict = dict()
with open('switches.yml', 'r') as f:
    vlans_dict = yaml.safe_load(f)

# Load VLAN definitions from YAML
with open('vlans.yml', 'r') as f:
    file_data = yaml.safe_load(f)

expected_vlans = {str(vlan['id']): vlan['name'] for vlan in file_data['vlans']}
switches = file_data['switches']

def showvlans():
    for switch in vlans_dict['switches']:
        print(f"Connecting to {switch}")
        connect = pyeapi.connect_to(switch)
        raw_cmd_result = connect.enable('show vlan')
        cmd_vlans_dict = raw_cmd_result[0]['result']['vlans']
        for vlan in cmd_vlans_dict:
            vlan_id = vlan
            print(f'vlan ID: {vlan_id} and Vlan name is: {cmd_vlans_dict[vlan]["name"]}')


def compare_vlans():
    for switch in switches:
        print(f"🔗 Connecting to {switch} ...")
        try:
            connect = pyeapi.connect_to(switch)
            raw_cmd_result = connect.enable('show vlan')
            cmd_vlans_dict = raw_cmd_result[0]['result']['vlans']

            # VLANs on the switch
            switch_vlans = {str(vlan_id): vlan_data['name'] for vlan_id, vlan_data in cmd_vlans_dict.items()}

            # Compare
            missing_vlans = [vid for vid in expected_vlans if vid not in switch_vlans]
            extra_vlans = [vid for vid in switch_vlans if vid not in expected_vlans]
            name_mismatch = [vid for vid in expected_vlans if vid in switch_vlans and expected_vlans[vid] != switch_vlans[vid]]

            # Print results
            if not missing_vlans and not extra_vlans and not name_mismatch:
                print(f"✅ {switch}: VLAN configuration matches file.\n")
            else:
                if missing_vlans:
                    print(f"❌ Missing VLANs: {missing_vlans}")
                if extra_vlans:
                    print(f"⚠️ Extra VLANs: {extra_vlans}")
                if name_mismatch:
                    print("🔸 Name mismatches:")
                    for vid in name_mismatch:
                        print(f"   VLAN {vid}: expected '{expected_vlans[vid]}', found '{switch_vlans[vid]}'")
                print()  # newline

        except Exception as e:
            print(f"❌ Failed to connect to {switch}: {e}\n")

compare_vlans()
