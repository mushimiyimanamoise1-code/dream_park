# DreamPark : Partie 0 (spécification fonctionnelle et spécification des tests)

**Auteurs :** MUSHIMIYIMANA MOISE
**Branche git :** `partie0`

Aucune fonctionnalité n'est implémentée : les méthodes lèvent `NotImplementedError`.
Les constructeurs se contentent de stocker les attributs.

## Structure
- `dreampark/` : squelettes de classes + docstrings + outils (contient les elements globals)
- `tests/` : classes de test (`unittest`), écrites pour échouer tant que la Partie 1+ n'est pas faite
- `docs/` : documentation `pydoc` (HTML)
- `generer_docs` : code pour generer les `pydoc`

## Prérequis et installation
** python 3.
** Le paquet tzdata, nécessaire pour zoneinfo :

```
python -m pip install tzdata
```

## Commandes (depuis la racine du projet)
```bash
python -m unittest discover -s tests -t . -v   # échecs attendus en partie 0 (car les methodes ne sont pas implementées)
python -m pydoc -w dreampark.parking           # générer la doc d'un module

NB : l'execution du fichier generer_docs.py, permet de generer tous les pydoc en meme temps
```



## Répartition du travail (à compléter)
| Classes / use cases | Spécification | Tests |
|---|---|---|
| [ex. Parking, Place, Placement] | [Prénom 1] | [Prénom 1] |
| [ex. Client, Abonnement, Contrat] | [Prénom 2] | [Prénom 2] |

## Modifications apportées au diagramme de classes (à justifier)
| # | Modification | Justification |
|---|---|---|
| 1 | `Parking.nbPlacesLibres` devient une propriété calculée (`/nbPlacesLibres` en UML) | Évite l'incohérence avec l'état réel des places. |
| 3 | `Place.idPlace` calculé = niveau + numéro | Cf. note du diagramme (ex. 'A1'). |
| 4 | Ajout de `Place.convient_a(voiture)` et `Place.liberer()` | Factorise le test de compatibilité et la libération (reprise de voiture). |
| 5 | `Parking.rechercher_place` retourne `None` si plein | « Valeur particulière » de l'énoncé. |
| 6 | `Parking.obtenir_instance()` et `reinitialiser()` ajoutés | Implémentation du singleton, isolation des tests. |
| 7 | `Service.effectuer()` abstraite ajoutée | Polymorphisme sur Maintenance/Entretien/Livraison. |
| 8 | `Client.abonnement` : un seul abonnement actif ; `est_super_abonne` = pack garanti | Note du diagramme UC (pack garanti = abonnement). |
| 9 | `Placement.voiture` et `Placement.place` ajoutés au constructeur | Le diagramme ne montre que les dates ; l'association est nécessaire. |
| 10 | `Acces.lancer_procedure_entree` : déroule le diagramme d'activité « Se garer » | Cohérence UC / activité / classes. |
