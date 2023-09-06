# VSL functions

Various VSL functions have been exposed; they can be accessed via the following aliased import

```python linenums="1"
import valsys.modeling.vsl as VSL
```

## Execute a VSL query
This returns data from a query. Could be in the form of widgets.
```python
VSL.execute_vsl_query(...)
```


::: valsys.modeling.vsl.execute_vsl_query

## Execute a VSL selectors query
This returns selectors only.

```python
VSL.execute_vsl_query_selectors(...)
```
::: valsys.modeling.vsl.execute_vsl_query_selectors