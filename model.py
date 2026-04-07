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



# model.py
# model.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv('dataset.csv')

# Ensure all required columns exist
required_columns = ['name', 'category', 'price', 'rating', 'image', 'description', 'stock', 'brand']
for col in required_columns:
    if col not in df.columns:
        if col == 'description':
            df[col] = 'No description available'
        elif col == 'stock':
            df[col] = 10
        elif col == 'brand':
            df[col] = 'Generic'
        elif col == 'image':
            # Add placeholder images based on category
            image_map = {
                'Electronics': 'https://cdn-icons-png.flaticon.com/512/3659/3659898.png',
                'Clothing': 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png',
                'Footwear': 'https://cdn-icons-png.flaticon.com/512/2589/2589189.png',
                'Furniture': 'https://cdn-icons-png.flaticon.com/512/1956/1956180.png',
                'Books': 'https://cdn-icons-png.flaticon.com/512/1341/1341148.png'
            }
            df[col] = df['category'].map(image_map).fillna('https://cdn-icons-png.flaticon.com/512/1995/1995572.png')

# Prepare features for ML
# One-hot encode categories
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_cat = encoder.fit_transform(df[['category']])

# Normalize price and rating
scaler = MinMaxScaler()
price_rating_scaled = scaler.fit_transform(df[['price', 'rating']])

# Combine features (category + price + rating)
features = np.hstack([encoded_cat, price_rating_scaled])

print(f"✅ Model initialized with {len(df)} products")
print(f"📊 Categories: {', '.join(df['category'].unique())}")
print(f"📁 Features shape: {features.shape}")

def recommend(product_name, top_n=4):
    """
    Recommend similar products using cosine similarity
    """
    try:
        if product_name not in df['name'].values:
            return {"error": f"Product '{product_name}' not found"}

        # Get product index
        idx = df[df['name'] == product_name].index[0]
        
        # Calculate similarity scores
        similarities = cosine_similarity([features[idx]], features)[0]
        
        # Get top N similar products (excluding itself)
        similar_indices = similarities.argsort()[::-1][1:top_n+1]
        
        recommendations = []
        for i in similar_indices:
            product = df.iloc[i]
            recommendations.append({
                'name': product['name'],
                'category': product['category'],
                'price': int(product['price']),
                'rating': float(product['rating']),
                'image': product['image'],
                'description': product['description'],
                'stock': int(product['stock']),
                'brand': product['brand'],
                'similarity_score': float(similarities[i])
            })
        
        return recommendations
    
    except Exception as e:
        return {"error": str(e)}

def filter_products(category="All", search="", min_price=None, max_price=None, sort_by=None):
    """
    Filter products with various criteria
    """
    try:
        filtered = df.copy()
        
        # Filter by category
        if category != "All":
            filtered = filtered[filtered['category'] == category]
        
        # Filter by search
        if search and search.strip():
            filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
        
        # Filter by price
        if min_price and min_price > 0:
            filtered = filtered[filtered['price'] >= float(min_price)]
        if max_price and max_price > 0:
            filtered = filtered[filtered['price'] <= float(max_price)]
        
        # Sort by
        if sort_by == 'price_asc':
            filtered = filtered.sort_values('price', ascending=True)
        elif sort_by == 'price_desc':
            filtered = filtered.sort_values('price', ascending=False)
        elif sort_by == 'rating':
            filtered = filtered.sort_values('rating', ascending=False)
        
        # Return products with full details
        return filtered[['name', 'category', 'price', 'rating', 'image', 'description', 'stock', 'brand']].to_dict(orient='records')
    
    except Exception as e:
        return {"error": str(e)}

def get_all_products():
    """
    Get all products with full details
    """
    try:
        return df[['name', 'category', 'price', 'rating', 'image', 'description', 'stock', 'brand']].to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}

def get_product_details(product_name):
    """
    Get detailed information about a specific product
    """
    try:
        product = df[df['name'] == product_name].iloc[0]
        return {
            'name': product['name'],
            'category': product['category'],
            'price': int(product['price']),
            'rating': float(product['rating']),
            'image': product['image'],
            'description': product['description'],
            'stock': int(product['stock']),
            'brand': product['brand']
        }
    except:
        return None

def get_categories():
    """
    Get all unique categories
    """
    try:
        return df['category'].unique().tolist()
    except:
        return []

def get_price_range():
    """
    Get min and max price from dataset
    """
    try:
        return {
            'min': int(df['price'].min()),
            'max': int(df['price'].max())
        }
    except:
        return {'min': 0, 'max': 100000}