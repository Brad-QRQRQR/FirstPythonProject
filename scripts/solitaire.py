from random import randint #導入random模組
import os #導入os模組

def check_input(saying, input_range, e_message, split = False): #輸入並做例外處理
    if split: #一行多個變數輸入
        while True:
            try:
                x, y = input(saying).split(' ')
                if x not in input_range or y not in input_range:
                    print(e_message[0])
                    print()
                    continue
                x = int(x); y = int(y)
                return x, y
            except ValueError:
                print(e_message[1])
                print()
            except Exception:
                print(e_message[2])
                print()
    else:
        while True:
            try:
                act = input(saying)
                if act not in input_range:
                    print(e_message[0])
                    print()
                    continue
                return act
            except Exception:
                print(e_message[2])
                print()

def cdn_check_input(saying, input_range, e_message):
    return check_input(saying, input_range, e_message, split = True)

def act_check_input(saying, input_range, e_message):
    return check_input(saying, input_range, e_message)

#建立牌的類別
class Card:
    def __init__(self):
        self.card = None
        self.cover = False
    
    def cv(self): #覆牌
        self.cover = True
        return self.cover
    
    def op(self): #翻牌
        self.cover = False
        return self.cover
    
    def on_table(self): #列印於牌桌上時，判斷牌是翻牌還是覆牌
        if self.cover:
            return 0
        else:
            return self.card

#建立線的類別，管理牌桌上每一直排
class Line:
    def __init__(self):
        self.container = [None]*8
        for i in range(8):
            self.container[i] = Card()

    def __getitem__(self, i):
        return self.container[i]

    def insert(self, i, data): #變更牌的位置
        self.container[i].card = data.card
        self.container[i].cover = data.cover

    def put(self, i, data): #放牌
        self.container[i].card = data

    def result(self): #回傳某行是否為收集好的牌組
        c = 8
        for i in range(len(self.container)):
            if not self.container[i].cover:
                if c == self.container[i].card:
                    c -= 1
                    continue
                else:
                    return False
            else:
                return False
        return True

def build_game(table, cards): #建立牌桌
    for i in range(8):
        for j in range(4):
            index = randint(0, len(cards) - 1 + 20)
            if table[i][j-1].card == None and j - 1 >= 0:
                continue
            else:
                try:
                    table[i][j].card = cards[index]
                except IndexError:
                    continue
                table[i][j].cv()
    return table

def print_table(table): #列印牌桌
    print(' ' * 3, end = '')
    #列印橫軸
    for i in range(8):
        print('|' + ' ' + '\'' + str(i + 1) + '\'' + ' ', end = '') #6字元
    print()
    dash_number = (int((6 * 8 + 3) / 2))
    print('－' * dash_number)

    #列印縱軸
    for i in range(8):
        print('\'' + str(i + 1) + '\'', end = '') 
        #列印牌
        for j in range(8):
            if table[j][i].card == None:
                print('|' + ' '*5, end = '') #6字元
            else:
                print('|'+ ' '*2 + str(table[j][i].on_table()) + ' '*2, end = '') #6字元
        print()
        print('－' * dash_number)

def give_cards(player_cards, cards): #發給玩家手牌
    if cards != []: #手牌未滿三張即補充
        while True:
            if len(player_cards) < 3:
                i = randint(0, len(cards) - 1)
                player_cards.append(cards[i])
                cards.pop(i)
            else:
                break
    
    #列印手牌
    print('你的手牌：', end = '')
    for i in range(len(player_cards)):
        print(str(player_cards[i]), end = ' ')
    print()
    
    return player_cards, cards

def choose_act(table, player_cards, done, e_msg): #接收玩家指令，進行動作
    act = act_check_input('移牌（1）翻牌（2）出牌（3）移動牌組（4）離開遊戲（5）要執行：', '12345', e_msg)
    
    def move(): #移牌
        start_x, start_y = cdn_check_input('要移動的牌：', '12345678', e_msg)
        final_x, final_y = cdn_check_input('要移到的位置：', '12345678', e_msg)

        if table[start_x - 1][start_y - 1].card == None:
            print('要移動的位置上並沒有牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][start_y if start_y < 8 else 7].card != None and start_y < 8:
            print('只能從每一排的最底下移牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][start_y - 1].cover == True and table[start_y - 1][start_x - 1].card != None:
            print('要移動的牌為覆蓋狀態')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[final_x - 1][final_y - 1].card != None:
            print('移動到的位置上有牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][start_y - 1].card + 1 != table[final_x - 1][(final_y - 1) - 1].card \
            and (final_y - 1) - 1 >= 0 \
            and not table[final_x-1][(final_y - 1) - 1].cover:
            print('排序由上到下應為依序由大數到小')
            print()
            return choose_act(table, player_cards, done, e_msg)
        else:
            trans = Card()
            trans.card = table[final_x - 1][final_y - 1].card
            trans.cover = table[final_x - 1][final_y - 1].cover
            table[final_x - 1].insert(final_y - 1, table[start_x - 1][start_y - 1])
            table[start_x - 1].insert(start_y - 1, trans)
            return table, player_cards, done
    
    def op_card(): #翻牌
        po_x, po_y = cdn_check_input('要翻開的牌：', '12345678', e_msg)
        
        if table[po_x-1][po_y if po_y < 8 else 7].card != None:
            print('只能從每一排的最底下翻牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif not table[po_x - 1][po_y - 1].cover:
            print('牌已翻開')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[po_x - 1][po_y - 1].card == None:
            print('位置上沒有牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        else:
            table[po_x - 1][po_y - 1].op()
            return table, player_cards, done
    
    def put(): #出牌
        input_range = []
        for i in player_cards:
            input_range.append(str(i))
        putting = int(act_check_input('要放入的牌：', input_range, e_msg))
        po_x, po_y = cdn_check_input('位置：', '12345678', e_msg)

        if table[po_x - 1][(po_y - 1) - 1].card == None \
        and (po_y - 1) - 1 >= 0 \
        and not table[po_x - 1][(po_y - 1) - 1].cover: 
            print('要放入的位置上方不能為空')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif putting + 1 != table[po_x - 1][(po_y - 1) - 1].card \
        and not table[po_x - 1][(po_y - 1) - 1].cover \
        and table[po_x - 1][po_y - 2].card != None:
            print('排序由上到下應為依序由大數到小')
            print()
            return choose_act(table, player_cards, done, e_msg)
        else:
            for i in range(len(player_cards)):
                if player_cards[i] == putting:
                    player_cards.pop(i)
                    break
            table[po_x - 1].put(po_y - 1, putting)
            return table, player_cards, done
    
    def move_cards(): #移動牌組
        start_x, start_y = cdn_check_input('牌組底端座標：', '12345678', e_msg)
        start_x = int(start_x)
        start_y = int(start_y)
        top_y = int(act_check_input('此行牌組頂端y座標：', '12345678', e_msg))
        final_column = int(act_check_input('要移到哪行：', '12345678', e_msg))
        
        if table[start_x - 1][start_y - 1].card == None:
            print('牌組底端並沒有牌')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][start_y if start_y < 8 else 7].card != None:
            print('牌組底端必須為該行的底端')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif start_y - top_y <= 0:
            print('牌組頂端座標不行在牌組底端座標下面')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][start_y - 1].cover:
            print('牌組底端的牌不能為覆蓋狀態')
            print()
            return choose_act(table, player_cards, done, e_msg)
        elif table[start_x - 1][top_y - 1].cover:
            print('牌組頂端的牌不能為覆蓋狀態')
            print()
            return choose_act(table, player_cards, done, e_msg)
        else:
            for i in range(top_y, (start_y - 2) + 1): #由上而下檢視
                if table[start_x - 1][i].card - 1 != table[start_x - 1][i + 1].card:
                    print('非牌組')
                    print()
                    return choose_act(table, player_cards, done, e_msg)
                else:
                    continue
        
        #紀錄目的地底端的y座標
        final_y = 0
        for i in table[final_column - 1].container:
            if i.card == None:
                break        
            else:
                final_y += 1
        
        if (top_y - start_y) + (8 - final_y) > 8:
            print('牌組過長，超出桌面底端')
            print()
            return choose_act(table, player_cards, done, e_msg)
        
        #判斷目的地底端跟要移動的牌組底端能否接連
        if table[final_column - 1][final_y - 1].cover or table[final_column - 1][final_y - 1].card == None:
            pass
        else:
            if table[final_column - 1][final_y - 1].card - 1 != table[start_x - 1][top_y - 1].card:
                print('不能移到此行！牌序必須由上而下、由大排到小')
                print()
                return choose_act(table, player_cards, done, e_msg)
        
        #由上而下移動牌組
        for i in range(top_y - 1, (start_y - 1) + 1):
            table[final_column - 1].insert((final_y - 1) + 1, table[start_x - 1][i])
            table[start_x - 1].container[i] = Card()
            final_y += 1
        return table, player_cards, done

    def leave(): #離開遊戲
        done = False
        return table, player_cards, done

    if act == '1':
        return move()
    if act == '2':
        return op_card()
    if act == '3':
        return put()
    if act == '4':
        return move_cards()
    if act == '5':
        return leave()

def judge(table, complete): #判斷是否連為一線
    for i in range(8):
        if table[i].result():
            table[i] = Line() #初始化
            complete += 1
    return table, complete

def solitaire(): #主程式
    done = True

    e_msg = ['不是可接受的指令喔', '請輸入xy座標，以空格為分隔，中間空格為半形空格', '未知錯誤']
    
    cards = [1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, \
             1, 2, 3, 4, 5, 6, 7, 8, ]
    player_cards = []
    
    line1 = Line()
    line2 = Line()
    line3 = Line()
    line4 = Line()
    line5 = Line()
    line6 = Line()
    line7 = Line()
    line8 = Line()
    table = [line1, line2, line3, line4, line5, line6, line7, line8]
    
    complete = 0
    
    table = build_game(table, cards)

    while done:
        os.system('cls') #清理畫面
        print_table(table)
        player_cards, cards = give_cards(player_cards, cards)
        print('完成的牌組：', str(complete))
        table, player_cards, done = choose_act(table, player_cards, done, e_msg)
        table, complete = judge(table, complete)
        
        if complete == 8:
            done = False

if __name__ == '__main__':
    solitaire()