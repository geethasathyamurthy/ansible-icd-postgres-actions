# Databases For PostgreSQL

Ansible playbooks for [Databases For PostgreSQL](https://cloud.ibm.com/docs/databases-for-postgresql) to perform the following operations:

* [configure WAL2JSON](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-wal2json)

You can create a Schematics Action, using these playbooks; and allow your team members to perform these Actions in a controller manner.  
Follow the instruction to onboard these Ansible playbooks as Schematics Action, and run them as Schematics Jobs. 

## Prerequisites
- PostgreSQL provisioned in your IBM Cloud Account. The detailed steps to provision the PostgreSQL on IBM Cloud 
is [here](https://github.com/Cloud-Schematics/VSI-database)

## Inputs:
- ID of deployed postgresql
- Region where postgresql is deployed
- Set a password for [repl_user](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-user-management#the-repl-user)
- Replication slot name
- Name of the database

## Run the ansible playbook using Schematics API

In this example, we will use the Schematics Actions API to configure `wal2json` Action, using the `wal2json.yml` playbook.  
Further, use the Schematics Job API to run the newly created `wal2json` action.
 
- Create a Schematics action: "wal2json"

  Use the `POST {url}/v2/actions` with the following payload:
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
                "git_repo_url": "https://github.com/Cloud-Schematics/ansible-icd-postgres-actions"
           }
      },
      "command_parameter": "wal2json.yml",
      "tags": [
        "string"
      ],
      "source_type": "GitHub",
      "inputs": [
        {
            "name": "region",
            "value": "us-east",
            "metadata": {
                "type": "string",
                "secure": true,
            }
        },
        {
            "name": "deployment_id",
            "value": "crn:v1:..............",
            "metadata": {
                "type": "string",
            }
        },
        {
            "name": "repl_password",
            "value": "mypassword",
            "metadata": {
                "type": "string",
                "secure": true,
                "default_value": "hellopassword"
            }
        },
        {
            "name": "slot_name",
            "value": "myslotname",
            "metadata": {
                "type": "string",
                "default_value": "some_slot_name"
            }
        },
        {
            "name": "database_name",
            "value": "ibmclouddb",
            "metadata": {
                "type": "string",
                "secure": false,
                "default_value": "mydb"
            }
        }
    ]
  }
  ```

  The response payload will include the Action ID, for the newly created Schematics Action definition.

- Create & run the Schematics Job for "wal2json"

  Use the `POST {url}/v2/jobs` with the following payload:
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

- Check the Schematics Job status and the ansible logs:

  Use the `GET {url}/v2/jobs/{job-id}/logs`. 
  Url: https://schematics.cloud.ibm.com
  
  Pass header: Authorization: {bearer token}

## Run the ansible playbook using Schematics UI

Steps:

- Open https://cloud.ibm.com/schematics/actions to view the list of Schematics Actions.
- Click `Create action` button to create a new Schematics Action definition
- In the Create action page - section 1, provide the following inputs, to create a `wal2json` action in `Draft` state.
  * Action name : wal2json
  * Resource group: default
  * Location : us-east
- In the Create action page - section 2, provide the following input
  * Github url : https://github.com/Cloud-Schematics/ansible-icd-postgres-actions
  * Click on `Retrieve playbooks` button
  * Select `wal2json.yml` from the dropdown
- In the Create action page - Advanced options, provide the following input
  * Add `region` as key and `<Name of the region>` as value
  * Add `deployment_id` as key and `<postgres deployment id>` as value
  * Add `repl_password` as key and `<repl user password>` as value
  * Add `slot_name` as key and `<replication slot name>` as value
  * Add `database_name` as key and `<name of existing database>` as value
- Press the `Next` button, and wait for the newly created `wal2json` action to move to `Normal` state.
- Once the `wal2json` action is in `Normal` state, you can press the `Run action` button to initiate the Schematics Job
  * You can view the job status and the job logs (or Ansible logs) in the Jobs page of the `wal2json` Schematics Action
  * Jobs page of the `wal2json` Schematics Action will list all the historical jobs that was executed using this Action definition

## Run the ansible playbook using Ansible Playbook command

```
ansible-playbook wal2json.yml -e "region=eu-gb deployment_id=<deployment-id> repl_password=<REPL_PASSWORD> slot_name=<SLOT_NAME> database_name=<DATABASE_NAME> bearer_token=<BEARER TOKEN>"
```

Sample Command:
```
ansible-playbook wal2json.yml -e "region=eu-gb deployment_id='crn:v1:bluemix:public:databases-for-postgresql:eu-gb:a/111111111111111111111111:22222222-2222-2222-2222-2222222222::' repl_password=Abc1234abc slot_name=myhappyslot database_name=ibmclouddb bearer_token='Bearer 11hgdvhgdvchgevdckjvedcjkvedcv'" -vvvv
```

## References

https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-wal2json
