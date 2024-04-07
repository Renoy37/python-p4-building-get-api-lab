#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries')
def bakeries():
    bakery_list = []
    
    for bakery in Bakery.query.all():
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at,
        }
        bakery_list.append(bakery_dict)
    
    return make_response(bakery_list)


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    
    if bakery is None:
        return make_response({'error': 'Bakery not found'}, 404)
    
    bakery_dict = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at,
        'updated_at': bakery.updated_at,
        'baked_goods': []
    }

    for baked_good in bakery.baked_goods:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at,
            'updated_at': baked_good.updated_at,
            'bakery_id': bakery.id
        }
        bakery_dict['baked_goods'].append(baked_good_data)

    return make_response(bakery_dict)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    baked_goods_list = []
    
    for baked_good in baked_goods:
        baked_good_dict = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at,
            'updated_at': baked_good.updated_at,
            'bakery': {
                'id': baked_good.bakery.id,
                'name': baked_good.bakery.name,
                'created_at': baked_good.bakery.created_at,
                'updated_at': baked_good.bakery.updated_at,
            }
        }
        baked_goods_list.append(baked_good_dict)
    
    return make_response(baked_goods_list)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if most_expensive is None:
        return jsonify({'error': 'No baked goods found'}), 404
    
    most_expensive_dict = {
        'id': most_expensive.id,
        'name': most_expensive.name,
        'price': most_expensive.price,
        'created_at': most_expensive.created_at,
        'updated_at': most_expensive.updated_at,
        'bakery': {
            'id': most_expensive.bakery.id,
            'name': most_expensive.bakery.name,
            'created_at': most_expensive.bakery.created_at,
            'updated_at': most_expensive.bakery.updated_at,
        }
    }
    
    return make_response(most_expensive_dict)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
