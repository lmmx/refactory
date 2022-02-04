"""
Rule spec for the replacement rule to replace an anonymous return value with an
assignment to the named variable ``output`` and then returned.
"""

__all__ = ["ReplaceAnonRetVal"]

ReplaceAnonRetVal = {
    "aliases": {
        "!1": {"ast.Name": {"id": "${output}"}},
        "!2": "ast.Return",
    },
    "preconditions": {
        "reltype": {
            "": "!2",
            "value": "ast.IfExp",
        }
    },
    "replacement": [
        {
            "ast.Assign": {
                "targets": ["!1"],
                "value": "@1",
            }
        },
        {"!2": {"value": "!1"}},
    ],
}
