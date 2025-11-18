import numpy as np


class HMM:
    """
    Hidden Markov Model
    Attributes
    ----------
    init_probs : dict
        Initial state probabilities.
    trans_probs : dict of dict
        Transition probabilities.
    emit_probs : dict of dict
        Emission probabilities.
    states : list
        Ordered list of HMM states.
    """

    def __init__(self, init_probs, trans_probs, emit_probs):
        """
        HMM characteristics for the initial probs, transition probs, and emission probs.

        Args:
            init_probs (dict): Initial probabilities of each state
            trans_probs (dict of dict): Transition probabilities of each state
            emit_probs (dict of dict): Emission probabilities of each state for observed symbols
        """
        self.states = list(init_probs.keys())
        self.init_probs = init_probs
        self.trans_probs = trans_probs
        self.emit_probs = emit_probs

    # Public Functions: Forward, Backward, Forward-Backward Algorithms
    def forward(self, obs):
        """
        Perform the Forward Algorithm and calculate the probabiltiy matrix and total accumulated probability for the observation given our HMM.

        Args:
            obs (str): observation
        Return:
            forward_matrix (array): matrices with the total probability at each given position
            accum_prob (float): total accumulated probability for the forward matrix (sum of last column)
        """
        # initialize forward matrix
        len_states = len(self.states)
        len_obs = len(obs)
        forward_matrix = np.zeros((len_states, len_obs))

        # initialize first column
        for i in range(len_states):
            state = self.states[i]
            forward_matrix[i, 0] = (
                self.init_probs[state] * self.emit_probs[state][obs[0]]
            )

        # fill the rest of the matrix
        for j in range(1, len_obs):
            for i in range(len_states):
                current_state = self.states[i]
                prob = 0
                # sum over all previous states
                for last_i in range(len_states):
                    prev_state = self.states[last_i]
                    prev_prob = forward_matrix[last_i][j - 1]
                    prob += (
                        prev_prob
                        * self.trans_probs[prev_state][current_state]
                        * self.emit_probs[current_state][obs[j]]
                    )

                forward_matrix[i, j] = prob

        # determine total accumulated probability (sum of both states for last col)
        accum_prob = np.sum(forward_matrix[:, -1])

        return forward_matrix, accum_prob

    def backward(self, obs):
        """
        Perform the Backward Algorithm and calculate the probabiltiy matrix and total accumulated probability for the observation given our HMM.

        Args:
            obs (str): observation
        Return:
            backward_matrix (array): matrices with the total probability at each given position
            accum_prob (float): total accumulated probability for the forward matrix (sum of last column)
        """
        # initialize backward matrix
        len_states = len(self.states)
        len_obs = len(obs)
        backward_matrix = np.zeros((len_states, len_obs))

        # initialize last col
        backward_matrix[:, -1] = 1

        # loop through each position of the matrix backwardsand get total probability
        # range(start = len-2 to exclude last col, stop = -1 to include index 0, step = -1 to move backwards)
        for j in range(len_obs - 2, -1, -1):
            for i in range(len_states):
                current_state = self.states[i]
                prob = 0  # initialize prob of each position

                # prob of position is the sum of all next states
                for next_i in range(len_states):
                    next_state = self.states[next_i]
                    next_obs = obs[j + 1]
                    next_prob = backward_matrix[next_i, j + 1]
                    prob += (
                        next_prob
                        * self.trans_probs[current_state][next_state]
                        * self.emit_probs[next_state][next_obs]
                    )

                backward_matrix[i, j] = prob

        # determine total accumulated probability
        # accumulated prob = sum of (initial state * prob of the accumulated prob at the state * prob of emission at the state) in the first col
        accum_prob = np.sum(
            [
                self.init_probs[self.states[i]]
                * self.emit_probs[self.states[i]][obs[0]]
                * backward_matrix[i, 0]
                for i in range(len_states)
            ]
        )

        return backward_matrix, accum_prob

    def forward_backward(self, obs):
        """
        Perform the Forward-Backward Algorithm. Calculate the probability of a position in the observation being assigned a particular hidden state using Posterior Marginal Probability (PMP), and use Posterior Decoding to determine path.

        Args:
            obs (str): observations
        Returns:
            path (str): decoded path
        """
        # initialize PMP matrix
        rows = len(self.states)
        columns = len(obs)
        PMP_matrix = np.zeros((rows, columns))

        # Get forward matrix, total accumulated forward probability
        forward_matrix, total_forward = self.forward(obs)

        # Get backward matrix, total accumulated backward probability
        backward_matrix, total_backward = self.backward(obs)

        print(f"total forward: {total_forward} \ntotal backward: {total_backward}")

        print(f"forward_matrix: {forward_matrix} \nbackward_matrix: {backward_matrix}")

        diff = total_forward - total_backward
        print(f"diff: {diff}")

        # do we want to create functions that calculates PMP and performs traceback? Similar to the max_probs and traceback functions from viterbi.
        # Calculate PMP for each position of the PMP matrix
        for i in range(rows):
            for j in range(columns):
                PMP_matrix[i, j] = self._PMP_calc(
                    i, j, forward_matrix, total_forward, backward_matrix, total_backward
                )

        # Select path using traceback
        path = self._posterior_decoding(PMP_matrix)

        return path

    # Helper Functions

    # Forward-Backward function uses _PMP_calc() to calculate the posterior marginal probability of each position
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


def main():
    # Example observation sequence
    obs = "ATGCAA"

    # Example initial probabilities (probability of starting in each state: E := Exon, I := Intron)
    init_probs = {"E": 0.6, "I": 0.4}

    # Example transition probabilities (probability of moving from one state to another)
    trans_probs = {"E": {"E": 0.8, "I": 0.2}, "I": {"E": 0.3, "I": 0.7}}

    # Example emission probabilities (probability of observing a symbol in a given state)
    emit_probs = {
        "E": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3},
        "I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
    }

    hmm = HMM(init_probs, trans_probs, emit_probs)
    print(f"Path: {hmm.forward_backward(obs)}")


if __name__ == "__main__":
    main()
