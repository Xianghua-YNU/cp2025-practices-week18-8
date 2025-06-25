import random
import math

def buffon_needle(n):
    hits = 0
    # 假设平行线间距为 1，针长也为 1
    for _ in range(n):
        # 针的中点与最近平行线的距离
        d = random.uniform(0, 0.5)  
        # 针与平行线的夹角
        theta = random.uniform(0, math.pi)  
        if d <= 0.5 * math.sin(theta):
            hits += 1
    if hits == 0:
        return 0
    return 2 * n / hits

# 不同实验次数
experiment_counts = [1000, 10000, 100000, 1000000]
for count in experiment_counts:
    pi_estimate = buffon_needle(count)
    print(f"实验次数: {count}, 估计的π值: {pi_estimate}")

