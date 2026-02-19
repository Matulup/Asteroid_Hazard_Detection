from config.preprocessor import (
    build_clean_dataset, load_clean_dataset, prepare_train_test_raw
)
from models.classifiers import train_all_models
from knowledgeBase.kb import KnowledgeBase


if __name__ == "__main__":
    print(">>> Costruzione dataset CLEAN da RAW...")
    build_clean_dataset()

    print("\n>>> Caricamento dataset CLEAN per verifica...")
    df = load_clean_dataset()
    print("Shape dataset clean:", df.shape)
    print("\nDistribuzione Hazardous nel dataset:")
    print(df["Hazardous"].value_counts().to_string())
    print("\nDistribuzione Hazardous (percentuali):")
    print(df["Hazardous"].value_counts(normalize=True).to_string())

    X_train_raw, X_test_raw, y_train, y_test = prepare_train_test_raw(
        test_size=0.2,
        random_state=42
    )

    log_model, dt_model, rf_model, knn_model, mlp_model = train_all_models(
        X_train_raw=X_train_raw,
        y_train=y_train,
        X_test_raw=X_test_raw,
        y_test=y_test,
        random_state=42,
    )

    print("\n>>> Preparazione asteroidi di Test con Prolog...")
    probas = rf_model.predict_proba(X_test_raw)[:, 1]

    try:
        kb = KnowledgeBase("knowledgeBase/main.pl")

        print("\n=== Prolog (10 asteroidi di Test) ===")
        for i in range(10):
            row = X_test_raw.iloc[i].to_dict()
            p = float(probas[i])

            risk_level, score_raw, score_norm, reasons, action = kb.is_risky(row, p)

            reasons_str = ", ".join(reasons) if reasons else "(none)"
            print(
                f"\n[{i}] ML proba = {p:.4f} | Prolog = {risk_level} | "
                f"ScoreRaw = {score_raw} | Score = {score_norm}/100 | Action = {action}"
            )
            print(f"  Reasons: {reasons_str}")
    except Exception as e:
        print(f"\n[WARN] Prolog non disponibile: {e}")
        print("Installa pyswip e SWI-Prolog per il modulo Knowledge Base.")