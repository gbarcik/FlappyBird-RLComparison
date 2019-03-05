import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"

import gym
import gym_flappy_bird
import os
import matplotlib.pyplot as plt
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import CnnPolicy
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines import DQN
from stable_baselines import ACER
import numpy as np
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines.common.vec_env import VecVideoRecorder, DummyVecEnv

best_mean_reward, n_steps = -np.inf, 0



# Create log dir
log_dir = "/tmp/gym/"
os.makedirs(log_dir, exist_ok=True)


env = gym.make('flappy-bird-v0')
# Logs will be saved in log_dir/monitor.csv
env = Monitor(env, log_dir, allow_early_resets=True)
env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run

#model = PPO2(MlpPolicy, env, verbose=1)
#model = DQN(MlpPolicy, env, verbose=1)
model = ACER(MlpPolicy, env, verbose=1,  tensorboard_log = './tmp/flappy_bird')
model.learn(total_timesteps=4000)

'''
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
'''

def movingAverage(values, window):
    """
    Smooth values by doing a moving average
    :param values: (numpy array)
    :param window: (int)
    :return: (numpy array)
    """
    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, 'valid')


def plot_results(log_folder, title='Learning Curve'):
    """
    plot the results

    :param log_folder: (str) the save location of the results to plot
    :param title: (str) the title of the task to plot
    """
    x, y = ts2xy(load_results(log_folder), 'timesteps')
    

    y = movingAverage(y, window=50)# window = 50
    # Truncate x
    print('x', x)
    x = x[len(x) - len(y):]

    fig = plt.figure(title)
    print('x', x)
    print('y', y)

    plt.plot(x, y)
    plt.xlabel('Number of Timesteps')
    plt.ylabel('Rewards')
    plt.title(title + " Smoothed")
    plt.show()


#plot_results(log_dir)

'''


## Save video

env_id = 'flappy-bird-v0'
video_folder = 'logs/videos/'
video_length = 100

env = DummyVecEnv([lambda: gym.make(env_id)])

obs = env.reset()

# Record the video starting at the first step
env = VecVideoRecorder(env, video_folder,
                       record_video_trigger=lambda x: x == 0, video_length=video_length,
                       name_prefix="random-agent-{}".format(env_id))

env.reset()
for _ in range(video_length + 1):
  action = [env.action_space.sample()]
  obs, _, _, _ = env.step(action)
env.close()


import imageio
import numpy as np

#from stable_baselines.common.policies import MlpPolicy
#from stable_baselines import A2C

#model = A2C(MlpPolicy, "LunarLander-v2").learn(100000)

images = []
obs = model.env.reset()
img = model.env.render(mode='rgb_array')
for i in range(350):
    images.append(img)
    action, _ = model.predict(obs)
    obs, _, _ ,_ = model.env.step(action)
    img = model.env.render(mode='rgb_array')

imageio.mimsave('flappy_bird.gif', [np.array(img[0]) for i, img in enumerate(images) if i%2 == 0], fps=29)





'''