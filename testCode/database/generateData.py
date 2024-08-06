from sklearn.datasets import make_moons
import matplotlib.pyplot as plt

x, y = make_moons(n_samples = 500, shuffle = True, noise = 0.15, random_state=42)

plt.scatter(x[:, 0], x[:, 1], c=y)
plt.show()
