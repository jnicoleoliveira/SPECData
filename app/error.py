# Author: Jasmine Oliveira
# Date: 07/18/2016

import os


def display_error(error_lbl, error_message):
    error_lbl.setText(error_message)


def is_valid_file(file_path):
    """
    Determines if file is valid.
    If it is a valid file_path, returns True. Otherwise, returns False.
    :param file_path: Specified FilePath
    :return:
    """
    # Determine if File Exists
    if os.path.exists(file_path) is False:
        return False

    # Determine if file extention is correct
    valid_ext = "sp", "lines", "cat"
    if str.split(str(file_path), '.')[1] not in valid_ext:
        return False

    return True


def get_file_error_message(file_path):
    """
    Returns the file error message, if a file has an error.
    Otherwise returns None.
    :param file_path: Specified FilePath string with error
    :return: String of error message, otherwise None.
    """
    # Determine if File Exists
    if os.path.exists(file_path) is False:
        error_message = "ERROR: Filepath " + file_path + " does not exist"
        return error_message

    # Determine if file extention is correct
    valid_ext = "sp", "lines", "cat"
    if str.split(str(file_path), '.')[1] not in valid_ext:
        error_message = "ERROR: Filepath " + file_path + " is an invalid file. Must be a .sp, .lines, or .cat file"
        return error_message

    return None