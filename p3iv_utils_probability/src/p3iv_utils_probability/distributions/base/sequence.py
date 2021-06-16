import numpy as np
import operator
from copy import deepcopy


class DistributionSequence(object):
    def __init__(self, dtype, *args, **kwargs):
        # set dtype value before super(); covariance check in inheritance uses this!
        self.dtype = dtype
        super(DistributionSequence, self).__init__(*args, **kwargs)

        self._n = 0

        if self.dtype.dim is 1:
            self._mean = np.array([])
            self._covariance = np.array([])
        else:
            self._mean = np.array([]).reshape(-1, self.dtype.dim)
            self._covariance = np.array([]).reshape(-1, self.dtype.dim, self.dtype.dim)

        self._components = np.empty(self._n, dtype=dtype)

    def __len__(self):
        return self._n

    def __getitem__(self, key):

        if isinstance(key, slice):
            dist = deepcopy(self)
            dist._mean = self._mean[key]
            dist._covariance = self._covariance[key]
            dist._n = len(dist._mean)
        elif isinstance(key, int):
            dist = self.__class__()
            dist.resize(1)
            dist.mean[0] = self._mean[key]
            dist.covariance[0] = self._covariance[key]
        else:
            raise Exception

        return dist

    def __repr__(self):
        return "Mean:\n%s\nCoVariance:\n%s\nLength:\n%s\n" % (str(self._mean), str(self._covariance), str(len(self)))

    def resize(self, n):
        self._n = n
        self._components = np.empty(self._n, dtype=self.dtype)

        if self.dtype.dim is 1:
            self._mean = np.zeros(n)
            self._covariance = np.zeros(n)
        else:
            self._mean = np.zeros(n * self.dtype.dim).reshape(-1, self.dtype.dim)
            self._covariance = np.zeros(n * self.dtype.dim * self.dtype.dim).reshape(-1, self.dtype.dim, self.dtype.dim)

    def size(self):
        return self._n

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        assert self._n == len(mean)
        if self.dtype.dim is 1:
            assert len(mean.shape) == 1
            self._mean = mean
        else:
            assert mean.shape == self._mean.shape
            self._mean = mean

    @property
    def covariance(self):
        return self._covariance

    @covariance.setter
    def covariance(self, covariance):
        assert self._n == len(covariance)
        if self.dtype.dim is 1:
            assert len(covariance.shape) == 1
            self._covariance = covariance
        else:
            assert covariance.shape == self._covariance.shape
            self._covariance = covariance

    @property
    def components(self):
        self._update_components()
        return self._components

    @components.setter
    def components(self, components):
        assert self._n == len(components)
        self._components = components
        if self.dtype.dim is 1:
            self._mean = np.empty([self._n])
            self._covariance = np.empty([self._n])
            for i in range(len(components)):
                self._mean[i] = components[i].mean[0, 0]
                self._covariance[i] = components[i].covariance[0, 0]
        else:
            self._mean = np.empty([self._n, self.dtype.dim])
            self._covariance = np.empty([self._n, self.dtype.dim, self.dtype.dim])
            for i in range(len(components)):
                self._mean[i] = components[i].mean
                self._covariance[i] = components[i].covariance

    def range(self, sigma):
        bounds = self.size() * [None]
        for i in range(self.size()):
            bounds[i] = self.components[i].range(sigma)
        return np.asarray(bounds)

    def append(self, other):
        assert isinstance(other, DistributionSequence)
        assert self.dtype.dim == other.dtype.dim
        self._n = len(self) + len(other)
        if self.dtype.dim is 1:
            self._mean = np.append(self._mean, other._mean)
            self._covariance = np.append(self._covariance, other._covariance)
            # are updated by the components.getter!
            # efficiency can be improved!
        else:
            self._mean = np.vstack([self._mean, other._mean])
            self._covariance = np.vstack([self._covariance, other._covariance])

    def _update_components(self):
        self._components = np.empty(self._n, dtype=self.dtype)
        for i in range(self._mean.shape[0]):
            self._components[i] = self.dtype(mean=self._mean[i], covariance=self._covariance[i])

    def _get_bound(self, operation, sigma):
        if self.dtype.dim is 1:
            m_dim_cov = self._mean
        else:
            m_dim_cov = np.expand_dims(self._mean, axis=1)
        return operation(m_dim_cov, self._covariance * sigma)
