from tables.entry.entry_assignments import *
from tables.get.get_peaks import *


def get_candidates(conn, frequency, threshold):
    cursor = conn.cursor()

    script= "SELECT molecules.name, molecules.mid, peaks.pid, peaks.frequency" \
            " FROM peaks JOIN molecules"\
            " WHERE molecules.mid=peaks.mid AND molecules.category='known' AND ABS(peaks.frequency - {freq})<={t}" \
            " ORDER BY ABS(peaks.frequency - {freq} ) ASC" \
            " LIMIT 5;".format(freq = frequency, t=threshold)
    #print script

    try:
        cursor.execute(script)
    except Exception as e:
        cursor.close()
        raise

    row = cursor.fetchone()
    return row

def get_initial_candidates(conn, frequency, query_pool, threshold):
    cursor = conn.cursor()

    script= "SELECT molecules.name, molecules.mid, peaks.pid, peaks.frequency" \
            " FROM molecules JOIN peaks" \
            " ON pid IN ( " + query_pool + " AND ABS(peaks.frequency - {freq})<={t})" \
            " ORDER BY ABS(peaks.frequency - {freq}) ASC" \
            " LIMIT 5;".format(t=threshold, freq=frequency)
   # print "\n Script: "
    #print script
    try:
        cursor.execute(script)
    except Exception as e:
        cursor.close()
        raise

    return cursor.fetchone()

def assign_from_list(conn, mid, midlist):
    unassigned_pids = get_unassigned_pid_list(conn,mid)    # get unnasigned exp pidlist
    query_pool = __midlist_to_pidlist_query(midlist)
    assignment_list = []
    for pid in unassigned_pids:
        pid = pid[0]
        exp_freq = get_frequency(conn, pid)   # Get exp frequency
        valid_peak = False
        try:
            name, assigned_mid, assigned_pid, assigned_freq = get_initial_candidates(conn, exp_freq, query_pool, 0.2)
            valid_peak=True
        except TypeError:
            valid_peak=False
            #print "Type Error: Trying next peak."
            print "TYPEERROR:: Frequency: " + str(exp_freq) + " has no match."

        if(valid_peak is True):
            # Add candidate
            print '\033[93m' + "ASSIGNING peak(" + str(pid) + "): freq: " + str(exp_freq) + " TO " + name + "freq: " + str(assigned_freq) + '\033[0m'
            add_assignment(conn, pid, assigned_mid)
            assignment_list.append(name)

    return assignment_list

def __midlist_to_pidlist_query(midlist):
    sql = "SELECT pid FROM molecules JOIN peaks " \
          "ON molecules.mid = peaks.mid AND ( peaks.mid={m}".format(m=midlist[0])

    for i in range(1, len(midlist)):
        sql += " OR peaks.mid=" + str(midlist[i])
    sql += ")"
    return sql

def assign_peaks(conn, mid):
    """
    Assigns peaks of an experiment molecule to known peaks
    Inputs assignments in database
    Returns a list of assignment names
    :param conn: Connection to SQLite database
    :param mid: Molecule ID (mid) to assign peaks to
    :return: List of assignment names
    """
    # Get pid List
    experiment_pids = get_pid_list(conn, mid)
    assignments = calculate_assignments(conn, mid, experiment_pids)
    return assignments


def calculate_assignments(conn, mid, pid_list):
    assignment_list = []

    for pid in pid_list:
        ##pid = pid[0]    # Get value in tuple
        exp_freq = get_frequency(conn, pid)   # Get frequency
        exp_inte = get_intensity(conn, pid)   # Get intensity

        try:
            # Get Candidate assignment
            name, assigned_mid, assigned_pid, assigned_freq = get_candidates(conn, exp_freq, 0.2)
        except TypeError:
            print "TYPEERROR:: Frequency: " + str(exp_freq) + " has no match."
            continue

        # Add Assignment to list
        add_assignment(conn, pid, mid, assigned_mid, assigned_pid)
        assignment_list.append(name)
        print '\033[91m' + "ASSIGNING peak(" + str(pid) + "):    [INTENSITY: " + str(exp_inte) + "]" \
            "[FREQ: " + str(exp_freq) + "]      TO      " + name + \
            " [FREQ: " + str(assigned_freq) + "] " + '\033[0m'

    return assignment_list


def printCursor(cursor):
    string = ""
    for row in cursor.fetchall():
        for column in row:
            string = string + "\t" + str(column)
        string = string + "\n"
    print string
