# Data models


``` mermaid
classDiagram

  class Model{
    String uid
    List~Case~ cases
    List~String~ tags
    Case first_case 
    
    pull_module(module_id) Module
    pull_line_item(line_item_id) LineItem
  }

  class Case{
    String uid
    String case
    List~Module~ modules
    Module first_module
  }

  class Module{
   String uid
   String name
   List~LineItem~ line_items
   List~Module~ child_modules



   find_module_by_id(module_id) Module
  }

```
``` mermaid
classDiagram

  class LineItem{
    String uid
    String name
    List~Fact~ facts
    List~String~ tags
    Bool facts_tracked

    pull_fact_by_id(fact_id) Fact
  }

  class Fact{
    String uid
    String identifier
    String formula
    String period
    String value
    String fmt
    Bool numeric
  }

```