from flask import Flask, render_template,request,jsonify
from model import recommend

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data=request.json
    category = data['category']
    price=data['price']

    results=recommend(category,price)
    return jsonify(results)
if __name__=='__main__':
    app.run(debug=True)
