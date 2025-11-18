# Introduction
Implementing forward, backward and forward-backword algorithm

# Pseudocode
## Class Attributes
```
init_probs : dict
    Initial state probabilities.
trans_probs : dict of dict
    Transition probabilities.
emit_probs : dict of dict
    Emission probabilities.
states : list
    Ordered list of HMM states.

```
## Main Functions:
### Forward Function
```
Args: observation

1. initialize forward matrix (number of states X length of obs)
2. for each row and column of the matrix, call on probability function
    add probability to probability matrix
3. determine total accumulated probability of the matrix

Return: forward probability matrix, total accumulated probabiltiy
```
$$\text{prob} = \sum \text{(probability of the prev position * transition probability from the prev to the current state * emission probability of the current position)}$$

### Backward Function
```
Args: observation

1. initialize backward matrix (number of states X length of obs)
2. set initial symbol probabiltiy = 1
3. for each row and column of the matrix in reverse, calculate the probability and add to probability matrix
4. determine total accumulated probability of the matrix

Return: backward probability matrix, total accumulated probability
```
$$\text{prob} = \sum{{\text{probability of next position * transition probability of current state to next state * emission probability of the next position}}}$$

### Forward-Backward Function
```
1. initialize matrix for PMP (number of states X length of obs)

2. Get foward matrix, total forward prob, backward matrix, total backward prob by calling the forward and backward functions.
    forward_matrix = first return of forward (index 0)
    total_forward = second return of forward function (index 1)
    backward_matrix = first return of backward function (index 0)
    total_backward = second return of backward function (index 1)
    
3. for each position of the PMP matrix, calculate the posterior marginal probability (call on _PMP_calc())

4. create paths by choosing greatest state for each position (call on _posterior_decoding())

Return: path of best states
```

## Helper Functions

## For Foward-Backward Function
```
_PMP_calc():
Args:
    i (int): current state position
    j (int): current symbol (observation position)
    forward_matrix (array): probability matrix of the observation based on the Forward Algorithm
    total_forward (float): total accumulated probability for the forward matrix (sum of last column)
    backward_matrix (array): probability matrix of the observation based on the Backward Algorithm
    total_backward (float): total accumulated probability for the backward matrix (sum of last column)
    
1. prob = average of the total forward and total backward probabilities (they should be similar so we can use either one for the calculation, but average could reduce rounding errors)
2. PMP = (forward probability in state i at position j * backward probability in state i at position j) / total probability

Return: PMP (posterior marginal probability)
```

```
_posterior_decoding():
Arg:
    PMP_matrix (array): matrices of posterior marginal probability

1. find the index of the best states for each column of the PMP matrix
2. use the index to access the states and produce a path of the best states

Return: path of best states
```



# Successes
We were able to understand what was needed for the algorithm very quickly. We also were able to meet up and work on the project together several times.

# Struggles
* understanding how posterior marginal probability and posterior decoding worked

# Personal Reflections
## Group Leader- Allen
I felt that this project was much smoother than some of the other projects. The alogrithms were straightforward to understand however we did have a bit of trouble when completing the forward-backward algorithm. However we later figured out the issue and got it to work. Overall, this went well especially since we had a few long sessions where we were able to work on this synchronously.

## Other member - Zoe
This project was fairly straightforward to implement, as the underlying theory closely follows the Viterbi Algorithm. We used the Viterbi algorithm as a template for our code and adapted it accordingly. One challenge arose when calculating the posterior marginal probabilities is that we initially forgot that the total accumulated forward and backward probabilities should be nearly identical. Once we understood this, it was a simple fix in our code. Additionally, we considered how posterior decoding works, noting that it selects the state with the highest posterior probability at each position. We realized that this approach could lead to issues when more than two states are available, as it may produce impossible paths. Despite these challenges, I believe we were able to implement the algorithm correctly and effectively.

# Generative AI Appendix
