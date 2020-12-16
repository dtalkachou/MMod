import logging

import numpy as np


class Channel:
    TOTAL_COUNT = 0

    def __init__(self, mu, reject_probability, on_reject):
        Channel.TOTAL_COUNT += 1
        self.id = Channel.TOTAL_COUNT

        self.reject_probability = reject_probability
        self.on_reject = on_reject
        self.mu = mu

        self.free = True
        self.end_at = 0
        self.request = None

    def run(self, start_at, request):
        self.free = False
        self.end_at = start_at + np.random.exponential(1 / self.mu)
        self.request = request
        logging.info('[Стартовал] Канал #%d: с %.4f до %.4f' %
                     (self.id, start_at, self.end_at))

    def try_free(self, cur_time):
        if not self.free and self.end_at < cur_time:
            self.free = True

            rejected = np.random.uniform() <= self.reject_probability
            if rejected:
                self.on_reject()
                self.run(cur_time, self.request)
                logging.info('[Отклонено] Канал #%d: освободится в %.4f' %
                             (self.id, cur_time))
            else:
                logging.info('[Выполнено] Канал #%d: осободился в %.4f' %
                             (self.id, cur_time))
                return self.request
