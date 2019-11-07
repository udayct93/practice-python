from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from sqlalchemy import ForeignKey

app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:rocky@1234@localhost:5432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
    __tablename__ ='user'
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email=db.Column(db.String)

class Products(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, ForeignKey('user.uid'))
    product_name = db.Column(db.String)
    product_type = db.Column(db.String)
    price = db.Column(db.String)


# class productSchema(ma.Schema):
    # class Meta:
        # fields = ('pid','uid','product_name','product_type','price')

class productSchema(ma.Schema):
        class Meta:
          fields = ('uid', 'first_name', 'last_name', 'email')

product_schema=productSchema(strict=True)
products_schemas=productSchema(many=True,strict=True)
# products_schem=productSchemad(many=True,strict=True)


#get all products
@app.route('/')
def home():
    return '<h1> user and prosuct details</h1>'
@app.route('/user/<parmid>', methods=['GET'])
def get_products(parmid):
        user_product = User.query.filter_by(uid=parmid).first()
        x = Products.query.filter_by(uid=user_product.uid).all()
        # print(x[0].__dict__)
        # print(x[1].__dict__)































# @app.route('/user/<parmid>', methods=['GET'])
# def get_products(parmid):
#         user_list = {}
#         dest={}
#         dest2 = {}
#         user_product = User.query.filter_by(uid=parmid).first()
#         x = user_product.uid
#         user_products = Products.query.filter_by(uid=x).all()
#         print(user_products)
#         for usr_prd in user_products:
#             product_dict = {
#             "pid": usr_prd.pid,
#             "price": usr_prd.price,
#             "product_name": usr_prd.product_name,
#             "product_type": usr_prd.product_type,
#             }
#             dest.update(product_dict)
#         print(dest)
#         user_dict = {
#         "uid": user_product.uid,
#         "first_name": user_product.first_name,
#         "last_name": user_product.last_name,
#         "email": user_product.email,
#         "product": dest
#         }
#
#         user_list.update(user_dict)
#         return jsonify(user_list)
#         # print(user_list)






#get one product
# @app.route('/product/<parmid>',methods=['GET'])
# def get_product(parmid):
#     product_list = []
#     user = User.query.filter_by(uid=parmid).first()
#     all_products = Products.query.filter_by(uid=user.uid)
#
#     for product in all_products:
#         product_dict = {
#             "pid": product.pid,
#             "price": product.price,
#             "product_name": product.product_name,
#             "product_type": product.product_type,
#             "uid": user.uid,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email
#         }
#         product_list.append(product_dict)
#     return jsonify(product_list)

# @app.route('/user',methods=['GET'])
# def get_users():
#     all_products=User.query.all()
#     results=product_schema.dump(all_products)
#     return jsonify(results.data)
#

if __name__ =='__main__':
    app.run(debug=True)

#
# {
#     "email": "siddesh@gmail.com",
#     "first_name": "siddesh",
#     "last_name": "T",
#     "product" : { "1" : {
#         "price": "2000",
#         "product_name": "headphone",
#         "product_type": "R",
#     },
#         "2" : {
#             "price": "2000",
#     "product_name": "display",
#     "product_type": "T",
#         }
#     }
#
# #   }
#
#
# class Product:
#
#     def __init__(self):
#         self.name = None
#         self.info = None
#
# class User:
#
#     def __init__(self):
#         self.name = None
#         self.email = None
#         self.product = Product()
#
#
# print(User().__dict__)