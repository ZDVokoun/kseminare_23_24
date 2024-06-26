#!/usr/bin/env python3
import argparse

import numpy as np

import sklearn.datasets

parser = argparse.ArgumentParser()
parser.add_argument("--clusters", default=3, type=int, help="Počet clusterů")
parser.add_argument("--examples", default=180, type=int, help="Počet dat")
parser.add_argument("--iterations", default=20, type=int, help="Počet iterací algoritmu KMeans")
parser.add_argument("--plot", default=False, const=True, nargs="?", type=str, help="Vykreslovat průběh algoritmu KMeans. Výstup si můžete také nechat uložit do souboru.")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")

def plot(args: argparse.Namespace, iteration: int,
         data: np.ndarray, centers: np.ndarray, clusters: np.ndarray) -> None:
    import matplotlib.pyplot as plt

    if args.plot is not True:
        if not plt.gcf().get_axes(): plt.figure(figsize=(4*2, 5*6))
        plt.subplot(6, 2, 1 + len(plt.gcf().get_axes()))
    plt.title("Inicializace KMeans" if not iteration else
              "KMeans po {}. iteraci".format(iteration))
    plt.gca().set_aspect('equal')
    plt.scatter(data[:, 0], data[:, 1], c=clusters)
    plt.scatter(centers[:, 0], centers[:, 1], marker="X", s=200,
                edgecolors="#ff0000", c=range(args.clusters),
                linewidths=2)
    if args.plot is True: plt.show()
    else: plt.savefig(args.plot, transparent=True, bbox_inches="tight")

def main(args: argparse.Namespace) -> np.ndarray:
    generator = np.random.RandomState(args.seed)
    data, target = sklearn.datasets.make_blobs(
        n_samples=args.examples, centers=args.clusters, n_features=2, random_state=args.seed)
    center_idicies = generator.choice(args.examples, args.clusters, replace=False)
    centers = data[center_idicies]

    if args.plot:
        plot(args, 0, data, centers, clusters=None)

    clusters = np.zeros(data.shape[0], dtype=np.int32)
    for iteration in range(args.iterations):
        for i in range(data.shape[0]):
            distances = np.linalg.norm(data[i] - centers, axis=1)
            clusters[i] = np.argmin(distances)

        new_centers = np.zeros_like(centers)
        for k in range(args.clusters):
            new_centers[k] = np.mean(data[clusters == k], axis=0)

        if np.all(centers == new_centers):
            break

        centers = new_centers

        if args.plot:
            plot(args, 1 + iteration, data, centers, clusters)

    return clusters

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    centers = main(args)
    print("Přiřazené skupiny:", centers, sep="\n")
