#!/usr/bin/env python3
import argparse

import numpy as np
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn import linear_model as lm, metrics

parser = argparse.ArgumentParser()

parser.add_argument("--learning_rate", default=0.01, type=float, help="Learning rate")
parser.add_argument("--l2", default=0.0, type=float, help="Síla L2 regularizace")
parser.add_argument(
    "--epochs", default=50, type=int, help="Počet epoch na trénování Minibatch SGD"
)
parser.add_argument("--batch_size", default=10, type=int, help="Velikost batche")
parser.add_argument("--data_size", default=100, type=int, help="Velikost datasetu")
parser.add_argument(
    "--test_size", default=0.5, type=float, help="Velikost testovací množiny"
)
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument("--plot", action="store_true", help="Vykreslit predikce")


def main(args: argparse.Namespace):
    # Nastavení seedu generátoru náhodných čísel
    generator = np.random.RandomState(args.seed)

    # Vytvoření náhodného datasetu na regresní úlohu
    data, target = sklearn.datasets.make_regression(
        n_samples=args.data_size, random_state=args.seed
    )

    # Přidání sloupce jedniček pro bias
    data = np.concatenate([data, np.ones([args.data_size, 1])], axis=1)

    # TODO: Rozdělte dataset na trénovací a testovací část, funkci z knihovny sklearn
    # předejte argumenty `test_size=args.test_size, random_state=args.seed`.
    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    # Vytvoření náhodných vah
    weights = generator.uniform(size=train_data.shape[1])

    train_rmses, test_rmses = [], []
    for epoch in range(args.epochs):
        # TODO: Pro každou epochu náhodně zamíchejte trénovací množinu.
        # Na zamíchání použijte generator.permutation, které vrátí náhodnou permutaci
        # čísel od 0 do počtu prvků v množině.
        perm = generator.permutation(np.arange(train_data.shape[0]));
        perm_train_data = train_data[perm]
        perm_train_target = train_target[perm]

        # TODO: Pro každou batch s velikostí args.batch_size spočítejte gradient
        # a upravte váhy. Pokud je args.l2 nenulové, tak upravte váhy i s l2 regularizací.
        # Můžete předpokládat, že args.batch_size je dělitelem počtu prvků v trénovací množině.
        for start in range(0, train_data.shape[0], args.batch_size):
            gradient = np.array(
                [
                    2 * (perm_train_data[i].dot(weights) - perm_train_target[i]) * perm_train_data[i]
                    for i in range(start, start + args.batch_size)
               ]
            ).sum(axis=0) / args.batch_size
            # print(gradient)
            weights -= args.learning_rate * (
                gradient + args.l2 * 2 * weights
            )

        # TODO: Na konci každé epochy spočítejte metriku RMSE na trénovací a testovací množině.
        # RMSE metrika se rovná odmocnině z MSE a můžete si funkci ze sklearn.metrics
        # říct, že chcete RMSE metriku.
        # RMSE metriku používáme hlavně proto, že když si budete vykreslovat chybu,
        # tak na grafu nebudou tak obří čísla na y-ové ose.
        train_rmse, test_rmse = metrics.mean_squared_error(
            train_target, train_data @ weights, squared=False
        ), metrics.mean_squared_error(test_target, test_data @ weights, squared=False)

        train_rmses.append(train_rmse)
        test_rmses.append(test_rmse)
        print(f"Epoch {epoch+1}: train = {train_rmse:.8f}, test = {test_rmse:.8f}")

    # TODO: Porovnajte si vaše RMSE na testovací množině s implementací z knihovny sklearn,
    # které se učí explicitně pomocí vzorce. Použijte model `Ridge` s parametrem `alpha=args.l2`.

    if (args.l2 != 0):
        sklearn_model = lm.Ridge(alpha=args.l2)
    else:
        sklearn_model = lm.LinearRegression()
    sklearn_model.fit(train_data, train_target)
    sklearn_predict = sklearn_model.predict(test_data)
    test_sklearn_rmse = metrics.mean_squared_error(
        test_target, sklearn_predict, squared=False
    )
    print(f"Sklearn RMSE = {test_sklearn_rmse:.8f}")

    # Vykreslení MSE na trénovací a testovací množině
    if args.plot:
        import matplotlib.pyplot as plt

        # Pro vykreslení grafů je potřeba mít nainstalovanou knihovnu matplotlib
        plt.plot(train_rmses, label="Trénovací chyba (RMSE)")
        plt.plot(test_rmses, label="Testovací chyba (RMSE)")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
