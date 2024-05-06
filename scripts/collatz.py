def check_input(): #無限輸入，並做例外處理
    while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
        try:
            n = input('請輸入一個數：')
            n = int(n)
            if n < 1: #如果n是負整數或0，提醒使用者錯誤
                print('1只接受正整數喔')
                print()
                continue #跳過本次迴圈，不會回傳變數 n
            return n
        except ValueError as e: #當將n轉成int時的錯誤
            print('只接受正整數')          
            print()
        except Exception: #避免有預期外的錯誤，導致程式直接崩潰
            print('未知錯誤')
            print()

def calculate(n, sequence): #計算
    while n > 1:
        sequence = sequence + str(n) + ', ' #將數值存到數列
        if n % 2 == 0: #n為偶數
            n = int(n / 2)
        else: #n為奇數
            n = int(3 * n + 1)
    sequence = sequence + str(n) + ', ' #將1存入數列 
    return sequence

def collatz(): #主程式
    sequence = ''
    n = 0
    print(
        '考拉茲猜想是仍未解決的數學問題\n'
        '內容是假設有一個正整數N\n'
        '如果是偶數，那麼N/2\n'
        '如果是奇數，那麼3*n + 1\n'
        '運算直到N為1\n'
        )
    n = check_input()
    sequence = calculate(n, sequence)
    print('數列：' + sequence + '...(4, 2, 1循環)') #輸出結果

if __name__ == '__main__':
    collatz()