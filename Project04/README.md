# Introduction

We will implement one of the primary assembly algorithms from short-read data that is used today, using a simple form of the algorithm where we *assume perfect sequencing*. That is, everything is sequenced exacty once and there are no errors or variants in the sequencing.

A graph is composed of **nodes** and **edges** and we will need to develop a data strcture to track edges between nodes in our graph. We have been provided with the basic class structure as well as descriptions of functions to `add_edge` and `remove_edge` from the graph. We will need to implement these functions in order to then build the de Bruijn graph.

In our implementation, we use a `defaultdict` data structure to hold a list of all edges in the graph where all "right" nodes connected to a "left" node are stored in a list for that node.

# Pseudocode

## Add Edge

```         

function add_edge(self, left, right):
        dictionary[left].append(right)
        return dictionary
```

## Remove Edge

```         
function remove_edge(self, left, right):
        dictionary[left].remove(right)
        return dictionary
```

## Build de Bruijn Graph

```         

function build_debruijn_graph(self, input string, k):
dictionary = {}
  For each kmer of input string:
      left <- string[0:k]
      right <- string[1:k+1]
      add_edge(left,right)   
      #add k-1 mers as nodes with a directed edge from left k-1 mer to right k-1 mer
  return dictionary
```

## Print Eulerian Walk

```         
function print_eularian_walk(self, seed = None):
        if seed is not None:
                set random seed  # random.seed(seed)

        first_node <- randomly select node
        return eularian_walk(first_node, seed)
        
```

## Eularian Walk

```         
#V1.0 - recursion
function eulerian_walk(node, seed = None):
        if seed is given:
                set seed
                
        tour <- add node to the list 
        edge <- randomly selected edge from dictionary  #random.choice?
        remove edge from node in the dictionary
        set the edge as the next node
        if the node has an empty list
                return tour
        else  # recurse
                next_tour <- eularian_walk(node)  # store next node and edge
                return tour + next_tour  # combine lists
                
```

# Successes

-   Creating and understanding the De Bruijn graph was much more straightforward than implementing the Eulerian Walk. Initially, we were unsure how to construct a `defaultdict` efficiently without multiple iterations, but once we realized that each k-mer consists of both a left and right part, the function's logic became much clearer.

# Struggles

-   Understanding how to use and apply recursion. This was a relatively unfamiliar concept for the both of us, so it took a bit of discecting before we were able to apply it appropriately.
-   Using self. to call on functions

# Personal Reflections

## Group Leader (Allen Benavidez)

My first obstacle when beginning this project was getting a better understanding of De Bruijn Graphs. I took some time to do some research on De Bruijn Graphs and Eulerian Walk to create a plan on how to tackle the project. Once Zoe and I started writing the pseudocode, things began to come together little by little. The good portion of our time was spent on writing the pseudocode for this project which really laid the foundation. We then went on to write our code which went smoothly for the most part since we had put a lot of effort into our pseudocode. We had some struggles, especially in the recursion portion as well as a few bugs that were occurring with our code, but we ultimately solved those issues by taking the time to look through our code and researching ways to properly apply recursion in our code. My biggest take away from this project has been the importance of creating good pseudocode as well as giving yourself enough time to go back and fix any bugs that occur.

## Other member (Zoe Chow)

As usual, I felt confused and overwhelmed after class, but after discussing the problem with Allen, we were able to better understand how the De Bruijn Graph and Eulerian Walk worked. We spent a large portion of the project pseudocoding and working through the two main functions. Once we fully grasped the task, the actual coding process became much simpler. Breaking down each function line by line helped us clarify our approach. For the Eulerian Walk function, I initially felt uncomfortable using recursion—despite encountering it in Project 2—and first implemented it using a while loop. However, after reading several resources like [GeeksforGeeks](https://www.geeksforgeeks.org/python/recursion-in-python/) and [w3schools](https://www.w3schools.com/python/gloss_python_function_recursion.asp), my understanding of recursion improved. At first, I incorrectly thought a for loop was necessary when pseudocoding the recursive solution, but I later realized that recursion continues calling the function until a base case is reached, eliminating the need for such a loop. I wrote separate versions of the recursion function to experiment with different recursive approaches, though we ultimately kept the version that made the most sense to both of us. In addition to recursion, de bruijn graphs, and eulerian walk, I was also a bit unfamiliar with using class functions. I have used them before in BINF6200, but I had completely forgotten about it. Therefore, there was a lot of debugging and fine-tuning required before the program worked correctly. This project introduced various concepts that were new to me, but I’m proud of our progress. Understanding how these ideas are implemented was both challenging and rewarding.

# Generative AI Appendix

As per the syllabus
