import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from qrlsim.aqm_envs.MM1_env import MM1Env

def main():
    vec_env = make_vec_env(MM1Env, n_envs=8, seed=42)
    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=1,
        tensorboard_log="./tensorboard_logs/mm1_ppo/",
        learning_rate=3e-4,
        n_steps=256,
        batch_size=256,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
    )
    model.learn(total_timesteps=200_000,tb_log_name="run1")
    model.save("ppo_mm1_queue")

    print("Training done")

if __name__ == "__main__":
    main()