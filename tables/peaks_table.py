# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/18/2016 (Refactored API)
# -----------------------------------------------------------------------------
# peaks_table.py:
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the peaks table in the SPECdata database system. A single row in the peaks
# table represents a single peak associated with a molecule.
#
#       Peaks table entries have the following format:
#           -> pid           (int:   id of the peak table entry)
#           -> mid           (int:   id of the associated molecules row)
#           -> frequency     (float: frequency of the peak)
#           -> intensity     (float: intensity of the peak)
#
#
#       Public Functions:
#           [Table Information]
#              * get_all_known_frequencies(conn)
#              * get_all_known_frequencies_with_mids(conn)
#              * get_frequencies_in_midlist(conn, mid_list, max=None, min=None)
#           [Entry Information]
#               * get_max_frequency(conn, mid)
#               * get_min_frequency(conn, mid)
#               * get_max_intensity(conn, mid)
#               * get_average_intensity(conn, mid)
#               * get_pid_list(conn, mid)
#               * get_peak_count(conn, mid, max_range=None, min_range=None)
#               * get_frequency_intensity_list(conn, mid, max=None, min=0)
#               * get_unassigned_pid_list(conn, mid)
#               * get_frequency(conn, pid)
#               * get_intensity(conn, pid)
#               * get_frequency_intensity(conn, pid)
#               * pid_exists(conn, pid)
#               * get_mid_from_frequency(conn, frequency)
#           [Insert Entry]
#               * import_file(conn, file_path, mid):
#           [Remove Entry]
#               * remove_all(conn, mid)
#               * remove_peak(conn, pid)
# -----------------------------------------------------------------------------

from molecules_table import mid_exists

###############################################################################
# Get Peaks Table Information
# -----------------------------------------------------------------------------
# Date: 06/2016
# -----------------------------------------------------------------------------
# Get data from the peaks table
# Public Functions:
#       * get_all_known_frequencies(conn)
#       * get_all_known_frequencies_with_mids(conn)
#       * get_frequencies_in_midlist(conn, mid_list, max=None, min=None)
###############################################################################


def get_all_known_frequencies(conn):
    # Set of all peaks for molecule
    cursor = conn.execute("SELECT frequency FROM molecules JOIN peaks"\
          " ON molecules.mid = peaks.mid"\
          " WHERE molecules.category='known'"\
          " or molecules.category='artifact'")
    frequencies = []
    rows =  cursor.fetchall()

    for row in rows:
        frequencies.append(row)

    return frequencies


def get_all_known_frequencies_with_mids(conn):
    # Set of all peaks for molecule
    cursor = conn.execute("SELECT peaks.mid, peaks.frequency FROM molecules JOIN peaks"\
          " ON molecules.mid = peaks.mid"\
          " WHERE molecules.category='known'"\
          " or molecules.category='artifact'"
          " ORDER BY peaks.frequency ASC;")
    mids = []
    frequencies = []
    rows = cursor.fetchall()

    for row in rows:
        mids.append(row[0])
        frequencies.append(row[1])

    return mids, frequencies


def get_frequencies_in_midlist(conn, mid_list, max=None, min=None):

    if max is None and min is None:
        query = "SELECT frequency FROM peaks"\
              " WHERE mid IN (" + ','.join(map(str, mid_list)) + ')'\
              " ORDER BY frequency ASC;"
    elif min is None:
        query = "SELECT frequency FROM peaks"\
              " WHERE mid IN (" + ','.join(map(str, mid_list)) + ')'\
              " AND frequency<{max} ORDER BY frequency ASC;".format(max=max)
    elif max is None:
        query = "SELECT frequency FROM peaks"\
              " WHERE mid IN (" + ','.join(map(str, mid_list)) + ')'\
              " AND frequency>{min} ORDER BY frequency ASC;".format(min=min)
    else:
        query = "SELECT frequency FROM peaks"\
              " WHERE mid IN (" + ','.join(map(str, mid_list)) + ')'\
              " AND frequency<{max} AND frequency>{min}" \
              " ORDER BY frequency ASC;".format(max=max, min=min)

    # Set of all peaks for molecule
    cursor = conn.execute(query)
    rows = cursor.fetchall()

    frequencies = []
    for row in rows:
        frequencies.append(row[0])

    return frequencies


###############################################################################
# Get Peaks Entry Information
# ----------------------------------------------------------------------------
# Date:  06/2016
# -----------------------------------------------------------------------------
# Public Functions:
#     [ by mid ]
#       * get_max_frequency(conn, mid)
#       * get_min_frequency(conn, mid)
#       * get_max_intensity(conn, mid)
#       * get_average_intensity(conn, mid)
#       * get_pid_list(conn, mid)
#       * get_peak_count(conn, mid, max_range=None, min_range=None)
#       * get_frequency_intensity_list(conn, mid, max=None, min=0)
#       * get_unassigned_pid_list(conn, mid)
#     [ by pid ]
#       * get_frequency(conn, pid)
#       * get_intensity(conn, pid)
#       * get_frequency_intensity(conn, pid)
#       * pid_exists(conn, pid)
#     [ by frequency ]
#       * get_mid_from_frequency(conn, frequency)

###############################################################################

def get_average_intensity(conn, mid):
    """
    Gets the average intensity of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Average intensity of a molecule
    """
    cursor = conn.execute("SELECT AVG(intensity) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity


def get_intensity(conn, pid):
    """
    Returns the intensity of a specified peak
    :param conn:
    :param pid:
    :return:
    """
    cursor = conn.execute("SELECT intensity FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity


def get_mid(conn, pid):
    """
    Returns the intensity of a specified peak
    :param conn:
    :param pid:
    :return:
    """
    cursor = conn.execute("SELECT mid FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    mid = line[0]
    return mid


def get_frequency(conn, pid):
    """
    Returns the frequency of a given peak
    :param conn: SQLite Database connection
    :param pid: Peak ID (pid) of specified peak
    :return:
    """
    cursor = conn.execute("SELECT frequency FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency


def get_frequency_intensity(conn, pid):
    """
    Returns frequency, intensity of a specified peak
    :param conn:
    :param pid:
    :return:
    """
    cursor = conn.execute("SELECT frequency, intensity FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    frequency = line[0]
    intensity = line[1]

    return frequency, intensity


def get_frequency_intensity_list(conn, mid, max=None, min=0):
    """
    Returns frequency and intensity list of a particular module
    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :param max: (opt) maximum interval value
    :param min: (opt) minimum interval value
    :return:
    """
    if max is None:
        cursor = conn.execute("SELECT frequency, intensity FROM peaks WHERE mid=? ORDER by frequency ASC;", (mid,))
    else:
        cursor = conn.execute("SELECT frequency, intensity FROM peaks WHERE mid=? "
                              "AND frequency<? AND frequency>? "
                              "ORDER by frequency ASC;", (mid, max, min,))

    rows = cursor.fetchall()

    frequency_list = []
    intensity_list = []
    for row in rows:
        frequency_list.append(row[0])
        intensity_list.append(row[1])

    return frequency_list, intensity_list


def get_max_frequency(conn, mid):
    """
    Gets the maximum frequency of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Maximum frequency of a molecule
    """
    cursor = conn.execute("SELECT MAX(frequency) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency


def get_max_intensity(conn, mid):
    """
    Gets the maximum intensity of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Maximum intensity of a molecule
    """
    cursor = conn.execute("SELECT MAX(intensity) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity


def get_mid_from_frequency(conn, frequency):

    cursor = conn.execute("SELECT mid FROM peaks "
                          "WHERE frequency=?", (frequency,))
    # print frequency
    row = cursor.fetchone()[0]

    return row


def get_min_frequency(conn, mid):
    """
    Gets the minimum frequency of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: minimum frequency of a molecule
    """
    cursor = conn.execute("SELECT MIN(frequency) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency


def get_peak_count(conn, mid, max_range=None, min_range=None):
    """
    Returns the count of peaks associated with this molecule
    :param conn:
    :param mid:
    :param max_range:
    :param min_range:
    :return:
    """

    if max_range is None:
        cursor = conn.execute("SELECT COUNT(pid) FROM PEAKS"\
                              " WHERE mid=?", (mid,))
        rows = cursor.fetchone()
        return rows[0]

    cursor = conn.execute("SELECT COUNT(pid) FROM PEAKS" \
                          " WHERE mid=? AND frequency<=?", (mid, max_range))
    rows = cursor.fetchone()
    return rows[0]


def get_pid_list(conn, mid):
    """
    Returns PID List (ordered by descending intensity)
    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :return:
    """
    cursor = conn.execute("SELECT pid FROM peaks"\
                          " WHERE mid=?" \
                          " ORDER BY intensity DESC",(mid,))
    rows = cursor.fetchall()

    if rows is not None:
        pid_list = []
        for row in rows:
            pid_list.append(row[0])

        return pid_list

    return None


def get_unassigned_pid_list(conn, mid):
    """

    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :return:
    """
    # Set of all peaks for molecule
    all = "(SELECT peaks.pid FROM molecules JOIN peaks"\
          " ON molecules.mid = peaks.mid"\
          " WHERE molecules.mid={m})".format(m=mid)

    # Set of all assigned peaks of the molecule
    assigned = "(SELECT peaks.pid FROM peaks JOIN assignments"\
               " ON peaks.pid=assignments.pid"\
               " WHERE peaks.mid={m})".format(m=mid)

    # Unassigned peaks (all - assigned)
    unassigned = "SELECT pid FROM " + all + " EXCEPT SELECT pid FROM " + assigned + ";"
    #print unassigned
    cursor = conn.execute(unassigned)

    return cursor.fetchall()


def pid_exists(conn, pid):
    """
    Determines if peaks entry is in the database (based on pid)
    :param conn: Sqlite3 database connection
    :param pid: Peak entry id (mid)
    :return: True if peak entry exists. False if entry does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM peaks WHERE pid=?", (pid,))
    row = cursor.fetchone()

    if row is None:
        # Info entry does not exist.
        return False

    # Info entry exists
    return True

###############################################################################
# Insert Peaks Table Entry
# -----------------------------------------------------------------------------
# Date: 06/27/2016
# -----------------------------------------------------------------------------
# Inserts row entries into the peaks table
# Public Functions:
#       * import_file(conn, file_path, mid):
# Private/Helper Functions::
#       * __import_dptfile(conn, filepath, mid)
#       * __import_txtfile(conn, filepath, mid):
#       * __import_catfile(conn, filepath, mid):
#       * __import_spfile(conn, filepath, mid):
#       * __import_linesfile(conn, filepath, mid):
#       * __import_listfile(conn, filepath, mid):
#       * __checkfile(filepath)
###############################################################################


def add_peak(conn, mid, frequency, intensity):
    """

    :param conn:
    :param mid:
    :param frequency:
    :param intensity:
    :return:
    """
    conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',
                 (mid, frequency, intensity))  # insert into peak table

    conn.commit()
    # Get the new entry's molecule id (mid)
    cursor = conn.execute('SELECT max(pid) FROM peaks')
    pid = cursor.fetchone()[0]

    return pid


def add_peaks(conn, mid, frequencies, intensities):
    """

    :param conn:
    :param mid:
    :param frequencies:
    :param intensities:
    :return:
    """
    if len(frequencies) != len(intensities):
        return ValueError

    for i in range(0, len(frequencies)):
        conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',
                     (mid, frequencies[i], intensities[i]))  # insert into peak table

        # Commit Changes
        conn.commit()


def import_file(conn, filepath, mid, peaks=False):
    """
    Imports file to peak table in spectrum database to it's associative molecule
    Molecule must exist for import
    Supports '.cat' , '.sp', '.lines', '.list', .txt', files.
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

    # Check if molecule entry exists
    if mid_exists(conn, mid) is False:
        # Molecule does not exist, ERR return
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    # Check if file can be opened
    if __checkfile(filepath) is False:
        # File cannot be opened. ERR return
        return False

    # Get File extention
    extention = str.split(filepath, ".")[1]

    # Match extention to its appropriate import function
    if extention == 'cat':
        __import_catfile(conn, filepath, mid)
    elif extention == 'sp':
        __import_spfile(conn, filepath, mid)
    elif extention == 'lines':
        __import_linesfile(conn, filepath, mid)
    elif extention == 'dpt':
        __import_dptfile(conn, filepath, mid)
    elif extention == 'txt':
        __import_txtfile(conn, filepath, mid, peaks)
    elif extention == 'list':
        __import_listfile(conn, filepath, mid)
    elif extention == 'ftb':
        __import_ftbfile(conn, filepath, mid, peaks)
    else:
        print "Invalid import file. EXTENTION must be: '.cat' , '.sp', '.lines'"
        return False

    return True


def __import_dptfile(conn, filepath, mid):
    """
    Inheritently Private Function, determines peaks of .sp File and imports to database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    from analysis import peak_finder

    # Get data from file
    frequencies = []
    intensities = []
    with open(filepath) as f:
        for line in f:
            point = line.split(",")
            frequencies.append(float(point[0]))   # get frequency
            intensities.append(float(point[1]))   # get actual intensity (logx ^ x)

    print "[Data Points collected: " + str(len(frequencies)) + "]"
    # Determine Peaks
    frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.2)

    print "[Peaks found: " + str(len(frequencies)) + "]"
    # Store peaks into file
    for i in range(0, len(frequencies)):
        conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, frequencies[i], intensities[i]))   # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_txtfile(conn, filepath, mid, peaks=False):
    """
    Inheritently Private Function, determines peaks of .sp File and imports to database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    from analysis import peak_finder
    import re

    delimiters = [" ", "\t", ",", ", "]
    regex = '|'.join((map(re.escape, delimiters)))

    # Get data from file
    frequencies = []
    intensities = []
    line_num = 0
    with open(filepath) as f:
        for line in f:
            line_num += 1
            if line is not None or line is not "":
                try:
                    point = re.split(regex, line.strip())

                    frequencies.append(float(point[0]))  # get frequency
                    intensities.append(float(point[1]))  # get actual intensity (logx ^ x)
                except IndexError:
                    print "IndexError in line: " + str(line_num)
                except ValueError:
                    print "ValueError in Line: " + str(line_num)

        if peaks is False:
            # Determine Peaks
            frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.2)

    # Store peaks into file
    for i in range(0, len(frequencies)):
        conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',
                     (mid, frequencies[i], intensities[i]))  # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_catfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports catfile to database
    Adds new molecule entry and its respective peaks
    Cancels action if molecule entry already exists (i.e. name && category)
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

    # Store peak data from file, to 'peaks' table
    # Uses associative 'mid' for entry's foreign key
    linenum = 0
    with open(filepath) as f:
        for line in f:
            linenum +=1
            try:
                point = str.split((line.strip()))
                freq = float(point[0])                         # get frequency
                inte = abs(float(point[2])) ** float(point[2]) # get actual intensity (logx ^ x)
                conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))  # insert into peak table
            except IndexError:
                print "IndexError in line: " + str(linenum)
            except ValueError:
                print "ValueError in Line: " + str(linenum)

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_spfile(conn, filepath, mid):
    """
    Inheritently Private Function, determines peaks of .sp File and imports to database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    from analysis import peak_finder

    # Get data from file
    frequencies = []
    intensities = []
    line_num = 0
    with open(filepath) as f:
        for line in f:
            line_num += 1
            point = str.split((line.strip()))
            try:
                frequencies.append(float(point[0]))  # get frequency
                intensities.append(float(point[1]))  # get actual intensity (logx ^ x)
            except IndexError:
                print "IndexError in line: " + str(line_num)
            except ValueError:
                print "ValueError in Line: " + str(line_num)

    # Determine Peaks
    frequencies, intensities = peak_finder.k_peak_finder(frequencies,
                                                         intensities)  #peak_finder.peak_finder(frequencies, intensities, 0.2)

    # Store peaks into file
    for i in range(0, len(frequencies)):
        conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, frequencies[i], intensities[i]))   # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_linesfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports .lines file to spectrum database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    # Store peak data in file, to 'peaks' table
    with open(filepath) as f:
        for line in f:
            point = str.split((line.strip()))
            freq = float(point[0])      # get frequency
            inte = float(point[1])      # get intensity
            conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))   # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_ftbfile(conn, filepath, mid, peaks=False):
    """
    Inheritently Private Function, determines peaks of .sp File and imports to database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    from analysis import peak_finder
    import re

    delimiters = ["ftmfreq:", "shots:", "dipole:", " ", "#intensity "]
    regex = '|'.join((map(re.escape, delimiters)))

    # Get data from file
    frequencies = []
    intensities = []
    line_num = 0
    with open(filepath) as f:
        for line in f:
            line += 1
            if line is not None or line is not "" or line[0] is '#':
                point = re.split(regex, line.strip())

                try:
                    frequencies.append(float(point[1]))  # get frequency
                    intensities.append(float(point[7]))  # get actual intensity (logx ^ x)
                except IndexError:
                    print "IndexError in line: " + str(line_num)
                except ValueError:
                    print "ValueError in line: " + str(line_num)

    print "PEAKS!!" + str(len(frequencies))
    if peaks is False:
        # Determine Peaks
        frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.2)

    # Store peaks into file
    for i in range(0, len(frequencies)):
        conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',
                     (mid, frequencies[i], intensities[i]))  # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __import_listfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports .list file to spectrum database
    .list file:
        contains a list of only frequencies. All associated
        intensities are automatically set equal to 1.
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    # Store peak data in file, to 'peaks' table
    with open(filepath) as f:
        for line in f:
            try:
                freq = float(line)  # get frequency
                conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?, 1.0)',
                             (mid, freq))  # insert into peak table
            except IndexError:
                continue
            except ValueError:
                continue

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "


def __checkfile(filepath):
    """
    Determines if a file can be opened / is a valid file.
    :param filepath: Filepath/name
    :return: True if file can be opened. False if cannot.
    """
    try:
        myfile = open(filepath)
    except IOError:
        print "Could not open file!"
        return False

    return True


##############################################################################
# Remove Peaks Table Entry
# -----------------------------------------------------------------------------
# Date: 07/01/2016
# -----------------------------------------------------------------------------
# Removes row entry/entries from the peaks table
# Public Functions:
#       * remove_all(conn, mid):
#       * remove_peak(conn, pid)
###############################################################################

def remove_all(conn, mid):
    """
    Removes all entries for a specified molecule
    :param conn: Connection to sqlite3 database
    :param mid: Molecule entry ID (mid) to remove associated peaks
    :return: True, if peaks are removed successfuly, otherwise False
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    conn.execute("DELETE FROM peaks WHERE mid={m}".format(m=mid))
    conn.commit()

    return True

def remove_peak(conn, pid):
    """
    Removes a specified peak entry, by its pid
    :param conn: Connection to sqlite3 database
    :param pid: Peak entry ID (pid
    :return: True, if peak removes successfuly, otherwise False
    """
    # Determine if pid exists
    if(pid_exists(conn, pid) is False):
        # Peak does not exist
        print "[ ERROR: Peak entry does not exist. Cancelling action. ]"
        return False

    # Exists, remove peak
    conn.execute("DELETE FROM peaks WHERE pid={p}".format(p=pid))
    conn.commit()

    return True
