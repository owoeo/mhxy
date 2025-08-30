from mouse_adapter import PyAutoGUIAdapter, MouseAdapter
import pyautogui
import random
import time
import math

def _generate_bezier_points(start_point, end_point, num_points=60):
    """为两个点生成一条贝塞尔曲线"""
    start_x, start_y = start_point
    end_x, end_y = end_point

    dist = math.hypot(end_x - start_x, end_y - start_y)
    offset_magnitude = min(dist / 3.0, 150)

    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    ctrl1_x = mid_x + random.uniform(-offset_magnitude, offset_magnitude)
    ctrl1_y = mid_y + random.uniform(-offset_magnitude, offset_magnitude)
    
    ctrl2_x = mid_x + random.uniform(-offset_magnitude, offset_magnitude)
    ctrl2_y = mid_y + random.uniform(-offset_magnitude, offset_magnitude)

    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = ( (1 - t)**3 * start_x + 
              3 * (1 - t)**2 * t * ctrl1_x + 
              3 * (1 - t) * t**2 * ctrl2_x + 
              t**3 * end_x )
        y = ( (1 - t)**3 * start_y + 
              3 * (1 - t)**2 * t * ctrl1_y + 
              3 * (1 - t) * t**2 * ctrl2_y + 
              t**3 * end_y )
        points.append((int(x), int(y)))
    return points

def move_mouse_humanly(mouse_adapter: MouseAdapter, start_point, end_point, duration_range=(0.5, 1.5)):
    """
    模拟人类移动鼠标的轨迹，实现变速效果。

    参数:
    - mouse_adapter: 鼠标适配器实例
    - start_point (tuple): 开始点的坐标 (x, y)。
    - end_point (tuple): 结束点的坐标 (x, y)。
    - duration_range (tuple): 一个包含最小和最大移动时间的元组，将在范围内随机选择一个时长。
    """
    
    start_x, start_y = start_point
    end_x, end_y = end_point
    
    # --- 1. 开始移动前的轻微抖动 ---
    if random.random() < 0.6: # 60%的概率在开始时抖动
        for _ in range(random.randint(2, 4)):
            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-3, 3)
            mouse_adapter.moveTo(start_x + shake_x, start_y + shake_y)

    # --- 2. 生成移动路径 ---
    # 随机决定使用单段还是多段曲线
    if random.random() < 0.4: # 40% 的概率使用多段曲线
        # 在起点和终点之间创建一个或两个中间点
        num_intermediate = random.randint(1, 2)
        
        points = []
        last_point = start_point
        
        for i in range(num_intermediate):
            # 计算中间点的大致位置
            progress = (i + 1) / (num_intermediate + 1)
            intermediate_x_base = start_x + (end_x - start_x) * progress
            intermediate_y_base = start_y + (end_y - start_y) * progress
            
            # 为中间点增加随机偏移
            offset_x = random.uniform(-50, 50)
            offset_y = random.uniform(-50, 50)
            
            intermediate_point = (intermediate_x_base + offset_x, intermediate_y_base + offset_y)
            
            # 生成从上一个点到中间点的曲线
            segment_points = _generate_bezier_points(last_point, intermediate_point)
            points.extend(segment_points[:-1]) # 避免重复添加点
            last_point = intermediate_point
            
        # 添加最后一段，从最后一个中间点到终点
        points.extend(_generate_bezier_points(last_point, end_point))

    else: # 60% 的概率使用单段曲线
        points = _generate_bezier_points(start_point, end_point)

    # --- 3. 模拟移动 --- 
    total_duration = random.uniform(duration_range[0], duration_range[1])
    tween = pyautogui.easeInCubic
    start_time = time.time()

    for i, point in enumerate(points):
        # 避免除以零的错误
        if len(points) > 1:
            progress = i / (len(points) - 1)
        else:
            progress = 1.0

        # 应用缓动函数，计算出时间的“逻辑”进度
        tweened_progress = tween(progress)
        
        # 根据缓动后的进度，计算出当前步骤应该在何时完成
        target_time = start_time + tweened_progress * total_duration
        
        # 等待直到到达目标时间
        sleep_time = target_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        # 移动鼠标（无抖动）
        mouse_adapter.moveTo(point[0], point[1])

        # --- 新增：随机停顿 ---
        if random.random() < 0.01:  # 10%的概率进行一次短暂的停顿
            time.sleep(random.uniform(0.05, 0.15))
            
    # --- 4. 结束移动后的轻微抖动（模拟微调） ---
    if random.random() < 0.7: # 70%的概率在结束时抖动
        for _ in range(random.randint(2, 5)):
            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-3, 3)
            mouse_adapter.moveTo(end_x + shake_x, end_y + shake_y)


# --- 使用示例 ---
if __name__ == "__main__":
    print("脚本将在 1 秒后开始...")
    print("请将鼠标移动到屏幕左上角以紧急停止程序。")
    time.sleep(1)

    mouse = PyAutoGUIAdapter()

    screen_width, screen_height = mouse.size()
    print(f"你的屏幕分辨率是: {screen_width}x{screen_height}")

    try:
        # 示例 1: 从当前位置移动到屏幕中心
        current_pos = mouse.position()
        print(f"鼠标当前位置: {current_pos}")
        target_pos = (screen_width // 2, screen_height // 2)
        print(f"准备移动到屏幕中心: {target_pos}")
        move_mouse_humanly(mouse, current_pos, target_pos, duration_range=(0.3, 0.5))
        print("移动完成!")
        
        time.sleep(1)

        # 示例 2: 从中心移动到一个随机位置
        current_pos = mouse.position()
        random_target_x = random.randint(0, screen_width - 1)
        random_target_y = random.randint(0, screen_height - 1)
        print(f"准备从 {current_pos} 移动到一个随机位置: ({random_target_x}, {random_target_y})")
        move_mouse_humanly(mouse, current_pos, (random_target_x, random_target_y), duration_range=(1.0, 2.0))
        print("移动完成!")

    except pyautogui.FailSafeException:
        print("安全保护启动：程序已紧急停止。")
    except Exception as e:
        print(f"发生错误: {e}")