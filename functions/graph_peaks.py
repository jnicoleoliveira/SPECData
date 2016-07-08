from tables.get import get_peaks


def graph_exp_assignment(conn, exp_mid, known_mid):

    # Get Peaks List
    exp_peaks_list = get_peaks.get_pidlist(conn, exp_mid)
    known_peaks_list = get_peaks.get_pidlist(conn, known_mid)

