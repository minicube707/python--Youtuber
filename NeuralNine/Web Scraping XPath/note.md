# XPath - Notes de cours

## 1. Qu'est-ce que XPath ?

**XPath** (*XML Path Language*) est un langage permettant de naviguer et de sélectionner des éléments dans un document **XML** ou **HTML**. Lien util: https://xpather.com/

Il est principalement utilisé pour :

* 🌐 Le web scraping
* 🤖 L'automatisation avec Selenium
* 📄 La manipulation de fichiers XML
* ✅ Les tests automatisés

---

## 2. Exemple de document HTML

```html
<html>
    <body>
        <h1>Titre</h1>
        <p class="texte">Bonjour</p>
    </body>
</html>
```

---

## 3. Chemin absolu (`/`)

Le caractère `/` indique un chemin complet depuis la racine du document.

```xpath
/html
```

```xpath
/html/body/h1
```

Résultat :

```html
<h1>Titre</h1>
```

> Les chemins absolus sont très précis mais deviennent rapidement fragiles si la structure de la page change.

---

## 4. Chemin relatif (`//`)

Le double slash recherche un élément **n'importe où** dans le document.

```xpath
//h1
```

Retourne tous les éléments `<h1>`.

Autres exemples :

```xpath
//p
```

```xpath
//div
```

```xpath
//button
```

---

## 5. Sélection avec un attribut

Les attributs sont précédés du symbole `@`.

HTML :

```html
<p class="texte">Bonjour</p>
```

XPath :

```xpath
//p[@class='texte']
```

Résultat :

```html
<p class="texte">Bonjour</p>
```

---

## 6. Plusieurs conditions

```xpath
//input[@type='text']
```

```xpath
//a[@href='/login']
```

```xpath
//input[@type='text' and @name='username']
```

---

## 7. L'opérateur `contains()`

Permet de vérifier qu'un texte est présent.

```xpath
//div[contains(@class,'menu')]
```

Correspond par exemple à :

```html
<div class="menu-principal">
```

ou

```html
<div class="grand-menu">
```

---

## 8. `starts-with()`

Recherche les attributs commençant par une valeur.

```xpath
//input[starts-with(@id,'user')]
```

Correspond à :

```html
<input id="user123">
```

```html
<input id="user_name">
```

---

## 9. `text()`

Permet d'accéder au texte contenu dans un élément.

HTML :

```html
<h1>Bienvenue</h1>
```

XPath :

```xpath
//h1/text()
```

Résultat :

```text
Bienvenue
```

---

## 10. `contains(text(), ...)`

Recherche un texte contenu dans un élément.

```xpath
//button[contains(text(),'Connexion')]
```

Correspond à :

```html
<button>Connexion</button>
```

ou

```html
<button>Se connecter - Connexion</button>
```

---

## 11. Position des éléments

Premier élément :

```xpath
(//a)[1]
```

Deuxième :

```xpath
(//a)[2]
```

Troisième :

```xpath
(//a)[3]
```

Dernier :

```xpath
(//a)[last()]
```

---

## 12. Parent (`..`)

Remonte d'un niveau dans l'arborescence.

```xpath
//span/..
```

---

## 13. Enfant (`/`)

Sélectionne uniquement les enfants directs.

```xpath
//div/p
```

---

## 14. Descendants (`//`)

Recherche tous les descendants.

```xpath
//div//a
```

---

## 15. Wildcard (`*`)

Le caractère `*` signifie **n'importe quel élément**.

Tous les éléments :

```xpath
//*
```

Tous les enfants :

```xpath
//div/*
```

---

## 16. Tous les attributs

```xpath
//div/@*
```

---

## 17. Opérateurs logiques

### ET (`and`)

```xpath
//input[@type='text' and @name='username']
```

### OU (`or`)

```xpath
//input[@type='text' or @type='email']
```

### Négation (`not()`)

```xpath
//input[not(@disabled)]
```

---

## 18. Fonctions XPath utiles

| Fonction        | Description         |
| --------------- | ------------------- |
| `text()`        | Texte de l'élément  |
| `contains()`    | Contient une valeur |
| `starts-with()` | Commence par        |
| `last()`        | Dernier élément     |
| `position()`    | Position actuelle   |
| `not()`         | Négation            |

---

## 19. Exemples pratiques

Tous les liens :

```xpath
//a
```

Toutes les images :

```xpath
//img
```

Tous les boutons :

```xpath
//button
```

Tous les formulaires :

```xpath
//form
```

Champ email :

```xpath
//input[@type='email']
```

Champ mot de passe :

```xpath
//input[@type='password']
```

Champ de recherche :

```xpath
//input[@type='search']
```

---

## 20. Exemple complet

HTML :

```html
<div class="card">
    <h2>Produit</h2>
    <span class="prix">29 €</span>
    <button>Acheter</button>
</div>
```

XPath :

Titre :

```xpath
//div[@class='card']/h2
```

Prix :

```xpath
//span[@class='prix']
```

Bouton :

```xpath
//button[text()='Acheter']
```

Ou plus souple :

```xpath
//button[contains(text(),'Acheter')]
```

---

# Résumé

| Symbole         | Signification     |
| --------------- | ----------------- |
| `/`             | Chemin absolu     |
| `//`            | Recherche partout |
| `@`             | Attribut          |
| `*`             | Tous les éléments |
| `..`            | Parent            |
| `text()`        | Texte             |
| `contains()`    | Contient          |
| `starts-with()` | Commence par      |
| `last()`        | Dernier élément   |
| `position()`    | Position          |
| `and`           | ET logique        |
| `or`            | OU logique        |
| `not()`         | Négation          |

---

# Bonnes pratiques

* Utiliser les **XPath relatifs (`//`)** lorsque c'est possible.
* Éviter les chemins absolus très longs.
* Préférer `contains()` lorsque les classes CSS sont susceptibles de changer.
* Tester les expressions XPath avec les outils de développement du navigateur (`F12`).
* Écrire des XPath simples et lisibles pour faciliter leur maintenance.
