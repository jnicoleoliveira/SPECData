from math import ceil

from filetypes import *


class ExperimentWriteUp:
    TAB = "\t"
    SPACE = " "
    COMMA = ","

    def __init__(self, experiment):
        self.experiment = experiment

    def export(self, validated_mids, path, type, format, delimiter=None, shots=None):
        """

        :param validated_mids:
        :param path:
        :param type:
        :param format:
        :param shots:
        :return:
        """

        ''' Get cleaned list of Frequencies and Intensities'''
        frequencies, intensities = \
            self.experiment.get_cleaned_experiment_intensities_list(validated_mids)

        if type == FileType.TEXT_FILE:
            string = self.__get_txt_string_format(frequencies, intensities, format, delimiter)
        elif type == FileType.LINES_FILE:
            string = self.__get_txt_string_format(frequencies, intensities, format, delimiter)
        elif type == FileType.QTFTM_FILE:
            string = self.__get_ftb_string_format(frequencies, intensities, format, shots)
        else:
            raise ValueError("Invalid LineFileType!" + str(type))

        ''' Export to File '''
        self.__export_string_to_file(string, path)

        return path

    def __get_txt_string_format(self, frequencies, intensities, format, delimiter=None):

        if format == FileFormat.DELIMITER:
            string = self.__get_frequencies_intensities_string(frequencies, intensities, delimiter)
        elif format == FileFormat.FREQUENCY_ONLY:
            string = self.__get_frequencies_string(frequencies)
        else:
            raise ValueError("Type-Format Mismatch!")

        return string

    def __get_ftb_string_format(self, frequencies, intensities, format, shots):
        if format is FileFormat.FTB_FIXED_SHOTS:
            string = self.__get_ftb_fixed_shots_string(frequencies, shots)
        elif format is FileFormat.FTB_ESTIMATED_SHOTS:
            string = self.__get_ftb_estimated_shots_string(frequencies, intensities, shots)
        else:
            raise ValueError("Type-Format Mismatch!")

        return string

    def export_cleaned_lines(self, validated_mids, path):
        """

        :param validated_mids:
        :return:
        """

        ''' Get cleaned list of Frequencies and Intensities'''
        frequencies, intensities = \
            self.experiment.get_cleaned_experiment_intensities_list(validated_mids)

        ''' Get String '''
        string = self.__get_frequencies_intensities_string(frequencies, intensities)

        ''' Export to File '''
        self.__export_string_to_file(string, path)

        return path

    def __get_ftb_fixed_shots_string(self, frequencies, n_shots):
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

    def __get_ftb_estimated_shots_string(self, frequencies, intensities, max_shots):

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

    def __get_frequencies_intensities_string(self, frequencies, intensities, delimiter=SPACE):
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

    def __get_frequencies_string(self, frequencies):
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

    def __export_string_to_file(self, string, path):
        """

        :param string
        :param path:
        :return: path
        """

        text_file = open(path, 'w')
        text_file.write(string)
        text_file.close()

        return path
