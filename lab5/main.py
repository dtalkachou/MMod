import os
import logging

import numpy as np
import pandas as pd
import markdown_generator as mg

from datetime import datetime

from system import System
from helpers import *

logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)


def generate_report(lambda_, mu, p, n, m, stats):
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = 'result_%s.md' % (datetime.now().strftime('%d%m%Y_%H%M%S'),)
    with open(os.path.join(path, filename), 'w') as f:
        doc = mg.Writer(f)
        doc.write_heading('Статистическое исследование')
        doc.writelines([
            'λ = %.2f' % lambda_, '',
            'μ = %.2f' % mu, '',
            'p = %.2f' % p, '',
            'n = %d, m = %d' % (n, m), ''
        ])

        df_c, df_times = stats.build()
        doc.writelines([
            df_c.describe().T.to_markdown(), '',
            df_times.describe().T.to_markdown(), ''
        ])

        doc.writelines([
            'Всего отклонено: %d' % stats.rejections, '',
            'Всего отменено: %d' % stats.cancellations, '',
            'Всего выполнено: %d' % len(stats.requests), ''
        ])

        states_bins, states_counts = stats.get_states_probs()

        doc.writelines([
            pd.DataFrame(data={
                'Теоретическая вероятность': get_state_probs(lambda_, p, n, m),
                'Практическая вероятность': states_counts / sum(states_counts)
            }).T.to_markdown(), ''
        ])

        cancel_prob = stats.get_cancel_prob()
        _rho = lambda_ / (mu * p)
        theor_cancel_prob = get_cancel_prob(_rho, n, m)
        relative_bandwidth = 1 - cancel_prob
        theor_relative_bandwidth = 1 - theor_cancel_prob
        absolute_bandwidth = relative_bandwidth * lambda_
        theor_absolute_bandwidth = lambda_ * theor_relative_bandwidth
        theor_queue_size = get_theor_interval_len(_rho, n, m)
        theor_channel_loaded = _rho * theor_relative_bandwidth
        theor_system_load = theor_queue_size + theor_channel_loaded

        doc.writelines([
            pd.DataFrame({
                'Вероятность отказа': [theor_cancel_prob, cancel_prob],
                'Относительная пропускная способность': [theor_relative_bandwidth, relative_bandwidth],
                'Абсолютная пропускная способность': [theor_absolute_bandwidth, absolute_bandwidth],
                'Длина очереди': [theor_queue_size, np.mean(stats.queue_sizes)],
                'Количество занятых каналов': [theor_channel_loaded, np.mean(stats.working_channels)],
                'Количество заявок в системе': [theor_system_load, np.mean(stats.total_requests)],
            }, index=['Теор.', 'Практ.']).T.to_markdown(), ''
        ])


def main():
    lambda_ = 3.55
    mu = 1.5
    p = 0.8
    n = 3
    m = 10

    system = System(n, m, lambda_, mu, p, 0.01, 10000)
    system.log()
    system.run()

    generate_report(lambda_, mu, p, n, m, system.stats)


if __name__ == '__main__':
    main()
