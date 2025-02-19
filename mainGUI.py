import ctypes
import win32com.client
# from win32com.client import Dispatch  # import moudles 第一次运行python -m pip install pywin32

from 升级 import 升级建筑
from 常用函数 import *
from 配置文件 import *

# 加载注册com组件的dll
免注册dll = ctypes.windll.LoadLibrary(R"op-0.4.5_with_model/tools.dll")
# 调用免注册dll中的setupA函数注册opdll
是否注册成功 = 免注册dll.setupA(bytes(R"op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
# 创建op对象
op = win32com.client.Dispatch("op.opsoft")


def 窗口调用(调用该方法的窗口):
    global op
    """
    在gui中使用多线程方式调用这个函数,即可开始执行脚本,需要给一个参数,你在哪一个窗口调用的,调用该方法的窗口,用于调用来打印脚本的运行状态.如何需要停止这个函数,调用该方法的窗口
    调用该方法的窗口.要求脚本停止设置未True即可
    本函数还有一个行为就是,将一些模拟器的状态返回到窗口类的变量中
                调用该方法的窗口.op=op
                窗口类.顶层窗口句柄=雷电模拟器运行信息[1]["顶层窗口句柄"]
                调用该方法的窗口.绑定窗口句柄 = 雷电模拟器运行信息[1]["绑定窗口句柄"]
    """

    打印状态 = 调用该方法的窗口.打印状态
    # 这是一些初始化信息，通常无需用户配置，故不写在配置文件
    进攻完毕次数 = 0
    找不到夜世界船的次数 = 0
    开始执行脚本时间 = time.time()
    当前金币 = -1
    当前圣水 = -1
    刷墙成功次数 = 0
    未绑定过窗口 = True

    def 点击(x, y, 延时=300):
        op.MoveTo(x, y)
        op.LeftClick()
        op.Delay(延时)

    def 关闭游戏(原因=None):
        subprocess.run(
            雷电模拟器安装目录 + "ldconsole.exe killapp  --index " + 雷电模拟器索引 + " --packagename \"" + 部落冲突包名 + "\"",
            shell=True)
        time.sleep(1)

        if 原因 is not None:
            打印状态(原因)

    正常结束上一轮打鱼而进入新一轮打鱼 = False  # 用于判断是否跳过前面的开模拟器,开游戏等操作,该变量会在循环超时,一直找不到夜世界船关闭游戏是置为False

    while True:  #循环进攻
        if 调用该方法的窗口.要求脚本停止 is True:
            打印状态("脚本已停止")
            return

        if 一直执行 is False:
            if time.time() - 开始执行脚本时间 > 需要执行多少秒:
                关闭游戏("到时间了")
                exit()
        #第一次循环和正常非正常结束循环的情况.则进入这个if,启动模拟器和游戏,和修复模拟器最小化情况
        if 正常结束上一轮打鱼而进入新一轮打鱼 is False:
            模拟器状态 = subprocess.run(雷电模拟器安装目录 + "ldconsole.exe list2", encoding='gbk',
                                        stdout=subprocess.PIPE)
            雷电模拟器运行信息 = 将雷电模拟器命令行返回信息解析为字典(模拟器状态.stdout)

            if 雷电模拟器运行信息[1]["绑定窗口句柄"] == 0:
                #启动模拟器并打开游戏
                subprocess.run(
                    雷电模拟器安装目录 + "ldconsole.exe launchex  --index " + 雷电模拟器索引 + " --packagename \"" + 部落冲突包名 + "\"",
                    shell=True)

                while True:  # 循环判断模拟器是否启动成功
                    模拟器状态 = subprocess.run(雷电模拟器安装目录 + "ldconsole.exe list2", encoding='gbk',
                                                stdout=subprocess.PIPE)
                    雷电模拟器运行信息 = 将雷电模拟器命令行返回信息解析为字典(模拟器状态.stdout)

                    if 雷电模拟器运行信息[1]["绑定窗口句柄"] == 0:
                        打印状态("等待模拟器启动")
                        continue
                    else:
                        打印状态("模拟器启动完毕")
                        break
            else:
                #模拟器如果已经启动了,就直接开游戏,这里有一个不好的地方是没有判断游戏是不是开启了,暴力直接打开游戏.因为如果不是因为错误关闭游戏的话新一轮打鱼游戏是已经开了的
                #进入这一个的情况有,用户干预,模拟器打开游戏未打卡;循环超时,计数器过大导致的关闭游戏
                subprocess.run(
                    雷电模拟器安装目录 + "ldconsole.exe runapp  --index " + 雷电模拟器索引 + " --packagename \"" + 部落冲突包名 + "\"",
                    shell=True)

            #为绑定窗口则绑定窗口
            # if op.IsBind() == 0:
            if 未绑定过窗口:
                是否成功绑定 = op.BindWindow(雷电模拟器运行信息[1]["绑定窗口句柄"], "dx2", "windows", "windows", 1)
                # 等待绑定窗口完成
                op.Delay(500)
                调用该方法的窗口.op = op
                调用该方法的窗口.顶层窗口句柄 = 雷电模拟器运行信息[1]["顶层窗口句柄"]
                调用该方法的窗口.绑定窗口句柄 = 雷电模拟器运行信息[1]["绑定窗口句柄"]
                打印状态("绑定窗口:" + str(是否成功绑定))
                未绑定过窗口 = False

            #判断窗口是否被最小化
            雷电模拟器是否最小化 = op.GetWindowState(雷电模拟器运行信息[1]["顶层窗口句柄"], 3)
            if 雷电模拟器是否最小化 == 1:
                打印状态("窗口已经最小化了,修改为还原状态")
                op.SetWindowState(雷电模拟器运行信息[1]["顶层窗口句柄"], 5)

            else:
                打印状态("没有最小化,脚本可以正常工作")

        打印状态("等待进入夜世界主界面")
        打印状态(
            "##########新一轮打鱼,目前是第" + str(进攻完毕次数) + f"次打鱼完毕了.刷墙成功了{刷墙成功次数}##########")
        # op.Capture(0, 0, 2000, 2000, "aaa1.bmp")
        # 判断循环是否超时间
        循环开始时间 = time.time()
        循环是否超时 = False
        升级建筑物致命错误次数 = 0
        while True:  #判断登录状态循环
            # 查找宝石数量旁边的宝石确定登录状态
            result, x, y = op.FindPic(752, 9, 789, 154, 目前脚本工作目录 + r"\img\宝石.jpg", "000000", 0.92, 0)
            # 找到了,证明已经登录,跳出循环
            if result != -1:
                break

            if time.time() - 循环开始时间 > 循环最大等待秒数:
                循环是否超时 = True
                关闭游戏("重启游戏,原因是一直没有成功登录！已经等待了" + str(循环最大等待秒数) + "秒")
                正常结束上一轮打鱼而进入新一轮打鱼 = False
                break
        #如果因为超时而关闭游戏,则回到循环开头,开游戏,进行下一次开游戏,打鱼等操作
        if 循环是否超时 is True:
            continue

        打印状态(f"成功进入夜世界主界面")
        打印状态(f"当前升级建筑时致命性错误次数为{升级建筑物致命错误次数}")

        #拉远视距
        for _ in range(20):
            op.KeyPressChar("f5")
        op.Delay(500)

        #获取当前金币圣水数量
        识别到的金币圣水字符串 = op.OcrEx(610, 15, 789, 89, "ffffff", 0.7)
        识别到的金币圣水字符串.replace(",", "")
        段落列表 = 识别到的金币圣水字符串.split('|')
        识别的列表 = []
        for 段落 in 段落列表:
            分割的片段 = 段落.split(',')
            识别的列表.append(分割的片段)

        try:
            if int(识别的列表[0][1]) < int(识别的列表[1][1]):
                当前金币 = int(识别的列表[0][2])
                当前圣水 = int(识别的列表[1][2])
            else:
                当前金币 = int(识别的列表[1][2])
                当前圣水 = int(识别的列表[0][2])
                打印状态(f"当前的金币为{识别的列表[1][2]},圣水为{识别的列表[0][2]}")
        except:
            打印状态("本次识别金币,圣水出错,当前未更新金币圣水,将打印上一次识别的结果或默认值")

        打印状态(f"当前的金币为{当前金币},圣水为{当前圣水}")

        是否因为多次找不到船而关闭了游戏 = False
        #通过船判断领取圣水地方
        a, x, y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\船.jpg", "000000", 0.5, 0)
        if x != -1:
            # 点击车
            点击(x - 79, y + 35)
            # 点击收集
            点击(605, 471)
            op.Delay(1000)
            # 关闭领取界面
            点击(699, 103)
        else:
            打印状态("没有找到夜世界的船")
            找不到夜世界船的次数 += 1
            if 找不到夜世界船的次数 > 10:
                关闭游戏("关闭游戏,原因:一直找不到夜世界的船")
                是否因为多次找不到船而关闭了游戏 = True
                正常结束上一轮打鱼而进入新一轮打鱼 = False
        #多次找不到船,游戏已经关闭,回到循环开始,重新进行下一次打鱼
        if 是否因为多次找不到船而关闭了游戏:
            continue

        # 必须升级建筑物在找夜世界船后面,因为升级建筑会去第二世界,导致找不到船
        while 进攻完毕次数 % 5 == 0:
            if 当前圣水 < 至少多少圣水开始刷墙:
                打印状态(f"留{至少多少圣水开始刷墙}圣水,不刷墙了")
                break

            if 当前金币 < 至少多少金币开始刷墙:
                打印状态(f"留{至少多少金币开始刷墙}金币,不刷墙了")
                break
            if 是否开启刷墙 is False:
                打印状态("刷墙已关闭,跳过刷墙")
                break

            if 升级建筑物致命错误次数 > 10:
                打印状态("多次升级建筑失败,本次运行跳过升级建筑")
                break
            else:
                升级信息, 是否致命错误, 建筑物需要资源, 资源类型 = 升级建筑(op, "城墙")
                # print(升级信息, 是否致命错误, 建筑物需要资源, 资源类型)

                if 是否致命错误 is True:
                    升级建筑物致命错误次数 += 1

                if "升级了" in 升级信息:
                    刷墙成功次数 += 1
                    continue
                else:
                    #刷墙完毕,或者不能刷墙退出升级建筑判断,等待一下,因为有时候游戏没反应过来,到时出兵失败
                    op.Delay(500)
                    break
        打印状态("开始搜索敌人,准备进攻")
        #点击进攻
        点击(58, 536, 700)
        #点击立即寻找
        点击(600, 380)

        # 判断循环是否进入战斗界面
        循环开始时间 = time.time()
        循环是否超时 = False
        while True:
            if time.time() - 循环开始时间 > 循环最大等待秒数:
                循环是否超时 = True
                关闭游戏(
                    "重启游戏,原因是一直卡白云或者某处,导致一直没进入战斗界面！已经等待了" + str(
                        循环最大等待秒数) + "秒")
                正常结束上一轮打鱼而进入新一轮打鱼 = False
                break

            # _, x, y = op.FindPic(0, 0, 2000, 2000,目前脚本工作目录 + r"\img\强化药水.jpg", "0", 0.9, 0)
            # _, x, y = op.FindPic(0, 0, 257, 115, 目前脚本工作目录 + r"\img\举报.bmp", "000000", 0.8, 0)
            _, x, y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\更换兵种箭头.bmp",
                                                 "000000", 0.6, 0)

            if x == -1:
                continue
            else:
                打印状态("开始进攻")
                break

        # 如果因为超时而关闭游戏,则回到循环开头,进行下一次开游戏,打鱼等操作
        if 循环是否超时 is True:
            continue

        识别到的剩余兵力字符 = op.OcrEx(20, 500, 2000, 2000, "ffffff-303030", 0.7)
        #print(识别到的剩余兵力字符)
        x, y = 寻找第一个非零x坐标(识别到的剩余兵力字符)
        点击(x, y)

        points = [(14, 309), (366, 37), (764, 311), (375, 473)]
        for 出兵所在直线 in range(4):
            line_equations = 计算相邻点所确定的直线(points)
            出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)], 出兵所在直线, 9)
            for 出兵点的元组 in 出兵点:
                点击(出兵点的元组[0], 出兵点的元组[1], 100)

        #点击选择英雄
        点击(47, 545)

        #出英雄
        点击(55, 299)

        #放英雄技能
        op.Delay(3000)
        点击(42, 554)

        第二场战斗是否已经开始 = False
        循环开始时间 = time.time()
        循环是否超时 = False
        while True:  #本循环有两个判断,判断是否存在第二次战斗和是否出现回营按钮
            if time.time() - 循环开始时间 > 180:
                循环是否超时 = True
                关闭游戏("重启游戏,原因为因为战斗好久没结束,或一直没有开始第二场战斗.已经等待了" + str(180) + "秒")
                正常结束上一轮打鱼而进入新一轮打鱼 = False
                break

            #如果第二次战斗还没打就判断两个,否则就一直判断回营图标的出现
            if 第二场战斗是否已经开始 == False:
                _, 换兵箭头x, 换兵箭头y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\更换兵种箭头.bmp",
                                                     "000000", 0.6, 0)

                if 换兵箭头x != -1:

                    循环开始时间 = time.time()  #因为开始第二场战斗,重置等待回营的超时时间,从现在重新计算等待时间
                    第二场战斗是否已经开始 = True  #确保下一次不判断,
                    打印状态("第二场次战斗")
                    #88,500,577,542

                    op.Delay(3000)
                    #识别兵种的数量4x等字符位置,确定还有剩余兵力的兵种,以点击
                    识别到的剩余兵力字符 = op.OcrEx(20, 500, 2000, 2000, "ffffff-303030", 0.7)
                    # print(识别到的剩余兵力字符)
                    x, y = 寻找第一个非零x坐标(识别到的剩余兵力字符)
                    点击(x, y)

                    points = [(14, 309), (366, 37), (764, 311), (375, 473)]
                    for 出兵所在直线 in range(4):
                        line_equations = 计算相邻点所确定的直线(points)
                        出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)],
                                                  出兵所在直线, 9)
                        for 出兵点的元组 in 出兵点:
                            点击(出兵点的元组[0], 出兵点的元组[1], 100)

                    # 点击选择英雄
                    点击(47, 545)

                    # 出英雄
                    点击(55, 299)

                    # 放英雄技能
                    op.Delay(3000)
                    点击(42, 554)

            _, 回营x, 回营y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\回营.jpg", "0", 0.6, 0)
            if 回营x == -1:
                continue
            else:
                打印状态("回营")
                点击(回营x, 回营y)
                进攻完毕次数 += 1
                打印状态("进攻完毕了" + str(进攻完毕次数) + "次")
                正常结束上一轮打鱼而进入新一轮打鱼 = True
                点击(回营x, 回营y)
                #多点击一次回营,以免速度太快没点到
                op.Delay(500)
                点击(回营x, 回营y)
                break

        # 如果因为超时而关闭游戏,则回到循环开头,进行下一次开游戏,打鱼等操作
        if 循环是否超时 is True:
            continue
