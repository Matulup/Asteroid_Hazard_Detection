try:
    from pyswip import Prolog
    HAS_PYSWIP = True
except ImportError:
    HAS_PYSWIP = False


class KnowledgeBase:
    def __init__(self, kb_path: str):
        if not HAS_PYSWIP:
            raise ImportError(
                "pyswip non installato. Installa con: pip install pyswip"
            )
        self.prolog = Prolog()
        self.prolog.consult(kb_path)

    def get_reasons(self, row: dict, proba: float):
        q = (
            "reasons("
            f"{float(row['Absolute Magnitude'])}, "
            f"{float(row['Est Dia in KM(max)'])}, "
            f"{float(row['Relative Velocity km per sec'])}, "
            f"{float(row['Miss Dist.(Astronomical)'])}, "
            f"{float(row['Minimum Orbit Intersection'])}, "
            f"{float(row['Eccentricity'])}, "
            f"{int(row['Orbit Uncertainity'])}, "
            f"{float(row['Jupiter Tisserand Invariant'])}, "
            f"{float(proba)}, Reasons)."
        )
        res = list(self.prolog.query(q))
        return res[0]["Reasons"] if res else []

    def is_risky(self, row: dict, proba: float):
        q = (
            "risk_assess("
            f"{float(row['Absolute Magnitude'])}, "
            f"{float(row['Est Dia in KM(max)'])}, "
            f"{float(row['Relative Velocity km per sec'])}, "
            f"{float(row['Miss Dist.(Astronomical)'])}, "
            f"{float(row['Minimum Orbit Intersection'])}, "
            f"{float(row['Eccentricity'])}, "
            f"{int(row['Orbit Uncertainity'])}, "
            f"{float(row['Jupiter Tisserand Invariant'])}, "
            f"{float(proba)}, Reasons, ScoreRaw, ScoreNorm, Level)."
        )

        res = list(self.prolog.query(q))
        if res:
            reasons = res[0]["Reasons"]
            score_raw = int(res[0]["ScoreRaw"])
            score_norm = int(res[0]["ScoreNorm"])
            level = str(res[0]["Level"]).upper()
            if level == "HIGH":
                action = "MONITOR_PRIORITY"
            elif level == "MEDIUM":
                action = "REVIEW"
            else:
                action = "SAFE"

            return level, score_raw, score_norm, reasons, action

        return "LOW", 0, 0, [], "SAFE"
