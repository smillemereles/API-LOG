from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
from auths import authenticate_api_key  

app = Flask(__name__)  

# Configuración de la base de datos
DB_CONFIG = {
    'DRIVER': '{SQL Server}',  
    'SERVER': 'LAPTOP-VLK7R72C',
    'DATABASE': 'LOGS',
    'Trusted_Connection': 'yes'
}

def get_db_connection():
    conn_str = f"DRIVER={DB_CONFIG['DRIVER']};SERVER={DB_CONFIG['SERVER']};DATABASE={DB_CONFIG['DATABASE']};Trusted_Connection={DB_CONFIG['Trusted_Connection']}"
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {str(e)}")
        raise

@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 * FROM logs")
        row = cursor.fetchone()
        if row:
            return jsonify({"message": "Database connection successful", "sample_data": str(row)}), 200
        else:
            return jsonify({"message": "Database connection successful, but no data found"}), 200
    except Exception as e:
        return jsonify({"error": f"Database connection failed: {str(e)}"}), 500

@app.route('/logs', methods=['GET', 'POST'])
@authenticate_api_key
def handle_logs():
    if request.method == 'GET':
        return get_logs()
    elif request.method == 'POST':
        return post_log()

def get_logs():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    service_name = request.args.get('serviceName')

    query = 'SELECT * FROM logs WHERE 1=1'
    params = []

    if start_date:
        try:
            parsed_start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
            params.append(parsed_start_date)
            query += ' AND timestamp >= ?'
        except ValueError:
            return jsonify({"error": "Invalid start date format. Use DD-MM-YYYY"}), 400

    if end_date:
        try:
            parsed_end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
            params.append(parsed_end_date)
            query += ' AND timestamp <= ?'
        except ValueError:
            return jsonify({"error": "Invalid end date format. Use DD-MM-YYYY"}), 400

    if service_name:
        params.append(service_name)
        query += ' AND service = ?'

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return jsonify(logs), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error querying logs"}), 500


def post_log():
    log = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = 'INSERT INTO logs (timestamp, service, log_level, message) VALUES (?, ?, ?, ?)'
        values = (log['timestamp'], log['service_name'], log['log_level'], log['message'])
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Log received", "log": log}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error saving log: {str(e)}"}), 500
    

if __name__ == '__main__':  

    app.run(debug=True, host='0.0.0.0', port=8080)
