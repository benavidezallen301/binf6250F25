from numpy._typing import _BoolCodes
from pandas.core.dtypes.generic import ABCDataFrame
import numpy as np  # Workhorse
import numpy.random as nr  # Setting up random distributions
import pandas as pd  # Simple convergence checks
from itertools import product  # For robust iteration
from copy import deepcopy  # For convergence checking
from array import array  # Faster base Python iteration
from collections import defaultdict 

try:
    # Special Json library that isn't only more efficient,
    # but also allows for setting floating point precision on print
    import ujson as json

    def to_json(data, precision=2):
        """Wrapper function to output dict to json with specific floating-point
        precision.

        Args:
            data (dict): some HMM probability matrix
            precision (int): Setting for floating-point precision (default: 2)

        Returns:
            (json): JSON representation of the dictionary
        """
        return json.dumps(data, indent=4, double_precision=precision)

except ImportError:
    import json

    def to_json(data, precision=2):
        """Wrapper function to output dict to json with specific floating-point
        precision.

        Note: Since the base `json.dumps` doesn't provide double_precision,
        this goes through an extra encoder step to handle the floats

        Args:
            data (dict): some HMM probability matrix
            precision (int): Setting for floating-point precision (default: 2)

        Returns:
            (json): JSON representation of the dictionary
        """
        out_json = json.dumps(data)
        loaded_json = json.loads(out_json, parse_float=lambda o: f"{float(o):.2g}")
        return json.dumps(loaded_json, sort_keys=True, indent=4)


# Gil-ify
np.set_printoptions(precision=2)
pd.set_option("precision", 2)


class BaseHMM(object):


    """Base class for HMM objects

    Class for holding HMM parameters and to allow for implementation of
    functions associated with HMMs

    Attributes:
        alphabet (str): The emissions used in the HMM (default: 'ACGT')
        hidden_states (str): The hidden states within the HMM (default: None)
        init_probs (dict of floats): β probabilities for initial steps (default: None)
        trans_probs (dict of dict of floats): Transition probabilities from one state to another given a state (default: None)
        emit_probs (dict of dict of floats): Emission probabilities of a letter given a state (default: None)
    """

    __all__ = ["alphabet", "hidden_states", "emit_probs", "trans_probs", "init_probs"]

    def __init__(
        self,
        alphabet="ARNDCEQGHILKMFPSTWYV",  # symbols of amino acids
        hidden_states=None,
        init_probs=None,
        trans_probs=None,
        emit_probs=None,
        seed=None,
        precision=2,
        tolerance=1e-10,
    ):
        """Instantiate the HMM

        Args:
            alphabet (str): The emissions used in the HMM (default: 'ACGT')
            hidden_states (list): The hidden states within the HMM (default: None)
            init_probs (dict of floats): β probabilities for initial steps (default: None)
            trans_probs (dict of dict of floats): Transition probabilities from one state to another given a state (default: None)
            emit_probs (dict of dict of floats): Emission probabilities of a letter given a state (default: None)
            seed (int): To set the random seed for numpy (default: None)
            precision (int): Floating-point precision (default: 2)
            tolerance (number): The acceptable tolerance between baum-welch iteration to determine if convergence has occured (default: 1e-10)
        """

        # Floating point precision
        self._precision = precision

        # For convergence checking
        self._tolerance = tolerance

        # Need at least the hidden states to initialize
        if hidden_states is None:
            raise ValueError('Hidden states must be provided')
        self.hidden_states = hidden_states
        self.alphabet = alphabet

        # Cursory initialization that allows users to set some prior
        self.init_probs = init_probs
        self.trans_probs = trans_probs
        self.emit_probs = emit_probs
        
        # If the user doesn't provide any probabilities, randomize some stuff
        self._initialize_random(seed)
    
    def _initialize_random(self, seed):
        """[PRIVATE] Used to completely initialize the HMM if any probability matrices
        provided. Will not overwrite given probabilities.

        Args:
            seed (int): To set the random seed for numpy
        """
        nr.seed(seed)
        if self.init_probs is None:

            # These aliases help keep line width down during the iteration and allows 
            # for simple dictionary comprehension
            states = self.hidden_states
            i_probs = nr.dirichlet(np.ones(len(self.hidden_states)))

            # Make a dictionary of floats (that sum up to 1) for all states in the HMM
            init = {state: np.float64(i_prob) for state, i_prob in zip(states, i_probs)}
            self.init_probs = init

        if self.trans_probs is None:

            # These aliases help keep line width down during the iteration and allows 
            # for simple dictionary comprehension
            states = product(self.hidden_states, self.hidden_states)
            t_probs = np.nditer(nr.dirichlet(np.ones(len(self.hidden_states)), size=len(self.hidden_states)))

            # Make a dictionary for each state that contains a dictionary of floats
            # that sum to 1 and represent each of the states used in the HMM
            trans = {}
            for (state, next_state), t_prob in zip(states, t_probs):
                trans.setdefault(state, {}).update({next_state: np.float64(t_prob)})
            self.trans_probs = trans

        if self.emit_probs is None:

            # These aliases help keep line width down during the iteration and allows 
            # for simple dictionary comprehension
            states_letters = product(self.hidden_states, self.alphabet)
            e_probs = np.nditer(nr.dirichlet(np.ones(len(self.alphabet)), size=len(self.hidden_states)))

            # Make a dictionary for each state that contains a dictionary of floats
            # that sum to 1 and represent each of the emissions used in the HMM
            emit = {}
            for (state, letter), e_prob in zip(states_letters, e_probs):
                emit.setdefault(state, {}).update({letter: np.float64(e_prob)})
            self.emit_probs = emit

    # All the `@property` and `@''.setter` methods are doing are allowing
    # for isolation and encapsulation of the internal datasets

    @property
    def init_probs(self):
        return self._initial

    @init_probs.setter
    def init_probs(self, init_probs):
        if init_probs is None:
            self._initial = None
        elif isinstance(init_probs, dict):
            if len(init_probs) != len(self.hidden_states):
                raise ValueError('Initial probabilites must be the length of the number of hidden states')
            if not np.isclose(sum(init_probs.values()), 1):
                raise ValueError('Initial probabilites must sum to 1')
            self._initial = init_probs
        else:
            raise SyntaxError('Initial probabilities must be None or a dictionary')

    @property
    def trans_probs(self):
        return self._transition

    @trans_probs.setter
    def trans_probs(self, trans_probs):
        if trans_probs is None:
            self._transition = None
        elif isinstance(trans_probs, dict):
            if len(trans_probs) != len(self.hidden_states):
                raise ValueError('Transition probabilites must be a square matrix')
            if len(trans_probs[self.hidden_states[0]]) != len(self.hidden_states):
                raise ValueError('Transition probabilites must be a square matrix')
            if not np.allclose([sum(trans_probs[state].values()) for state in self.hidden_states], 1):
                raise ValueError('Transition probabilites must sum to 1 along a given axis')
            self._transition = trans_probs
        else:
            raise SyntaxError('Transition probabilities must be None or a dictionary')

    @property
    def emit_probs(self):
        return self._emission

    @emit_probs.setter
    def emit_probs(self, emit_probs):
        if emit_probs is None:
            self._emission = None
        elif isinstance(emit_probs, dict):
            if len(emit_probs) != len(self.hidden_states):
                raise ValueError('Emission probabilites must be length of hidden states by length of alphabet')
            if len(emit_probs[self.hidden_states[0]]) != len(self.alphabet):
                raise ValueError('Emission probabilites must be length of hidden states by length of alphabet')
            emit = pd.DataFrame.from_dict(emit_probs).T
            emit.columns = list(self.alphabet)
            if not np.allclose([sum(emit_probs[state].values()) for state in self.hidden_states], 1):
                raise ValueError('Emission probabilites must sum to 1 along a given axis')
            self._emission = emit_probs
        else:
            raise SyntaxError('Emission probabilities must be None or a dictionary')

    @property
    def hidden_states(self):
        return self._hidden_states

    @hidden_states.setter
    def hidden_states(self, hidden_states):
        if isinstance(hidden_states, str):
            self._hidden_states = hidden_states
        elif isinstance(hidden_states, (tuple, list)):
            self._hidden_states = ''.join(hidden_states)

    @property
    def alphabet(self):
        return self._alph

    @alphabet.setter
    def alphabet(self, alphabet):
        if isinstance(alphabet, str):
            self._alph = alphabet
        elif isinstance(alphabet, (tuple, list)):
            self._alph = ''.join(alphabet)

    def __str__(self):
        out_text = [f'Alphabet: {self.alphabet}',
                    f'Hidden States: {self.hidden_states}',
                    f'Initial Probabilities: {to_json(self.init_probs, self._precision)}',
                    f'Transition Probabilities: {to_json(self.trans_probs, self._precision)}',
                    f'Emission Probabilities: {to_json(self.emit_probs, self._precision)}']
        return '\n'.join(out_text)

    @classmethod
    def __dir__(cls):
        return cls.__all__

    def __eq__(self, other):
        """Solely used by the `baum_welch` function to check for convergence"""
        if np.allclose(pd.Series(self.init_probs), pd.Series(other.init_probs), atol=self._tolerance):
            if np.allclose(pd.DataFrame(self.trans_probs), pd.DataFrame(other.trans_probs), atol=self._tolerance):
                if np.allclose(pd.DataFrame(self.emit_probs), pd.DataFrame(other.emit_probs), atol=self._tolerance):
                    return True
        return False

class ProfileHMM(BaseHMM):
    """Main class for Profile HMM objects

    Class for holding Profile HMM parameters and to allow for implementation of functions associated with PHMMs

    Attributes:
        alphabet (str): The emissions used in the HMM (default: 'ACGT')
        hidden_states (list): The hidden states within the HMM (default: None)
        init_probs (dict of floats): β probabilities for initial steps (default: None)
        trans_probs (dict of dict of floats): Transition probabilities from one state to another given a state (default: None)
        emit_probs (dict of dict of floats): Emission probabilities of a letter given a state (default: None)
    """

    @classmethod
    def __dir__(cls):
        return cls.__all__

    def read_msa(self, file):
        """read file and return list of sequences"""

        msa = []  # list to store seqs
        with open(file, "r", encoding='utf-8') as infile:
            for line in infile:
                if not line.startswith('>'):
                    msa.append(line)
        
        return msa
        
    def column_classification(self, msa):
        """classify if msa columns are matches or insertions"""

        num_seqs = len(msa)

        # check if all sequences are the same length
        if len(set(len(s) for s in msa)) == 1:
            len_seq = len(msa[0])
        else:
            raise ValueError("Sequences must be the same length.")

        # Initialize a matrix to store 1 if residue is an Amino Acid and 0 if -
        AA_matrix = np.zeros((num_seqs, len_seq))

        for i, seq in enumerate(msa):
            for j, res in enumerate(seq):
                if res in self.alphabet:
                    AA_matrix[i, j] = 1
                else:
                    AA_matrix[i, j] = 0

        classifications = []
        match_counter = 0
        # Determine if col is a match or insertion
        for col_idx, col in enumerate(zip(*AA_matrix)):
            if sum(col) / num_seqs > 0.5:
                match_counter += 1
                classifications.append(
                    {"position": col_idx, "col_type": "match", "state": f"M{match_counter}"}
                )

            else:
                classifications.append(
                    {"position": col_idx, "col_type": "insertion", "state": f"I{col_idx}"}
                )

        # Define Profile Length
        L = match_counter

        return classifications, L


    def define_hiddenstates(self, L):
        """create hidden states"""

        # Begin and End states
        states = ["Begin", "End"]

        # Match states: M1 -> ML
        match_states = [f"M{i}" for i in range(1, L+1)]
        
        # Deletion states: D1 -> DL
        del_states = [f"D{i}" for i in range(1, L+1)]

        # Insertion states: I0 -> IL
        insert_states = [f"I{i}" for i in range(0, L+1)]

        # Combine all
        states.extend(match_states)
        states.extend(insert_states)
        states.extend(del_states)

        return states

    
    def build_trans_structure(self, L):
        """build transition probability structure for PHMM

        Args: 
            L (int): number of match states (L)

        Returns:
            trans_prob (dict of dict): trans prob with placeholders
        """
        self.trans_probs = {}

        # Begin state transitions
        self.trans_probs['Begin'] = {
            'M1': 1/3,
            'I0': 1/3,
            'D1': 1/3
        }

        # Match state transitions
        for i in range(1, L+1):
            if i < L:  # M1 -> ML-1
                self.trans_probs[f"M{i}"] = {
                    f"M{i+1}": 1/3,
                    f"I{i}": 1/3,
                    f"D{i+1}": 1/3
                }
            else:  # last match: ML
                self.trans_probs[f"M{L}"] = {
                    f"I{L}": 1/2,
                    "End": 1/2
                }

        # Insertion state transitions (can self-loop)
        for i in range(0, L+1):
            if i == 0:  # first insertion
                self.trans_probs["I0"] = {
                    "I0": 1/3,
                    "M1": 1/3,
                    "D1": 1/3
                }
            elif i < L:
                self.trans_probs[f"I{i}"] = {
                    f"I{i}": 1/3,
                    f"M{i+1}": 1/3,
                    f"D{i+1}": 1/3
                }
            else:  # last insertion
                self.trans_probs[f"I{L}"] = {
                    f"I{L}": 1/2,
                    "End": 1/2
                }

        # Deletion state transitions
        for i in range(1, L+1):
            if i < L:
                self.trans_probs[f"D{i}"] = {
                    f"M{i+1}": 1/3,
                    f"I{i}": 1/3,
                    f"D{i+1}": 1/3
                }
            else:
                self.trans_probs[f"D{L}"] = {
                    f"I{L}": 1/2,
                    "End": 1/2
                }
        
        # End state
        self.trans_probs["End"] = {}

        return self.trans_probs

    
    def labeled_path(self, seq, column_classification):
        """
        Label each position in a sequence with its corresponding state.

        Args: 
            seq (str): sequence from msa
            column_classification: list of dicts from step 1
        Return:
            path (list of tuples): [(state, emission)]
        """

        # Begin path
        path = [("Begin", None)]

        for i, res in enumerate(seq):
            col_info = column_classification[i]  #dictionary of position, type, state
            col_type = col_info["col_type"]
            col_state = col_info["state"]
            if col_type == "match":
                if res == "-":  # gap in match column = deletion
                    path.append((f"D{col_state[1:]}", None))
                else:  # res in match column = match
                    path.append((col_state, res))

            elif col_type == "insertion":
                if res != "-":
                    # res in insertion column = insertion
                    path.append((col_state, res))
                # skip if res is a gap in the insertion column
        
        # End
        path.append(("End", None))
        return path


    def estimate_emit_probs(self, msa, column_classification):
        """estimate emission probs from labeled sequences"""

        # initialize emit probs
        self.emit_probs = {}

        # count emissions for each state
        emission_counts = defaultdict(lambda: defaultdict(int))
        for seq in msa:
            path = self.labeled_path(seq, column_classification)
            for state, emission in path:
                if emission is not None:
                    emission_counts[state][emission] += 1

        possible_aa = len(self.alphabet)
        b = 1  # set pseudocount
        aa_total = sum(sum(inner_dict.values()) for inner_dict in emission_counts.values())  # total count within the entire dictionary 

        for state, counts in emission_counts.items():
            total_count = sum(counts.values())  # total count in each state
            self.emit_probs[state] = {}

            # insertion emission(a) = p(a)
            if state[0] == "I":
                for aa in self.alphabet:
                    aa_freq = counts.get(aa, 0)
                    prob = aa_freq/aa_total
                    self.emit_probs[state][aa] = prob
            else:
                # emission(a) = count (a) in state / (total residues aligned in state + 20b)
                for aa in self.alphabet:  # for each possible aa 
                    aa_freq = counts.get(aa, 0)  # get count for aa within state
                    prob = (aa_freq + b) / (total_count + possible_aa * b)  # calculate emit prob for aa
                    self.emit_probs[state][aa] = prob

        return self.emit_probs

    
    def estimate_trans_probs(self, msa, column_classification):
