#!/usr/bin/python

# from ibm_vpc import VpcV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator
# from ibm_cloud_sdk_core import ApiException
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
import requests
from requests.exceptions import HTTPError
import time

import urllib.parse

REQUIRED_PARAMETERS = [
    ('deployment_id', 'str'),
    ('region', 'str'),
]

module_args = dict(
    deployment_id=dict(
        required=True,
        type='str'),
    region=dict(
        required=True,
        type='str'),
    env_bearer_token=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IC_IAM_TOKEN']),
        required=False),
    bearer_token=dict(
        required=False,
        no_log=True,
        type='str'),
    repl_password=dict(
        required=False,
        type='str',
        no_log=True),
    slot_name=dict(
        required=False,
        type='str'),
    database_name=dict(
        required=False,
        type='str'),
)

def run_module():

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # New resource required arguments checks
    missing_args = []
    for arg, _ in REQUIRED_PARAMETERS:
        if module.params[arg] is None:
            missing_args.append(arg)
    if missing_args:
        module.fail_json(msg=(
            "missing required arguments: " + ", ".join(missing_args)))
    
    dep_id = urllib.parse.quote(module.params["deployment_id"], safe='')
    url = "https://api.{}.databases.cloud.ibm.com/v4/ibm/deployments/{}/configuration".format(module.params["region"], dep_id)
    payload="{\n    \"configuration\": {\n       \"wal_level\": \"logical\",\n       \"max_replication_slots\": 21,\n       \"max_wal_senders\": 21\n    }\n}"
    
    if module.params["bearer_token"]:
        headers = {'Content-Type': 'application/json', 'Authorization': module.params["bearer_token"]}
    else:
        headers = {'Content-Type': 'application/json', 'Authorization': module.params["env_bearer_token"]}


    # configuring deployment for wal2json
    try:
        response = requests.request("PATCH", url, headers=headers, data=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        module.fail_json(msg=("Configuring deployment failed"))
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        module.fail_json(msg=("Configuring deployment failed"))
    else:
        print('Success!')

    if response.status_code != 200:
        module.fail_json(msg=("Configuring deployment failed"))

    time.sleep(8)
    #module.exit_json(**response.json())
    
    # change password for repl user
    payload = "{\"user\": {\"password\": \"%s\"}}" % module.params["repl_password"]
    url = "https://api.{}.databases.cloud.ibm.com/v4/ibm/deployments/{}/users/repl".format(module.params["region"], dep_id)

    try:
        response = requests.request("PATCH", url, headers=headers, data=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        module.fail_json(msg=("Repl password change failed"))
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        module.fail_json(msg=("Repl password change failed"))
    else:
        print('Success!')

    if response.status_code != 202:
        module.fail_json(msg=("Repl password change failed"))

    time.sleep(8)

    # Create a replication slot on the database
    url = "https://api.{}.databases.cloud.ibm.com/v4/ibm/deployments/{}/postgresql/logical_replication_slots".format(module.params["region"], dep_id)
    payload="{\"logical_replication_slot\": {\n    \"name\": \"%s\",\n    \"database_name\": \"%s\",\n    \"plugin_type\": \"wal2json\"\n    }\n}" % (module.params["slot_name"], module.params["database_name"])
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        module.fail_json(msg=("Replication Slot creation failed"))
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        module.fail_json(msg=("Replication Slot creation failed"))
    else:
        print('Success!')

    if response.status_code != 202:
        module.fail_json(msg=("Replication Slot creation failed"))

    module.exit_json(**response.json())

def main():
    run_module()

if __name__ == '__main__':
    main()