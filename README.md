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
{'!1': {<class 'ast.Name'>: {id**: `${output}`}}, '!2': <class 'ast.Return'>}
```

This representation of the two aliases in the `ReplaceAnonRetVal` pattern (which compiles to a
`refactor.Rule` for the [refactor][refactor-lib] library) can be read as follows:

[refactor-lib]: https://github.com/isidentical/refactor/

- The **alias name** `!1` is a `str` (though an `Alias` class is implemented, it'd be hard to access the
  `dict` by key if that were used as the key...). Aliases are the only `str`-type part of the
  `RefactorRuleSpec.aliases` dict.
- The **AST node** `ast.Name` is what it says on the tin (from the stdlib `ast` library). The same goes
  for `ast.Return`. These are the AST nodes for a named variable and a return statement in Python.
- `id**` (and any other name with `**` after) represents a **kwarg name** (i.e. the keyword argument
  passed to the AST node preceding it, in this case the `ast.Name` takes an `id` keyword argument).
- `${output}` is a **string literal** in a pattern: that is, it represents the string `"output"`.
  The `${}` wrapped around the string is used to denote a string literal.

The rest still has to be parsed and validated:

```py
>>> rs.preconditions
Preconditions(reltype="{'': '!2', 'value': 'ast.IfExp'}")
>>> rs.replacement
[{'ast.Assign': {'targets': ['!1'], 'value': '@1'}}, {'!2': {'value': '!1'}}]
>>> vrs = rs.validate()
>>> vrs
```
