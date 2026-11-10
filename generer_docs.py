"""Génère la documentation pydoc de tout le package dans docs/."""
import importlib
import os
import pkgutil
import pydoc
import traceback

import dreampark

os.makedirs("docs", exist_ok=True)
os.chdir("docs")

noms = ["dreampark"] + [f"dreampark.{m.name}" for m in pkgutil.iter_modules(dreampark.__path__)]

for nom in noms:
    try:
        importlib.import_module(nom)
        pydoc.writedoc(nom)
    except Exception:
        print(f"\n--- ÉCHEC : {nom} ---")
        traceback.print_exc()

print("\nModules traités :", len(noms))