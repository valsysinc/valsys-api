# Workflow examples

This is a collection of examples of how to use the Valsys library.

## Spawn a model
This is one of the most involved processes, in terms of the required data.

In the below example, we show how to spawn a `SBUX` model and obtains its model `uid`. 

```python
# Import the spawn_model function from the modeling service
from valsys.modeling.service import spawn_model

# Import the class for the model seed configuration data
from valsys.seeds.model import ModelSeedConfigurationData

# Define the model seed configuration data
model_seed_config = ModelSeedConfigurationData(
    company_name = 'STARBUCKS CORP',
    ticker = 'SBUX',
    template_name = 'dcf-standard',
    proj_period = 3,
    hist_period = 2,
    industry_group = 'RETAIL-EATING \u0026 DRINKING PLACES',
    start_period = 2019,
    start_date = "2022-07-08T14:18:33.050Z"
)

# Spawn the model and obtain the new modelID
spawned_model_id = spawn_model(model_seed_config)
```

If the `template_name` is incorrectly entered (e.g., typo, or something that doesnt exist), a `TemplateNotFoundException` is thrown explaining 
```
TemplateNotFoundException: template not found for template_name: dcf-standard2
```

## Append tags to an existing model
This assumes knowledge of the models `uid`.
```python
# Import the append_tags function from the modeling service
from valsys.modeling.service import append_tags
# define the models uid
model_uid = "0xe50deb"
# define the tags to be appended to the model
tags_to_append = ["t5", "t4"]
# append the tags
append_tags(model_uid, tags_to_append)
```

## Share a model
The API allows a model to be shared to another user. This is done by referencing the modelsID, the email of the user the model is to be shared with, and the permissions that the user will have over the model.
### With a single user
```python
# Import the share_model function from the modeling service
from valsys.modeling.service import share_model
# Import the permissions types 
from valsys.modeling.models import Permissions

# define the models uid
model_uid = "0xe50deb"
# define the email of the user the model is to be shared with
email_to_share_to = "jack.fuller@valsys.io"
# define the permissions for the user
permission = Permissions.VIEW
# share the model
share_model(model_uid, email_to_share_to, permission=permission)
```
### With multiple user and different permissions
```python
# Import the share_model function from the modeling service
from valsys.modeling.service import share_model
# Import the permissions types 
from valsys.modeling.models import Permissions

# define the models uid
model_uid = "0xe50deb"
# define the list of emails of the users the model is to be shared with;
# note that we are allowed to put different permissions per user.
users = [
    ("jack.fuller@valsys.io", Permissions.VIEW),
    ("simon.bessey@valsys.io", Permissions.EDIT)
]

# share the model
for email, permission in users:
    share_model(model_uid, email, permission=permission)
```



## Obtain module information for a model

It will be common to need module information: for example, moduleIDs.

This workflow shows how to obtain the module meta data for a model. Crucially, this shows the module hierarchy, as well as the module IDs and names.

```python
from valsys.modeling.service import pull_model_information, pull_case

model_uid = "0xe50deb"

first_case_info = pull_model_information(model_uid).first
case = pull_case(first_case_info.uid)
module_info = case.module_meta
```
will result in `module_info` being something like
```json
[
    {
        "name": "DCF", 
        "uid": "0xe50c46", 
        "children": [
            {
                "name": "Balance Sheet", 
                "uid": "0xe50dbd", 
                "children": [
                    {
                        "name": "Equity", 
                        "uid": "0xe50cd3", 
                        "children": []
                    }, 
                    {
                        "name": "Liabilities", 
                        "uid": "0xe50d22", 
                        "children": []
                    }, 
                ]
            }, 
            {
                "name": "DCF Drivers", 
                "uid": "0xe50fe6", 
                "children": []
            }, 
            {
                "name": "Income Statement", 
                "uid": "0xe510a8", 
                "children": [
                    {
                        "name": "Earnings Per Share", 
                        "uid": "0xe50c5f", 
                        "children": []
                    }, 
                    {
                        "name": "Operating Income", 
                        "uid": "0xe50cf8", 
                        "children": []
                    }, 
                ]
            },
            {
                "name": "Cash Flow statement", 
                "uid": "0xe51235", 
                "children": [
                    {
                        "name": "Cash Flow From Operating Activities", 
                        "uid": "0xe50c1b", 
                        "children": []
                    }
                ]
            }
        ]
    }
]

```
Note that the nested structure highlights the modules parent-child relationship. Each modules `name`, `uid`, and `children` modules are returned.

## Add child module to existing module
Adding a child module requires knowledge of the parent modules `uid`.
```python
# Import the add_child_module function from the modeling service
from valsys.modeling.service import add_child_module, pull_model_information
# define the model uid
model_uid = '0xe50deb'
# define the uid of the parent module
parent_module_uid = '0xe51235'
# define the name of the new module
new_module_name = 'new module'
# go get the case uid for the model
case_uid = pull_model_information(model_uid).first.uid
# use the above data to add a child module
add_child_module(parent_module_uid, new_module_name, model_uid, case_uid)
```

## Add line item to a module
This workflow allows a line item to be added to an existing module; it requires knowledge of the `modelID`, and `moduleID`. One must provide the `name` of the new line item, and the `order` of the line item in the module.
```python
# Import the add_line_item function from the modeling service
from valsys.modeling.service import add_line_item, pull_model_information
# Define the required data
model_id = '0xe50deb'
module_id = '0xe51235'
line_item_name = 'new line item'
line_item_order = 10

# Get the caseID from the modelID
case_id = pull_model_information(model_id).first.uid
# Add the new line item
# returns a new line line object.
new_line_item = add_line_item(model_id = model_id, case_id = case_id, module_id = module_id, name = line_item_name, order = line_item_order)
```
Note that adding the same line item multiple times will result in an error.