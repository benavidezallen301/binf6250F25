# Introduction
Implementing Baum Welch Algorithm 

# Pseudocode
Put pseudocode in this box:

```

initialization
    set up HMM model 
    set up initial states 
    set up convergence criteria (iterations = 100) or threshold (difference)
    set up pseudocounts
functions we will need: convergence

Expectation 
    run forward-backward function (return posterior probabilities and recorded path)
    Using decoded path from forward-backward, calculate expected counts for transition and emissions
functions we will need: forward, backward, forward-backward, expected counts

Maximization
    calculate probabilites with our expected counts
    update model parameters based on calculated expected counts
    (Normalize to ensure valid probability distributions)
    (Scale values to prevent numerical underflow)
functions we will need: initial probs, emission probs, transition probs, update model

Iteration and Convergence
    Have model converge for one sequence (then we will make it work for multiple)
    


    




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
