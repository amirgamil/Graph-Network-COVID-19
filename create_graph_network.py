import pandas as pd
import numpy as np
import os
import itertools
import json


with open("data.json") as f:
    data = json.load(f)
print(data)
