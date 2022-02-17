import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

filename = "spacedata{}.csv"

timestamps = []
values = []

for it in range(1, 5):
    """
    First I iterated through the files, and put every pair of data into
    the 'timestamps' and 'values' arrays.
    I used string formatting to be able to dynamically change the name of the file to open.
    """
    rows = pd.read_csv(filename.format(it), header=None, sep=",")
    timestamps.extend(rows[0])
    values.extend(rows[1])


def show_split_mean_values():
    """
    The amount of data is too large, so I split the data into 2000 pieces.
    The function displays the mean value of every piece.
    This way we have a displayable amount of data, and get a basic understanding of the dataset.
    """
    splits = []

    step_size = math.floor(len(values) / 2000)
    for i in range(2000):
        splits.append(values[0 + i * step_size:(i + 1) * step_size])

    if step_size * 2000 != len(values):
        splits.append(values[step_size * 2000:])

    splits_mean = []

    for s in splits:
        mean = np.mean(s)
        splits_mean.append(mean)

    plt.plot(splits_mean)
    plt.ylabel("Value")
    plt.show()
    """
    The figure clearly shows that the data values are divided between two intervals.
    The two intervals are around ~131 and ~0.
    After this, I split the original arrays into 2 arrays. One is for the values around 131
    and the other one is for the values around 0.
    """


show_split_mean_values()


big_values = []
big_timestamps = []
small_values = []
small_timestamps = []


def into_two_arrays():
    for idx in range(len(values)):
        """
        Splitting the original array into two arrays.
        Choosing a relatively big interval includes the possible outliers 
        -> Arbitrary choice of 131 - 65 as the lower limit of the interval of the big numbers.
        """
        if values[idx] >= 131 - 65:
            big_values.append(values[idx])
            big_timestamps.append(timestamps[idx])
        else:
            small_values.append(values[idx])
            small_timestamps.append(timestamps[idx])

    plot1 = plt.figure(1)
    plt.plot(big_values[:4000])
    plt.ylabel("Value")
    plot2 = plt.figure(2)
    plt.plot(small_values[:4000])
    plt.ylabel("Value")
    plt.show()
    """
    The two figures show that both arrays draw out a line similar to the sine curve.
    A period is about 600-650 record long.
    (In other words, the sine curve gets in the same state/position after every 600-650 records of data.) 
    """


into_two_arrays()


def get_peaks(v, ts):
    """
    Getting peaks (or outliers) using the interquartile range method.
    These outliers could be deleted or replaced with interpolated values.
    """
    outliers = []
    perc25 = np.percentile(v, 25)
    perc75 = np.percentile(v, 75)
    iqr = perc75 - perc25
    lower_bound = perc25 - 1.5 * iqr
    upper_bound = perc75 + 1.5 * iqr
    for i in range(len(v)):
        if v[i] >= upper_bound or v[i] <= lower_bound:
            outliers.append([v[i], ts[i]])

    return outliers


big_value_outliers = get_peaks(big_values, big_timestamps)
small_value_outliers = get_peaks(small_values, small_timestamps)


def get_indicators(v):
    """
    This function returns the statistical indicators for the given dataset.
    """
    mean = np.mean(v)
    median = np.median(v)
    mode = stats.mode(v)
    standard_dev = np.std(v)

    return [mean, median, mode, standard_dev]


big_value_indicators = get_indicators(big_values)
small_value_indicators = get_indicators(small_values)

print("Number of outliers in the array of big values: " + str(len(big_value_outliers)))
print("Number of outliers in the array of small values: " + str(len(small_value_outliers)))
print("Indicators of the array of big values")
print(big_value_indicators)
print("Indicators of the array of small values")
print(small_value_indicators)



