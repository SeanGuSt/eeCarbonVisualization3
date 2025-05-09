import pandas as pd
merge_on = "Pedon ID"
suffix = "_x"
d = {'Pedon ID' : [1, 2, 3, 4, 5], 'Pedon': ["S1999NY", "S1950ND", "54ND01", "S1953ND", "S1950ND02"]}
b = {'Bottom': [0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6], 'Pedon ID': [0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6],  'Layer': ["xbox" for _ in range(len([0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]))], 'Top': [0, 0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]}
df1 = pd.DataFrame(data = d)
df2 = pd.DataFrame(data = b)
df_merge = df1.merge(df2, on = merge_on, suffixes=[suffix, None])
print(df1)
print(df2)
print(df_merge)