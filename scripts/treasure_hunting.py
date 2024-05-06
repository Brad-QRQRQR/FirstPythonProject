from random import randint #導入random模組

def check_input(saying, input_range, error_msg): #無限輸入，並做例外處理
    while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
        try:
            choice = input(saying)
            if choice not in input_range: #如果不是可用的指令，提醒使用者
                print(error_msg)
                print()
                continue #跳過本次迴圈，不會回傳變數choice
            return choice
        except Exception: #避免有預期外的錯誤，導致程式直接崩潰
            print('未知錯誤')
            print()

def build_map(now): #建立尋寶地圖
    treasure_map = [None, now]
    for i in range(2 ** 10 - 1):
        treasure_map.append(randint(0, 3))
    return treasure_map

def user_choose(now, minus, health_points): #接收往左或往右的指令，並更新玩家位置
    print('現在生命值：' + str(health_points))
    choice = check_input('要走左邊還是右邊（0左1右）：', '01', '只能輸入0和1喔')
    print()
    if choice == '0': #往左邊
        for i in range(1, 1023+1):
            if now == i:
                minus = now #記錄使用者上一次的位置，為了在與怪物對決逃跑時能夠回到上一個位置
                now = now + now
                break
    else: #往右邊
        for i in range(1, 1023+1):
            if now == i:
                minus = now + 1 #記錄使用者上一次的位置，為了在與怪物對決逃跑時能夠回到上一個位置
                now = now + (now + 1)
                break
    return now, minus

def user_act(now, treasure_map, treasure, act, health_points, arms): #輸出情境並要求使用者輸入應對
    if treasure_map[now] == 0: #遇到怪物
        print('你現在手上有'+str(arms)+'個武器')
        act = check_input('遇到了怪物，你要（3逃跑4決鬥）：', '34', '只能輸入3和4喔')
        print()
    elif treasure_map[now] == 1: #撿到武器
        arms += 1
        print('你拿到了武器')
        print()
    elif treasure_map[now] == 2: #撿到回復藥水
        if health_points == 2:
            print('你喝了回復藥水，好像沒什麼效果，不過喝完之後稍稍振奮精神')
        else:
            health_points += 1
            print('你拿到了回復藥水，生命值+1')
        print()
    else: #拿到寶藏
        treasure = treasure + 1
        print('你拿到了寶藏！')
        print()
    return act, treasure, health_points, arms

def judge(act, health_points, now, minus, arms): #如果遇到怪獸，判斷應對結果
    if act != None: #如果有遇到怪獸，才判斷應對
        if act == '3': #逃跑
            now = now - minus
            print('你倉皇而逃，僥倖沒有受傷')
            print()
        elif act == '4': #決鬥
            if arms <= 0:
                health_points -= 1
                print('你狼狽地敗給了怪獸，落魄逃離現場，不知身處何處，生命值-1')
                print()
            else:
                arms -= 1
                print('你成功擊退怪獸，繼續前進')
                print()
    else: #沒有遇到怪獸則跳過
        pass
    return now, health_points

def result(health_points, now, treasure, done): #判斷生命值是否歸零或遊戲結束
    if health_points == 0: #生命值歸零
        print('你在遠大的旅途中，不幸傷亡慘重，生命值歸零')
        done = False
    elif now >= 512: #遊戲結束
        if treasure == 0:
            print('你走出了層層迷宮，卻沒有拿到寶藏，真是可惜')
        else:
            print('你走出了層層迷宮，收穫了'+str(treasure)+'個寶藏')
        done = False
    else: #還沒結束，繼續遊戲
        done = True
    return done


#主程式
def treasure_hunting():
    treasure = 0
    arms = 0
    health_points = 2
    
    now = 1
    minus = 0 #用來記錄使用者上一步的位置
    
    done = True
    treasure_map = build_map(now)

    while done:
        act = None #初始化
        
        now, minus = user_choose(now, minus, health_points)
        act, treasure, health_points, arms = user_act(now, treasure_map, treasure, act, health_points, arms)
        now, health_points = judge(act, health_points, now, minus, arms)
        
        done = result(health_points, now, treasure, done)

if __name__ == '__main__':
    treasure_hunting()