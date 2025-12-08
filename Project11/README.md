

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
```

## 4. Integration with `HMM.py`
```
Class ProfileHMM(BaseHMM):
    def hiddenstate:
    def init_probs:
    def trans_probs
    def_emit_probs

```





# Successes

# Struggles
* We struggled to understand the algorithm and implement it into existing hmm file

# Personal Reflections
## Group Leader (Allen Benavidez)
## Other member (Zoe Chow)

# Generative AI Appendix


