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
    atomic_count = 711
    town = "hiroshima"
    sponsor = "ibm"
    sponsor = "jetbrains"
    sponsor = "rsj foundation"
    code = "26-Z2-4"

    minutes = intToRoman(datetime.now().minute)
    heslo = minutes + len(minutes) * "w" + "1"
    heslo += town + (len(town) - Counter(town)[" "]) * "A"
    heslo += "1" + sponsor + (len(sponsor) - 1) * "A"
    heslo += code
    iod = Counter(heslo)["I"]
    kal = Counter(heslo)["K"]
    vanad = Counter(heslo)["V"]
    nitro = Counter(heslo)["N"]
    phos = Counter(heslo)["P"]
    sulph = Counter(heslo)["S"]

    heslo += (atomic_count - sulph * 16 - phos * 15 - iod * 53 - kal * 19 - vanad * 23 - nitro * 7) * "Hw" 
    heslo += "1"
    print(len(heslo))
    print(heslo)
    # print(heslo)
    # res = requests.post("https://ksp.mff.cuni.cz/api/tasks/generate?task=36-4-4&subtask=1", data=heslo, headers={"Authorization": f"Bearer {token}"})
    # print(res.json())

