# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
from algorithms.tree import max_path_sum as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    var_0 = module_0.helper(none_type_0, none_type_0)
    assert var_0 == 0
    module_0.max_path_sum(var_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = "q3fxy"
    module_0.helper(str_0, str_0)


@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b"\xe4\xdf\x06\x16\x18\xae\xe6\xa2\xa4;"
    module_0.max_path_sum(bytes_0)
