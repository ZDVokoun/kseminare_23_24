#!/usr/bin/env python3
import argparse

import numpy as np
import sklearn.datasets
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()

parser.add_argument("--classes", default=10, type=int, help="Počet tříd pro klasifikaci")
parser.add_argument("--learning_rate", default=0.01, type=float, help="Learning rate")
parser.add_argument("--epochs", default=50, type=int, help="Počet epoch na trénování Minibatch SGD")
parser.add_argument("--batch_size", default=10, type=int, help="Velikost batche")
parser.add_argument("--data_size", default=100, type=int, help="Velikost datasetu")
parser.add_argument("--test_size", default=0.5, type=float, help="Velikost testovací množiny")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")

def softmax(y):
    x = np.exp(y)
    return x/np.sum(x, axis=1, keepdims=True)

def main(args: argparse.Namespace):
    # Nastavení seedu generátoru náhodných čísel
    generator = np.random.RandomState(args.seed)

    # Vytvoření náhodného datasetu na klasifikační úlohu se dvěma třídami
    # třídy mají hodnotu 0 a 1
    data, target = sklearn.datasets.make_classification(
        n_samples=args.data_size, n_informative=args.classes,
        n_classes=args.classes, random_state=args.seed
    )

    # Přidání sloupce jedniček pro bias
    data = np.concatenate([data, np.ones([args.data_size, 1])], axis=1)

    # TODO: (SGD) Rozdělte dataset na trénovací a testovací část, funkci z knihovny sklearn
    # předejte argumenty `test_size=args.test_size, random_state=args.seed`.
    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    # Vytvoření náhodných vah
    weights = generator.uniform(size=[args.classes,train_data.shape[1]], low=-0.1, high=0.1)

    for epoch in range(args.epochs):
        # TODO: (SGD) Pro každou epochu náhodně zamíchejte trénovací množinu.
        # Na zamíchání použijte generator.permutation, které vrátí náhodnou permutaci
        # čísel od 0 do počtu prvků v množině.
        # Nemíchejte původní trénovací dataset, ale jen jeho kopii, tedy
        # `train_data` zůstane nezměněný přes všechny epochy.
        perm = generator.permutation(np.arange(train_data.shape[0]));
        perm_train_data = train_data[perm]
        perm_train_target = train_target[perm]

        # TODO: Pro každou batch s velikostí args.batch_size spočítejte gradient
        # a upravte váhy.
        # Můžete předpokládat, že args.batch_size je dělitelem počtu prvků v trénovací množině.
        for start in range(0, train_data.shape[0], args.batch_size):
            X_batch = perm_train_data[start: start + args.batch_size]
            y_batch = perm_train_target[start: start + args.batch_size]
            dot_prod = X_batch @ weights.T
            pred = softmax(dot_prod)
            for i in range(args.classes):
                for j in range(args.batch_size):
                    t = np.zeros(args.classes)
                    t[y_batch[j]] = 1
                    weights[i] -= args.learning_rate * (pred[j] - t)[i] * X_batch[j]

        # TODO: Na konci každé epochy spočítejte accuracy metriku na trénovací a testovací množině.
        # Accuracy metrika se počítá jako počet správných predikcí děleno počtem všech predikcí.
        # Metriku můžete spočítat explicitně nebo pomocí funkce `sklearn.metrics.accuracy_score`.
        # Metrika accuracy chce na vstupu již klasifikovaná data, ne pravděpodobnosti.
        prob_train = train_data @ weights.T
        pred_train = np.argmax(prob_train,axis=1)
        prob_test = test_data @ weights.T
        pred_test = np.argmax(prob_test,axis=1)
        train_accuracy, test_accuracy = accuracy_score(
            train_target, np.round(pred_train)
        ), accuracy_score(test_target, np.round(pred_test))

        # TODO: Poté spočítejte chybu logistické regrese na trénovací a testovací množině.
        # Chybu můžete spočítat explicitně nebo využít funkce `log_loss` v knihovně sklearn.
        # log-loss namísto accuracy chce na vstupu pravděpodobnosti, ne již klasifikovaná data.
        train_log_loss, test_log_loss = log_loss(train_target, prob_train, labels=np.arange(10)), log_loss(
            test_target, prob_test
        )

        print(f"Epoch {epoch+1}: train loss {train_log_loss:.6f} acc {train_accuracy*100:.2f}%, test loss {test_log_loss:.6f} acc {test_accuracy*100:.2f}%")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
