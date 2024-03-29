
# Exposed modeling functions
A useful subset of modeling functions have been exposed. To access them, import via
```python linenums="1"
from valsys.modeling.service import X
```
For example, `from valsys.modeling.service import tag_model`.

The exposed functions are listed out below.

If a number of imports are expected to be used, in order to not explode the number of imports, it may be useful to import and alias the entire modeling service via
```python linenums="1"
import valsys.modeling.service as Modeling
```
In which case functions are used via
```python linenums="1"
Modeling.tag_model(...)
Modeling.filter_user_models(...)
```
in which we used a placeholder for the correct function arguments.

## Model operations

### Model pulling
```python linenums="1"
pull_model(model_id)
```
::: valsys.modeling.service.pull_model


### Model tagging

```python linenums="1"
tag_model(model_id: str, tags: List[str])
```

::: valsys.modeling.service.tag_model



### Model sharing
```python linenums="1"
share_model(model_id: str, email: str, permission: str)
```
::: valsys.modeling.service.share_model

The model is shared to the user with specified permissions; the allowed values are

* `permission` = `view`
* `permission` = `edit`
* `permission` = `fullAccess`
  
Any other permission value will result in a `NotImplementedError` exception being thrown.

The allowed permissions and the correct strings can be found via
```python linenums="1"
from valsys.modeling.models import Permissions
```
So, for example, `Permissions.VIEW` could be provided to the `share_model` function call.

If you attempt to share the model with a user that dosent exist, a `ShareModelException` will be thrown.

### Model deleting
```python
delete_models(model_ids: List[str])
```
:::valsys.modeling.service.delete_models

### Model searching/filtering
```python linenums="1"
filter_user_models
```
::: valsys.modeling.service.filter_user_models


### Get model information
```python linenums="1"                
pull_model_information(model_id: str)                
```
:::valsys.modeling.service.pull_model_information

This function returns a `ModelInformation` object, whose structure is
```python linenums="1"
class ModelInformation:
    uid: str # the uid of the model
    tags: List[str] # tags on the model
    cases: List[CaseInformation] # list of case information inside the model
```
in which a `CaseInformation` object has the structure
```python linenums="1"
class CaseInformation:
    uid: str # the uid of the case
    case: str # the name of the case
```



### Get model case
```python linenums="1"
pull_case(case_id: str)
```
:::valsys.modeling.service.pull_case

### Recalculate model
```python linenums="1"
recalculate_model(model_id: str)
```
:::valsys.modeling.service.recalculate_model

### Dynamic updates
```python linenums="1"
dynamic_updates()                      
```
:::valsys.modeling.service.dynamic_updates


## Module operations
### Add child module
```python linenums="1"
add_child_module(parent_module_id: str, name: str, model_id: str, case_id: str) 
```
:::valsys.modeling.service.add_child_module

### Delete module
```python linenums="1"
remove_module(model_id: str, module_id: str)
```
:::valsys.modeling.service.remove_module

### Rename module
```python linenums="1"
rename_module(model_id: str, module_id: str, new_module_name: str) 
```
:::valsys.modeling.service.rename_module



## Line item operations
### Add line item
```python linenums="1"
add_line_item(case_id: str, model_id: str, module_id: str, name: str, order: int)                      
```
::: valsys.modeling.service.add_line_item

### Delete line item
```python linenums="1"
delete_line_item(model_id: str, module_id: str, line_item_id: str)                    
```
::: valsys.modeling.service.delete_line_item

### Tag a line item
```python linenums="1"
tag_line_item(model_id: str, line_item_id: str, tags: List[str])                    
```
:::valsys.modeling.service.tag_line_item

### Edit line items
```python linenums="1"
edit_line_items(model_id: str, line_items: List[LineItem])                    
```
:::valsys.modeling.service.edit_line_items

## Fact operations
### Edit formula
```python linenums="1"
edit_formula(case_id: str, model_id: str, facts: List[Fact])                      
```
:::valsys.modeling.service.edit_formula


## Model groups
### Get model groups
```python
pull_model_groups()
```
:::valsys.modeling.service.pull_model_groups


### Add new model group
```python
new_model_groups(group_name: str, model_ids: List[str]) 
```
:::valsys.modeling.service.new_model_groups

### Update model groups
```python
update_model_groups(uid: str, name: str, model_ids: List[str])
```
:::valsys.modeling.service.update_model_groups
