# from mhxy import *

from mhxy_baotu import *
from mhxy_ghost import *
from mhxy_yabiao import *
from mhxy_mijing import *

class _FubenTask:
    _x = 1
    _y = 2
    _flag = False

    def __init__(self, _x, _y, _flag):
        self._x = _x
        self._y = _y
        self._flag = _flag


FubenTask_count = 5
# 等级类型，0=89,1=69
levelType = 0

class Fuben:
    xiashi_fix = 5.6 + 0
    _fubenIdx = 0
    fubenPos = [
        # ("xiashi", 13, 15),
        ("xiashi", 7, 15),

        ("norm", 19, 15),
        ("norm", 13, 15),
        ("norm", 7, 15)
    ]
    config = {
        'lastFuben': r'resources/small/fuben_flag.png'
    }

    def __init__(self, idx=0) -> None:
        # init(resizeToNice=True)
        init(idx=idx, resizeToNice=False)

    def _changan(self):
        return Util.locateCenterOnScreen(r'resources/fuben/activity.png')

    # 流程任务
    def _do(self):
        def clickSkip(locate, idx):
            reachPos = Util.locateCenterOnScreen(r'resources/fuben/select.png')
            if reachPos is not None:
                # 对话
                pyautogui.leftClick(reachPos.x, reachPos.y + relativeY2Act(1.5))
            elif Util.locateCenterOnScreen(r'resources/fuben/skipJuqing.png') is not None:
                # 跳过剧情动画
                Util.leftClick(-3, 7)
            elif Util.locateCenterOnScreen(r'resources/small/blood.png') is None:
                # 阅读剧情
                Util.leftClick(-3, 1.8)
            else:
                # 追踪任务
                Util.leftClick(-3, 5.5)
            cooldown(1)

        def doUntil2Changan():
            changanPos = self._changan()  # 550,543
            while changanPos is None:
                # 找不到头像则正在对话点击头像位置跳过 直到找到头像位置
                doUtilFindPic([r'resources/small/enter_battle_flag.png', r'resources/fuben/activity.png'], clickSkip)
                changanPos = self._changan()
                cooldown(2)

        #  进入第一个副本为起点
        doUntil2Changan()
        if self._fubenIdx >= len(self.fubenPos):
            return False
        elif self.fubenPos[self._fubenIdx][0] == "xiashi":
            # 已领取的侠士任务所在坐标
            Util.leftClick(-3, self.xiashi_fix)
            cooldown(2.0)
            Util.leftClick(self.fubenPos[self._fubenIdx][1], self.fubenPos[self._fubenIdx][2])
            self._fubenIdx += 1
        else:
            cooldown(1)
            Util.leftClick(7.5, 1.5)
            cooldown(0.5)
            Util.leftClick(3, 4.5)
            cooldown(1)
            lastFuben = Util.locateCenterOnScreen(self.config['lastFuben'])
            i = 0
            while lastFuben is None and i in range(0, 2):
                pyautogui.moveTo(winRelativeX(10), winRelativeY(10))
                pyautogui.dragTo(winRelativeX(10), winRelativeY(4.6), duration=0.8)
                cooldown(1.5)
                lastFuben = Util.locateCenterOnScreen(self.config['lastFuben'])
                i += 1
            if lastFuben is not None:
                cooldown(1)
                pyautogui.leftClick(lastFuben.x + relativeX2Act(3), lastFuben.y + relativeY2Act(0.2))
                cooldown(5)
                se = Util.locateCenterOnScreen(r'resources/fuben/selectfuben.png')
                #  11
                pyautogui.leftClick(se.x, se.y)
                cooldown(2)
                # 下一个副本
                Util.leftClick(self.fubenPos[self._fubenIdx][1], self.fubenPos[self._fubenIdx][2])
                self._fubenIdx += 1
        return True

    def loginIn(self):
        cooldown(1)
        loginInBtn = Util.locateCenterOnScreen(r'resources/fuben/loginin.png')
        if loginInBtn is not None:
            pyautogui.leftClick(loginInBtn.x, loginInBtn.y)
        cooldown(5)
        Util.leftClick(12, 13.5)

    def moveToBaixiao(self):
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
        # 点击百晓仙子
        cooldown(0.5)
        baixiaoxianzi = pyautogui.locateCenterOnScreen(r'resources/fuben/' + str('') + 'baixiaoxianzi.png',
                                                       # collect_caiji
                                                       region=(frame.left, frame.top, frame.right, frame.bottom),
                                                       confidence=0.9)
        if baixiaoxianzi is not None:
            pyautogui.leftClick(baixiaoxianzi.x, baixiaoxianzi.y)
            cooldown(6)

    # 打开队伍面板，检查是否有离线队友
    def checkLixian(self):
        # 检查是否有离线队友
        lixianCount = 0
        while lixianCount < 4:
            liXian = pyautogui.locateCenterOnScreen(r'resources/ghost/liXian.png',  # collect_caiji
                                                    region=(frame.left, frame.top, frame.right, frame.bottom),
                                                    confidence=0.9)
            if liXian is not None:
                pyautogui.leftClick(liXian.x, liXian.y)
                deleteTeam = pyautogui.locateCenterOnScreen(r'resources/ghost/deleteTeam.png',  # collect_caiji
                                                            region=(
                                                                frame.left, frame.top, frame.right, frame.bottom),
                                                            confidence=0.9)
                if deleteTeam is not None:
                    pyautogui.leftClick(deleteTeam.x, deleteTeam.y)
            lixianCount += 1

    def checkAddTeam(self):
        t = datetime.datetime.now().timestamp()
        hanHua = True
        while hanHua:
            closePopupWindow()
            # 开始喊话
            clickIconPicIfExist(r'resources/fuben/hanhua.png')
            clickIconPicIfExist(r'resources/fuben/currentSelect.png')
            clickIconPicIfExist(r'resources/fuben/currentUnSelect.png')
            if levelType == 0:
                Util.write("勇武三本+20鬼速度来稳定勇武三本+20鬼速度来稳定勇武三本+20鬼速度来稳定")
            elif levelType == 1:
                Util.write("双本+20鬼速度来稳定双本+20鬼速度来稳定双本+20鬼速度来稳定")
            clickIconPicIfExist(r'resources/fuben/agreeButton.png')
            clickIconPicIfExist(r'resources/fuben/closeDialog.png')
            cooldown(10)
            # 打开队伍面板
            closePopupWindow()
            Util.doubleClick(-1.5, 4)
            cooldown(1)
            teamPanel = Util.locateCenterOnScreen(r'resources/fuben/' + '' + 'duiwumianban.png')
            if teamPanel is None:
                return True
            print("检查是否有离线队友")
            # 检查是否有离线队友
            self.checkLixian()
            # 如果队伍不足5人，开始喊话
            count = 0
            for teamMate in TEAMMATE_LIST:
                position = pyautogui.locateAllOnScreen(teamMate._pic,  # collect_caiji
                                                       region=(frame.left, frame.top, frame.right, frame.bottom),
                                                       confidence=0.9)
                if position is not None:
                    count += len(list(position))
            print('队伍助战数量：', count)
            # 第一次组队可能不会出现助战的情况，做兼容性处理
            team5 = pyautogui.locateCenterOnScreen(r'resources/ghost/team5.png',  # collect_caiji
                                                   region=(frame.left, frame.top, frame.right, frame.bottom),
                                                   confidence=0.9)
            if count > 0 or team5 is None:
                # self.yijianhanhua()
                print("队伍不足5人，继续喊话")
            else:
                hanHua = False
            t2 = datetime.datetime.now().timestamp()
            # 如果喊话超过5分钟，跳出循环
            if t2 - t > 60 * 5:
                hanHua = False
                return True

    def fuben(self, start):
        global FubenTask_count
        count = start - 1
        while count < FubenTask_count:
            if count == start - 1:
                # 任务开始前关闭弹窗广告
                closePopupWindow()

                # self.checkIfFinishTask(60)

                # 移动位置到长安城百晓仙子
                self.moveToBaixiao()

                # 开始组队
                clickIconPicIfExist(r'resources/ghost/create_team.png')

                zhongkui = pyautogui.locateCenterOnScreen(r'resources/ghost/create_team_success.png',  # collect_caiji
                                                          region=(frame.left, frame.top, frame.right, frame.bottom),
                                                          confidence=0.9)
                if zhongkui is not None:
                    pyautogui.leftClick(zhongkui.x, zhongkui.y)
                    # 自动匹配
                    clickIconPicIfExist(r'resources/ghost/auto_find.png')
                else:
                    # 已有队伍，直接确定
                    cooldown(1)
                    clickIconPicIfExist(r'resources/fuben/normal.png')
                    clickIconPicIfExist(r'resources/ghost/confirm.png')

                result = self.checkAddTeam()
                if result:
                    print("检查队伍失败，重新开始任务")
                    continue

            # 队伍人数组满后，开始领任务
            closePopupWindow()
            self.moveToBaixiao()

            print("点击选择副本")
            clickIconPicIfExist(r'resources/fuben/' + route + 'choseFuben.png')

            # 计算普通副本任务数
            cooldown(1)
            fubenTasks = pyautogui.locateAllOnScreen(r'resources/fuben/' + route + 'enterFuben.png',  # collect_caiji
                                                     region=(frame.left, frame.top, frame.right, frame.bottom),
                                                     confidence=0.9)
            enterList = list(fubenTasks)
            print("副本入口：", enterList)
            FubenTask_count = len(enterList)
            enter = enterList.__getitem__(count)
            pyautogui.leftClick(enter.left, enter.top)
            cooldown(2)

            checkFlag = True
            while checkFlag:
                closePopupWindow()
                print("开始检查副本任务是否进入战斗")
                battle_flag = Util.locateCenterOnScreen(r'resources/ghost/' + route + 'battleFlag2.png')
                if battle_flag is None:
                    clickIconPic(r'resources/fuben/' + route + 'jump.png', 5)
                    cooldown(2)
                    clickIconPicIfExist(r'resources/fuben/' + route + 'clickPingmu.png')
                    cooldown(1)
                    blood = Util.locateCenterOnScreen(r'resources/fuben/' + route + 'blood.png')
                    if blood is not None:
                        clickIconPicIfExist(r'resources/fuben/' + route + 'task_black.png')
                    cooldown(1)
                    result = clickIconPic(r'resources/ghost/' + route + 'startGhost.png', 5)
                    if result:
                        print("当前副本已完成")
                        count += 1
                        break
                    else:
                        # fubenBattleCount = 0
                        # while fubenBattleCount < 5:
                        #     cooldown(0.5)
                        #     fubenBattleCount += 1
                        #     fubenBattle = Util.locateCenterOnScreen(r'resources/fuben/' + route + 'fubenBattle.png')
                        #     if fubenBattle is None:
                        #         pyautogui.leftClick()
                        #     else:
                        #         break
                        battle_list = [r'resources/fuben/' + route + 'fubenBattle1.png', r'resources/fuben/' + route + 'fubenBattle2.png']
                        ret = clickIconPic(battle_list, 7)
                        if ret:
                            clickIconPicByCount(r'resources/fuben/' + route + 'continue_juqing.png', 0.4, 5)
                            clickIconPic(battle_list, 2)
                cooldown(10)


# 副本 进入第一个副本为起点 小窗口
if __name__ == '__main__':
    input_out = input("角色等级？0：89，1：69。请输入：")
    # # pyautogui.PAUSE = 1
    levelType = int(input_out)
    print("请手动激活窗口（10秒内）")
    time.sleep(10)
    print("start task....")
    Fuben().fuben(1)
    print("end task(fuben)....start task(ghost)")
    Ghost().ghostNew(1)
    Baotu().baotu()
    Yabiao().yabiao()
    Mijing().mijing(levelType)

