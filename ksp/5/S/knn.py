#!/usr/bin/env python3
import argparse

import numpy as np
import sklearn.datasets
import sklearn.metrics
import sklearn.model_selection
import sklearn.preprocessing


parser = argparse.ArgumentParser()

parser.add_argument("--k", default=1, type=int, help="Kolik nejbližších sousedů se má uvažovat")
parser.add_argument("--plot", default=False, const=True, nargs="?", type=str, help="Vykreslit chybné příklady klasifikace pro danou třídu. Výstup si můžete také nechat uložit do souboru.")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument("--test_size", default=0.25, type=float, help="Velikost testovací množiny")

def main(args: argparse.Namespace) -> float:
    data, target = sklearn.datasets.fetch_openml('mnist_784', version=1, as_frame=False, return_X_y=True, parser="liac-arff")
    data, target = data[:1000], target[:1000]
    target = target.astype(np.int32)
    data = sklearn.preprocessing.MinMaxScaler().fit_transform(data)

    train_data, test_data, train_target, test_target = sklearn.model_selection.train_test_split(data, target, test_size=args.test_size, random_state=args.seed)

    test_neighbors = np.argsort(np.linalg.norm(test_data[:, None] - train_data[None, :], axis=2), axis=1)[:, :args.k]
    test_predictions = np.array([np.bincount(train_target[neighbors]).argmax() for neighbors in test_neighbors])

    accuracy = sklearn.metrics.accuracy_score(test_target, test_predictions)

    if args.plot:
        import matplotlib.pyplot as plt
        examples = [[] for _ in range(10)]
        for i in range(len(test_predictions)):
            if test_predictions[i] != test_target[i] and not examples[test_target[i]]:
                examples[test_target[i]] = [test_data[i], *train_data[test_neighbors[i]]]
        examples = [[img.reshape(28, 28) for img in example] for example in examples if example]
        examples = [[example[0]] + [np.zeros_like(example[0])] + example[1:] for example in examples]
        plt.imshow(np.concatenate([np.concatenate(example, axis=1) for example in examples], axis=0), cmap="gray")
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
        plt.show() if args.plot is True else plt.savefig(args.plot, transparent=True, bbox_inches="tight")

    return accuracy


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    accuracy = main(args)
    print("K-nn přesnost se {} sousedy: {:.2f}%".format(
        args.k, 100 * accuracy))

