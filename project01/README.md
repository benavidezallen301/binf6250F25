# Introduction
Algorithm that processes [VCF file](project01/clinvar_20190923_short.vcf) and produces a dictionary that counts diseases that have an `AF_EXAC` key less than 0.0001. 

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
* Created a general outline of what we wanted each function to do
* Good runtime
* Learned how properly append to lists
* Gained familiarity with VCF files
* Properly used `.find()` function and extract data

# Struggles
Our main issue was having the counter count the diseases properly. Our results initially counting individual letters, 'not_specified', 'not_provided'. We created a separate code to ensure that we were correctly extracting CLNDN values, and realized that our `parse_line()` function was storing some values as strings instead because we used `=` instead of `.append`. After fixing the code, we ran into another issue where the loop in `read_file()` kept failing because the code was trying to add lists into the dictionary as keys. We realized that some lists were returned as lists of lists, causing the loop to fail. We changed the code to an  `if else` statements to fix the issue.

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
It has been a year since I practiced Python. This project served as a good refresher, allowing me to practice not only Python syntax but also create and use dictionaries. Furthermore, when I took courses for Data Analytics and Machine Learning, although I practiced a lot of programming in R, it was not object-oriented programming. This method of programming requires more planning to decipher how to implement the different functions properly. This project also taught me how to pseudo-code. Although I am not confident in my pseudo-code, I plan to improve on it in the future. I usually write down my plan and jot down notes, similar to pseudo-code, but it does not follow the proper structure or syntax that pseudo-code has. By learning pseudo-code, I aim to improve my planning strategy, which will come in handy for more complicated projects.

# Generative AI Appendix
[ChatGPT conversation](https://chatgpt.com/share/68c4af41-209c-800b-903e-1c02002b9cf0)
