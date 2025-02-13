from mhxy import *


class Yabiao:

    def moveToBiaoTou(self):
        # 打开大地图
        cooldown(0.5)
        posBigMap = (frame.left + relativeX2Act(1),
                     frame.top + relativeY2Act(2))
        print("click bigMap", posBigMap)
        pyautogui.leftClick(posBigMap[0],
                            posBigMap[1])
        cooldown(0.5)
        # 选择长安城
        # 点击长安城
        Util.leftClick(13.4, 12.4)

        cooldown(0.5)
        # 打开小地图
        posSmallMap = (frame.left + relativeX2Act(3.5),
                       frame.top + relativeY2Act(2))
        pyautogui.leftClick(posSmallMap[0],
                            posSmallMap[1])
        # 点击镖头
        cooldown(0.5)
        position = Util.locateCenterOnScreen(r'resources/yabiao/' + route + 'biaotou.png')
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            cooldown(12)

    def yabiao(self):
        print('-----开始押镖流程-----')
        count = 0
        while count < 2:
            closePopupWindow()
            self.moveToBiaoTou()
            clickIconPicIfExist(r'resources/yabiao/' + route + 'normalYabiao.png')
            cooldown(0.5)
            clickIconPicIfExist(r'resources/yabiao/' + route + 'confirmYabiao.png')

            # 开始检查押镖任务是否做完
            cooldown(5)
            while True:
                cooldown(10)
                print("开始检查押镖任务是否完成------")
                closePopupWindow()
                battleFlag = Util.locateCenterOnScreen(r'resources/ghost/' + route + 'battleFlag2.png')
                # 押镖中
                yabiaozhong = Util.locateCenterOnScreen(r'resources/yabiao/' + route + 'yabiaozhong.png')
                cooldown(0.5)
                yabiao_mark = Util.locateCenterOnScreen(r'resources/yabiao/' + route + 'yabiao_mark.png')
                # 押镖按钮
                yabiaoButton = Util.locateCenterOnScreen(r'resources/yabiao/' + route + 'normalYabiao.png')
                print('battleFlag:', battleFlag)
                print('yabiaozhong:', yabiaozhong)
                print('yabiao_mark:', yabiao_mark)
                print('yabiaoButton:', yabiaoButton)
                if battleFlag is None and yabiaozhong is None and yabiao_mark is None:
                    if yabiaoButton is not None:
                        pyautogui.leftClick(yabiaoButton.x, yabiaoButton.y)
                        cooldown(0.5)
                        clickIconPicIfExist(r'resources/yabiao/' + route + 'confirmYabiao.png')
                    else:
                        print("------跳出押镖任务检查，当前次数：------", count)
                        break
            count += 1
        print("------押镖任务已完成------")


# 大窗口
if __name__ == '__main__':
    time.sleep(0.2)
    print("start task....")
    init()
    Yabiao().yabiao()
