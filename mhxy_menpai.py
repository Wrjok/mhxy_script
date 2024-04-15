from mhxy import *


class Menpai:
    def menpai(self):
        flag = True
        t = datetime.datetime.now().timestamp()
        while flag:
            # closePopupWindow()
            print("开始检查是否进入战斗--------")
            battle_flag = Util.locateCenterOnScreen(r'resources/menpai/battle.png')
            if battle_flag is None:
                clickIconPic(r'resources/menpai/task.png', 7)
                clickIconPic(r'resources/menpai/task.png', 7)
                clickIconPic(r'resources/menpai/enterBattle.png', 10)
            cooldown(8)
            t2 = datetime.datetime.now().timestamp()
            if t2 - t > 60*60:
                print("门店定时任务结束---------")
                flag = False

# 副本 进入第一个副本为起点
if __name__ == '__main__':
    pyautogui.PAUSE = 0.5
    print("start task....")
    init()
    Menpai().menpai()
