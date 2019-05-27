import pandas as pd

#Creating initial data
start_data = {'fruit': ["banana", "banana", "apple", "apple", "orange", "orange"],
              'certainty_level %': [57, 52, 48, 43, 88, 99]}

df = pd.DataFrame(start_data)

#Saving data
df.to_csv('fruit_database.csv', index=False)

#Reading data
df_csv = pd.read_csv('fruit_database')

#Create test data2
df2 = pd.DataFrame({'fruit': ["banana", "apple", "banana", "banana", "banana","pineapple", "pineapple", "pineapple", "pineapple", "pineapple"],
                    'certainty_level %': [88, 99, 1, 58, 95, 10, 20, 40, 90, 30]})

#Concat/appending
concat = pd.concat([df_csv, df2], sort=True, ignore_index=True)

#Saving after concat
concat.to_csv('fruit_database.csv', index=False)

print(concat)