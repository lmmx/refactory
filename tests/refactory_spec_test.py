from pytest import fixture, mark

import refactory
from refactory.spec import load_spec
from refactory.patterns.early_returns import ReplaceAnonRetVal


@mark.parametrize("spec,n_aliases,n_subs", [(ReplaceAnonRetVal, 2, 2)])
def test_load_spec_multi_replace_with_string_literal_id(spec, n_aliases, n_subs):
    rs = load_spec(spec)
    assert len(rs.aliases) == n_aliases
    assert rs.preconditions.reltype # Do something with it
    assert len(rs.replacement) == n_subs
