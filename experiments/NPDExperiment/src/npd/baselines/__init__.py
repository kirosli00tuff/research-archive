"""The three registered baselines. Computed locally, free, on identical days."""

from npd.baselines.logistic import LOGISTIC, fit_logistic, rank_logistic
from npd.baselines.mom_12_1 import MOM_12_1, momentum_12_1, rank_mom_12_1
from npd.baselines.sign_last import SIGN_LAST, rank_sign_last

BASELINE_NAMES: tuple[str, ...] = (SIGN_LAST, MOM_12_1, LOGISTIC)

__all__ = [
    "BASELINE_NAMES",
    "LOGISTIC",
    "MOM_12_1",
    "SIGN_LAST",
    "fit_logistic",
    "momentum_12_1",
    "rank_logistic",
    "rank_mom_12_1",
    "rank_sign_last",
]
