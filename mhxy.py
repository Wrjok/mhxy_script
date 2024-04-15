import datetime
import json
import time

import pyautogui
from pygetwindow import PyGetWindowException

try:
    import pytesseract
except ImportError:
    pass
import pyperclip


class Frame:
    left = 0
    top = 0
    right = 0
    bottom = 0

    def __init__(self, left, top):
        self.left = left
        self.top = top

    def __str__(self):
        return "left:" + str(self.left) + " top:" + str(self.top) + " right:" + str(self.right) + " bottom:" + str(
            self.bottom)


# 窗口左上侧位置
frame = Frame(0, 0)

# 窗口固定大小
originSize = [1040, 807]
niceSize = (907, 707)
# 鼠标到变化态需要向做微调距离
resizeOffset = (10, 7)
frameSize = [0, 0]

frameSizeCm = [28.1, 21.8]

# 是否发生跨天
_newDayClick = False

# 分辨率路由
route = ''


class _Teammate:
    _type = 1
    _pic = 2

    def __init__(self, _type, _pic):
        self._type = _type
        self._pic = _pic


# 助战图标配置
TEAMMATE_LIST = [
    # 物理输出
    _Teammate(1, r'resources/ghost/wuLi.png'),
    # 法术输出
    _Teammate(2, r'resources/ghost/faShu.png'),
    # 治疗
    _Teammate(3, r'resources/ghost/zhiLiao.png'),
    # 封印
    _Teammate(4, r'resources/ghost/fengYin.png'),
    # 辅助
    _Teammate(5, r'resources/ghost/fuZhu.png')
]


# relativeSize = lambda x, y: (frameSize[0] * x / frameSizeCm[0],
#                              frameSize[1] * y / frameSizeCm[1])
# relativeX2Act = lambda xcm: frameSize[0] * xcm / frameSizeCm[0]
# relativeY2Act = lambda ycm: frameSize[1] * ycm / frameSizeCm[1]

def relativeSize(x, y):
    return (frameSize[0] * x / frameSizeCm[0],
            frameSize[1] * y / frameSizeCm[1])


def relativeX2Act(xCm):
    return frameSize[0] * abs(xCm) / frameSizeCm[0]


def relativeY2Act(yCm):
    return frameSize[1] * abs(yCm) / frameSizeCm[1]


def winRelativeX(x):
    return frame.right - relativeX2Act(x) if x < 0 else frame.left + relativeX2Act(x)


def winRelativeY(y):
    return frame.bottom - relativeY2Act(y) if y < 0 else frame.top + relativeY2Act(y)


def winRelativeXY(x, y):
    return (winRelativeX(x), winRelativeY(y))


# 百分比方法不是很实用，因为窗口大小变化，ui并不是百分比变化的
def percentX(x):
    return frameSize[0] * (abs(x) / 100)


def percentY(y):
    return frameSize[1] * (abs(y) / 100)


def winPercentX(x):
    return frame.right - percentX(x) if x < 0 else frame.left + percentX(x)


def winPercentY(y):
    return frame.bottom - percentY(y) if y < 0 else frame.top + percentY(y)


def winPercentXY(x, y):
    return (winPercentX(x), winPercentY(y))


def battling(battleingPic=r'resources/origin/zhen_tian.png'):
    return Util.locateOnScreen(battleingPic) is not None


# 关闭任务侧边栏
def closeMission():
    Util.leftClick(-7, 4.3)
    # print("关闭任务侧边栏")
    # pyautogui.hotkey('alt', 'p')


# 结束战斗后进行操作
def escapeBattleDo(do, battleingPic=r'resources/small/enter_battle_flag.png', battleDoFunc=None):
    alreadyDo = False
    battleDo = False
    while True:
        if not battling(battleingPic=battleingPic):
            battleDo = False
            if not alreadyDo:
                # 脱离战斗
                print("escape battle")
                cooldown(1.5)
                alreadyDo = True
                do()
                cooldown(2)
            else:
                # 战斗外当已完成了动作
                cooldown(2)
        else:
            # 战斗中
            alreadyDo = False
            if not battleDo:
                # 进入战斗
                print("enter battle")
                cooldown(3)
                battleDo = True
                # 进入战斗后做一次
                if battleDoFunc is not None:
                    battleDoFunc()
                cooldown(2)
            else:
                # 战斗中当已完成了动作
                cooldown(2)


def doUtilFindPic(pic, do):
    def find():
        if isinstance(pic, list):
            for idx, each in enumerate(pic):
                locate = Util.locateCenterOnScreen(each)
                if locate is not None:
                    return locate, idx
            return None, None
        else:
            return Util.locateCenterOnScreen(pic), None

    locate, idx = find()
    # 最少执行一次
    while locate is None:
        do(locate, idx=idx)
        locate, idx = find()
        cooldown(1)
    return locate, idx


# 副本式任务
def doNormFubenMission():
    def reach():
        return Util.locateCenterOnScreen(r'resources/fuben/select.png')

    # 流程任务
    def do():
        reachPos = reach()
        while reachPos is None:
            def clickSkip():
                Util.leftClick(-1, -2)

            # 找不到头像则正在对话点击头像位置跳过 直到找到头像位置
            doUtilFindPic(r'resources/avatar.png', clickSkip)
            reachPos = reach()
            cooldown(2)
        pyautogui.leftClick(reachPos.x, reachPos.y)

    escapeBattleDo(do)


def cooldown(second):
    time.sleep(max(0, second))


class Util:
    @staticmethod
    def locateCenterOnScreen(pic, same=0.9):
        if isinstance(pic, list):
            res = None
            for i in pic:
                res = pyautogui.locateCenterOnScreen(i,
                                                     region=(frame.left, frame.top, frame.right, frame.bottom),
                                                     confidence=same)
                if res is not None:
                    print('图片名称', i)
                    return res
            return res
        else:
            # pyautogui.locateOnWindow 只能有一个标题所以不可取
            return pyautogui.locateCenterOnScreen(pic,
                                                  region=(frame.left, frame.top, frame.right, frame.bottom),
                                                  confidence=same)

    @staticmethod
    def locateOnScreen(pic):
        # return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom))
        return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom), confidence=0.9)

    @staticmethod
    def leftClick(x, y):
        pyautogui.leftClick(winRelativeX(x), winRelativeY(y))

    @staticmethod
    def doubleClick(x, y):
        pyautogui.doubleClick(winRelativeX(x), winRelativeY(y))

    @staticmethod
    def click(x, y, clicks, buttons):
        pyautogui.click(winRelativeX(x), winRelativeY(y), clicks=clicks, button=buttons)

    @staticmethod
    def write(text):
        # 不支持中文
        # pyautogui.typewrite(text)
        pyperclip.copy(text)
        # print(pyperclip.paste())
        # pyautogui.hotkey('Ctrl', 'v')
        pyautogui.keyDown('Ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('Ctrl')
        pyautogui.keyUp('v')
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')

    @staticmethod
    def ocr(region, type=None):
        # 识别汉字
        img = pyautogui.screenshot(
            region=(winRelativeX(region[0]), winRelativeY(region[1]), winRelativeX(region[2]), winRelativeY(region[3])))
        # 只检测数字
        config = None
        # 中文
        lang = 'chi_sim'
        if type == 'number':
            config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
        elif type == "eng":
            lang = 'eng'
        text = pytesseract.image_to_string(img, lang=lang, config=config)
        return text


def resize2Nice(windows):
    while not windows.isActive:
        cooldown(1)
    pyautogui.moveTo(windows.right - resizeOffset[0], windows.bottom - resizeOffset[1])
    pyautogui.dragTo(windows.left + (niceSize[0] - resizeOffset[0]), windows.top + (niceSize[1] - resizeOffset[1]),
                     duration=1.3)


def newDayCloseCheck(do):
    global _newDayClick
    if datetime.datetime.now().hour == 0 and (not _newDayClick):
        _newDayClick = True
        cooldown(8)
        newDay = Util.locateCenterOnScreen(r'resources/origin/new_day.png')
        do(newDay)
        return True
    return False


def init(idx=0, resizeToNice=False):
    global frameSizeCm

    def getFrameSize(idx):
        windows = None
        while windows is None or windows.left < 0:
            windowsList = pyautogui.getWindowsWithTitle('梦幻西游：时空')
            windowsList = list(filter(lambda x: x.left > 0, windowsList))
            windowsList.sort(key=lambda x: x.left)

            moniqiWin = pyautogui.getWindowsWithTitle("梦幻西游 - MuMu模拟器")
            if moniqiWin is not None:
                moniqiWin = list(filter(lambda x: x.left > 0, moniqiWin))
                moniqiWin.sort(key=lambda x: x.left)
                for each in moniqiWin:
                    windowsList.append(each)

            if len(windowsList) > 0:
                windows = windowsList[idx]
            cooldown(0.5)
        frameSize[0] = windows.width
        frameSize[1] = windows.height
        return windows

    # pyautogui.PAUSE = 1  # 调用在执行动作后暂停的秒数，只能在执行一些pyautogui动作后才能使用，建议用time.sleep
    pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常

    # location1 = Util.locateOnScreen(r'resources/mine_head.png')
    windows = getFrameSize(idx)
    print("窗口大小:", frameSize)
    print("窗口大小CM:", frameSizeCm)
    if resizeToNice:
        resize2Nice(windows)
        windows = getFrameSize(idx)
        print("调整后窗口大小:", frameSize)
    if resizeToNice or frameSize[0] == niceSize[0]:
        frameSizeCm = [frameSizeCm[0] * (niceSize[0] / originSize[0]), frameSizeCm[1] * (niceSize[1] / originSize[1])]
        print("调整后窗口大小CM:", frameSizeCm)
    frame.left = windows.left
    frame.top = windows.top
    frame.right = frame.left + frameSize[0]
    frame.bottom = frame.top + frameSize[1]
    print("窗口四角位置:", frame)
    try:
        windows.activate()
        print('窗口激活成功！')
    except PyGetWindowException:
        print('窗口激活失败！', PyGetWindowException)
        pass


def parse_request(request):
    raw_list = request.split("\r\n")
    # GET /search?sourceid=chrome&ie=UTF-8&q=ergterst HTTP/1.1
    fst = raw_list[0].split(' ')
    request = {"method": fst[0], "url": fst[1]}
    for index in range(1, len(raw_list)):
        item = raw_list[index].split(":")
        if len(item) == 2:
            request.update({item[0].lstrip(' '): item[1].lstrip(' ')})
    return request


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def __avgShoujueNum(n=4):
    last = 0
    for i in range(n - 1, -1, -1):
        last = n / (n - i) + last
    return last


# 关闭各种弹窗广告任务（可扩展）
# 广告图列表
NORM_ADVERT_LIST = [
    # “X” 符号
    r'resources/common/big_delete.png',
    r'resources/common/delete.png',
    r'resources/common/red_delete.png',
    r'resources/ghost/team_delete.png',
    r'resources/ghost/delete_discount.png',
    r'resources/ghost/delete_bigmap.png',
    r'resources/ghost/delete_white.png',
    r'resources/ghost/delete_reDian.png',
    r'resources/ghost/delete_remind.png',
    # “取消” 符号
    r'resources/ghost/cancel.png',
    r'resources/ghost/cancel2.png'
]


def closePopupWindow():
    advertList = NORM_ADVERT_LIST
    count = 0
    while count < 5:
        for advert in advertList:
            point = pyautogui.locateCenterOnScreen(advert,
                                                   region=(frame.left, frame.top, frame.right, frame.bottom),
                                                   confidence=0.9)
            if point is not None:
                print("发现弹窗广告：", advert)
                # 点击叉掉
                pyautogui.PAUSE = 0.5
                pyautogui.leftClick(point.x, point.y)
            count += 1


# 通用方法，找到元素则点击(必须点击)
def clickIconPic(pic, wait):
    t = datetime.datetime.now().timestamp()
    flag = True
    while flag:
        position = None
        if isinstance(pic, list):
            for i in pic:
                position = pyautogui.locateCenterOnScreen(i,
                                                          region=(frame.left, frame.top, frame.right, frame.bottom),
                                                          confidence=0.9)
                if position is not None:
                    break
        else:
            position = pyautogui.locateCenterOnScreen(pic,
                                                      region=(frame.left, frame.top, frame.right, frame.bottom),
                                                      confidence=0.9)
        if position is not None:
            pyautogui.leftClick(position.x, position.y)
            flag = False
        cooldown(1)
        t2 = datetime.datetime.now().timestamp()
        # 指定时间内还没点击到则跳出循环
        if t2 - t > wait:
            flag = False
            return True


# 通用方法，找到元素则点击(有则点击)
def clickIconPicIfExist(pic):
    cooldown(0.5)
    create_team = pyautogui.locateCenterOnScreen(pic,  # collect_caiji
                                                 region=(frame.left, frame.top, frame.right, frame.bottom),
                                                 confidence=0.9)
    print("点击-" + str(pic) + "-位置：", create_team)
    if create_team is not None:
        pyautogui.leftClick(create_team.x, create_team.y)
        return True
    return False


def clickIconPicByCount(pic, sleep, maxCount):
    count = 0
    while count < maxCount:
        count += 1
        cooldown(sleep)
        create_team = pyautogui.locateCenterOnScreen(pic,  # collect_caiji
                                                     region=(frame.left, frame.top, frame.right, frame.bottom),
                                                     confidence=0.9)
        if create_team is not None:
            pyautogui.leftClick(create_team.x, create_team.y)
