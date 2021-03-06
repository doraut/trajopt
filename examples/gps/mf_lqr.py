import gym
from trajopt.gps import MFGPS

import warnings
warnings.filterwarnings("ignore")


# lqr task
env = gym.make('LQR-TO-v0')
env._max_episode_steps = 100000

env_sigma = env.unwrapped._sigma
state = env.reset()

init_state = tuple([state, env_sigma])

alg = MFGPS(env, nb_steps=60,
            kl_bound=5.,
            init_state=init_state,
            init_action_sigma=100.)

# run gps
trace = alg.run(nb_episodes=25, nb_iter=10, verbose=True)

# plot dists
alg.plot()

# execute and plot
data = alg.sample(25, stoch=False)

import matplotlib.pyplot as plt

plt.figure()
for k in range(alg.dm_state):
    plt.subplot(alg.dm_state + alg.dm_act, 1, k + 1)
    plt.plot(data['x'][k, ...])

for k in range(alg.dm_act):
    plt.subplot(alg.dm_state + alg.dm_act, 1, alg.dm_state + k + 1)
    plt.plot(data['u'][k, ...])

plt.show()

# plot objective
plt.figure()
plt.plot(trace)
plt.show()
