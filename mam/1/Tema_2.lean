import mam.Cislo1


def povrch_kvadru (a b c : Nat) : Nat := 2 * (a*b + b*c + c*a)

#eval povrch_kvadru 2 3 4    /- `52` -/
#eval povrch_kvadru 6 6 6    /- `216` -/
#eval povrch_kvadru 14 0 7    /- `196` -/
#eval povrch_kvadru 999 1000 1001   /- `5999998` -/

private def s (a b c: Float) : Float := (a + b + c) / 2

def obsah_trojuhelniku (a b c : Float) : Float := 
  Float.sqrt ((s a b c) * ((s a b c) - a) * ((s a b c) - b) * ((s a b c) - c))

#eval obsah_trojuhelniku 12.7 15.8 19.4    /- `99.957071` -/
#eval obsah_trojuhelniku 3 4 5    /- `6` -/
#eval obsah_trojuhelniku 12 5 13    /- `30` -/
#eval obsah_trojuhelniku 1 1 1    /- `0.433013` -/
#eval obsah_trojuhelniku 1 1 0    /- `0` -/
#eval obsah_trojuhelniku 2 1 1    /- `0` -/
#eval obsah_trojuhelniku 500 999 500    /- `11166.366909` -/

/-
Funkce parita vrací pro výraz parita (2 - 3) "sude", protože funkce
parita přijímá jen přirozená čísla a z dokumentace Leanu se můžeme
dočíst následující:

For natural numbers, this operator saturates at 0: a - b = 0 when a ≤ b. 

Z toho vyplývá, že se výraz (2 - 3) vynuloval, proto to vracelo tento výsledek.
-/

def je_ctvrta_mocnina (a : Nat) : Bool := Nat.sqrt (Nat.sqrt a) ^ 4 = a

#eval je_ctvrta_mocnina 15
#eval je_ctvrta_mocnina 16
#eval je_ctvrta_mocnina 17
#eval je_ctvrta_mocnina 0
#eval je_ctvrta_mocnina 1
#eval je_ctvrta_mocnina 2
#eval je_ctvrta_mocnina 3
#eval je_ctvrta_mocnina 4
#eval je_ctvrta_mocnina 5
#eval List.filter je_ctvrta_mocnina (List.range 5000) /- `[0, 1, 16, 81, 256, 625, 1296, 2401, 4096]` -/

private def d (a b c : Float) : Float := b^2 - 4 * a * c

def reseni_kvadraticke_rovnice (a b c : Float) : List Float := 
  if d a b c < 0
  then []
  else if d a b c > 0
    then [(-b - Float.sqrt (d a b c)) / ( 2 * a ), (-b + Float.sqrt (d a b c)) / ( 2 * a )]
    else [(-b) / ( 2 * a )]

/- `x^2 = 2` -/
#eval reseni_kvadraticke_rovnice 1 0 (-2)
/- `[-1.414214, 1.414214]` -/

/- `x^2 = 9` -/
#eval reseni_kvadraticke_rovnice (-1) 0 9
/- `[3, -3]` -/

/- `x^2 = 1/2` -/
#eval reseni_kvadraticke_rovnice 2 0 (-1)
/- `[-0.707107, 0.707107]` -/

/- `25x^2 = 1` -/
#eval reseni_kvadraticke_rovnice (-25) 0 1
/- `[0.2, -0.2]` -/

/- `x^2 + 2x + 1 = 0` -/
#eval reseni_kvadraticke_rovnice 1 2 1
/- `[-1]` -/

/- `x^2 + x + 1 = 0` -/
#eval reseni_kvadraticke_rovnice 1 1 1
/- `[]` -/

/- `x^2 + -6x + 9 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-6) 9
/- `[3]` -/

/- `x^2 + -6x + 10 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-6) 10
/- `[]` -/

/- `x^2 - 14x + 49 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-14) 49
/- `[7]` -/

/- `x^2 - 14x + 50 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-14) 50
/- `[]` -/

/- `x^2 - 14x + 48 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-14) 48
/- `[6, 8]` -/

/- `x^2 - 29x - 28 = 0` -/
#eval reseni_kvadraticke_rovnice 1 (-29) 28
/- `[1, 28]` -/

/- `x^2 + 18x + 77 = 0` -/
#eval reseni_kvadraticke_rovnice 1 18 77
/- `[-11, -7]` -/

/- `77x^2 + 18x + 1 = 0` -/
#eval reseni_kvadraticke_rovnice 77 18 1
/- `[-0.142857, -0.0909091]` -/

/- `16x^2 + 40x + 25 = 0` -/
#eval reseni_kvadraticke_rovnice 16 40 25
/- `[-1.25]` -/

/- `25x^2 + 40x + 16 = 0` -/
#eval reseni_kvadraticke_rovnice 25 40 16
/- `[-0.8]` -/

partial def ciferace (a : Nat) : Nat := 
  if a >= 10 
    then ciferace (ciferny_soucet a)
    else a

#eval ciferace 3
#eval ciferace 52
#eval ciferace 919
#eval ciferace 999
#eval ciferace 123456
#eval ciferace 100000000000000000000000000000000000000000000000000000001
#eval ciferace 9999999999999999999999999999999999999999999999999999999999999

-- Přes řádek
private def c (g : Nat → Nat → Nat → Nat) (x y : Nat) : Nat → Nat
  | 0 => (g x y 0)
  | n + 1 => Nat.max (g x y n) (c g x y n)

-- Přes obdélník
private def b (g : Nat → Nat → Nat → Nat) (x n : Nat) : Nat → Nat
  | 0 => (c g x 0 n)
  | m + 1 => Nat.max (c g x m n) (b g x n m)

-- Přes kvádr
private def a (g : Nat → Nat → Nat → Nat) (n : Nat) : Nat → Nat
  | 0 => (b g 0 n n)
  | m + 1 => Nat.max (b g m n n) (a g n m)

def maximum_z_krychle (g : Nat → Nat → Nat → Nat) (n : Nat) : Nat := 
  (a g n n) 

#eval maximum_z_krychle (fun x y z => x + y - z) 10    /- `18` -/
#eval maximum_z_krychle (fun x y z => x * (6-x) * y * (4-y) * z * (10-z)) 7    /- `900` -/

private def not_a_prime(x: Nat) : Nat → Bool
  | 0 => x == 0 || x == 1
  | 1 => false
  | n + 1 => (not_a_prime x n) || (x % (n + 1) == 0)

def je_prvocislo (a : Nat) : Bool := 
  (!not_a_prime a (a - 1)) 

private def get_sum_of_dividers (x: Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => 
    if x % (n + 1) = 0 
    then n + 1 + get_sum_of_dividers x n
    else get_sum_of_dividers x n

def je_dokonale_cislo (a : Nat) : Bool := 
  (get_sum_of_dividers a (a - 1)) = a 


def vypis_splnujici_do (podminka : Nat → Bool) (n : Nat) :=
List.filter podminka (List.range (n+1))

def seznam_prvocisel_do (n : Nat) :=
vypis_splnujici_do je_prvocislo n

#eval seznam_prvocisel_do 40
#eval seznam_prvocisel_do 100

def seznam_dokonalych_cisel_do (n : Nat) :=
vypis_splnujici_do je_dokonale_cislo n

#eval seznam_dokonalych_cisel_do 500
#eval seznam_dokonalych_cisel_do 10000
