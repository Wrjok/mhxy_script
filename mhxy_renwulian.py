from mhxy import *

value_goods_list = [
    r'resources/tasklink/valuegoods/baitan_fenhen.png',
    r'resources/tasklink/valuegoods/baitan_huixin.png',
    r'resources/tasklink/valuegoods/baitan_huyou.png',
    r'resources/tasklink/valuegoods/baitan_jianjia.png',
    r'resources/tasklink/valuegoods/baitan_jiaojian.png',
    r'resources/tasklink/valuegoods/baitan_jiaoke.png',
    r'resources/tasklink/valuegoods/baitan_juci.png',
    r'resources/tasklink/valuegoods/baitan_kanpo.png',
    r'resources/tasklink/valuegoods/baitan_lianhuan.png',
    r'resources/tasklink/valuegoods/baitan_liaoran.png',
    r'resources/tasklink/valuegoods/baitan_lingshen.png',
    r'resources/tasklink/valuegoods/baitan_qixi.png',
    r'resources/tasklink/valuegoods/baitan_shanzou.png',
    r'resources/tasklink/valuegoods/baitan_shengjie.png',
    r'resources/tasklink/valuegoods/baitan_shunshi.png',
    r'resources/tasklink/valuegoods/baitan_wuwei.png',
    r'resources/tasklink/valuegoods/baitan_yinshang.png',
    r'resources/tasklink/valuegoods/baitan_yufa.png',
    r'resources/tasklink/valuegoods/baitan_ziran.png',
    r'resources/tasklink/valuegoods/jinlan_baitan.png',
    r'resources/tasklink/valuegoods/meigui_baitan.png',
    r'resources/tasklink/valuegoods/shoujue_baitan.png'
]


class TaskLink:
    is_buy = False  # 遇传说物品默认不买
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

    # 智能传说流程
    def smart_legend(self):
        cooldown(1)
        # 点击挂机位置
        Util.leftClick(12.4, 1.6)
        cooldown(0.5)
        Util.leftClick(12.4, 1.6)
        cooldown(0.5)
        # 点击推荐地图开始挂机
        Util.leftClick(10.8, 9.9)

        t = datetime.datetime.now().timestamp()  # 传说流程起始时间，超过20分钟结束任务
        t2 = datetime.datetime.now().timestamp()  # 自动挂机起始时间，超过20分钟结束任务
        while True:
            cooldown(10)
            print('-------开始检查传说任务--------')
            jiao_baobao = Util.locateCenterOnScreen(r'resources/tasklink/' + route + 'jiao_baobao.png')
            if jiao_baobao is not None:
                pyautogui.leftClick(jiao_baobao.x, jiao_baobao.y)
                print('-------上交物品，传说流程结束--------')
                break
            else:
                closePopupWindow()

            auto_battle = Util.locateCenterOnScreen(r'resources/ghost/' + route + 'battleFlag2.png')
            if auto_battle is not None:
                t2 = datetime.datetime.now().timestamp()

            # 当前时间
            now = datetime.datetime.now().timestamp()
            if now - t > 60 * 20:
                print('-------超过20分钟，传说流程结束--------')
                self.is_buy = True
                break
            if now - t2 > 60 * 2:
                print('-------超过2分钟，自动进入战斗--------')
                cooldown(0.5)
                # 点击挂机位置
                Util.leftClick(12.4, 1.6)
                cooldown(0.5)
                # 点击推荐地图开始挂机
                Util.leftClick(10.8, 9.9)

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
            # 判断是否需要进入传说
            pos = Util.locateCenterOnScreen(value_goods_list)
            print('传说物品位置：', pos)
            cooldown(0.5)
            jiao_baobao = Util.locateCenterOnScreen(r'resources/tasklink/' + route + 'jiao_baobao.png')
            if pos is not None and jiao_baobao is None:
                if not self.is_buy:
                    print('-------检测到物品开始传说任务--------')
                    closePopupWindow()
                    self.smart_legend()
                    t = datetime.datetime.now().timestamp()
                else:
                    self.is_buy = False
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
