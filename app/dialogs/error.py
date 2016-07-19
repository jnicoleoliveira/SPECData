# Author: Jasmine Oliveira
# Date: 07/18/2016

import os


def display_error(error_lbl, error_message):
    error_lbl.setText(error_message)


def is_valid_file(error_lbl, file_path):
    """
    Determines if file is valid.
    If not a valid file, displays error message to error label
    :param error_lbl: Error Message label
    :param file_path: Specified FilePath
    :return:
    """
    # Determine if File Exists
    if os.path.exists(file_path) is False:
        error_message = "ERROR: Filepath " + file_path + " does not exist"
        display_error(error_lbl, error_message)
        return False

    # Determine if file extention is correct
    valid_ext = "sp", "lines", "cat"
    if str.split(str(file_path), '.')[1] not in valid_ext:
        error_message = "ERROR: Filepath " + file_path + " is an invalid file. Must be a .sp, .lines, or .cat file"
        display_error(error_lbl, error_message)
        return False

    return True
