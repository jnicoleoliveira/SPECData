import sqlite3
from tables.peaks.peaks_get import *

def get_candidates(conn, frequency):
    cursor = conn.cursor()

    script= "SELECT molecules.name, molecules.mid, peaks.pid, peaks.frequency" \
            " FROM peaks JOIN molecules"\
            " WHERE molecules.mid=peaks.mid AND molecules.category='known'" \
            " ORDER BY ABS(peaks.frequency - {freq} ) ASC" \
            " LIMIT 5;".format(freq = frequency)
    print script

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
    unassigned_pids = get_unassigned_pidlist(conn,mid)    # get unnasigned exp pidlist
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
    # Get pid List
    pidlist = []
    pidlist = get_pidlist(conn, mid)
    alist = get_assignments(conn, pidlist)
    print alist


def get_assignments(conn, pidlist):
    assignment_list = []

    for pid in pidlist:
        pid = pid[0]    # Get tuple
        exp_freq = get_frequency(conn, pid)   # Get frequency

        # Get Candidate assignment
        name, assigned_mid, assigned_pid, frequency = get_candidates(conn, exp_freq)

        # Add candidate
        print "ASSIGNING peak(" + str(pid) + "): freq: " + str(exp_freq) + " TO " + name + "freq: " + str(frequency)
        add_assignment(conn, pid, assigned_mid)
        assignment_list.append(name)

    return assignment_list


def add_assignment(conn, pid, assigned_mid):
    cursor = conn.execute("INSERT INTO assignments(pid, assigned_mid) VALUES (?,?)",(pid, assigned_mid))
    conn.commit()


def printCursor(cursor):
    string = ""
    for row in cursor.fetchall():
        for column in row:
            string = string + "\t" + str(column)
        string = string + "\n"
    print string
