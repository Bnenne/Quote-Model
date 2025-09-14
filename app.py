from flask import Flask, jsonify, request
from src.predict import get_prediction
from sentence_transformers import SentenceTransformer
from keras.models import load_model

app = Flask(__name__)

encoding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
clf_model = load_model("src/quote_classifier_model_v1_1.keras")

@app.route('/predict')
def predict():
    print("Incoming request")
    message = request.headers.get('Message')

    prediction = get_prediction(message, encoding_model, clf_model)

    return jsonify(prediction), 200

if __name__ == "__main__":
    app.run(debug=True)