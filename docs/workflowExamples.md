# Workflow examples

This contains a bunch of examples of how to use the library.

## Append tags to an existing model
This assumes knowledge of the models `uid`.
```python
# Import the append_tags function from the modeling service
from valsys.modeling.service import append_tags
# define the models uid
uid = "0xe50deb"
# define the tags to be appended to the model
tags_to_append = ["t5", "t4"]
# append the tags
append_tags(uid, tags_to_append)
```

## Share a model
### With a single user
```python
# Import the share_model function from the modeling service
from valsys.modeling.service import share_model
# define the models uid
uid = "0xe50deb"
# define the email of the user the model is to be shared with
email_to_share_to = "jack.fuller@valsys.io"
# define the permissions for the user
permission = "view"
# share the model
share_model(uid, email_to_share_to, permission=permission)
```
### With multiple user and different permissions
```python
# Import the share_model function from the modeling service
from valsys.modeling.service import share_model
# define the models uid
uid = "0xe50deb"
# define the list of emails of the users the model is to be shared with;
# note that we are allowed to put different permissions per user.
users = [
    ("jack.fuller@valsys.io", "view"),
    ("simon.bessey@valsys.io", "edit")
]

# share the model
for email, permission in users:
    share_model(uid, email, permission=permission)
```

## Obtain module information for a model
```python
from valsys.modeling.service import pull_model_information, pull_case

uid = "0xe50deb"

first_case_info = pull_model_information(uid).first
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
from valsys.modeling.service import add_child_module
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