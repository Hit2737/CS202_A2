# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
from algorithms.tree import path_sum2 as module_0
import builtins as module_1


def test_case_0():
    none_type_0 = None
    var_0 = module_0.path_sum(none_type_0, none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    object_0 = module_1.object()
    module_0.path_sum(object_0, object_0)


def test_case_2():
    none_type_0 = None
    var_0 = module_0.path_sum2(none_type_0, none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    int_0 = 50
    module_0.path_sum2(int_0, int_0)


def test_case_4():
    none_type_0 = None
    var_0 = module_0.path_sum3(none_type_0, none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_5():
    object_0 = module_1.object()
    module_0.path_sum3(object_0, object_0)
