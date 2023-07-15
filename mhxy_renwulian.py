from mhxy import *


class TaskLink:

    def moveToLuXiaoRan(self):
        # 打开大地图
        cooldown(0.5)
        posBigMap = (frame.left + relativeX2Act(1),
                     frame.top + relativeY2Act(2))
        print("click bigMap", posBigMap)
        pyautogui.leftClick(posBigMap[0],
                            posBigMap[1])
        cooldown(0.5)
        # 选择东海湾
        # 点击东海湾
        collect = pyautogui.locateCenterOnScreen(r'resources/tasklink/' + route + 'chang_shou.png',  # collect_caiji
                                                 region=(frame.left, frame.top, frame.right, frame.bottom),
                                                 confidence=0.9)
        if collect is not None:
            pyautogui.leftClick(collect.x, collect.y)

        cooldown(0.5)
        # 打开小地图
        posSmallMap = (frame.left + relativeX2Act(3.5),
                       frame.top + relativeY2Act(2))
        pyautogui.leftClick(posSmallMap[0],
                            posSmallMap[1])
        # 点击云乐游
        cooldown(0.5)
        position = Util.locateCenterOnScreen(r'resources/tasklink/' + route + 'lu_xiaoran.png')
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            cooldown(10)

    def taskLink(self):
        print('------开始经验任务链--------')
        closePopupWindow()

        self.moveToLuXiaoRan()

        clickIconPicIfExist(r'resources/tasklink/' + route + 'getTaskLink.png')
        clickIconPicIfExist(r'resources/tasklink/' + route + 'accept.png')
        clickIconPicIfExist(r'resources/mijing/' + route + 'confirmMijing.png')
        clickIconPicIfExist(r'resources/tasklink/' + route + 'lu_dialog.png')

        t = datetime.datetime.now().timestamp()
        while True:
            cooldown(1)
            closePopupWindow()
            pic = r'resources/tasklink/' + route + 'jingyanlian.png'
            create_team = pyautogui.locateCenterOnScreen(pic,  # collect_caiji
                                                         region=(frame.left, frame.top, frame.right, frame.bottom),
                                                         confidence=0.8)
            print("点击-" + str(pic) + "-位置：", create_team)
            if create_team is not None:
                pyautogui.leftClick(create_team.x, create_team.y)
                t = datetime.datetime.now().timestamp()
            clickIconPicIfExist(r'resources/tasklink/' + route + 'getTaskLink.png')
            clickIconPicIfExist(r'resources/tasklink/' + route + 'battle.png')
            clickIconPicIfExist(r'resources/tasklink/' + route + 'buy_baobao.png')
            clickIconPicIfExist(r'resources/tasklink/' + route + 'jiao_baobao.png')
            t2 = datetime.datetime.now().timestamp()
            # 超过三分钟没有检测到任务，停止循环
            if t2 - t > 60 * 3:
                print('停止经验链任务')
                break
        print('------经验任务链结束--------')


# 大窗口
if __name__ == '__main__':
    pyautogui.PAUSE = 0.5
    print("start task....")
    init()
    TaskLink().taskLink()
