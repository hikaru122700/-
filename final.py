def end():
    print(ans)
    for i in range(4):
        print(ans_buka[i])

    exit()


N = int(input())
A = [list(map(int, input().split())) for _ in range(N)]
sum_imp = 1 << 50
key_ind = -1
import time
from sortedcontainers import SortedSet, SortedList, SortedDict

ans_list = [[] for _ in range(5)]
place = [[] for _ in range(5)]
start_time = time.time()
ans = ''
loc = [[-1] * N for _ in range(N)]
D = 1 << 10  # 十分大きい数でクレーンで吊り上がっている数に適応
cost_A = [[-1] * N for _ in range(N)]
pass_list = []
tenntou_number = 0
lazyshoot = SortedSet()
# count_A = [0] * N
for i in range(N):
    for j in range(N):
        cost_A[i][j] = A[i][j] % 5

for i in range(N):
    if sum(cost_A[i]) < sum_imp:
        sum_imp = sum(cost_A[i])
        key_ind = i
recieve = [0] * N


def move_get(i, j, ti, tj):
    ri, rj = i, j
    if i != ti and j != 4:
        rj = j + 1
        ans = 'R'
    elif i > ti:
        ri = i - 1
        ans = 'U'
    elif i < ti:
        ri = i + 1
        ans = 'D'
    elif j > tj:
        rj = j - 1
        ans = 'L'
    elif j < tj:
        rj = j + 1
        ans = 'R'
    if len(place[0]) < len(place[1]) and place[1][len(place[0])] == [ri, rj]:
        return i, j, '.'
    return ri, rj, ans


def move_put(i, j, ti, tj):
    ri, rj = i, j
    if j > tj:
        rj = j - 1
        ans = 'L'
    elif j < tj:
        rj = j + 1
        ans = 'R'
    elif i > ti:
        ri = i - 1
        ans = 'U'
    elif i < ti:
        ri = i + 1
        ans = 'D'
    if len(place[0]) < len(place[1]) and place[1][len(place[0])] == [ri, rj]:
        return i, j, '.'
    return ri, rj, ans


# for i in range(N):
#     loc[i][0] = A[i].pop(0)
# print('loc:', loc)
inf = 1 << 60

DIJ = [(0, 1), (0, -1), (-1, 0), (1, 0)]
DIJ_mozi = 'RLUD'


def board_check_King(i, j):
    if 0 <= i < 5 and 0 <= j < 5:
        return True
    else:
        return False


def get_next_boll(x, y):
    '''
    もっとどん欲にしたい
    '''
    key = SortedList()
    for i in range(5):
        key.add([recieve[i], i])
    for _, k in key:
        if recieve[k] >= inf:
            continue
        for i in range(x, x + 5):
            i %= 5
            for j in [2, 1, 3, 0]:
                if N * k <= loc[i][j] <= recieve[k] + N * k:
                    return i, j

    box_place = -1
    importance = inf
    for i in range(N):
        if loc[i][0] == -1:
            continue
        if importance > loc[i][0] % 5:
            importance = loc[i][0] % 5
            box_place = i
    if box_place == -1:
        return -1, -1
    return box_place, 0


move_get_flag = False


def where_to_move(x, y, boll_num):
    for i in range(N):
        if recieve[i] >= inf:
            continue
        if N * i <= boll_num <= recieve[i] + N * i:
            return i, 4
    for i in range(x, x + 5):
        i %= 5
        for j in range(3, -1, -1):
            if i == x and j == y:
                continue
            if loc[i][j] == -1:
                return i, j
    ans_list.append(boll_num)
    pass_list.append(boll_num)
    return x, 4


def add_place(kind, S):
    if S == 'B':
        return
    before_x = place[kind][-1][0]
    before_y = place[kind][-1][1]
    if S == 'U':
        place[kind].append([before_x - 1, before_y])
    elif S == 'D':
        place[kind].append([before_x + 1, before_y])
    elif S == 'L':
        place[kind].append([before_x, before_y - 1])
    elif S == 'R':
        place[kind].append([before_x, before_y + 1])
    else:
        place[kind].append([before_x, before_y])


def stay(kind):
    x, y = place[kind][-1]
    place[kind].append([x, y])


def add_place_buka(kind, S):
    if S == 'B':
        return
    before_x, before_y = place[kind][-1]
    if S == 'U':
        if [before_x - 1, before_y] == place[0][len(place[kind])]:
            stay(kind)
            return False
        if kind == 3 and len(place[4]) > len(place[3]) \
                and [before_x - 1, before_y] == place[4][len(place[3])]:
            stay(kind)
            return False
        place[kind].append([before_x - 1, before_y])
    elif S == 'D':
        if [before_x + 1, before_y] == place[0][len(place[kind])]:
            stay(kind)
            return False
        if kind == 3 and len(place[4]) > len(place[3]) \
                and [before_x + 1, before_y] == place[4][len(place[3])]:
            stay(kind)
            return False
        place[kind].append([before_x + 1, before_y])
    elif S == 'L':
        if [before_x, before_y - 1] == place[0][-1]:
            stay(kind)
            return False
        place[kind].append([before_x, before_y - 1])
    elif S == 'R':
        if [before_x, before_y - 1] == place[0][-1]:
            stay(kind)
            return False
        place[kind].append([before_x, before_y + 1])
    else:
        place[kind].append([before_x, before_y])
    return True


def chenge_loc_get(x, y):
    tmp = loc[x][y]
    if y == 0 and len(A[x]) >= 1:
        loc[x][y] = A[x].pop(0)
    else:
        loc[x][y] = -1
    return tmp


def chenge_loc_put(x, y, boll_num):
    global tenntou_number
    if y == 4:
        if recieve[x] + 5 * x != boll_num:
            tenntou_number += boll_num - recieve[x] + 5 * x
        recieve[x] += 1
        ans_list[x].append(boll_num)
        if recieve[x] % 5 == 0:
            recieve[x] = inf
        if recieve == [inf] * 5:
            end()
        return
    loc[x][y] = boll_num


def buka_slide_Right4(x, y, kind, boll_num):
    '''
    今持ってるボールの情報も追加して考えたい
    '''
    king_x, king_y = place[0][-1]

    if loc[x][y + 1] != -1 or loc[x][y] == -1:
        return False
    if place[0][-1][0] == x and boll_num == -1:
        return False
    if place[3][-1][0] == x and len(place[3]) > len(place[4]) + 1:
        return False
    if place[3][-1][0] == x and abs(king_x - x) == 1 and king_y <= 3:
        return False
    if ans_buka[2][-1] == '.':
        return False

    boll_num = chenge_loc_get(x, y)
    chenge_loc_put(x, y + 1, boll_num)
    key = 'PRQL'
    ans_buka[kind - 1] += key
    for i in range(4):
        add_place(kind, key[i])
    return True


def buka_slide_Right3(x, y, kind, boll_num):
    '''
    pone4, kingと当たる可能性を排除する
    '''
    if loc[x][y + 1] != -1 or loc[x][y] == -1:
        return False
    if boll_num == -1 and abs(place[0][-1][0] - x) <= 1 and place[0][-1][
        1] <= 4:
        return False
    if boll_num != -1 and (place[0][-1] == [x, 4] or 0 <= place[0][-1][1] <= 1):
        return False
    if len(place[4]) > len(place[3]) + 1:
        return False
    if len(place[3]) + 1 < len(place[1]) and place[1][len(place[3])][0] == x:
        return False
    boll_num = chenge_loc_get(x, y)
    chenge_loc_put(x, y + 1, boll_num)
    key = 'PRQL'
    ans_buka[kind - 1] += key
    for i in range(4):
        add_place(kind, key[i])
    return True


def buka_slide_Upper(x, y, kind, boll_num):
    global ti, tj, direct3, direct4
    if x == 0:
        return False
    king_x, king_y = place[0][len(place[kind])]
    if len(place[kind]) <= 21:
        return False
    if kind == 1 and abs(x - 1 - king_x) + 5 - king_y <= 2:
        return False
    if kind == 4 and ans_buka[2][-1] == '.':
        return False
    if kind == 4 and direct4 == 'D':
        return False
    if kind == 3 and direct3 == 'D':
        return False
    if kind != 4:
        if loc[x][y] == -1 or loc[x - 1][y] != -1 or x <= loc[x][y] // 5:
            return False
    else:
        if loc[x][y] == -1 or loc[x - 1][y] != -1 or (
                x <= loc[x][y] // 5 and len(A[x]) == 0):
            return False
    if boll_num == -1 and (place[0][-1][0] == x and place[0][-1][1] <= y + 1):
        return False
    if boll_num == -1 and (
            place[0][-1][0] == x - 1 and place[0][-1][1] <= y + 2):
        return False
    if boll_num != -1 and x - 1 <= place[0][-1][0] <= x and place[0][-1][
        1] <= y:
        return False
    if kind == 3 and loc[x - 1][y - 1] != -1:
        return False
    if kind == 3 and x == place[4][-1][0] and len(place[4]) > len(place[3]):
        return False

    boll_num = chenge_loc_get(x, y)
    chenge_loc_put(x - 1, y, boll_num)
    key = 'PUQ'
    ans_buka[kind - 1] += key
    for i in range(len(key)):
        add_place(kind, key[i])
    return True


def buka_slide_Down(x, y, kind, boll_num):
    global direct3, direct4
    king_x, king_y = place[0][-1]
    if x == 4:
        return False
    if kind == 1 and abs(x + 1 - king_x) + 5 - king_y <= 2:
        return False
    if kind == 4 and ans_buka[2][-1] == '.':
        return False
    if kind == 4 and direct4 == 'U':
        return False
    if kind == 3 and direct3 == 'U':
        return False
    if kind != 4:
        if loc[x][y] == -1 or loc[x + 1][y] != -1 or x >= loc[x][y] // 5:
            return False
    else:
        if loc[x][y] == -1 or loc[x + 1][y] != -1 or not (
                x <= loc[x][y] // 5 and len(A[x]) == 0):
            return False
    if x <= place[0][-1][0] <= x + 1 and boll_num == -1:
        return False
    if kind == 3 and loc[x + 1][y - 1] != -1:
        return False
    if boll_num != -1 and x <= place[0][-1][0] <= x + 1 and place[0][-1][
        1] <= y:
        return False
    if kind == 3 and x == place[4][-1][0] and len(place[4]) > len(place[3]):
        return False
    boll_num = chenge_loc_get(x, y)
    chenge_loc_put(x + 1, y, boll_num)
    key = 'PDQ'
    ans_buka[kind - 1] += key
    for i in range(len(key)):
        add_place(kind, key[i])
    return True


direct4 = 'U'


def move_pone4(boll_num):
    '''
    right方向のみ動かすのではなく、上下方向にも動かしてみる
    '''
    global direct4
    pone4_x, pone4_y = place[4][-1]
    if pone4_x == 0 and direct4 == 'U':
        direct4 = 'D'
    elif pone4_x == 4 and direct4 == 'D':
        direct4 = 'U'
    if buka_slide_Upper(pone4_x, pone4_y, 4, boll_num):
        return
    if buka_slide_Down(pone4_x, pone4_y, 4, boll_num):
        return
    if buka_slide_Right4(pone4_x, pone4_y, 4, boll_num):
        return
    if add_place_buka(4, direct4):
        ans_buka[3] += direct4
    else:
        ans_buka[3] += '.'


direct3 = 'U'


def move_pone3(boll_num, flag3):
    global direct3
    pone3_x, pone3_y = place[3][-1]
    if pone3_x == 0 and direct3 == 'U':
        direct3 = 'D'
    elif pone3_x == 4 and direct3 == 'D':
        direct3 = 'U'
    if direct3 == 'U' and buka_slide_Upper(pone3_x, pone3_y, 3, boll_num):
        return
    if direct3 == 'D' and buka_slide_Down(pone3_x, pone3_y, 3, boll_num):
        return
    if buka_slide_Right3(pone3_x, pone3_y, 3, boll_num):
        return
    # print('len(place[3])', len(place[3]), ans_buka[2][len(place[3])-2])
    if add_place_buka(3, direct3):
        ans_buka[2] += direct3
    else:
        if place[3][-1] != place[0][-1]:
            ans_buka[2] += '.'
        else:
            if direct3 == 'U':
                direct3 = 'D'
            else:
                direct3 = 'U'
            if flag3:
                place[3] = place[3][:-1]
                move_pone3(boll_num, False)
            else:
                ans_buka[2] += 'B'
                place[3][-1] = [-1, -1]


def buka_shoot(x, y, kind, boll_num):
    num = loc[x][y]
    key_lst = []
    for i in range(5):
        key_lst.append(recieve[i] + 5 * i)

    goal = num // 5
    king_x, king_y = place[0][len(place[1])]
    to_x, to_y = get_next_boll(king_x, king_y)
    if num not in key_lst:
        return False
    if boll_num == -1:
        if min(x, goal) <= king_x <= max(x, goal) or \
                min(x, goal) <= to_x <= max(x, goal):
            return False
    else:
        if min(x, goal) <= king_x <= max(x, goal) or \
                min(x, goal) <= boll_num // 5 <= max(x, goal):
            return False
    boll_num = chenge_loc_get(x, y)
    '''
    上の行は消さない
    '''
    key = 'PR'
    if goal - x > 0:
        key += 'D' * (goal - x)
    if goal - x < 0:
        key += 'U' * (x - goal)
    key += 'QL'
    ans_buka[kind - 1] += key
    for i in range(len(key)):
        add_place(kind, key[i])
    lazyshoot.add((len(key), goal, 4, num))
    return True


def buka_slide_left(x, y, kind, boll_num):
    if loc[x][y] != -1:
        return False
    if loc[x][y - 1] == -1:
        return False
    if len(place[3]) > len(place[1]) and place[3][len(place[1])][0] == x:
        return False
    if place[0][len(place[kind])][0] == x:
        return False
    if abs(place[0][len(place[kind])][0] - x) <= 1 and \
            place[0][len(place[kind])][1] == 4:
        return False
    boll_num = chenge_loc_get(x, y - 1)
    chenge_loc_put(x, y, boll_num)
    key = 'LPRQ'
    ans_buka[kind - 1] += key
    for i in range(len(key)):
        add_place(kind, key[i])
    return True


direct1 = 'D'


def move_pone1(boll_num):
    global to_x, to_y, x, y, ans, boll_x, boll_y, ti, tj
    global direct1
    pone1_x, pone1_y = place[1][-1]
    if pone1_x == 0 and direct1 == 'U':
        direct1 = 'D'
    elif pone1_x == 4 and direct1 == 'D':
        direct1 = 'U'
    if buka_shoot(pone1_x, pone1_y, 1, boll_num):
        return
    if buka_slide_Upper(pone1_x, pone1_y, 1, boll_num):
        return
    if buka_slide_Down(pone1_x, pone1_y, 1, boll_num):
        return

    if buka_slide_left(pone1_x, pone1_y, 1, boll_num):
        return
    if add_place_buka(1, direct1):
        ans_buka[0] += direct1
    else:
        if place[1][-1] != place[0][-1]:
            ans_buka[0] += '.'
        else:
            ans_buka[0] += 'B'
            place[1][-1] = [-1, -1]


def move_king():
    global to_x, to_y, x, y, ans, boll_x, boll_y, boll_num, ti, tj
    if boll_num == -1:
        # print('debag2')
        if (to_x == -1 and to_y == -1) \
                or len(place[0]) <= max(len(place[4]), len(place[3]),
                                        len(place[1])):
            to_x, to_y = get_next_boll(x, y)
            for j in range(len(lazyshoot)):
                if min(x, to_x) <= lazyshoot[j][1] <= max(x, to_x):
                    to_x = -1
                    to_y = -1
        if len(place[0]) <= 16:
            to_x, to_y = 0, 0
        if to_x == -1 and to_y == -1:
            ans += '.'
            stay(0)
            return
        if x != to_x or y != to_y:
            x, y, tmp = move_get(x, y, to_x, to_y)
            ans += tmp
            add_place(0, tmp)
        else:
            ans += 'P'
            add_place(0, 'P')
            boll_x, boll_y = x, y
            boll_num = chenge_loc_get(x, y)

    else:
        ti, tj = where_to_move(boll_x, boll_y, boll_num)
        # print('x, y, ti, tj:', x, y, ti, tj)
        if x != ti or y != tj:
            # print('debag2')
            x, y, tmp = move_put(x, y, ti, tj)
            ans += tmp
            # print('tmp:', tmp)
            add_place(0, tmp)
        else:
            ans += 'Q'
            add_place(0, 'Q')
            chenge_loc_put(x, y, boll_num)
            boll_num = -1
            to_x, to_y = -1, -1


'''
関数は上のみしか書かない

'''

ans_buka = ['PRRRQLLLPRRQLLPRQB' for _ in range(4)]
ans_buka[3] = ans_buka[3][:-1] + 'L'
ans_buka[2] = ans_buka[2][:-1] + 'D'
ans_buka[0] = 'PRRRQLLLPRRQR'
x, y = 0, 0
boll_num = -1
before_num = -1
loc[0][0] = A[0].pop(0)
for i in range(5):
    place[i].append([i, 0])

for i in range(1, 5):
    for j in range(len(ans_buka[i - 1])):
        add_place(i, ans_buka[i - 1][j])
'''
これでpone4のみまだ動いている
pone3もまだ動いている
'''
for i in range(1, 5):
    for j in range(4):
        if i == 1 and j == 2:
            continue
        loc[i][3 - j] = A[i].pop(0)

boll_x = 0
boll_y = 0

while len(place[1]) < len(place[0]):
    move_pone1(boll_num)
while len(place[3]) < len(place[0]):
    move_pone3(boll_num)
while len(place[4]) < len(place[0]):
    move_pone4(boll_num)
to_x, to_y = -1, -1
while True:
    # if len(place[0]) == 73:
    #     print('loc:', loc)
    #     print('recieve:', recieve)
    tmp_lazyshoot = SortedSet()
    while len(lazyshoot) != 0:
        count, lx, ly, num = lazyshoot.pop(0)
        if count == 1:
            chenge_loc_put(lx, ly, num)
        else:
            tmp_lazyshoot.add((count - 1, lx, ly, num))
    lazyshoot = tmp_lazyshoot

    move_king()
    while len(place[0]) > len(place[1]):
        move_pone1(boll_num)
    while len(place[0]) > len(place[3]) and ans_buka[2][-1] != 'B':
        move_pone3(boll_num, True)
    while len(place[0]) > len(place[4]):
        move_pone4(boll_num)

    execution_time = time.time() - start_time
    if execution_time >= 2.9:
        print(ans[:300])
        for i in range(4):
            print(ans_buka[i][:min(len(ans_buka[i]), 300)])
        exit()

    '''
    pone4のみ動かし続けてみたい
    まずはloc干渉しないで動き続けられるかどうかを考えたい
    '''
