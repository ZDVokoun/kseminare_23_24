#!/usr/bin/env python3
import argparse
import lzma
import os
import pickle
import sys
import urllib.request

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    MinMaxScaler,
    OneHotEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.metrics import mean_squared_error

class Dataset:
    """Dataset databáze spamu

    Dataset obsahuje tyto informace:
    - frekvence výskytu vybraných 48 slov v e-mailech
      (slova: 'make', 'address', 'all', '3d', 'our', 'over', 'remove', 'internet',
              'order', 'mail', 'receive', 'will', 'people', 'report', 'addresses',
              'free', 'business', 'email', 'you', 'credit', 'your', 'font', '000',
              'money', 'hp', 'hpl', 'george', '650', 'lab', 'labs', 'telnet', '857',
              'data', '415', '85', 'technology', '1999', 'parts', 'pm', 'direct', 'cs',
              'meeting', 'original', 'project', 're', 'edu', 'table', 'conference')
    - frekvence výskytu vybraných 6 znaků v e-mailech
      (znaky: ';', '(', '[', '!', '$', '#')
    - průměrná délka souvislé sekvence velkých písmen
    - nejdelší souvislá sekvence velkých písmen
    - celkový počet velkých písmen

    Cílem je predikovat, zda je e-mail spam nebo ne.
    """
    def __init__(self,
                 name="dataset36-5-S.npz",
                 url="https://ksp.mff.cuni.cz/h/ulohy/36/36-5-S/competition-datasets/"):
        if not os.path.exists(name):
            print("Downloading dataset {}...".format(name), file=sys.stderr)
            urllib.request.urlretrieve(url + name, filename=name)

        # načtení serializovaného datasetu
        dataset = np.load(name)

        self.train_data = dataset['train_data']
        self.test_data = dataset['test_data']
        self.train_target = dataset['train_target']
        # pozor: obsahuje vektor -1
        self.test_target = dataset['test_target']


parser = argparse.ArgumentParser()

parser.add_argument("--seed", default=42, type=int, help="Random seed")


def main(args):
    # nastavení seedu
    np.random.seed(args.seed)

    # načtení datasetu
    dataset = Dataset()

    # TODO: Natrénujte model
    model = Pipeline(
        [
            (
                "ct",
                ColumnTransformer(
                    [
                        ("scale", StandardScaler(), np.arange(0,57)),
                    ]
                ),
            ),
            # ("reg", MLPClassifier([50,50,10],activation='relu')),
            ("ml", MLPClassifier([50,100,10],activation='relu')),
        ]
    )
    model.fit(dataset.train_data, dataset.train_target)

    # Pokud si budete chtít uložit model (nebo celou pipeline),
    # se vám může hodit toto:
    # with lzma.open("competition.model", "wb") as model_file:
    #     pickle.dump(model, model_file)

    # Poté načtení modelu uděláte takto:
    # with lzma.open("competition.model", "rb") as model_file:
    #     model = pickle.load(model_file)

    print(
        f"Train RMSE: {mean_squared_error(dataset.train_target, model.predict(dataset.train_data), squared=False)}"
    )
    pred = model.predict(dataset.test_data)

    with open("36-5-S-prediction.txt", "w") as prediction_file:
        for p in pred:
            print(p, file=prediction_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

