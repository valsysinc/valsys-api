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

::: valsys.modeling.service.tag_model

## Model sharing
```python
share_model(model_id: str, email: str, permission: str)
```
::: valsys.modeling.service.share_model

The model is shared to the user with specified permissions; the allowed values are

* `permission` = `view`
* `permission` = `edit`
* `permission` = `fullAccess`
  
Any other permission value will result in a `NotImplementedError` exception being thrown.

The allowed permissions and the correct strings can be found via
```python
from valsys.modeling.models import Permissions
```
So, for example, `Permissions.VIEW` could be provided to the `share_model` function call.

If you attempt to share the model with a user that dosent exist, a `ShareModelException` will be thrown.

## Get model information
```python                
pull_model_information(model_id: str)                
```
:::valsys.modeling.service.pull_model_information

This function returns a `ModelInformation` object, whose structure is
```python
class ModelInformation:
    uid: str # the uid of the model
    tags: List[str] # tags on the model
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
pull_case(case_id: str)
```
:::valsys.modeling.service.pull_case

## Recalculate model
```python
recalculate_model(model_id: str)
```
Recalculates the model

## Add a child module
```python
add_child_module(parent_module_id: str, name: str, model_id: str, case_id: str) 
```
:::valsys.modeling.service.add_child_module


## Add a line item
```python
add_line_item(case_id: str, model_id: str, module_id: str, name: str,
                  order: int)                      
```
:::valsys.modeling.service.add_line_item