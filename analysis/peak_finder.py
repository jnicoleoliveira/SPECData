# Author: Marie-Aline Martin
# Author: Jasmine Oliveira
# Author: Kyle Crabtree
# Date: 06/16/16

from math import ceil

import numpy as np
from scipy.signal import savgol_filter


def smooth(s_list, n):
    """
    Smooths list by 2*n points
    :param s_list:
    :param n: 1D list of points
    :return: 1D List of smoothed points
    """
    s_smooth = list(s_list)
    for i in range(n, len(s_list) - n):
        s_smooth[i] = np.mean(s_list[i - n:i + n])
    return s_smooth


def peak_finder(s_freq_list, s_int_list, s_autoclean):
    """
     Finds Peaks in 2D data
        (1) Finds and Removes Noise level
        (2) Smooths Functions
        (3) Determines Peaks
    :param s_freq_list: Frequency List (x)
    :param s_int_list: Intensity List (y)
    :param s_autoclean: AutoClean Integer
    :return: Frequency Peak List, Intensity Peak List
    """

    # (1) Find Noise Level
    n_split = 10
    part_len = len(s_freq_list) // n_split
    noise_list = []

    # Append the noise list for each portion
    for i in range(n_split):
        # define the noise as a function of the median times the median
        # this value can be decreased to peak up more weak lines
        if s_autoclean == 0:
            noise = 3.5 * np.median(s_int_list[i * part_len:(i + 1) * part_len])
        else:
            noise = 5 * np.median(s_int_list[i * part_len:(i + 1) * part_len])
        for j in range(i * part_len, (i + 1) * part_len):
            noise_list.append(noise)

    # Complete the noise list so that it has the same length as the frequency list
    for i in range(len(s_freq_list) % n_split):
        noise_list.append(noise)

    # ---------------------------------------------------
    # SMOOTH FUNCTIONs
    # ---------------------------------------------------
    n = int(ceil(len(s_int_list)))
    int_smooth1 = smooth(s_int_list, (n / 500))
    int_smooth2 = smooth(s_int_list, (n / 10000))
    int_smooth3 = smooth(s_int_list, (n / 20000))

    # ---------------------------------------------------
    # PEAK DETECTION
    # ---------------------------------------------------

    peak_int_list = []
    peak_freq_list = []

    ## everything relative to smooth_list can be un-commented to plot the resulting smoothed curve
    # smooth_list = []

    # lower_limit and peak_int_fig are used for the purpose of clarity on the plot only
    lower_limit = 0.2
    peak_int_fig = []

    # The peaks are defined as:
    # - the local maximum of 4 points
    # - an intensity higher than the noise detection limit
    # - an intensity higher that the average of the 3 smooth *2 (purely empirical)
    # That last point is very important and allows to limit the number of peaks,
    # in particular on the shoulder of very intense lines, where local maxima on the noise can be above the intensity threshold (large number of points smoothing)
    # It also allows to not peak very broad features that can't be molecular lines

    for i in range(2, len(s_int_list) - 2):
        if (s_int_list[i - 2] < s_int_list[i - 1] < s_int_list[i] > s_int_list[i + 1] or s_int_list[i - 1] < s_int_list[
            i] > s_int_list[i + 1] > s_int_list[i + 2]) \
                and s_int_list[i] > noise_list[i] \
                and s_int_list[i] > (int_smooth1[i] + int_smooth2[i] + int_smooth3[i]) / 1.5 \
                and 6000 < s_freq_list[i] < 19000:
            peak_int_list.append(s_int_list[i])
            peak_int_fig.append(s_int_list[i] + lower_limit)
            peak_freq_list.append(s_freq_list[i])

    return peak_freq_list, peak_int_list


def optimized_peak_finder(frequencies, intensities):
    n_split = 10
    window = 4
    i_size = len(intensities)
    lower_limit = 0.2

    # Get Noise List
    # noise_list = get_noise_list(frequencies, intensities, n_split, True)
    # Smooth Lists
    smoothed = smooth(intensities, (i_size / 1000))

    # Obtain Peak Indexes
    indexes = get_peaks(intensities, i_size)

    # Obtain indexed subset of frequencies and intensities
    frequencies = [frequencies[i] for i in indexes]
    intensities = [intensities[i] for i in indexes]

    return frequencies, intensities


def get_noise_list(frequencies, intensities, n_split=10, autoclean=False):
    # (1) Find Noise Level
    n_split = 5
    part_len = len(frequencies) // n_split
    noise_list = []
    avg_intensity = sum(intensities) / len(intensities)
    print part_len

    # Append the noise list for each portion
    for i in range(n_split):
        # define the noise as a function of the median times the median
        # this value can be decreased to peak up more weak lines
        if autoclean is True:
            noise = avg_intensity + np.median(intensities[i * part_len:(i + 1) * part_len]) / 2
        else:
            noise = autoclean * np.median(intensities[i * part_len:(i + 1) * part_len])

        for j in range(i * part_len, (i + 1) * part_len):
            noise_list.append(noise)

    # Complete the noise list so that it has the same length as the frequency list
    for i in range(len(frequencies) % n_split):
        noise_list.append(noise)

    return noise_list


def get_peaks(a, n, peaks=[]):
    window = 5
    panel = (window - 1) / 2

    if n + panel > len(a) or n - panel < 0:
        return peaks

    if not _is_valid_panel(a, n / 2, panel):
        print "Valid Right"
        peaks.append(get_peaks(a, n / 2))
    elif not _is_valid_panel(a, n / 2, -panel):
        print "Valid Left"
        peaks.append(get_peaks(a, n / 2))
    else:
        peaks.append(n / 2)
        print "peak found"
        peaks.append(get_peaks(a, n / 2))
        peaks.append(get_peaks(a, n / 2))

    return peaks


def _is_valid_panel(a, i, panel):
    """
    Use -panel to indicate direction
    :param a:
    :param i:
    :param panel_size:
    :return:
    """
    for x in range(0, panel):
        if a[i + x] < a[i]:
            return False
    return True


# def peak_finder_peakutils(s_freq_list, s_int_list, threshold=0.1):
#     """
#      Finds Peaks in 2D data
#         (1) Normalizes Intensities
#         (2) PeakUtils Determines Peaks
#     :param s_freq_list: Frequency List (x)
#     :param s_int_list: Intensity List (y)
#     :param threshold:
#     :return: Frequency Peak List, Intensity Peak List
#     """
#
#     avg = sum(s_int_list) / len(s_int_list)
#     s_freq_list, s_int_list = clear_baseline(s_freq_list, s_int_list, avg)
#
#     y = s_int_list
#     y = smooth_savgol(s_int_list)
#     # Peak Finder: Obtain indexes of peaks in intensity list
#     indexes = peakutils.indexes(y, thres=threshold)
#
#     # Obtain indexed subset of frequencies and intensities
#     frequencies = [s_freq_list[i] for i in indexes]
#     intensities = [s_int_list[i] for i in indexes]
#
#     return frequencies, intensities


def clear_baseline(frequencies, intensities, limit):
    f2 = []
    i2 = []
    for i in range(0, len(intensities)):
        if intensities[i] > limit:
            f2.append(frequencies[i])
            i2.append(intensities[i])

    return f2, i2


def smooth_savgol(intensities, window=5, polynomial=2):
    x = np.array(intensities)
    y = savgol_filter(x, 5, 2)
    return y


def k_peak_finder(xarray, yarray, snr=3, re=False):
    """
    Kyle Crabtree peak finding algorithm (BlackChirp)
    :param xarray:
    :param yarray:
    :param snr:
    :return:
    """

    # compute smoothed 2nd derivative for strong peaks
    d2y = savgol_filter(yarray, 11, 6, deriv=2)

    # build noise model
    chunks = 50
    chunk_size = len(yarray) // chunks
    avg = []
    noise = []
    dat = []
    outnoise = np.empty(len(yarray))
    outbaseline = np.empty(len(yarray))
    for i in range(chunks):
        if i + 1 == chunks:
            dat = yarray[i * chunk_size:]
        else:
            dat = yarray[i * chunk_size:(i + 1) * chunk_size]

        # Throw out any points that are 10* the median and recalculate
        # Do this until no points are removed.
        done = False
        while not done:
            if len(dat) == 0:
                break
            med = np.median(dat)
            fltr = [d for d in dat if d < 10 * med]
            if len(fltr) == len(dat):
                done = True
            dat = fltr

        # now, retain the mean and stdev for later use
        if len(dat) > 2:
            avg.append(np.mean(dat))
            noise.append(np.std(dat))
        else:
            # something went wrong with noise detection... ignore section
            # probably a chunk containing only 0.0
            avg.append(0.0)
            noise.append(1.)

        if i + 1 == chunks:
            outnoise[i * chunk_size:] = noise[i]
            outbaseline[i * chunk_size:] = avg[i]
        else:
            outnoise[i * chunk_size:(i + 1) * chunk_size] = noise[i]
            outbaseline[i * chunk_size:(i + 1) * chunk_size] = avg[i]

    outx = []
    outy = []
    outidx = []
    outsnr = []

    # if a point has SNR > threshold, look for local min in 2nd deriv.
    for i in range(2, len(yarray) - 2):
        try:
            snr_i = (yarray[i] - avg[i // chunk_size]) / noise[i // chunk_size]
            if snr_i >= snr:
                if (d2y[i - 2] > d2y[i - 1] > d2y[i] < d2y[i + 1] or
                                    d2y[i - 1] > d2y[i] < d2y[i + 1] < d2y[i + 2]):
                    outx.append(xarray[i])
                    outy.append(yarray[i])
                    outidx.append(i)
                    outsnr.append(snr_i)
        except IndexError:
            continue

    # test interval points
    # interval_points = list(filter((lambda x: 18957 < x < 19018)), yarray)
    min = 9492  # 18900##
    max = 9497  # 19100##
    min_pad = min - 50
    max_pad = max + 50

    if re is False:

        indexes = []
        for i in range(0, len(outx)):
            if min < outx[i] < max:
                indexes.append(i)

        for index in sorted(indexes, reverse=True):
            del outx[index]
            del outy[index]

        interval_x = []
        interval_y = []
        for i in range(0, len(xarray)):
            if min_pad < xarray[i] < max_pad:
                interval_y.append(yarray[i])
                interval_x.append(xarray[i])

        threshold = float((max - min)) / len(indexes)
        print threshold
        freq, inten = k_peak_finder(interval_x, interval_y, threshold, re=True)

        index = indexes[0]
        for i in range(0, len(freq)):
            if min < freq[i] < max:
                outx.insert(index, freq[i])
                outy.insert(index, inten[i])
                index += 1

    return outx, outy  # , outidx, outsnr, outnoise, outbaseline


def main():
    import matplotlib.pyplot as plot
    from tests.example.peak_finding_tests import read_data
    file_path = "/home/joli/Downloads/Av_CP343-CP348_ft.sp"

    frequencies, intensities = read_data(file_path)
    noise_list = get_noise_list(frequencies, intensities, 10, 3.5)
    noise_list_auto = get_noise_list(frequencies, intensities, 10, True)
    max_x = max(frequencies)
    max_y = max(intensities)
    avg = (max_y - max(noise_list)) / 2 / 2 / 2 / 2
    p_x, p_y = optimized_peak_finder(frequencies, intensities)

    plot.plot(frequencies, intensities, color='black')
    plot.plot(frequencies, noise_list, color='green')
    plot.plot(frequencies, noise_list_auto, color='blue')
    plot.plot(frequencies, smooth_savgol(intensities), color='pink')
    plot.plot(frequencies, smooth(intensities, (len(intensities) / 10000)), color='yellow')
    # plot.axhline(linewidth=4,y=avg, color='purple', xmin=0, xmax=max_x)
    plot.bar(p_x, p_y, color='orange')
    # plot.plot(frequencies, smooth_savgol(intensities), color='black')
    #
    # # frequencies, intensities = peakdetect.peakdet(intensities, .3, frequencies)
    # frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.001)
    # plot.bar(frequencies, intensities, color='red')
    #
    # print len(frequencies)
    plot.show()


if __name__ == '__main__':
    main()
