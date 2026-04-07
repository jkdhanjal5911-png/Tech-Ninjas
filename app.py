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