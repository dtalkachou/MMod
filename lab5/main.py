import logging

from request import Request

from system import System

logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)


def main():
    lambda_ = 3.55
    mu = 1.5
    p = 0.8
    m = 10
    n = 3

    system = System(n, m, lambda_, mu, p, 0.01, 10000)
    system.log()
    system.run()


if __name__ == '__main__':
    main()
