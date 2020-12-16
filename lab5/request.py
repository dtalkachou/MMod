import logging


class Request:
    TOTAL = 0

    def __init__(self, cur_time):
        Request.TOTAL += 1
        self.id = Request.TOTAL
        self.time_in_queue = 0
        self.time_in_system = 0
        self.start_in_queue = cur_time
        self.start_in_system = cur_time

    def enqueue(self, cur_time):
        self.start_in_queue = cur_time
        logging.info('[Поступил] Запрос #%d в %s' % (self.id, cur_time))

    def dequeue(self, cur_time):
        self.time_in_queue += cur_time - self.start_in_queue
        logging.info('[Выполнен] Запрос #%d в %s' % (self.id, cur_time))

    def out(self, cur_time):
        self.time_in_system += cur_time - self.start_in_system

    def __str__(self):
        return 'Запрос #%d: в очереди %.4f, в системе %.4f' % \
               (self.id, self.time_in_queue, self.time_in_system)
