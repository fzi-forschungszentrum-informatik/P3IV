#pragma once

#include <cassert>
#include <cmath>
#include <vector>


namespace util_probability {


template <class T>
static inline T abs(const T& a) {
    return a < T(0.0) ? -a : a;
}


inline double abs(double x) {
    return std::abs(x);
}

/// Erf implementation according to Abramowitz & Stegun
/// A polynomial approximation with a maximal error of 1.2e-7. This approximation is based on Chebyshev fitting.
/// Numerical Recipes in Fortran 77: The Art of Scientific Computing
/// (ISBN 0-521-43064-X), 1992, page 214, Cambridge University Press.
/// Implementation is based on:
/// source: http://rextester.com/discussion/FVYOC97045/std-erf-versus-erf-impl-Abramowitz-Stegun-
/// which is almost the same in the source book Fortran77 recipes.
/// See also: https://en.wikipedia.org/wiki/Error_function#Polynomial
template <typename T>
inline T erf_impl(T v) {
    const T t = T(1) / (T(1) + T(0.5) * abs(v));

    static const T c[] = {T(1.26551223),
                          T(1.00002368),
                          T(0.37409196),
                          T(0.09678418),
                          T(-0.18628806),
                          T(0.27886807),
                          T(-1.13520398),
                          T(1.48851587),
                          T(-0.82215223),
                          T(0.17087277)};

    T result =
        T(1) -
        t * std::exp(
                (-v * v) - c[0] +
                t * (c[1] +
                     t * (c[2] +
                          t * (c[3] + t * (c[4] + t * (c[5] + t * (c[6] + t * (c[7] + t * (c[8] + t * (c[9]))))))))));

    return (v >= T(0)) ? result : -result;
}


template <typename T>
inline T norm_cdf(const T& v, const T& mean, const T& std) {
    return 0.5 * (1.0 + erf_impl((v - mean) * (M_SQRT1_2 / std)));
}

template <typename T>
inline T trnorm_cdf(T v, const double& mean, const double& std, const double& a, const double& b) {
    /* a = lower truncation bound
       b = upper truncation bound
    */
    assert(a < b);

    T zeta = T((v - mean) / std);
    T alpha = T((a - mean) / std);
    T beta = T((b - mean) / std);
    T cdf_alpha = T(0); /* if -inf */
    T cdf_beta = T(1);  /* if +inf, by definition of the cdf */

    if (!std::isinf(a))
        cdf_alpha = norm_cdf(alpha, 0.0, 1.0);

    if (!std::isinf(b))
        cdf_beta = norm_cdf(beta, 0.0, 1.0);


    return (norm_cdf(zeta, 0.0, 1.0) - cdf_alpha) / (cdf_beta - cdf_alpha);
}

} // namespace util_probability