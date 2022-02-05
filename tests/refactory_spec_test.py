import ast

from pytest import mark

from refactory.namespacing.alias import Alias
from refactory.namespacing.ast_ns import KwargName
from refactory.namespacing.literal import StringLiteral
from refactory.patterns.early_returns import ReplaceAnonRetVal
from refactory.spec import load_spec

dict_aliasval = {ast.Name: {KwargName("id"): StringLiteral("output")}}


@mark.parametrize("val1,val2", [(dict_aliasval, ast.Return)])
@mark.parametrize("spec,n_subs", [(ReplaceAnonRetVal, 2)])
def test_load_spec_multi_replace_with_string_literal_id(spec, n_subs, val1, val2):
    rs = load_spec(spec)
    assert [*rs.aliases] == [repr(Alias(k)) for k in rs.aliases]
    assert [a.alias_val for a in [*rs.aliases.values()]] == [val1, val2]

    assert rs.preconditions.reltype  # Do something with it
    assert len(rs.replacement) == n_subs
