from flask import Flask, request, jsonify, render_template
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

