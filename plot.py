import matplotlib
import numpy as np
import time

# Saves images, rather than opening up a window
matplotlib.use("Agg")
import matplotlib.pyplot as plt

font = {"family": "Proxima Nova", "weight": "light", "size": 18}

matplotlib.rc('font', **font)
matplotlib.rc('axes', edgecolor="w")
matplotlib.rc('xtick.major', size=0)
matplotlib.rc('xtick.minor', size=0)
matplotlib.rc('ytick.major', size=0)
matplotlib.rc('ytick.minor', size=0)



plt.plot(data,'c', linewidth=2.5)
plt.ylim(min(data) - 1, max(data) + 1)

data_len = np.arange(len(data))

ydata_copy = data[:]
ydata_copy[0] = ""

date = time.strftime("%B %d %I:%M %p")

plt.xticks(data_len, ("", date, "", "", date, ""))


plt.savefig("font-test.png")