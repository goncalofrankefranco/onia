import pandas as pd

# Series: 1 Dimensional Labeled Array that can hold any data type
dataSeries = [100, 200, 300, 401, 503]
dataLabels = ["A", "B", "C", "D", "E"]

series = pd.Series(dataSeries, index=dataLabels)
seriesLabels = pd.Series(dataLabels)
"""
print(series)
print(series.loc["A"])
print(series.iloc[2])
print(series[series > 300])
"""

# Series Dictionaries - Uses dictionary labels as labels

# DataFrame: 2 Dimensional Data Structure

DataDataFrame = {
    "Name": ["Spongebob", "Patrick", "Squidward"],
    "Age": [30, 35, 50]
}

df = pd.DataFrame(DataDataFrame, index = ["Employee #1", "Employee #2", "Employee #3"])

print(df)

# New column:
df["Job"] = ["Cook", "N/A", "Cashier"]

# New row:
new_row_indexed = pd.DataFrame([{"Name": "Sandy", "Age": 28, "Job": "Engineer"}], index = ["Employee #4"])
df = pd.concat([df, new_row_indexed])
"""
print(df)
"""

# Importing:
dfI = pd.read_csv("Data/pokemon.csv")
#dfIjson = pd.read_json("Data/pokemon.json")
"""
print(dfI)
print(dfI.to_string()) #All text
"""

# Selection:
# BY COLUMN:
"""
print(dfI[["Name", "Type 1"]].to_string())
"""

# BY ROW:
dfIrow = pd.read_csv("Data/pokemon.csv", index_col = "Name")
"""
print(dfIrow.loc["Pikachu"])
print(dfIrow.loc[["Charizard", "Mewtwo"], ["Attack", "Defense"]])
print(dfIrow.iloc[0:11, 0:3].to_string())

while True:
    pokemon = input("Enter Pokemon Name: ")
    try:
        print(dfIrow.loc[pokemon])
    except KeyError:
        print("Pokemon not in List")
"""

# Filtering: keeping the rows that meet a certain condition

strong_pokemon = dfIrow[(dfIrow["Attack"] > 100) | (dfIrow["Defense"] > 100)]
tuff_pokemon = dfIrow[dfIrow["Defense"] > 100]
#print(strong_pokemon.to_string())

# Aggregate Functions: used to summarize and analyse data
"""
print(dfI["Attack"].mean())
print(dfI.mean(numeric_only=True))
"""
# Types of funtions: Mean, Sum, Min, Max, Count

# Groups:
group = dfI.groupby("Type 1")
"""
#print(group) #Doesn't work
print(group["#"].count()) #Works
#print(group["Attack"].mean())
"""

# Data Cleaning:
# 1. DROP IRRELEVANT COLUMNS:
newdfIrow = dfIrow.drop(columns=["Legendary", "#"])
#print(newdfIrow)

# 2. HANDLE MISSING DATA:
filteredDfIrow = dfIrow.dropna(subset=["Type 2"])
filledDfIrow = dfIrow.fillna({
    "Type 2": "None"
})
#print(filteredDfIrow)

# 3. FIX INCONSISTENT VALUES:
fixedDfIrow = dfIrow
fixedDfIrow["Legendary"] = fixedDfIrow["Legendary"].replace({
    False: "No",
    True: "Yes"
})
#print(fixedDfIrow)

# 4. FIX DATA TYPES:
dataFixedDfIrow = dfIrow
dataFixedDfIrow["Legendary"] = fixedDfIrow["Legendary"].astype(bool)

# 5. REMOVE DUPLICATES:
dfIrow = dfIrow.drop_duplicates()
