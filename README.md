# dream_park projet global
# DreamPark : système de gestion de parking

Projet Python, Université Toulouse 2 – Jean-Jaurès, Licence MIASHS (parcours Informatique et SHS), 3ᵉ année.

**Livraison actuelle :** Partie 0, spécification fonctionnelle et spécification des tests (branche `partie0`).
Aucune fonctionnalité n'est implémentée : les méthodes lèvent `NotImplementedError`. Seuls les constructeurs (stockage et validation des attributs) sont écrits.

## Auteurs

| Nom | Rôle |
|---|---|
| MUSHIMIYIMANA MOISE | Chargé de l'implementation et realisation du code |
| [NOM Prénom du binôme] | Chargé de la documentation et des tests |

**Dépôt git :** https://github.com/mushimiyimanamoise1-code/dream_park

## Livraisons

| Partie | Contenu | Branche | État |
|---|---|---|---|
| 0 | Spécification fonctionnelle et spécification des tests | `partie0` | en cours |
| 1 | Use case « Se garer » | `partie1` | à faire |
| 2 | Use case « Reprendre la voiture » | `partie2` | à faire |
| 3 | Gestion des statistiques | `partie3` | à faire |
| 4 | Interface graphique | `partie4` | à faire |

Chaque partie est construite par copie de la précédente.

## Structure du projet

```
dreampark/            code (squelettes documentés)
  abonnement.py       Abonnement
  acces.py            Acces
  client.py           Client
  contrat.py          Contrat
  equipements.py      Camera, Teleporteur, BorneTicket, PanneauAffichage
  outils.py           maintenant(), aujourd_hui() (heure de France)
  parking.py          Parking (singleton)
  place.py            Place
  placement.py        Placement
  service.py          Service, Maintenance, Entretien, Livraison, Voiturier
  voiture.py          Voiture
tests/                tests unitaires (unittest), un fichier par module
docs/                 documentation générée par pydoc (HTML)
generer_docs.py       script de génération de la documentation
TESTS.md              noms attendus par les tests et hypothèses
README.md
```

## Prérequis et installation

- Python 3.9 ou plus récent.
- Sous Windows, le paquet `tzdata` est nécessaire pour `zoneinfo` :

```bash
python -m pip install tzdata
```

Sans `tzdata`, `outils.py` se replie sur l'heure de la machine.

## Commandes

À lancer depuis la racine du projet (le dossier qui contient `dreampark/` et `tests/`).

```bash
# Tests unitaires (en Partie 0, les échecs sont attendus : ce sont les spécifications)
python -m unittest discover -s tests -t . -v

# Un seul fichier de tests
python -m unittest tests.test_parking -v

# Documentation pydoc de tout le package, dans docs/
python generer_docs.py

# Documentation d'un seul module
python -m pydoc -w dreampark.parking
```

## Conventions

- **Nommage :** méthodes et fonctions en `snake_case` (`rechercher_place`) ; attributs et propriétés en `camelCase` (`estLibre`, `nbPlacesLibres`), comme dans le diagramme de classes.
- **Documentation :** chaque classe et chaque méthode a une docstring (rôle, `:param:`, `:return:`, `:raises:`), qui constitue la spécification fonctionnelle.
- **Dates :** toutes les dates et heures sont en heure de France, via `outils.py` (`aujourd_hui()` retourne une `date`, `maintenant()` un `datetime` sans fuseau).
- **Erreurs :** `ValueError` pour une valeur invalide, `RuntimeError` pour une opération impossible dans l'état courant, `PermissionError` pour un service réservé aux abonnés.

## Répartition du travail

| Classes / use cases | Spécification | Tests |
|---|---|---|
| [ex. Parking, Place, Placement, Voiture] | [Prénom 1] | [Prénom 1] |
| [ex. Client, Abonnement, Contrat, Service] | [Prénom 2] | [Prénom 2] |
| [ex. Acces, équipements, outils] | [Prénom 1 / Prénom 2] | [Prénom 1 / Prénom 2] |

Intégration (menu, tests d'intégration) : [en binôme].

## Modifications apportées aux artefacts de modélisation

L'énoncé exige de justifier toute modification du diagramme de classes.

| # | Modification | Justification |
|---|---|---|
| 1 | `Parking.prix` conservé, valeur par défaut 0, contrôle `prix >= 0` | Conforme au diagramme. [préciser : tarif horaire ?] |
| 2 | `Parking.nbPlacesLibres` est une propriété calculée | Attribut dérivé (`/nbPlacesLibres`) : évite l'incohérence avec l'état réel des places. |
| 3 | `Place.idPlace` calculé = niveau + numéro | Note du diagramme (ex. « A1 », « C15 »). |
| 4 | `Place` : dimensions bornées (longueur 4 à 6 m, hauteur 2 à 4 m), niveau = une lettre majuscule | Le diagramme ne borne pas ces valeurs ; bornes réalistes et identifiants non ambigus. |
| 5 | Ajout de `Place.convient_a(voiture)` et `Place.liberer()` | Factorise le test de compatibilité et la libération à la reprise de la voiture. |
| 6 | `Parking.rechercher_place` retourne `None` si aucune place ne convient | « Valeur particulière » de l'énoncé. |
| 7 | Singleton : `Parking.obtenir_instance()` et `reinitialiser()` ajoutés ; le constructeur enregistre l'instance et lève `RuntimeError` si elle existe déjà | Une seule instance garantie, sans contournement par `Parking(...)` ; isolation des tests. |
| 8 | `Parking` crée ses places (niveaux A, B, ...) dans son constructeur | Composition `Parking ◆── Place` : le parking possède ses places. |
| 9 | `Voiture.estDansParking` est une propriété dérivée des placements en cours | Évite de maintenir un booléen à la main ; le diagramme le montre comme un attribut simple. |
| 10 | `Placement` reçoit `voiture` et `place` dans son constructeur ; `dateDebut` vaut aujourd'hui par défaut | Le diagramme ne montre que les dates ; l'association est nécessaire pour libérer la place. |
| 11 | `Contrat` dans son propre module ; `dateDebut` par défaut = aujourd'hui ; le jour de `dateFin` est inclus | Classe d'association distincte ; règle de durée explicite. |
| 12 | `Service.effectuer()` abstraite ajoutée ; dates de service en `datetime` | Polymorphisme sur Maintenance, Entretien, Livraison ; l'heure de la demande est utile (le diagramme indique `Date`). |
| 13 | `Client` : validation du nom et de l'adresse dans le constructeur [confirmer : pas de méthode d'inscription séparée] | Le constructeur crée déjà le client ; une méthode d'inscription ferait double emploi. |
| 14 | `outils.py` : `maintenant()` et `aujourd_hui()` centralisent la date de France | Une seule source de date pour toutes les classes ; repli si `tzdata` est absent. |
| 15 | `Acces` crée sa caméra, sa borne, son panneau et ses deux téléporteurs dans son constructeur | Le diagramme montre une agrégation ; création interne par simplicité, un accès en a toujours un de chaque. |
| 16 | [À décider] `Parking.acces1` et `acces2` | Le diagramme relie `Parking` à ses deux accès dans les deux sens ; seul `Acces → Parking` est implémenté. Un test ignoré (`@unittest.skip`) est prêt. |
| 17 | [À décider] `Contrat.client` et `Contrat.abonnement` | `Contrat` est une classe d'association ; sans ces liens, `Client.se_desabonner()` ne peut pas retrouver son contrat. |

## Hypothèses retenues

- Tous les niveaux du parking ont le même nombre de places (`nbPlacesParNiveau` est un entier, comme dans le diagramme).
- Rompre un contrat ne donne lieu à aucun remboursement ; la formule d'abonnement (`Abonnement`) n'est pas modifiée et le contrat reste dans l'historique.
- Les services (maintenance, entretien, livraison) sont réservés aux abonnés ; le pack garanti est un abonnement particulier (le client devient super-abonné).
- `Client.entrer_parking` n'incrémente `nbFrequentations` que si une place est attribuée.
- Les places créées par un parking acceptent au minimum une voiture de 1,5 m de haut et 4,0 m de long.
- [autres hypothèses à ajouter]

## Tests

Les tests sont écrits avec `unittest`, un fichier par module, avec une docstring par test décrivant le comportement vérifié : cas normaux, cas limites et cas d'erreur. Le détail des noms attendus et des hypothèses se trouve dans `TESTS.md`.

En Partie 0 ils échouent faute d'implémentation. Ils doivent tous passer à la fin de la Partie 1, à l'exception des tests ignorés (`@unittest.skip`) liés aux décisions ouvertes ci-dessus.

## Gestion du code

- Une branche par livraison (`partie0` à `partie4`), à pousser sur le dépôt du département.
- Les deux membres du binôme participent aux commits, à la maintenance et à la gestion du dépôt : [nombre de commits par personne, à renseigner à la livraison].
