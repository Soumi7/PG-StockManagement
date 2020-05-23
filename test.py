import pickle
from datetime import datetime , timedelta
import pandas as pd
import numpy as np

df=pd.read_csv("GROUP_OF_DATASETS/VEGETABLES.csv")

import matplotlib.pyplot as plt

plt.hist(np.log(df["quantity"]))

plt.show()

# print(df["quantity"].mean())
