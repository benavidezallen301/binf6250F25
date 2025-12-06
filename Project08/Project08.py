import numpy as np
import math


class HMM:
    """
    Hidden Markov Model
    Attributes
    ----------
    init_probs : dict
        Log initial state probabilities.
    trans_probs : dict of dict
        Log transition probabilities.
    emit_probs : dict of dict
        Log emission probabilities.
    states : list
        Ordered list of HMM states.
    """

    def __init__(self, init_probs, trans_probs, emit_probs):
        """
        Log probabilities for the initial probs, transition probs, and emission probs.
        Args:
            init_probs (dict): Initial probabilities of each state
            trans_probs (dict of dict): Transition probabilities of each state
            emit_probs (dict of dict): Emission probabilities of each state for observed symbols
        """
        self.states = list(init_probs.keys())
        self.init_probs = {state: math.log(prob) for state, prob in init_probs.items()}
        self.trans_probs = {
            state: {
                transition: math.log(prob)
                for transition, prob in trans_probs[state].items()
            }
            for state in trans_probs
        }
        self.emit_probs = {
            state: {sym: math.log(prob) for sym, prob in emit_probs[state].items()}
            for state in emit_probs
        }

    def viterbi(self, obs):
        """ """
        len_states = len(self.states)
        len_obs = len(obs)

        # initialize matrix with -inf since working in log-space
        v_matrix = np.full((len_states, len_obs), -math.inf)
        # initialize traceback matrix
        traceback = np.zeros((len_states, len_obs), dtype=int)

        # handle first col
        for i, state in enumerate(self.states):
            v_matrix[i, 0] = self.init_probs[state] + self.emit_probs[state][obs[0]]

        # fill in the rest of the matrix
        for j in range(1, len_obs):  # for each emit in the obs
            # iterate through the states
            for i, state in enumerate(self.states):
                prob_candidates = []
                # calculate prob given the previous state
                for last_i, prev_state in enumerate(self.states):
                    prev_prob = v_matrix[last_i][j - 1]
                    prob = (
                        prev_prob
                        + self.trans_probs[prev_state][state]
                        + self.emit_probs[state][obs[j]]
                    )
                    prob_candidates.append(prob)

                # add greatest prob for current state and emit to matrix
                best_prev = np.argmax(prob_candidates)
                v_matrix[i][j] = prob_candidates[best_prev]
                traceback[i][j] = best_prev

        # termination
        last_state = np.argmax(v_matrix[:, -1])

        # traceback
        path = [last_state]
        for j in range(len_obs - 1, 0, -1):
            path.append(traceback[path[-1]][j])

        path = path[::-1]  # reverse to get left → right

        # convert indices to label names
        return "-".join(self.states[i] for i in path)


def main():
    # Example observation sequence
    obs = "GGCACTGAA"

    # Example initial probabilities (probability of starting in each state)
    init_probs = {"I": 0.2, "G": 0.8}

    # Example transition probabilities (probability of moving from one state to another)
    trans_probs = {"I": {"I": 0.7, "G": 0.3}, "G": {"I": 0.1, "G": 0.9}}

    # Example emission probabilities (probability of observing a symbol in a given state)
    emit_probs = {
        "I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
        "G": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3},
    }

    hmm = HMM(init_probs, trans_probs, emit_probs)
    print(f"Optimal Path: {hmm.viterbi(obs)}")


if __name__ == "__main__":
    main()
