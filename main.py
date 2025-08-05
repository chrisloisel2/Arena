from envs.arena_env import ArenaEnv
import time

if __name__ == "__main__":
    env = ArenaEnv(render_mode=True)
    obs, _ = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()  # Action aléatoire
        obs, reward, done, _, _ = env.step(action)
        env.render()
        time.sleep(0.1)

    env.close()
    print("Game Over")
