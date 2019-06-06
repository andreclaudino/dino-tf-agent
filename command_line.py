import numpy as np

from dino_ia.environment.dino_enviroment import DinoEnv

if __name__ == '__main__':

    environment = DinoEnv()

    environment.serve()

    time_step = environment.reset()
    print(time_step)
    cumulative_reward = time_step.reward

    for _ in range(1000):
        time_step = environment.step(np.random.randint(-1, 1))
        print(time_step)
        cumulative_reward += time_step.reward
