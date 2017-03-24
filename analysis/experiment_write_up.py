import datetime
from math import ceil

from filetypes import *


###############################################################################
# Public Functions
###############################################################################

def export_cleaned_lines(experiment, validated_mids, path, type, format, delimiter=None, shots=None):
    """

    :param experiment:
    :param validated_mids:
    :param path:
    :param type:
    :param format:
    :param delimiter:
    :param shots:
    :return:
    """

    ''' Get cleaned list of Frequencies and Intensities'''
    frequencies, intensities = \
        experiment.get_cleaned_experiment_intensities_list(validated_mids)

    if type == FileType.TEXT_FILE:
        string = __get_txt_string_format(frequencies, intensities, format, delimiter)
    elif type == FileType.LINES_FILE:
        string = __get_txt_string_format(frequencies, intensities, format, delimiter)
    elif type == FileType.QTFTM_FILE:
        string = __get_ftb_string_format(frequencies, intensities, format, shots)
    elif type == FileType.CSV_FILE:
        string = __get_txt_string_format(frequencies, intensities, format, delimiter)
    else:
        raise ValueError("Invalid LineFileType!" + str(type))

    ''' Export to File '''
    __export_string_to_file(string, path)

    return path


def export_analysis_summary(experiment, path, max_width=80):
    """
    SPECdata Analysis Write-Up
    :param experiment
    :param path:
    :return: path
    """
    string = ""
    TITLE = "SPECdata Analysis Write-Up"
    SECTION_1 = "INFO"
    SECTION_2 = "ANALYSIS OVERVIEW"

    INFO_LEFT_LIST = ["Name:", "Composition:", "Type:", "Units", "Notes:"]
    INFO_RIGHT_LIST = [experiment.name, experiment.get_composition(),
                       experiment.get_type(), experiment.get_units(), experiment.get_notes()]

    ANALYSIS_LEFT_LIST = ["Total Peaks: ", "Unnassigned Peaks: ", "Validated Peaks:", "Validated Molecules:"]
    ANALYSIS_RIGHT_LIST = [len(experiment.experiment_peaks), experiment.get_unnassigned_count(),
                           experiment.get_validated_count()[1], experiment.get_validated_molecules_count()]
    MATCHES_LEFT = []
    MATCHES_RIGHT = []
    for key, value in experiment.validated_matches.iteritems():
        MATCHES_LEFT.append(value.name)
        MATCHES_RIGHT.append(value.m)

    ''' Build String '''
    # Title
    string += __get_header_string_format(TITLE) + NEW_LINE
    string += "(" + __get_datetime_string_format() + ")" + (NEW_LINE * 2)

    # Section 1: Info
    string += __get_header_string_format(SECTION_1) + NEW_LINE
    string += __get_list_format(INFO_LEFT_LIST, INFO_RIGHT_LIST) + NEW_LINE

    # Section 2: Analysis
    string += __get_header_string_format(SECTION_2) + NEW_LINE
    string += __get_list_format(ANALYSIS_LEFT_LIST, ANALYSIS_RIGHT_LIST) + NEW_LINE
    string += __get_list_format(MATCHES_LEFT, MATCHES_RIGHT)

    ''' Export to File '''
    __export_string_to_file(string, path)

    return path


###############################################################################
# Helper Functions
###############################################################################

def __get_list_format(left_list, right_list):
    string = ""

    if len(left_list) != len(right_list):
        return ValueError

    max_buff = 4 + max([len(s) for s in left_list])

    for i in range(0, len(left_list)):
        buff = max_buff - (len(left_list[i]))
        string += str(left_list[i]) + (" " * buff) + str(right_list[i]) + NEW_LINE

    return string


def __get_datetime_string_format():
    now = datetime.datetime.now()
    return str(now.month) + "/" + str(now.day) + "/" + str(now.year) + \
           ": " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)


def __get_header_string_format(title, width=80):
    return ("-" * width) + NEW_LINE + str(title) + NEW_LINE + ("-" * width)


def __get_txt_string_format(frequencies, intensities, format, delimiter=None):
    if format == FileFormat.DELIMITER:
        string = __get_frequencies_intensities_string(frequencies, intensities, delimiter)
    elif format == FileFormat.FREQUENCY_ONLY:
        string = __get_frequencies_string(frequencies)
    else:
        raise ValueError("Type-Format Mismatch!")

    return string


def __get_ftb_string_format(frequencies, intensities, format, shots):
    if format is FileFormat.FTB_FIXED_SHOTS:
        string = __get_ftb_fixed_shots_string(frequencies, shots)
    elif format is FileFormat.FTB_ESTIMATED_SHOTS:
        string = __get_ftb_estimated_shots_string(frequencies, intensities, shots)
    else:
        raise ValueError("Type-Format Mismatch!")

    return string


def __get_ftb_fixed_shots_string(frequencies, n_shots):
    """

    :param frequencies:
    :param n_shots:
    :return:
    """
    string = ""
    for frequency in frequencies:
        line = 'ftm:%5.3f shots:%1s dipole:1.0' % (frequency, n_shots)
        string += line + "\n"
    return string


def __get_ftb_estimated_shots_string(frequencies, intensities, max_shots):
    string = ""
    for i in range(0, len(frequencies)):
        frequency = frequencies[i]  # Get Frequency
        intensity = intensities[i]  # Get Intensity

        n_shots = ceil(2 / (5 * intensity)) * 2  # Estimate n_shots
        n_shots = 10 if n_shots < 10 else n_shots  # Set lower limit
        n_shots = max_shots if n_shots > max_shots else n_shots  # Set upper limit

        line = 'ftm:%5.3f shots:%1s dipole:1.0' % (frequency, n_shots)
        string += line + "\n"

    return string


def __get_frequencies_intensities_string(frequencies, intensities, delimiter=SPACE):
    """
    Generates a string list with frequency delimiter, and intensity
    Default delimiter is a space (" ").
    :param frequencies:
    :param intensities:
    :return:
    """

    ''' Generate String ( frequency *delimiter* intensity ) '''
    txt_string = ""
    for i in range(0, len(frequencies)):
        txt_string += str(frequencies[i]) + delimiter + str(intensities[i])
        txt_string += "\n"

    return txt_string


def __get_frequencies_string(frequencies):
    """
    Generates a string with frequencies seperated by a newline character
    :param frequencies:
    :return:
    """

    ''' Generate String of list of frequencies '''
    txt_string = ""
    for i in range(0, len(frequencies)):
        txt_string += str(frequencies[i]) + "\n"

    return txt_string


def __export_string_to_file(string, path):
    """

    :param string
    :param path:
    :return: path
    """

    text_file = open(path, 'w')
    text_file.write(string)
    text_file.close()

    return path
