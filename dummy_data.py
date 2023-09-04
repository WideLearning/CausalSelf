import pandas as pd
import numpy as np
from parse import add_lags

names = [
    "Mood",
    "Energy",
    "Deep_work",
    "Stoicism",
    "Optimization_power",
    "Sleep",
    "Meditation",
    "Sport",
    "Social_interactions",
]

effects = [
    ("Sleep", "Mood", 0.3),
    ("Meditation", "Energy", 0.5),
    ("Meditation", "Optimization_power", 0.8),
    ("Energy", "Sport", 1.2),
    ("Energy", "Mood", 0.1),
    ("Mood", "Social_interactions", 0.2),
]

N = 140
data = np.random.standard_normal(size=(N, len(names)))
used_as_source : set[str] = set()

for source, target, impact in effects:
    used_as_source.add(source)
    assert target not in used_as_source
    data[:, names.index(target)] += data[:, names.index(source)] * impact

df = add_lags(pd.DataFrame(data, columns=names), 0)
df.to_csv("dummy.csv")