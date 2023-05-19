# @Author: Alex Alvarado-Barahona
# @Date:   2023-02-01T20:02:18-08:00
# @Email:  alexaab@stanford.edu
# @Filename: RLAgent.py
# @Last modified by:   Alex A.
# @Last modified time: 2023-02-01T20:03:33-08:00

# EOF

from Components.Agent import Agent
from Components.Ball import Ball

import numpy as np
import tensorflow as tf 
from tensorflow import keras 
from keras import layers
from keras.models import load_model


HIT = "hit"
MOVE = "re-adjusted"

HIT_REWARD = 10
WIN_REWARD = 0
MOVE_CORRECTLY_REWARD = 0
WRONG_MOVE_REWARD = -1

class RLAgent(Agent):
    def __init__(self, position, perception_latency=..., max_movement_speed=..., max_hit_speed=..., t=1):
        super().__init__(position, False, perception_latency, max_movement_speed, max_hit_speed)
        self._id = "RL"
        self.t = t  # specifies time interval: seconds. By Defualt
        self._move_actions = [0, 1, 2] # left, right, stay
        self._hit_actions = [3, 4, 5]  # hit1, hit2, hit3 in this order
        self._hit_spaces = {}
        
        self.model = load_model('working-rlagent.h5')
        self.critic_value_history = []
        self.actions_probs_history = []
        self.rewards_history = []
        self.running_reward = 0
        self.episode_reward = 0  # will get reset every episode 
        self.episode_count = 0
        self.optimizer = keras.optimizers.Adam(learning_rate=.01)
        self.huber_loss = keras.losses.Huber()
        self.eps = np.finfo(np.float32).eps.item()
        self.num_actions = 6
        self.gamma = .95
        # self._init_model()
        self.last_action = ""
        self.moved_closer = None

    def _init_model(self):
        self.num_inputs = 4
        self.num_hidden = 128
        inputs = layers.Input(shape=(self.num_inputs,))
        common = layers.Dense(self.num_hidden, activation="relu")(inputs)
        action = layers.Dense(self.num_actions, activation="softmax")(common)
        critic = layers.Dense(1)(common)
        self.model = keras.Model(inputs=inputs, outputs=[action, critic])

    def _hit(self, num_hit_actions, action, game_ball:Ball): 
        assert action in self._hit_actions
        coords = np.linspace(0, 5, num_hit_actions + 1) # to create num_hit_action intervals
        # print(coords)
        curAction = self._hit_actions[0]
        for i in range(1, len(coords)): 
            lat1, lat2 = coords[i-1], coords[i]
            self._hit_spaces[curAction] = (lat1, lat2)
            curAction += 1
        # print(self._hit_spaces)

        # now for the hit logic
        aimCoords = self._hit_spaces[action]

        newVelocity = self._defaultHit(aimCoords[0], aimCoords[1], game_ball=game_ball)

        game_ball.setVelocity(newVelocity=newVelocity)        

        #TODO: Reset temporal latency somewhere: unless I decide to scrap

    # TODO: negative reward for moving away from ball laterally
    def _RLMove(self, action, game_ball:Ball):
        reward = MOVE_CORRECTLY_REWARD
        assert action in self._move_actions
        self.moved_closer = True
        if action == 0: 
            # move left
            newLateral = self.position["lateral"] - self.maximum_velocity * self.t
            if game_ball._position["lateral"] > self.position["lateral"]: 
                reward = 0
                # self.moved_closer = False
            self._move(newLateral)
        elif action == 1: 
            # move right
            newLateral = self.position["lateral"] + self.maximum_velocity * self.t
            if game_ball._position["lateral"] < self.position["lateral"]: 
                reward = 0
                # self.moved_closer = False
            self._move(newLateral)
        elif action == 2: 
            # stay put
            # self.moved_closer = False
            reward = 0
        return reward

    def performAction(self, game_ball:Ball, state, force=None): 

        if (self.last_action == HIT):
            reward = HIT_REWARD
            self.rewards_history.append(reward)
            self.episode_reward += reward
            self.last_action = ""  # reset

        if (self.last_action == MOVE):
            reward = MOVE_CORRECTLY_REWARD
            # if self.moved_closer == True: 
            #     reward = MOVE_CORRECTLY_REWARD
            # else: 
            #     # reward = -1 * MOVE_CORRECTLY_REWARD
            #     reward = 0  # don't punish staying still
            self.rewards_history.append(reward)
            self.episode_reward += reward
            self.last_action = ""  # reset


        # assert len(self.actions_probs_history) == len(self.critic_value_history)
        # assert len(self.critic_value_history) == len(self.rewards_history)
        state = tf.convert_to_tensor(state)
        state = tf.expand_dims(state, 0)
        # print(state)

        action_probs, critical_value = self.model(state)

        self.critic_value_history.append(critical_value[0, 0])

        action = np.random.choice(self.num_actions, p=np.squeeze(action_probs))
        self.actions_probs_history.append(tf.math.log(action_probs[0, action]))

        reward = 0
        if action in self._hit_actions: 
            # check if it is a valid hit
            # within_depth_tolerance = True if self.position["depth"] - game_ball._position["depth"] < self.depth_tolerance else False

            depth_dist = self.position["depth"] - game_ball._position["depth"]
            within_depth_tolerance = depth_dist > 0 and depth_dist < self.depth_tolerance
            within_lateral_tolerance = True if abs(game_ball._position["lateral"] - self.position["lateral"]) < self.lateral_tolerance else False
            if (within_depth_tolerance and within_lateral_tolerance): 
                # and self.position["depth"] - game_ball._position["depth"] <= 0
                self._hit(len(self._hit_actions), action, game_ball=game_ball)
                self.last_action = HIT
                return HIT
            else: 
                # reward = 0  # you are swinging at air
                # self.rewards_history.append(reward)
                # self.episode_reward += reward
                self.last_action = MOVE
                self.moved_closer = False
                
        # mutually exclusive
        if action in self._move_actions:
            reward = self._RLMove(action, game_ball)
            self.last_action = MOVE

        # have to wait to see how the game turns out for the reward associated with the hit

        # self.rewards_history.append(reward)
        # self.episode_reward += reward

        return MOVE

    def endOfRally(self, i_won_rally):
        # print(tape)
        # one last reward based on who won/lost
        reward = 0
        if self.last_action == HIT:
            # finally assign the reward
            if i_won_rally: 
                reward = WIN_REWARD
            else: 
                reward = HIT_REWARD


        if self.last_action == MOVE:
            if not i_won_rally: 
                reward = WRONG_MOVE_REWARD  # wrong move
            else: 
                # means other player hit it out of bounds
                reward = 0   # no reward

        self.last_action = ""
        self.rewards_history.append(reward)
        self.episode_reward += reward

        # running_reward = .05 * self.episode_reward + (1 - .05) * running_reward
    
    def endOfEpisode(self, tape):
        # print("Checking if these are equal.....\n")
        # print("Size of Reward History: ", len(self.rewards_history))
        # print("Size of action probs History: ", len(self.actions_probs_history))
        # print("Size of critic value History: ", len(self.critic_value_history))
        assert len(self.actions_probs_history) == len(self.critic_value_history)
        assert len(self.critic_value_history) == len(self.rewards_history)



        print("The reward for this game: ", self.episode_reward)

        returns = []
        discounted_sum = 0
        for r in self.rewards_history[::-1]:
            discounted_sum = r + self.gamma * discounted_sum
            returns.insert(0, discounted_sum)
        returns = np.array(returns)
        returns = (returns - np.mean(returns)) / (np.std(returns) + self.eps)
        returns = returns.tolist()

        # Calculating loss values to update our network
        history = zip(self.actions_probs_history, self.critic_value_history, returns)
        actor_losses = []
        critic_losses = []
        for log_prob, value, ret in history:
            # At this point in history, the critic estimated that we would get a
            # total reward = `value` in the future. We took an action with log probability
            # of `log_prob` and ended up recieving a total reward = `ret`.
            # The actor must be updated so that it predicts an action that leads to
            # high rewards (compared to critic's estimate) with high probability.
            diff = ret - value
            actor_losses.append(-log_prob * diff)  # actor loss

            # The critic must be updated so that it predicts a better estimate of
            # the future rewards.
            critic_losses.append(
                self.huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))
            )

        # Backpropagation
        loss_value = sum(actor_losses) + sum(critic_losses)
        grads = tape.gradient(loss_value, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

        # Clear the loss and reward history
        self.actions_probs_history.clear()
        self.critic_value_history.clear()
        self.rewards_history.clear()
        # RESET
        self.episode_reward = 0  

#EOF