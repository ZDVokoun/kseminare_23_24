import mam.Cislo2


def nasobky_sedmi : Nat → List Nat
| 0 => []
| n + 1 => (7 * n) :: (nasobky_sedmi n)

#eval nasobky_sedmi 6

-- Implementace níže je chybná, protože porovná čísla na indexech (0, 1), (2, 3), (4, 5)
-- ale neporovná čísla na indexech (1, 2), (3, 4) atd. To způsobí, že například pro vstup
-- [5, 5, 2, 2] vrátí tato funkce true

def je_konst {T : Type} [DecidableEq T] : List T → Bool
| [ ]                      => true
| [ _ ]                    => true
| prvni :: druhy :: zbytek => (prvni = druhy) && je_konst zbytek

#eval je_konst [5, 5, 5, 5]
#eval je_konst [5, 5, 3, 5]
#eval je_konst [1, 5, 5, 5]
#eval je_konst [5, 5, 5, 4]
#eval je_konst [5, 2, 5, 5]
#eval je_konst ['a', 'A']
#eval je_konst ['a', 'a']

-- Příklad vstupu, kdy funkce vrátí chybný výsledek
#eval je_konst [5, 5, 2, 2]

def soucin : List Int → Int
| [] => 1
| a :: lst => a * (soucin lst)

#eval soucin [2, 3]
#eval soucin [-3, 15, -2]
#eval soucin [953812, -748513, 0, -982331, 198234]

def vynech_opakovani {T : Type} [DecidableEq T] : List T → List T
| [ ] => []
| [ a ] => [ a ]
| a :: b :: lst => if (a = b) then (vynech_opakovani (b :: lst)) else a :: (vynech_opakovani (b :: lst))

#eval vynech_opakovani [1, 3, 3, 7]
#eval vynech_opakovani ['a', 'b', 'b', 'b', 'b', 'a', 'b', 'c', 'c', 'a']
#eval vynech_opakovani [7, 2, 2, 2, 2, 2]
#eval vynech_opakovani [4, 4, 4, 4, 5, 6]
#eval vynech_opakovani [0]
#eval vynech_opakovani [0, 0, 0]
#eval vynech_opakovani (List.range 8)
#eval vynech_opakovani ((List.range 8) ++ obrat (List.range 8))
#eval vynech_opakovani (List.map (· % 2) (List.range 20))
#eval vynech_opakovani (List.map (· / 2) (List.range 20))
#eval vynech_opakovani (List.map (· / 10) (List.range 20))
#eval vynech_opakovani (List.map je_ctverec (List.range 100))
#eval String.mk (vynech_opakovani "".toList)
#eval String.mk (vynech_opakovani "ahoj".toList)
#eval String.mk (vynech_opakovani "ahoooooooooooooooooooooooj".toList)
#eval String.mk (vynech_opakovani "       a           b            c      ".toList)

def pref_util (last: Int) : List Int → List Int
| [] => []
| a :: lst => (a + last) :: (pref_util (a + last) lst)

def prefixove_soucty : List Int → List Int
| lst => pref_util (0) lst

#eval prefixove_soucty [1, 2, 5, 0]
#eval prefixove_soucty [1, -5, 3, 2, 2, 2, 2]
#eval prefixove_soucty [0, 0, 10, -1, -2, -3, -4, -5, 0, 10, 0]

def postfixove_soucty : List Int → List Int
| lst => obrat_rychle (prefixove_soucty (obrat_rychle lst))

#eval postfixove_soucty [1, 2, 5, 0]
#eval postfixove_soucty [1, -5, 3, 2, 2, 2, 2]
#eval postfixove_soucty [0, 0, 10, -1, -2, -3, -4, -5, 0, 10, 0]
