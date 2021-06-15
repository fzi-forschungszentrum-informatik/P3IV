
import numpy as np


def finite_differences(x, dt, difference_type="backward"):

    if len(x.shape) is 1:
        x = x.reshape(x.shape[0], 1)

    v = np.diff(x, axis=0) / dt
    a = np.diff(v, axis=0) / dt
    j = np.diff(a, axis=0) / dt

    if "forward" in difference_type:
        v, a, j = forward_differences(v, a, j)
    elif "backward" in difference_type:
        v, a, j = backward_differences(v, a, j)

    return v, a, j


def forward_differences(v, a, j):
    dim = v.shape[-1]
    v = np.vstack((v, np.zeros((np.min([1, v.shape[0]]), dim))))
    a = np.vstack((a, np.zeros((np.min([2, v.shape[0]]), dim))))
    j = np.vstack((j, np.zeros((np.min([3, v.shape[0]]), dim))))

    return v, a, j


def backward_differences(v, a, j):
    dim = v.shape[-1]
    v = np.vstack((np.zeros((np.min([1, v.shape[0]]), dim)), v))
    a = np.vstack((np.zeros((np.min([2, v.shape[0]]), dim)), a))
    j = np.vstack((np.zeros((np.min([3, v.shape[0]]), dim)), j))
    return v, a, j
