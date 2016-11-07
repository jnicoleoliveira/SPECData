import experiment


class ExperimentWriteUp:

    def __init__(self, experiment):
        self.experiment = experiment

    def export_cleaned_lines(self, validated_mids, path):
        """

        :param validated_match_mids:
        :return:
        """

        ''' Get cleaned list of Frequencies and Intensities'''
        frequencies, intensities = \
            self.experiment.get_cleaned_experiment_intensities_list(validated_mids)

        ''' Get String '''
        string = self.__get_frequencies_intensities_string(frequencies, intensities)

        ''' Export to File '''
        self.__export_string_to_text_file(string, path)

        return path

    def __get_frequencies_intensities_string(self, frequencies, intensities):
        """
        Generates a string with
        :param frequencies:
        :param intensities:
        :return:
        """
        ''' Generate String ( frequency *tab* intensity ) '''
        txt_string = ""
        for i in range(0, len(frequencies)):
            txt_string += str(frequencies[i]) + " " + str(intensities[i])
            txt_string += "\n"

        return txt_string

    def __export_string_to_text_file(self, string, path):
        """

        :param string
        :param path:
        :return: path
        """

        text_file = open(path, 'w')
        text_file.write(string)
        text_file.close()

        return path
