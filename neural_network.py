"""
3-layer Neural Network Class with Backpropagation

Developed by Joao Francisco B. S. Martins <joaofbsm@dcc.ufmg.br>
"""
import time
import math
import numpy as np

# Sigmoid activation function
def sigmoid(x):
	return 1.0 / (1.0 + np.exp(-x))

# By the chain rule we know that the derivative of the sigmoid function(s)
# is: s' = s * (1 - s). x is the value of s already calculated previously.
def sigmoid_derivative(x):
	return x * (1.0 - x)

# Convert output layer neurons value to single value output shown in dataset
def network_to_dataset(layer):
	return value

# Convert single value output shown in dataset to output layer neurons value
def dataset_to_network(value, n_units):
	output_layer = np.zeros(n_units)
	output_layer[value] = 1.0
	return output_layer

# Cross-entropy cost function
def cost_function(output, expected):
	return np.dot(-expected, np.log(output)) - np.dot((1 - expected), np.log(1 - output))

class NeuralNetwork(object):

	def __init__(self, n_input, n_hidden, n_output):

		# Number of units per layer
		self.n_input = n_input
		self.n_hidden = n_hidden
		self.n_output = n_output

		np.random.seed(1)

		# Initialize weights with random floats from the interval [-0.001, 0.001]
		self.hidden_weights = (2 * np.random.random((n_hidden, n_input + 1)) - 1) * 0.001
		self.output_weights = (2 * np.random.random((n_output, n_hidden + 1)) - 1) * 0.001

		# Activation values for neurons generated in the forward propagation step
		self.input_activation = np.zeros(n_input)
		self.hidden_activation = np.zeros(n_hidden)
		self.output_activation = np.zeros(n_output)

		# Delta values initialized as array of 0's
		self.hidden_delta = np.zeros(n_hidden)
		self.output_delta = np.zeros(n_output)

		# DELTA is the accumulator for the (mini)batch gradient descent
		self.hidden_DELTA = np.zeros((n_hidden, n_input + 1))
		self.output_DELTA = np.zeros((n_output, n_hidden + 1))

	# Forward propagation in the network for the given input. The activation function used is the sigmoid function.
	def forward_propagate(self, input):

		# Input layer(The activation function is not used here)
		self.input_activation = input

		# Hidden layer
		for neuron in range(self.n_hidden):
			activation = self.hidden_weights[neuron][-1]  # Input bias weight
			for synapse in range(self.n_input):
				activation += self.input_activation[synapse] * self.hidden_weights[neuron][synapse]
			self.hidden_activation[neuron] = sigmoid(activation)

		# Output layer
		for neuron in range(self.n_output):
			activation = self.output_weights[neuron][-1]  # Hidden bias weight
			for synapse in range(self.n_hidden):
				activation += self.hidden_activation[synapse] * self.output_weights[neuron][synapse]
			self.output_activation[neuron] = sigmoid(activation)

		return self.output_activation

	def calculate_deltas(self, expected):

		# Output layer
		for k in range(self.n_output):
			self.output_delta[k] = (self.output_activation[k] - expected[k]) * sigmoid_derivative(self.output_activation[k]) 
			self.output_DELTA[k][-1] += self.output_delta[k]
			for j in range(self.n_hidden):
				# Update acumulator for weights connected to the output layer
				self.output_DELTA[k][j] += self.output_delta[k] * self.hidden_activation[j]  

		# Hidden layer
		for j in range(self.n_hidden):
			error = 0.0
			for k in range(self.n_output):
				error += self.output_delta[k] * self.output_weights[k][j]
			self.hidden_delta[j] = error * sigmoid_derivative(self.hidden_activation[j]) 
			self.hidden_DELTA[j][-1] += self.hidden_delta[j]
			for i in range(self.n_input):
				# Update acumulator for weights connected to the hidden layer from the input
				self.hidden_DELTA[j][i] += self.hidden_delta[j] * self.input_activation[i]

	def update_weights(self, l_rate):
		# Weights of the connections that go from the hidden layer to the output layer(output_weights)

		for k in range(self.n_output):
			self.output_weights[k][-1] -= (l_rate * self.output_DELTA[k][-1])  # Update hidden bias weight
			for j in range(self.n_hidden):
				self.output_weights[k][j] -= (l_rate * self.output_DELTA[k][j])
		#		self.output_weights[k][j] -= (l_rate * self.output_delta[k] * self.hidden_activation[j])

		# Weights of the connections that go from the input layer to the hidden layer(hidden_weights)
		for j in range(self.n_hidden):
			self.hidden_weights[j][-1] -= (l_rate * self.hidden_DELTA[j][-1])  # Update input bias weight
			for i in range(self.n_input):
				self.hidden_weights[j][i] -= (l_rate * self.hidden_DELTA[j][i])
		#		self.hidden_weights[j][i] -=  (l_rate * self.hidden_delta[j] * self.input_activation[i])

	# We use the same training function to run every gradient descent algorithm requested:
	# - Standard Gradient Descent: batch size = number of input instances.
	# - Stochastic Gradient Descent: batch size = 1.
	# - Mini-batch Gradient Descent: 1 < batch size < number of input instances.
	def train(self, x, y, n_epoch, batch_size, l_rate, output_file):
		n_instance = x.shape[0]
		n_batch = n_instance / batch_size
		for epoch in range(n_epoch):
			instance = 0
			for batch in range(n_batch):
				loss = 0.0
				self.hidden_DELTA = np.zeros((self.n_hidden, self.n_input + 1))
				self.output_DELTA = np.zeros((self.n_output, self.n_hidden + 1))
				for i in range(batch_size):
					output =  self.forward_propagate(x[instance])
					expected = dataset_to_network(y[instance], self.n_output)
					loss += cost_function(output, expected)
					self.calculate_deltas(expected)
					instance += 1
				self.output_DELTA /= batch_size
				self.hidden_DELTA /= batch_size
				self.update_weights(l_rate)
				loss /= batch_size
			#	print ">epoch=", epoch, "batch=", batch, "loss=", loss
#				loss = cost_function(output, expected)
#				print ">epoch=", epoch, "batch=", batch, "loss=", loss

			with open(output_file, 'a') as f:
				f.write(str(epoch) + ',' + str(loss) + '\n')
				f.close()
			print ">epoch=", epoch, "loss=", loss

	def predict(self, input):
		pass

	def evaluate_precision(self):
		pass