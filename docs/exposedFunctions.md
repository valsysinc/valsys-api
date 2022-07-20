# Exposed modeling functions
A useful subset of modeling functions have been exposed. To access them, import via
```python
from valsys.modeling.service import X
```
For example, `from valsys.modeling.service import tag_model`.

The exposed functions are listed out below

## Model tagging
```python
tag_model(model_id: str, tags: List[str])
```
Tag the model with `model_id` (`str`) with the list of `tags` (`List[str]`).

## Model sharing
```python
share_model(model_id: str, email: str, permission: str)
```
Share model with `model_id` the users `email`.

The model is shared to the user with specified permissions; the allowed values are
* `permission` = `view`
* `permission` = `edit`
Any other permission value will result in a `NotImplementedError` exception being thrown.

If you attempt to share the model with a user that dosent exist, a `ShareModelException` will be thrown.

## Get model information
```python                
pull_model_information(model_id: str)                
```
Pulls the model information for the `model_id`.

This function returns a `ModelInformation` object, whose structure is
```python
class ModelInformation:
    uid: str # the uid of the model
    cases: List[CaseInformation] # list of case information inside the model
```
in which a `CaseInformation` object has the structure
```python
class CaseInformation:
    uid: str # the uid of the case
    case: str # the name of the case
```



## Get model case
```python
pull_case(uid: str)
```
Retreive a `Case` by its uid.
Returns... TODO

## Recalculate model
```python
recalculate_model(model_id: str)
```
Recalculates the model

## Add a child module
```python
add_child_module(parent_module_id: str, name: str, model_id: str, case_id: str) 
```
Add a new module to the parent module.

Inputs:
* `parent_module_id` (str): the moduleID of the parent
* `name` (str): the name of the new module
* `model_id` (str): the ID of the model into which the module is to be inserted
* `case_id` (str): the caseID of the module.

Returns the newly constructed `Module` object.

## Add a line item
```python
add_line_item(case_id: str, model_id: str, module_id: str, name: str,
                  order: int)                      
```