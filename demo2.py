import matplotlib.pyplot as plt

class PlotStorage:
    def __init__(self):
        self.plot = None

    def create_plot(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        self.plot = fig

# Create an instance of the class and create a plot
storage = PlotStorage()
storage.create_plot()

# The plot is now stored in the `plot` property of the `storage` instance
print(type(storage.plot))

storage.plot.savefig("plot.png")