import numpy as np
from copy import deepcopy


class HMM:
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
        self.len_states = len(states)

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
        len_obs = len(obs)

        forward_matrix = np.zeros((self.len_states, len_obs))

        for i in range(self.len_states):
            state = self.states[i]
            first_obs = obs[0]
            forward_matrix[i,0] = (
                self.init_probs[state] *
                self.emit_probs[state][first_obs]
            )
        
        #To fill the matrix
        for j in range(1, len_obs):
            next_sym = obs[j]
            for i in range(self.len_states):
                curr_state = self.states[i]
                prob = 0
                for last_i in range(self.len_states):
                    prev_state = self.states[last_i]
                    prev_val = forward_matrix[last_i, j-1]
                    prob += self._calc_prob(prev_val, prev_state, curr_state, next_sym)

                forward_matrix[i,j] = prob

        total_forward = np.sum(forward_matrix[:, -1])
        return forward_matrix, total_forward


    
    def backward(self, obs):
        """
        Create the backward algorithm
        """
        len_obs = len(obs)
        backward_matrix = np.zeros((self.len_states, len_obs))

        backward_matrix[:, -1] = 1

        for j in range(len_obs -2, -1, -1):
            next_sym = obs[j + 1]

            for i in range(self.len_states):
                curr_state = self.states[i]
                prob = 0

                for next_i in range(self.len_states):
                    next_state = self.states[next_i]
                    next_val = backward_matrix[next_i, j + 1]
                    prob += self._calc_prob(next_val, curr_state, next_state, next_sym)
                
                backward_matrix[i,j] = prob
            
        accum = np.sum(
            [
                self.init_probs[self.states[i]] * self.emit_probs[self.states[i]][obs[0]] * self.bwd_matrix[i, 0]
                for i in range(self.len_states)
            ]
        )

        return backward_matrix, accum

    def exp_max(self, obs):
        """
        Calculate and update models 
        """

        total_prob = 0  # initialize total prob
        poss_i, poss_t, poss_e = self._copy_reset()  # initialize models to store possible initial, transition, and emission values

        for seq in obs:
            fwd_prob, fwd_matrix = self.forward(seq, self.states)
            bwd_prob, bwd_matrix = self.backward(seq, self.states)

            # update total_prob throughout
            total_prob += (fwd_prob + bwd_prob)/2

            for state_i, state in enumerate(self.states):
                for seq_i, letter in enumerate(seq):

                    # calculate new prob for initial and emission models
                    new_prob = fwd_matrix[state_i][seq_i] * bwd_matrix[state_i][seq_i]

                    # update initial probabilities
                    if seq_i == 0:
                        poss_i[state] += new_prob

                    # update emission probabilities
                    poss_e[state][letter] += new_prob

            # calculate and update transition probabiltiies
            for next_state_i, next_state in enumerate(self.states):
                for seq_i in range(len(seq)-1):  # index 0 to last of the sequence 
                    poss_t[state][next_state] += (
                        fwd_matrix[state_i][seq_i]
                        * self.trans_probs[state][next_state]
                        * self.emit_probs[next_state][seq[seq_i+1]]
                        * bwd_matrix[next_state_i][seq_i+1]
                    )
        
        # scale
        scaled_i = {key: value/total_prob for key, value in poss_i.items()}
        scaled_t = {
            key1: {key2: value / total_prob for key2, value in inner_t.items()}
            for key1, inner_t in poss_t.items()
        }
        scaled_e = {
            key1: {key2: value / total_prob for key2, value in inner_e.items()}
            for key1, inner_e in poss_e.items()
        }

        # normalize

        new_i = {key: value/sum(scaled_i.values()) for key, value in scaled_i.items()}
        new_t = {
            key1: {key2: value/sum(inner_t.values()) for key2, value in inner_t.items()}
            for key1, inner_t in scaled_t.items()
        }
        new_e = {
            key1: {key2: value/sum(inner_e.values()) for key2, value in inner_e.items()}
            for key1, inner_e in scaled_e.items()
        }

        return new_i, new_t, new_e

    def converge():
        """
        """


    def _calc_prob(self, prob, from_state, to_state, emit):
        """
        calculate probabilities for forward and backward algorithms

        Args:
            prob (float): previous probability/next probability
            from_state (str): where the calculation is coming from
            to_state (str): next state
            emit (str): emission from the sequence

        Return:
            prob (float): forward/backward probability at that position
        """
        prob = prob * self.trans_probs[from_state][to_state] * self.emit_probs[to_state][emit]
        return prob

    def _copy_reset(self):
        next_i_probs = self.init_probs.copy()
        next_t_probs = self.trans_probs.copy()
        next_e_probs = self.emit_probs.copy()

                # reset model for update
        for state in states:
            next_i_probs[state] = 0
            for emit in self.emissions:
                next_e_probs[state][emit] = 0
            
            for next_state in states:
                next_t_probs[state][next_state] = 0

        return next_i_probs, next_t_probs, next_e_probs

    def _comp_models(self, new_i, new_t, new_e):
        """
        helper function to compare the new and old models

        Args:
            new_i (dict): new initial probability model for comparison
            new_t (dict of dict): new transition probability model for comparison
            new_e (dict of dict): new emission probability model for comparison

        Return:
            True/False: will be used to tell convergence model if the models are close enough or not
        """


    
   
if __name__ == "__main__":

    # 1. Define a simple list of states
    states = ["H", "L"]   # High / Low GC, or any states you want

    # 2. Create an HMM with random parameters (init_probs=None etc.)
    model = HMM(states=states, seed=123)

    # 3. Print the randomly initialized model
    print("\n=== INITIAL PROBABILITIES ===")
    print(model.init_probs)

    print("\n=== TRANSITION PROBABILITIES ===")
    for s in model.trans_probs:
        print(s, model.trans_probs[s])

    print("\n=== EMISSION PROBABILITIES ===")
    for s in model.emit_probs:
        print(s, model.emit_probs[s])

    # 4. Create a random test observation sequence
    obs = "ACGTACGTAC"

    print("\n=== FORWARD RESULTS ===")
    fwd, fprob = model.forward(obs)
    print(fwd)
    print("Forward total prob =", fprob)

    print("\n=== BACKWARD RESULTS ===")
    bwd, bprob = model.backward(obs)
    print(bwd)
    print("Backward total prob =", bprob)

    print("\n=== FORWARD-BACKWARD (decoded path) ===")
    path = model.forward_backward(obs)
    print("Decoded path:", path)
