import sys


def checking(number: float | int) -> int | float:
    """
    Убирает .0 в целом числе которое программа интерпретирует как дробное,
    возвращает то же число, только целое

    :param number: Дробное число вида X.0, где Х – целая часть числа, либо уже заведомо целое число
    :return: То же число, только в целом виде с точки зрения python, либо то же дробное число, если оно действительно дробное
    """
    if len(str(number)) >= 2 and str(number)[-2] == '.' and str(number)[-1] == '0':
        return int(str(number)[:-2])
    else:
        return number


def correct_number(
        number: str) -> int | float:  # на вход подаётся токен-число со скобками и унарными знаками, возвращает число без скобок и унарных знаков
    """
    На вход подаётся токен-число в виде строки со скобками и унарными знаками, возвращается число без скобок и унарных знаков

    :param number: Строковое число со скобками и унарными знаками
    :return: То же число типа int или float без скобок и унарных знаков
    (в крайнем случае число может возвращаться только с одним унарным минусом)
    """
    if number.count('-') % 2 == 0:
        if '.' in number:
            return float(number.replace('(', '').replace(')', '').replace('-', '').replace('+', ''))
        else:
            return int(number.replace('(', '').replace(')', '').replace('-', '').replace('+', ''))
    else:
        if '.' in number:
            return -float(number.replace('(', '').replace(')', '').replace('-', '').replace('+', ''))
        else:
            return -int(number.replace('(', '').replace(')', '').replace('-', '').replace('+', ''))


def parser(string: str) -> list[str]:
    """
    На вход подаётся строка, введённая пользователем с клавиатуры уже в ОПЗ, возвращается список операндов и бинарных операций

    :param string: строка, введённая пользователем с клавиатуры в ОПЗ
    :return: список операндов и бинарных операций
    """
    base_parser = ' '  # основной парсер, который будет являться строкой с пробелами между операциями и операндами
    if len(string) % 2 == 1:  # поскольку идем по строке и парсим её попарными символами, то проверяем четность кол-ва элементов в изначальной строке
        string += ' '
    for t in range(1, len(string), 2):  # парсим строку и записываем её в основной парсер base_parser
        # слияние // или ** 2
        if (string[t - 1] == '/' and base_parser[-1] == '/') or (string[t - 1] == '*' and base_parser[-1] == '*'):
            base_parser += string[t - 1] + ' ' + string[t]
            continue
        # слияние двух остальных знаков 2
        if (string[t - 1] in '%+-' and base_parser[-1] in '%+-*/') or (
                string[t - 1] in '%+-*/' and base_parser[-1] in '%+-'):
            base_parser += ' '
        # слияние скобки и знака 2
        if (string[t - 1] == '(' and base_parser[-1] in '%*/') or (string[t - 1] in '%*+-/' and base_parser[-1] == ')'):
            base_parser += ' '
        # слияние числа и знака 2
        if (base_parser[-1] in '0123456789' and string[t - 1] in '+-*/%') or (
                base_parser[-1] in '*/%' and string[t - 1] in '0123456789'):
            base_parser += ' '
        # слияние двух )( скобок 2
        if (base_parser[-1] == ')' and string[t - 1] == '('):
            base_parser += ' '
        # слияние скобки и числа 2
        if (base_parser[-1] == ')' and string[t - 1] in '0123456789') or (
                base_parser[-1] in '0123456789' and string[t - 1] == '('):
            base_parser += ' '
        # слияние скобки и знака 1
        if (string[t] == '(' and string[t - 1] in '%*/') or (string[t] in '%*+-/' and string[t - 1] == ')'):
            base_parser += string[t - 1] + ' ' + string[t]
        # слияние двух остальных знаков 1
        elif (string[t - 1] in '%+-*/' and string[t] in '%+-') or (string[t - 1] in '%+-' and string[t] in '%+-*/'):
            base_parser += string[t - 1] + ' ' + string[t]
        # слияние числа и знака 1
        elif (string[t - 1] in '*/%' and string[t] in '0123456789') or (
                string[t - 1] in '0123456789' and string[t] in '+-*/%'):
            base_parser += string[t - 1] + ' ' + string[t]
        # слияние двух )( скобок 1
        elif (string[t - 1] == ')' and string[t] == '('):
            base_parser += string[t - 1] + ' ' + string[t]
        # слияние // или ** 1
        elif (string[t - 1] == '/' and string[t] == '/') or (string[t - 1] == '*' and string[t] == '*'):
            base_parser += ' ' + string[t - 1] + string[t]
        # слияние скобки и числа 1
        elif (string[t - 1] == ')' and string[t] in '0123456789') or (
                string[t - 1] in '0123456789' and string[t] == '('):
            base_parser += string[t - 1] + ' ' + string[t]
        # общий случай
        else:
            base_parser += string[t - 1] + string[t]
    return base_parser.split()  # разбиваем парсер по пробелам, ведь теперь мы её исправили и добавили нужные пробелы


def operation(stack: list[int | float], item: str) -> None:
    """
    В функцию передаём стек чисел и бинарную операцию ('+', '-', '*', '/', '//', '%', '**'),
    функция берёт два последних числа из стека, применяет бинарную операцию над ними,
    результат кладёт в конец стека вместо двух последних элементов, ничего не возвращая

    :param stack: список чисел
    :param item: бинарная операция
    :return: функция ничего не возвращает, а лишь изменяет стек
    """
    if item == '+':
        result = stack[-2] + stack[-1]
        stack.pop(-1)
        stack.pop(-1)
        stack.append(result)
    elif item == '-':
        result = stack[-2] - stack[-1]
        stack.pop(-1)
        stack.pop(-1)
        stack.append(result)
    elif item == '*':
        result = stack[-2] * stack[-1]
        stack.pop(-1)
        stack.pop(-1)
        stack.append(result)
    elif item == '/':
        try:  # проверка на деление на 0
            result = stack[-2] / stack[-1]
            stack.pop(-1)
            stack.pop(-1)
            stack.append(checking(result))
        except ZeroDivisionError:
            raise ZeroDivisionError("Делить на ноль нельзя!")
    elif item == '//':
        try:  # проверка того, что делитель — не 0
            if type(stack[-2]) == int and type(stack[-1]) == int:  # проверка на то, что числа целые
                result = int(stack[-2]) // int(stack[-1])
                stack.pop(-1)
                stack.pop(-1)
                stack.append(result)
            else:
                raise ValueError("Ошибка! Числа не целые!")
        except ZeroDivisionError:
            raise ZeroDivisionError("Делить на ноль нельзя!")
    elif item == '%':
        try:
            if type(stack[-2]) == int and type(stack[-1]) == int:  # проверка того, что числа целые
                result = int(stack[-2]) % int(stack[-1])
                stack.pop(-1)
                stack.pop(-1)
                stack.append(result)
            else:
                raise ValueError("Ошибка! Числа не целые!")
        except ZeroDivisionError:
            raise ZeroDivisionError("Делить на ноль нельзя!")
    elif item == '**':
        result = stack[-2] ** stack[-1]
        stack.pop(-1)
        stack.pop(-1)
        stack.append(result)


def is_it_number_bro(item: str) -> bool:
    """
    Функция проверяет, является ли передаваемый элемент item числом, в функцию передается строковое число,
    возвращаются булевы значения True, если в строке находится число, False, если знак

    :param item: строковое число
    :return: булево значение
    """
    if item.count('.') > 1:
        raise ValueError("Некорректно введено вещественное число")
    return item.replace('.', '').replace('-', '').replace(')', '').replace('(', '').replace('+', '').isdigit()


def right(stack: list) -> bool:
    """
    Функция на вход принимает стек чисел и проверяет, что количество чисел в нем больше 1 и никаких токенов-букв нет,
    только в таком случае можно применить бинарную операцию, иначе программа останавливается
    :param stack: стек чисел
    :return: булево значение
    """
    return len(stack) > 1 and (type(stack[-2]) == float or type(stack[-2]) == int) and (
            type(stack[-1]) == float or type(stack[-1]) == int)


def calculate(tokens: list[str], stack: list[int | float]) -> int | float:
    """
    Функция на вход получает список операндов и бинарных операций, а также пустой стек, в который она будет складывать
    числа из списка токенов, если в стеке лежат числа (проверяется функцией is_it_number_bro()), и применять к ним бинарные
    операции, предварительно проверив, не имеет ли число вид х.0, где х - целая часть числа; перед применением бинарной
    операции проверяется, что в стеке есть хотя бы два числа (функция right()), после проверки операция выполняется с помощью
    функции operation()

    :param tokens: список операндов и бинарных операций
    :param stack: пустой список, в который будут складываться все числа
    :return: единственное число оставшееся в стеке
    """
    for item in tokens:  # идём по массиву операндов и операций
        if is_it_number_bro(item):  # проверка того, что текущий элемент является числом
            stack.append(correct_number(item))  # кладём числа в стек
        else:  # если текущий элемент в цикле — операция, то вызываем функцию применения бинарной операции над двумя последними операндами в стеке
            if right(stack):  # проверка того, что в стеке есть хотя бы два числа и нет неизвестных токенов
                operation(stack, item)
            else:  # иначе программа останавливается
                raise ValueError('Неправильно введено выражение')
    if len(stack) > 1:  # проверка того, что в стеке осталось 1 число и,
        # соответственно, количество бинарных операций в парсере было ровно на одно меньше чем чисел
        raise ValueError('Неправильно введено выражение')
    return stack[0]  # выводим оставшийся элемент стека, который является результатом выражения


def main() -> None:
    """
    Основная часть программы-калькулятора, которая выводит результат вычисления функции calculate, в которую передается
    результат вычисления функции parser, в которую на вход подаётся выражение, вводимое с клавиатуры пользователем
    :return: None
    """
    string, stack = input(), []  # вводимая строка с клавиатуры и пока что пустой стек чисел
    tokens = parser(string)
    try:
        print(calculate(tokens, stack))
    except ValueError as mistake:
        print(f"{mistake}")
    except ZeroDivisionError as mistake:
        print(f"{mistake}")


if __name__ == "__main__":
    main()
