

# BINF6250 - Project 11: Profile HMM
# Introduction

# Pseudocode

## 1. MSA Parsing and Column Classification
```
Read MSA FASTA files and store sequences as a list called msa (will require parsing for the lines that do not start with >)

Initialize an AA_matrix to store 1 or 0 if the residue in the sequence is an amino acid
For each seq in sequences:
    For each residue in the seq:
        If the residue is a letter:
            Add 1 to the AA_matrix at that position ([seq_i, res_i])

Initialize dictionary to store column classification ({position: Mi+1 or Ii})
For each column of the AA_matrix:
    If the sum(column)/total number of sequences is >= 0.5:
        It is a match and add Mi+1 to the list of column classification 
    else:
        It is an insertion and add Ii to the list of column classification

Return a dictionary of column classifications, indicating if the position is a match or an insertion
{position: classification} or dict of dict {col_indx: , state: }
```

## 2. Profile HMM Topology Construction
```
Define hidden states: 
    hiddenstates = ['Begin', 'End', 
                    'M1',..., 'ML',
                    'I0', ..., 'IL', 
                    'D1', ..., 'DL']
    (L is the profile length/length of matches)      

Define Allowed Transitions:
    Iterate through the hiddenstates and create a dict of dict with each hidden state to the following possible hidden state with placeholder probabilities        
```

## 3. Parameter Estimation from Labeled Columns
```
    #Labeled paths
    If column is determined to be Match:
        rename the bases that were match as M_i (i being the position)
        rename the gaps in that same column as deletions

    #Emission Probabilities
    For every state M_i:
        total_count -> number of residues in the column
        residue_frequency -> number of times the specific type of residue we are evaluating appeared in the column
        b <- the pseudocount equal to 1
        possible_amino_acids <- 20
        formula -> (residue_frequency + b ) / (total_count + possible_amino_acids*b) # gives us prob

    If intersion state:
        We use a "pre-calculated" frequency. We can simply use the probability of an amino acid occuring across
        all sequences. Example: if amino acid "L" occurs 25 times and there are 100 amino acids then prob = 0.25

    #Transition Probabilities
    create dictionary of dictionaries and create keys for states "M","I","D".
    Keep record in that dictionary how many times a state transitions to another specific state.
    Example  {
        M:{I:4,D:2,M:10}
        I:{M:12,I:1,D:3}
    }
```

## 4. Integration with `HMM.py`
```
Class ProfileHMM(BaseHMM):
    def hiddenstate:
        Determine whether this state is match or insertion (using the 50% threshold)
    def init_probs:
        P(Begin) = 1
    def trans_probs:
        calculates probs from the dictionary of dictionary keeping tally of transitions from one state to another
    def_emit_probs:
        if column is "Match" then use the match calculation formula
        if column is "Insertion" then use the pre-calculated probability
        

```





# Successes

# Struggles
* We struggled to understand the algorithm and implement it into existing hmm file

# Personal Reflections
## Group Leader (Allen Benavidez)
## Other member (Zoe Chow)

# Generative AI Appendix


