import math
import time
import json
from datetime import datetime

# === ALGORITHME 1379 v1.1 – PAR mamson1295-cpu ===
def miller_rabin_deterministe(n):
    if n in {2, 3, 5, 7, 11}: return True
    if n < 2 or n % 2 == 0 or n % 3 == 0: return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    témoins = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37]
    for a in témoins:
        if a >= n: break
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1: break
        else:
            return False
    return True

def est_premier_rapide(n):
    if n < 2: return False
    if n in {2, 3, 5, 7}: return True
    if n % 2 == 0 or n % 5 == 0: return False
    if str(n)[-1] not in '1379': return False
    if n < 1_000_000:
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0: return False
        return True
    return miller_rabin_deterministe(n)

def prochain_premier_1379(p_n2, p_n1, p_n):
    c = p_n1 + p_n - p_n2
    ecart1 = p_n - p_n1
    ecart2 = p_n1 - p_n2
    borne = max(30, 3 * max(ecart1, ecart2, 6), int(math.log(p_n + 1)**2), 1500)
    fin = c + borne
    x = p_n + 2
    if x % 2 == 0: x += 1
    while x <= fin:
        if str(x)[-1] in '1379' and est_premier_rapide(x):
            return x
        x += 2
    while True:
        if str(x)[-1] in '1379' and est_premier_rapide(x):
            return x
        x += 2

# === RECORD MONDIAL EN COURS ===
def generer_record(limite=10**18):
    premiers = [2, 3, 5]
    p_n2, p_n1, p_n = 2, 3, 5
    debut = time.time()
    compteur = 3
    dernier_affichage = time.time()

    print("DÉMARRAGE DU RECORD MONDIAL – 1379 PRIME PREDICTOR")
    print(f"Par mamson1295-cpu | Début : {datetime.now()}\n")

    while p_n < limite:
        suivant = prochain_premier_1379(p_n2, p_n1, p_n)
        premiers.append(suivant)
        p_n2, p_n1, p_n = p_n1, p_n, suivant
        compteur += 1

        if time.time() - dernier_affichage > 10:
            vitesse = compteur / (time.time() - debut)
            print(f"{compteur:,} premiers | Dernier = {p_n:,} | Vitesse = {vitesse:,.0f}/s")
            dernier_affichage = time.time()

            with open("record_1379.json", "w") as f:
                json.dump({
                    "author": "mamson1295-cpu",
                    "count": compteur,
                    "last_prime": p_n,
                    "time_seconds": time.time() - debut,
                    "date": str(datetime.now()),
                    "algorithm": "1379 Prime Predictor v1.1",
                    "github": "https://github.com/mamson1295-cpu/1379-prime-record"
                }, f, indent=2)

    print(f"\nRECORD BATTU ! {compteur:,} nombres premiers générés !")
    return premiers

if __name__ == "__main__":
    generer_record()