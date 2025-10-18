from cvprac.cvp_client import CvpClient as cvp_client
import requests
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

cvp = '192.168.0.5'
cvp_user = 'arista'
cvp_pw = '8zj2jdvkbj4fqkku'

"""If there are more than one CVP, I mean cluster then we can do this
    client.connect([cvp1,cvp2,cvp3], cvp_user, cvp_pw)
"""

"""For CVAAS
    cvp= 'arista.io'
    cvp_token = 'dfsdfsdfsd'
    cvp_user = 'arista'
    tenant = 'tenant_name'
    client.connect(nodes=['www.arista.io'], username='', password='', cvaas_token=cvp_token, is_cvaas=true, tenant=tenant)
"""

client = cvp_client()
client.connect([cvp], cvp_user, cvp_pw)

directory = "configs"
exists = os.path.exists(directory)
if not exists:
    os.makedirs(directory)

configlets = client.api.get_configlets(start=0, end=0)

for item in configlets['data']:
    configlet_name = item['name']
    config = item['config']
        # Replace problematic filename characters
    safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in configlet_name)
    # Build full path
    filepath = os.path.join(directory, f"{safe_name}.cfg")
    # Write file
    with open(filepath, 'w') as f:
        f.write(config)

    print(f"✅ Saved configlet '{configlet_name}' → {filepath}")        


    
