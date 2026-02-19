:- use_module(library(lists)).

large_asteroid(AbsMag) :- AbsMag =< 22.0.
very_large_asteroid(AbsMag) :- AbsMag =< 20.0.

significant_diameter(DiaMax) :- DiaMax >= 0.15.

close_moid(MOID) :- MOID =< 0.05.
very_close_moid(MOID) :- MOID =< 0.01.

close_approach(MissDist) :- MissDist =< 0.1.
very_close_approach(MissDist) :- MissDist =< 0.02.

high_velocity(Vel) :- Vel >= 20.0.
very_high_velocity(Vel) :- Vel >= 35.0.

high_eccentricity(Ecc) :- Ecc >= 0.6.

uncertain_orbit(OrbUnc) :- OrbUnc >= 5.

ml_high(P) :- P >= 0.55.
ml_very_high(P) :- P >= 0.80.


trigger(large_asteroid, AbsMag, _, _, _, _, _, _, _, _) :-
    large_asteroid(AbsMag).

trigger(very_large_asteroid, AbsMag, _, _, _, _, _, _, _, _) :-
    very_large_asteroid(AbsMag).

trigger(significant_diameter, _, DiaMax, _, _, _, _, _, _, _) :-
    significant_diameter(DiaMax).

trigger(close_moid, _, _, _, _, MOID, _, _, _, _) :-
    close_moid(MOID).

trigger(very_close_moid, _, _, _, _, MOID, _, _, _, _) :-
    very_close_moid(MOID).

trigger(close_approach, _, _, _, MissDist, _, _, _, _, _) :-
    close_approach(MissDist).

trigger(very_close_approach, _, _, _, MissDist, _, _, _, _, _) :-
    very_close_approach(MissDist).

trigger(high_velocity, _, _, Vel, _, _, _, _, _, _) :-
    high_velocity(Vel).

trigger(very_high_velocity, _, _, Vel, _, _, _, _, _, _) :-
    very_high_velocity(Vel).

trigger(high_eccentricity, _, _, _, _, _, Ecc, _, _, _) :-
    high_eccentricity(Ecc).

trigger(uncertain_orbit, _, _, _, _, _, _, OrbUnc, _, _) :-
    uncertain_orbit(OrbUnc).

trigger(ml_high, _, _, _, _, _, _, _, _, Proba) :-
    ml_high(Proba).

trigger(ml_very_high, _, _, _, _, _, _, _, _, Proba) :-
    ml_very_high(Proba).



trigger(large_and_close, AbsMag, _, _, MissDist, _, _, _, _, _) :-
    large_asteroid(AbsMag),
    close_approach(MissDist).

trigger(large_and_fast, AbsMag, _, Vel, _, _, _, _, _, _) :-
    large_asteroid(AbsMag),
    high_velocity(Vel).

trigger(close_moid_uncertain, _, _, _, _, MOID, _, OrbUnc, _, _) :-
    close_moid(MOID),
    uncertain_orbit(OrbUnc).

trigger(close_fast_approach, _, _, Vel, MissDist, _, _, _, _, _) :-
    close_approach(MissDist),
    high_velocity(Vel).

trigger(large_eccentric, _, DiaMax, _, _, _, Ecc, _, _, _) :-
    significant_diameter(DiaMax),
    high_eccentricity(Ecc).



reasons(AbsMag, DiaMax, Vel, MissDist, MOID, Ecc, OrbUnc, TJ, Proba, Reasons) :-
    findall(R,
        trigger(R, AbsMag, DiaMax, Vel, MissDist, MOID, Ecc, OrbUnc, TJ, Proba),
        Reasons).



reason_weight(very_large_asteroid, 4).
reason_weight(very_close_moid, 4).
reason_weight(very_close_approach, 4).
reason_weight(very_high_velocity, 3).

reason_weight(large_asteroid, 3).
reason_weight(close_moid, 3).
reason_weight(close_approach, 3).

reason_weight(significant_diameter, 2).
reason_weight(high_velocity, 2).
reason_weight(high_eccentricity, 2).
reason_weight(uncertain_orbit, 2).

reason_weight(ml_high, 1).
reason_weight(ml_very_high, 2).

reason_weight(large_and_close, 3).
reason_weight(large_and_fast, 3).
reason_weight(close_moid_uncertain, 3).
reason_weight(close_fast_approach, 3).
reason_weight(large_eccentric, 2).

reason_weight(_, 1).



risk_score(Reasons, ScoreRaw) :-
    findall(W,
        ( member(R, Reasons),
          reason_weight(R, W)
        ),
        Ws),
    sum_list(Ws, ScoreRaw).

risk_level_from_score(ScoreRaw, high)   :- ScoreRaw >= 15, !.
risk_level_from_score(ScoreRaw, medium) :- ScoreRaw >= 7,  !.
risk_level_from_score(_, low).

max_risk_score(30).

cap_100(X, 100) :- X > 100, !.
cap_100(X, X).

risk_score_norm(ScoreRaw, ScoreNorm) :-
    max_risk_score(Max),
    Max > 0,
    Tmp is round(100 * ScoreRaw / Max),
    cap_100(Tmp, ScoreNorm).



risk_assess(AbsMag, DiaMax, Vel, MissDist, MOID, Ecc, OrbUnc, TJ, Proba,
            Reasons, ScoreRaw, ScoreNorm, Level) :-
    reasons(AbsMag, DiaMax, Vel, MissDist, MOID, Ecc, OrbUnc, TJ, Proba, Reasons),
    risk_score(Reasons, ScoreRaw),
    risk_score_norm(ScoreRaw, ScoreNorm),
    risk_level_from_score(ScoreRaw, Level).
