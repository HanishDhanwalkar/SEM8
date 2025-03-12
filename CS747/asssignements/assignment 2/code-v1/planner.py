import random
import argparse
import numpy as np

class Planner():
    def __init__(self, mdp_file, algo, policy=None):
        self.mdp_file = mdp_file
        self.policy = policy
        
        self.read_mdp()
                
        if algo == "hpi":
            self.hpi_algo(policy=policy)
        elif algo == "lp":
            self.lp_algo()
        else:
            print("invalid algorithm specifice. Chose from hpi and lp")
            
            
    def read_mdp(self):
        with open(self.mdp_file) as f:
            lines = f.readlines()
            
        self.num_states = int(lines[0].split()[1])
        self.num_actions = int(lines[1].split()[1])
        self.end_states = set(map(int, lines[2].split()[1:]))
        # print(self.num_states, self.num_actions, self.end_states)
        
        self.transitions = { (s, a): [] for s in range(self.num_states) for a in range(self.num_actions) }
        
        for line in lines[3:]:
            parts = line.split()
            if parts[0] == "transition":
                s1, ac, s2, r, p = int(parts[1]), int(parts[2]), int(parts[3]), float(parts[4]), float(parts[5])
                self.transitions[(s1, ac)].append((s2, r, p))
                
            elif parts[0] == "mdptype":
                self.mdptype = parts[1]
                
            elif parts[0] == "discount":
                self.gamma = float(parts[1])
        
        for key in self.transitions:
            print(key, ": ", self.transitions[key])
        
        
    def hpi_algo(self, policy):
        def policy_evaluation(policy, tol=1e-9):
            V = np.zeros(self.num_states)
            while True:
                delta = 0
                for s in range(self.num_states):
                    if s in self.end_states:
                        continue
                    v = V[s]
                    a = policy[s]
                    V[s] = sum(p * (r + self.gamma * V[s2]) for s2, r, p in self.transitions.get((s, a), []))
                    delta = max(delta, abs(v - V[s]))
                if delta < tol:
                    break
            return V
        
        def policy_improvement(V):
            policy_stable = True
            policy = np.zeros(self.num_states, dtype=int)
            
            for s in range(self.num_states):
                if s in self.end_states:
                    continue
                
                action_values = []
                for a in range(self.num_actions):
                    action_value = sum(p * (r + self.gamma * V[s2]) for s2, r, p in self.transitions.get((s, a), []))
                    action_values.append(action_value)
                
                best_action = np.argmax(action_values)
                if best_action != policy[s]:
                    policy_stable = False
                policy[s] = best_action
            return policy, policy_stable
        
        policy = np.zeros(self.num_states, dtype=int)
        while True:
            V = policy_evaluation(policy)
            new_policy, stable = policy_improvement(V)
            if stable:
                break
            policy = new_policy
        return V, policy
    
    def lp_algo(self):
        pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MDP Solver")
    parser.add_argument("--mdp", help="path to the input MDP file", required=True, type=str, default="./data/mdp/continuing-mdp-2-2.txt")
    parser.add_argument("--algorithm", help="algorithm followed by one of hpi and lp", default="hpi", required=True, choices=["hpi", "lp"])
    parser.add_argument("--policy", help="path to the policy file", default=None)
    args = parser.parse_args()

    # size = int(args.size)
    # alpha = float(args.alpha)
    
    planner = Planner(args.mdp, args.algorithm, args.policy)
    
    