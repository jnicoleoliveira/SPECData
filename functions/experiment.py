import math as math
from config import conn
from tables.get.get_peaks import get_pid_list
from tables.get.get_peaks import get_frequency, get_intensity

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

        self.__get_peaks()           # Populate Peaks list

    def __get_peaks(self):
        # Get PID List
        # get_pid_list function already returns order by descending intensity
        pid_list = get_pid_list(conn,self.mid)

        Rst = 1 # Ranking of Intensity Strength

        # Create peak objects with PID, and Ranking of Intensity Strength (Rst)
        for pid in pid_list:
            peak = self.Peak(pid, Rst)
            self.experiment_peaks.append(peak)
            Rst += 1

        self.N = Rst   # Store N, the number of Peaks

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
        # Determine probabilities of all the molecule matches
        for key, value in molecule_matches.iteritems():
            value.M = len(molecule_matches)
            value.get_probability()
            #for m in molecule_matches:
        #    m.get_probability()

    def print_matches(self):
        for key, value in self.molecule_matches.iteritems():
            p = value.p *100
            print " " + str(value.name) + "                                 " + str(p) + "%"
        #for match in self.molecule_matches:
        #    print match.name + "     " + str(match.p * 100) + "%"

    class Peak:

        def __init__(self, pid, Rst):
            self.pid = pid
            self.Rst = Rst      # Ranking of strength compared to all peaks
            self.n = 0          # Total number of assignments
            self.matches = []   # Matches
            self.frequency = 0
            self.intensity = 0

            self.__get_frequency_and_intensity()    # Get Frequency and Intensity of the peak

        def __get_frequency_and_intensity(self):
            self.frequency = get_frequency(conn, self.pid)
            self.intensity = get_intensity(conn, self.pid)

        def get_matches(self):
            """

            :return: List of Matches Match()
            """
            if len(self.matches)> 0:
                del self.matches
                self.matches = []

            threshold = 0.2
            frequency = self.frequency

            cursor = conn.cursor()

            # SQLite Script, that returns name, mid, and pid of matched known molecules in database
            #   that are within the threshold of the specified frequency and are
            #   ordered by the closeness of the frequencies to the specified frequency
            script = "SELECT molecules.name, molecules.mid, peaks.pid" \
                     " FROM peaks JOIN molecules" \
                     " WHERE molecules.mid=peaks.mid AND molecules.category='known' AND ABS(peaks.frequency - {freq})<={t}" \
                     " ORDER BY ABS(peaks.frequency - {freq} ) ASC".format(freq=frequency, t=threshold)

            try:
                cursor.execute(script)
            except Exception as e:
                cursor.close()
                raise

            rows = cursor.fetchall()

            self.n = len(rows)                      # Set number of matches
            n_sum = (self.n * (self.n+1))/2
            #n_factorial = math.factorial(self.n)    # Get n!
            i = 0                                   # ith element

            for row in rows:
                #p = float(self.n-i)/float(n_factorial)          # Determine probability of the match, p
                p = float(self.n-i)/n_sum
                i +=1
                #print p
                match = Match(row[0], row[1], row[2], float(p), self.pid, self.Rst)     # Create Match object
                self.matches.append(match)                                       # Add Match to matches

            return self.matches


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
        self.__determine_probability()
        return self.p

    def __determine_probability(self):
        """
        SUM( prob of match * strength of the experimental line) * 1/N!
        :return:
        """
        # Determine summation of matched probabilities
        # Probability == SUM( prob of match * strength of the experimental line)
        n_sum = (self.N*(self.N+1))/2
        m_sum = (self.M*(self.M+1))/2
        for match in self.matches:
            #self.p += float(match.p)
            self.p += (float(match.p)) * (self.N - match.Rst) #* self.m
        #self.p /= self.m

        self.p /= n_sum
        #self.p /= m_sum
        #print self.p
        # Multiply this by 1/N+N-1+...
        #self.p /= n_sum
        #self.p *= 1/(math.factorial(self.N))


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
