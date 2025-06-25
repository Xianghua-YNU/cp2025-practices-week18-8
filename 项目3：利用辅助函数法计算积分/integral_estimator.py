import numpy as np

# 参数设置
N = 1000000  # 样本数

# 生成随机数
u = np.random.rand(N)
x = u**2  # 逆变换采样

# 计算被积函数值
f = 2 / (np.exp(x) + 1)

# 计算积分估计
I_estimate = np.mean(f)

# 计算统计误差
f_squared = f**2
var_f = np.mean(f_squared) - np.mean(f)**2
error = np.sqrt(var_f / N)

print(f"积分估计值: {I_estimate:.6f}")
print(f"统计误差: {error:.6f}")
