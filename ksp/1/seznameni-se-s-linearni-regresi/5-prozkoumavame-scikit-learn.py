import sklearn.datasets
import sklearn.linear_model as lm
import sklearn.metrics as metrics

diabetes = sklearn.datasets.load_diabetes()

# Vypočítáme část, kterou použijeme k trénování a testování
percent = 90
train_size = int(len(diabetes.data)*percent/100)

# Rozdělíme dataset
train_data = diabetes.data[:train_size]
train_target = diabetes.target[:train_size]
test_data = diabetes.data[train_size:]
test_target = diabetes.target[train_size:]

estimator = lm.LinearRegression()
estimator.fit(train_data,
              train_target)
prediction = estimator.predict(test_data)

print(f"Predikce: {prediction}")
print(f"Reálná hodnota: {test_target}")
print(f"MSE: {metrics.mean_squared_error(test_target, prediction)}")

# Vybral jsem metriku, která získá maximální chybu, protože pro předpověď
# vývoje cukrovky je dle mého názoru minimalizovat extrémní výchylky.
print(f"Max error: {metrics.max_error(test_target,prediction)}")



