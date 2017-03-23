import tables.affirmedassignment_table as affirmed_assignments
import tables.assignments_table as assignments
import tables.experimentinfo_table as info
import tables.molecules_table as molecules
import tables.peaks_table as peaks
from config import conn


class Experiment:

    exp_average_intensity = None
    max_frequency = None
    def __init__(self, name, mid, match_threshold=0.2):
        """
        Experiment Object, represents an experiment, its peaks, molecule matches and its associated probabilities.
        :param name: Name of experiment
        :param mid:  Molecule ID (MID) of experiment
        """
        self.name = name
        self.mid = mid
        self.match_threshold = match_threshold
        self.ratio_threshold = 0.05

        self.N = 0                   # Total Number of peak lines
        self.experiment_peaks = []   # List of peaks    (obj: Peak)
        self.validated_peaks = []    # Subset of experiment peaks (if saved)
        self.is_saved = False

        # Match info
        self.validated_matches = {}
        self.molecule_matches = {}   # Dict of Molecule Matches (obj: MoleculeMatch)
        self.possible_matches = {}
        self.__setup__()             # Populate Peaks list

    ###############################################################################
    # Setup Functions
    ###############################################################################
    def __setup__(self):

        # get_pid_list function already returns order by descending intensity
        pid_list = peaks.get_pid_list(conn,self.mid)  # Get PID List of the molecule

        Rst = 1 # Ranking of Intensity Strength

        # Get Average Intensity
        Experiment.exp_average_intensity = peaks.get_average_intensity(conn, self.mid)

        # Get Max Frequency
        Experiment.max_frequency = peaks.get_max_frequency(conn, self.mid)

        # Create peak objects with PID, and Ranking of Intensity Strength (Rst)
        for pid in pid_list:

            peak = self.Peak(pid, Rst)  # create peak object

            # Determine if the peak has an existing assignment
            aid = assignments.assignment_exists(conn, pid)

            if aid:
                # print "ADDING: " + str(aid)
                self.__add_existing_assignment(aid, peak)
            else:
                # No assignment. Add to experiment peaks to be analyzed
                self.experiment_peaks.append(peak)
                Rst += 1

        self.N = Rst   # Store N, the number of Peaks
        # Remove Peaks where intensity is less than the average

    def __add_existing_assignment(self, aid, peak):

        self.is_saved = True

        # -- Collect Data -- #
        pid = peak.pid
        status = affirmed_assignments.get_status(conn, aid)
        assigned_pid = assignments.get_assigned_pid(conn, aid)
        mid = peaks.get_mid(conn, assigned_pid)
        name = molecules.get_name(conn, mid)

        # Create a Match Object
        match = Match(name, mid, assigned_pid, 1, pid, 1)

        # Add to Validated_Matches (MoleculeMatch subset)
        if status == 'validated':
            self.validated_peaks.append(peak)

            if self.validated_matches.has_key(mid) is False:
                self.validated_matches[mid] = self.MoleculeMatch(name, mid, self.N, self.ratio_threshold)
                self.validated_matches[mid].set_status_as_validated()
                self.validated_matches[mid].p = 1

            self.validated_matches[mid].add_match(match)

    def __load_saved_data(self):
        print "[LOADED SAVED DATA]"
        self.experiment_peaks.extend(self.validated_peaks)
        self.molecule_matches.update(self.validated_matches)

    ###############################################################################
    # Analysis Functions
    ###############################################################################
    def get_assigned_molecules(self):
        """
        Gets Matches/Assignments for peaks
        Populates molecule_matches list
        :return:
        """
        if not self.experiment_peaks:
            print "[ No peaks in experiment found ]"
            return  # NEED TO THROW ERROR HERE

        molecule_matches = self.molecule_matches

        # Get Matches for each peak
        for p in self.experiment_peaks:
            matches = p.get_matches()       # Get Matches associated with the peak

            # Add matches to associated Molecule Match
            for m in matches:
                mid = m.mid

                # Determine if this is match is of a new molecule
                if molecule_matches.has_key(mid) is False:
                    # New Molecule, add new entry to matches
                    molecule_matches[mid] = self.MoleculeMatch(m.name, mid, self.N, self.ratio_threshold)

                molecule_matches[mid].add_match(m)  # Add match to molecule

        # Now, after getting necessary data...
        # Determine initial probabilities of all the molecule matches
        for key, value in molecule_matches.iteritems():
            value.M = len(molecule_matches)
            value.get_probability()
            # print value.name + "(" + str(value.m) + ")"
        print "\tCandidate Matches: " + str(len(molecule_matches))

        mm = molecule_matches.copy()
        # Remove all false matches
        for key, value in mm.iteritems():
            if value.p is 0:
                del molecule_matches[key]
        print "\tLikely Matches: " + str(len(molecule_matches))

        # Reavaluate probabilities
        for key, value in molecule_matches.iteritems():
            value.M = len(molecule_matches)
            value.get_probability()

        if self.is_saved:
            self.__load_saved_data()

    def add_a_molecule(self, mid):
        name = molecules.get_name(conn, mid)
        mol = Experiment.MoleculeMatch(name, mid, self.N)

        cursor = conn.cursor()

        for p in self.experiment_peaks:

            if p.is_pending():
                frequency = peaks.get_frequency(conn, p.pid)
                script = "SELECT name, mid, pid, MIN(ABS(frequency - {freq})) FROM" \
                         " (SELECT molecules.name, molecules.mid, peaks.pid, peaks.frequency" \
                         " FROM peaks JOIN molecules " \
                         " ON peaks.mid=molecules.mid" \
                         " WHERE molecules.mid={mid} AND ABS(peaks.frequency - {freq}) <= {thresh})" \
                         "".format(mid=mid, freq=frequency, thresh=self.match_threshold)
                try:
                    cursor.execute(script)
                except Exception as e:
                    cursor.close()
                    raise
                rows = cursor.fetchone()
                if rows is not None and rows[0] is not None:
                    print "found match!"
                    print rows
                    row = rows[0]
                    name = row[0]
                    mid = row[1]
                    pid = row[2]
                    distance = row[3]

                    match = Match(name, mid, pid, 1, p.pid, 1)
                    mol.add_match(match)
        self.molecule_matches[mid] = mol
        return mol

    ###############################################################################
    # Status Functions
    ###############################################################################
    def validate_a_match(self, mid):
        #if mid is not None:
        self.molecule_matches[mid].set_status_as_validated()

        self.validated_matches[mid] = self.molecule_matches[mid]
        #    del self.molecule_matches[mid]

        pids = []
        for m in self.molecule_matches[mid].matches:
            pids.append(m.exp_pid)

        for peak in self.experiment_peaks:
            if peak.pid in pids:
                peak.set_status_as_validated()

    def invalidate_a_match(self, mid):
        #if mid is not None:
        self.molecule_matches[mid].set_status_as_invalidated()

        #self.invalidated_matches[mid] = self.molecule_matches[mid]
        #    del self.molecule_matches[mid]

        pids = []
        for m in self.molecule_matches[mid].matches:
            pids.append(m.exp_pid)

        for peak in self.experiment_peaks:
            if peak.pid in pids:
                # reset experiment peak to be pending, if previously validated
                peak.set_status_as_pending()

    def save_affirmed_matches(self):
        """
        Saves all verified matches (rejected, or accepted)
        :return:
        """

        # delete all currently associated
        affirmed_assignments.remove_all(conn, self.mid)
        assignments.remove_all(conn, self.mid)

        # add current association
        for key, value in self.molecule_matches.iteritems():

            if value.is_validated() or value.is_invalidated():
                for m in value.matches:
                    exp_pid = m.exp_pid
                    assigned_pid = m.pid
                    if not assignments.assignment_exists(conn, exp_pid, assigned_pid):
                        aid = assignments.new_assignment_entry(conn, exp_pid, assigned_pid)
                        affirmed_assignments.new_entry(conn, aid, value.status)

    ###############################################################################
    # Getter Functions
    ###############################################################################
    def get_experiment_frequencies_intensities_list(self):
        return peaks.get_frequency_intensity_list(conn, self.mid)

    def get_unvalidated_experiment_intensities_list(self):
        """
        Gets the frequencies and intensities of ONLY invalidated
        experimental peaks.
        :return:
        """
        frequencies = []
        intensities = []

        for p in self.experiment_peaks:
            if not p.is_validated():
                f, i = peaks.get_frequency_intensity(conn, p.pid)
                frequencies.append(f)
                intensities.append(i)

        return frequencies, intensities

    def get_unvalidated_pids_list(self):
        """
        Gets the pids of ONLY unvalidated
        experimental peaks.
        :return:
        """
        pids = []

        for p in self.experiment_peaks:
            if not p.is_validated():
                pids.append(p.pid)

        return pids

    def get_validated_experiment_intensities_list(self):
        """x
        Gets the frequencies and intensities of ONLY validated
        experimental peaks.
        :return:
        """
        frequencies = []
        intensities = []

        for p in self.experiment_peaks():
            if p.is_validated():
                f, i = peaks.get_frequency_intensity(conn, p.pid)
                frequencies.append(f)
                intensities.append(i)

        return frequencies, intensities

    def get_cleaned_experiment_intensities_list(self, validated_mids):
        """
        Returns a list of frequencies and intensities of
        lines that were assigned by the molecules with the
        given validated_mids. If a molecule given is not validated,
        the matches will not be cleared.
        :param validated_mids: List of validated molecule mids
        :return:
        """
        minus_pids = []  # List of pids to be extracted
        frequencies = []
        intensities = []

        ''' Get List of pids associated with validated_mids '''
        for mid in validated_mids:
            match = self.molecule_matches[mid]
            if match.is_validated():
                minus_pids.extend(match.get_matched_experiment_pids())

        ''' Get list of Frequencies/Intensites - peaks in minus_pids '''
        for p in self.experiment_peaks:
            if p.pid not in minus_pids:
                frequencies.append(p.frequency)
                intensities.append(p.intensity)
        return frequencies, intensities

    def get_assigned_peaks_count(self):
        count = 0
        for key, value in self.molecule_matches.iteritems():
            count += value.m

        return count

    def get_validated_count(self):
        """

        :return:
        """
        peak_count = 0
        mol_count = 0
        for key, value in self.molecule_matches.iteritems():
            if value.is_validated():
                mol_count += 1
                peak_count += len(value.matches)

        return mol_count, peak_count

    def get_unnassigned_count(self):
        return len(self.experiment_peaks) - self.get_validated_count()[1]

    def get_validated_molecules_count(self):
        return len(self.validated_matches)

    def get_invalidated_peaks_count(self):
        """

        :return:
        """
        peak_count = 0
        mol_count = 0
        for key, value in self.molecule_matches.iteritems():
            if value.is_invalidated():
                mol_count += 1
                peak_count += len(value.matches)
        return mol_count, peak_count

    def get_assigned_names(self):
        assigned_names = []
        for key, value in self.molecule_matches.iteritems():
            assigned_names.append(value.name)

        return assigned_names

    def get_assigned_mids(self):
        assigned_mids = []
        for key, value in self.molecule_matches.iteritems():
            assigned_mids.append(value.mid)

        return assigned_mids

    def is_validated_molecule(self, mid):
        """ Determines if a molecule is validated"""
        return mid in self.validated_matches

    def get_sorted_molecule_matches(self):
        import operator
        # Get Tuples
        sorted = self.molecule_matches.values()
        sorted.sort(key=operator.attrgetter('p'), reverse=True)

        return sorted

    def get_all_matches_list(self):
        """ Gets list of all molecule_matches's matches"""
        matches = []
        for key, value in self.molecule_matches.iteritems():
            matches.extend(value.matches)

        return matches

    def get_unassigned_peaks(self):
        unassigned = []
        for p in self.experiment_peaks:
            if p.status == "validated" is False:
                unassigned.append(p)
        return unassigned

    def print_matches(self):
        """
        Print Molecule Matches of experiment.
        :return:
        """
        buff = 30       # Space Buffer
        scale = 100     # Scale Factor (p * scale)
        sorted = []     # Sorted tuple(name,p) list

        print "NAME" + (' '*(buff - 4)) + "[P]    " + "[RATIO]"     # Print Header
        print '-' * (buff+12)

        # Get Tuples
        for key, value in self.molecule_matches.iteritems():
            sorted.append((key, value.p * scale))    # Append name and scaled probability values

        sorted.sort(key=lambda tup: tup[1],reverse=True)    # Sorts tuples in place

        for value in sorted:
            name = str(self.molecule_matches[value[0]].name)
            prob = str(round(value[1], 2))
            ratio = str(round(self.molecule_matches[value[0]].ratio, 2))

            space_length = buff - len(name)                           # Get length of space
            print name + (' ' * space_length) + prob + "   " + ratio  # Print Line

    def get_type(self):
        return info.get_type(conn, self.mid)

    def get_units(self):
        return info.get_units(conn, self.mid)

    def get_composition(self):
        return info.get_composition(conn, self.mid)

    def get_notes(self):
        return info.get_notes(conn, self.mid)

    ###############################################################################
    #
    # Internal Classes
    #
    ###############################################################################
    class Peak:

        def __init__(self, pid, Rst):
            """

            :param pid:
            :param Rst:
            """
            ''' Analysis '''
            self.pid = pid
            self.Rst = Rst      # Ranking of strength compared to all peaks
            self.n = 0          # Total number of assignments
            self.matches = []   # Matches

            ''' Peak Attributes '''
            self.frequency = 0
            self.intensity = 0
            self.intensity_to_avg = None

            ''' Validation '''
            self.status = "pending"
            self.validated_match = None

            ''' Get Data '''
            self.__get_frequency_and_intensity()    # Get Frequency and Intensity of the peak

        ###############################################################################
        # Status Functions
        ###############################################################################

        def set_status_as_validated(self):
            """ Sets status a validated"""
            self.status = "validated"

        def set_status_as_pending(self):
            """ Sets status a pending"""
            self.status = "pending"

        def is_validated(self):
            """
            Determines if status is validated
            :return: True if status is validated, Otherwise: False
            """
            if self.status is "validated":
                return True
            return False

        def is_pending(self):
            """
            Determines if status is pending
            :return: True if status is pending, Otherwise: False
            """
            if self.status is "validated":
                return True
            return False

        ###############################################################################
        # Setup Functions
        ###############################################################################

        def __get_frequency_and_intensity(self):
            self.frequency = peaks.get_frequency(conn, self.pid)
            self.intensity = peaks.get_intensity(conn, self.pid)
            self.intensity_to_avg = self.intensity/Experiment.exp_average_intensity

        ###############################################################################
        # Analysis Functions
        ###############################################################################

        def get_matches(self):
            """

            :return: List of Matches Match()
            """

            if len(self.matches)> 0:
                del self.matches
                self.matches = []

            threshold = 0.2
            rows = self.get_candidates(threshold)   # Get candidates. Tuple: (name, mid, pid, difference_freq)

            self.n = len(rows)                      # Set number of matches
            #n_triangle = (self.n * (self.n+1))/2    # Triangular number of n
            i = 0                                   # ith element

            for row in rows:
                #p = float(self.n-i)/n_triangle      # Determine probability of the match, p
                name = row[0]
                mid = row[1]
                pid = row[2]
                distance = row[3]
                # Determine probability by range (difference: =0->100% to =threshold->0%)
                p = (threshold-float(distance))/threshold
                p *= (self.intensity/self.intensity_to_avg)
                i +=1
                match = Match(name, mid, pid, float(p), self.pid, self.Rst)     # Create Match object
                self.matches.append(match)                                              # Add Match to matches

            return self.matches

        def get_candidates(self, threshold):
            frequency = self.frequency

            cursor = conn.cursor()

            # SQLite Script, that returns name, mid, and pid of matched known molecules in database
            #   that are within the threshold of the specified frequency and are
            #   ordered by the closeness of the frequencies to the specified frequency
            #script = "SELECT molecules.name, molecules.mid, peaks.pid, ABS(peaks.frequency - {freq})" \
            #         " FROM peaks JOIN molecules" \
            #         " WHERE molecules.mid=peaks.mid AND molecules.category='known' AND ABS(peaks.frequency - {freq})<={t}" \
            #         " ORDER BY ABS(peaks.frequency - {freq} ) ASC".format(freq=frequency, t=threshold)
            script = "SELECT name, mid, pid, MIN(ABS(frequency - {freq})) FROM" \
                        " (SELECT molecules.name, molecules.mid, peaks.pid, peaks.frequency" \
                        " FROM peaks JOIN molecules" \
                        " WHERE molecules.mid=peaks.mid AND molecules.category IN ('known', 'artifact') AND ABS(peaks.frequency - {freq})<={t}" \
                        " ORDER BY ABS(peaks.frequency - {freq} ) ASC)" \
                      " GROUP BY mid".format(freq=frequency, t=threshold)

            try:
                cursor.execute(script)
            except Exception as e:
                cursor.close()
                raise

            rows = cursor.fetchall()
            return rows

    class MoleculeMatch:

        def __init__(self, name, mid, N, ratio_threshold):
            """

            :param name: Name of Matched Molecule
            :param mid: MID of Matched Molecule
            """
            self.M = 0
            self.N = N
            self.name = name
            self.mid = mid

            self.ratio_threshold = ratio_threshold
            self.ratio = 0
            self.m = 0          # Total number of matches
            self.matches = []   # List of Match matches
            self.p = 0          # Total Probability of the molecule

            self.status = "pending"

        ###############################################################################
        # Status Functions
        ###############################################################################

        def set_status_as_validated(self):
            self.status = "validated"

        def set_status_as_invalidated(self):
            self.status = "invalidated"

        def is_validated(self):
            """
            Determines if status is validated
            :return: True if status is validated, Otherwise: False
            """
            if self.status == "validated":
                return True
            return False

        def is_invalidated(self):
            """
            Determines if status is invalidated
            :return: True if status is invalidated, Otherwise: False
            """
            if self.status == "invalidated":
                return True
            return False

        def is_pending(self):
            """
            Determines if status is pending
            :return: True if status is pending, Otherwise: False
            """
            if self.status is "pending":
                return True
            return False

        ###############################################################################
        # Analysis Functions
        ###############################################################################

        def get_probability(self):
            """
            Returns the probability of the molecule's presence in the Experiment
            :return:
            """
            self.p = 0
            if self.determine_valid_ratio() is True:
                self.__determine_probability()  # Determine probability

            return self.p

        def determine_valid_ratio(self):
            # Determine matches to all peaks ratio
            total_peaks = peaks.get_peak_count(conn, self.mid, Experiment.max_frequency)
            ratio = float(self.m) / total_peaks

            if float(ratio) < self.ratio_threshold:
                return False

            self.ratio = ratio
            return True

        def __determine_probability(self):
            """
            SUM( prob of match * strength of the experimental line) * 1/N!
            :return:
            """
            self.p = 1
            # Probability == SUM( prob of match * strength of the experimental line)
            N_triangle = (self.N*(self.N+1))/2      # Triangular sum of N
            if N_triangle == 0:
                return 0
            m_sum = (self.M*(self.M+1))/2
            peak_p = 0

            # Determine summation of matched peaks
            for match in self.matches:
                peak_p += float(match.p) * (self.N - match.Rst - 1)

            self.p *= peak_p
            self.p /= N_triangle    # Divide by n-triangle
            #self.p /= self.m
            #self.p /= m_sum

        def add_match(self, match):
            """

            :param match:
            :return:
            """
            self.matches.append(match)
            self.m += 1

        def get_matched_experiment_pids(self):
            pids = []
            for m in self.matches:
                pids.append(m.exp_pid)

            return pids


class Match:

    def __init__(self, name, mid, pid, p, exp_pid, Rst):
        """

        :param name: Name of Match
        :param mid: MID of Match
        :param pid: PID of Match
        :param p: Probability of Match
        :param exp_pid: Experiment PID
        :param Rst: Ranking of Intensity Strength of the Experiment Peak
        """
        self.name = name
        self.mid = mid
        self.pid = pid
        self.p = p
        self.exp_pid = exp_pid
        self.Rst = Rst      # Ranking of strength in experiment line
