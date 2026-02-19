# Asteroid Hazard Detection

Sistema di classificazione automatica della pericolosità dei Near-Earth Objects (NEO) basato su tecniche di Machine Learning supervisionato e ragionamento logico con Prolog.

## Struttura del progetto

```
Asteroid_Hazard_Detection/
├── config/
│   └── preprocessor.py        # Preprocessing, feature engineering, train/test split
├── data/
│   ├── dataset.py             # Classe Dataset per caricamento CSV
│   ├── raw/
│   │   └── nasa.csv           # Dataset originale NASA (4687 NEO, 40 feature)
│   └── processed/
│       └── nasa_clean.csv     # Dataset pulito (17 feature selezionate)
├── models/
│   └── classifiers.py         # Training 5 modelli con GridSearchCV/RandomizedSearchCV 10-fold CV
├── knowledgeBase/
│   ├── rules.pl               # Regole Prolog (trigger singoli, composti, pesi, score)
│   ├── main.pl                # Entry point Prolog
│   └── kb.py                  # Interfaccia Python-Prolog
├── docs/                      # Documentazione
├── main.py                    # Pipeline principale
├── requirements.txt
└── README.md
```

## Modelli addestrati

| Modello             | Accuracy       | Precision      | Recall         | F1-score       | ROC AUC        |
|---------------------|----------------|----------------|----------------|----------------|----------------|
| Logistic Regression | 0.9339 ± 0.0173| 0.7306 ± 0.0536| 0.9338 ± 0.0596| 0.8198 ± 0.0420| 0.9892 ± 0.0061|
| Decision Tree       | 0.9957 ± 0.0071| 0.9804 ± 0.0293| 0.9934 ± 0.0200| 0.9868 ± 0.0219| 0.9987 ± 0.0027|
| **Random Forest**   | 0.9989 ± 0.0032| 0.9934 ± 0.0187| 1.0000 ± 0.0000| 0.9967 ± 0.0097| 1.0000 ± 0.0003|
| KNN                 | 0.8838 ± 0.0269| 0.5897 ± 0.0655| 0.9139 ± 0.0602| 0.7169 ± 0.0529| 0.9532 ± 0.0214|
| MLP                 | 0.9904 ± 0.0100| 0.9671 ± 0.0420| 0.9735 ± 0.0327| 0.9703 ± 0.0307| 0.9994 ± 0.0013|

Il miglior modello è il **Random Forest** con F1-score = 0.9967.

## Knowledge Base (Prolog)

Il modulo Prolog integra la probabilità ML con regole esperte di dominio astronomico:
- **Trigger singoli**: magnitudine assoluta, diametro, MOID, miss distance, velocità, eccentricità, incertezza orbitale
- **Trigger composti**: asteroide grande + vicino, grande + veloce, MOID basso + orbita incerta, approccio ravvicinato + alta velocità
- **Score pesato**: ogni trigger ha un peso; lo score totale determina il livello di rischio (LOW / MEDIUM / HIGH)

## Esecuzione

```bash
pip install -r requirements.txt
python main.py
```

**Requisiti aggiuntivi**: SWI-Prolog installato nel sistema per il modulo Knowledge Base.
