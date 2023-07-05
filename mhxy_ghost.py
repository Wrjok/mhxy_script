import datetime as dt
import os
import sys
import threading
from configparser import ConfigParser

import playsound as pl
from pyautogui import FailSafeException

from mhxy import *





class Ghost:
    maxRound = 99
    # 程序运行标志
    _flag = True
    # 是否发生跨天
    _newDayClick = False
    _count = 0
    # 捉鬼开始时间
    _beginHour = 0
    _startTimestamp = None
    _chaseWin = None
    # 任务位置
    chasepos = 1
    # 自动领双数
    _doublePointNumPer100 = -1

    def __init__(self, idx=0) -> None:
        conn = ConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'resources/ghost/ghost.ini')
        print(file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在")
        conn.read(file_path)
        chasepos = int(conn.get('main', 'chasepos'))
        maxRound = int(conn.get('main', 'maxRound'))
        doublePointNumPer100 = int(conn.get('main', 'doublePointNumPer100'))
        resize = bool(int(conn.get('main', 'resize')))
        if chasepos is not None:
            print("读取配置：任务位置为：" + str(chasepos))
            self.chasepos = chasepos
        if maxRound is not None:
            print("读取配置：捉鬼轮数为：" + str(maxRound))
            self.maxRound = maxRound
        if doublePointNumPer100 is not None:
            print("读取配置：领双数为：" + str(doublePointNumPer100))
            self._doublePointNumPer100 = doublePointNumPer100
        print("读取配置：调整窗口大小：" + str(resize))

        init(int(idx), resizeToNice=resize)  # True

        self._chaseWin = (winRelativeX(-1), winRelativeY(3.7))
        super().__init__()

    def _chaseWinFix(self):
        return relativeY2Act(2 * (self.chasepos + (1 if self._newDayClick and self._beginHour != 0 else 0)))

    def getDialog(self):
        cooldown(1)
        Util.leftClick(7.5, 1.5)
        cooldown(1)
        Util.leftClick(3, 4.5)
        cooldown(2)
        mission = Util.locateCenterOnScreen(r'resources/ghost/mission.png')
        i = 0
        while mission is None and i in range(0, 2):
            pyautogui.moveTo(winRelativeX(10), winRelativeY(12.5))
            pyautogui.dragTo(winRelativeX(10), winRelativeY(4.6), duration=0.8)
            cooldown(1)
            mission = Util.locateCenterOnScreen(r'resources/ghost/mission.png')
            i += 1
        if mission is not None:
            cooldown(1)
            pyautogui.leftClick(mission.x + relativeX2Act(3.5), mission.y + relativeY2Act(0.2))

    def getPoint(self):
        cooldown(2)
        Util.leftClick(11, 1.5)
        cooldown(2)
        for each in range(0, self._doublePointNumPer100):
            Util.leftClick(20, 16)
            cooldown(0.2)
        cooldown(2)
        Util.leftClick(23, 3.5)
        cooldown(2)
        pass

    def _startMission(self, location):
        # 领任务
        pyautogui.leftClick(location.x, location.y)
        # +3 整点第二个任务
        print("关闭对话框 ", self._chaseWin)
        cooldown(1)
        five = Util.locateOnScreen(r'resources/ghost/team_not_full.png')
        if five is not None:
            # 按取消
            pyautogui.leftClick(five.left + five.width - 120, five.top + five.height - 20)
        # 校验双倍 self.__count % 25 == 0
        if self._count % 25 == 0 and self._doublePointNumPer100 != -1:
            pyautogui.click(self._chaseWin[0], self._chaseWin[1] + self._chaseWinFix(), clicks=1,
                            button=pyautogui.LEFT)
            cooldown(0.2)
            self.getPoint()
            pyautogui.click(self._chaseWin[0], self._chaseWin[1] + self._chaseWinFix(), clicks=1,
                            button=pyautogui.LEFT)
        else:
            # 关对话 + 追踪
            pyautogui.click(self._chaseWin[0], self._chaseWin[1] + self._chaseWinFix(), clicks=2,
                            button=pyautogui.LEFT)

    def _newDayCloseDiagDo(self, newDay):
        if newDay is None:
            return
        pyautogui.leftClick(newDay.x, newDay.y)
        cooldown(1)
        Util.leftClick(-1, -3)

    def go(self):
        cooldown(1)
        Util.leftClick(6.8, 1.5)
        cooldown(0.5)
        Util.leftClick(3, 4.7)
        cooldown(1)
        tag = Util.locateCenterOnScreen('resources/ghost/activity_tag.png')
        i = 0
        while tag is None and i in range(0, 2):
            pyautogui.moveTo(winRelativeX(10), winRelativeY(10))
            pyautogui.dragTo(winRelativeX(10), winRelativeY(4.6), duration=0.8)
            cooldown(1.5)
            tag = Util.locateCenterOnScreen('resources/ghost/activity_tag.png')
            i += 1
        if tag is not None:
            cooldown(1)
            pyautogui.leftClick(tag.x + relativeX2Act(3.5), tag.y + relativeY2Act(0.2))

    def _startGhostDo(self):
        cooldown(5 * 60)

    def ghost(self):
        # _thread.start_new_thread(resumeIfDisconnect, ("Thread-1", 2,))
        def initStartLocation():
            return Util.locateCenterOnScreen('resources/ghost/start_ghost0.png')

        while self._flag:
            # 是否继续捉鬼弹窗 虽然使用确定即可，但是截图截得长了，所以locateOnScreen获取相对截图右下点的位置
            completeLocation = Util.locateOnScreen('resources/ghost/complete_ghost0.png')
            startLocation = None
            if newDayCloseCheck(self._newDayCloseDiagDo):
                self._newDayClick = True

            if completeLocation is None:
                # 对话框：捉鬼任务选项。
                startLocation = initStartLocation()

            if completeLocation is not None:
                # 选择继续捉鬼
                pyautogui.leftClick(completeLocation.left + completeLocation.width - 50,
                                    completeLocation.top + completeLocation.height - 20)
                startLocation = initStartLocation()
                print("结束抓鬼 ", completeLocation)
            if startLocation is not None:
                self._count += 1
                print("已完成抓鬼" + str(self._count) + "轮数")
                if self._count > self.maxRound:
                    self._flag = False
                    # pl.playsound('resources/common/music.mp3')
                else:
                    self._startMission(startLocation)
                    self._startTimestamp = dt.datetime.now()
                    print("开始抓鬼 ", startLocation)
                    self._startGhostDo()
                if self._count % 25 == 0:
                    print("完成一千双")
                    pl.playsound('resources/common/music.mp3')
            # 二十分钟没有下一轮 怀疑掉线
            if self._startTimestamp is not None and (dt.datetime.now() - self._startTimestamp).seconds > 25 * 60:
                Util.leftClick(self._chaseWin[0], self._chaseWin[1] + self._chaseWinFix())
                naozhong = threading.Thread(target=pl.playsound('resources/common/music.mp3'))
                # 闹钟提醒
                naozhong.start()
            cooldown(2)

    def moveToZhongkui(self):
        # 打开大地图
        posBigMap = (frame.left + relativeX2Act(1),
                     frame.top + relativeY2Act(2))
        print("click bigMap", posBigMap)
        pyautogui.leftClick(posBigMap[0],
                            posBigMap[1])
        # 选择长安城
        # 点击长安城
        collect = pyautogui.locateCenterOnScreen(r'resources/common/chang_an_cheng.png',  # collect_caiji
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
        # 点击钟馗
        cooldown(0.5)
        zhongkui = pyautogui.locateCenterOnScreen(r'resources/ghost/zhong_kui.png',  # collect_caiji
                                                  region=(frame.left, frame.top, frame.right, frame.bottom),
                                                  confidence=0.9)
        if zhongkui is not None:
            pyautogui.leftClick(zhongkui.x, zhongkui.y)
            cooldown(8)

    # 一键喊话（帮派，当前频道）
    def yijianhanhua(self):
        position = pyautogui.locateCenterOnScreen(r'resources/ghost/han_hua.png',  # collect_caiji
                                                  region=(frame.left, frame.top, frame.right, frame.bottom),
                                                  confidence=0.9)
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            position = pyautogui.locateCenterOnScreen(r'resources/ghost/bangpai_channel.png',  # collect_caiji
                                                      region=(frame.left, frame.top, frame.right, frame.bottom),
                                                      confidence=0.9)
            if position is not None:
                pyautogui.leftClick(position.x, position.y)

        position = pyautogui.locateCenterOnScreen(r'resources/ghost/han_hua.png',  # collect_caiji
                                                  region=(frame.left, frame.top, frame.right, frame.bottom),
                                                  confidence=0.9)
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            position = pyautogui.locateCenterOnScreen(r'resources/ghost/current_channel.png',  # collect_caiji
                                                      region=(frame.left, frame.top, frame.right, frame.bottom),
                                                      confidence=0.9)
            if position is not None:
                pyautogui.leftClick(position.x, position.y)
        cooldown(23)

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
            cooldown(1)
            teamPanel = Util.locateCenterOnScreen(r'resources/fuben/' + '' + 'duiwumianban.png')
            if teamPanel is None:
                return True
            print("检查是否有离线队友")
            # 检查是否有离线队友
            self.checkLixian()
            clickIconPicIfExist(r'resources/ghost/auto_find.png')
            # 如果队伍不足4人，开始喊话
            count = 0
            for teamMate in TEAMMATE_LIST:
                position = pyautogui.locateAllOnScreen(teamMate._pic,  # collect_caiji
                                                       region=(frame.left, frame.top, frame.right, frame.bottom),
                                                       confidence=0.9)
                if position is not None:
                    count += len(list(position))
            print('队伍助战数量：', count)
            # 第一次组队可能不会出现助战的情况，做兼容性处理
            team4 = pyautogui.locateCenterOnScreen(r'resources/ghost/team4.png',  # collect_caiji
                                                   region=(frame.left, frame.top, frame.right, frame.bottom),
                                                   confidence=0.9)
            team5 = pyautogui.locateCenterOnScreen(r'resources/ghost/team5.png',  # collect_caiji
                                                   region=(frame.left, frame.top, frame.right, frame.bottom),
                                                   confidence=0.9)
            if count > 1 or (team4 is None and team5 is None):
                self.yijianhanhua()
            else:
                hanHua = False
            t2 = datetime.datetime.now().timestamp()
            # 如果喊话超过5分钟，跳出循环
            if t2-t > 60*5:
                hanHua = False
                return True

    def checkIfFinishTask(self, wait=0):
        judgeCount = 0
        check_flag = True
        while check_flag:
            # 每分钟检查一次
            cooldown(wait)
            print('----开始检查队友和任务是否完成------wait:', wait)
            closePopupWindow()
            auto_battle2 = pyautogui.locateCenterOnScreen(r'resources/ghost/battleFlag2.png',  # collect_caiji
                                                          region=(frame.left, frame.top, frame.right, frame.bottom),
                                                          confidence=0.9)
            if auto_battle2 is not None:
                clickIconPicIfExist(r'resources/ghost/battleFlag.png')
                clickIconPicIfExist(r'resources/ghost/team.png')
                self.checkLixian()
                clickIconPicIfExist(r'resources/ghost/auto_find.png')
                closePopupWindow()
                # 关掉菜单栏
                clickIconPicIfExist(r'resources/ghost/closeMenu.png')
            else:
                print('auto_battle2:', auto_battle2)
                startGhost = pyautogui.locateCenterOnScreen(r'resources/ghost/startGhost.png',  # collect_caiji
                                                            region=(frame.left, frame.top, frame.right, frame.bottom),
                                                            confidence=0.9)
                if startGhost is None:
                    # 抓完一轮鬼，跳出循环
                    print("跳出循环")
                    judgeCount += 1
                    check_flag = False
                else:
                    print("检查是否进入战斗")
                    cooldown(10)
                    closePopupWindow()
                    # 检查是否进入战斗
                    enter_battle = pyautogui.locateCenterOnScreen(r'resources/ghost/battleFlag2.png',
                                                                  # collect_caiji
                                                                  region=(
                                                                  frame.left, frame.top, frame.right, frame.bottom),
                                                                  confidence=0.9)
                    if enter_battle is None:
                        # 打开大地图
                        posBigMap = (frame.left + relativeX2Act(1),
                                     frame.top + relativeY2Act(2))
                        print("click bigMap:检查是否进入战斗", posBigMap)
                        pyautogui.leftClick(posBigMap[0],
                                            posBigMap[1])
                        # 选择长安城
                        # 点击长安城
                        collect = pyautogui.locateCenterOnScreen(r'resources/common/chang_an_cheng.png',
                                                                 # collect_caiji
                                                                 region=(
                                                                     frame.left, frame.top, frame.right,
                                                                     frame.bottom),
                                                                 confidence=0.9)
                        if collect is not None:
                            pyautogui.leftClick(collect.x, collect.y)
                        cooldown(0.5)
                        # 打开队伍面板
                        Util.doubleClick(-1.5, 4)
                        self.checkAddTeam()
                        closePopupWindow()
                        cooldown(0.5)
                        Util.leftClick(-4.4, 4)
                        clickIconPicIfExist(r'resources/ghost/startGhost.png')

    # source:0=无限抓鬼，1=一条龙抓鬼
    def ghostNew(self, source):
        t = datetime.datetime.now().timestamp()
        while True:
            t2 = datetime.datetime.now().timestamp()
            if source == 1 and t2-t > 60*30:
                break

            # 任务开始前关闭弹窗广告
            closePopupWindow()

            # self.checkIfFinishTask(60)

            # 移动位置到长安城钟馗
            self.moveToZhongkui()

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
                clickIconPicIfExist(r'resources/ghost/confirm.png')

            result = self.checkAddTeam()

            # 队伍人数组满后，开始领任务
            closePopupWindow()
            self.moveToZhongkui()

            print("点击捉鬼任务按钮")
            clickIconPicIfExist(r'resources/ghost/zhuogui_renwu.png')

            # 点击任务栏开始抓鬼
            closePopupWindow()
            clickIconPicIfExist(r'resources/ghost/zk_dialog.png')
            clickIconPicIfExist(r'resources/ghost/startGhost.png')
            clickIconPicIfExist(r'resources/ghost/startGhost.png')

            self.checkIfFinishTask(60)
        print("-----抓鬼任务已完成--------")


# 小窗口 pyinstaller -F mhxy_ghost.py
if __name__ == '__main__':
    idx = 0 if len(sys.argv) <= 1 else sys.argv[1]
    pyautogui.PAUSE = 1  # 调用在执行动作后暂停的秒数，只能在执行一些pyautogui动作后才能使用，建议用time.sleep
    pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
    try:
        Ghost(idx=idx).ghostNew(0)
    except (FailSafeException):
        pl.playsound('resources/common/music.mp3')
