def check_input(saying, input_range, e_message): #無限輸入，並做例外處理
    def not_in_range(infix): #判斷是否為可用的運算子或運算元
        for i in infix:
            if i not in input_range:
                return True

    def incorrect_infix(infix, i, operand, operator):
        if infix[i] in operator and infix[i + 1] in operator: #運算子相連
            if infix[i] not in ['(', ')', '-'] and infix[i + 1] not in ['(', ')', '-']: #非括號或負號
                return True
            elif infix[i] in '-' and infix[i + 1] in operator: #負號
                return False
            else:
                return False
        elif infix[i] in operand and infix[i + 1] in operand: #運算元相連
            return True
        else:
            return False

    def true_infix(infix): #判斷是否為中序運算式
        operand = 'qwertyuiopasdfghjklzxcvbnm'
        operator = '+-*/^=()'

        if infix[0] in [o for o in operator if o not in ['(', ')']]: #運算式最前頭為除了括號的運算子
            return False
        elif infix[len(infix) - 1] in [o for o in operator if o not in ['(', ')']]: #運算式最尾端為除了括號的運算子
            return False
        
        for i in range(len(infix) - 1):
            if incorrect_infix(infix, i, operand, operator):
                return False
        return True

    while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
        try:
            infix = input(saying)
            
            if not_in_range(infix): #不在可輸入的運算元或運算子內，則提醒使用者
                print(e_message[0])
                print()
                continue #跳過本次迴圈，繼續詢問使用者
            
            if true_infix(infix): #判斷其是否為中序
                return infix
            else:
                print(e_message[1])
                print()
                continue #跳過本次迴圈，繼續詢問使用者
        except Exception: #避免有預期外的錯誤，導致程式直接崩潰
            print('未知錯誤')
            print()

#建立堆疊類別
class Stack:
    def __init__(self): #初始化
        self.stack = []

    def push(self, data):
        return self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def __str__(self):
        return '{0}'.format(self.stack)

    def __len__(self):
        return len(self.stack)

    def __getitem__(self, i):
        if self.stack != []:
            return self.stack[i]

def caculate(infix, postfix): #將前序轉後序
    stack = Stack()
    tmp = str() #在轉換過程中記錄上一次的運算符號，用來判斷接下來搜尋到的是否為負號

    #如果要放入堆疊的運算子優先權較低或相等，則回傳True
    def priority(operator):
        if operator == None:
            return 0
        elif operator in ['(']:
            return 5
        elif operator in ['n-']:
            return 4
        elif operator in ['^']:
            return 3
        elif operator in ['*', '/']:
            return 2
        elif operator in ['+', '-']:
            return 1

    def stack_pop(postfix):
        p = stack.pop()
        postfix += p if p != 'n-' else '-'
        return postfix

    #中序式轉後序式
    for i in infix:
        if tmp in ['+', '-', '*', '/', '^', '(', ')'] and i in '-': #運算元前有負號
            i = 'n' + i

        if i in ['+', '-', '*', '/', '^', 'n-', '(', ')']: #遇到運算子，要判斷優先權來push或pop
            if i == ')': #遇到右括號特殊處理
                while stack[-1] != '(':
                    postfix = stack_pop(postfix)
                stack.pop() #把左括號pop
                continue #右括號不放進堆疊，直接繼續搜尋下一個運算符號   
            while priority(i) <= priority(stack[-1]) and stack[-1] != '(': #判斷優先權，看是否要pop
                postfix = stack_pop(postfix)
            stack.push(i) #把運算子放進堆疊
        else: #運算元直接pop
            postfix += i
        tmp = i

    for _ in range(len(stack)): #將堆疊內剩餘的運算子pop
        if stack[-1] == '(':
            stack.pop()
        else:
            postfix = stack_pop(postfix)
    
    return postfix

def expression_translation(): #主程式
    input_range = 'qwertyuiopasdfghjklzxcvbnm+-*/^=()'
    e_msg = ['不是可辨別的運算式喔', '不正確的運算式']
    infix = check_input('請輸入一運算式：', input_range, e_msg)
    infix = list(infix)
    postfix = ''
    postfix = caculate(infix, postfix)
    print('其後序運算式為：'+postfix)

if __name__ == '__main__':
    expression_translation()