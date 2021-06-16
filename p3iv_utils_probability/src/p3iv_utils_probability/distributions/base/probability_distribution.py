import abc


class ProbabilityDistribution(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(ProbabilityDistribution, self).__init__()

    @abc.abstractmethod
    def mean(self, *args):
        pass

    @abc.abstractmethod
    def covariance(self, *args):
        pass

    @abc.abstractmethod
    def pdf(self, *args):
        pass

    @abc.abstractmethod
    def cdf(self, *args):
        pass
