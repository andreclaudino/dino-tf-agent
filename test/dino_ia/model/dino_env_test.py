from time import sleep

from tf_agents.environments import utils as env_utils

from dino_ia.model.dino_env import DinoEnv


class TestDinoEnv:

    def test_step(self):
        environment = DinoEnv()
        sleep(1)
        env_utils.validate_py_environment(environment, episodes=3000)
