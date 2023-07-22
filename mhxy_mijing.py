from mhxy import *


class Mijing:

    def moveToYunLeYou(self):
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
        Util.leftClick(-5.8, -9)

        cooldown(0.5)
        # 打开小地图
        posSmallMap = (frame.left + relativeX2Act(3.5),
                       frame.top + relativeY2Act(2))
        pyautogui.leftClick(posSmallMap[0],
                            posSmallMap[1])
        # 点击云乐游
        cooldown(0.5)
        position = Util.locateCenterOnScreen(r'resources/mijing/' + route + 'yunleyou.png')
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            cooldown(8)

    def mijing(self, levelType):
        print('-----开始秘境流程，levelType：-----', levelType)
        closePopupWindow()
        self.moveToYunLeYou()
        clickIconPicIfExist(r'resources/mijing/' + route + 'getMijingTask.png')
        cooldown(2)

        # 首次做任务，默认选择简单任务
        enterMijing = Util.locateCenterOnScreen(r'resources/mijing/' + route + 'enterMijing.png')
        if enterMijing is not None:
            pyautogui.leftClick(enterMijing.x, enterMijing.y)
            cooldown(0.5)
            clickIconPicIfExist(r'resources/mijing/' + route + 'confirmMijing.png')

        cooldown(2)
        # 点击第一个怪开始任务(相对位置)(勇武，精锐位置不同，需要区分)
        if levelType == 0:
            Util.leftClick(5.7, 10.7)
        elif levelType == 1:
            Util.leftClick(6.7, 10.7)
        clickIconPicIfExist(r'resources/mijing/' + route + 'battle.png')
        clickIconPicIfExist(r'resources/mijing/' + route + 'battleAgain.png')
        cooldown(1)

        # 开始检查秘境任务是否做完
        while True:
            cooldown(7)
            print("开始检查秘境任务是否完成------")
            closePopupWindow()
            clickIconPicIfExist(r'resources/fuben/' + route + 'fubenBattle2.png')

            # 追踪任务之前检查是否战斗失败，失败一次结束任务
            battleFail = Util.locateCenterOnScreen(r'resources/mijing/' + route + 'battleFail.png')
            if battleFail is not None:
                print("---战斗失败，停止检查任务------")
                break

            # 点击追踪任务(相对位置)
            Util.leftClick(-1, 9)

        print("------秘境任务已完成------")


# 大窗口
if __name__ == '__main__':
    input_out = input("角色等级？0：89，1：69。请输入：")
    print("请手动激活窗口（5秒内）")
    time.sleep(5)
    print("start task....")
    init()
    Mijing().mijing(int(input_out))
