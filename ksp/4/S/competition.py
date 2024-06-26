#!/usr/bin/env python3
import argparse
import lzma
import os
import pickle
import sys
import urllib.request

from sklearn.preprocessing import (
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegressionCV

import numpy as np

class Dataset:
    """Dataset obrázků čísel

    Dataset obsahuje tyto informace:
    - 8x8 pixelů obrázků čísel 0 až 9
    - každý pixel má hodnotu 0 až 16
    Hodnoty jednotlivých pixelů vznikly tak, že se vzal
    bitmapový obrázek a pro každý 4x4 nepřekrývající blok
    se spočetlo počet černých pixelů.

    Cílem je predikovat, které číslo se nachází na obrázku.
    """
    def __init__(self,
                 name="dataset36-4-S.npz",
                 url="https://ksp.mff.cuni.cz/h/ulohy/36/36-4-S/competition-datasets/"):
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
                        ("scaler", StandardScaler(), np.arange(0,dataset.train_data.shape[1]))
                    ], remainder = 'passthrough'
                ),
            ),
            ("poly", PolynomialFeatures(3, interaction_only=True, include_bias=False)),
            ("reg", LogisticRegressionCV(max_iter=1000, fit_intercept=False)),
        ]
    )


    model.fit(dataset.train_data, dataset.train_target)

    # Pokud si budete chtít uložit model (nebo celou pipeline),
    # se vám může hodit toto:
    with lzma.open("competition.model", "wb") as model_file:
        pickle.dump(model, model_file)

    # Poté načtení modelu uděláte takto:
    # with lzma.open("competition.model", "rb") as model_file:
    #     model = pickle.load(model_file)

    pred = model.predict(dataset.test_data)

    with open("36-4-S-prediction.txt", "w") as prediction_file:
        for p in pred:
            print(p, file=prediction_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
