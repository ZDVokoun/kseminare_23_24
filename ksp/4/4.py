import requests
from datetime import datetime
from collections import Counter
import re

def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]
 
    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
 
    ans = (thousands + hundreds +
           tens + ones)
 
    return ans

if __name__ == "__main__":
    with open("/home/ondra/.config/ksp-api-token") as f:
        token = f.readline().strip()
    # gen = requests.post("https://ksp.mff.cuni.cz/api/tasks/generate?task=36-4-4&subtask=1", headers={"Authorization": f"Bearer {token}"})
    atomic_count = 792
    town = "zaporizhzhia"
    sponsor = "rsj foundation"
    sponsor = "jetbrains"
    sponsor = "ibm"
    code = """
#!/usr/bin/env python3
# Author: Dan Skýpala
from math import inf
n, k = map(int, input().split())

boxes = []
lids = []
for i in range(n):
    a, b = map(int, input().split())
    boxes.append(a)
    lids.append(b)

# states[i][j] - trojice:
# - nejvyšší hodnota čaje, kterou jsme schopni zachránit
#   v prvních i-1 krabicích, kde poslední víko je na i+j-k-té krabici
# - ze kterého předchozího j jsme stav vyrobili
# - kam jsme dali víko z téhle pozice
states = [[(-inf, -1, False)]*(2*k+1) for i in range(n+1)]
states[0][k] = (0, -1, False)
for i in range(n):
    if lids[i]: # umístíme víko
        val_max, j_max = -inf, -1
        for j in range(2*k+1):
            if i+j-k >= n:
                break
            if states[i][j][0] > val_max:
                val_max = states[i][j][0]
                j_max = j
            states[i+1][j] = max(states[i+1][j], (val_max + boxes[i+j-k], j_max, i+j-k))

    else: # posuneme všechny krabice o 1 dopředu
        states[i+1][0] = (states[i][0][0], 0, -inf)
        for j in range(2*k):
            states[i+1][j] = max(states[i+1][j], (states[i][j+1][0], j+1, -inf))

# zpětná rekonstrukce
res_j = states[-1].index(max(states[-1]))
print(states[-1][res_j][0])
for i in range(n, 0, -1):
    if states[i][res_j][2] != -inf:
        print(i, states[i][res_j][2]+1)
    res_j = states[i][res_j][1]
    """
    code = re.sub(r'[^\x00-\x7F]+|\n',' ', code)

    minutes = intToRoman(datetime.now().minute)
    heslo = minutes + len(minutes) * "w" + "1"
    heslo += town + (len(town) - Counter(town)[" "]) * "A"
    heslo += "1" + sponsor + (len(sponsor) - 1) * "A"
    iod = Counter(heslo)["I"]
    kal = Counter(heslo)["K"]
    vanad = Counter(heslo)["V"]
    nitro = Counter(heslo)["N"]
    phos = Counter(heslo)["P"]

    heslo += (atomic_count - phos * 15 - iod * 53 - kal * 19 - vanad * 23 - nitro * 7) * "Hw" 
    heslo += "1" + code + (sum(1 for c in code if c.isupper())) * "w" + (sum(1 for c in code if c.islower())) * "A"
    print(heslo)
    # res = requests.post("https://ksp.mff.cuni.cz/api/tasks/generate?task=36-4-4&subtask=1", data=heslo, headers={"Authorization": f"Bearer {token}"})
    # print(res.json())

