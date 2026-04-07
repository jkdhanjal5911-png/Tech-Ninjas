# from flask import Flask, render_template,request,jsonify
# from model import recommend

# app=Flask(__name__)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/get_recommendations', methods=['POST'])
# def get_recommendations():
#     data=request.json
#     category = data['category']
#     price=data['price']

#     results=recommend(category,price)
#     return jsonify(results)
# if __name__=='__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Sample data (replace with your real dataset)
# products = [
#     {"name": "Laptop", "category": "Electronics", "price": 50000},
#     {"name": "Phone", "category": "Electronics", "price": 20000},
#     {"name": "Shirt", "category": "Clothes", "price": 800},
#     {"name": "Jeans", "category": "Clothes", "price": 1200}
# ]

# @app.route("/", methods=["GET", "POST"])
# def home():
#     results = []
#     if request.method == "POST":
#         category = request.form.get("category")
#         if category:
#             # Filter products by category
#             results = [p for p in products if p["category"] == category]
#     return render_template("index.html", results=results)

# if __name__ == "__main__":
#     app.run(debug=True)
# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # Your products (can be from CSV too)
# products = [
#     {"name":"Redmi Note 12","category":"Electronics","price":15000,"rating":4.3,"image":"img/1.jpeg"},
#     {"name":"Samsung Galaxy M34","category":"Electronics","price":18000,"rating":4.4,"image":"https://source.unsplash.com/400x300/?smartphone"},
#     {"name":"Men T-Shirt","category":"Clothing","price":500,"rating":4.1,"image":"https://source.unsplash.com/400x300/?tshirt"},
#     {"name":"Nike Shoes","category":"Footwear","price":3500,"rating":4.6,"image":"https://source.unsplash.com/400x300/?shoes"},
#     # Add all other products here...
# ]

# @app.route("/")
# def home():
#     return render_template("index.html")

# # Endpoint to get products (can filter by category)
# @app.route("/get_products", methods=["POST"])
# def get_products():
#     data = request.get_json()
#     cat = data.get("category")
#     search = data.get("search", "").lower()
#     filtered = products

#     if cat and cat != "All":
#         filtered = [p for p in filtered if p["category"] == cat]

#     if search:
#         filtered = [p for p in filtered if search in p["name"].lower()]

#     return jsonify(filtered)

# # Recommendation endpoint
# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.get_json()
#     product_name = data.get("productName")
#     selected = next((p for p in products if p["name"] == product_name), None)
#     if not selected:
#         return jsonify([])

#     recommended = [
#         {**p, "score": 2 + (1 if abs(p["price"] - selected["price"]) < 2000 else 0) + (1 if abs(p["rating"] - selected["rating"]) < 0.5 else 0)}
#         for p in products
#     ]
#     recommended = sorted(recommended, key=lambda x: x["score"], reverse=True)
#     recommended = [p for p in recommended if p["name"] != product_name][:4]
#     return jsonify(recommended)

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
from model import recommend, filter_products, get_all_products
import traceback

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_products", methods=["POST"])
def get_products():
    try:
        data = request.get_json()
        print(f"📥 Received request: {data}")  # Debug log
        
        category = data.get("category", "All")
        search = data.get("search", "")
        min_price = data.get("min_price")
        max_price = data.get("max_price")
        
        products = filter_products(category, search, min_price, max_price)
        print(f"📤 Returning {len(products) if not isinstance(products, dict) else 0} products")  # Debug log
        
        return jsonify(products)
    except Exception as e:
        print(f"❌ Error in get_products: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)})

@app.route("/recommend", methods=["POST"])
def recommend_route():
    try:
        data = request.get_json()
        print(f"🤖 Recommendation request for: {data.get('productName')}")  # Debug log
        
        product_name = data.get("productName")
        recs = recommend(product_name)
        
        return jsonify(recs)
    except Exception as e:
        print(f"❌ Error in recommend: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)})

@app.route("/all_products", methods=["GET"])
def all_products():
    try:
        products = get_all_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True, port=5000)