# Introduction
Algorithm that processes VCF file and produces a dictionary that counts diseases that have an `AF_EXAC` key less than 0.0001.

# Pseudocode

```
def parse_line(line):
  stripped_line = strip line of whitespace and split by tabs
  INFO = save the 7th index

  split INFO by ';' and save into a list
  use find function to search up AF_EXAC
  if AF_EXAC < 0.0001:
    if CLNDN is 'not_specified' or 'not_provided'
      continue
    else
      create list that stores associated diseases in CLNDN
  
  returns list
  

def read_file(file):
  open file as infile
    for each line of infile
      if line starts with '#':
        continue
      else:
        CLNDN = parse_line(line)
  counter = {}
  for key in counter:
    for disease in CLNDN:
      if disease is not found in the key:
        counter[disease] = 1
      else
        counter[disease] += 1

  return counter

read_file(filename)  
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
