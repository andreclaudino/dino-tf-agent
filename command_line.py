import dino_ia.server
import numpy as np
from time import sleep

if __name__ == '__main__':
    # environment = dino_ia.server.start()
    environment = dino_ia.server.socket.enviroment

    time_step = environment.reset()
    print(time_step)
    cumulative_reward = time_step.reward

    for _ in range(1000):
        time_step = environment.step(np.random.randint(-1, 1))
        print(time_step)
        cumulative_reward += time_step.reward

    sleep(1000)
