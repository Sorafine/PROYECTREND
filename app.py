from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'mydb'),
    'port': int(os.getenv('DATABASE_PORT', 3306))
}

conn = mysql.connector.connect(**db_config)

@app.route('/RegistrarCartera', methods=['GET', 'POST'])
def registrar_cartera():
    conn = mysql.connector.connect(**db_config) #"**"Esta sintaxis permite pasar un diccionario como argumentos de conexión
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM TIPOCARTERA")
    tipos = cursor.fetchall()
    mensaje = None

    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_id = request.form['tipo']
        precio = request.form['precio']
        fecha = request.form['fecha']

        cursor.execute("""
            INSERT INTO CARTERA (DESCRIPCAR, PRECIOCAR, FECHACAR, CODTIPCAR)
            VALUES (%s, %s, %s, %s)
        """, (nombre, precio, fecha, tipo_id))

        conn.commit()
        mensaje = "Se grabó el registro satisfactoriamente"

    cursor.close()
    conn.close()
    return render_template("RegistrarCartera.html", mensaje=mensaje, tipos=tipos)


@app.route('/ConsultarCartera', methods=['GET'])
def consultar_cartera():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM TIPOCARTERA")
    tipos = cursor.fetchall()
    carteras = []

    tipo_id = request.args.get('tipo')
    if tipo_id:
        cursor.execute("""
            SELECT c.CODCAR, c.DESCRIPCAR, t.NOMBTIPCAR, c.PRECIOCAR, c.FECHACAR
            FROM CARTERA c
            JOIN TIPOCARTERA t ON c.CODTIPCAR = t.CODTIPCAR
            WHERE c.CODTIPCAR = %s
        """, (tipo_id,))
        carteras = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("ConsultarCartera.html", carteras=carteras, tipos=tipos)


@app.route('/')
def home():
    return redirect(url_for('registrar_cartera'))

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    if not os.path.exists(app.config ['UPLOAD_FOLDER']):
        os.makedirs(app.config [ 'UPLOAD_FOLDER'])
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
