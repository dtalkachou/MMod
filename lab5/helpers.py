import math


def get_free_probability(p, n, m):
    p0 = 1

    for k in range(1, n + 1):
        p0 += p ** k / math.factorial(k)

    p0 += p ** (n + 1) * (1 - (p / n) ** m) / (n * math.factorial(n) * (1 - p / n))

    return 1 / p0


def get_state_probs(rho, n, m):
    p0 = get_free_probability(rho, n, m)
    probs = [p0]

    for k in range(1, n + 1):
        probs.append(rho ** k / math.factorial(k) * p0)

    for k in range(1, m + 1):
        probs.append(rho ** (n + k) / (n ** k * math.factorial(n)) * p0)

    return probs


def get_cancel_prob(p, n, m):
    p0 = get_free_probability(p, n, m)
    return p ** (n + m) / (n ** m * math.factorial(n)) * p0


def get_theor_interval_len(rho, n, m):
    p0 = get_free_probability(rho, n, m)
    return p0 * rho**(n + 1) / (n * math.factorial(n)) * sum(k * (rho / n)**(k - 1) for k in range(1, m + 1))
