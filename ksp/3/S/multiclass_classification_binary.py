#!/usr/bin/env python3
import argparse

import numpy as np
import sklearn.datasets
import sklearn.linear_model
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()

parser.add_argument("--classes", default=10, type=int, help="Počet epoch na trénování Minibatch SGD")
parser.add_argument("--data_size", default=100, type=int, help="Velikost datasetu")
parser.add_argument("--test_size", default=0.5, type=float, help="Velikost testovací množiny")
parser.add_argument("--seed", default=42, type=int, help="Náhodný seed")
parser.add_argument("--type", default="ovr", choices=["ovr", "ovo"], help="Typ klasifikátoru")
parser.add_argument("--test", action='store_true', help="Vypisovat testovací hlášky")

class OneVsRest:
    def __init__(self, classes, seed, test):
        self.classes = classes
        # Do této proměnné si uložte modely natrénované během učení
        self.models = None
        self.seed = seed
        self.test = test

    def fit(self, data, target):
        # TODO: Vytvořte si pole o velikosti `self.classes` a natrénujte
        # modely. Každý model bude `sklearn.linear_model.LogisticRegression`
        # a každý bude mít nastavený parametr `random_state` na `self.seed`
        # (nic jiného nenastavujte).
        # Každý model má rozpoznávat jednu třídu od ostatních.

        self.models = self.classes * [None]
        for class_idx in range(self.classes):
            # Pro lehčí implementaci: pomocí `target[target != class_idx] = -1`
            # nastavíte cílové hodnoty (targety) na -1 pro všechny třídy, které nejsou
            # `class_idx`. Před touto změnou si nezapomeňte targety zkopírovat.
            self.models[class_idx] = sklearn.linear_model.LogisticRegression(random_state=self.seed)
            cur_target = target.copy()
            cur_target[target != class_idx] = -1
            self.models[class_idx].fit(data, cur_target)

    def predict(self, data):
        predictions = []

        for idx, dato in enumerate(data):
            # Predict funkce na sklearn modelu očekávájí 2D pole
            dato = dato[np.newaxis, :]

            probas = [0] * self.classes
            for model in self.models:
                # TODO: Pro každý model získejte pravděpodobnost, že dané dato
                # patří do třídy `i`.
                # Model vrací pravděpodobnosti pro všechny (pro nás 2 třídy), ale
                # jaká pravděpodobnost patří jaké třídě zjistíte pomocí
                # atributu `classes_` na jednotlivých modelech.
                probas[model.classes_[1]] = model.predict_proba(dato)[0][1]

            if self.test and idx < 5:
                # Testovací výpis pro kontrolu správnosti.
                print(" ".join(map(lambda x: f"{x:.4f}", probas)))

            # Vybere třídu s nejvyšší pravděpodobností.
            # Vracíme čísla tříd od 0 do self.classes-1.
            predictions.append(np.argmax(probas))

        return predictions

class OneVsOne:
    def __init__(self, classes, seed, test):
        self.classes = classes
        # Do této proměnné si uložte modely natrénované během učení
        self.models = None
        self.seed = seed
        self.test = test

    def fit(self, data, target):
        # TODO: Vytvořte si pole o velikosti `self.classes * (self.classes - 1) / 2`
        # a natrénujte modely. Každý model bude
        # `sklearn.linear_model.LogisticRegression` a každý bude mít nastavený
        # parametr `random_state` na `self.seed` (nic jiného nenastavujte).
        # Každý model má rozpoznávat jednu dvojici tříd.

        self.models = self.classes * (self.classes - 1) // 2 * [None]
        i = 0
        for class1 in range(self.classes):
            for class2 in range(class1 + 1, self.classes):
                # TODO: Pro lehčí implementaci: pomocí `target[(target==1) + (target==2)]`
                # vyberete jen třídy 1 a 2 z pole target.
                # Poté si stačí uložit tento výběr do jiné proměnné, abyste si
                # target nepřepsali. Podobný výběr uděláte i pro data:
                # `data[(target==1) + (target==2)]`.
                # Pokud nebudete chtít použít tento "trik", tak pro reproduvatelnost
                # testů vybírejte data a targety naráz, aby se zachovalo pořadí dat.
                cur_data = data[(target==class1) + (target == class2)]
                cur_target = target[(target==class1) + (target == class2)]
                self.models[i] = sklearn.linear_model.LogisticRegression(random_state=self.seed)
                self.models[i].fit(cur_data,cur_target)
                i += 1

    def predict(self, data):
        predictions = []
        for idx, dato in enumerate(data):
            # Predict funkce na sklearn modelu očekávájí 2D pole
            dato = dato[np.newaxis, :]

            votes = [0] * self.classes
            for model in self.models:
                # TODO: Pro každý model získejte klasifikaci třídy.
                # Každý model hlasuje právě pro jednu třídu.
                # Tip: Predict vrací čísla tříd na kterých model byl natrénován.
                # Model natrénovaný na páru tříd 2 a 8 bude predikovat třídy 2 a 8.
                votes[model.predict(dato)[0]] += 1

            if self.test and idx < 5:
                # Testovací výpis pro kontrolu správnosti.
                print(" ".join(map(str, votes)))

            # Vybere třídu s nejvíce hlasy.
            # Vracíme čísla tříd od 0 do self.classes-1.
            predictions.append(np.argmax(votes))

        return predictions


def main(args: argparse.Namespace):
    # Nastavení seedu generátoru náhodných čísel
    generator = np.random.RandomState(args.seed)

    # Vytvoření náhodného datasetu na klasifikační úlohu s počtem tříd `args.classes`.
    # Třídy mají hodnotu 0 až args.classes-1
    data, target = sklearn.datasets.make_classification(
        n_samples=args.data_size, n_informative=args.classes,
        n_classes=args.classes, random_state=args.seed
    )

    # TODO: Rozdělte dataset na trénovací a testovací část, funkci z knihovny sklearn
    # předejte argumenty `test_size=args.test_size, random_state=args.seed`.
    train_data, test_data, train_target, test_target = train_test_split(
        data, target, test_size=args.test_size, random_state=args.seed
    )

    if args.type == "ovr":
        classifier = OneVsRest(args.classes, args.seed, args.test)
    else:
        classifier = OneVsOne(args.classes, args.seed, args.test)

    classifier.fit(train_data, train_target)
    predictions = classifier.predict(test_data)

    if args.test:
        print("Predikované třídy pro první 10 dat:")
        print(" ".join(map(str, predictions[:10])))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
