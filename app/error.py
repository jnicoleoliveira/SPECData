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
    valid_ext = "sp", "lines", "cat", "dpt", "txt"
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
    valid_ext = "sp", "lines", "cat", "dpt", "txt"
    if str.split(str(file_path), '.')[1] not in valid_ext:
        error_message = "ERROR: Filepath " + file_path + " is an invalid file. Must be a .sp, .lines, or .cat file"
        return error_message

    return None


def path_exists(file_path):
    """
    Determines if path exists
    :param file_path: file path of
    :return: True if path exists, false otherwise
    """
    # Determine if File Exists
    return os.path.exists(file_path)


def is_file(file_path):
    """
    Determines if the path is a file
    :param file_path: (sting) File path
    :return:
    """
    return os.path.isfile(file_path)


def get_file_name(file_path):
    if path_exists(file_path):
        return os.path.basename(file_path)


def molecule_entry_exists(conn, name, category):
    """
    Determines if a molecule entry exists in a
    database.
    :param conn: SQLite Connection
    :param name: (string) Name of molecule
    :param category: (string) Molecule category
    :return: True if it exists, False otherwise
    """
    from tables.molecules_table import get_mid

    mid = get_mid(conn, name, category)

    if mid is None:
        return False

    return True


