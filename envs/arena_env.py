import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game.arena_game import ArenaGame

class ArenaEnv(gym.Env):
    def __init__(self, render_mode=False):
        super().__init__()
        self.render_mode = render_mode
        self.game = ArenaGame(render_mode=self.render_mode)

        # Observation: [x_pnj, y_pnj, x_player, y_player, hp_pnj, hp_player]
        self.observation_space = spaces.Box(low=0, high=1000, shape=(6,), dtype=np.float32)

        # Action: 0=stay, 1=forward, 2=turn_left, 3=turn_right, 4=attack, 5=flee
        self.action_space = spaces.Discrete(6)

    def reset(self, seed=None, options=None):
        self.game.reset()
        obs = self.game.get_observation()
        return np.array(obs, dtype=np.float32), {}

    def step(self, action):
        reward, done = self.game.step(action)
        obs = self.game.get_observation()
        return np.array(obs, dtype=np.float32), reward, done, False, {}

    def render(self):
        if self.render_mode:
            self.game.render()

    def close(self):
        self.game.close()
