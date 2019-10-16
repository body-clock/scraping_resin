import pandas as pd

df = pd.read_csv("new_york_state.csv")
df_clean = df.drop_duplicates(subset=['name'])
df_sorted = df_clean.sort_values(by="type_of_listing")
df_sorted.to_csv("ny_state_clean.csv")
