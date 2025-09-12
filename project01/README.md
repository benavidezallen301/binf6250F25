# Introduction
Algorithm that processes [VCF file](/clinvar_20190923_short.vcf) and produces a dictionary that counts diseases that have an `AF_EXAC` key less than 0.0001. 

# Pseudocode

```
def parse_line(line):
  split_line = strip line of whitespace and split by tabs
  info = save the 7th index

  create and initiate CLNDN list that we will return

  find position of AF_EXAC
  if AF_EXAC position is available:
    extract value and
    if AF_EXAC < 0.0001:
      find and extract CLNDN value
      if CLNDN has '|':
        CLNDN = CLNDN value split by '|' using .split() which returns a list
      else:
        append CLNDN value to CLNDN list
  
  returns CLNDN list
  

def read_file(file):
  create and initiate disease count dictionary
  open file as infile
    for each line of infile
      if line starts with '#':
        continue
      else:
        CLNDN = parse_line(line)

    for each disease in CLNDN list
      if disease is not 'not_specified' or 'not_provided':
        if disease is in disease count dictionary:
          add 1 to the key with the same disease
        else
          create key and set as 1
      else
        continue

  return disease count dictionary

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
