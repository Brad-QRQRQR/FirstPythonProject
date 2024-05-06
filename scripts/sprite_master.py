from random import randint #導入random模組

def check_input(saying, input_range, e_message): #無限輸入，並做例外處理
    while True: #無限迴圈，如果使用者輸入錯誤則會要求再次輸入
        try:
            x = input(saying)
            if x not in input_range: #不在可選精靈內，則提醒使用者
                print(e_message)
                print()
                continue #跳過本次迴圈，不會回傳變數x
            return x
        except Exception: #避免有預期外的錯誤，導致程式直接崩潰
            print('未知錯誤')
            print()

def user_select_sprite(sprite_number, use_sprite, sprite_name, user_select = True): #選擇精靈
    if user_select:
        player_sprite = check_input('請選擇要使用的精靈（1火精靈2水精靈3木精靈）：', sprite_number, '不在可選精靈範圍內喔')
        who = '我方'
    else:
        player_sprite = str(randint(1, 3))
        who = '敵方'
    
    for i in sprite_number: #在串列中找尋使用精靈，i為str
        if i == player_sprite:
            print(who + use_sprite[int(i) - 1])
    
    if player_sprite == '1':
        return sprite_name[0]
    elif player_sprite == '2':
        return sprite_name[1]
    elif player_sprite == '3':
        return sprite_name[2]

def enemy_select_sprite(sprite_number, use_sprite, sprite_name): #敵人亂數生成使用精靈
    return user_select_sprite(sprite_number, use_sprite, sprite_name, user_select = False)

def user_attack(sprite_name, skill, user_attack = True): #選擇攻擊招式
    if user_attack:
        for i in skill: #列印招式
            if i == None:
                continue
            else:
                print(sprite_name[int(i) - 1], end = ' ')
        print()
        choice = check_input('請選擇要使用的招式：', skill, '不在可選招式範圍喔')
        who = '我方使用'
    else:
        while True:
            choice = str(randint(1, 5))
            if choice in skill:
                break
        who = '敵方使用'
    
    for i in skill: #在串列中找尋使用招式
        if i == choice:
            print(who + sprite_name[int(i) - 1]) #輸出使用精靈
            skill.insert(int(i) - 1, None)
            skill.remove(i)

    choice = int(choice)
    return choice

def enemy_attack(sprite_name, skill): #敵人亂數生成攻擊招式
    return user_attack(sprite_name, skill, user_attack = False)

def judge(user_health, enemy_health, user_choice, enemy_choice): #判斷回合中誰造成敵方傷害
    #比大小
    if user_choice < enemy_choice:
        user_health = user_health - 1
        print('玩家血量減一')
    elif user_choice == enemy_choice:
        print('平手')
    elif user_choice > enemy_choice:
        enemy_health = enemy_health - 1
        print('敵方血量減一')
    return user_health, enemy_health

def health_report(user_health, enemy_health): #列印雙方血量壯態
    print('玩家血量：' + str(user_health))
    print('敵人血量：' + str(enemy_health))

def result(user_skill, user_health, enemy_health): #判斷誰輸誰贏
    #其中一方生命者歸零則輸
    if user_health == 0:
        print('敵方贏了')
        done = False
        return done
    elif enemy_health == 0:
        print('玩家贏了')
        done = False
        return done
    
    #沒有一方歸零的話，看雙方剩餘血量誰比較多
    count = 0
    for i in user_skill:
        if i == None:
            count = count + 1
        if count == 5:
            if user_health > enemy_health:
                print('敵方贏了')
                done = False
                return done
            elif user_health < enemy_health:
                print('玩家贏了')
                done = False
                return done
            elif user_health == enemy_health:
                print('平手')
                done = False
                return done
    done = True
    return done

def sprite_master(): #主程式
    done = True
    
    #精靈
    sprite_number = ['1', '2', '3']
    use_sprite = ['使用火精靈', '使用水精靈', '使用木精靈']
    
    #技能
    user_skill = ['1', '2', '3', '4', '5']
    enemy_skill = ['1', '2', '3', '4', '5']
    fire_sprite = ['普通攻擊(1)', '火光四濺(2)', '巨火怒號(3)', '酷熱地獄(4)', '藍焰燃天(5)'] 
    water_sprite = ['普通攻擊(1)', '水箭瀰漫(2)', '雷雨交加(3)', '水簾蓋地(4)', '呼天喚雨(5)']
    wood_sprite = ['普通攻擊(1)', '荊棘叢生(2)', '欣欣向榮(3)', '根結盤繞(4)', '天崩地裂(5)']
    sprite_name = [fire_sprite, water_sprite, wood_sprite]
    
    #玩家與敵人初始生命值
    user_health = 3
    enemy_health = 3
    
    #選擇精靈
    user_sprite = user_select_sprite(sprite_number, use_sprite, sprite_name)
    enemy_sprite = enemy_select_sprite(sprite_number, use_sprite, sprite_name)
    print()
    
    while done:
        #選擇招式
        user_choice = user_attack(user_sprite, user_skill)
        enemy_choice = enemy_attack(enemy_sprite, enemy_skill)
        print()
        
        #判斷回合勝利
        user_health, enemy_health = judge(
                                        user_health, enemy_health, \
                                        user_choice, enemy_choice
                                        )

        #輸出雙方血量狀況
        health_report(user_health, enemy_health)
        print()
        
        #判斷終局結果，如未終局則繼續
        done = result(user_skill, user_health, enemy_health)

if __name__ == '__main__':
    sprite_master()