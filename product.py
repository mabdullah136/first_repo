from flask import Flask,request, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename
import os.path
import secrets
app= Flask(__name__)

def db_connection():
    return sqlite3.connect('practice')

UPLOAD_FOLDER='static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def generate_random_filename(filename):
    _, extension = os.path.splitext(filename)
    random_hex = secrets.token_hex(8)
    new_filename = random_hex + extension
    return new_filename

@app.route('/createProduct',methods=['POST'])
def createProduct():
    try:
        product_id=request.form.get('product_id')
        product_name=request.form.get('product_name')
        product_price=request.form.get('product_price')
        product_color=request.form.get('product_color')
        product_image=request.files.get('product_image')
        if not product_name or not product_price or not product_color or not product_image:
           return jsonify({'error':'missing data requird'}),400
        if not allowed_file(product_image.filename):
           return jsonify({'error':'Unsupported image data'}),400
        conn=db_connection()
        cursor=conn.cursor()
        filename = secure_filename(product_image.filename)
        fn=generate_random_filename(filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'],fn)
        insert_query = "INSERT INTO product (product_name, product_price, product_color,product_image) VALUES (?, ?, ?, ?)"
        params = (product_name, product_price, product_color, image_path)
        cursor.execute(insert_query, params)
        conn.commit()
        product_image.save(image_path)
        conn.close()
        return jsonify({'message': 'Product created successfully'})    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getAllProduct',methods=['GET'])
def get_all_product():
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM product')
    products=cursor.fetchall()
    if products is None:
        conn.close()
        return jsonify({'error':'product not found'})    
    product_list=[{
        'product_id':product[0],
        'product_name':product[1],
        'product_price':product[2],
        'product_color':product[3],
        'product_image':product[4]
    }for product in products]
    conn.commit()
    conn.close()
    return jsonify(product_list)

@app.route('/getById/<int:product_id>',methods=['GET'])
def get_product_by_id(product_id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM product where product_id = ?',(product_id,))
    products=cursor.fetchone()
    if products is None:
        conn.close()
        return jsonify({'error':'product not found'}),404    
    product_list=[{
        'product_id':products[0],
        'product_name':products[1],
        'product_price':products[2],
        'product_color':products[3],
        'product_image':products[4]
    }]
    conn.commit()
    conn.close()
    return jsonify(product_list),201

@app.route('/updateProduct/<int:product_id>', methods=['POST'])
def update_product(product_id):
    try:
        product_data = {
            'product_name': request.form.get('product_name'),
            'product_price': request.form.get('product_price'),
            'product_color': request.form.get('product_color')
        }
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM product WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        product_data = {key: value for key, value in product_data.items() if value is not None}

        if 'product_image' in request.files:
            image_file = request.files['product_image']
            if image_file and allowed_file(image_file.filename):
                if product[4]:
                    os.remove(product[4])
                filename = secure_filename(image_file.filename)
                fn = generate_random_filename(filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], fn)
                image_file.save(image_path)
                product_data['product_image'] = image_path

        if not product_data:
            return jsonify({'error': 'No valid data provided'}), 400

        update_query = 'UPDATE product SET '
        params = []
        for key, value in product_data.items():
            update_query += f'{key} = ?, '
            params.append(value)

        update_query = update_query.rstrip(', ')
        update_query += ' WHERE product_id = ?'
        params.append(product_id)
        cursor.execute(update_query, params)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product data updated successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteProduct/<int:product_id>',methods=['DELETE'])
def deleteProduct(product_id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM product where product_id=?',(product_id,))
    product=cursor.fetchone()
    if product is None:
        conn.close()
        return jsonify({'error':'product not found'}),401
    filename=product[4]
    os.remove(filename)
    cursor.execute('DELETE FROM product where product_id=?',(product_id,))
    conn.commit()
    conn.close()
    return jsonify({'message':'product deleted successfully'}),201

app.run(debug=True)