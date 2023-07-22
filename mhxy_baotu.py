from mhxy import *


class Baotu:
    # 挖宝图
    def waBaoTu(self):
        print('-----开始挖宝流程-----')
        count = 0
        while count < 2:
            closePopupWindow()
            # 打开包裹并整理
            clickIconPicIfExist(r'resources/baotu/' + route + 'baoguo.png')
            clickIconPicIfExist(r'resources/baotu/' + route + 'zhenglibaoguo.png')
            cooldown(0.5)
            baoguobaotu = Util.locateCenterOnScreen(r'resources/baotu/' + route + 'baoguobaotu.png')
            if baoguobaotu is None:
                print('包裹没有宝图，结束挖宝')
                break

            # 使用宝图
            clickIconPicIfExist(r'resources/baotu/' + route + 'baoguobaotu.png')
            cooldown(1)
            clickIconPicIfExist(r'resources/baotu/' + route + 'baoguoshiyong.png')

            # 开始检查挖宝任务是否结束
            t = datetime.datetime.now().timestamp()
            while True:
                cooldown(3)
                shiyong = Util.locateCenterOnScreen(r'resources/baotu/' + route + 'shiyong.png')
                if shiyong is not None:
                    pyautogui.leftClick(shiyong.x, shiyong.y)
                    t = datetime.datetime.now().timestamp()
                else:
                    # 如果超过75秒没找到宝图使用按钮，停止循环
                    t2 = datetime.datetime.now().timestamp()
                    if t2 - t > 75:
                        print('停止循环挖宝，当前次数：', count)
                        break
            count += 1
        print('-----挖宝任务已完成-------')

    def moveToDianXiaoEr(self):
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
        # 点击店小二
        cooldown(0.5)
        dianxiaoer = pyautogui.locateCenterOnScreen(r'resources/baotu/' + route + 'dianxiaoer.png',
                                                    # collect_caiji
                                                    region=(frame.left, frame.top, frame.right, frame.bottom),
                                                    confidence=0.9)
        if dianxiaoer is not None:
            pyautogui.leftClick(dianxiaoer.x, dianxiaoer.y)
            cooldown(10)

    def baotu(self):
        # 开始挖宝图
        # 打开队伍面板(如果有队伍先退出)
        Util.doubleClick(-1.5, 4)
        cooldown(0.5)
        # Util.locateCenterOnScreen(r'resources/baotu/'+route+'leaveTeam.png')
        clickIconPicIfExist(r'resources/baotu/' + route + 'leaveTeam.png')
        closePopupWindow()
        self.moveToDianXiaoEr()
        clickIconPicIfExist(r'resources/baotu/ting.png')
        clickIconPicIfExist(r'resources/baotu/suanpan.png')
        cooldown(0.5)
        clickIconPicIfExist(r'resources/baotu/' + route + 'baotu.png')

        # 开始检查宝图任务是否做完
        cooldown(30)
        flag = True
        while flag:
            print("开始检查宝图任务是否完成------")
            closePopupWindow()
            battleFlag = Util.locateCenterOnScreen(r'resources/ghost/' + route + 'battleFlag2.png')
            baotu = Util.locateCenterOnScreen(r'resources/baotu/' + route + 'baotu.png')
            if battleFlag is None:
                if baotu is None:
                    flag = False
                else:
                    pyautogui.leftClick(baotu.x, baotu.y)
            cooldown(60)
        print("------宝图任务已完成------")
        self.waBaoTu()


# 大窗口
if __name__ == '__main__':
    pyautogui.PAUSE = 0.5
    print("start task....")
    init()
    Baotu().baotu()
