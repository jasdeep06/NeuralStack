# NeuralStack
Attempt to implement Neural Stack from paper "Learning to transduce from unbounded memory".The paper can be found [here](https://arxiv.org/pdf/1506.02516v3.pdf)
#### This project is in progress and will see a lot of modification and progress in coming days.
When I implement papers like these,I prefer to break the tasks in sections.
The file `NStackForward.py` does forward propogations through stacks.It defines the main structure of neural stacks and gives implementation of reading from the stack and writing to the stack.It also defines push and pop operations and how they effect strength vector.

The second file `NStackBackprop.py` does a backpropogation through the stack and thus determines how error propagates through the stack.

#### This project will be modified to reverse a squence using a Neural stack in coming days.

