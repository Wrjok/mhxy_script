from mhxy import *


class Hanhua:
    def hanhua(self, content):
        while True:
            # 开始喊话
            clickIconPicIfExist(r'resources/fuben/hanhua.png')
            clickIconPicIfExist(r'resources/fuben/currentSelect.png')
            clickIconPicIfExist(r'resources/fuben/currentUnSelect.png')
            Util.write(content)
            clickIconPicIfExist(r'resources/fuben/agreeButton.png')
            clickIconPicIfExist(r'resources/fuben/closeDialog.png')
            cooldown(5)

    def hanhuaWithText(self):
        cooldown(3)
        Util.write("哈哈哈哈哈")
        # while True:
        #     Util.leftClick(5, 2)
        #     cooldown(1)
        #     Util.write("哈哈哈哈哈")
        #     cooldown(1)
        #     Util.leftClick(13, 2)
        #     cooldown(2)


# 喊话
if __name__ == '__main__':
    input_out = input("喊话内容。请输入：")
    print("请手动激活窗口（5秒内）")
    time.sleep(5)
    print("start task....")
    init()
    Hanhua().hanhua(input_out)
