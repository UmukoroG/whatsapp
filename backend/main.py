from flask import Flask, request, jsonify
from entities.seller import Seller
from entities.db_driver import sellersEntity, db, salesEntity

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def process_image():
    data, name = request.form, request.form.get('name')
    phone_number, path = data.get('phone_number'), data.get('path')

    if not Seller.is_seller(phone_number, db):
        Seller.register_seller(phone_number, name, sellersEntity, db)
    response = Seller(phone_number, db).renew_subscription(path)
    return jsonify({"message": response.txt})


if __name__ == '__main__':
    app.run()
