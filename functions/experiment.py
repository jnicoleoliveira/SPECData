from config import conn
import tables.get.get_peaks as peaks


class Experiment:

    def __init__(self, name, mid, match_threshold=0.2):
        """
        Experiment Object, represents an experiment, its peaks, molecule matches and its associated probabilities.
        :param name: Name of experiment
        :param mid:  Molecule ID (MID) of experiment
        """
        self.name = name
        self.mid = mid
        self.match_threshold = match_threshold
        self.N = 0                   # Total Number of peak lines
        self.experiment_peaks = []   # List of peaks    (obj: Peak)
        self.molecule_matches = {}   # Dict of Molecule Matches (obj: MoleculeMatch)
        self.possible_matches = {}
        self.exp_average_intensity = None
        self.__setup()           # Populate Peaks list

    def __setup(self):

        # get_pid_list function already returns order by descending intensity
        pid_list = peaks.get_pid_list(conn,self.mid)  # Get PID List of the molecule

        Rst = 1 # Ranking of Intensity Strength

        # Get Average Intensity
        self.exp_average_intensity = peaks.get_average_intensity(conn, self.mid)

        # Create peak objects with PID, and Ranking of Intensity Strength (Rst)
        for pid in pid_list:
            peak = self.Peak(pid, Rst, self.exp_average_intensity)
            self.experiment_peaks.append(peak)
            Rst += 1

        self.N = Rst   # Store N, the number of Peaks


        # Remove Peaks where intensity is less than the average

    def get_experiment_frequencies_intensities_list(self):
        return peaks.get_frequency_intensity_list(conn,self.mid)

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

    def get_assigned_molecules(self):
        """
        Gets Matches/Assignments for peaks
        Populates molecule_matches list
        :return:
        """
        if not self.experiment_peaks:
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
                    molecule_matches[mid] = MoleculeMatch(m.name, mid, self.N)    # New Molecule, add new entry to matches

                molecule_matches[mid].add_match(m)  # Add match to molecule

        # Now, after getting necessary data...
        # Determine initial probabilities of all the molecule matches
        for key, value in molecule_matches.iteritems():
            value.M = len(molecule_matches)
            value.get_probability()
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

    class Peak:

        def __init__(self, pid, Rst, intensity_to_avg):
            self.pid = pid
            self.Rst = Rst      # Ranking of strength compared to all peaks
            self.n = 0          # Total number of assignments
            self.matches = []   # Matches
            self.frequency = 0
            self.intensity = 0
            self.intensity_to_avg = intensity_to_avg
            self.__get_frequency_and_intensity()    # Get Frequency and Intensity of the peak

        def __get_frequency_and_intensity(self):
            self.frequency = peaks.get_frequency(conn, self.pid)
            self.intensity = peaks.get_intensity(conn, self.pid)
            self.intensity_to_avg = self.intensity/self.intensity_to_avg

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
            n_triangle = (self.n * (self.n+1))/2    # Triangular number of n
            i = 0                                   # ith element

            for row in rows:
                #p = float(self.n-i)/n_triangle      # Determine probability of the match, p
                p = (threshold-float(row[3]))/threshold     # Determine probability by range (difference: =0->100% to =threshold->0%)
                p *= (self.intensity/self.intensity_to_avg)
                i +=1
                match = Match(row[0], row[1], row[2], float(p), self.pid, self.Rst)     # Create Match object
                self.matches.append(match)                                              # Add Match to matches

            return self.matches

        def get_candidates(self, threshold):
            frequency = self.frequency

            cursor = conn.cursor()

            # SQLite Script, that returns name, mid, and pid of matched known molecules in database
            #   that are within the threshold of the specified frequency and are
            #   ordered by the closeness of the frequencies to the specified frequency
            script = "SELECT molecules.name, molecules.mid, peaks.pid, ABS(peaks.frequency - {freq})" \
                     " FROM peaks JOIN molecules" \
                     " WHERE molecules.mid=peaks.mid AND molecules.category='known' AND ABS(peaks.frequency - {freq})<={t}" \
                     " ORDER BY ABS(peaks.frequency - {freq} ) ASC".format(freq=frequency, t=threshold)

            try:
                cursor.execute(script)
            except Exception as e:
                cursor.close()
                raise

            rows = cursor.fetchall()
            return rows


class MoleculeMatch:

    def __init__(self, name, mid, N):
        """

        :param name: Name of Matched Molecule
        :param mid: MID of Matched Molecule
        """
        self.M = 0
        self.N = N
        self.name = name
        self.mid = mid

        self.ratio = 0
        self.m = 0          # Total number of matches
        self.matches = []   # List of Match matches
        self.p = 0          # Total Probability of the molecule

    def add_match(self, match):
        """

        :param match:
        :return:
        """
        self.matches.append(match)
        self.m += 1

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
        total_peaks = peaks.get_peak_count(conn, self.mid)
        ratio = float(self.m) / total_peaks
        #print ratio
        if float(ratio) < 0.2:
            #print ratio
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
        N_triangle = (self.N*(self.N+1))/2      # Trianglar sum of N
        m_sum = (self.M*(self.M+1))/2
        peak_p = 0

        # Determine summation of matched peaks
        for match in self.matches:
            peak_p += float(match.p) * (self.N - match.Rst - 1)

        self.p *= peak_p
        self.p /= N_triangle    # Divide by n-triangle
        #self.p /= self.m
        #self.p /= m_sum

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
