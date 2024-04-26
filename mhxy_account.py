from mhxy_baotu import *
from mhxy_yabiao import *
from mhxy_mijing import *

class _AccountInfo:
    name = ''
    role = ''

    def __init__(self, name, role):
        self.name = name
        self.role = role

Account_Role_List = [
    _AccountInfo(r'resources/account/' + route + 'rjwu01.png', r'resources/account/' + route + 'shi-tuo.png'),
    _AccountInfo(r'resources/account/' + route + 'mobile.png', r'resources/account/' + route + 'fang-cun.png'),
    _AccountInfo(r'resources/account/' + route + 'mobile.png', r'resources/account/' + route + 'pu-tuo.png'),
    _AccountInfo(r'resources/account/' + route + 'mobile.png', r'resources/account/' + route + 'difu.png')
]

class SwitchAccount:
    def change_account(self, levelType, name, role):
        print('-----开始切换账号，levelType：-----', levelType)
        closePopupWindow()
        clickIconPicIfExist(r'resources/account/' + route + 'plus.png')
        clickIconPicIfExist(r'resources/account/' + route + 'system.png')
        clickIconPicIfExist(r'resources/account/' + route + 'switch.png')
        clickIconPicIfExist(r'resources/account/' + route + 'logout.png')
        cooldown(3)
        # 判断账号是否成功登出
        sanjiaofu = Util.locateCenterOnScreen(r'resources/account/' + route + 'sanjiaofu.png')
        if sanjiaofu is None:
            print("---未检测到三角符，登出失败，重新登出------")
            self.change_account(levelType, name, role)

        clickIconPicIfExist(r'resources/account/' + route + 'sanjiaofu.png')
        # 选择账号
        clickIconPicIfExist(name)
        clickIconPicIfExist(r'resources/account/' + route + 'enterGame.png')
        cooldown(2)
        clickIconPicIfExist(r'resources/account/' + route + 'wo-zhidao.png')
        cooldown(3)
        Util.leftClick(17.5, 12.8)
        clickIconPicIfExist(r'resources/account/' + route + 'role.png')
        clickIconPicIfExist(role)
        # 等待游戏载入时间2秒
        cooldown(5)
        # 开始执行任务
        baotu = Baotu()
        baotu.baotu()
        yabiao = Yabiao()
        yabiao.yabiao()
        mijing = Mijing()
        mijing.mijing(levelType)
        print("------"+role+":单人任务已完成------")

    def change_account_circle(self, levelType):
        for role in Account_Role_List:
            self.change_account(levelType, role.name, role.role)

# 大窗口
if __name__ == '__main__':
    input_out = input("角色等级？0：89，1：69。请输入：")
    print("请手动激活窗口（5秒内）")
    time.sleep(5)
    print("start task....")
    init()
    SwitchAccount().change_account_circle(int(input_out))
