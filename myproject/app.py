import flask
from models import *
from sqlalchemy import select
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://anu:1234@localhost:5432/flaskdb"
# initialize the app with the extension
db.init_app(app)



@app.route("/")
def home():
    return "Hello, world"


@app.route("/product", methods=['GET'])
def list_products():
    # import pdb; pdb.set_trace()
    query = db.select(Product).order_by(Product.name)
    products = db.session.execute(query).scalars().all()
    ret = []
    for product in products:
        # image_url = [image.url for image in ProductImage.query.filter_by(product_id=product.id).all()]
        image = ProductImage.query.filter_by(product_id=product.id).first()
        image_url = image.url if image else None
        category = Category.query.get(product.category_id)
        details = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_name": category.name if category else None,
            "image": image_url,
        }
        ret.append(details)
    return flask.jsonify(ret)

@app.route('/products/add', methods=['POST'])
def create_product():
    data = flask.request.get_json()
    
    # Find category by name
    category_name = data['category_name']
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()

    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        category_id=category.id  # Use the found category's ID
    )
    db.session.add(new_product)
    db.session.commit()

    images_data = data['image']
    new_image = ProductImage(
        url=images_data,
        product_id=new_product.id
    )
    db.session.add(new_image)
    
    db.session.commit()

    ret = {
        "id": new_product.id,
        "name": new_product.name,
        "description": new_product.description,
        "price": new_product.price,
        "category_id": new_product.category_id,
        "category_name": category.name,
        "image": images_data,
    }
    return flask.jsonify(ret)



# ###################################

@app.route('/categories/add', methods=['POST'])
def create_category():
    data = flask.request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    ret = {
        "id": new_category.id,
        "name": new_category.name
    }
    return flask.jsonify(ret)

@app.route('/categories', methods=['GET'])
def get_categories():
    query = db.select(Category).order_by(Category.name)
    categories = db.session.execute(query).scalars()
    ret = []
    for category in categories:
      products_list = []
      for product in category.products:
          product_dict = {
              'id': product.id,
              'name': product.name,
              'price': float(product.price),
          }
          products_list.append(product_dict)
      
      category_dict = {
          'id': category.id,
          'name': category.name,
          'products': products_list
      }
      ret.append(category_dict)
    return flask.jsonify(ret)




if __name__ == "__main__":
  init_db()
  app.run(port=5000)





