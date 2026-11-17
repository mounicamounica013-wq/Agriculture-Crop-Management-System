from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mouni1619_",
        database="agriculture_db"
    )

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Farmer")
    farmers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Farm")
    farms_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Crop")
    crops_count = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(quantity_harvested), 0) FROM Harvest")
    production = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        farmers=farmers_count,
        farms=farms_count,
        crops=crops_count,
        production=production
    )

@app.route("/crops")
def crops():
    return render_template("crops.html")

@app.route("/farms")
def farms():
    return render_template("farms.html")

@app.route("/farmers")
def farmers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT farmer_id, name, contact, address FROM Farmer")
    farmer_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("farmers.html", farmers=farmer_data)

@app.route("/inputs")
def inputs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT input_id, fertilizer_type, quantity_used,
               input_cost, application_date
        FROM Agricultural_Input
    """)
    input_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("inputs.html", inputs=input_data)
@app.route("/irrigation")
def irrigation():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT irrigation_id, cultivation_id, irrigation_date, water_quantity, irrigation_method FROM Irrigation")

    irrigation_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("irrigation.html", irrigation=irrigation_data)
@app.route("/harvest")
def harvest():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT harvest_id, cultivation_id, harvest_date,
               quantity_harvested, quality_category, selling_price
        FROM Harvest
    """)

    harvest_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("harvest.html", harvest=harvest_data)
@app.route("/analysis")
def analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Crop.crop_name,
               Cultivation.cultivated_area,
               Harvest.quantity_harvested,
               Harvest.selling_price,
               Agricultural_Input.input_cost
        FROM Cultivation
        JOIN Crop ON Cultivation.crop_id = Crop.crop_id
        JOIN Harvest ON Cultivation.cultivation_id = Harvest.cultivation_id
        JOIN Agricultural_Input
        ON Cultivation.cultivation_id = Agricultural_Input.cultivation_id
    """)

    analysis_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("analysis.html", analysis=analysis_data)


if __name__ == "__main__":
    app.run(debug=True)