# Introduction
In this project, we explored the Markov model and generating text based off it. With a snippet from *One Fish, Two Fish, Red Fish, Blue Fish* by Dr. Seuss, we trained first Markov model to be memory-less- only taking one word or "state" at a time into account. We then created an *Nth* order Markov chain where the model has a memory of *N* amount of prior states to give our program the capability of generating higher-order models. Finally, we 
created functions to generate randomized text based off of the Markov model created. To ensure functionality, we tested these functions on the entirety of *One Fish, Two Fish, Red Fish, Blue Fish* as well as some Shakespeare.

# Pseudocode
Function build_markov_model(markov_model, new_text):
Feed it an empty dictionary and text
Run through the text word by word
Document the word and the word that follows after and make sure to tally occurrences as dictionary of dictionaries
Add mechanism to detect start and end of string
Return the dictionary of dictionaries

Function build_markov_model(markov_model, text, order=1):
If its order 1, follow previous function
If order > 1, then:
Use index to keep track of position
Create variable state to take into account order and read according to order size

Function get_next_word(current_word, markov_model, seed=42):
Find the word in our markov_model, get the words that follow it and count their occurrences
Divide each word's occurrence by the total amount of possibilities to get its probability
Use numpy to randomly select the next word based on probablities

Function generate_random_text(markov_model, seed=42):
Generate a new string based on the markov_model 
Start with word or words associated with *S*
Continously generate the next word until it produces *E*
Return the string

#All the fish
Create empty markov_model dictionary
Read in the one_fish_two_fish.txt
Run build_markov_model()
Run generate_random_text()

#shakespeare
Use working directory path to sonnets.txt
Run pre-existing code


# Successes
We figured out how to account for the order in our code quicker than we anticipated. We were fast to create rough drafts for 
each function. Despite our conflicting schedules we were pretty good on keeping communication with ideas, code changes and 
having teams meetings.

# Struggles
initial struggle was understanding markov models and the expectation for the task. Both of team members are novice coders and it required extra time to have working functions. We also struggled with debugging, accessing the markov model and transforming the data into appropriate data types.

# Personal Reflections
## Group Leader
When first starting the project I quickly realized that this project would be a little different than our previous project. Although we went over Markov Models in class, a lot of it I did not understand. I took some time to research and review what markov models were in order to feel more comfortable tackling this project. I felt a bit better coding in this project compared to the last project since I feel like last week provided a bit of a refresher from BINF 6200. Github was also a bit easier to navigate this time around and I was quick to create the pull request and set up the project.

## Other member
This project presented great challenges in my knowledge and understanding of data structures, rewarding me with a deeper understanding of dictionary manipulation through the concept of Markov models. Although not applied in this project, I deeply appreciate the application of this model type to omics and cannot wait to continue learning about this and other model types to oen day apply it in a relevant setting. I regret not being able to explore numpy more, as I know a true Markov model utilizes matrices to extract the chances of a future state but I did not utilize numpy's array generation and manipulation capabilities.

# Generative AI Appendix
OpenAI. (2025, September 23). What is .setdefault() and How to use .setdefault() in Python? ChatGPT (Version GPT-4). https://chat.openai.com/
