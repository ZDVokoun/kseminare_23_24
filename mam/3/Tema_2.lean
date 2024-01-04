import mam.Cislo3

theorem na_druhou (a : ℚ) : a ^ 2 = a * a := by
  exact pow_two a

example (a b c d : ℕ) (a_je : a = b + d) (b_je : b = a * a) (c_je : c = b + d) (d_je : d = c * c) :
    b ^ d = d ^ b := by
  rw [b_je, d_je, a_je, c_je]

example (a b c d : ℤ) (a_je : a = d ^ 4) (b_je : b = 1 / c) (c_je : c = a - b) (d_je : d = 4 * a) :
    (a + b) ^ 2 - c ^ 2 = b * d := by
  rw [c_je, d_je, b_je, a_je]
  ring

example (x : ℝ) : 50*x^2 - 126*x + 96 ≥ 0 := by
  have test : 2500*x^2 - 6300*x + 3969 ≥ 0
  · convert_to (50*x - 63)^2 ≥ 0
    ring
    nlinarith
  linarith

example (x y : ℝ) : 2 * x^3 * y^3 ≤ x^4 * y^2 + x^2 * y^4 := by
  have : 0 ≤ x^4 * y^2 - 2 * x^3 * y ^ 3 + x^2 * y^4
  · convert_to 0 ≤ (x^2 * y - x * y^2) ^ 2
    ring
    nlinarith
  linarith

example (x y z : ℝ) : 4*x^2 + 12*x*y - 4*x*z + 9*y^2 - 6*y*z + z^2 ≥ 0 := by
  convert_to (2*x + 3*y - z)^2 ≥ 0
  · ring
  nlinarith

example (a b : ℝ) (ha : 0 < a) (hb : 0 < b) : 1 / a + 1 / b ≤ a / b^2 + b / a^2 := by
  have : (a+b)*(a-b)^2 ≥ 0
  · nlinarith
  have : a^3 + b^3 - a^2 * b - a * b^2 ≥ 0
  · convert this
    ring
  have : a^3 + b^3 ≥ a^2 * b + a * b^2
  · linarith
  have : (a^3 + b^3)/(a^2 * b^2) ≥ (a^2 * b + a * b^2)/(a^2 * b^2)
  · have levy : (a^3 + b^3) ≥ 0
    nlinarith
    have samozrejmnost : (a^2 * b^2) ≤ (a^2 * b^2)
    exact refl (a^2 * b^2)
    have delitel : (a^2 * b^2) > 0
    have : 0 < a * b
    nlinarith
    nlinarith
    exact div_le_div levy this delitel samozrejmnost
  have : a^3/(a^2 * b^2) + b^3/(a^2 * b^2) ≥ (a^2 * b + a * b^2)/(a^2 * b^2)
  · convert this
    exact div_add_div_same (a^3) (b^3) (a^2 * b^2)
  have : (a^2 * b)/(a^2 * b^2) + (a * b^2)/(a^2 * b^2) ≤ a^3/(a^2 * b^2) + b^3/(a^2 * b^2)
  · convert this
    exact div_add_div_same (a^2 * b) (a * b^2) (a^2 * b^2)
   -- jediné, co zbývá, je jen zjednodušit výraz (vykrátit všechny zlomky)
