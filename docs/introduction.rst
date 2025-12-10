StreamOptions – Présentation
============================

Objectif du projet
------------------

``StreamOptions`` est une application Streamlit permettant de **pricer des options
européennes** à partir de données de marché réelles :

* chargement de séries historiques via **Yahoo Finance** (`yfinance`),
* estimation d'un **prix spot** et d'une **volatilité annuelle**,
* calcul du prix de l’option et des Greeks via la **formule fermée de Black–Scholes**,
* estimation du prix par **simulation Monte Carlo**,
* comparaison avec un **modèle binomial**.

L’idée est de fournir un outil pédagogique, interactif et reproductible pour voir
comment les méthodes de pricing réagissent quand on change le sous-jacent, la
volatilité, la maturité ou le strike.


Architecture générale
---------------------

L’arborescence du projet est la suivante :

.. code-block:: text

   stream_options/
   ├─ Home.py                 # Page d’accueil Streamlit (point d’entrée)
   ├─ requirements.txt        # Dépendances du projet
   ├─ LICENSE                 # Licence
   │
   ├─ core/                   # Cœur métier (logique Python)
   │  ├─ pricing.py           # Monte Carlo + Black-Scholes + classe OptionPricer
   │  └─ data_io.py           # Récupération des données Yahoo + calcul S0 & volatilité
   │
   ├─ pages/                  # Pages Streamlit
   │  ├─ 01_Monte_Carlo.py    # Interface Monte Carlo (trajectoires, convergence, etc.)
   │  ├─ 02_Black_Scholes.py  # Interface Black-Scholes (prix + Greeks)
   │  └─ 03_Binomial.py       # Interface modèle binomial
   │
   ├─ tests/                  # Tests unitaires (pytest)
   │  ├─ test_pricing.py          # Test Black-Scholes + Monte Carlo (core.pricing)
   │  ├─ test_monte_carlo.py      # Tests dédiés à la partie simulation
   │  ├─ test_black_scholes.py    # Tests sur la cohérence des prix BS
   │  └─ test_binomial_model.py   # Tests sur le modèle binomial
   │
   ├─ Bases de données/
   │  └─ yf_data/             # Données Yahoo Finance
   │     ├─ name_tickers.csv  # Liste de tickers + noms lisibles
   │     └─ *.csv             # Historiques téléchargés (AAPL_2020-2025, etc.)
   │
   ├─ utils/
   │  └─ plotting.py          # Fonctions graphiques (ex : hero_home pour la page Home)
   │
   ├─ docs/                   # Documentation Sphinx
   │  ├─ conf.py              # Configuration Sphinx
   │  ├─ index.rst            # Page d’accueil de la doc
   │  ├─ introduction.rst     # Ce fichier : présentation du projet
   │  └─ api_reference.rst    # Référence de l’API Python (automodule)
   │
   ├─ roadmap/                # Notes de conception
   │  ├─ README.md            # Idées, TODO, vision du projet
   │  └─ pictures/            # Schémas, Gantt, logo, etc.
   │
   └─ slides/                 # Support de soutenance
      └─ presentation.tex / pdf


Organisation du code
--------------------

Le code est structuré autour de plusieurs sous-modules.

``core.pricing``
~~~~~~~~~~~~~~~~

Module contenant toute la **logique de pricing**.

Fonctions principales :

* :func:`core.pricing.simulate_gbm_paths`  
  Simule des trajectoires de Mouvement Brownien Géométrique (modèle de
  Black–Scholes) à partir d’un prix initial, d’un taux sans risque, d’une
  volatilité, d’une maturité, d’un nombre de pas et d’un nombre de simulations.

* :func:`core.pricing.price_european_option_mc`  
  Utilise les trajectoires simulées pour estimer par **Monte Carlo** le prix
  d’une option européenne (Call ou Put), ainsi que l’écart-type de l’estimateur.

* :class:`core.pricing.OptionPricer`  
  Implémente la **formule fermée de Black–Scholes** et calcule les Greeks
  (delta, gamma, vega, theta, rho). La classe valide les paramètres en amont
  et expose une méthode :py:meth:`OptionPricer.black_scholes` qui renvoie un
  dictionnaire prêt à être utilisé dans l’interface Streamlit.

``core.data_io``
~~~~~~~~~~~~~~~~

Module dédié aux **données de marché**.

* :func:`core.data_io.download_history_yahoo`  
  Télécharge l’historique de prix quotidiens pour un ticker donné entre deux
  dates, via l’API ``yfinance``. Les données sont sauvées dans
  ``Bases de données/yf_data`` pour permettre la reproductibilité.

* :func:`core.data_io.compute_spot_and_vol_from_history`  
  À partir d’un DataFrame de prix, calcule :

  * le **prix spot** ``S0`` (dernier prix),
  * la **volatilité annuelle historique**, à partir des rendements log quotidiens.

Ce module est le point d’entrée pour tout ce qui concerne les paramètres
de marché utilisés dans les pages Streamlit.

``pages`` – interfaces Streamlit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les scripts de ce dossier correspondent aux **trois pages principales** de
l’application :

* ``Home.py`` – page d’accueil, présentation rapide du projet et menu de
  navigation dans la barre latérale.

* ``01_Monte_Carlo.py`` – interface pour la méthode de **Monte Carlo** :

  * choix du ticker, de la période d’historique et du type d’option (Call/Put),
  * réglage du strike, de la maturité, du taux d’actualisation, du nombre
    de trajectoires, etc.,
  * visualisation de trajectoires simulées, de la distribution du prix à
    maturité, de la convergence de l’estimateur et du prix historique.

* ``02_Black_Scholes.py`` – interface pour la **formule de Black–Scholes** :

  * affichage du prix théorique,
  * calcul et visualisation des principaux Greeks,
  * comparaison possible avec le prix de marché (via l’historique).

* ``03_Binomial.py`` – interface pour le **modèle binomial** :

  * paramétrage du nombre de pas,
  * convergence du prix binomial vers la formule fermée,
  * visualisation de l’arbre de prix.

``tests``
~~~~~~~~~

Dossier regroupant les **tests unitaires** (framework ``pytest``) :

* ``test_pricing.py`` – vérifie que le prix Black–Scholes est correct
  pour un cas de référence et que la fonction Monte Carlo renvoie un prix
  positif avec des dimensions de trajectoires cohérentes.

* ``test_monte_carlo.py`` – tests plus détaillés sur la simulation :
  distributions plausibles, gestion des erreurs de paramètres, reproductibilité
  via la graine aléatoire, etc.

* ``test_black_scholes.py`` – tests de cohérence sur la formule fermée
  (par exemple : prix de Call ≥ 0, Call ≥ max(S0 – K e^{-rT}, 0), etc.).

* ``test_binomial_model.py`` – vérifie la stabilité et la convergence du
  modèle binomial.

``utils.plotting``
~~~~~~~~~~~~~~~~~~

Module utilitaire contenant des fonctions de **mise en forme graphique**.
Par exemple :

* ``hero_home`` : composant affiché sur la page d’accueil (logo, tagline,
  court texte de présentation).

D’autres fonctions peuvent être ajoutées ici pour factoriser le style des
graphiques (choix des couleurs, labels, titres, etc.).


Flux d’exécution typique
------------------------

En pratique, le pipeline est le suivant :

1. L’utilisateur choisit un **ticker** et une **période** dans l’interface
   Monte Carlo ou Black–Scholes.
2. La page appelle :func:`core.data_io.download_history_yahoo` pour récupérer
   l’historique de prix et :func:`core.data_io.compute_spot_and_vol_from_history`
   pour obtenir ``S0`` et la volatilité annuelle.
3. Selon la page :

   * Monte Carlo : appel à :func:`core.pricing.price_european_option_mc`.
   * Black–Scholes : création d’un :class:`core.pricing.OptionPricer` puis
     appel de :py:meth:`OptionPricer.black_scholes`.
   * Binomial : appel au modèle binomial (module dédié dans ``pages``).

4. Les résultats sont formatés et passés aux fonctions de **visualisation**
   (courbes de trajectoires, histogrammes, convergence, prix historique).

Ce découpage permet de séparer clairement **logique métier**, **accès
aux données** et **interface utilisateur**.


Utilisation rapide
------------------

1. Cloner le dépôt et installer les dépendances (dans un environnement virtuel) :

   .. code-block:: bash

      git clone https://github.com/<USER>/stream_options.git
      cd stream_options
      pip install -r requirements.txt

2. Lancer l’application Streamlit :

   .. code-block:: bash

      streamlit run Home.py

   L’interface se lance alors sur ``http://localhost:8501`` dans le navigateur.

3. Lancer les tests automatiques :

   .. code-block:: bash

      pytest

4. Re-générer la documentation Sphinx (HTML) :

   .. code-block:: bash

      cd docs
      python -m sphinx -b html . _build/html

   Ouvrir ensuite ``docs/_build/html/index.html`` dans un navigateur.


Tests, CI et qualité
--------------------

Les tests sont intégrés dans un **workflow GitHub Actions** qui :

* installe automatiquement les dépendances à partir de ``requirements.txt``,
* exécute ``pytest`` à chaque *push* sur la branche ``master``,
* signale les échecs directement dans l’interface GitHub.

L’objectif est de garantir que les principales briques (simulations,
formule de Black–Scholes, modèle binomial) restent stables et compatibles
entre elles au fur et à mesure de l’évolution du projet.


Évaluation temps / mémoire
--------------------------

Pour la méthode Monte Carlo, nous avons réalisé une courte évaluation
*temps / précision* :

* le temps de calcul croît linéairement avec le **nombre de trajectoires**,
* l’écart-type de l’estimateur décroît en :math:`1 / \sqrt{N}`,
  ce qui est confirmé empiriquement,
* pour un compromis raisonnable entre précision et temps de réponse dans
  Streamlit, nous utilisons typiquement de 5 000 à 20 000 trajectoires.

Ce type d’analyse justifie les valeurs par défaut proposées dans l’interface
et documente les limitations actuelles (par exemple sur des machines peu
puissantes).


Limitations et pistes d’amélioration
------------------------------------

Quelques pistes possibles pour la suite :

* intégrer d’autres modèles de volatilité (volatilité locale, stochastique),
* ajouter le pricing d’options exotiques (barrières, lookback, etc.),
* proposer davantage d’indicateurs de risque (VaR, CVaR),
* améliorer encore la gestion des erreurs utilisateur dans l’interface.
