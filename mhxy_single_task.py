from mhxy_baotu import *
from mhxy_yabiao import *
from mhxy_mijing import *

# 单人任务一条龙
if __name__ == '__main__':
    input_out = input("角色等级？0：89，1：69。请输入：")
    # # pyautogui.PAUSE = 1
    levelType = int(input_out)
    print("请手动激活窗口（10秒内）")
    time.sleep(10)
    print("start task....")
    init()
    Baotu().baotu()
    Yabiao().yabiao()
    Mijing().mijing(levelType)

