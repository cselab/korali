*********************************
Deep Supervisor
*********************************

Uses a combination of a training and evaluation :ref:`Neural Networks <module-neuralnetwork>` to solve a :ref:`Supervised Learning <module-problem-supervisedlearning>` problem. At each generation, it applies one or more optimization steps based on the loss function and the input/solutions received. The input and solutions may change in between generations.

Inference is fully openMP parallelizable, so that different openMP threads can infer from the learned parameters simultaneously. The training part should be done sequentially.  
