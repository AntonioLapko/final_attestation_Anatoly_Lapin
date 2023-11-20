from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from catboost import CatBoostClassifier
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://alapin:1234@localhost:5432/final_attestation'

db = SQLAlchemy(app)

class Milk(db.Model):
    __tablename__ = 'milk'
    id = db.Column(db.Integer, primary_key=True)
    lot = db.Column(db.Integer, unique=True, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    ot = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.String(120), nullable=False)
    def json(self):
        return {'id': self.id, 'lot': self.lot, 'ph': self.ph, 'ot': self.ot, 'temperature': self.temperature, 'color': self.color,
                'quality': self.quality}

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/milk', methods=['POST'])
def create_milk():
  try:
    data = request.get_json()
    new_milk = Milk(lot=data['lot'], ph=data['ph'], ot=ph_to_t(data['ph']), temperature=data['temperature'], color=data['color'], quality=forecast_milk_grade(data['ph'], data['temperature'], data['color']))
    db.session.add(new_milk)
    db.session.commit()
    return make_response(jsonify({'message': 'milk created'}), 201)
  except:
    return make_response(jsonify({'message': 'error creating milk, lot already exist'}), 500)

@app.route('/milk', methods=['GET'])
def get_milks():
  try:
    milks = Milk.query.all()
    return make_response(jsonify([milk.json() for milk in milks]), 200)
  except:
    return make_response(jsonify({'message': 'error getting milk'}), 500)


@app.route('/milk/<int:lot>', methods=['GET'])
def get_milk(lot):
  try:
    milk = Milk.query.filter_by(lot=lot).first()
    if milk:
      return make_response(jsonify({'milk': milk.json()}), 200)
    return make_response(jsonify({'message': 'milk not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error getting milk'}), 500)


@app.route('/milk/<int:lot>', methods=['PUT'])
def update_milk(lot):
  try:
    milk = Milk.query.filter_by(lot=lot).first()
    if milk:
      data = request.get_json()
      milk.lot = data['lot']
      milk.ph = data['ph']
      milk.t = ph_to_t(data['ph'])
      milk.temperature = data['temperature']
      milk.color = data['color']
      milk.quality = forecast_milk_grade(data['ph'], data['temperature'], data['color'])
      db.session.commit()
      return make_response(jsonify({'message': 'milk updated'}), 200)
    return make_response(jsonify({'message': 'milk not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error updating milk'}), 500)


@app.route('/milk/<int:lot>', methods=['DELETE'])
def delete_milk(lot):
  try:
    milk = Milk.query.filter_by(lot=lot).first()
    if milk:
      db.session.delete(milk)
      db.session.commit()
      return make_response(jsonify({'message': 'milk deleted'}), 200)
    return make_response(jsonify({'message': 'milk not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error deleting milk'}), 500)

def forecast_milk_grade(ph:float, temperature:int, color:int):
    new_milk_grade = pd.DataFrame({'ph': [ph], 'temperature': [temperature], 'color': [color]})
    new_milk_grade['ph'] = new_milk_grade['ph'].astype('float')
    a=new_milk_grade.iloc[[0],[0]]
    b=a['ph'].squeeze()
    print(b)
    new_milk_grade['t'] = ph_to_t(b)
    model_milk_grade = CatBoostClassifier()
    model_milk_grade.load_model('model_milk_grade.cbm')
    forecast = model_milk_grade.predict(new_milk_grade)[0]
    if forecast == 0: result = "непригодное"
    if forecast == 1: result = "умеренное"
    if forecast == 2: result = "высокое"
    return result

def ph_to_t(b):
    t1 = (16, 17, 19, 20, 21, 22)
    if b < 6.4 or b > 6.8: c = t1[5]
    if b == 6.4: c = tq[4]
    if b == 6.5: c = t1[3]
    if b == 6.6: c = t1[2]
    if b == 6.7: c = t1[1]
    if b == 6.8: c = t1[0]
    return c

if __name__ == "__main__":
    app.run(debug=True)