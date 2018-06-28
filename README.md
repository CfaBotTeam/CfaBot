# CfaBot

Le bot possède plusieurs options de lancement:

--model: Chemin vers le répertoire qui contient le modèle spacy avec les vecteurs de mot
--dataset: Chemin vers le fichier XML qui contient les problèmes du CFA que l'on souhaite traiter
--glossary: Chemin vers le fichier JSON qui contient le dictionnaire des termes techniques et définitions associées
--provider-mode: Mode de récupération des définitions. Spécifier 'gloss-only'

Les gros fichiers de modèle n'ont pas été déposés sur le repository car trop volumineux. Pour lancer le Bot avec les options par défaut, il suffit de lancer la commande:

python Scripts/main.py

Pour faire fonctionner le bot avec les options par défaut, il convient tout de même de télécharger le modèle spacy disponible à l'adresse suivante (il s'agit du modèle avec les vecteurs de mots dédiés à la finance):
https://www.dropbox.com/s/2qhy8dv32h5s4ce/cfa_spacy_mdl-investopedia_plus_cfa.zip?dl=0


Par ailleurs les modules suivants doivent être installés:
pip install pandas
pip install spacy
pip install python-levenshtein
pip install pexpect
pip install http://download.pytorch.org/whl/cu91/torch-0.4.0-cp36-cp36m-linux_x86_64.whl 
pip install torchvision
pip install spicy
pip install sklearn
