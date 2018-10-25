import numpy as np


def get_snake(n):
    way = 'r'
    arr = [[0 for _ in range(n)] for _ in range(n)]
    i = 0
    j = 0
    # count = 1
    go_to = n - 1
    ch_go_to = 3
    cou_go_to = 0
    passed_way = 0
    for count in range(1, n ** 2 + 1):
        arr[i][j] = count
        if count == n ** 2:
            arr[i][j] = 0
        # print(count, i, j, cou_go_to, go_to)
        count += 1
        if way == 'r':
            if passed_way == go_to:
                way = 'd'
                i += 1
                cou_go_to += 1
                passed_way = 1
            else:
                passed_way += 1
                j += 1
        elif way == 'd':
            if passed_way == go_to:
                way = 'l'
                j -= 1
                cou_go_to += 1
                passed_way = 1
            else:
                i += 1
                passed_way += 1
        elif way == 'l':
            if passed_way == go_to:
                way = 'u'
                i -= 1
                cou_go_to += 1
                passed_way = 1
            else:
                j -= 1
                passed_way += 1
        elif way == 'u':
            if passed_way == go_to:
                way = 'r'
                j += 1
                cou_go_to += 1
                passed_way = 1
            else:
                i -= 1
                passed_way += 1
        if cou_go_to == ch_go_to:
            cou_go_to = 0
            go_to -= 1
            if ch_go_to == 3:
                ch_go_to = 2
    return arr


for s in range(3, 8):
    norm = []
    cou = 1
    for i in range(s):
        norm.append([])
        for j in range(s):
            norm[-1].append(cou)
            print(norm[-1][-1], end=' ')
            cou += 1
        print()
    print()
    sn = get_snake(s)
    for i in range(s):
        for j in range(s):
            print(sn[i][j], end=' ')
        print()
    print("-----------------------------------------------------")

