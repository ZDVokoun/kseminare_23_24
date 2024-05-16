#!/usr/bin/env python3
import argparse

import sklearn.datasets
import numpy as np
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default="wine", type=str, help="Použitý dataset; buď `wine` nebo `diabetes`",
                    choices=["wine", "diabetes"])
parser.add_argument("--max_depth", default=None, type=int, help="Maximální hloubka rozhodovacího stromu")
parser.add_argument("--max_leaves", default=None, type=int, help="Maximální počet listů stromu")
parser.add_argument("--min_to_split", default=2, type=int, help="Minimální počet dat pro rozdělení vrcholu (listu)")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument("--test_size", default=0.25, type=float, help="Velikost testovací množiny")

def SE(targets):
    pr = np.mean(targets)
    targets -= np.ones(len(targets)) * pr
    return targets.dot(targets)


class TreeNode:
    def __init__(self,data) -> None:
        self.split_feature = -1
        self.split_value = -1
        self.left = None
        self.right = None
        self.data = data

    def best_split(self):
        for feature in range(self.data.shape[1]):
            indices = np.argsort(self.data[:,feature])
            for i in range(indices.shape[0] - 1)


def main(args: argparse.Namespace):
    # Načtení datasetu.
    data, target = getattr(sklearn.datasets, "load_{}".format(args.dataset))(return_X_y=True)

    # TODO: Rozdělte dataset na trénovací a testovací část, funkci z knihovny sklearn
    # předejte argumenty `test_size=args.test_size, random_state=args.seed`.
    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    # TODO: Implementace binárního rozhodovacího stromu
    #
    # - Budete implementovat strom pro klasifikaci i regresi podle typu
    #   datasetu. `wine` dataset je pro klasifikaci a `diabetes` pro regresi.
    #
    # - Pro klasifikaci: Pro každý list predikujte třídu, která je nejčastější
    #   (a pokud je těchto tříd několik, vyberte tu s nejmenším číslem).
    # - Pro regresi: Pro každý list predikujte průměr target (cílových) hodnot.
    #
    # - Pro klasifikaci použijte jako kritérium entropy kritérium a pro regresi
    #   použijte jako kritérium SE (squared error).
    #
    # - Pro rozdělení vrcholu vyzkoušejte postupně všechny featury. Pro každou
    #   featuru vyzkoušejte všechna možná místa na rozdělení seřazená vzestupně
    #   a rozdělte vrchol na místě, který nejvíce sníží kritérium.
    #   Pokud existuje takových míst několik, vyberte první z nich.
    #   Každé možné místo na rozdělení je průměrem dvou nejbližších unikátních hodnot
    #   featur z dat odpovídající danému vrcholu.
    #   Např. pro čtyři data s hodnotami featur 1, 7, 3, 3 jsou místa na rozdělení 2 a 5.
    #
    # - Rozdělení vrcholu povolte pouze pokud:
    #   - pokud hloubka vrcholu je menší než `args.max_depth`
    #     (hloubka kořenu je nula). Pokud `args.max_depth` je `None`,
    #     neomezujte hloubku stromu.
    #   - pokud je méně než `args.max_leaves` listů ve stromě
    #     (list je vrchol stromu bez synů). Pokud `args.max_leaves` je `None`,
    #     neomezujte počet listů.
    #   - je alespoň `args.min_to_split` dat v daném vrcholu.
    #   - hodnota kritéria není nulová.
    #
    # - Pokud `args.max_leaves` není `None`: opakovaně rozdělujte listové vrcholy,
    #   které splňují podmínky na rozdělení vrcholu a celková hodnota kritéria
    #   ($c_{levý syn} + c_{pravý syn} - c_{rodič}$) nejvíce klesne.
    #   Pokud je několik takových vrcholů, vyberte ten, který byl vytvořen dříve
    #   (levý syn je považován, že je vytvořený dříve než pravý syn).
    #
    #   Pokud `args.max_leaves` je `None`, použijte rekurzivní přístup (nejdříve rozdělujte
    #   levé syny, poté pravé syny) a rozdělte každý vrchol, který splňuje podmínky.
    #   Tento rekurzivní přístup není důležitý v této úloze, ale až v nasledující
    #   úloze - Random Forest.
    #
    # - Nakonec vypočítejte trénovací a testovací chybu
    #   - RMSE, root mean squared error, pro regresi
    #   - accuracy pro klasifikaci
    
    if args.dataset == 'diabetes':
        train_rmse = ...
        test_rmse = ...
        print("Train RMSE: {:.5f}".format(train_rmse))
        print("Test RMSE: {:.5f}".format(test_rmse))
    else:
        train_accuracy = ...
        test_accuracy = ...
        print("Train accuracy: {:.1f}%".format(100 * train_accuracy))
        print("Test accuracy: {:.1f}%".format(100 * test_accuracy))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
