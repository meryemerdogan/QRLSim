from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env

from qrlsim.aqm_envs.MM1_env import MM1Env

def main():
    # Vectorized env (DQN can use 1 env, not many)
    vec_env = make_vec_env(MM1Env, n_envs=1, seed=42)

    model = DQN(
        policy="MlpPolicy",
        env=vec_env,
        verbose=1,
        tensorboard_log="./tensorboard_logs/mm1_dqn/",
        learning_rate=1e-3,
        buffer_size=50_000,
        learning_starts=1_000,
        batch_size=64,
        gamma=0.99,
        exploration_fraction=0.2,
        exploration_final_eps=0.05,
        target_update_interval=500,
    )

    model.learn(total_timesteps=200_000,tb_log_name="run1")
    model.save("dqn_mm1_queue")

    print("DQN training complete!")


if __name__ == "__main__":
    main()
