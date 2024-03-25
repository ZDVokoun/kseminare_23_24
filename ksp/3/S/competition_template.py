#!/usr/bin/env python3
import argparse
import lzma
import os
import pickle
import sys
import urllib.request

import numpy as np

class Dataset:
    """Dataset pacientů

    Dataset obsahuje tyto informace (v tomto pořadí):
    - 15 binárních atributů
    - 6 číselných atributů
    
    Cílem je predikovat, zda pacient má poruchu štítné žlázy (1) nebo ne (2).
    """
    def __init__(self,
                 name="dataset36-3-S.npz",
                 url="https://ksp.mff.cuni.cz/h/ulohy/36/36-3-S/competition-datasets/"):
        if not os.path.exists(name):
            print("Downloading dataset {}...".format(name), file=sys.stderr)
            urllib.request.urlretrieve(url + name, filename=name)

        # načtení serializovaného datasetu
        dataset = np.load(name, allow_pickle=True)

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
    model = ...

    # Pokud si budete chtít uložit model (nebo celou pipeline),
    # se vám může hodit toto:
    # with lzma.open("competition.model", "wb") as model_file:
    #     pickle.dump(model, model_file)

    # Poté načtení modelu uděláte takto:
    # with lzma.open("competition.model", "rb") as model_file:
    #     model = pickle.load(model_file)

    pred = model.predict(dataset.test_data)

    with open("36-3-S-prediction.txt", "w") as prediction_file:
        for p in pred:
            print(p, file=prediction_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
