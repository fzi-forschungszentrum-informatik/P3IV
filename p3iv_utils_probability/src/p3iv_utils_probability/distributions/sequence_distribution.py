from p3iv_utils_probability.distributions.base import DistributionSequence
from p3iv_utils_probability.distributions.univariate_distribution import UnivariateNormalDistribution
from p3iv_utils_probability.distributions.bivariate_distribution import BivariateNormalDistribution
from p3iv_utils_probability.distributions.truncated_distribution import TruncatedUnivariateNormalDistribution


class UnivariateNormalDistributionSequence(DistributionSequence, UnivariateNormalDistribution):
    def __init__(self, *args, **kwargs):
        super(UnivariateNormalDistributionSequence, self).__init__(dtype=UnivariateNormalDistribution, *args, **kwargs)


class BivariateNormalDistributionSequence(DistributionSequence, BivariateNormalDistribution):
    def __init__(self, *args, **kwargs):
        super(BivariateNormalDistributionSequence, self).__init__(dtype=BivariateNormalDistribution, *args, **kwargs)


class TruncatedUnivariateNormalDistributionSequence(DistributionSequence, TruncatedUnivariateNormalDistribution):
    def __init__(self, *args, **kwargs):
        super(TruncatedUnivariateNormalDistributionSequence, self).__init__(
            dtype=TruncatedUnivariateNormalDistribution, *args, **kwargs
        )
