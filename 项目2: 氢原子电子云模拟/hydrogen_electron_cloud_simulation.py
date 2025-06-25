import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class HydrogenAtomSimulator:
    def __init__(self):
        # 物理常数
        self.a = 5.29e-2  # 玻尔半径 (nm)
        self.D_max = 1.1  # 最大概率密度
        self.r0 = 0.25    # 收敛半径 (nm)
    
    def probability_density(self, r):
        """计算氢原子基态电子概率密度"""
        return (4 * r**2 / self.a**3) * np.exp(-2 * r / self.a)
    
    def simulate_electron_cloud(self, num_points=10000, r_max=1.0):
        """
        模拟氢原子电子云
        参数:
            num_points: 要生成的电子位置数量
            r_max: 最大考虑半径(nm)
        返回:
            points: 电子位置的3D坐标数组
        """
        points = []
        generated = 0
        
        print("开始模拟电子云...")
        while generated < num_points:
            # 在球坐标系中随机生成点
            r = np.random.uniform(0, r_max)
            theta = np.random.uniform(0, np.pi)
            phi = np.random.uniform(0, 2 * np.pi)
            
            # 计算该半径处的概率密度
            D = self.probability_density(r)
            D_normalized = D / self.D_max  # 归一化到[0,1]
            
            # 接受-拒绝采样
            if np.random.random() < D_normalized:
                # 转换为笛卡尔坐标
                x = r * np.sin(theta) * np.cos(phi)
                y = r * np.sin(theta) * np.sin(phi)
                z = r * np.cos(theta)
                points.append([x, y, z])
                generated += 1
                
                # 进度显示
                if generated % 1000 == 0:
                    print(f"已生成 {generated}/{num_points} 个电子位置")
        
        print("模拟完成!")
        return np.array(points)
    
    def plot_electron_cloud(self, points):
        """可视化电子云"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制电子位置
        ax.scatter(points[:,0], points[:,1], points[:,2], 
                   s=1, alpha=0.3, c='blue')
        
        # 设置坐标轴
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_zlabel('Z (nm)')
        ax.set_title('氢原子基态电子云分布')
        
        # 等比例缩放
        max_range = np.max(np.abs(points))
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)
        
        plt.tight_layout()
        plt.show()
    
    def plot_radial_density(self):
        """绘制径向概率密度函数"""
        r_values = np.linspace(0, 1.0, 500)
        D_values = self.probability_density(r_values)
        
        plt.figure(figsize=(8, 6))
        plt.plot(r_values, D_values, 'b-', linewidth=2)
        plt.axvline(self.r0, color='r', linestyle='--', label=f'收敛半径 r0={self.r0}nm')
        plt.axhline(self.D_max, color='g', linestyle='--', label=f'最大密度 D_max={self.D_max}')
        
        plt.xlabel('半径 r (nm)')
        plt.ylabel('概率密度 D(r)')
        plt.title('氢原子基态电子径向概率密度分布')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def parameter_analysis(self):
        """分析不同参数对电子云分布的影响"""
        # 不同玻尔半径的影响
        a_values = [self.a, self.a*0.8, self.a*1.2]  # 原始值、减小20%、增大20%
        r_values = np.linspace(0, 0.5, 300)
        
        plt.figure(figsize=(10, 6))
        for a_val in a_values:
            D = (4 * r_values**2 / a_val**3) * np.exp(-2 * r_values / a_val)
            plt.plot(r_values, D, label=f'a = {a_val:.3f} nm')
        
        plt.xlabel('半径 r (nm)')
        plt.ylabel('概率密度 D(r)')
        plt.title('不同玻尔半径对电子概率密度的影响')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    simulator = HydrogenAtomSimulator()
    
    while True:
        print("\n氢原子电子云模拟程序")
        print("1. 模拟电子云")
        print("2. 查看径向概率密度")
        print("3. 参数影响分析")
        print("4. 退出程序")
        
        choice = input("请选择功能(1/2/3/4): ")
        
        if choice == '1':
            try:
                num_points = int(input(f"请输入要模拟的电子数量(默认10000): ") or "10000")
                r_max = float(input(f"请输入最大半径(nm, 默认1.0): ") or "1.0")
                
                points = simulator.simulate_electron_cloud(num_points, r_max)
                simulator.plot_electron_cloud(points)
            except ValueError:
                print("输入无效，请重新输入数字")
        
        elif choice == '2
