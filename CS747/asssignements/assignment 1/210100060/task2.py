import numpy as np
from task1 import Algorithm

class CostlySetBanditsAlgo(Algorithm):
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
        self.sum_rewards = np.zeros(num_arms)
        self.pulls = np.zeros(num_arms, dtype=int)
        self.t = 0  # Time step counter

    def give_query_set(self):
        self.t += 1
        ucbs = []
        for i in range(self.num_arms):
            if self.pulls[i] == 0:
                ucbs.append(1e5)  # High value for unexplored arms
            else:
                avg = self.sum_rewards[i] / self.pulls[i]
                confidence = np.sqrt((2 * np.log(self.t)) / self.pulls[i])
                ucbs.append(avg + confidence)
        
        # Sort arms in descending order of UCB
        sorted_arms = np.argsort(ucbs)[::-1]
        
        max_value = -np.inf
        best_m = 1
        
        for m in range(1, self.num_arms + 1):
            current_m_arms = sorted_arms[:m]
            sum_ucb = sum(ucbs[i] for i in current_m_arms)
            current_value = (sum_ucb - 1) / m
            # Update if current_value is higher, or equal but m is larger
            if current_value > max_value or (current_value == max_value and m > best_m):
                max_value = current_value
                best_m = m
        
        query_set = sorted_arms[:best_m].tolist()
        return query_set

    def get_reward(self, arm_index, reward):
        self.sum_rewards[arm_index] += reward
        self.pulls[arm_index] += 1