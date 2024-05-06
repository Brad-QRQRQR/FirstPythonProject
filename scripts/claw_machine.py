def check_input(saying, e_message, input_range = False): #無限輸入，並做例外處理
    if input_range:
        while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
            try:
                x, y = input(saying).split(' ')
                x = int(x); y = int(y)
                if 1 <= x < 10000 and 1 <= y < 10000:
                    return x, y
                else: #不在範圍內，則提醒使用者
                    print(e_message[0])
                    print()
            except ValueError: #當將x和y轉成int時的錯誤
                print(e_message[1])
                print()
            except Exception: #避免有預期外的錯誤，導致程式直接崩潰
                print('未知錯誤')
                print()
    else:
        while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
            try:
                x, y = input(saying).split(' ')
                x = int(x); y = int(y)
                return x, y
            except ValueError: #當將x和y轉成int時的錯誤
                print(e_message)
                print()
            except Exception: #避免有預期外的錯誤，導致程式直接崩潰
                print('未知錯誤')
                print()

def range_check(saying, e_message):
    return check_input(saying, e_message, input_range = True)

def min_order_x(doll_cdn, n): #x座標由小排到大
    for i in range(n-1): #最差情況要重複排n-1次
        for j in range(n-1):
            if doll_cdn[0][j] > doll_cdn[0][j+1]: #右邊比左邊小，右邊的座標換到左邊
                doll_cdn[0][j], doll_cdn[0][j+1] = doll_cdn[0][j+1], \
                                                doll_cdn[0][j]        
                doll_cdn[1][j], doll_cdn[1][j+1] = doll_cdn[1][j+1], \
                                                doll_cdn[1][j]
    return doll_cdn

def min_order_y(doll_cdn, n): #y座標由小排到大，但x座標維持由小到大
    for i in range(n-1): #最差情況要重複排n-1次
        for j in range(n-1):
            if doll_cdn[0][j] == doll_cdn[0][j+1] and \
               doll_cdn[1][j] > doll_cdn[1][j+1]: #右邊比左邊小，右邊的座標換到左邊
                doll_cdn[0][j], doll_cdn[0][j+1] = doll_cdn[0][j+1], \
                                                doll_cdn[0][j]        
                doll_cdn[1][j], doll_cdn[1][j+1] = doll_cdn[1][j+1], \
                                                doll_cdn[1][j]
    return doll_cdn

def calculate(doll_cdn, n, y): #計算最多能抓到幾個娃娃
    dolls = []
    start = 0
    start_count = 0
    done = True
    while done:
        doll_count = 0 #初始化
        start_count = 0 #初始化
        for j in range(start, n):
            if doll_cdn[0][start] == doll_cdn[0][j]: #x座標相同才進行y座標判斷
                if doll_cdn[1][start] + y >= doll_cdn[1][j]: #判斷在夾子寬內是否可以夾起
                    doll_count = doll_count + 1
                    start_count = start_count + 1
                else:
                    break
            else: #沒有的話就下一次迴圈
                continue
        
        dolls.append([
            doll_count, \
            (doll_cdn[0][start], doll_cdn[1][start]) 
        ])
        start = start + start_count #為下一次迴圈從x座標不同者開始

        if start >= n: #如果全部都已經搜索完畢，終止迴圈
            done = False
    return dolls

def max_order_dolls(dolls): #找出可夾取的最多娃娃的位置及數量
    for i in range(len(dolls) - 1):
        for j in range(len(dolls) - 1):
            if dolls[j][0] < dolls[j + 1][0]:
                dolls[j][0], dolls[j + 1][0] = dolls[j + 1][0], dolls[j][0]
                dolls[j][1], dolls[j + 1][1] = dolls[j + 1][1], dolls[j][1]
    return dolls

def output(dolls): #輸出結果
    print('夾子左端點座標在'+str(dolls[0][1])+'可以抓到最多的娃娃為'+str(dolls[0][0])+'個')
    for i in dolls[1:]:
        if i[0] == dolls[0][0]: #如與排序後的第一個相同者也印出
            print('夾子左端點座標在'+str(i[1])+'可以抓到最多的娃娃為'+str(i[0])+'個')

def claw_machine(): #主程式
    saying1 = '請輸入娃娃數和夾子寬：'
    e_msg1 = ['娃娃數以及夾子寬過大，兩者都只能介於1~10000之間', '請輸入娃娃數與夾子寬（皆為整數），中間以半形空格間隔']
    saying2 = '請輸入娃娃座標：'
    e_msg2 = '請輸入xy座標（皆為整數），中間以半形空格間隔'

    #輸入娃娃數、夾子寬、娃娃座標
    n, y = range_check(saying1, e_msg1)
    print()
    doll_cdn = [[0]*n for i in range(2)]
    for i in range(0, n):
        doll_cdn[0][i], doll_cdn[1][i] = check_input(saying2, e_msg2)
    
    #將娃娃座標排序
    doll_cdn = min_order_x(doll_cdn, n)
    doll_cdn = min_order_y(doll_cdn, n)
    
    #計算可抓到最多娃娃的位置以及數量
    dolls = calculate(doll_cdn, n, y)
    dolls = max_order_dolls(dolls)
    
    #輸出
    output(dolls)

if __name__ == '__main__':
    claw_machine()