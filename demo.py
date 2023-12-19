from matplotlib import pyplot as plt
import numpy as np
from firefly.math.allan import allan_variance, plot_allan_deviation, identify_white_noise_coefficient, identify_random_walk_coefficient
from firefly.math.noise import white_noise, random_walk

fs = 100
N = 100000
# x = 18. * white_noise(N, fs=fs)
# print(x)

# print(np.std(x))

# (tau, avar,) = allan_variance(x, dt=1/fs, n_clusters=100)

# adev = np.sqrt(avar)

# ax = plot_allan_deviation(tau, adev)

# N = identify_white_noise_coefficient(adev=adev, tau=tau, ax=ax)
# print(N)
# plt.show()

x = 1. * random_walk(npts=10000000, fs=fs)
(tau, avar,) = allan_variance(x, dt=1/fs, n_clusters=100)

adev = np.sqrt(avar)

ax = plot_allan_deviation(tau, adev)

K = identify_random_walk_coefficient(adev=adev, tau=tau, ax=ax)
print(K)

plt.show()
