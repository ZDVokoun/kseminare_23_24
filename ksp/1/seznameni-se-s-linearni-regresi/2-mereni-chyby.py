[N, F] = [int(i) for i in input().split(" ")]
w = [float(i) for i in input().split(" ")]
MSE = 0
for _ in range(N):
    [*x, correct] = [float(i) for i in input().split(" ")]
    x.append(1)
    prediction = sum([x[i] * w[i] for i in range(F + 1)])
    MSE += (prediction - correct)**2
MSE /= N
print(MSE)
