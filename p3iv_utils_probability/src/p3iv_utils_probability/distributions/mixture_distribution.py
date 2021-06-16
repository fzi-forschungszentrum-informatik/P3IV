import numpy as np
import warnings
from p3iv_utils_probability.distributions.base import DistributionSequence, Mixture
from .univariate_distribution import UnivariateNormalDistribution
from .sequence_distribution import UnivariateNormalDistributionSequence, TruncatedUnivariateNormalDistributionSequence
from .truncated_distribution import TruncatedUnivariateNormalDistribution


class UnivariateNormalMixtureDistribution(Mixture):
    def __init__(self, **kwargs):
        """
        A mixture of Univariate Normal distribution.
        """
        super(UnivariateNormalMixtureDistribution, self).__init__(
            mixture_data_type=UnivariateNormalDistribution, **kwargs
        )


class TruncatedUnivariateNormalMixtureDistribution(Mixture):
    def __init__(self, *args, **kwargs):
        """
        A mixture of Truncated Univariate Normal distribution.
        """
        super(TruncatedUnivariateNormalMixtureDistribution, self).__init__(
            mixture_data_type=TruncatedUnivariateNormalDistribution, *args, **kwargs
        )


class UnivariateNormalSequenceMixtureDistribution(Mixture):
    def __init__(self, **kwargs):
        """
        A mixture of Univariate Normal distribution.
        """
        super(UnivariateNormalSequenceMixtureDistribution, self).__init__(
            mixture_data_type=UnivariateNormalDistributionSequence, **kwargs
        )


class TruncatedUnivariateNormalSequenceMixtureDistribution(Mixture):
    def __init__(self, **kwargs):
        """
        A mixture of Univariate Normal distribution.
        """
        super(TruncatedUnivariateNormalSequenceMixtureDistribution, self).__init__(
            mixture_data_type=TruncatedUnivariateNormalDistributionSequence, **kwargs
        )
