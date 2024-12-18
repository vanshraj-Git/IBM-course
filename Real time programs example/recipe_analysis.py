import pandas as pd #type:ignore
import numpy as np #type:ignore
import re
import requests  # To fetch data from URL #type:ignore
import io

# 1. Load the dataset from URL into a pandas DataFrame
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0103EN-SkillsNetwork/labs/Module%202/recipes.csv'
response = requests.get(URL)
recipes = pd.read_csv(io.StringIO(response.text))
print('Data successfully read into dataframe!')

# 2. List all ingredient column names
ingredients = list(recipes.columns.values)

# 3. Search for specific ingredients (rice, wasabi, soy)
for keyword in ["rice", "wasabi", "soy"]:
    matches = [col for col in ingredients if re.search(f".*({keyword}).*", col, re.IGNORECASE)]
    print(f"Ingredients containing '{keyword}': {matches}")

# 4. Rename the first column to "cuisine"
recipes.columns.values[0] = "cuisine"

# 5. Convert all cuisine names to lowercase
recipes["cuisine"] = recipes["cuisine"].str.lower()

# 6. Standardize cuisine names (e.g., 'austria' -> 'austrian')
cuisine_mapping = {
    "austria": "austrian", "belgium": "belgian", "china": "chinese",
    "canada": "canadian", "netherlands": "dutch", "france": "french",
    "germany": "german", "india": "indian", "indonesia": "indonesian",
    "iran": "iranian", "italy": "italian", "japan": "japanese",
    "israel": "israeli", "korea": "korean", "lebanon": "lebanese",
    "malaysia": "malaysian", "mexico": "mexican", "pakistan": "pakistani",
    "philippines": "philippine", "scandinavia": "scandinavian",
    "spain": "spanish_portuguese", "portugal": "spanish_portuguese",
    "switzerland": "swiss", "thailand": "thai", "turkey": "turkish",
    "vietnam": "vietnamese", "uk-and-ireland": "uk-and-irish",
    "irish": "uk-and-irish"
}

for old, new in cuisine_mapping.items():
    recipes.loc[recipes["cuisine"] == old, "cuisine"] = new

# 7. Filter out cuisines with less than 50 occurrences
recipes_counts = recipes["cuisine"].value_counts()
cuisines_to_keep = recipes_counts[recipes_counts > 50].index
rows_before = recipes.shape[0]
recipes = recipes[recipes["cuisine"].isin(cuisines_to_keep)]
rows_after = recipes.shape[0]

print(f"{rows_before - rows_after} rows removed!")

# 8. Replace "Yes" with 1 and "No" with 0 in the ingredient columns
recipes.replace({"Yes": 1, "No": 0}, inplace=True)

# 9. Check for recipes with specific ingredients (rice, soy sauce, wasabi, seaweed)
required_columns = ["rice", "soy_sauce", "wasabi", "seaweed"]
if all(col in recipes.columns for col in required_columns):
    check_recipes = recipes[
        (recipes["rice"] == 1) &
        (recipes["soy_sauce"] == 1) &
        (recipes["wasabi"] == 1) &
        (recipes["seaweed"] == 1)
    ]
    print("Recipes with rice, soy sauce, wasabi, and seaweed:")
    print(check_recipes)
else:
    print("Some required columns are missing.")

# 10. Summarize the ingredient counts
ingredient_counts = recipes.iloc[:, 1:].sum()
ing_df = pd.DataFrame({"ingredient": ingredient_counts.index, "count": ingredient_counts.values})
ing_df.sort_values(by="count", ascending=False, inplace=True)
print("Ingredient counts:")
print(ing_df)

# 11. Group recipes by cuisine and compute the average ingredient usage
cuisines = recipes.groupby("cuisine").mean()

# 12. Define a function to print the top ingredients for each cuisine
def print_top_ingredients(row):
    print(row.name.upper())  # Print cuisine name in uppercase
    row_sorted = row.sort_values(ascending=False) * 100  # Sort ingredients by percentage
    top_ingredients = row_sorted.index[:4]  # Get top 4 ingredients
    top_percentages = row_sorted.values[:4]  # Get their corresponding percentages

    for ingredient, percentage in zip(top_ingredients, top_percentages):
        print(f"{ingredient} ({int(percentage)}%)", end=' ')
    print("\n")

# 13. Apply the function to print top ingredients for each cuisine
print("\nTop ingredients for each cuisine:")
cuisines.apply(print_top_ingredients, axis=1)


