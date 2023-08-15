from mhxy import *


class Haidi:

    def haidi(self, chaseWin):
        # 流程任务 领取任务后起点
        print('-------开始召唤灵任务--------')
        t = datetime.datetime.now().timestamp()
        while True:
            cooldown(1)
            clickIconPicIfExist(r'resources/ghost/' + route + 'startGhost.png')
            clickIconPicIfExist(r'resources/fuben/' + route + 'fubenBattle1.png')
            clickIconPicIfExist(r'resources/fuben/' + route + 'fubenBattle2.png')
            t2 = datetime.datetime.now().timestamp()
            if t2 - t > 60 * 42:
                break
        print('-------结束召唤灵任务--------')


# 副本 进入第一个副本为起点
if __name__ == '__main__':
    pyautogui.PAUSE = 0.5
    print("start task....")
    init()
    Haidi().haidi((winRelativeX(-3), winRelativeY(6)))
