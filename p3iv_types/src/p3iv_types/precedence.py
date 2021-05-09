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
