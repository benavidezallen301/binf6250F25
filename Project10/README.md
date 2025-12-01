# Introduction
Implementing Baum Welch Algorithm 

# Pseudocode
Put pseudocode in this box:

## Initialize
Randomly assign values that add up to 1 for initial, trans, and emission probs

## Expectation and Maximization Steps
1. Run forward-backward algorithm on all sequences and store matrix and total probs for each of the sequences

2. Update probabilities for initial, trans, and emission probabilities with the right side of the functions
    * Iterate through sequences
        * Iterate through states
            * Iterate through each position 
                * Calculate initial and emission probs
        * Iterate through next states
            * Iterate through next positions
                * Calculate transition probs: 
                    sum(forward prob of the current position * transition prob of current state to next state * emission prob of the next emission at the next state * backward prob of the next position at the next state) for each position of each sequence

```{python}
intial_prob
trans_prob
emission_prob
total_prob = 0

for each sequence
    get fwd prob, fwd matrix, bwd prob, and bwd matrix
    update total_prob using the avg of the fwd and bwd probs 
    for each state
        for position and letter in the sequence:
            # update initial_prob: sum the forward*backward of the initial position
            if position is 0, update initial prob using the formula below:
                initial_prob[state] += forward[state][seq_i] * backward[state][seq_i]

            # update emission_prob: sum the forward*backward of every position in which the emission occurs
            ?for unique_emission in emissions:
                if emission == unique_emission:
                    emission_prob[state][emission] += forward[state][seq_i] * backward[state][seq_i]

        # update the trans_prob: sum(forward[i]*trans_prob[state][state]*emission_prob[next_state][next_i]*backward_prob[next_i])
        for next_state in states:
            for next_i in positions:
                trans_prob[state][next_state] += forward[seq_i]*trans_prob[state][state]*emission_prob[next_state][next_i]*backward_prob[next_i]
```

3. Scale and Normalize the updated probablities
    * Scale by dividing with the total forward/backward probability
        * handles underflow issues, so we do not need to do calculations in log space
    * Normalize by dividing the probability with the total initial/trans/emission probability for each state 
        * ensures that the probabilities add up to 1 

## Convergence:
Compare old model with new:
    * can use ==, close_to, etc. 
    * if the new model is not close enough to the old model, update old with new
    * else, break


    




```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
