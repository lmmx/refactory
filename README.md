# refactory
Refactor utility with patterns composed of validated AST rules

## Installation

```sh
pip install refactory
```

- Requires Python 3.10+ (for keyword-only dataclasses for convenient recursive JSON parsing)

## Usage

To load a pattern stored in the library (a "rule spec"), use the `load_spec` helper function:

```py
>>> import refactory
>>> rule_spec = refactory.patterns.early_returns.ReplaceAnonRetVal
>>> rs = refactory.load_spec(rule_spec)
>>> rs.aliases
{'!1': {<class 'ast.Name'>: {id*: `${output}`}}, '!2': <class 'ast.Return'>}
```

The rest still has to be parsed and validated:

```py
>>> rs.preconditions
Preconditions(reltype="{'': '!2', 'value': 'ast.IfExp'}")
>>> rs.replacement
[{'ast.Assign': {'targets': ['!1'], 'value': '@1'}}, {'!2': {'value': '!1'}}]
>>> vrs = rs.validate()
>>> vrs
```
