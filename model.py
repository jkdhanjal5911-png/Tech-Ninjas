# import pandas as pd
# df =pd.read_csv('dataset.csv')
# def recommend(category,price):
#     price=int(price)
#     #Filter same category
#     filtered=df[df['category'] == category].copy()

#     #sort by closest price
#     filtered['diff']=abs(filtered['price'] - price)
#     result=filtered.sort_values(by='diff')
#     return result[['name','price']]
# print(recommend('electronics',500))



import pandas as pd

# Load dataset
df = pd.read_csv('dataset.csv')

# Ensure price column is numeric
df['price'] = df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

def recommend(category, price, top_n=5):
    try:
        # Convert price to number
        price = float(price)
    except ValueError:
        return "Error: Price must be a number."
    
    # Make category case-insensitive
    category = str(category).lower()
    
    # Check if category exists
    if category not in df['category'].str.lower().unique():
        return f"Error: Category '{category}' not found. Available categories: {list(df['category'].unique())}"
    
    # Filter products in the category
    filtered = df[df['category'].str.lower() == category].copy()
    
    # Compute difference from target price
    filtered['diff'] = abs(filtered['price']<= price)
    if filtered.empty:
        return "No product is available under the price in this category"
    # Sort by closest price
    result = filtered.sort_values(by='diff',ascending=False)
    
    # If no products found
    if result.empty:
        return "No products found in this category."
    
    return result[['name', 'price']]

#input 
user_category=input("Select the category: ")
user_price=input('Price: ')
print(recommend(user_category,user_price))