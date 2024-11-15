import numpy as np
import os
import robosuite as suite
from robosuite.wrappers import GymWrapper
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from robosuite.environments.manipulation.lift import Lift
from PointEnv import PointEnv

#register_env(GoToPointTask)

if __name__=="__main__":

    target_ee_position = np.array([0.3,0,0])

    env = PointEnv(
        robots="Panda",  
        has_renderer=False,  # Rn I unabled visual sim if its needed
        has_offscreen_renderer=False,
        use_camera_obs=False,
        reward_shaping=True  #  dense reward
    )
    env.set_target_position(target_ee_position)
    # Vectorize and Normalize Environment
    my_wrapped_env = GymWrapper(env)
    my_vec_env = DummyVecEnv([lambda: my_wrapped_env])
    my_vec_env = VecNormalize(my_vec_env, norm_obs=True, norm_reward=True)

    # Set up and train the PPO model
    file_path = "point_model.zip"
    if os.path.exists(file_path):
        print("Loading model")
        model = PPO.load("point_model")
        model.env = my_vec_env
    else:
        model = PPO(
            policy="MlpPolicy",      
            env=my_vec_env,          
            learning_rate=0.0003,   
            n_steps=3000,            
            batch_size=500,          
            verbose=1,                
            tensorboard_log='/home/fri/tb.log'
        )


    model.learn(
        total_timesteps=25000,  
        log_interval=1
    )

    # Save the trained model
    model.save("point_model")
