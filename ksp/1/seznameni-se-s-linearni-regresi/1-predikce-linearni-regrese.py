[N, F] = [int(i) for i in input().split(" ")]
w = [float(i) for i in input().split(" ")]
for _ in range(N):
    x = [float(i) for i in input().split(" ")]
    x.append(1)
    print(sum([x[i] * w[i] for i in range(F + 1)]))
