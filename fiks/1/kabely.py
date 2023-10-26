t = int(input())
for _ in range(t):
    top = []
    right = []
    bottom = []
    left = []
    h,w,n = [int(i) for i in input().split(" ")]
    for _ in range(n):
        c = tuple(input().split(" "))
        if int(c[0]) == 0:
            top.append(c)
        elif int(c[1]) == 0:
            left.append(c)
        elif int(c[0]) == h:
            bottom.append(c)
        else:
            right.append(c)
    lst = top + right + bottom + left
    i = 0
    prev = lst[0][2]
    found = False
    while (len(lst) > 1 or len(lst) % 2 != 0):
        # print(len(lst))
        if (i == len(lst) - 1):
            i = 0
            if not found:
                break
            found = False
        else:
            i += 1
        old_prev = prev
        prev = lst[i][2]
        if old_prev == lst[i][2]:
            found = True
            if i != 0:
                del lst[i]
                del lst[i - 1]
            else:
                del lst[len(lst) - 1]
                del lst[0]
            i -= 2
    if len(lst) != 0:
        print("ajajaj")
    else:
        print("pujde to")



     
