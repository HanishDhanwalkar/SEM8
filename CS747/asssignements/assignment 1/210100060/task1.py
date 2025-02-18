"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars
from scipy.optimize import bisect

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_divergence(p, q):
    if p == 0:
        return - (1-p)*math.log(1-q) if q < 1 else float('inf')
    elif p == 1:
        return - p*math.log(q) if q > 0 else float('inf')
    elif q == 0:
        return float('inf')
    elif q == 1:
        return float('inf')
    else:
        return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.t = 0
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.t +=1
        ucb_values = np.zeros(self.num_arms)
        for i in range(self.num_arms):
            if self.counts[i] > 0:
                ucb_values[i] = self.values[i] + math.sqrt((2 * math.log(self.t)) / self.counts[i])
            else:
                ucb_values[i] = float('inf')  
        return np.argmax(ucb_values)
        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.t = 0
        self.epsilon = 1e-3
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.t += 1
        kl_ucb_values = np.zeros(self.num_arms)

        for i in range(self.num_arms):
            if self.counts[i] > 0:
                p = self.values[i]  
                c = math.log(self.t) + 3 * math.log(math.log(self.t)) 
                def kl_diff(q):
                    if q <= 0 or q >= 1: 
                        return float('inf')
                    return kl_divergence(p, q) - c / self.counts[i]

                low = p
                high = 1.0 if p < 1 else (p + (1-p)/2) # Adjust high if p is close to 1

                try:
                    q = bisect(kl_diff, low, high, xtol=self.epsilon)
                    kl_ucb_values[i] = q
                except ValueError: 
                    kl_ucb_values[i] = float('inf') 

            else:
                kl_ucb_values[i] = float('inf')  

        return np.argmax(kl_ucb_values)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE
    


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.alphas = np.ones(num_arms)
        self.betas = np.ones(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        samples = [np.random.beta(self.alphas[i], self.betas[i]) for i in range(self.num_arms)]
        return np.argmax(samples)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward == 1:
            self.alphas[arm_index] += 1
        else:
            self.betas[arm_index] += 1
        # END EDITING HERE

