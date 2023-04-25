# env_setup.py
import os
import numpy as np
import gym
import time
import retro
import subprocess
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.vec_env import SubprocVecEnv


def import_rom(roms_directory="ROM/"):
    subprocess.run(["python3", "-m", "retro.import", roms_directory])

class CustomWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(256, 200, 3), dtype=np.uint8)

    def observation(self, observation):
        return np.transpose(observation, (1, 0, 2))
    
    def action(self, action):
        # The action passed to the environment should be an array of length equal to the number of buttons
        num_buttons = self.env.num_buttons
        return np.array(action).reshape(-1, num_buttons)
    
class CustomVecTransposeImage(VecTransposeImage):
    def transpose_image(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            return np.transpose(image, (2, 0, 1))
        elif len(image.shape) == 4:
            return np.transpose(image, (0, 3, 1, 2))
        else:
            raise ValueError(f"Unsupported image shape: {image.shape}")

def create_env():
    game = "StreetFighterIISpecialChampionEdition-Genesis"
    scenario = "scenario"

    import_rom()

    try:
        env = retro.make(game, scenario=scenario)
        # env.frameskip = 3

    except gym.error.Error:
        print(f"{game} is not available. Please make sure the ROM is in the specified directory.")
        exit()

    env = CustomWrapper(env)
    env = DummyVecEnv([lambda: env])  # Wrap the environment in a DummyVecEnv first
    env = CustomVecTransposeImage(env)  # Then apply the CustomVecTransposeImage wrapper

    return env


if __name__ == "__main__":
    env = create_env()
    obs = env.reset()

    for _ in range(1000):
        env.render()
        action = [env.action_space.sample()]  # Wrap the action in a list
        obs, reward, done, info = env.step(action)
        time.sleep(0.01)

    print("Environment created successfully.")