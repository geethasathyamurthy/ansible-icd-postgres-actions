# Databases For PostgreSQL- Configure Wal2json

Use this role to configure WAL2JSON for PostgreSQL.

## PreRequisites
This example needs a PostgreSQL provisioned on IBM Cloud. The detailed steps to provision the PostgreSQL on IBM Cloud 
is [here](https://github.com/Cloud-Schematics/postgresql_wal2json)

## Automate the playbook execution with schematics action 

Create schematics action to run Ansible playbook in IBM Cloud. In the example we will use schematics actions API to illustrate the execution of playbook.
 
- Create a Schematics action:

 Make POST request {url}/v2/actions using following payload:
 
 Url: https://schematics.cloud.ibm.com
 
 Pass header: Authorization: {bearer token}
 
  ```
  {
      "name": "wal2json",
      "description": "This Action can be used to configure wal2json",
      "location": "us-east",
      "resource_group": "Default",
       "source": {
           "source_type" : "git",
           "git" : {
                "git_repo_url": "https://github.com/Cloud-Schematics/postgresql_wal2json"
           }
      },
      "command_parameter": "wal2json.yml",
      "tags": [
        "string"
      ],
      "source_readme_url": "stringtype",
      "source_type": "GitHub",
  }
  ```

- Create a job that will run the playbook:

  Make POST request to {url}/v2/jobs using following payload:
  
  Url: https://schematics.cloud.ibm.com
  
  Pass header: Authorization: {bearer token}
 
    ```
    {
      "command_object": "action",
      "command_object_id": {action-id from the response of above request},
      "command_name": "ansible_playbook_run",
      "command_parameter": "wal2json.yml"
    }
    ```

- Check the progress by getting ansible logs:

  Make GET request to {url}/v2/jobs/{job-id}/logs.
 
  Url: https://schematics.cloud.ibm.com
  
  Pass header: Authorization: {bearer token}

## Execute the playbook using Schematics UI

Steps:

- Login to cloud.ibm.com
- From top left open the Navigation menu
- Tap Schematics
- Again in left side navigation menu, tap on Actions
- Click on Create action button(right side of screen)
- Give action name, resource-group, location and hit create button
- In github url box pass: https://github.com/Cloud-Schematics/postgresql_wal2json
- Hit retrieve playbooks button
- Select wal2json playbook from Playbooks dropdown
- Tap next button
- Once the action come in normal state, Hit run action button.
- You can check job logs in Jobs page

## Running Ansible command
```
ansible-playbook wal2json.yml -e "region=eu-gb deployment_id=<deployment-id> repl_password=<REPL_PASSWORD> slot_name=<SLOT_NAME> database_name=<DATABASE_NAME> bearer_token=<BEARER TOKEN>"
```

Sample Command:
```
ansible-playbook wal2json.yml -e "region=eu-gb deployment_id='crn:v1:bluemix:public:databases-for-postgresql:eu-gb:a/111111111111111111111111:22222222-2222-2222-2222-2222222222::' repl_password=Abc1234abc slot_name=myhappyslot database_name=ibmclouddb bearer_token='Bearer 11hgdvhgdvchgevdckjvedcjkvedcv'" -vvvv
```

## References
https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-wal2json