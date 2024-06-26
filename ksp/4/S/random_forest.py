#!/usr/bin/env python3
import argparse

import numpy as np
import sklearn.datasets
from sklearn.model_selection import train_test_split
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--bagging", default=False, action="store_true", help="Použít bagging")
parser.add_argument("--dataset", default="digits", type=str, help="Použitý dataset")
parser.add_argument("--feature_subsampling", default=1, type=float, help="Pravděpodobnost vybrání jednotlivých featur")
parser.add_argument("--max_depth", default=None, type=int, help="Maximální hloubka rozhodovacího stromu")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument("--test_size", default=0.25, type=float, help="Velikost testovací množiny")
parser.add_argument("--trees", default=1, type=int, help="Počet stromů použitých v random forestu")


def subsample_features(number_of_features: int) -> np.ndarray:
    '''Vrátí masku featur, které mají být použity při hledání nejlepšího rozdělení.'''
    return generator_feature_subsampling.uniform(size=number_of_features) <= args.feature_subsampling

def bootstrap_dataset(train_data: np.ndarray) -> np.ndarray:
    '''Vrátí indexy dat, které mají být použity pro trénování rozhodovacího stromu.'''
    return generator_bootstrapping.choice(len(train_data), size=len(train_data), replace=True)

class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = self._grow_tree(X, y, depth=0)

    def predict(self, X):
        return np.array([self._predict(inputs) for inputs in X])

    def _predict(self, inputs):
        node = self.tree
        while node.left:
            if inputs[node.feature] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

    def _find_best_split(self, X, y):
        _, num_features = X.shape
        feature_mask = subsample_features(num_features)
        best_criteria = None
        best_sets = None
        best_score = float('inf')

        for feature in range(num_features):
            if not feature_mask[feature]:
                continue

            feature_values = sorted(set(X[:, feature]))
            if len(feature_values) == 1:
                continue
            thresholds = [(feature_values[i] + feature_values[i + 1]) / 2 for i in range(len(feature_values) - 1)]

            for threshold in thresholds:
                left_indices = X[:, feature] < threshold
                right_indices = ~left_indices

                left_y, right_y = y[left_indices], y[right_indices]

                score = self._entropy(left_y) + self._entropy(right_y)

                if score < best_score:
                    best_criteria = (feature, threshold)
                    best_sets = (left_indices, right_indices)
                    best_score = score

        return best_criteria, best_sets

    def _grow_tree(self, X, y, depth):
        if (depth < self.max_depth if self.max_depth is not None else True) and len(set(y)) > 1:
            best_criteria, best_sets = self._find_best_split(X, y)

            if best_criteria:
                left = self._grow_tree(X[best_sets[0]], y[best_sets[0]], depth + 1)
                right = self._grow_tree(X[best_sets[1]], y[best_sets[1]], depth + 1)
                return TreeNode(best_criteria[0], best_criteria[1], left, right)

        return TreeNode(value=self._leaf_value(y))

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -len(y) * np.sum([p * np.log2(p) for p in ps if p > 0])

    def _leaf_value(self, y):
        return Counter(y).most_common(1)[0][0]

class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class RandomForest:
    def __init__(self, n_trees, max_depth, bagging):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.bagging = bagging
        self.trees = []

    def fit(self, X, y):
        for _ in range(self.n_trees):
            if self.bagging:
                indices = bootstrap_dataset(X)
                X_sample, y_sample = X[indices], y[indices]
            else:
                X_sample, y_sample = X, y

            tree = DecisionTree(max_depth=self.max_depth)

            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.array([self._vote(predictions) for predictions in tree_predictions.T])

    def _vote(self, predictions):
        counter = Counter(predictions)
        max_votes = max(counter.values())
        winners = [key for key, count in counter.items() if count == max_votes]
        return min(winners)

def main(args: argparse.Namespace):
    # Načtení datasetu.
    data, target = getattr(sklearn.datasets, "load_{}".format(args.dataset))(return_X_y=True)

    # Rozdělte dataset na trénovací a testovací část.
    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    # Vytvoření náhodných generátorů.
    global generator_feature_subsampling
    generator_feature_subsampling = np.random.RandomState(args.seed)

    global generator_bootstrapping    
    generator_bootstrapping = np.random.RandomState(args.seed)

    # Implementace Random Forest

    rf = RandomForest(
        n_trees=args.trees,
        max_depth=args.max_depth,
        bagging=args.bagging
    )

    rf.fit(train_data, train_target)
    train_predictions = rf.predict(train_data)
    test_predictions = rf.predict(test_data)

    train_accuracy = np.mean(train_predictions == train_target)
    test_accuracy = np.mean(test_predictions == test_target)

    print("Train accuracy: {:.1f}%".format(100 * train_accuracy))
    print("Test accuracy: {:.1f}%".format(100 * test_accuracy))

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
