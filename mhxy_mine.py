from mhxy import *


class _MinePoint:
    wait = 10
    pic = 10
    offsetY = 0

    def __init__(self, wait, pic, offsetY=20):
        self.wait = wait
        self.pic = pic
        self.offsetY = offsetY


# 矿图列表
NORM_MINE_LIST = [
    # 矿
    _MinePoint(3, r'resources/mine/norm_purple_shade_mine.png'),
    _MinePoint(3, r'resources/mine/norm_purple_mine.png'),
    _MinePoint(5, r'resources/mine/blue_mine.png'),
    _MinePoint(5, r'resources/mine/norm_blue_shade_mine.png'),

    _MinePoint(7, r'resources/mine/norm_green_mine.png'),
    # MinePoint(7, r'resources/mine/norm_green_shade_mine.png'),

    _MinePoint(10, r'resources/mine/norm_grey_mine.png'),
    _MinePoint(10, r'resources/mine/norm_grey_shade_mine.png')
    # 采集
    # _MinePoint(8, r'resources/mine/norm_cao.png', 20),
]


# 关闭花果小地图
class MineUtil:
    @staticmethod
    def closeSmallMap(type):
        if type == "daxue":
            pos = (-7, 6)
        elif type == "changshou":
            pos = (-6, 6)
        else:
            pos = (-7.8, 3.8)
        Util.leftClick(pos[0], pos[1])


class _StandPoint:
    mineList = NORM_MINE_LIST

    def move2Point(self):
        pass


class _FstStandPoint(_StandPoint):
    relativeX = 0
    relativeY = 0
    mineList = []

    def __init__(self, x, y, map="huaguo", cooldown=4, mineList=None):
        self.map = map
        self.relativeX = x
        self.relativeY = y
        self.cooldown = cooldown
        if mineList is None:
            self.mineList = NORM_MINE_LIST
        else:
            self.mineList = mineList

    def move2Point(self):
        # self.newDayCloseDiag()
        # 打开大地图
        posBigMap = (frame.left + relativeX2Act(1),
                     frame.top + relativeY2Act(2))
        print("click bigMap", posBigMap)
        pyautogui.leftClick(posBigMap[0],
                            posBigMap[1])
        # 选择花果山
        posMap = None
        if self.map == "huaguo":
            posMap = (-4.5, 8.3)
            print("click 花果山", posMap)
        elif self.map == "daxue":
            posMap = (11, 6.3)
        elif self.map == "changshou":
            posMap = (3.5, 11.2)
        Util.leftClick(posMap[0], posMap[1])
        # self.newDayCloseDiag()
        # 打开小地图
        cooldown(0.5)
        posSmallMap = (frame.left + relativeX2Act(3.5),
                       frame.top + relativeY2Act(2))
        pyautogui.leftClick(posSmallMap[0],
                            posSmallMap[1])
        # 选择右上部分的点
        cooldown(1)
        posMove = winRelativeXY(self.relativeX, self.relativeY)
        pyautogui.leftClick(posMove[0],
                            posMove[1])
        MineUtil.closeSmallMap(self.map)
        closeMission()
        cooldown(self.cooldown)

    def newDayCloseDiag(self):
        def do(newDay):
            if newDay is None:
                return
            pyautogui.leftClick(newDay.x, newDay.y)
            cooldown(1)
            Util.leftClick(-1, -3)

            def scroll2Lingshifu(locate, idx):
                pyautogui.moveTo(winRelativeX(-9), winRelativeY(-4.9))
                pyautogui.dragTo(winRelativeX(-9), winRelativeY(6.7), duration=1)
                cooldown(0.2)

            locate, idx = doUtilFindPic(r'resources/mine/lingshifu.png', scroll2Lingshifu)
            if locate is not None:
                pyautogui.leftClick(locate.x, locate.y)
                cooldown(0.2)
                Util.leftClick(11, 13)
                cooldown(0.7)
                # pyautogui.leftClick(newDay.x, newDay.y)
                Util.leftClick(-1.5, 4)
                cooldown(0.2)
                Util.leftClick(-2.5, 3.7)
                cooldown(0.7)

        newDayCloseCheck(do)


class _NormStandPoint(_StandPoint):
    # 相对小地图的位置
    relativeX = 0
    relativeY = 0
    map = "huaguo"

    def __init__(self, x, y, cooldown=6, map="huaguo", mineList=None):
        self.relativeX = x
        self.relativeY = y
        self.map = map
        self.cooldown = cooldown
        if mineList is None:
            self.mineList = NORM_MINE_LIST
        else:
            self.mineList = mineList

    def move2Point(self):
        # 打开小地图
        posSmallMap = (frame.left + relativeX2Act(3.5),
                       frame.top + relativeY2Act(2))
        pyautogui.leftClick(posSmallMap[0],
                            posSmallMap[1])
        # 选择右上部分随意点
        cooldown(0.5)
        posMove = winRelativeXY(self.relativeX, self.relativeY)
        pyautogui.leftClick(posMove[0],
                            posMove[1])
        MineUtil.closeSmallMap(self.map)
        cooldown(self.cooldown)


class Mine:
    _lastMineTime = datetime.datetime.now().timestamp()
    mark = True

    # 所有定义站立点
    _standPoints = (
        _FstStandPoint(
            -10, 10, map="huaguo", cooldown=4
        ),
        _NormStandPoint(
            12.5, 9, cooldown=5
        ),
        _NormStandPoint(
            18.5, -5.5, cooldown=9
        ),
        _NormStandPoint(
            10, -5, cooldown=7
        ),
        _NormStandPoint(
            10, 14, cooldown=3
        )

        # _FstStandPoint(
        #     7, 8.4, map="changshou", cooldown=6
        # ),
        # _NormStandPoint(
        #     13.5, 9, map="changshou", cooldown=4
        # ),
        # _NormStandPoint(
        #     13.5, 11, map="changshou", cooldown=3
        # ),
        # _NormStandPoint(
        #     -15, 14, map="changshou", cooldown=3
        # ),
        # _NormStandPoint(
        #     18.5, 14.5, map="changshou", cooldown=4
        # ),
        # _NormStandPoint(
        #     20, 10, map="changshou", cooldown=5
        # )
    )

    # 小地图
    _smallMap = Frame(0, 0)

    def _initForMine(self):
        pyautogui.PAUSE = 0.3
        self._smallMap.left = frame.left + relativeX2Act(7.5)
        self._smallMap.top = frame.top + relativeY2Act(3.7)
        self._smallMap.right = frame.right - relativeX2Act(7.5)
        self._smallMap.bottom = frame.bottom - relativeY2Act(2.8)
        print("init smallMap:", self._smallMap)

    def _changeMapPos(self, mapPos):
        self._standPoints[mapPos % len(self._standPoints)].move2Point()
        return self._standPoints[mapPos % len(self._standPoints)]

    def __init__(self, idx=0) -> None:
        super().__init__()
        init(resizeToNice=False, idx=idx)
        self._initForMine()
        self._lastMineTime = datetime.datetime.now().timestamp()

    def _mining(self, mineList=None):
        def waitMining():
            collect = pyautogui.locateCenterOnScreen(r'resources/mine/cai_kuang_zhong.png',  # collect_caiji
                                                     region=(frame.left, frame.top, frame.right, frame.bottom),
                                                     confidence=0.8)
            while collect is not None:
                cooldown(1)
                collect = pyautogui.locateCenterOnScreen(r'resources/mine/cai_kuang_zhong.png',  # collect_caiji
                                                         region=(frame.left, frame.top, frame.right, frame.bottom),
                                                         confidence=0.8)

        def waitMoveOk():
            mineSelect = pyautogui.locateCenterOnScreen(r'resources/mine/mine_select.png',
                                                        region=(frame.left, frame.top, frame.right, frame.bottom),
                                                        confidence=0.96)
            if mineSelect is not None:
                pyautogui.leftClick(mineSelect.x, mineSelect.y)
            collect = None
            count = 0
            while collect is None:
                if count > 10:
                    return False
                cooldown(1)
                collect = pyautogui.locateCenterOnScreen(r'resources/mine/collect.png',  # collect_caiji
                                                         region=(frame.left, frame.top, frame.right, frame.bottom),
                                                         confidence=0.8)
                count += 1
            return True

        if mineList is None:
            mineList = NORM_MINE_LIST
        # 等待时间 点位信息
        count = 0
        while count < len(mineList):
            for mine in mineList:
                point = pyautogui.locateCenterOnScreen(mine.pic,
                                                       region=(frame.left, frame.top, frame.right, frame.bottom),
                                                       confidence=0.96)
                if point is not None:
                    print("发现矿：", mine.pic)
                    p = (mine.wait, point.x, point.y)
                    # 点击矿
                    pyautogui.leftClick(point.x, point.y - mine.offsetY)  # -20 采集
                    if point.y <= frame.top + relativeY2Act(3.5):
                        continue
                    res = waitMoveOk()
                    # 出现采矿按钮并且点位不会碰到地图
                    if res:
                        # 点击挖
                        self._lastMineTime = datetime.datetime.now().timestamp()
                        Util.leftClick(-5, -3.5)
                        # cooldown(mine.wait)
                        waitMining()
                        # 验证码的出现规则目前是每一天时间出现一次，可以先手动挖一两轮再挂
                        yanzhen = Util.locateCenterOnScreen(r'resources/mine/yanzhen.png')
                        if yanzhen is not None:
                            # 挖到验证码停止，然后等10秒手动验证（大概两轮就出，所以没选择报警）
                            self.mark = False
                            cooldown(10)
                            return
                            # 报警提示
                            # pl.playsound('resources/common/music.mp3')
                        count += 1
                        # 根据颜色等待 3-5-7-10 秒
                        if p[0] == -1:
                            # 五级采矿点 -1 表示连续中间十次完成采矿
                            pyautogui.click(frameSize[0] >> 1, frameSize[1] >> 1, clicks=10, duration=0.08,
                                            button=pyautogui.LEFT)
                        else:
                            cooldown(p[0] - 3)
                else:
                    count += 1

    def mineMain(self):
        mapPos = 0
        standPoint = self._changeMapPos(mapPos)
        print('开始----------------------')
        # 没有改变过位置
        notChange = True
        while self.mark:
            self._mining(standPoint.mineList)
            # mine = mining()
            now = datetime.datetime.now()
            minute = now.minute
            second = now.second
            # 修改位置
            if minute % 5 == 0 and second > 10 and notChange:
                mapPos = 0
                standPoint = self._changeMapPos(mapPos)
                notChange = False
            elif mapPos < 2 * len(self._standPoints) - 1:
                mapPos += 1
                standPoint = self._changeMapPos(mapPos)
            else:
                notChange = True
            cooldown(2)
            # 如果有广告弹窗，则关闭
            closePopupWindow()
            # 30 分钟没挖到矿 跳出循环
            if datetime.datetime.now().timestamp() - self._lastMineTime > 60 * 11:
                self.mark = False


# 大窗口
if __name__ == '__main__':
    time.sleep(0.2)
    print("start task....")
    Mine().mineMain()
    # 挖完矿关机

    print("结束挖矿")
