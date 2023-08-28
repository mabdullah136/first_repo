from flask import Flask,request,jsonify
import sqlite3
app=Flask(__name__)

def db_connection():
    return sqlite3.connect('practice')

@app.route('/placeOrder',methods=['POST'])
def placeOrder():
    customer_id=request.form.get('customer_id')
    product_id=request.form.get('product_id')
    price=request.form.get('price')
    date_of_purchase=request.form.get('date_of_purchase')
    total_paid=request.form.get('total_paid')
    order_status=request.form.get('order_status')
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer WHERE id = ?',(customer_id,))
    customer=cursor.fetchone()
    cursor.execute('SELECT * FROM product where product_id = ?',(product_id,))
    product=cursor.fetchone()

    if customer is None or product is None:
        conn.close()
        return jsonify({'error':'customer or product is not found'})
    
    cursor.execute('INSERT INTO customer_orders (customer_id,product_id,price,date_of_purchase,total_paid,order_status) VALUES (?,?,?,?,?,?)',(customer_id,product_id,price,date_of_purchase,total_paid,order_status))
    conn.commit()
    conn.close()
    return jsonify({'message':'order placed successfully'})

@app.route('/getAllOrder',methods=['GET'])
def getAllOrder():
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer_orders')
    customer_orders=cursor.fetchall()
    if customer_orders is None:
        conn.close()
        return jsonify({'error':'customer_order not found'}),201
    customer_order_list = [{
        'id':customer_order[0],
        'customer_id':customer_order[1],
        'product_id':customer_order[2],
        'price':customer_order[3],
        'date_of_purchase':customer_order[4],
        'total_paid':customer_order[5],
        'order_status':customer_order[6]
    }for customer_order in customer_orders]
    return jsonify(customer_order_list)

@app.route('/getOrderById/<int:id>',methods=['GET'])
def getOrderById(id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer_orders where id = ?',(id,))
    customer_orders=cursor.fetchone()
    if customer_orders is None:
        conn.close()
        return jsonify({'error':'customer_order not found'}),201
    customer_order_list = [{
        'id':customer_orders[0],
        'customer_id':customer_orders[1],
        'product_id':customer_orders[2],
        'price':customer_orders[3],
        'date_of_purchase':customer_orders[4],
        'total_paid':customer_orders[5],
        'order_status':customer_orders[6]
    }]
    return jsonify(customer_order_list)

@app.route('/getOrderBySpecificCustomerId/<int:customer_id>',methods=['GET'])
def getOrderBySpecificCustomerId(customer_id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer_orders where customer_id = ?',(customer_id,))
    customer_orders=cursor.fetchall()
    print(len(customer_orders))
    if len(customer_orders) == 0:
        conn.close()
        return jsonify({'error':'customer_order not found'}),201
    customer_order_list = [{
        'id':customer_order[0],
        'customer_id':customer_order[1],
        'product_id':customer_order[2],
        'price':customer_order[3],
        'date_of_purchase':customer_order[4],
        'total_paid':customer_order[5],
        'order_status':customer_order[6]
    }for customer_order in customer_orders]
    return jsonify(customer_order_list)

@app.route('/updateOrder/<int:id>',methods=['PUT'])
def updateOrder(id):
    update_data=request.args
    print(update_data)
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer_orders WHERE id = ?',(id,))
    customer_orders=cursor.fetchone()
    if customer_orders is None:
        conn.close()
        return jsonify({'error':'customer_order is not found'})
    update_query = 'UPDATE customer_orders SET '
    params = []
    for key,value in update_data.items():
            if key in ['customer_id','product_id','price','date_of_purchase','total_paid','order_status']:
                update_query +=f'{key} = ?, '
                params.append(value)
    update_query=update_query.rstrip(', ')
    update_query += ' WHERE id = ?'
    params.append(id)
    cursor.execute(update_query, params)
    conn.commit()
    conn.close()
    return jsonify({'message':'customer_order updated successfully'}),201

@app.route('/deleteOrder/<int:id>',methods=['DELETE'])
def deleteOrder(id):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM customer_orders WHERE id = ?',(id,))
    customer_order=cursor.fetchone()
    if customer_order is None:
        conn.close()
        return jsonify({'error':'customer_order is not found'}),404
    cursor.execute('DELETE FROM customer_orders WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    return jsonify({'message':'customer_order is deleted Successfully'}),201

app.run(debug=True)

