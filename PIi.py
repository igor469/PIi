import configparser
import logging
import time
from decimal import Decimal, getcontext


def read_config(path: str):
    """Считывает параметры N и L из файла конфигурации."""
    parser = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
    parser.read(path, encoding='utf-8')
    n = parser.getint('Main', 'N')
    l = parser.getint('Main', 'L')
    return n, l


def validate_params(n: int, l: int):
    """Проверяет диапазоны параметров."""
    if not (1 <= n <= 1000000):
        raise ValueError('N должен быть от 1 до 1000000')
    if not (1 <= l <= 100):
        raise ValueError('L должен быть от 1 до 100')


def compute_pi(n: int) -> str:
    """Вычисляет число Pi с помощью формулы Чудновских."""
    # Устанавливаем точность немного больше требуемой
    getcontext().prec = n + 5
    C = 426880 * Decimal(10005).sqrt()
    M = 1
    L = 13591409
    X = 1
    K = 6
    S = Decimal(L)

    for i in range(1, n // 14 + 1):
        M = (K**3 - 16 * K) * M // (i**3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12

    pi = C / S
    # Возвращаем только N знаков после запятой
    return format(pi, f'.{n}f')[2:]


def write_result(digits: str, l: int, path: str):
    """Записывает вычисленные знаки числа Pi в файл по L знаков в строке."""
    with open(path, 'w', encoding='utf-8') as f:
        for i in range(0, len(digits), l):
            f.write(digits[i:i + l] + '\n')


if __name__ == '__main__':
    logging.basicConfig(
        filename='PIi.log',
        level=logging.INFO,
        format='%(asctime)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logging.info('Старт программы')
    print('Старт программы')

    try:
        n, l = read_config('PIi.ini')
        validate_params(n, l)
    except Exception as e:
        logging.error('Ошибка чтения параметров: %s', e)
        raise

    start_calc = time.time()
    logging.info('Начало вычисления числа Pi')

    digits = compute_pi(n)

    end_calc = time.time()
    logging.info('Завершено вычисление числа Pi')

    write_result(digits, l, 'PIi.prn')

    elapsed = end_calc - start_calc
    if n > 0:
        est_million = elapsed / n * 1_000_000
    else:
        est_million = 0.0

    logging.info('Время для вычисления 1 млн знаков Pi: %.2f секунд', est_million)
    logging.info('Завершение программы')
    print('Завершение программы')
