
from pytest import mark

from refactory.namespacing.alias import Alias
from refactory.namespacing.ast_ns import AstStatement, KwargName
from refactory.namespacing.literal import StringLiteral
from refactory.patterns.early_returns import ReplaceAnonRetVal
from refactory.spec import load_spec

dict_aliasval_key = AstStatement("ast.Name")
dict_aliasval_val = {KwargName("id"): StringLiteral("output")}


@mark.parametrize(
    "val1k,val1v,val2",
    [(dict_aliasval_key, dict_aliasval_val, AstStatement("ast.Return"))],
)
@mark.parametrize("spec,n_subs", [(ReplaceAnonRetVal, 2)])
def test_load_spec_multi_replace_with_string_literal_id(
    spec, n_subs, val1k, val1v, val2
):
    rs = load_spec(spec)
    assert [*rs.aliases] == [Alias(f"!{a.idx}") for a in rs.aliases]
    rs_alias_1, rs_alias_2 = rs.aliases.values()
    [(rsa_1_k, rsa_1_v)] = rs_alias_1.alias_val.items()
    assert rsa_1_k == val1k
    assert rsa_1_v == val1v
    assert rs_alias_2.alias_val == val2

    assert rs.preconditions.reltype  # Do something with it
    assert len(rs.replacement) == n_subs
