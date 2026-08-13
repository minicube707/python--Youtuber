# Concurrence et parallélisme en Python : async, multithreading, multiprocessing, subprocess

Python propose plusieurs façons de gérer la concurrence et le parallélisme, chacune adaptée à des cas d'usage bien précis. Ce document explique le fonctionnement de chacune de ces approches, leurs cas d'usage idéaux, et leurs limites.

## 1. `async` (asyncio) — la concurrence coopérative

`asyncio` permet d'exécuter du code de manière **concurrente** (mais pas parallèle) sur un **seul thread**. Le principe repose sur une boucle d'événements (*event loop*) qui gère plusieurs tâches (`coroutines`) en alternant entre elles. Quand une tâche atteint une opération bloquante (comme une requête réseau), elle "rend la main" (`await`) à la boucle d'événements, qui peut alors exécuter une autre tâche pendant que la première attend. C'est une concurrence **coopérative** : le code doit explicitement céder le contrôle avec `await`, contrairement au threading où le système d'exploitation peut interrompre un thread à tout moment. Il n'y a **pas de vrai parallélisme** ici : un seul thread, un seul cœur CPU utilisé, mais une excellente efficacité pour gérer des milliers de tâches d'attente simultanées avec très peu de overhead (pas de création de threads ou de processus).

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com"] * 5
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())
```

**Quand l'utiliser** : idéal pour les tâches **I/O bound** avec un très grand nombre d'opérations concurrentes (serveurs web, clients HTTP, websockets, bases de données asynchrones). Nécessite que les bibliothèques utilisées soient compatibles `async` (ex: `aiohttp`, `asyncpg`), sinon on perd tout le bénéfice.

---

## 2. `threading` (multithreading) — plusieurs threads, un seul processus

Le multithreading crée plusieurs threads au sein d'un **même processus**, qui partagent la même mémoire. En théorie, ces threads pourraient s'exécuter en parallèle sur plusieurs cœurs CPU. Mais en Python (dans l'implémentation standard CPython), le **GIL** (*Global Interpreter Lock*) empêche plusieurs threads d'exécuter du bytecode Python **en même temps**. Un seul thread peut détenir le GIL à un instant donné. Cependant, le GIL est **libéré automatiquement** lors des opérations d'I/O (lecture de fichier, requête réseau, etc.), ce qui permet à d'autres threads de s'exécuter pendant ce temps. Le threading est donc utile pour l'attente, mais n'apporte aucun gain pour du calcul pur.

```python
import threading
import requests

def fetch(url, results, index):
    response = requests.get(url)
    results[index] = response.status_code

urls = ["https://example.com"] * 5
results = [None] * len(urls)
threads = []

for i, url in enumerate(urls):
    t = threading.Thread(target=fetch, args=(url, results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(results)
```

**Quand l'utiliser** : bon pour les tâches **I/O bound** quand on travaille avec des bibliothèques **bloquantes** (non-async), comme `requests`. Moins efficace qu'`asyncio` pour des milliers de tâches simultanées (chaque thread a un coût mémoire et de contexte), mais plus simple à intégrer dans du code existant synchrone. **Inutile voire contre-productif pour du CPU bound** à cause du GIL.

---

## 3. `multiprocessing` — plusieurs processus, vrai parallélisme

Le module `multiprocessing` crée de **véritables processus séparés**, chacun avec son propre interpréteur Python et son propre espace mémoire. Comme chaque processus a son propre GIL, ils peuvent s'exécuter **réellement en parallèle** sur plusieurs cœurs CPU. C'est la seule solution native en Python pour contourner la limitation du GIL. La contrepartie : les processus ne partagent pas la mémoire, donc échanger des données entre eux nécessite une sérialisation (`pickle`) via des mécanismes comme les `Queue`, `Pipe`, ou la mémoire partagée, ce qui ajoute de l'overhead. Le démarrage d'un processus est aussi plus coûteux que celui d'un thread.

```python
from multiprocessing import Pool
import math

def calcul_intensif(n):
    return sum(math.sqrt(i) for i in range(n))

if __name__ == "__main__":
    valeurs = [10_000_000] * 4
    with Pool(processes=4) as pool:
        resultats = pool.map(calcul_intensif, valeurs)
    print(resultats)
```

**Quand l'utiliser** : idéal pour les tâches **CPU bound** (calcul scientifique, traitement d'images, compression, machine learning) qu'on veut répartir sur plusieurs cœurs pour exploiter pleinement le matériel. À éviter pour des tâches légères ou très nombreuses à cause du coût de création des processus et de la sérialisation des données.

---

## 4. `subprocess` — lancer des programmes externes

`subprocess` ne concerne pas la concurrence au sein de votre programme Python, mais permet de **lancer et contrôler d'autres programmes** (exécutables, scripts shell, autres langages) depuis Python, en tant que processus enfants indépendants. Contrairement à `multiprocessing` qui lance d'autres instances de Python exécutant du code Python, `subprocess` peut exécuter **n'importe quel programme** du système (`ls`, `ffmpeg`, un script bash, un binaire compilé en C, etc.). On peut récupérer sa sortie standard, lui envoyer une entrée, vérifier son code de retour, et éventuellement attendre sa fin ou le laisser tourner en arrière-plan.

```python
import subprocess

resultat = subprocess.run(
    ["ffmpeg", "-i", "video.mp4", "-vn", "audio.mp3"],
    capture_output=True,
    text=True
)

print(resultat.stdout)
print("Code de retour :", resultat.returncode)
```

**Quand l'utiliser** : dès que vous devez interagir avec un **programme externe** non-Python (outils système, binaires spécialisés, scripts shell, autres runtimes comme Node.js). Ce n'est pas un outil de parallélisation de votre logique Python, mais un outil d'**intégration système**.

---

## Résumé : quelle différence entre les 4 ?

| Approche | Mécanisme | Parallélisme réel ? | Cas d'usage idéal |
|---|---|---|---|
| **asyncio** | Un seul thread, coroutines coopératives | Non | I/O bound, très nombreuses tâches concurrentes (réseau, API) |
| **threading** | Plusieurs threads, un processus, limité par le GIL | Non (sauf pendant l'I/O) | I/O bound avec libs bloquantes (non-async) |
| **multiprocessing** | Plusieurs processus indépendants | Oui | CPU bound, calculs lourds à répartir sur plusieurs cœurs |
| **subprocess** | Lancement de programmes externes | Oui (processus séparé) | Exécuter un programme non-Python depuis votre script |

En résumé, la question à se poser est double :
1. **Le code Python que j'écris fait-il attendre (I/O) ou calculer (CPU) ?**
   - I/O bound → `asyncio` (si les libs le supportent) ou `threading` (sinon).
   - CPU bound → `multiprocessing`.
2. **Ai-je besoin d'exécuter mon propre code Python en parallèle, ou un programme externe ?**
   - Code Python → `multiprocessing` / `threading` / `asyncio`.
   - Programme externe → `subprocess`.

`asyncio` et `threading` résolvent le même type de problème (I/O bound) avec des philosophies différentes (coopératif vs préemptif), tandis que `multiprocessing` est la seule option pour du vrai parallélisme CPU en contournant le GIL, et `subprocess` sort complètement du cadre de la concurrence "interne" pour piloter des processus externes.
