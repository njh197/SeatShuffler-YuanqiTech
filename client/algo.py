import random

def allocate_groups(n, m, pre_boys, pre_girls, total_boys, total_girls):
    """
    分配学生到各组，使男女比例差和人数差尽量小
    
    参数:
    n: 组数
    m: 每组最大容量列表
    pre_boys: 每组预分配男生数列表
    pre_girls: 每组预分配女生数列表
    total_boys: 总男生数
    total_girls: 总女生数
    
    返回:
    result: 列表，每个元素为(男生数, 女生数)的元组
    """
    
    # 1. 计算预分配后的剩余学生
    total_pre_boys = sum(pre_boys)
    total_pre_girls = sum(pre_girls)
    
    remaining_boys = total_boys - total_pre_boys
    remaining_girls = total_girls - total_pre_girls
    remaining_students = remaining_boys + remaining_girls
    
    # 计算每组预分配总人数和剩余容量
    pre_total = [pre_boys[i] + pre_girls[i] for i in range(n)]
    remaining_capacity = [m[i] - pre_total[i] for i in range(n)]
    
    # 2. 分配每组总人数（使每组总人数尽量平均）
    # 创建索引列表并按剩余容量排序
    indices = list(range(n))
    indices.sort(key=lambda i: remaining_capacity[i])
    
    # 使用二分查找找到最小的D
    low, high = 0, max(remaining_capacity)
    while low < high:
        mid = (low + high) // 2
        total_capacity = sum(min(remaining_capacity[i], mid) for i in indices)
        if total_capacity >= remaining_students:
            high = mid
        else:
            low = mid + 1
    
    D = low
    
    # 计算每组分配的剩余学生数
    s = [min(remaining_capacity[i], D) for i in range(n)]
    
    # 调整超额分配
    total_s = sum(s)
    if total_s > remaining_students:
        excess = total_s - remaining_students
        # 从容量较大的组开始减少分配
        for i in reversed(indices):
            if s[i] > 0 and excess > 0:
                s[i] -= 1
                excess -= 1
                if excess == 0:
                    break
    
    # 计算每组总人数
    total_per_group = [pre_total[i] + s[i] for i in range(n)]
    
    # 3. 分配剩余男女生数量（使男女比例尽量接近全局比例）
    total_students = total_boys + total_girls
    global_ratio = total_boys / total_students if total_students > 0 else 0
    
    # 计算每组的目标男生数
    target_boys = []
    for i in range(n):
        ideal_total_boys = global_ratio * total_per_group[i]
        target_remaining_boys = ideal_total_boys - pre_boys[i]
        target_boys.append(target_remaining_boys)
    
    # 初始化剩余男生分配
    x = [0] * n
    for i in range(n):
        if target_boys[i] < 0:
            x[i] = 0
        elif target_boys[i] > s[i]:
            x[i] = s[i]
        else:
            x[i] = int(target_boys[i])
    
    # 调整男生分配
    current_boys = sum(x)
    K = remaining_boys - current_boys
    
    if K > 0:
        # 需要增加男生分配
        candidates = []
        for i in range(n):
            if x[i] < s[i] and target_boys[i] > x[i]:
                candidates.append((i, target_boys[i] - x[i]))
        
        candidates.sort(key=lambda item: item[1], reverse=True)
        
        for i in range(min(K, len(candidates))):
            idx = candidates[i][0]
            x[idx] += 1
    
    elif K < 0:
        # 需要减少男生分配
        candidates = []
        for i in range(n):
            if x[i] > 0 and target_boys[i] < x[i]:
                candidates.append((i, x[i] - target_boys[i]))
        
        candidates.sort(key=lambda item: item[1], reverse=True)
        
        for i in range(min(-K, len(candidates))):
            idx = candidates[i][0]
            x[idx] -= 1
    
    # 计算每组女生分配
    y = [s[i] - x[i] for i in range(n)]
    
    # 计算最终每组男生和女生数
    result = []
    for i in range(n):
        final_boys = pre_boys[i] + x[i]
        final_girls = pre_girls[i] + y[i]
        result.append((final_boys, final_girls))
    
    return result

def allocate_groups_separated(n, m, pre_boys, pre_girls, total_boys, total_girls):
    """
    分配学生到各组，使每组人数尽量平均，同时男女尽量分开
    
    参数:
    n: 组数
    m: 每组最大容量列表
    pre_boys: 每组预分配男生数列表
    pre_girls: 每组预分配女生数列表
    total_boys: 总男生数
    total_girls: 总女生数
    
    返回:
    result: 列表，每个元素为(男生数, 女生数)的元组
    """
    
    # 1. 计算预分配后的剩余学生
    total_pre_boys = sum(pre_boys)
    total_pre_girls = sum(pre_girls)
    
    remaining_boys = total_boys - total_pre_boys
    remaining_girls = total_girls - total_pre_girls
    remaining_students = remaining_boys + remaining_girls
    
    # 计算每组预分配总人数和剩余容量
    pre_total = [pre_boys[i] + pre_girls[i] for i in range(n)]
    remaining_capacity = [m[i] - pre_total[i] for i in range(n)]
    
    # 2. 分配每组总人数（使每组总人数尽量平均）
    # 创建索引列表并按剩余容量排序
    indices = list(range(n))
    indices.sort(key=lambda i: remaining_capacity[i])
    
    # 使用二分查找找到最小的D
    low, high = 0, max(remaining_capacity)
    while low < high:
        mid = (low + high) // 2
        total_capacity = sum(min(remaining_capacity[i], mid) for i in indices)
        if total_capacity >= remaining_students:
            high = mid
        else:
            low = mid + 1
    
    D = low
    
    # 计算每组分配的剩余学生数
    s = [min(remaining_capacity[i], D) for i in range(n)]
    
    # 调整超额分配
    total_s = sum(s)
    if total_s > remaining_students:
        excess = total_s - remaining_students
        # 从容量较大的组开始减少分配
        for i in reversed(indices):
            if s[i] > 0 and excess > 0:
                s[i] -= 1
                excess -= 1
                if excess == 0:
                    break
    
    # 计算每组总人数
    total_per_group = [pre_total[i] + s[i] for i in range(n)]
    
    # 3. 分配剩余男女生数量（使男女尽量分开）
    # 策略：尽量将男生集中到部分组，女生集中到另一部分组
    
    # 创建组索引列表，按预分配男生数排序（男生多的组优先分配男生）
    group_indices = list(range(n))
    group_indices.sort(key=lambda i: pre_boys[i], reverse=True)
    
    # 初始化剩余男生分配
    x = [0] * n
    
    # 计算每组可以分配的男生数上限（考虑容量和预分配）
    max_boys_per_group = [m[i] - pre_girls[i] for i in range(n)]
    
    # 分配男生：从预分配男生多的组开始，尽量分配男生
    remaining_boys_to_assign = remaining_boys
    for i in group_indices:
        if remaining_boys_to_assign <= 0:
            break
            
        # 该组最多能分配的男生数
        max_boys_here = min(s[i], max_boys_per_group[i] - pre_boys[i])
        
        # 分配尽可能多的男生到该组
        boys_to_assign = min(remaining_boys_to_assign, max_boys_here)
        x[i] = boys_to_assign
        remaining_boys_to_assign -= boys_to_assign
    
    # 如果还有剩余男生，尝试分配到其他组
    if remaining_boys_to_assign > 0:
        # 找出还能分配男生的组
        available_groups = []
        for i in range(n):
            if x[i] < s[i] and max_boys_per_group[i] - pre_boys[i] - x[i] > 0:
                available_groups.append(i)
        
        # 按剩余容量分配
        available_groups.sort(key=lambda i: max_boys_per_group[i] - pre_boys[i] - x[i], reverse=True)
        
        for i in available_groups:
            if remaining_boys_to_assign <= 0:
                break
                
            max_additional_boys = min(
                s[i] - x[i],  # 该组剩余可分配学生数
                max_boys_per_group[i] - pre_boys[i] - x[i]  # 该组剩余男生容量
            )
            
            additional_boys = min(remaining_boys_to_assign, max_additional_boys)
            x[i] += additional_boys
            remaining_boys_to_assign -= additional_boys
    
    # 分配女生
    y = [s[i] - x[i] for i in range(n)]
    
    # 检查女生分配是否超出容量
    for i in range(n):
        max_girls_here = m[i] - pre_boys[i] - x[i]
        if y[i] > max_girls_here:
            # 需要调整：将多余的女生转为男生
            excess_girls = y[i] - max_girls_here
            y[i] = max_girls_here
            x[i] += excess_girls
    
    # 计算最终每组男生和女生数
    result = []
    for i in range(n):
        final_boys = pre_boys[i] + x[i]
        final_girls = pre_girls[i] + y[i]
        result.append((final_boys, final_girls))
    
    return result

def allocate_groups_random(n, m, pre_boys, pre_girls, total_boys, total_girls):
    """
    分配学生到各组，使每组人数尽量平均，同时完全随机地分配不同性别
    
    参数:
    n: 组数
    m: 每组最大容量列表
    pre_boys: 每组预分配男生数列表
    pre_girls: 每组预分配女生数列表
    total_boys: 总男生数
    total_girls: 总女生数
    
    返回:
    result: 列表，每个元素为(男生数, 女生数)的元组
    """
    
    # 1. 计算预分配后的剩余学生
    total_pre_boys = sum(pre_boys)
    total_pre_girls = sum(pre_girls)
    
    remaining_boys = total_boys - total_pre_boys
    remaining_girls = total_girls - total_pre_girls
    remaining_students = remaining_boys + remaining_girls
    
    # 计算每组预分配总人数和剩余容量
    pre_total = [pre_boys[i] + pre_girls[i] for i in range(n)]
    remaining_capacity = [m[i] - pre_total[i] for i in range(n)]
    
    # 2. 分配每组总人数（使每组总人数尽量平均）
    # 创建索引列表并按剩余容量排序
    indices = list(range(n))
    indices.sort(key=lambda i: remaining_capacity[i])
    
    # 使用二分查找找到最小的D
    low, high = 0, max(remaining_capacity)
    while low < high:
        mid = (low + high) // 2
        total_capacity = sum(min(remaining_capacity[i], mid) for i in indices)
        if total_capacity >= remaining_students:
            high = mid
        else:
            low = mid + 1
    
    D = low
    
    # 计算每组分配的剩余学生数
    s = [min(remaining_capacity[i], D) for i in range(n)]
    
    # 调整超额分配
    total_s = sum(s)
    if total_s > remaining_students:
        excess = total_s - remaining_students
        # 从容量较大的组开始减少分配
        for i in reversed(indices):
            if s[i] > 0 and excess > 0:
                s[i] -= 1
                excess -= 1
                if excess == 0:
                    break
    
    # 计算每组总人数
    total_per_group = [pre_total[i] + s[i] for i in range(n)]
    
    # 3. 完全随机地分配剩余男女生数量
    # 创建一个包含所有剩余学生的列表，1代表男生，0代表女生
    all_students = [1] * remaining_boys + [0] * remaining_girls
    
    # 随机打乱学生列表
    random.shuffle(all_students)
    
    # 分配学生到各组
    x = [0] * n  # 每组分配的男生数
    y = [0] * n  # 每组分配的女生数
    
    index = 0
    for i in range(n):
        # 为第i组分配s[i]个学生
        for j in range(s[i]):
            if index < len(all_students):
                if all_students[index] == 1:
                    x[i] += 1
                else:
                    y[i] += 1
                index += 1
    
    # 计算最终每组男生和女生数
    result = []
    for i in range(n):
        final_boys = pre_boys[i] + x[i]
        final_girls = pre_girls[i] + y[i]
        result.append((final_boys, final_girls))
    
    return result

# 示例用法
if __name__ == "__main__":
    n = 6
    m = [5,6,5,5,6,5]
    pre_boys = [1,0,0,0,0,1]
    pre_girls = [0,0,1,0,0,0]
    total_boys = 13
    total_girls = 14
    for func in [allocate_groups,allocate_groups_separated,allocate_groups_random]:
        result = func(n, m, pre_boys, pre_girls, total_boys, total_girls)
        for i, (boys, girls) in enumerate(result):
            print(f"(Team{i+1}): {boys}(B)+{girls}(G)={boys+girls}/{m[i]}")
        print('\n')
