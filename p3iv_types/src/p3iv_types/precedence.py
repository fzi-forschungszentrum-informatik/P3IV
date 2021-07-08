# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)


class Precedence(object):
    def __int__(self, priority=None, give_way=None):
        if priority is None:
            priority = []
        if give_way is None:
            give_way = []

        for v in priority + give_way:
            isinstance(v, str)

        self.priority = priority
        self.give_way = give_way
