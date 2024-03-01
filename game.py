import curses
import random
import time

testing = False

food_age = 500
food_number = 10

stdsrc = curses.initscr()
curses.noecho()
curses.cbreak()
stdsrc.keypad(True)
stdsrc.nodelay(True)
curses.curs_set(False)

maxl = curses.LINES - 1
maxc = curses.COLS - 1


score=0


world = []
player_l = player_c = 0
food = []
enemy = []

def random_place():
    a = random.randint(0, maxl)
    b = random.randint(0, maxc)
    while world[a][b] != ' ':
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)
    return a, b

def init():
    global player_c, player_l
    for i in range(-1, maxl+1):
        world.append([])
        for j in range(-1, maxc+1):
            world[i].append(' 'if random.random() > 0.03 else '.')
           
    for i in range(food_number):
        fl,fc = random_place()
        fa = random.randint(food_age, food_age*5)
        food.append((fl,fc,fa))
       
    for i in range (3):
        el, ec = random_place()
        enemy.append((el,ec))
   
    player_l , player_c = random_place()
       
           
def in_range(a, min, max):
    if a > max:
        return max
    if a < min:
        return min
    return a


def draw():
   
    for i in range(maxl):
        for j in range(maxc):
            stdsrc.addch(i,j,world[i][j])
    stdsrc.addstr(1,1, f"Score: {score}")
    #showing the food        
    for f in food:
         fl, fc, fa = f
         stdsrc.addch(fl, fc , '🍕')  
   
    for e in enemy:
         l, c = e
         stdsrc.addch(l,c,"💣")
   
    #showing the player    
    stdsrc.addch(player_l, player_c, '✈')  
         
    stdsrc.refresh()  

def move(c):
    ''' get one of asdw and move eoward that direction'''
   
    global player_l , player_c
    if c == 'w' and world[player_l-1][player_c] != '.':
        player_l -= 1
    elif c == 's' and world[player_l+1][player_c] != '.':
        player_l += 1
    elif c == 'a' and world[player_l][player_c-1] != '.':
        player_c -= 1
    elif c == 'd'and world[player_l][player_c+1] != '.':
        player_c += 1  
     
    player_l = in_range(player_l, 0, maxl - 1)
    player_c = in_range(player_c, 0, maxc - 1)  
   
   

def check_food():
    global score
    for i in range(len(food)):
        fl, fc, fa = food[i]
        fa -= 1
        if fl == player_l and fc == player_c:
            score += 10
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
           
        if fa <= 0:
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
           
        food[i] = (fl, fc, fa)
           
           
def move_enemy():
    global playing
    for i in range (len(enemy)):
        l, c = enemy[i]
        if random.random()>0.8:
            if l > player_l:
                l-= 1
        if random.random()>0.8:
            if c > player_c:
                c -= 1
        if random.random()>0.8:
            if l < player_l:
                l += 1
        if random.random()>0.8:
            if c < player_c:
                c += 1
            l += random.choice([0, 1, -1])
            c += random.choice([0, 1, -1])
            l = in_range(l, 0, maxl-1)
            c = in_range(c, 0, maxc -1)
            enemy[i] = (l, c)
        if l == player_l and c == player_c and not testing:
            stdsrc.addstr(maxl//2, maxc//2, "YOU DIED!")
            stdsrc.refresh()
            time.sleep(3)
            playing = False



init()

playing = True
while playing:
    try:
        c = stdsrc.getkey()
    except:
        c = ' '
    if c in 'asdw':
        move(c)
    elif c == 'q':
        playing = False
    check_food()
    move_enemy()
    time.sleep(0.05)
    draw()

stdsrc.addnstr(maxl//2, maxc//2, "Thanks for Playing!")
stdsrc.refresh()
time.sleep(2)
stdsrc.clear()
stdsrc.refresh()