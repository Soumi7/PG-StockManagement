import pickle
from datetime import datetime , timedelta
import pandas as pd

loaded_model=pickle.load(open("Final_Mod.pkl","rb"))

print(type(loaded_model))