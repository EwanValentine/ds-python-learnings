import numpy as np
import pandas as pd

data = np.array([['', 'Name', 'Age'],
                 ['1', 'Ewan Valentine', '29'],
                 ['2', 'Someone Else', '29'],
                 ['3', 'Some Old-Cunt', '64']])

df = pd.DataFrame(data=data[1:,1:],
                  index=data[1:,0],
                  columns=data[0, 1:])

print(df)
