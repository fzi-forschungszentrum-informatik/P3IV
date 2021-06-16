import numpy as np
import warnings


class Mixture(object):
    def __init__(self, *args, **kwargs):
        """
        A mixture of probability distributions
        :param weights: weights of the components of the mixture
        :param args: [truncation_upper_array, truncation_lower_array]
        :param kwargs: "mean", "covariance", "mixture_data_type", "components"
        """

        self.components = []  # Contains the GaussianData components of the mixture
        self.data_length = None
        self.nr_of_components = 0
        self.weights = []
        self.__mixture_data_type = None
        self._mean = None  # one row represents a one gaussian. Will be an array of arrays (2D).
        self._covariance = None  # one row represents a one gaussian.

        if all(i in list(kwargs.keys()) for i in ["mixture_data_type", "weights", "mean", "covariance"]):
            """
            if len(kwargs["mean"].shape) == 1:
                kwargs["mean"] = np.expand_dims(kwargs["mean"], axis=0)
            if len(kwargs["covariance"].shape) == 1:
                kwargs["covariance"] = np.expand_dims(kwargs["covariance"], axis=0)
            assert len(kwargs["mean"].shape) == 2
            assert kwargs["mean"].shape == kwargs["covariance"].shape
            assert len(kwargs["weights"]) == kwargs["mean"].shape[0] >= 1
            """
            self._set_properties_of_distribution(*args, **kwargs)
        elif "components" in list(kwargs.keys()):
            assert len(kwargs["weights"]) == len(kwargs["components"]) >= 1
            self._set_distribution_components(kwargs["weights"], kwargs["components"])
        elif len(kwargs["weights"]) < 1:
            raise Exception("Weights not specified!")
        else:
            raise Exception("Mixture data cannot be created")

        if np.sum(kwargs["weights"]) != 1.0:
            text = "Weights of the mixture does not sum to 1, but to : " + str(np.sum(kwargs["weights"]))
            raise Exception(text)
        elif len(kwargs["weights"]) == 1:
            warnings.warn("This is not a MixtureData; it has a single component")

    def _set_properties_of_distribution(self, *args, **kwargs):
        self.__mixture_data_type = kwargs["mixture_data_type"]
        self.weights = kwargs["weights"]  # weights of the mixture components
        self._mean = np.asarray(kwargs["mean"])  # one row represents a one gaussian.
        self._covariance = np.asarray(kwargs["covariance"])  # one row represents a one gaussian.
        self.data_length = self._mean.shape[-1]
        self.nr_of_components = len(self.weights)

        self._create_components(*args)

    def _set_distribution_components(self, weights, components):

        self.__mixture_data_type = type(components[0])
        self.weights = weights
        self.components = components

        self.data_length = components[0].mean.shape[-1]
        self.nr_of_components = len(self.weights)
        self._mean = np.empty([len(components), self.data_length])
        self._covariance = np.empty([len(components), self.data_length])
        for i in range(len(components)):
            self._mean[i, :] = components[i].mean
            self._covariance[i, :] = components[i].covariance

    def range(self, sigma):
        """
        Returns the bounds of all components
        """
        bounds = []
        for c in self.components:
            bounds.append(c.range(sigma))
        return np.asarray(bounds)

    def _create_components(self, *args):
        """
        Set the components that build up the mixture. Store them in self.components
        :param args: a list which comprises upper and lower truncation array for each comp.
        :return:
        """

        self.components = []
        for i in range(len(self.weights)):

            if args:
                new_args = [a[i] for a in args]
                self.components.append(
                    self.__mixture_data_type(*new_args, mean=self._mean[i], covariance=self._covariance[i])
                )
                continue

            self.components.append(self.__mixture_data_type(*args, mean=self._mean[i], covariance=self._covariance[i]))

    def cdf(self, idx, x):
        cdf_comp = np.array([comp.cdf(idx, x) for comp in self.components])

        return np.sum(self.weights * cdf_comp)

    def __str__(self):
        l1 = "%s\n" % (str(type(self).__name__))
        l2 = "Has %s components\n" % (str(self.nr_of_components))
        l3 = "With weights : %s" % (str(self.weights))
        return l1 + l2 + l3

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        self._mean = mean
        self._create_components()

    @property
    def covariance(self):
        return self._covariance

    @covariance.setter
    def covariance(self, covariance):
        self._covariance = covariance
        self._create_components()
