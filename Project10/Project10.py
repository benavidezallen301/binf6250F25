import numpy as np
from copy import deepcopy


class BaseHMM:
    """
    Base class for Hidden Markov Model objects
    Attributes
    ----------
    emissions : str
        The emissions used in the HMM (default: 'ACGT')
    states : list
        Ordered list of HMM states
    init_probs : dict
        Initial state probabilities
    trans_probs : dict of dict
        Transition probabilities
    emit_probs : dict of dict
        Emission probabilities
    seed : int
        Number to set seed to control randomness
    precision : int
        Number for floating point precision
    tolerance : float
        Acceptable range of variation 
    """

    def __init__(self, emissions = 'ACGT', states, init_probs = None, trans_probs = None, emit_probs = None, seed): # precision, tolerance):
        if states is None:
            raise ValueError("States cannot be empty")
        self.states = states

        self.emissions = emissions

        self.init_probs = init_probs
        self.trans_probs = trans_probs
        self.emit_probs = emit_probs

        self._initialize_model(seed)

    def _initialize_model(self, seed):
        """
        Initialize HMM if probability matrices are not provided.

        Args:
            seed (int): random seed for numpy
        """
        np.random.seed(seed)

        # Initial Probs
        if self.init_probs is None:
            i_probs = np.random.dirichlet(np.ones(len(self.states)))

            self.init_probs = {state: prob for state, prob in zip(self.states, i_probs)}

        # Transition Probs
        if self.trans_probs is None:
            


    
class HMM(BaseHMM):
    """ 
    """
    