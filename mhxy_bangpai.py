from mhxy_renwulian import *


class _MissionType:

    def complete(self, locate, **kwargs):
        # 点击任务选项
        pyautogui.leftClick(locate.x, locate.y)


class _Fanwen(_MissionType):
    _noSubmitList = []

    def __init__(self) -> None:
        super().__init__()
        self.pic = r'resources/bangpai/fanwen.png'


class _Wupin(_MissionType):
    _noSubmitList = []

    def __init__(self) -> None:
        super().__init__()
        self.pic = [r'resources/bangpai/wupin.png', r'resources/bangpai/shangjiao.png', r'resources/bangpai/wupin2.png']

    def complete(self, locate, **kwargs):
        if kwargs['itemIdx'] == 0 or kwargs['itemIdx'] == 2:
            shangchen = Util.locateCenterOnScreen(r'resources/bangpai/shangchen.png') is not None
            # 选择第二个商品（防止商品被买）
            # 顺势上交
            if shangchen:
                Util.leftClick(-7, 8)
                pyautogui.leftClick(locate.x, locate.y)
                cooldown(2)
                Util.leftClick(-5, -5)
            else:
                pyautogui.leftClick(locate.x, locate.y)
        else:
            pyautogui.leftClick(locate.x, locate.y)


class _Battle(_MissionType):
    def __init__(self) -> None:
        super().__init__()
        self.pic = [r'resources/bangpai/fanwen.png', r'resources/bangpai/qiecuo.png']

    def complete(self, locate, **kwargs):
        # 点击战斗后退出战斗
        pyautogui.leftClick(locate.x, locate.y)


class _Hanhua(_MissionType):
    def __init__(self) -> None:
        super().__init__()
        self.pic = r'resources/bangpai/hanhua.png'


class _Xunluo(_MissionType):

    def completeMark(self):
        # 完成一次战斗
        pass


class _Guaji(_Xunluo):
    def complete(self, locate, **kwargs):
        # 每次战斗后15秒不再次进入战斗 现在是不断点击追踪
        pass


class Bangpai:
    # 其他类型不断点击追踪做就完了，找不到特征判断
    _mayMissionList = [_Wupin(), _Battle(), _Fanwen(), _Hanhua()]

    # 有特征图片的任务
    def _findPic(self):
        itemIdx = None
        for idx, each in enumerate(self._mayMissionList):
            if each.pic is None:
                continue
            locate = None
            if isinstance(each.pic, list):
                for iid, item in enumerate(each.pic):
                    locate = pyautogui.locateCenterOnScreen(item, confidence=0.9)
                    itemIdx = iid
                    if locate is not None:
                        break
            else:
                locate = pyautogui.locateCenterOnScreen(each.pic, confidence=0.9)
            if locate is not None:
                return idx, locate, itemIdx
        return None, None, None

    def _finish(self):
        return pyautogui.locateCenterOnScreen(r'resources/bangpai/finish.png', confidence=0.9) is not None

    def do(self, chaseWin):
        while not self._finish():
            pyautogui.leftClick(chaseWin[0], chaseWin[1])
            idx, locate, itemIdx = self._findPic()
            while locate is None:
                if battling():
                    cooldown(4)
                idx, locate, itemIdx = self._findPic()
                cooldown(1)
                if locate is None:
                    # 没法判断特征图片的任务都能通过不断点击追踪完成
                    pyautogui.leftClick(chaseWin[0], chaseWin[1])
                cooldown(1)

            self._mayMissionList[idx].complete(locate, itemIdx=itemIdx)
            cooldown(1)

    def do_bang_pai(self):
        closePopupWindow()
        print('--------开始帮派任务-----------')
        clickIconPicIfExist(r'resources/bangpai/' + route + 'plus.png')
        clickIconPicIfExist(r'resources/bangpai/' + route + 'bangpai.PNG')
        cooldown(0.5)
        Util.leftClick(-1.9, -5.5)
        cooldown(0.5)
        Util.leftClick(5.6, -4.4)
        clickIconPicIfExist(r'resources/bangpai/' + route + 'qianwang.PNG')
        clickIconPic(r'resources/bangpai/' + route + 'lingqu.PNG', 3)
        clickIconPicIfExist(r'resources/bangpai/' + route + 'huzi.PNG')

        t = datetime.datetime.now().timestamp()
        while True:
            cooldown(1)
            closePopupWindow()
            pic = [r'resources/bangpai/' + route + 'qinglong.PNG', r'resources/bangpai/' + route + 'qinglong.PNG',
                   r'resources/bangpai/' + route + 'zhuque.PNG', r'resources/bangpai/' + route + 'xuanwu.PNG']
            create_team = Util.locateCenterOnScreen(pic, 0.8)
            print('点击帮派任务栏位置：', create_team)
            if create_team is not None:
                pyautogui.leftClick(create_team.x, create_team.y)
                t = datetime.datetime.now().timestamp()
            clickIconPicIfExist(r'resources/bangpai/' + route + 'renwu.PNG')
            clickIconPicIfExist(r'resources/bangpai/' + route + 'use.PNG')
            clickIconPicIfExist(r'resources/bangpai/' + route + 'qiechuo.PNG')
            clickIconPicIfExist(r'resources/bangpai/' + route + 'buy_baobao.png')
            clickIconPicIfExist(r'resources/bangpai/' + route + 'jiao_baobao.png')
            t2 = datetime.datetime.now().timestamp()
            # 超过三分钟没有检测到任务，停止循环
            if t2 - t > 60 * 3:
                print('停止帮派任务')
                break
        print('------帮派任务结束--------')


# 大窗口
if __name__ == '__main__':
    pyautogui.PAUSE = 0.5
    input_out = input('1帮派，2任务链，3全部，请选择：')
    print("请在5秒内激活窗口")
    time.sleep(5)
    task_type = int(input_out)
    print("start task....")
    init()
    if task_type == 1:
        Bangpai().do_bang_pai()
    elif task_type == 2:
        TaskLink().taskLink()
    else:
        Bangpai().do_bang_pai()
        TaskLink().taskLink()

