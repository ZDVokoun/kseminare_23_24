#!/usr/bin/env python3
import argparse
import numpy as np
import sklearn.datasets
from sklearn.model_selection import train_test_split
from collections import Counter
import heapq

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset",
    default="wine",
    type=str,
    help="Použitý dataset; buď `wine` nebo `diabetes`",
    choices=["wine", "diabetes"],
)
parser.add_argument(
    "--max_depth", default=None, type=int, help="Maximální hloubka rozhodovacího stromu"
)
parser.add_argument(
    "--max_leaves", default=None, type=int, help="Maximální počet listů stromu"
)
parser.add_argument(
    "--min_to_split",
    default=2,
    type=int,
    help="Minimální počet dat pro rozdělení vrcholu (listu)",
)
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument(
    "--test_size", default=0.25, type=float, help="Velikost testovací množiny"
)


class DecisionTree:
    def __init__(self, criterion, max_depth=None, max_leaves=None, min_to_split=2):
        self.criterion = criterion
        self.max_depth = max_depth
        self.max_leaves = max_leaves
        self.min_to_split = min_to_split
        self.tree = None

    def fit(self, X, y):
        self.n_leaves = 0
        self.tree = self._grow_tree(X, y)

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
        best_criteria = None
        best_sets = None
        best_score = float("inf")

        for feature in range(num_features):
            feature_values = sorted(set(X[:, feature]))
            if len(feature_values) == 1:
                continue
            thresholds = [
                (feature_values[i] + feature_values[i + 1]) / 2
                for i in range(len(feature_values) - 1)
            ]

            for threshold in thresholds:
                left_indices = X[:, feature] < threshold
                right_indices = ~left_indices

                if sum(left_indices) < 1 or sum(right_indices) < 1:
                    continue

                left_y, right_y = y[left_indices], y[right_indices]

                if self.criterion == "entropy":
                    score = self._entropy(left_y) + self._entropy(right_y)
                elif self.criterion == "se":
                    score = self._se(left_y) + self._se(right_y)

                if score < best_score:
                    best_criteria = (feature, threshold)
                    best_sets = (left_indices, right_indices)
                    best_score = score

        best_decrease = 0
        if self.criterion == "entropy":
            best_decrease = best_score - self._entropy(y)
        elif self.criterion == "se":
            best_decrease = best_score - self._se(y)

        return best_criteria, best_sets, best_decrease

    def _grow_tree(self, X, y):
        root = TreeNode(value=self._leaf_value(y))
        q = [(-np.inf, root, X, y, 0)]
        while q and (self.max_leaves is None or len(q) < self.max_leaves):
            _, cur, X_cur, y_cur, depth = heapq.heappop(q)
            num_samples, _ = X_cur.shape
            if (
                (depth < self.max_depth if self.max_depth is not None else True)
                and num_samples >= self.min_to_split
                and len(set(y_cur)) > 1
            ):
                best_criteria, best_sets, _ = self._find_best_split(X_cur, y_cur)
                if best_criteria:
                    left = TreeNode(value=self._leaf_value(y_cur[best_sets[0]]))
                    _, _, left_decrease = self._find_best_split(
                        X_cur[best_sets[0]], y_cur[best_sets[0]]
                    )
                    heapq.heappush(
                        q,
                        (
                            left_decrease,
                            left,
                            X_cur[best_sets[0]],
                            y_cur[best_sets[0]],
                            depth + 1,
                        ),
                    )
                    right = TreeNode(value=self._leaf_value(y_cur[best_sets[1]]))
                    _, _, right_decrease = self._find_best_split(
                        X_cur[best_sets[1]], y_cur[best_sets[1]]
                    )
                    heapq.heappush(
                        q,
                        (
                            right_decrease,
                            right,
                            X_cur[best_sets[1]],
                            y_cur[best_sets[1]],
                            depth + 1,
                        ),
                    )
                    cur.left = left
                    cur.right = right
                    cur.feature = best_criteria[0]
                    cur.threshold = best_criteria[1]
        return root

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -len(y) * np.sum([p * np.log2(p) for p in ps if p > 0])

    def _se(self, y):
        return np.sum((y - np.mean(y)) ** 2)

    def _leaf_value(self, y):
        if self.criterion == "entropy":
            return Counter(y).most_common(1)[0][0]
        elif self.criterion == "se":
            return np.mean(y)


class TreeNode:
    def __init__(self, value=None):
        self.feature = None
        self.threshold = None
        self.left = None
        self.right = None
        self.value = value

    # Just to make the heap working
    def __lt__(self, other):
        return self.value < other.value


def main(args: argparse.Namespace):
    data, target = getattr(sklearn.datasets, "load_{}".format(args.dataset))(
        return_X_y=True
    )

    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    if args.dataset == "diabetes":
        tree = DecisionTree(
            criterion="se",
            max_depth=args.max_depth,
            max_leaves=args.max_leaves,
            min_to_split=args.min_to_split,
        )
    else:
        tree = DecisionTree(
            criterion="entropy",
            max_depth=args.max_depth,
            max_leaves=args.max_leaves,
            min_to_split=args.min_to_split,
        )

    tree.fit(train_data, train_target)

    train_pred = tree.predict(train_data)
    test_pred = tree.predict(test_data)

    if args.dataset == "diabetes":
        train_rmse = np.sqrt(np.mean((train_pred - train_target) ** 2))
        test_rmse = np.sqrt(np.mean((test_pred - test_target) ** 2))
        print("Train RMSE: {:.5f}".format(train_rmse))
        print("Test RMSE: {:.5f}".format(test_rmse))
    else:
        train_accuracy = np.mean(train_pred == train_target)
        test_accuracy = np.mean(test_pred == test_target)
        print("Train accuracy: {:.1f}%".format(100 * train_accuracy))
        print("Test accuracy: {:.1f}%".format(100 * test_accuracy))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
