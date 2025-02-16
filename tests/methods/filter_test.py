from testing import greater_than_four


def test_ml_empty(ml_empty):
    assert ml_empty.filter(greater_than_four) == ml_empty


def test_ml_with_one_int_truthy(ml_with_one_int_truthy):
    assert ml_with_one_int_truthy.filter(bool) == ml_with_one_int_truthy


def test_ml_with_one_int_falsy(ml_with_one_int_falsy):
    assert ml_with_one_int_falsy.filter(bool) == list([])
