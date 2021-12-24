# OOP Course: Assignment 3:
## Preface
In this assigment, we were tasked to recreate our work from the previous assignment (written in JAVA) to Python.
Again, our task is to create a program to save, load, and perform various other different actions on directed weighted
graphs. In addition, the graph has to have a UI to present it to the user.

## Classes and Algorithms
We received several abstract classes to implement (as if interfaces in Java), as well as some json files to test the
algorithms on. The graph is to be built from json and be able to be written to json. The UML of class structure is
shown below. To view the explanation on how each algorithm is implemented, click here.

## Tests and Performance
To test the correctness of the program and its functions, several tests were run, which included, beyond the basic
tests, a comparison test between the outputs of this program and the program written in Java, for those tests which are
difficult to compute by hand. A detailed comparison between the two sets of algorithms, including runtime comparisons,
can be viewed here.


|                        | is Connected           | Shortest Path Distance | Shortest Path      | Center         | TSP (for 6 cities) |
| ---------------------- | ---------------------- | ---------------------- | ------------------ | -------------- | ------------------ |
| 1,000 Nodes            | 0.215                  | 0.211                  | 0.222              | 2.09           | 0.344              |
| 10,000 Nodes           | 0.914                  | 0.996                  | 0.987              | 27 min, 34 sec | 4.747              |
| 100,000 Nodes          | 16.421                 | 68                     | 71                 | Timeout        | 21 min, 31 sec     |