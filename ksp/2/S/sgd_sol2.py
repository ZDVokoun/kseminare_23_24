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


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
