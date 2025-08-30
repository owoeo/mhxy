from mouse_mover import move_mouse_humanly
import pyautogui

# 获取起点和终点
start_point = pyautogui.position()
end_point = (800, 600)

# 调用函数
move_mouse_humanly(start_point, end_point, (0.001, 0.003))

