import logging

import numpy as np
import pandas as pd

from channel import Channel
from request import Request


class Stats:
    def __init__(self, smo):
        self.smo = smo

        self.queue_sizes = []
        self.working_channels = []
        self.total_requests = []
        self.requests = []
        self.request_queue_times = []
        self.request_times = []

        self.work_intervals = []
        self.process_intervals = []

        self.rejections = 0
        self.cancellations = 0

    def collect(self):
        cur_working_channels = 0
        for channel in self.smo.channels:
            cur_working_channels += not channel.free

        cur_queue_size = len(self.smo.queue)

        self.queue_sizes.append(cur_queue_size)
        self.working_channels.append(cur_working_channels)
        self.total_requests.append(cur_queue_size + cur_working_channels)

    def cancel(self):
        self.cancellations += 1

    def reject(self):
        self.rejections += 1

    def add_work(self, interval):
        self.work_intervals.append(interval)

    def add_process(self):
        self.process_intervals.append(self)

    def out(self, request):
        self.requests.append(request)
        self.request_queue_times.append(request.time_in_queue)
        self.request_times.append(request.time_in_system)

    def build(self):
        d = {'Размер очереди': self.queue_sizes,
             'Занятые каналы': self.working_channels,
             'Заявки в системе': self.total_requests}

        d1 = {'Время запроса в очереди': self.request_queue_times,
              'Время запроса в системе': self.request_times}

        return pd.DataFrame(data=d), pd.DataFrame(data=d1)

    def get_cancel_prob(self):
        return self.cancellations / self.smo.request_limit

    def get_states_probs(self):
        states = [0]  # система пуста
        states += list(range(1, self.smo.n + 1))  # работают каналы
        states += list(range(self.smo.n + 1, self.smo.n + self.smo.m + 1))  # работают каналы и занята очередь

        state_counts = np.zeros(len(states))

        for req in self.total_requests:
            state_counts[req] += 1

        return states, state_counts


class System:
    def __init__(self, n, m, lambda_, mu, p, tick_size, request_limit):
        self.n = n
        self.m = m
        self.lambda_ = lambda_
        self.mu = mu
        self.p = p
        self.q = 1 - p
        self.tick_size = tick_size
        self.request_limit = request_limit

        self.stats = Stats(self)

        self.request = 0
        self.channels = [
            Channel(self.mu, self.q, self.request_rejected) for _ in range(n)
        ]
        self.queue = []
        self.cur_time = 0.
        self.next_time = np.random.exponential(lambda_)

    def log(self):
        logging.info('Текущее время %.4f, следующий запрос поступит %.4f' %
                     (self.cur_time, self.next_time))

    def request_rejected(self):
        self.stats.reject()

    def push(self, request=None):
        if not request:
            self.request += 1
            request = Request(self.cur_time)

        if len(self.queue) < self.m:
            request.enqueue(self.cur_time)
            self.queue.append(request)
        else:
            self.stats.cancel()
            logging.info('[Отменён] %s' % (request, ))

    def free_channels(self):
        for channel in self.channels:
            request = channel.try_free(self.cur_time)
            if request:
                request.out(self.cur_time)
                self.stats.out(request)

    def dequeue_requests(self):
        for channel in self.channels:
            if not len(self.queue):
                return

            if channel.free:
                request = self.queue.pop(0)
                request.dequeue(self.cur_time)
                channel.run(self.cur_time, request)

    def free_all(self):
        while not self.is_all_free():
            self.tick()

    def is_all_free(self):
        for channel in self.channels:
            if not channel.free:
                return False
        return True

    def tick(self):
        self.free_channels()
        self.dequeue_requests()
        self.stats.collect()

        self.cur_time += self.tick_size

    def run(self):
        while self.request < self.request_limit:
            if self.cur_time >= self.next_time:
                self.next_time = self.cur_time + \
                                 np.random.exponential(1 / self.lambda_)
                self.push()
                self.log()

            self.tick()

        self.free_all()
