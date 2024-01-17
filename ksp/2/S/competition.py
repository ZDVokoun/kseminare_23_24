#!/usr/bin/env python3
import argparse
import lzma
import os
import pickle
import sys
import urllib.request

import numpy as np
from sklearn import metrics
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import Pipeline


class Dataset:
    """Dataset půjčovny kol

    Dataset obsahuje tyto informace:
    - Hodina - hodina v rámci dne
    - Teplota - ve stupních Celsia
    - Vlhkost vzduchu - %
    - Rychlost větru - m/s
    - Viditelnost - v jednotkách 10m
    - Rosný bod - ve stupních Celsia
    - Sluneční záření - MJ/m^2
    - Množství srážek - mm
    - Výška sněhové pokrývky - cm
    - Roční období - (0: zima, 1: jaro, 2: léto, 3: podzim)
    - Prázdniny - (0: ne, 1: ano)
    - Fungoval systém - (0: ne, 1: ano)
    - Den   - 1-31
    - Měsíc - 1-12
    - Rok   - 2017 nebo 2018

    Cílová proměnná je počet půjčených kol v dané hodině.
    """

    def __init__(
        self,
        name="dataset36-2-S.npz",
        url="https://ksp.mff.cuni.cz/h/ulohy/36/36-2-S/competition-datasets/",
    ):
        if not os.path.exists(name):
            print("Downloading dataset {}...".format(name), file=sys.stderr)
            urllib.request.urlretrieve(url + name, filename=name)

        # načtení serialovaného datasetu
        dataset = np.load(name, allow_pickle=True)

        self.train_data = dataset["train_data"]
        self.test_data = dataset["test_data"]
        self.train_target = dataset["train_target"]
        # pozor: obsahuje vektor -1
        self.test_target = dataset["test_target"]


parser = argparse.ArgumentParser()

parser.add_argument("--seed", default=42, type=int, help="Random seed")
parser.add_argument("--load", default=None, type=str, help="Load saved model")


def main(args):
    # nastavení seedu
    np.random.seed(args.seed)

    # načtení datasetu
    dataset = Dataset()

    if args.load is None:
        ct = ColumnTransformer(
            [
                ("scaler", StandardScaler(), [1, 2, 3, 4, 5, 6, 7, 8]),
                ("passthrough", "passthrough", [10, 11]),
                ("onehot", OneHotEncoder(), [0, 9, 12, 13, 14]),
            ]
        )
        polytrans = PolynomialFeatures(2, include_bias=False, interaction_only=True)

        model = Pipeline(
            [
                ("column", ct),
                ("poly", polytrans),
                ("reg", RidgeCV(alphas=np.linspace(34, 35, 11))),
            ]
        )
        model.fit(dataset.train_data, dataset.train_target)

        # Pokud si budete chtít uložit model (nebo celou pipeline),
        # se vám může hodit toto:
        with lzma.open("competition.model", "wb") as model_file:
            pickle.dump(model, model_file)
    else:
        # Poté načtení modelu uděláte takto:
        with lzma.open(args.load, "rb") as model_file:
            model = pickle.load(model_file)
        print(f"Best lambda: {model.named_steps['reg'].alpha_}")
        print(
            f"Train RMSE: {metrics.mean_squared_error(dataset.train_target, model.predict(dataset.train_data), squared=False)}"
        )

    pred = model.predict(dataset.test_data)

    with open("36-2-S-prediction.txt", "w") as prediction_file:
        for p in pred:
            print(p, file=prediction_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
