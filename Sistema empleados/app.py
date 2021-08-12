from flask import Flask
from flask import render_template, request, redirect,url_for,flash
from flaskext.mysql import MySQL
from datetime import date
today = date.today()

# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")

app=Flask(__name__)
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'deudas'
app.secret_key="developer"
mysql.init_app(app)
@app.route('/')
def index():
    sql="SELECT * FROM `personas` ;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    empleados=cursor.fetchall()
    conn.commit() 
    return render_template('personas/index.html',empleados=empleados)
@app.route('/crear')
def crear():

    return render_template("personas/create.html")
@app.route('/store', methods=["POST"])
def storage():
    nombre=request.form['txtnombre']
    telefono=request.form['numtele']
    abonos=0
    saldo=0
    direccion=request.form['txtdireccion']
    if nombre=="" or telefono =="" or abonos =="" or saldo =="" or direccion =="":
        flash("Recuerda llenar los datos de los campos")
        return redirect(url_for('crear'))
    #formato para subir fotos/archivos
    #foto=request.files['foto']
    #if foto.filename!='':
    """         now=datetime.now()
        tiempo=now.strftime("Y%H%M%S")
        nuevoNombre=tiempo+foto.filename
        foto.save("uploads/"+nuevoNombre) """
    sql="INSERT INTO `personas` (`id`, `nombre`, `direccion`, `telefono`, `abonos`, `saldo`) VALUES (NULL, %s, %s, %s, %s, %s);"
    datos=(nombre,direccion,telefono,abonos,saldo)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    flash("Usuario creado con exito")
    return redirect(url_for("index"))
@app.route('/destroy/<int:id>')
def destruir(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id=%s",(id))
    conn.commit()
    return redirect('/')
@app.route('/edit/<int:id>')
def editar(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id=%s",(id))
    persona=cursor.fetchall()
    conn.commit()
    return render_template('personas/edit.html',personas=persona)
@app.route('/update', methods=["POST"])
def actualizar():
    nombre=request.form['txtnombre']
    telefono=request.form['numtele']
    abonos=request.form['numabono']
    saldo=request.form['numsaldo']
    direccion=request.form['txtdireccion']
    id=request.form['txtid']

    sql="UPDATE  personas SET nombre=%s, direccion=%s, telefono=%s, abonos=%s, saldo=%s WHERE id=%s;"
    datos=(nombre,direccion,telefono,abonos,saldo,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
@app.route('/movimiento/<int:id>')
def move(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id=%s",(id))
    persona=cursor.fetchall()
    conn.commit() 
    return render_template('personas/movimiento.html', personas=persona,fecha=d1)

@app.route('/abonos', methods=["POST"])
def abonar():
    #id=request.form['txtid']
    nombre=request.form['txtnombre']
    fecha=request.form['txtfecha']
    tipo=request.form['tipo']
  
    cantidad=request.form['cantidad']
    if nombre=="" or fecha =="" or tipo ==""  or cantidad =="":
        flash("Recuerda llenar los datos de los campos")
        return redirect(url_for('abonar'))
 
    sql="INSERT INTO `movimientos` (`id`, `nombre`, `fecha`, `tipo`, `cantidad`) VALUES (NULL, %s, %s, %s, %s);"
    datos=(nombre,fecha,tipo,cantidad)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    cursor.execute("SELECT  * FROM personas WHERE nombre=%s;",(nombre))
    datos=cursor.fetchall()
    if tipo=="Préstamo":
        cantidad=float(cantidad)*-1;
    
    nvSaldo=float(datos[0][5])+float(cantidad);
    conn.commit()
    print(nvSaldo)
    cursor.execute("UPDATE personas SET saldo=%s WHERE nombre=%s;",(nvSaldo,nombre))
    conn.commit()
    return redirect(url_for('index'))
@app.route('/consultar/<str>')
def consulta(str):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM movimientos WHERE nombre=%s",(str))
    persona=cursor.fetchall()
    print(persona)
    conn.commit() 
    if len(persona)==0:
        flash("No se han generado movimientos")
    
    return render_template('personas/consultas.html', personas=persona)
   
if __name__=='__main__':
    app.run(debug=True)