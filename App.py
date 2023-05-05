from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '44.203.193.51'
#Puerto IPv4 público de la capa de datos

app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = '0i160t47'
#Usuario y contraseña para poder acceder al mySQL

app.config['MYSQL_DB'] = 'socrud'
#Nombre de la base de datos de mySQL que se quiere utilizar

mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data=cur.fetchall()
    return render_template('index.html', productos = data)


@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST': 
        nombre = request.form['nombre']
        precio = request.form['precio']
        tipo = request.form['tipo']
        stock = request.form['stock']
        
        cur = mysql.connection.cursor()
        
        cur.execute('INSERT INTO productos (nombre, precio, tipo, stock) VALUES (%s, %s, %s, %s)', 
        (nombre, precio, tipo, stock))
        mysql.connection.commit()
        
        flash('Producto insertado')
        return redirect(url_for('Index'))


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
        
        cur.execute("""UPDATE productos SET nombre = %s, precio = %s, tipo = %s, stock = %s WHERE id = %s""", (nombre, precio, tipo, stock,id ))
        
        mysql.connection.commit()
        flash('Producto actualizado')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    
    cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    
    flash('Producto eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 5000, debug = True)
