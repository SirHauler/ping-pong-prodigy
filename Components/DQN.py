from tensorforce.agents import Agent
import numpy as np
from tensorforce.environments import Environment as EnvironmentTFS

# NOTE: Uninstalled tensorflow-metal
# SEE: https://stackoverflow.com/questions/72459142/tensorflow-m1-mac-multiple-default-opkernel-registrations-match-nodedef-node

class DQN:
    def __init__(self, states, actions, lrate=1e-1, discount=0.99, exploration=0.3):
        self._states = states
        self._actions = actions
        self._state_history = []
        self._action_history = []

        class CustomEnvironment(EnvironmentTFS):
            def __init__(self):
                super().__init__()

            # Note that states are all one-hot encoded
            def states(self):
                # NOTE: This is a one-hot encoding (encodes relative lateral position of ball WRT to agent)
                return dict(type='float', shape=(len(states),))

            def actions(self):
                # return dict(type='int', num_values=len(actions))
                # NOTE: This is a one-hot encoding (allows for simulatenous movement and hitting)
                return dict(type='float', shape=len(actions),)

            # Optional: should only be defined if environment has a natural fixed
            # maximum episode length; otherwise specify maximum number of training
            # timesteps via Environment.create(..., max_episode_timesteps=???)
            def max_episode_timesteps(self):
                return super().max_episode_timesteps()

            # Optional additional steps to close environment
            def close(self):
                super().close()

            def reset(self):
                state = np.random.random(size=(len(self._states),))
                return state

            def execute(self, actions):
                # next_state = np.random.random(size=(8,))
                # terminal = False  # Always False if no "natural" terminal state
                # reward = np.random.random()
                # return next_state, terminal, reward
                # NOTE: We should never be running this
                pass

        self._agent = a = Agent.create(agent='dqn', 
                                    batch_size=10,
                                    learning_rate=lrate,
                                    discount=discount,
                                    environment=EnvironmentTFS.create(environment=CustomEnvironment,
                                                                      max_episode_timesteps=100),
                                    exploration=exploration,
                                    memory=12)
    
    def performAction(self, current_state: int):
        # This performs the one-hot encoding
        state_test = np.zeros(len(self._states), dtype=float)
        state_test[current_state - 1] = 1.0
        # The agent takes a certain action
        action = self._agent.act(states=state_test)
        self._action_history.append(action)
        return action
    
    def updateUnderstanding(self, true_terminal, reward):
        # true_terminal, reward = False, 3
        assert true_terminal is False
        self._agent.observe(terminal=true_terminal, reward=reward)