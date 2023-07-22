from flask import Flask, request, jsonify
from entities.seller import Seller
from entities.db_driver import sellersEntity

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.form
    name, path = data.get('name'), data.get('path')
    phone_number = data.get('phone_number')

    if not Seller.is_seller(phone_number):
        Seller.register_seller(phone_number, name, sellersEntity)
    response = Seller(phone_number).renew_membership(path)
    return jsonify({"message": response.txt})


if __name__ == '__main__':
    app.run()