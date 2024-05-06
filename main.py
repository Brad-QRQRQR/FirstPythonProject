import os, sys

#導入六支程式
from scripts.collatz import collatz
from scripts.sprite_master import sprite_master
from scripts.treasure_hunting import treasure_hunting
from scripts.claw_machine import claw_machine
from scripts.expression_translation import expression_translation
from scripts.solitaire import solitaire

done = True
introduction = '離開遊戲（0）' \
            '考拉茲猜想（1）' \
            '精靈大師（2）' \
            '尋寶（3）' \
            '夾娃娃（4）' \
            '運算式轉換（5）' \
            '數字接龍（6）'
choice_saying = '請問要玩哪一個遊戲呢：'
choice_range = ['0', '1', '2', '3', '4', '5', '6']
e_message = '不是可接受的選擇喔'

def game_message(introduction): #列印出遊戲介紹
    print(introduction)

def wait(): #遊戲結束後，停留任意時間供使用者查看最後的遊戲結果
    input('按任意鍵繼續')
    os.system('cls')

def check_input(saying, input_range, e_messge): #輸入，並做例外處理
    while True:
        try:
            choice = input(saying)
            if choice in input_range: #在可選遊戲範圍內時，回傳使用者選擇
                return choice
            else: #如果不是，提醒使用者錯誤
                print(e_messge)
                continue
        except Exception: #避免有預期外的錯誤，導致程式直接崩潰
            print('未知錯誤')

def main(done, introduction, saying, range, e_message): #主程式
    while done:
        game_message(introduction)
        choice = check_input(saying, range, e_message)
        if choice == '0':
            print()
            print('感謝遊玩')
            input('按任意鍵退出')
            sys.exit()
        elif choice == '1':
            print()
            collatz()
            wait()
        elif choice == '2':
            print()
            sprite_master()
            wait()
        elif choice == '3':
            print()
            treasure_hunting()
            wait()
        elif choice == '4':
            print()
            claw_machine()
            wait()
        elif choice == '5':
            print()
            expression_translation()
            wait()
        elif choice == '6':
            print()
            solitaire()
            wait()

if __name__ == '__main__':
    main(done, introduction, choice_saying, choice_range, e_message)