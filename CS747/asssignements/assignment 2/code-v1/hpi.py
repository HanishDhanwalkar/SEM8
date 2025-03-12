import numpy as np


class HPI():
    def __init__(self, mdpfile):
        self.load_mdp(mdpfile)
        
        
    def load_mdp(self, mdpfile):
        with open(mdpfile) as f:
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
            
    
            

    def policy_evaluation(self, policy, theta=0.001):
        V = np.zeros(self.num_states)
        
        while True:
            delta = 0.0
             
            for s in range(self.num_states):
                if s in self.end_states:
                    continue
                
                v = V[s]
                a = policy[s]
                V[s] = sum(p * (r + self.gamma * V[s2]) for s2, r, p in self.transitions.get((s, a), []))
                delta = max(delta, abs(v - V[s]))
                if delta < theta:
                    break
            return V
            
    def policy_improvement(self, V):
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
    
    def howards_policy_iteration(self):
        policy = np.zeros(self.num_states, dtype=int)
        while True:
            V = self.policy_evaluation(policy)
            print(f"olf policy: {policy}")
            new_policy, stable = self.policy_improvement(V)
            print(f"new policy: {new_policy}")
            if stable:
                break
            policy = new_policy
        return V, policy
                

    
if __name__ == "__main__":
    hpi = HPI("data\mdp\continuing-mdp-2-2.txt")
    # V, policy = hpi.howards_policy_iteration()
    
    # for s in range(hpi.num_states):
    #     print(f"{V[s]:.6f} {policy[s]}")
    