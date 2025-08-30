from abc import ABC, abstractmethod
import pyautogui

class MouseAdapter(ABC):
    @abstractmethod
    def moveTo(self, x, y, duration=0.0):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def position(self):
        pass

class PyAutoGUIAdapter(MouseAdapter):
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.0001

    def moveTo(self, x, y, duration=0.0):
        pyautogui.moveTo(x, y, duration=duration)

    def size(self):
        return pyautogui.size()

    def position(self):
        return pyautogui.position()
