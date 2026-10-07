"""自定义 manager-based Cartpole：调整奖励与重置分布，保留标准观测接口。"""
from isaaclab.utils import configclass
from isaaclab_tasks.manager_based.classic.cartpole.cartpole_env_cfg import CartpoleEnvCfg


@configclass
class ResearchCartpoleEnvCfg(CartpoleEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.rewards.pole_pos.weight = -2.0
        self.rewards.cart_vel.weight = -0.02
        self.events.reset_cart_position.params['position_range'] = (-1.5, 1.5)
        self.events.reset_pole_position.params['position_range'] = (-0.35, 0.35)
