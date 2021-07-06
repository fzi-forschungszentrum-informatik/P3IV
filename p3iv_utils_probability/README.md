# Probability Utilities

There are already dozens of probability libraries with diverse utility functions available as open source software. Even though these libraries are powerful, they lack several simple functionalities that a prediction and planning researcher might need. This package aims to cover these deficits.

Normal (or Gaussian) distributions are frequently used in engineering. While dealing with timely equidistant sequential data, such as Motion (or in other words 'trajectory'), one can set up mean value $\mathbf{\mu}$ and covariance matrices $\Sigma$ with all the variables. If there is no cross-correlation between the entries of the data, which is often the assumption made in our domain, the matrix is very sparse and it is inefficient to store the matrix in this form. One solution is to use sparse matrix methods, other one is to define a separate, application-specific data container.

Dealing with uncertainties necessitate performing arithmetic operations with these. For univariate distributions, the rules are pretty simple to apply whereas in higher dimensions, this becomes intractable.

This package implements data containers for such multi-variate, univariate, bivariate distributions both as single or array wise operations. It further extends them as with their truncated counterparts. It is implemented both in Python and C++, whereas the C++ implementation doesn't match the Python variant exactly: the simulation framework internally uses the Python implementation and in the current version, C++ implementation is kept for convenience. Its visualization tools are written by using Matplotlib to allow to plot these distributions easily.

Note that, probability and cumulative density functions the bivariate truncated normal distribution is experimental and may contain bugs!

## Usage

Python implementations of the distributions are done by observing multiple inheritance, allowing to derive new distribution types; such as mixture distributions. Because mro can be confusing to novice programmers in Python, some simple examples on usage are provided below.

### Arithmetic operations with normal distributions
```python
import numpy as np
from p3iv_utils_probability.distributions import UnivariateNormalDistribution


m0 = 1.0
v0 = 5.0
u0 = UnivariateNormalDistribution(mean=m0, covariance=v0)

m1 = 2.0
v1 = 3.0
u1 = UnivariateNormalDistribution(mean=m1, covariance=v1)

sum_distr = u0 + u1
sub_distr = u0 - u1
assert(isinstance(sum_distr, UnivariateNormalDistribution))
assert(isinstance(sub_distr, UnivariateNormalDistribution))

x = 1.0
y = 2.0
print(sum_distr.pdf(x, y))
print(sub_distr.pdf(x, y))
```

### Truncated univariate normal distribution
```python
import numpy as np
from p3iv_utils_probability.distributions import TruncatedUnivariateNormalDistribution


m0 = 1.0
v0 = 5.0
u0 = TruncatedUnivariateNormalDistribution(
    mean=m, covariance=v, lower_truncation=0, upper_truncation=4
)
lower, upper = u0.range(2)

print(("\nUpper bound : {}\n".format(upper)))
print(("\nLower bound : {}\n".format(lower)))

print(u0.pdf(3.0))
print(u0.cdf(5.0))

```


### Bivariate normal distribution

```python
import numpy as np
from p3iv_utils_probability.distributions import BivariateNormalDistribution


m0 = np.array([[1, 2]])
v0 = np.array([[5, 0], [0, 1]])
t0 = BivariateNormalDistribution(mean=m0, covariance=v0)
# this will return the mean values and ellipse parameters of 1-sigma region
t0.range(1)
# array([1., 2., 0., 2.23606798, 1.])
```

### Bivariate distribution sequence
```python
import numpy as np
from p3iv_utils_probability.distributions import BivariateNormalDistributionSequence


m = np.array([[1, 0], [2, 2], [3, 3]])
v = np.array([[[5, 0], [0, 1]], [[3, 0], [0, 3]], [[1, 0], [0, 1]]])
distribution = BivariateNormalDistributionSequence()
distribution.resize(3)
distribution.mean = m
distribution.covariance = v
print(distribution)

```
## Requirements

```
scipy>=1.2.1
```

## Misc

### [Doxygen documentation](http://tas.private.MRT.pages.mrt.uni-karlsruhe.de/util_probability/doxygen/index.html)
### [Coverage report](http://tas.private.MRT.pages.mrt.uni-karlsruhe.de/util_probability/coverage/index.html)
