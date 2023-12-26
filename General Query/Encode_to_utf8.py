# import pandas as pd

# # Read the CSV file (change 'file.csv' to your file name)
# data = pd.read_csv('General Query/amazon.csv')

# # Write the data back to a new CSV file with UTF-8 encoding
# data.to_csv('file_utf8.csv', index=False)

file_path = r'C:\Users\warda\OneDrive\Desktop\Master Model\General Query\amazon.csv'

with open(file_path, 'rb') as file:
    data = file.read()

# Print the problematic byte(s) causing the issue
problematic_bytes = [x for x in data if x >= 128]
print(problematic_bytes)
