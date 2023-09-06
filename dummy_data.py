import numpy as np
import pandas as pd

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

# cause, effect, time lag, effect size
effects = [
    ("Sleep", "Sleep", 2, 0.5),
    ("Sleep", "Sleep", 1, 0.2),
    ("Sleep", "Mood", 0, 0.3),
    ("Sport", "Sport", 2, 0.2),
    ("Sport", "Sport", 1, -0.5),
    ("Meditation", "Energy", 0, 0.5),
    ("Meditation", "Optimization_power", 0, 0.8),
    ("Energy", "Sport", 0, 1.2),
    ("Energy", "Mood", 0, 0.4),
    ("Mood", "Sport", 0, 0.2),
    ("Mood", "Social_interactions", 0, 0.2),
]

warmup = 1000
N = warmup + 150
data = np.random.standard_normal(size=(N, len(names)))
used_as_source = np.zeros((N, len(names)))


for i in range(2, N):
    for source, target, lag, size in effects:
        v = names.index(source)
        u = names.index(target)
        used_as_source[i - lag, v] = True
        assert not used_as_source[i, u]
        data[i, u] += data[i - lag, v] * size


df = add_lags(pd.DataFrame(data[warmup:], columns=names), 2)
df.to_csv("dummy_dataset.csv")
