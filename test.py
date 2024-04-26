import pyautogui

from mhxy import *
import time
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

if __name__ == '__main__':
    list1 = [1, 2]
    print(isinstance(list1, list))
    # input_out = input("你好：")
    pyautogui.PAUSE = 1
    # 坐标校准
    init()
    time.sleep(3)
    # Util.doubleClick(-4.4, 4)
    # baixiaoxianzi = pyautogui.locateCenterOnScreen(r'resources/taskLink/' + route + 'low_neidan.png',
    #                                                # collect_caiji
    #                                                region=(frame.left, frame.top, frame.right, frame.bottom),
    #                                                confidence=0.9)
    # print(baixiaoxianzi)
    # pyautogui.leftClick(baixiaoxianzi.x, baixiaoxianzi.y)
    Util.leftClick(17.5, 12.8)
    # pyautogui.moveTo(840, 883)
    # pyautogui.leftClick(840, 883)
    x, y = pyautogui.position()
    positionStr = '鼠标坐标点（X,Y）为：{},{}'.format(str(x).rjust(4), str(y).rjust(4))
    print(positionStr)
    # pyautogui.moveTo(863, 526)
    # raw_request = 'GET /search?sourceid=chrome&ie=UTF-8&q=ergterst HTTP/1.1\r\nHost: www.google.com\r\nConnection: keep-alive\r\nAccept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\r\nUser-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.45 Safari/534.13\r\nAccept-Encoding: gzip,deflate,sdch\r\nAvail-Dictionary: GeNLY2f-\r\nAccept-Language: en-US,en;q=0.8\r\n'
    # request = parse_request(raw_request)
    # print(request)
    # print('\n')
    # print(request.keys())
    # time.sleep(3)
    # aa = pyautogui.locateAllOnScreen('resources/ghost/test.png',region=(0,0,2000,2000),confidence=0.8)
    # b = list(aa)
    # for pos in b:
    #     print(pos)
    #     print(len(b))
    # windowsList = pyautogui.getWindowsWithTitle('雷电模拟器')
    # window = windowsList[0]
    # left = window.left
    # top = window.top
    # width = window.width
    # height = window.height
    # print(str(left)+'--'+str(top)+'--'+str(width)+'--'+str(height))