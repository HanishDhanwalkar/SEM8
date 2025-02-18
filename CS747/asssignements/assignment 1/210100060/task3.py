# Task 3
# Using inspiration from code in task1.py and simulator.py write the appropriate functions to create the plot required.

import numpy as np
import matplotlib.pyplot as plt
from bernoulli_bandit import *
from task1 import Algorithm
from multiprocessing import Pool
import time


# DEFINE your algorithm class here
class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon, epsilon):
        super().__init__(num_arms, horizon)
        self.eps = epsilon
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)  # Tie-breaking: first encountered max
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# DEFINE single_sim_task3() HERE
def single_sim_task3(seed, epsilon, PROBS, HORIZON):
    np.random.seed(seed)
    shuffled_probs = np.random.permutation(PROBS)
    bandit = BernoulliBandit(probs=shuffled_probs)
    algo_inst = Eps_Greedy(num_arms=len(shuffled_probs), horizon=HORIZON, epsilon=epsilon)
    for t in range(HORIZON):
        arm_to_be_pulled = algo_inst.give_pull()
        reward = bandit.pull(arm_to_be_pulled)
        algo_inst.get_reward(arm_index=arm_to_be_pulled, reward=reward)
    return bandit.regret()

# DEFINE simulate_task3() HERE
def simulate_task3(algorithm, probs, horizon, num_sims=50):
    """simulates algorithm of class Algorithm
    for BernoulliBandit bandit, with horizon=horizon
    """
    
    def multiple_sims(num_sims=50):
        with Pool(10) as pool:
            sim_out = pool.starmap(single_sim_task3,    
                [(i, algorithm, probs, horizon) for i in range(num_sims)])
        return sim_out 

    sim_out = multiple_sims(num_sims)
    regrets = np.mean(sim_out)

    return regrets

# DEFINE task3() HERE
def task3():
    """generates the plots and regrets for task3
    """
  
    ARM_MEANS=[0.7, 0.6, 0.5, 0.4, 0.3]
    HORIZON=30000
    
    epsilons = np.arange(0, 1.01, 0.01)
    regrets = []
    
    for eps in epsilons:
        print(f"for epsilon={eps:.2f}", end=" | ")
        regrets.append(simulate_task3(eps, ARM_MEANS, HORIZON))
        print(f"regret = {regrets[-1]:.2f}")

    print(regrets)
    
    plt.figure(figsize=(8, 5))
    plt.plot(epsilons, regrets, marker='o', linestyle='-', markersize=3)
    plt.xlabel("Epsilon")
    plt.ylabel("Regret")
    plt.title("Effect of Epsilon on Regret in Epsilon-Greedy Algorithm")
    # plt.grid()
    plt.savefig("task3_regret_vs_epsilon.png")
    plt.show()
  
# Call task3() to generate the plots
if __name__ == "__main__":
    task3()