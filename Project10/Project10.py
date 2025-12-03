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
        
        # Initialize: β_T(i) = 1 for all states
        backward_matrix[:, -1] = 1
        
        # Iterate backwards through time
        for j in range(len_obs - 2, -1, -1):  # Fixed indentation
            for i in range(self.len_states):  # Fixed indentation
                curr_state = self.states[i]
                prob = 0
                
                for next_i in range(self.len_states):  # Fixed indentation
                    next_state = self.states[next_i]
                    next_val = backward_matrix[next_i, j + 1]
                    next_sym = obs[j + 1]
                    prob += self._calc_prob(next_val, curr_state, next_state, next_sym)
                
                backward_matrix[i, j] = prob
        
        # Calculate probability of observation sequence
        accum = np.sum(
            [
                self.init_probs[self.states[i]]
                * self.emit_probs[self.states[i]][obs[0]]
                * backward_matrix[i, 0]  
                for i in range(self.len_states)
            ]
        )
        
        return backward_matrix, accum

    def exp_max(self, obs):
        """
        Expectation and Maximum Steps of Baum-Welch. We scaled and normalized our calculations to prevent numerical underflow instead of working in Log-Phase. 
        Returns:
            new_i (dict): New Initial Probabilties
            new_t (dict of dict): New Transition Probabilities
            new_e (dict of dict): New Emission Probabilities
        """

        total_prob = 0  # initialize total prob
        poss_i, poss_t, poss_e = self._copy_reset()  # initialize models to store possible initial, transition, and emission values

        for seq in obs:
            fwd_matrix, fwd_prob = self.forward(seq)
            bwd_matrix, bwd_prob = self.backward(seq)

            # update total_prob throughout
            total_prob += (fwd_prob+bwd_prob)/2

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
    


    def converge(self, new_i, new_t, new_e, old_i, old_t, old_e):
        """
        Checks if the new model is close to the old model
        Args:
            new_i (dict): New Initial Probabilites
            new_t (dict of dict): New Transition Probabilities
            new_e (dict of dict): New Emission Probabilities
            old_i (dict): Last Initial Probabilities
            old_t (dict of dict): Last Transition Probabilties
            old_e (dict of dict): Last Emission Probabilities
        """
        # compare each individual component of the model
        init = self._comp_models(new_i, old_i)
        trans = self._comp_models(new_t, old_t)
        emit = self._comp_models(new_e, old_e)

        # if all components are close, then return true, else false
        if init and trans and emit:
            return True
        else:
            return False

    def baum_welch(self, obs, max_iter=1000):
        """
        Baum-welch algorithm 
        Args:
            obs (list): list of sequences
            max_iter (int): max number of iterations
        Return:
            Initial Probabilities
            Transition Probabilities
            Emission Probabilities
        """    
        for i in range(max_iter):
            # save old param for comparison
            old_i = self.init_probs.copy()
            old_t = deepcopy(self.trans_probs)
            old_e = deepcopy(self.emit_probs)

            # get new model
            new_i, new_t, new_e = self.exp_max(obs)

            # check if models are close
            # if true break, else update 
            if self.converge(new_i, new_t, new_e, old_i, old_t, old_e):
                print(f"Converge after {i} iterations")
                break
            else:
                self.init_probs = new_i
                self.trans_probs = new_t
                self.emit_probs = new_e

        return self.init_probs, self.trans_probs, self.emit_probs




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
        """
        Helper function to create new initial, transition, and emission probability holders
        """
        next_i_probs = self.init_probs.copy()
        next_t_probs = deepcopy(self.trans_probs)
        next_e_probs = deepcopy(self.emit_probs)

                # reset model for update
        for state in self.states:
            next_i_probs[state] = 0
            for emit in self.emissions:
                next_e_probs[state][emit] = 0
            
            for next_state in self.states:
                next_t_probs[state][next_state] = 0

        return next_i_probs, next_t_probs, next_e_probs

    def _comp_models(self, new_model, old_model):
        """
        helper function to compare the new and old models

        Args:
            new_model (dict): new probability model for comparison
            old_model (dict): old probability model for comparison

        Return:
            True/False: will be used to tell convergence model if the models are close enough or not
        """

        new_val = new_model.values()
        old_val = old_model.values()

        # Convert to lists
        new_list = list(new_val)
        old_list = list(old_val)

        # Check if they're dictionaries (nested structure)
        if isinstance(new_list[0], dict):
            # For nested dictionaries (like transition/emission probs) flatten the nested values
            new_flat = [v for d in new_list for v in d.values()]
            old_flat = [v for d in old_list for v in d.values()]
            return np.allclose(new_flat, old_flat)
        else:
            # For simple values (like initial probs)
            return np.allclose(new_list, old_list)
 
 
   
if __name__ == "__main__":
    obs = ["GGCACTGAA", "ATGCAATGC", "AATGCCTGA"]
    seq = "GGCACTGAA"
    hmm = HMM(states= ["H","L"], seed = 42)
    init, trans, emit = hmm.baum_welch(obs)
    print(f"Initial Probabilities: {init}")
    print(f"Transition probabilites: {trans}")
    print(f"Emission Probabilites: {emit}")

