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

    def __init__(self,states, emissions = 'ACGT', init_probs = None, trans_probs = None, emit_probs = None, seed = 42): # precision, tolerance):

        if states is None:
            raise ValueError("States cannot be empty")
        self.states = states

        self.emissions = emissions

        self.init_probs = init_probs
        self.trans_probs = trans_probs
        self.emit_probs = emit_probs
        self._initialize_probs(seed)


    def _initialize_probs(self, seed):
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
            self.trans_probs = dict()
            for state in self.states:
                t_probs = np.random.dirichlet(np.ones(len(self.states)))
                self.trans_probs[state] = {s2: p for s2, p in zip(self.states, t_probs)}
        
        #Emission Probs
        if self.emit_probs is None: 
            self.emit_probs = dict()
            for state in self.states:
                e_probs = np.random.dirichlet(np.ones(len(self.emissions)))
                self.emit_probs[state] = {e: p for e, p in zip(self.emissions,e_probs)}
    
    def forward(self,obs):
        """
        Create the foward algorithm
        """
        len_states = len(self.states)
        len_obs = len(obs)

        forward_matrix = np.zeros((len_states, len_obs))

        for i in range(len_states):
            state = self.states[i]
            first_obs = obs[0]
            forward_matrix[i,0] = (
                self.init_probs[state] *
                self.emit_probs[state][first_obs]
            )
        
        #To fill the matrix
        for j in range(1, len_obs):
            next_obs = obs[j]
            for i in range(len_states):
                curr_state = self.states[i]
                prob = 0
                for k in range(len_states):
                    prev_state = self.states[k]
                    prev_val = forward_matrix[k, j -1]
                    trans = self.trans_probs[prev_state][curr_state]
                    emit = self.emit_probs[curr_state][next_obs]
                    prob += prev_val * trans * emit
                forward_matrix[i,j] = prob
        total_forward = np.sum(forward_matrix[:, -1])
        return forward_matrix, total_forward


    
    def backward(self, obs):
        """
        Create the backward algorithm
        """
        len_states = len(self.states)
        len_obs = len(obs)

        backward_matrix = np.zeros((len_states, len_obs))

        backward_matrix[:, -1] = 1

        for j in range(len_obs -2, -1, -1):
            next_sym = obs[j + 1]

            for i in range(len_states):
                curr_state = self.states[i]
                prob = 0

                for k in range(len_states):
                    next_state = self.states[k]
                    next_val = backward_matrix[k,j + 1]
                    trans = self.trans_probs[curr_state][next_state]
                    emit = self.emit_probs[next_state][next_sym]
                    prob += next_val * trans * emit
                
                backward_matrix[i,j] = prob
            
            accum = 0
            first_sym = obs[0]
            for i in range(len_states):
                init = self.init_probs[self.states[i]]
                emit = self.emit_probs[self.states[i]][first_sym]
                back = backward_matrix[i, 0]
                accum += init * emit * back
        return backward_matrix, accum
    
    def forward_backward(self, obs):
        len_states = len(self.states)
        len_obs = len(obs)

        PMP = np.zeros((len_states, len_obs))

        forward_matrix, total_forward = self.forward(obs)
        backward_matrix, total_backward = self.backward(obs)

        for i in range(len_states):
            for j in range(len_obs):
                PMP[i,j] = self.PMP_calc(
                    i,j,
                    forward_matrix, total_forward,
                    backward_matrix, total_backward
                )
        path = self._posterior_decoding(PMP)

        return path
    

    def _PMP_calc(
        self, i, j, forward_matrix, total_forward, backward_matrix, total_backward
    ):
        """
        Calculate the posterior marginal probability of each state and symbol of the observation.

        Arg:
            i (int): current state position
            j (int): current symbol (observation position)
            forward_matrix (array): probability matrix of the observation based on the Forward Algorithm
            total_forward (float): total accumulated probability for the forward matrix (sum of last column)
            backward_matrix (array): probability matrix of the observation based on the Backward Algorithm
            total_backward (float): total accumulated probability for the backward matrix (sum of last column)
        Returns:
            PMP (float): posterior marginal probability for the current position
        """

        prob = (total_forward + total_backward) / 2

        PMP = forward_matrix[i, j] * backward_matrix[i, j] / prob

        return PMP

    # Forward-Backward function uses _posterior_decoding() to determint the most probable state at each position
    def _posterior_decoding(self, PMP_matrix):
        """
        Perform Posterior Decoding to find the most probable state at each position

        Arg:
            PMP_matrix (array): matrices of posterior marginal probability
        Returns:
            path (str):
        """

        # find index of best state in each position
        best_states = list(np.argmax(PMP_matrix, axis=0))

        # generate path from best_states
        path = "-".join(self.states[i] for i in best_states)

        return path


    
#class HMM(BaseHMM):
    """ 
    computes the Baum-Welch algorithm using the BaseHMM attributes
    """
    
