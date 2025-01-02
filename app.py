from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Linear Regression class
class LinearRegression:
    def __init__(self, learning_rate, no_of_iterations):
        self.learning_rate = learning_rate
        self.no_of_iterations = no_of_iterations

    def fit(self, X, Y):
        self.m, self.n = X.shape
        self.w = np.zeros(self.n)
        self.b = 0
        self.X = X
        self.Y = Y
        for _ in range(self.no_of_iterations):
            self.update_weights()

    def update_weights(self):
        Y_prediction = self.predict(self.X)
        dw = -(2 / self.m) * (self.X.T.dot(self.Y - Y_prediction))
        db = -(2 / self.m) * np.sum(self.Y - Y_prediction)
        self.w -= self.learning_rate * dw
        self.b -= self.learning_rate * db

    def predict(self, X):
        return np.dot(X, self.w) + self.b


# Load and preprocess the dataset
data = pd.read_csv('insurance.csv')
data['sex'] = data['sex'].map({'male': 1, 'female': 0})
data['smoker'] = data['smoker'].map({'yes': 1, 'no': 0})
data = data.drop(columns=['region'])
X = data[['age', 'sex', 'bmi', 'children', 'smoker']].values
y = data['charges'].values

# Scale the data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train the model
model = LinearRegression(learning_rate=0.01, no_of_iterations=1000)
model.fit(X, y)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        data = request.json
        age = int(data.get('age'))
        sex = 1 if data.get('sex') == 'male' else 0
        bmi = float(data.get('bmi'))
        children = int(data.get('children'))
        smoker = 1 if data.get('smoker') == 'yes' else 0

        # Preprocess input (scale and reshape)
        input_data = np.array([[age, sex, bmi, children, smoker]])
        input_data = scaler.transform(input_data)

        # Predict charges
        prediction = model.predict(input_data)[0]

        # Ensure no negative predictions
        prediction = max(0, prediction)

        return jsonify({"prediction": round(prediction, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
