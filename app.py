from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)


config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'api_consultas'
}

@app.route('/api/plantillas', methods=['POST'])
def crear_plantilla():
    data = request.json
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO plantillas_C (PL_NOMBRE, PL_PLANTILLASQL, PL_CREADOPOR)
    VALUES (%s, %s, %s)
    """
    valores = (data['PL_NOMBRE'], data['PL_PLANTILLASQL'], data['PL_CREADOPOR'])
    
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Plantilla creada"}), 201

@app.route('/api/resultados', methods=['GET'])
def obtener_resultados():
    cs_id = request.args.get('CS_ID')
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    
    sql = """
    SELECT RS_EJECUTADOEN, RS_RUTA_RESUL, RS_ESTADO 
    FROM resultados_C 
    WHERE RS_CS_ID = %s
    """
    cursor.execute(sql, (cs_id,))
    resultados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(resultados), 200

if __name__ == '__main__':
    app.run(debug=True)