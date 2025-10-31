# BINF6250 Project07: Burrows-Wheeler Transformation
# Introduction
The Burrows-Wheeler Transform (BWT) is a powerful algorithm used in data compression and bioinformatics. In this project, we will use BWT to compress and revert a string. This works by sorting all possible cyclic rotations of a string lexicographically and extracting the last column of the sorted matrix. 

# Pseudocode
## Burrows-Wheeler Transform
```
FUNCTION suffix_array:
  takes input string and returns list of integers representing the starting positions of the lexicographically sorted suffixes
  1. take input string
  2. create BWT matrix
  3. sort BWT matrix lexicographically
      numpy to rotate/scramble rows?
  4. Return list of integers of sorted starting positions and sorted matrix
  
  
FUNCTION BWT_from_suffix_array:
  calculates BWT from a suffix array. Uses suffix array to identify the character that precedes each suffix in the sorted order. 
  takes input string and suffix positions and returns BWT of the input string
  1. takes input string and suffix positions
  2. iterates through suffix positions to find bwt string
  3. returns bwt string (last column of BWT)
```

## Inverting Burrows-Wheeler Transform
```
FUNCTION cal_count:
  takes input string and returns a dictionary that indicates the count of characters lexicographically smaller than it
  Keys: unique letters
  Value: count of characters lexicographically smaller than it
  1. call Counter to count each character
  2. create separate dictionary that iterates through items and adds up lexicographically smaller characters


FUNCTION cal_occur: 
  calculate occurrence of each unique character within the bwt_string
  takes bwt_string and returns dictionary of list with occurence counts
  Ex. cal_occur('annb$aa') -> 
        {'$': [0, 0, 0, 0, 1, 1, 1], 'a': [0, 1, 1, 1, 1, 2, 3], 'b': [0, 0, 0, 1, 1, 1, 1], 'n': [0, 0, 2, 2, 2, 2, 2]}
  
  1. takes bwt_string
  2. initialize defaultdict of lists to be length of the string with 0s
  3. iterate through string and add 1 to key at the position that corresponds to the character 
      each position in list correlates to characters of the string, if there is an occurence add 1 


FUNCTION update_range:
  updates search range during backward search in the BWT pattern matching algorithm
  Args:
        lower: The lower boundary of the current range.
        upper: The upper boundary of the current range.
        count: cal_count dictionary
        occur: cal_occur dictionary
        a: The character being processed in the pattern.
    
    Returns:
        A tuple containing the updated lower and upper boundaries of the range.
  
  1. caluculate new start position using character's count and occurerences at range start
  2. calculate new end position using character's count and occurrences at range end
  3. return new start and end positions
      
    


FUNCTION find_match:
  searches for all occurrences of the query string within the. reference string and returns a list of integers representing the starting positions of the occurrences of the query string within the reference string
  Args:
        query: The pattern string to search for.
        reference: The text string to search within.
    
  Returns:
        A list of integers representing the 0-based starting positions of all occurrences of the query string within the reference string. 
        Empty list if no matches are found.
        
        
  1. initialize search range to cover the entire transformed text
  2. for each character in the pattern, processing from right to left: 
      i. update the search range based on the current character
      ii. if the range becomes empty then return empty list as pattern is not found
      
  3. Collect all suffix positions within final range
  4. return list of matching positions
```

# Successes
We were able to write most of the code quite smoothly since we took some time in our first meeting to layout some well thought out pseudocode. After taking some time to gain a better understanding of the pattern matching process, we were able to tackle the latter half effectively. Despite being in different timezones, we were able to meet up and work through code.

# Struggles
We had some trouble creating the find_match() function at first since we were wondering how exactly we should set up the functions sequentially but after sometime of working we were able to set it up correctly. We specifically had some trouble with the way our update_range() function since we originally had it as being inclusive at the lower which would result in incorrect ranges.

# Personal Reflections
## Allen Benavidez
I felt that this project was quite difficult since the algorithm was a little difficult to follow when it got to the pattern matching process. I took extra time to study the algorithm since it was important for this project to fully understand first before diving into the code. After, taking some time I was able to better understand what was required for the assignment.

## Zoe Chow
This project was much easier for me to understand conceptually compared to the last. It was very helpful to write out the matrices and do the calculations by hand. Different timezones made it hard to communicate, but our initial pseudocode session helped us map things out before we coded. I feel much more satisfied with this project than the last conceptually. 

## Michael Bambha


# Generative AI Appendix
As per the syllabus

