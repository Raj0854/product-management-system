from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app)

filename = "products.json"
upload_folder = "static/uploads"
os.makedirs(upload_folder, exist_ok=True)


def load_products():
    if not os.path.exists(filename):
        products = [
            {
                "id": 1,
                "name": "Wireless Mouse",
                "category": "Electronics",
                "price": 799,
                "image": "https://images.unsplash.com/photo-1527814050087-3793815479db",
            },
            {
                "id": 2,
                "name": "Mechanical Keyboard",
                "category": "Electronics",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3",
            },
            {
                "id": 3,
                "name": "USB-C Fast Charger",
                "category": "Accessories",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0",
            },
            {
                "id": 4,
                "name": "Bluetooth Speaker",
                "category": "Electronics",
                "price": 1899,
                "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1",
            },
            {
                "id": 5,
                "name": "Laptop Backpack",
                "category": "Bags",
                "price": 1599,
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62",
            },
            {
                "id": 6,
                "name": "Stainless Steel Water Bottle",
                "category": "Home & Kitchen",
                "price": 699,
                "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8",
            },
            {
                "id": 7,
                "name": "Running Shoes",
                "category": "Footwear",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            },
            {
                "id": 8,
                "name": "Cotton T-Shirt",
                "category": "Clothing",
                "price": 599,
                "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
            },
            {
                "id": 9,
                "name": "Smart Watch",
                "category": "Wearables",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
            },
            {
                "id": 10,
                "name": "LED Desk Lamp",
                "category": "Home & Kitchen",
                "price": 999,
                "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c",
            },
            {
                "id": 11,
                "name": "Noise Cancelling Headphones",
                "category": "Electronics",
                "price": 4999,
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
            },
            {
                "id": 12,
                "name": "Mobile Phone Stand",
                "category": "Accessories",
                "price": 399,
                "image": "https://images.unsplash.com/photo-1609592424587-3c7e2d5e8a8e",
            },
            {
                "id": 13,
                "name": "Gaming Mouse Pad",
                "category": "Gaming",
                "price": 899,
                "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7",
            },
            {
                "id": 14,
                "name": "Power Bank 20000mAh",
                "category": "Electronics",
                "price": 1799,
                "image": "https://images.unsplash.com/photo-1609592424587-3c7e2d5e8a8e",
            },
            {
                "id": 15,
                "name": "Office Chair",
                "category": "Furniture",
                "price": 7499,
                "image": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8",
            },
        ]
        save_products(products)
        return products
    with open(filename, "r") as file:
        return json.load(file)


def save_products(products):
    with open(filename, "w") as file:
        json.dump(products, file, indent=4)


# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = load_products()
    return jsonify(products), 200


# GET SPECIFIC PRODUCT
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"message": "Product not found"}), 404


# POST data
@app.route("/products", methods=["POST"])
def add_product():
    products = load_products()

    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    image = request.files.get("image")

    # Required fields
    if not name or not category or not price:
        return (
            jsonify(
                {"message": "name, category and price all three fields are required"}
            ),
            400,
        )

    # Name validation
    if not isinstance(name, str) or name.strip() == "":
        return jsonify({"message": "Invalid name! Name cannot be empty"}), 400

    # Category validation
    if not isinstance(category, str) or category.strip() == "":
        return jsonify({"message": "Invalid category! Category cannot be empty"}), 400

    # Price validation
    try:
        price = float(price)
    except ValueError:
        return jsonify({"message": "Invalid price! Enter a valid number"}), 400

    if price <= 0:
        return (
            jsonify(
                {"message": "Invalid price! Price cannot be negative or less than zero"}
            ),
            400,
        )

    # Image validation
    if not image or image.filename == "":
        return jsonify({"message": "Product image is required"}), 400

    # Save image
    filename = secure_filename(image.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    image_path = os.path.join(upload_folder, unique_filename)
    image.save(image_path)

    # Generate ID
    if len(products) == 0:
        new_id = 1
    else:
        new_id = max(product["id"] for product in products) + 1

    new_product = {
        "id": new_id,
        "name": name.strip(),
        "category": category.strip(),
        "price": price,
        "image": f"/static/uploads/{unique_filename}",
    }

    products.append(new_product)
    save_products(products)

    return (
        jsonify({"message": "new product added successfully", "product": new_product}),
        201,
    )


# PUT DATA
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_proudct(product_id):
    products = load_products()
    data = request.get_json()
    if not data:
        return jsonify({"message": "product details cannot be empty"})
    allowed_fields = {"name", "category", "price"}
    for field in data:
        if field not in allowed_fields:
            return jsonify({"message": "Unexpected field", "fields": field})
    if not all(field in data for field in allowed_fields):
        return jsonify(
            {"message": "Name, category, price all three details are required."}
        )
    if not isinstance(data["name"], str) or data["name"].strip() == "":
        return jsonify({"message": "Invalid Name! Enter valid name"})

    if not isinstance(data["category"], str) or data["category"].strip() == "":
        return jsonify({"message": "Invalid category! Enter valid category"})

    if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
        return jsonify({"message": "Invalid price! Enter valid price"})
    for product in products:
        if product["id"] == product_id:
            product["name"] = data["name"]
            product["category"] = data["category"]
            product["price"] = data["price"]
            save_products(products)
            return (
                jsonify(
                    {"message": "product updated succesfully", "products": product}
                ),
                200,
            )
    return jsonify({"message": "product not found"}), 404


# patch data
@app.route("/products/<int:product_id>", methods=["PATCH"])
def update_field(product_id):
    products = load_products()
    data = request.get_json()
    if not data:
        return jsonify({"message": "Product deatisl cannot be empty"})
    allowed_fields = {"name", "category", "price"}
    for field in data:
        if field not in allowed_fields:
            return jsonify({"message": "unexpected fields", "fields": field})
    if "name" in data:
        if not isinstance(data["name"], str) or data["name"].strip() == "":
            return jsonify({"message": "Invalid name! Enter a correct name."}), 400
    if "category" in data:
        if not isinstance(data["category"], str) or data["category"].strip() == "":
            return (
                jsonify({"message": "Invalid category! Enter a correct category."}),
                400,
            )
    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
            return jsonify({"message": "Invalid price! Enter a correct price."}), 400
    for product in products:
        if product["id"] == product_id:
            if "name" in data:
                product["name"] = data["name"]
            if "category" in data:
                product["category"] = data["category"]
            if "price" in data:
                product["price"] = data["price"]
            save_products(products)
            return (
                jsonify(
                    {"message": "Product updated successfully.", "Product": product}
                ),
                200,
            )

    return jsonify({"message": "product not found"}), 404


# delete data
@app.route("/products/<int:product_id>", methods=["DELeTE"])
def delete_product(product_id):
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            save_products(products)
            return (
                jsonify(
                    {"message": "product deleted successfully", "product": product}
                ),
                200,
            )
    return jsonify({"message": "Product not found"}), 404


# run file
if __name__ == "__main__":
    app.run(debug=True)
