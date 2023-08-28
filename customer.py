from flask import Flask,request, jsonify
from markupsafe import escape
import sqlite3
app= Flask(__name__)

def db_connection():
    return sqlite3.connect('practice')

@app.route('/createCustomer', methods=['POST'])
def createCustomer():
    customer_name = request.form.get('customer_name')
    email = request.form.get('email')
    address = request.form.get('address')
    total_orders = int(request.form.get('total_orders'))
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customer (customer_name, email, address, total_orders) VALUES (?, ?, ?, ?)',
                       (customer_name, email, address, total_orders))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer data inserted successfully'}), 201

@app.route('/deleteCustomer/<int:id>', methods=['DELETE'])
def deleteCustomer(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer WHERE id = ?', (id,))
    customer = cursor.fetchone()
    if customer is None:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404
    cursor.execute('DELETE FROM customer WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer deleted successfully'}),201

@app.route('/getAllCustomers', methods=['GET'])
def getAllCustomers():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()
    if customers is None:
        conn.close()
        return jsonify({'error':'customer not found'}),401
    customers_list = [{
        'id': customer[0],
        'customer_name': customer[1],
        'email': customer[2],
        'address': customer[3],
        'total_orders': customer[4]
    } for customer in customers]
    conn.commit()
    conn.close()
    return jsonify(customers_list),201

@app.route('/getCustomersById/<int:id>', methods=['GET'])
def getCustomersById(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer where id = ?',(id,))
    customers = cursor.fetchone()
    if customers is None:
        conn.close()
        return jsonify({'error':'customer not found'})
    customers_list = [{
        'id': customers[0],
        'customer_name': customers[1],
        'email': customers[2],
        'address': customers[3],
        'total_orders': customers[4]
    }]
    conn.commit()
    conn.close()
    return jsonify(customers_list),201

@app.route('/updateCustomer/<int:id>',methods=['PUT'])
def updateCustomer(id):
    
    update_data=request.args
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer where id = ?',(id,))
    customer=cursor.fetchone()
    update_query = 'UPDATE customer SET '
    params = []
    for key, value in update_data.items():
            if key in ['customer_name', 'email', 'address', 'total_orders']:
                update_query += f'{key} = ?, '
                params.append(value)
    update_query = update_query.rstrip(', ')
    update_query += ' WHERE id = ?'
    params.append(id)
    cursor.execute(update_query, params)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Customer data updated successfully'}), 200

app.run(debug=True)

