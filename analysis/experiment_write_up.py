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

        ''' Export to File '''
        self.__export_frequencies_intensities_to_text_file__(frequencies, intensities, path)

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
            txt_string += str(frequencies) + "\t" + str(intensities)

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

#background-color: rgba(0, 128, 128, 154);
##008080
#background-color: rgb(82, 82, 82);