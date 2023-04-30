from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '3.88.249.223'
# La IP de la base de datos

app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = '0i160t47'
# El tipo de usuario con su constraseña respectiva del mySQL

app.config['MYSQL_DB'] = 'socrud'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data=cur.fetchall()
    return render_template('index.html', productos = data)
    #Mostrar todos los datos de la tabla "productos" del mySQL

@app.route('/create_producto', methods=['POST'])
def create_producto():
    if request.method == 'POST': 
        nombre = request.form['nombre']
        precio = request.form['precio']
        tipo = request.form['tipo']
        stock = request.form['stock']
        cur = mysql.connection.cursor() 

        cur.execute('INSERT INTO productos (nombre, precio, tipo, stock) VALUES (%s, %s, %s, %s)', 
        (nombre, precio, tipo, stock)) 
        mysql.connection.commit() 

        flash('Contacto agregado')
        return redirect(url_for('Index')) 
#index.html

@app.route('/edit/<id>')
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-producto.html', producto = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        tipo = request.form['tipo']
        stock = request.form['stock']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE productos 
        SET nombre = %s, 
        precio = %s, 
        tipo = %s, 
        stock = %s 
        WHERE id = %s
        """, (nombre, precio, tipo, stock, id ))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))
    #index.html

@app.route('/delete/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))
#index.html

if __name__ == '__main__':
    app.run(port = 5000, debug = True)