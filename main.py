from flask import Flask, request, jsonify
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)
