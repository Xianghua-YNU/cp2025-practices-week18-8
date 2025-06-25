import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

class NuclearReactionSimulator:
    def __init__(self, size=100, num_neutrons=50, fission_prob=0.8, 
                 absorption_prob=0.15, reproduction_factor=2.5):
        # 模拟参数设置
        self.size = size  # 模拟区域大小
        self.num_neutrons = num_neutrons  # 初始中子数
        self.fission_prob = fission_prob  # 裂变概率
        self.absorption_prob = absorption_prob  # 吸收概率
        self.reproduction_factor = reproduction_factor  # 平均每次裂变产生的中子数
        
        # 初始化网格和中子
        self.grid = np.zeros((size, size))  # 网格表示模拟区域
        self.neutrons = []  # 当前中子位置列表
        self.initialize_simulation()
        
        # 用于跟踪模拟统计数据
        self.neutron_counts = [num_neutrons]
        self.time_steps = [0]
    
    def initialize_simulation(self):
        """初始化模拟：在中心区域随机放置初始中子"""
        center = self.size // 2
        radius = self.size // 10
        
        for _ in range(self.num_neutrons):
            # 在中心区域随机生成中子位置
            while True:
                x = np.random.randint(center-radius, center+radius)
                y = np.random.randint(center-radius, center+radius)
                if 0 <= x < self.size and 0 <= y < self.size:
                    self.neutrons.append((x, y))
                    break
    
    def simulate_step(self):
        """模拟一个时间步的链式反应过程"""
        new_neutrons = []
        reactions = 0
        
        # 处理每个中子
        for x, y in self.neutrons:
            # 中子移动到相邻位置
            dx, dy = np.random.choice([-1, 0, 1], 2)
            new_x, new_y = x + dx, y + dy
            
            # 检查是否在模拟区域内
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                # 模拟反应过程
                rand = np.random.random()
                
                if rand < self.fission_prob:
                    # 发生裂变，产生新中子
                    reactions += 1
                    num_new = np.random.poisson(self.reproduction_factor)
                    for _ in range(num_new):
                        # 新中子随机放置在裂变位置附近
                        fx = new_x + np.random.randint(-2, 3)
                        fy = new_y + np.random.randint(-2, 3)
                        if 0 <= fx < self.size and 0 <= fy < self.size:
                            new_neutrons.append((fx, fy))
                elif rand < self.fission_prob + self.absorption_prob:
                    # 被吸收，中子消失
                    pass
                else:
                    # 散射，中子继续存在
                    new_neutrons.append((new_x, new_y))
        
        # 更新网格和统计数据
        self.grid = np.zeros((self.size, self.size))
        for x, y in new_neutrons:
            self.grid[x, y] += 1
        
        self.neutrons = new_neutrons
        self.neutron_counts.append(len(new_neutrons))
        self.time_steps.append(self.time_steps[-1] + 1)
        
        return reactions
    
    def run_simulation(self, num_steps=100):
        """运行完整的模拟过程"""
        for _ in range(num_steps):
            reactions = self.simulate_step()
            # 如果中子数为0，终止模拟
            if len(self.neutrons) == 0:
                break
    
    def visualize_simulation(self):
        """可视化模拟结果"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 创建自定义颜色映射
        colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]  # 黑色 -> 红色 -> 黄色
        cmap = LinearSegmentedColormap.from_list('neutron_cmap', colors, N=100)
        
        # 可视化中子分布
        im = ax1.imshow(self.grid, cmap=cmap, interpolation='nearest', 
                        vmin=0, vmax=5)
        ax1.set_title('中子分布')
        ax1.set_xlabel('X坐标')
        ax1.set_ylabel('Y坐标')
        fig.colorbar(im, ax=ax1, label='中子数')
        
        # 可视化中子数量随时间的变化
        ax2.plot(self.time_steps, self.neutron_counts, 'b-', linewidth=2)
        ax2.set_title('中子数量随时间变化')
        ax2.set_xlabel('时间步')
        ax2.set_ylabel('中子数')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, num_steps=50):
        """创建模拟动画"""
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title('链式反应模拟')
        
        # 创建自定义颜色映射
        colors = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]  # 黑色 -> 红色 -> 黄色
        cmap = LinearSegmentedColormap.from_list('neutron_cmap', colors, N=100)
        
        im = ax.imshow(self.grid, cmap=cmap, interpolation='nearest', 
                      vmin=0, vmax=5)
        ax.set_xlabel('X坐标')
        ax.set_ylabel('Y坐标')
        fig.colorbar(im, ax=ax, label='中子数')
        
        def update(frame):
            self.simulate_step()
            im.set_data(self.grid)
            ax.set_title(f'链式反应模拟 - 时间步: {frame+1}, 中子数: {len(self.neutrons)}')
            return im,
        
        ani = FuncAnimation(fig, update, frames=num_steps, interval=200, 
                           blit=True, repeat=False)
        
        plt.tight_layout()
        plt.show()
        
        return ani

# 运行模拟示例
if __name__ == "__main__":
    # 参数设置
    size = 100  # 模拟区域大小
    initial_neutrons = 50  # 初始中子数
    fission_prob = 0.8  # 裂变概率
    absorption_prob = 0.15  # 吸收概率
    reproduction_factor = 2.5  # 每次裂变产生的平均中子数
    
    # 创建并运行模拟
    simulator = NuclearReactionSimulator(
        size=size, 
        num_neutrons=initial_neutrons,
        fission_prob=fission_prob,
        absorption_prob=absorption_prob,
        reproduction_factor=reproduction_factor
    )
    
    # 可视化模拟过程
    simulator.create_animation(num_steps=50)
    
    # 或者只显示最终结果
    # simulator.run_simulation(num_steps=50)
    # simulator.visualize_simulation()
