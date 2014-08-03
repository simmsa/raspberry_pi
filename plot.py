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

def plot_data(data, dates, file_name):

    plt.plot(data, 'c', linewidth=2.5) #c = Cyan
    plt.ylim(min(data) - 1, max(data) + 1)

    data_len = np.arange(len(data))

    xticks_data = []
    start = 1
    data_len_2 = len(data)

    first_quarter, third_quarter = int(round(data_len_2 * 0.16)), int(round(data_len_2 * 0.84))

    for x in xrange(data_len_2):
        if x == first_quarter:
            xticks_data.append(dates[0])
        elif x == third_quarter:
            xticks_data.append(dates[-1])
        else:
            xticks_data.append("")
        start = start + 1


    plt.xticks(data_len, xticks_data)

    plt.title("Greenhouse temps starting %s" % dates[0])

    plt.savefig(file_name)

    return file_name

if __name__=="__main__":
    data = [x for x in range(1000)]
    date = time.strftime("%B %d %I:%M %p") # Month Day of the Month, Hour(12 hour clock), Minute, am or pm
    dates = [date for x in range(1000)]

    plot_data(data, dates, "function-test.png")
