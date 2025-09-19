def soma(a, b):
    return a + b

def subtrai(a, b):
    return a - b

def multiplica(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Divisão por zero!")
    return a / b

def eh_par(n):
    return n % 2 == 0

def test_soma():
    assert soma(2, 3) == 5

def test_subtrai():
    assert subtrai(7, 4) == 3

def test_multiplica():
    assert multiplica(3, 5) == 15

def test_divide():
    assert divide(10, 2) == 5

def test_divide_zero():
    import pytest
    with pytest.raises(ValueError):
        divide(5, 0)

def test_eh_par_true():
    assert eh_par(4) is True

def test_eh_par_false():
    assert eh_par(5) is False
