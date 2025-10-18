from cvprac.cvp_client import CvpClient as cvp_client
import requests
import json


from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

cvp = '192.168.0.5'
cvp_user = 'arista'
cvp_pw = '8zj2jdvkbj4fqkku'

client = cvp_client()
client.connect([cvp], cvp_user, cvp_pw)

tasks = client.api.get_tasks_by_status('Pending')
#print(json.dumps(tasks, indent=4, sort_keys=True))


for task in tasks:
    task_id = task['workOrderId']
    hostname = task['workOrderDetails']['netElementHostName']
    print(f'running taskID {task_id} for {hostname}')
    client.api.execute_task(task_id)