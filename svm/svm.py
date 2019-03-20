import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import stats
from sklearn.svm import SVC
import seaborn as sns
sns.set()

data = None
with open("../data/mock/chars/processed.json") as f:
    data = json.load(f)

X = []
Y = []

for p in data:
    if p["alive"] == -1 or p["dead"] == p["alive"]:
        continue

    cult = hash(p["culture"])
    tmp = ["isMale", "birth", "death", "alCount", "bookCount", "povCount"]
    x = [cult] + [p[foo] or 0 for foo in tmp]
    print(x)

    X.append(x)
    Y.append(p["alive"])

model = SVC(kernel='linear', C=1E10)
model.fit(X, Y)
