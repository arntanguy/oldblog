Title: Multi-layered Perceptron using OpenCL 
Date: 2014-02-28 
Tags: programmation, opencl, neural networks, perceptron 
Summary: Detailled explanation on how to create a fully-connected Perceptron neural network. The code is written using OpenCL. 
disqus_identifier: geenux-perceptron-opencl

I recently discovered **neural networks**, and I was instantly very interested by the topic. I am a big fan of computer vision, 
and have always had a feeling that this field was doomed by the sheer amount of possible combinations possible. How could we ever come up with an
algorithm that wouldn't crash at the first unexpected input? How can we analyse complex behaviour, such as distinguishing distress in a metro when
so much trivial noise and movements are going on? How could we ever get robots intelligent enough to cope with their environment as well, or even better than
we do? I believe I'm starting to see a glimmer of hope in neural networks, that we could one day achieve such things, that at the moment seem like a daunting task.
Of course a perceptron is way too simple a network for such things, but one has to start somewhere, hasn't he?

I am convinced that it is utterly useless to read thousands of pages on neural networks to try and understand their behaviour. The best way to approach them
is by trial and error. In this article, I will show you what a perceptron is, how to implement and train it using **GPU computing with OpenCL**. 

# What is a perceptron

A perceptron is basically a binary classifier: it will either tell you that the input values you provided match with the model it that has previously
been learnt, or tell you that they don't. That is for a single output neuron. By providing several outputs, it is possible to use
the perceptron as a classifier, effectively separating the input set in several classes.

So basically, it is a **linear classifier**. You're probably wondering what you have to gain using a perceptron instead of SVM (Support Vector Machine),
or similar algorithm. Well, actually not much. The perceptron was discovered before SVM was developped, and since then, SVM has pretty much
replaced all uses of the perceptron. 

Even though, the perceptron can be seen as the very basis of neural networks, and is a stepping stone on which one has to
walk on in order to fully understand the concepts behind neural network algorithms.
As all neural networks, it requires a great amount of inter-connected neurons to provide enough capacity to learn a given model.
It is thus a challenge to use a perceptron to accomplish complicated classification in real-time. Also, the training task can be a daunting computation, that might have
to be ran loads of time before fine-tuning the training to achieve the expected outcome. 


A fully-connected perceptron is probably the simplest neural network you could ever think of. It is composed of several layers, each containing a given number of neurons.
Each neuron of a layer is connected to every single neuron of the following layer. Each connection has an associated weight. It is by adjusting these weights that the network will
tune himself to any linear classification problem, of course given that the network has enough complexity for the given problem (i.e has a sufficient number of neurons and layers 
for it to be able to learn the model). 

There are three types of layers:

* **The input layer**: it is the first layer, where you set the initial data that your perceptron will be working on.
* **The hidden layers**: these are all the layers between the input and output layer. They're basically the ones that will be doing all the work of learning a 
    model and computing input values against the model in order to classify them.
* **The output layer**: composed of one or several neurons. This layer represents the result of the classification, where each neuron represent a specific class. 
    
Each neuron value in the hidden layers and the output layer is computed as the weighted sum of all the neurons' values linked to it by the weights linking them together.


![Perceptron layers]({filename}/images/programmation/neural/perceptron.png)



Hopefully, neural networks are generally **highly parallel algorithm**, and the perceptron is probably their king.
In this article, I will present how to implement a fully-connected perceptron using **OpenCL**. This article will explain in detail the training algorithm,
along with its naive implementation. A later article will discuss a faster training algorithm, and optimizations to the kernel presented here. 


# Training algorithm : gradient backpropagation

Training a perceptron is a minimization problem. We define a training set as a set of (input -> output) values.
The goal of the training is to find the weights that minimize the distance between the output computed by the 
perceptron on the output corresponding to the same input in the training set.

In this article we'll train a perceptron that is able to recognise a **xor** operation. 
First of all, here is the xor truth table:

  a | b | xor(a,b) 
  --|---|----------
  0 | 0 | 0 
  0 | 1 | 1 
  1 | 0 | 1 
  1 | 1 | 0 

So the goal of the training will be to find the weights needed for the perceptron to give the correct output for all possible inputs a and b of the 
truth table.

In order to train the weights, we will use an algorithm based on a gradient descent.
First, let us define some notations:

* $n$: number of cells in layer, designed by an index $i$ with $0 <= i <= n$ 
* $q$: number of layers
* $k$: index of an output cell
* $c_k$: expected output for output cell k for entry x
* $o_k$: computed output for output cell k for entry x
* $x_{ij}$: input value associated with link between cell i towards cell j
* $w_{ij}$: weight
* **Succ(i)**: set of cells that have the output of cell i as an input 
* **Pred(i)**: set of cells whose output is an input of cell i
* $y_i$: weighted sum of cell i $$y_i = \sum{w_{ij}x_{ij}}$$
* $o_i$: output of cell i $$o_i = \sigma(y_i)$$ where $\sigma$ is the sigmoid function: $$\sigma(x) = \frac{1}{1+e^{-x}}$$
* $S$ : Learning set

![Notations]({filename}/images/programmation/neural/perceptron_notation.png)

Before getting deeper into the algorithm, let's just give an overview of what we'll have to do. First, we need to compute the value of every single neuron from the input
to the output layer. Once we have that, we can compare the output with the expected output, and compute the gradient $\delta$ for the output layer.
Then, we compute $\delta$ for every layer based on the value of the following layer. This is a process called backpropagation. 
Finally we update the weight values using the neuron's and $\delta$ values previously computed.

**The algorithm goes as follow**:

* Randomly initialize all weights in interval $[-0.5, 0.5]$
* Repeat until convergence
    * Pick example $(x, c)$ in $S$ (x: input value, c: expected output)
    * Compute output $o$ for input $x$
    * For each output cell $i$ (in output layer)
        * Compute $\delta_i$ for each cell of the output layer: $$\delta_i = \sigma'(y_i)(c_i-o_i) = o_i(1-o_i)(c_i-o_i)$$
    * For each layer from $q-1$ to $1$
        * Compute $\delta_i$ for each cell of the current layer: $$\delta_i = \sigma'(y_i)\sum_{k\in\text{Succ(i)}}{\delta_k w_{ki}} = o_i(1-o_i)\sum_{k\in\text{Succ(i)}}{\delta_k w_{ki}}$$
    * Update weights: for each weight $w_{ij}$
      $$w_{ij} = w_{ij} + \epsilon \delta_i x_{ij}$$


## Note on thresholding

The values of each layer need to be thresholded. To do so, we add a "virtual neuron", called *bias* in each layer, with a fixed value of 1. By updating the associated weights as well, this neuron can be used as an automatic threshold.
           
![Bias]({filename}/images/programmation/neural/perceptron_bias.jpg)


# Implementation


## Core structure

We have to be able to create an arbitrary number of layers, each containing an arbitrary number of neurons.
Each layer must be connected to the following layer for execution, but also to the previous layer for the training
phase (backpropagation). Thus, the perceptron data structure will be implemented as a double-linked list of layers.

Thus, we create two main classes:

* PerceptronLayer : represents a layer of the network. Each layer is composed of:
    * an array of neuron values.
    * an array representing the weights from this neuron to all neurons of the next layer.
    * a pointer to the next layer
    * a pointer to the previous layer
* Perceptron : manages the creation/removal of layers, training, execution of the network. It only needs to 
store a pointer to the first and last layers.

## OpenCL

We are now going to see how this can be implemented using OpenCL. This section depicts a very raw and poorly implemented
version of the algorithm. It is only meant to be kept simple so that it provides a clear basis onto which further optimisations can be thought of.

First, let's start with the execution part of the network.

### Execution

The execution is really straightforward. It is just a matter of computing the new value of each neuron based on the weighted sum of all neurons from the previous layer. Thus, the kernel will take as input the weights and values for each input neuron (neurons from the previous layer), and will have as output an array containing the new values of the neurons in the current layer.
The kernel is thus ran in order on the 2nd, 3rd.... Nth layer.

The following kernel can be used to compute the new value for each neuron. Note that it is far from optimal as local memory isn't used at all for the weighted sum!

    ::opencl
        /**
        * @brief Computes one layer of the perceptron given the previous one and the
        * weights
        * The kernel is run once for each layer.
        * The work items are each tasked with computing the output of a single neuron
        * of the out layer.
        *
        * @param out_layer_size
        *   Size of the output layer (number of elements in the output array that will
        *   contain the result for each neuron).
        * @param in_layer_size
        *   Number of elements of the input layer
        * @param in_value
        *   Values of the neuron in the previous layer
        * @param in_weights
        *   Array containing the weights for each input neuron. It is organised as a
        *   two dimensional matrix, written by concatenating each line in the array
        *   [ w11, w12, w13, ...
        *     w21, w22, w23, ...
        *     ..., ..., ..., ...
        *   ]
        *   Where wij is the weight linking the neuron i of the input layer to the
        *   neuron j of the output layer
        *   The last weights of each row represent the weights for the "biais neuron",
        *   whose role is to threshold the values.
        *   Thus, this kernel should be run with a NDRange of in_layer_size-1
        * @param out_values
        *   Computed values for the current layer
        */
        void kernel perceptron(
                const int in_layer_size,
                const int out_layer_size,
                global const float *in_value,
                global const float* in_weights,
              global float* out_values)
        {
            private const int global_id = get_global_id(0);
            private const int out_layer_s = out_layer_size;
            private const int in_layer_s = in_layer_size;
        
            private float sum = 0.;
            for(int i=0; i < in_layer_s; i++) {
                sum += in_weights[i+in_layer_s*global_id] * in_value[i];
            }
            out_values[global_id] = sigmoid(sum);
        }


### Training

First, we initialize the weights in range $[-0.5; 0.5]$. This is done on the host side, 
as random algorithm can be quite tricky to implement efficiently on GPU.

All the rest is done in OpenCL. There is a kernel for each step of the algorithm described above.
It should be fairly easy to understand by reading the code and comments.

* **perceptron_train_output_layer** : forward propagation that computes delta for the output layer
* **perceptron_train_backpropagate** : backpropagation that computes delta for every single layer
* **perceptron_train_update_weights** : update the weight based on the previously computed delta-values.
* **perceptron_train_update_weights_intertia** : another version of the algorithm, updating the weights faster when far from convergence, and getting slower and slower as the convergence zone approaches. This requires however to keep track of the weights from the two previous iterations.


    ::opencl
        float sigmoid(float x)
        {
            return 1./(1. + exp(-x));
        }

        /**
         * @brief Computes delta for all of the output neurons.
         * 
         * @param values
         *      Values of the output layer
         * @param expected_values
         *      Values expected as output of the perceptron
         * @param delta
         *      Output of the function: computes the delta needed for the training algorithm
         **/
        void kernel perceptron_train_output_layer(
                global const float* values,
                global const float* expected_values,
                global float* delta)
        {
            private const float ci = expected_values[get_global_id(0)];
            private const float oi = values[get_global_id(0)];
            // Equivalent to sigmoid'(yi) * (ci-oi)
            delta[get_global_id(0)] = oi * (1-oi) * (ci-oi); 
        }
        
        /**
         * @brief Computes delta for all layers (but the last one) 
         * 
         * @param curr_size
         *      Size of current layer
         * @param succ_layer_size
         *      Size of the output layer of current layer 
         * @param current_layer_values 
         *      Values of current layer (calculated during forward propagation)
         * @param weights
         * @param succ_layer_delta_i
         *      Values of delta for the next layer 
         **/
        void kernel perceptron_train_backpropagate(
                const int curr_size,
                const int succ_layer_size,
                global const float* current_layer_values,
                global const float* weights,
                global const float* succ_layer_delta_i,
                // output
                global float* current_delta_out
                )
        {
            private const int i = get_global_id(0);
            private const float oi = current_layer_values[get_global_id(0)];
            private const int succ_size = succ_layer_size;
        
            private float sum = 0.f;
            for(int k=0; k < succ_size; k++) {
                sum += succ_layer_delta_i[k] * weights[i + curr_size * k];
            }
            current_delta_out[i] = oi*(1-oi) * sum;
        }
        
        /**
         * @brief Update the weights according to values of delta computed during backpropagation
         * 
         * @param out_layer_size
         * @param epsilon_value
         *      Parameter controlling the rate of convergence.
         *      epsilon too low will lead to a very slow convergence,
         *      epsilon too high will prevent convergence
         * @param pred_values
         * @param delta
         * @param weights
         **/
        void kernel perceptron_train_update_weights(
                const int out_layer_size,
                const float epsilon_value,
                global const float *pred_values,
                global const float *delta,
                global float* weights)
        {
            private const int global_id = get_global_id(0);
            private const int out_layer_s = out_layer_size;
            private const float val = pred_values[global_id % out_layer_s];
        
            // XXX to change
            private const float epsilon = epsilon_value;
            // For each weight
            weights[global_id] += epsilon * delta[global_id /out_layer_s] * val; 
        }
        
        /**
         * @brief Update the weights according to values of delta computed during backpropagation
         * Uses the weights computed in the two previous training steps to accelerate convergence.
         * 
         * @param out_layer_size
         * @param epsilon_value
         *      Parameter controlling the rate of convergence.
         *      epsilon too low will lead to a very slow convergence,
         *      epsilon too high will prevent convergence
         * @param beta_value
         *      Parameter controlling the non-linear convergence rate
         * @param pred_values
         * @param delta
         * @param previous_weights2
         *        Weights at the k-2 iteration
         * @param weights
         *        As input, weights at the k-1 iteration.
         *        As output, new weight at the k iteration
         **/
        void kernel perceptron_train_update_weights_inertia(
                const int out_layer_size,
                const float epsilon_value,
                const float beta_value,
                global const float *pred_values,
                global const float *delta,
                global const float *previous_weights2,
                global float* weights)
        {
            private const int global_id = get_global_id(0);
            private const int out_layer_s = out_layer_size;
            private const float val = pred_values[global_id % out_layer_s];
            // wij(k-1)
            private const float w1 = weights[global_id];
            // wij(k-2)
            private const float w2 = previous_weights2[global_id];
        
            // XXX to change
            private const float epsilon = epsilon_value;
            private const float beta = beta_value;
            //printf("w1-w2: %f\n", w1-w2);
            // For each weight
            weights[global_id] = w1 + epsilon * delta[global_id /out_layer_s] * val
                                + beta *  (w1-w2); 
        }
        

# Conclusion

This article showed how to easily create a perceptron neural network using OpenCL. 
This is one of my first OpenCL projects, and  I'm perfectly aware that this is far from being an optimal 
code. This article was partly meant as a reminder for myself of how I implemented the perceptron, so that I can
later on come back to it and improve upon it. The main thing remaining to do would be to make proper use of local memory,
in order to considerably improve the efficiency of the weighted sums computations. I will describe this in another article later on.

The full code is available on my github account [here](https://github.com/geenux/perceptron)

I want to thank [Lionel Filatre](http://www.i3s.unice.fr/~fillatre), Professor at the University of Polytech'Nice-Sophia
for his lectures on neural networks. 
