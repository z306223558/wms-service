# coding=utf-8
from task.constants import TaskType

import time
import random


class FunctionUtils(object):

    def generate_order_number(self, order_type):
        return 'L{}MS{}{}{}S{}8'.format(self.generate_db_table_router(),
                                        self.generate_db_table_router(),
                                        self._generate_sign_key_by_type(order_type),
                                        int(round(time.time() * 1000)),
                                        ''.join(random.sample('0123456789', 4)))

    @staticmethod
    def _generate_sign_key_by_type(order_type):
        return TaskType.ORDER_PREFIX[order_type - 1]

    @staticmethod
    def generate_db_table_router():
        return ''.join(random.sample('01234', 2))
