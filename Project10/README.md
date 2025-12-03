# BINF6250 - Baum-Welch Algorithm
## Allen Benavidez, Zoe Chow

# Introduction
Implementing Baum Welch Algorithm includes 4 key steps: Initialization, Expectation, Maximization, and Iteration/Convergence. 

In our version, we chose to scale and normalize instead of working in log-phase. 

# Pseudocode
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



# Successes
The coding portion wasn’t too difficult once we worked out the algorithm and created a pseudocode. Getting started was a bit challenging, but breaking the problem into smaller parts and tackling them individually allowed us to focus on specific aspects of the algorithm and ultimately complete it as a whole.

# Struggles
* We struggled to understand how the formulas worked for baum-welch at the beginning, but after talking it out with Marcus, we were able to have a better grasp on what to do/how to implement them.


# Personal Reflections
## Group Leader
I found this project to be somewhat difficult since the baum-welch algorithm was not clear to me at first. Other aspects felt familiar so that helped me to not feel totally lost. Zoe and I took our time with this project and tackled it one piece at a time and met up several times to go over parts of the code. Overall, I am happy with where we got with our algorithm even though there are areas of improvment.

## Other member - Zoe
The formulas of this algorithm were a bit confusing to me at first, but after doing additional research and talking it out with Marcus, I was able to understand how to implement them. Allen and I broke down the code and split up the work, which allowed me to give my full attention to specific aspects of the algorithm. It was also easier to understand and explain what we did when we came back to discuss our work. This algorithm is not perfect, but I think we got pretty far. I'm still not 100% certain that I implemented the formulas correctly because the results looked a bit strange as it continued to iterate and converge, but the probabilities still add up to 1 within the dictionaries and the scaling should've handled any numerical underflow issues. 

# Generative AI Appendix
[Understanding the Formulas](https://claude.ai/chat/0df910f5-cc4d-4c8f-b900-362a9f8e1b07)
