import numpy as np
import itertools
import random

class WumpusWorldPOMDP:
    def __init__(self, grid_size, pit_locs, wumpus_loc, gold_loc, start_position):
        self.grid_size = grid_size
        self.pit_locs = pit_locs
        self.wumpus_loc = wumpus_loc
        self.gold_loc = gold_loc
        self.current_state = start_position
        self.state_space = list(itertools.product(range(grid_size), repeat=2))
        self.belief_state = np.full((grid_size, grid_size), 1.0 / (grid_size ** 2))
        self.actions = ["up", "down", "left", "right"]
        self.has_gold = False
        self.start_position = start_position 
        self.reset_world()
        # You can add more detailed implementation here

    def reset_world(self):
        # Reset the agent's position to the start position
        self.current_state = self.start_position

        # Reset the belief state to a uniform distribution
        self.belief_state = np.full((self.grid_size, self.grid_size), 1.0 / (self.grid_size ** 2))

        # Reset the flag indicating whether the agent has the gold
        self.has_gold = False

       

        print("The Wumpus world has been reset.")

    def perceive_environment(self, state):
        # Simplified observation model
        stench = any([self.manhattan_distance(state, self.wumpus_loc) == 1])
        breeze = any([self.manhattan_distance(state, pit) == 1 for pit in self.pit_locs])
        glitter = (state == self.gold_loc)
        return (stench, breeze, glitter)

    def manhattan_distance(self, state_a, state_b):
        return abs(state_a[0] - state_b[0]) + abs(state_a[1] - state_b[1])

    def get_transition_probability(self, state, action, next_state):
        # For a deterministic world, the transition probability is either 0 or 1
        expected_next_state = self.get_next_state(state, action)
        return 1 if next_state == expected_next_state else 0

    def get_next_state(self, state, action):
        x, y = state
        if action == "up" and y < self.grid_size - 1:
            return (x, y+1)
        elif action == "down" and y > 0:
            return (x, y-1)
        elif action == "left" and x > 0:
            return (x-1, y)
        elif action == "right" and x < self.grid_size - 1:
            return (x+1, y)
        return state  # If the action is not possible, stay in the current state

    def update_belief_state(self, action, observation):
        new_belief_state = np.zeros_like(self.belief_state)

        for state in self.state_space:
            prob_sum = 0
            for next_state in self.state_space:
                transition_prob = self.get_transition_probability(state, action, next_state)
                obs_prob = self.get_observation_probability(next_state, observation)
                prob_sum += self.belief_state[state] * transition_prob * obs_prob
            new_belief_state[next_state] = prob_sum

        # Normalize the new belief state
        self.belief_state = new_belief_state / np.sum(new_belief_state)

    def get_observation_probability(self, next_state, observation):
        # Assuming perfect observations
        actual_observation = self.perceive_environment(next_state)
        return 1 if actual_observation == observation else 0

    def choose_action(self):
        # For the sake of example, we choose an action randomly
        # Replace this with a more sophisticated decision-making process
        actions = ['move_north', 'move_south', 'move_east', 'move_west', 'grab', 'shoot']
        return np.random.choice(actions)

    def simulate_action(self, current_state, action):
        # # This function simulates the result of an action and provides an observation
        # next_state = self.get_next_state(current_state, action)
        # observation = self.perceive_environment(next_state)
        
        # self.current_state = next_state
         x, y = self.current_state
         if action == 'move_north' and y > 0:
                new_state = (x, y-1)
         elif action == 'move_south' and y < self.grid_size - 1:
                new_state = (x, y+1)
         elif action == 'move_east' and x < self.grid_size - 1:
                new_state = (x+1, y)
         elif action == 'move_west' and x > 0:
                new_state = (x-1, y)
         elif action == 'grab' and self.current_state == self.gold_loc:
                self.has_gold = True
                new_state = self.current_state
         else:
                new_state = self.current_state  # No movement for invalid actions

            # Simplified observation
         observation = 'breeze' if new_state in self.pit_locs else 'glitter' if new_state == self.gold_loc else 'none'
          # Update the current state to the new state after action is simulated
         self.current_state = new_state
         return new_state, observation

    def play(self):
        self.reset_world() 
        current_state =  self.current_state#(0, 1)  # assuming the agent starts at (0, 0)

        while current_state != self.gold_loc:
            action = self.choose_action()
            next_state, observation = self.simulate_action(current_state, action)
            self.update_belief_state(action, observation)
            current_state = next_state
            print(f"Moved to {current_state}, Observation: {observation}")

            if current_state in self.pit_locs or current_state == self.wumpus_loc:
                print("Game Over: Fell into a pit or encountered the Wumpus!")
                break

            if current_state == self.gold_loc:
                print("Found the Gold!")
                break

# Example setup
grid_size = 4
pit_locs = [(1, 1), (2, 2)]
wumpus_loc = (3, 3)
gold_loc = (3, 0)
start_position = (0, 0)


game = WumpusWorldPOMDP(grid_size, pit_locs, wumpus_loc, gold_loc, start_position)
game.play()
