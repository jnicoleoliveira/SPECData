import matplotlib.pyplot as plt
from tables.get import get_peaks
from tables.get import get_assignments
from tables.get import get_molecules

def graph_experiment_and_assignment(conn, exp_mid, assigned_mid, subplot=True, show_assigned_lines=True):
    lower_limit = 0.2

    # Get Experiment Peaks List and Assigned Peaks List
    exp_pids= get_peaks.get_pid_list(conn, exp_mid)
    assigned_pids = get_assignments.get_assigned_pid_list(conn,assigned_mid,exp_mid)

    # Get names
    exp_name = get_molecules.getName(conn, exp_mid)
    assigned_name = get_molecules.getName(conn, assigned_mid)

    # Determine Axes
    # Axes are determined my maximum values of experiment freq/inte values
    x_axis = get_peaks.get_max_frequency(conn, exp_mid)
    y_axis = get_peaks.get_max_intensity(conn, exp_mid)

    # Get assigned and experiment frequency(x), and intensity(y) lists
    assigned_frequency_list, assigned_intensity_list = get_peaks.get_frequency_intensity_list(conn, assigned_mid)
    experiment_frequency_list, experiment_intensity_list = get_peaks.get_frequency_intensity_list(conn, exp_mid)

    if(subplot is True):
        # Begin Plotting
        plt.figure(1)

        ## Sublot for Assigned molecule ##
        ax1 = plt.subplot(211)
        plt.axis([0, x_axis, 0, y_axis])
        plt.xlabel("Frequency")
        plt.ylabel("Intensity")
        plt.title("Assigned: " + assigned_name)

        # Plot Assigned
        plt.bar(assigned_frequency_list, assigned_intensity_list, bottom=-lower_limit, width=0.001, edgecolor='red')
        #plt.plot(assigned_frequency_list, assigned_intensity_list, color='red')

        ## Sublot for experiment molecule ##
        plt.subplot(212, sharex=ax1)
        plt.axis([0, x_axis, 0, y_axis])
        plt.xlabel("Frequency")
        plt.ylabel("Intensity")
        plt.title("Experiment: " + exp_name)

        # Plot Experiment
        plt.bar(experiment_frequency_list, experiment_intensity_list, bottom=-lower_limit, width=0.001, edgecolor='black')
        #plt.plot(experiment_frequency_list, experiment_intensity_list, color='black')
    else:
        # Set Labels and Title
        plt.xlabel("Frequency")
        plt.ylabel("Intensity")
        plt.title(exp_name + " and " + assigned_name)

        # Plot Experiment
        plt.plot(experiment_frequency_list, experiment_intensity_list, color='black')
        # Plot assigned
        #plt.plot(assigned_frequency_list, assigned_intensity_list, color='blue')
        plt.bar(assigned_frequency_list, assigned_intensity_list, bottom=-lower_limit*3, width=0.001, edgecolor='red')

    if(show_assigned_lines is True):
        frequencies, intensities = __get_assigned_lines_frequency_intensity_lists(conn, assigned_mid, exp_mid)
        y = []
        for f in frequencies:
            y.append(y_axis)
        #plt.bar(frequencies, y, bottom=-lower_limit, width=0.001, edgecolor='red')

        plt.bar(frequencies, intensities, bottom=-lower_limit, width=0.001, edgecolor='red')
    # Show plot
    plt.show(block=True)


def __get_assigned_lines_frequency_intensity_lists(conn, assigned_mid, mid):

    assigned_pids = get_assignments.get_assigned_pid_list(conn,assigned_mid,mid)
    frequencies = []
    intensities = []
    for pid in assigned_pids:
        frequencies.append(get_peaks.get_frequency(conn, pid))
        intensities.append(get_peaks.get_intensity(conn, pid))

    return frequencies, intensities

