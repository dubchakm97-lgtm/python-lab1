import pytest
from main import checking, correct_number, parser, operation, is_it_number_bro, right, calculate

def test_checking():
    assert checking(5.0)==5
    assert checking(6.0)==6
    assert checking(100.0)==100

def test_correct_number():
    assert correct_number('-(-4)')==4
    assert correct_number('+(5)')==5
    assert correct_number('-1')==-1

def test_parser():
    assert parser('-(4)5+ 78//3 *9 +')==['-(4)', '5', '+', '78', '//', '3', '*', '9', '+']
    assert parser('-(4)(+5) - (6)+')==['-(4)', '(+5)', '-', '(6)', '+']

def test_operation():
    stack = [5, -4, 5.2, -1]
    operation(stack, '+')
    assert stack == [5, -4, 4.2]

    with pytest.raises(ValueError, match='Числа не целые!'):
        operation([5, -4, 5.2, 0], '%')

    stack = [5, -4, 5, 2]
    operation(stack, '/')
    assert stack==[5, -4, 2.5]

def test_is_it_number_bro():
    assert is_it_number_bro('6.5')==True
    with pytest.raises(ValueError, match="Некорректно введено вещественное число"):
        is_it_number_bro('3.14.5')

def test_right():
    assert right([5, 6])==True
    assert right([5.7, 6.1])==True
    assert right([5.7])==False
    assert right(['1x', 5])==False

def test_calculate():
    assert calculate(['(-5)', '3', '*', '4', '+', '2', '/'], [])==-5.5
    assert calculate(['4.5', '(-2.5)', '+', '3', '*', '7', '/'], []) == 0.8571428571428571
    with pytest.raises(ValueError, match="Неправильно введено выражение"):
        calculate(['5', '+'], [])
