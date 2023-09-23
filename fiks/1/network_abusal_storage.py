t = int(input())
for _ in range(t):
    n = int(input())
    lst = [int(i) for i in input().split(" ")]
    res = 1
    for k in range(n, 0, -1):
        c = 0
        for j in lst:
            if j % k == 0:
                c += 1
        if c >= k:
            res = k
            break
    print(res)
