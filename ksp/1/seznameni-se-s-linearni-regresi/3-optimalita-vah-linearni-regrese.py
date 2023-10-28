[N, F] = [int(i) for i in input().split(" ")]
w = [float(i) for i in input().split(" ")]
features = []
answers = []
predictions = []
for _ in range(N):
    [*x, correct] = [float(i) for i in input().split(" ")]
    x.append(1)
    features.append(x)
    answers.append(correct)
    predictions.append(sum([x[i] * w[i] for i in range(F + 1)]))
for i in range(F + 1):
    der = sum([2*(predictions[j] - answers[j]) * features[j][i] for j in range(N)]) / N
    if abs(der) > 10e-6:
        print("NE")
        exit()
print("ANO")



