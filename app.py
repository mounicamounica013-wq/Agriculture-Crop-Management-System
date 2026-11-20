from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "agriculture-local-key")

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="agri_app",
        password=os.environ.get("DB_PASSWORD"),
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

    # Recently Registered Farmers
    cursor.execute("""
        SELECT farmer_id, name, contact, village, district, registration_date
        FROM Farmer
        ORDER BY farmer_id DESC
        LIMIT 5
    """)

    recent_farmers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        farmers=farmers_count,
        farms=farms_count,
        crops=crops_count,
        production=production,
        recent_farmers=recent_farmers
    )



@app.route("/crops")
def crops():
    search = request.args.get("search", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT crop_id, farm_id, crop_name, season,
               crop_category, expected_duration_days
        FROM Crop
        WHERE crop_name LIKE %s
           OR season LIKE %s
           OR crop_category LIKE %s
        ORDER BY crop_id DESC
    """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    crop_data = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT crop_category)
        FROM Crop
        WHERE crop_category IS NOT NULL
          AND crop_category != ''
    """)
    category_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT season)
        FROM Crop
        WHERE season IS NOT NULL
          AND season != ''
    """)
    season_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "crops.html",
        crops=crop_data,
        search=search,
        category_count=category_count,
        season_count=season_count
    )


@app.route("/add_crop", methods=["GET", "POST"])
def add_crop():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        farm_id = request.form.get("farm_id") or None
        crop_name = request.form["crop_name"].strip()
        season = request.form["season"].strip()
        crop_category = request.form.get("crop_category", "").strip() or None
        duration = request.form.get("expected_duration_days") or None

        try:
            cursor.execute("""
                INSERT INTO Crop
                (farm_id, crop_name, season,
                 crop_category, expected_duration_days)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                farm_id,
                crop_name,
                season,
                crop_category,
                duration
            ))

            conn.commit()
            flash("Crop added successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            print("Database Error:", err)
            flash("Unable to add crop. Please check the details.", "error")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("crops"))

    cursor.execute("""
        SELECT farm_id, location
        FROM Farm
        ORDER BY farm_id DESC
    """)
    farm_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("add_crop.html", farms=farm_data)


@app.route("/edit_crop/<int:crop_id>", methods=["GET", "POST"])
def edit_crop(crop_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        farm_id = request.form.get("farm_id") or None
        crop_name = request.form["crop_name"].strip()
        season = request.form["season"].strip()
        crop_category = request.form.get("crop_category", "").strip() or None
        duration = request.form.get("expected_duration_days") or None

        try:
            cursor.execute("""
                UPDATE Crop
                SET farm_id=%s,
                    crop_name=%s,
                    season=%s,
                    crop_category=%s,
                    expected_duration_days=%s
                WHERE crop_id=%s
            """, (
                farm_id,
                crop_name,
                season,
                crop_category,
                duration,
                crop_id
            ))

            conn.commit()
            flash("Crop updated successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            print("Database Error:", err)
            flash("Unable to update crop.", "error")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("crops"))

    cursor.execute("""
        SELECT crop_id, farm_id, crop_name, season,
               crop_category, expected_duration_days
        FROM Crop
        WHERE crop_id=%s
    """, (crop_id,))

    crop_data = cursor.fetchone()

    cursor.execute("""
        SELECT farm_id, location
        FROM Farm
        ORDER BY farm_id DESC
    """)
    farm_data = cursor.fetchall()

    cursor.close()
    conn.close()

    if crop_data is None:
        flash("Crop not found!", "error")
        return redirect(url_for("crops"))

    return render_template(
        "edit_crop.html",
        crop=crop_data,
        farms=farm_data
    )


@app.route("/delete_crop/<int:crop_id>", methods=["POST"])
def delete_crop(crop_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Crop WHERE crop_id=%s",
            (crop_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            flash("Crop deleted successfully!", "success")
        else:
            flash("Crop not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        print("Database Error:", err)
        flash(
            "This crop is linked to other records and cannot be deleted.",
            "error"
        )

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("crops"))

@app.route("/farms")
def farms():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Farm.farm_id, Farm.farmer_id,
               Farmer.name, Farm.location, Farm.total_area
        FROM Farm
        LEFT JOIN Farmer
        ON Farm.farmer_id = Farmer.farmer_id
        ORDER BY Farm.farm_id DESC
    """)

    farm_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("farms.html", farms=farm_data)
@app.route("/add_farm", methods=["GET", "POST"])
def add_farm():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        farmer_id = request.form["farmer_id"]
        location = request.form["location"]
        total_area = request.form["total_area"]

        cursor.execute("""
            INSERT INTO Farm (farmer_id, location, total_area)
            VALUES (%s, %s, %s)
        """, (farmer_id, location, total_area))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Farm added successfully!", "success")
        return redirect(url_for("farms"))

    cursor.execute("SELECT farmer_id, name FROM Farmer ORDER BY name")
    farmer_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("add_farm.html", farmers=farmer_data)
@app.route("/edit_farm/<int:farm_id>", methods=["GET", "POST"])
def edit_farm(farm_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        farmer_id = request.form["farmer_id"]
        location = request.form["location"]
        total_area = request.form["total_area"]

        cursor.execute("""
            UPDATE Farm
            SET farmer_id=%s, location=%s, total_area=%s
            WHERE farm_id=%s
        """, (farmer_id, location, total_area, farm_id))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Farm updated successfully!", "success")
        return redirect(url_for("farms"))

    cursor.execute("""
        SELECT farm_id, farmer_id, location, total_area
        FROM Farm
        WHERE farm_id=%s
    """, (farm_id,))

    farm_data = cursor.fetchone()

    cursor.execute("SELECT farmer_id, name FROM Farmer ORDER BY name")
    farmer_data = cursor.fetchall()

    cursor.close()
    conn.close()

    if farm_data is None:
        flash("Farm not found!", "error")
        return redirect(url_for("farms"))

    return render_template(
        "edit_farm.html",
        farm=farm_data,
        farmers=farmer_data
    )
@app.route("/delete_farm/<int:farm_id>", methods=["POST"])
def delete_farm(farm_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Farm WHERE farm_id=%s",
            (farm_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            flash("Farm deleted successfully!", "success")
        else:
            flash("Farm not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Unable to delete farm.", "error")
        print("Database Error:", err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("farms"))   
@app.route("/farmers")
def farmers():
    search = request.args.get("search", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT farmer_id, name, contact, address,
               gender, age, email, village, taluk,
               district, farmer_type, total_land_area,
               farming_experience, main_crop,
               irrigation_facility, registration_date
        FROM Farmer
        WHERE name LIKE %s
           OR contact LIKE %s
           OR village LIKE %s
           OR district LIKE %s
        ORDER BY farmer_id DESC
    """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    farmer_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "farmers.html",
        farmers=farmer_data,
        search=search
    )

@app.route("/edit_farmer/<int:farmer_id>", methods=["GET", "POST"])
def edit_farmer(farmer_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form.get("name")
        contact = request.form.get("contact")
        gender = request.form.get("gender")
        age = request.form.get("age") or None
        alternate_contact = request.form.get("alternate_contact")
        email = request.form.get("email")

        door_no = request.form.get("door_no")
        street = request.form.get("street")
        village = request.form.get("village")
        taluk = request.form.get("taluk")
        district = request.form.get("district")
        state = request.form.get("state")
        pincode = request.form.get("pincode")

        address = ", ".join(
            value for value in [
                door_no, street, village, taluk,
                district, state, pincode
            ] if value
        )

        farmer_type = request.form.get("farmer_type")
        total_land_area = request.form.get("total_land_area") or None
        farming_experience = request.form.get("farming_experience") or None
        main_crop = request.form.get("main_crop")
        irrigation_facility = request.form.get("irrigation_facility")

        try:
            cursor.execute("""
                UPDATE Farmer SET
                    name=%s, contact=%s, address=%s,
                    gender=%s, age=%s, alternate_contact=%s,
                    email=%s, door_no=%s, street=%s,
                    village=%s, taluk=%s, district=%s,
                    state=%s, pincode=%s, farmer_type=%s,
                    total_land_area=%s, farming_experience=%s,
                    main_crop=%s, irrigation_facility=%s
                WHERE farmer_id=%s
            """, (
                name, contact, address, gender, age,
                alternate_contact, email, door_no, street,
                village, taluk, district, state, pincode,
                farmer_type, total_land_area,
                farming_experience, main_crop,
                irrigation_facility, farmer_id
            ))

            conn.commit()
            flash("Farmer details updated successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to update farmer details.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("farmers"))

    cursor.execute("""
    SELECT farmer_id, name, contact, address,
           gender, age, email, alternate_contact,
           door_no, street, village, taluk,
           district, state, pincode, farmer_type,
           total_land_area, farming_experience,
           main_crop, irrigation_facility,
           registration_date
    FROM Farmer
    WHERE farmer_id=%s
""", (farmer_id,))
    farmer = cursor.fetchone()

    cursor.close()
    conn.close()

    if farmer is None:
        flash("Farmer not found.", "error")
        return redirect(url_for("farmers"))

    return render_template("edit_farmer.html", farmer=farmer)
    return render_template("edit_farmer.html", farmer=farmer)



# DELETE FARMER
@app.route("/delete_farmer/<int:farmer_id>", methods=["POST"])
def delete_farmer(farmer_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Farmer WHERE farmer_id=%s",
            (farmer_id,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            flash("Farmer deleted successfully!", "success")
        else:
            flash("Farmer not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Unable to delete farmer.", "error")
        print("Database Error:", err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("farmers"))


# ADD INPUT
@app.route("/add_input", methods=["GET", "POST"])
def add_input():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cultivation_id = request.form.get("cultivation_id")
        fertilizer_type = request.form.get("fertilizer_type")
        quantity_used = request.form.get("quantity_used")
        input_cost = request.form.get("input_cost")
        application_date = request.form.get("application_date")

        try:
            cursor.execute("""
                INSERT INTO `input`
                (cultivation_id, fertilizer_type, quantity_used,
                 input_cost, application_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                cultivation_id,
                fertilizer_type,
                quantity_used,
                input_cost,
                application_date
            ))

            conn.commit()
            flash("Input added successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to add input.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("inputs"))

    

    cursor.execute("""
        SELECT c.cultivation_id,
               cr.crop_name,
               f.location,
               c.season
        FROM Cultivation c
        LEFT JOIN Crop cr
            ON c.crop_id = cr.crop_id
        LEFT JOIN Farm f
            ON c.farm_id = f.farm_id
    """)

    cultivation_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "add_input.html",
        cultivations=cultivation_data
    )

# EDIT INPUT
@app.route("/edit_input/<int:input_id>", methods=["GET", "POST"])
def edit_input(input_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cultivation_id = request.form.get("cultivation_id")
        fertilizer_type = request.form.get("fertilizer_type")
        quantity_used = request.form.get("quantity_used")
        input_cost = request.form.get("input_cost")
        application_date = request.form.get("application_date")

        try:
            cursor.execute("""
                UPDATE `input`
                SET cultivation_id=%s,
                    fertilizer_type=%s,
                    quantity_used=%s,
                    input_cost=%s,
                    application_date=%s
                WHERE input_id=%s
            """, (
                cultivation_id,
                fertilizer_type,
                quantity_used,
                input_cost,
                application_date,
                input_id
            ))

            conn.commit()
            flash("Input updated successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to update input.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("inputs"))

    cursor.execute("""
        SELECT input_id, cultivation_id, fertilizer_type,
               quantity_used, input_cost, application_date
        FROM `input`
        WHERE input_id=%s
    """, (input_id,))

    input_data = cursor.fetchone()

    cursor.execute("SELECT cultivation_id, crop_id, season FROM Cultivation")
    cultivation_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "edit_input.html",
        input=input_data,
        cultivation=cultivation_data
    )

# DELETE INPUT
@app.route("/delete_input/<int:input_id>", methods=["POST"])
def delete_input(input_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM `input` WHERE input_id=%s",
            (input_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            flash("Input deleted successfully!", "success")
        else:
            flash("Input not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Unable to delete input.", "error")
        print("Database Error:", err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("inputs"))

# INPUTS
@app.route("/inputs")
def inputs():

    search = request.args.get("search", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.input_id, i.cultivation_id,
               i.fertilizer_type, i.quantity_used,
               i.input_cost, i.application_date,
               c.season, cr.crop_name
        FROM `input` i
        LEFT JOIN Cultivation c
            ON i.cultivation_id = c.cultivation_id
        LEFT JOIN Crop cr
            ON c.crop_id = cr.crop_id
        WHERE i.fertilizer_type LIKE %s
           OR cr.crop_name LIKE %s
           OR CAST(i.cultivation_id AS CHAR) LIKE %s
        ORDER BY i.input_id DESC
    """, (f"%{search}%", f"%{search}%", f"%{search}%"))

    input_data = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*),
               COALESCE(SUM(quantity_used), 0),
               COALESCE(SUM(input_cost), 0),
               COUNT(DISTINCT fertilizer_type)
        FROM `input`
        WHERE fertilizer_type LIKE %s
    """, (f"%{search}%",))

    summary = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "inputs.html",
        inputs=input_data,
        search=search,
        summary=summary
    )

# IRRIGATION MANAGEMENT
@app.route("/irrigation")
def irrigation():

    search = request.args.get("search", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT irrigation_id, cultivation_id,
               irrigation_date, water_quantity,
               irrigation_method
        FROM Irrigation
        WHERE irrigation_method LIKE %s
           OR CAST(cultivation_id AS CHAR) LIKE %s
        ORDER BY irrigation_id DESC
    """, (f"%{search}%", f"%{search}%"))

    irrigation_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "irrigation.html",
        irrigation=irrigation_data,
        search=search
    )


# ADD IRRIGATION
@app.route("/add_irrigation", methods=["GET", "POST"])
def add_irrigation():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cultivation_id = request.form.get("cultivation_id")
        irrigation_date = request.form.get("irrigation_date")
        water_quantity = request.form.get("water_quantity")
        irrigation_method = request.form.get("irrigation_method")

        try:
            cursor.execute("""
                INSERT INTO Irrigation
                (cultivation_id, irrigation_date,
                 water_quantity, irrigation_method)
                VALUES (%s, %s, %s, %s)
            """, (
                cultivation_id,
                irrigation_date,
                water_quantity,
                irrigation_method
            ))

            conn.commit()
            flash("Irrigation added successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to add irrigation.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("irrigation"))

    cursor.execute("""
        SELECT c.cultivation_id,
               cr.crop_name,
               f.location,
               c.season
        FROM Cultivation c
        LEFT JOIN Crop cr ON c.crop_id = cr.crop_id
        LEFT JOIN Farm f ON c.farm_id = f.farm_id
    """)

    cultivations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "add_irrigation.html",
        cultivations=cultivations
    )


# EDIT IRRIGATION
@app.route("/edit_irrigation/<int:irrigation_id>", methods=["GET", "POST"])
def edit_irrigation(irrigation_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cultivation_id = request.form.get("cultivation_id")
        irrigation_date = request.form.get("irrigation_date")
        water_quantity = request.form.get("water_quantity")
        irrigation_method = request.form.get("irrigation_method")

        try:
            cursor.execute("""
                UPDATE Irrigation
                SET cultivation_id=%s,
                    irrigation_date=%s,
                    water_quantity=%s,
                    irrigation_method=%s
                WHERE irrigation_id=%s
            """, (
                cultivation_id,
                irrigation_date,
                water_quantity,
                irrigation_method,
                irrigation_id
            ))

            conn.commit()
            flash("Irrigation updated successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to update irrigation.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("irrigation"))

    cursor.execute("""
        SELECT irrigation_id, cultivation_id,
               irrigation_date, water_quantity,
               irrigation_method
        FROM Irrigation
        WHERE irrigation_id=%s
    """, (irrigation_id,))

    irrigation_data = cursor.fetchone()

    cursor.execute("""
        SELECT c.cultivation_id,
               cr.crop_name,
               f.location,
               c.season
        FROM Cultivation c
        LEFT JOIN Crop cr ON c.crop_id = cr.crop_id
        LEFT JOIN Farm f ON c.farm_id = f.farm_id
    """)

    cultivations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "edit_irrigation.html",
        irrigation=irrigation_data,
        cultivations=cultivations
    )


# DELETE IRRIGATION
@app.route("/delete_irrigation/<int:irrigation_id>", methods=["POST"])
def delete_irrigation(irrigation_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Irrigation WHERE irrigation_id=%s",
            (irrigation_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            flash("Irrigation deleted successfully!", "success")
        else:
            flash("Irrigation record not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Unable to delete irrigation.", "error")
        print("Database Error:", err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("irrigation"))


# HARVEST MANAGEMENT
@app.route("/harvest")
def harvest():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT harvest_id, cultivation_id,
               harvest_date, quantity_harvested,
               quality_category, selling_price
        FROM Harvest
        ORDER BY harvest_id DESC
    """)

    harvest_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("harvest.html", harvest=harvest_data)

# ADD HARVEST
@app.route("/add_harvest", methods=["GET", "POST"])
def add_harvest():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        cultivation_id = request.form.get("cultivation_id")
        harvest_date = request.form.get("harvest_date")
        quantity_harvested = request.form.get("quantity_harvested")
        quality_category = request.form.get("quality_category")
        selling_price = request.form.get("selling_price")

        try:
            cursor.execute("""
                INSERT INTO Harvest (
                    cultivation_id, harvest_date,
                    quantity_harvested, quality_category,
                    selling_price
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                cultivation_id, harvest_date,
                quantity_harvested, quality_category,
                selling_price
            ))

            conn.commit()
            flash("Harvest record added successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to add harvest record.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("harvest"))

    cursor.execute("""
        SELECT cultivation_id
        FROM Cultivation
        ORDER BY cultivation_id
    """)
    cultivations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "add_harvest.html",
        cultivations=cultivations
    )


# EDIT HARVEST
@app.route("/edit_harvest/<int:harvest_id>", methods=["GET", "POST"])
def edit_harvest(harvest_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        cultivation_id = request.form.get("cultivation_id")
        harvest_date = request.form.get("harvest_date")
        quantity_harvested = request.form.get("quantity_harvested")
        quality_category = request.form.get("quality_category")
        selling_price = request.form.get("selling_price")

        try:
            cursor.execute("""
                UPDATE Harvest
                SET cultivation_id=%s,
                    harvest_date=%s,
                    quantity_harvested=%s,
                    quality_category=%s,
                    selling_price=%s
                WHERE harvest_id=%s
            """, (
                cultivation_id, harvest_date,
                quantity_harvested, quality_category,
                selling_price, harvest_id
            ))

            conn.commit()
            flash("Harvest record updated successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Unable to update harvest record.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("harvest"))

    cursor.execute("""
        SELECT harvest_id, cultivation_id,
               harvest_date, quantity_harvested,
               quality_category, selling_price
        FROM Harvest
        WHERE harvest_id=%s
    """, (harvest_id,))

    harvest_data = cursor.fetchone()

    cursor.execute("""
        SELECT cultivation_id
        FROM Cultivation
        ORDER BY cultivation_id
    """)

    cultivations = cursor.fetchall()

    cursor.close()
    conn.close()

    if harvest_data is None:
        flash("Harvest record not found!", "error")
        return redirect(url_for("harvest"))

    return render_template(
        "edit_harvest.html",
        harvest=harvest_data,
        cultivations=cultivations
    )

# DELETE HARVEST
@app.route("/delete_harvest/<int:harvest_id>", methods=["POST"])
def delete_harvest(harvest_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Harvest WHERE harvest_id=%s",
            (harvest_id,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            flash("Harvest record deleted successfully!", "success")
        else:
            flash("Harvest record not found!", "error")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Unable to delete harvest record.", "error")
        print("Database Error:", err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("harvest"))


# ANALYSIS DASHBOARD
@app.route("/analysis")
def analysis():
    conn = get_connection()
    cursor = conn.cursor()

    # Crop-wise production, area, selling price and input cost
    cursor.execute("""
        SELECT
            cr.crop_name,
            COALESCE(ca.total_area, 0),
            COALESCE(hq.total_quantity, 0),
            CASE
                WHEN COALESCE(hq.total_quantity, 0) > 0
                THEN hq.total_revenue / hq.total_quantity
                ELSE 0
            END,
            COALESCE(ic.total_cost, 0)
        FROM Crop cr

        LEFT JOIN (
            SELECT crop_id, SUM(cultivated_area) AS total_area
            FROM Cultivation
            GROUP BY crop_id
        ) ca ON cr.crop_id = ca.crop_id

        LEFT JOIN (
            SELECT
                c.crop_id,
                SUM(h.quantity_harvested) AS total_quantity,
                SUM(h.quantity_harvested * h.selling_price) AS total_revenue
            FROM Harvest h
            JOIN Cultivation c
                ON h.cultivation_id = c.cultivation_id
            GROUP BY c.crop_id
        ) hq ON cr.crop_id = hq.crop_id

        LEFT JOIN (
            SELECT
                c.crop_id,
                SUM(i.input_cost) AS total_cost
            FROM `input` i
            JOIN Cultivation c
                ON i.cultivation_id = c.cultivation_id
            GROUP BY c.crop_id
        ) ic ON cr.crop_id = ic.crop_id

        ORDER BY cr.crop_name
    """)

    analysis_data = cursor.fetchall()

    # Chart data
    crop_production = [
        (item[0], float(item[2] or 0))
        for item in analysis_data
    ]

    yield_data = [
        (
            item[0],
            float(item[2] / item[1]) if item[1] else 0
        )
        for item in analysis_data
    ]

    revenue_cost_data = [
        (
            item[0],
            float(item[2] * item[3]),
            float(item[4])
        )
        for item in analysis_data
    ]

    cursor.close()
    conn.close()

    return render_template(
        "analysis.html",
        analysis=analysis_data,
        crop_production=crop_production,
        yield_data=yield_data,
        revenue_cost_data=revenue_cost_data
    )

@app.route("/add_farmer", methods=["GET", "POST"])
def add_farmer():

    if request.method == "POST":

        name = request.form.get("name")
        contact = request.form.get("contact")
        address = request.form.get("address")

        gender = request.form.get("gender")
        age = request.form.get("age") or None
        alternate_contact = request.form.get("alternate_contact")
        email = request.form.get("email")

        door_no = request.form.get("door_no")
        street = request.form.get("street")
        village = request.form.get("village")
        taluk = request.form.get("taluk")
        district = request.form.get("district")
        state = request.form.get("state")
        pincode = request.form.get("pincode")

        farmer_type = request.form.get("farmer_type")
        total_land_area = request.form.get("total_land_area") or None
        farming_experience = request.form.get("farming_experience") or None
        main_crop = request.form.get("main_crop")
        irrigation_facility = request.form.get("irrigation_facility")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Farmer (
                    name, contact, address, gender, age,
                    alternate_contact, email, door_no, street,
                    village, taluk, district, state, pincode,
                    farmer_type, total_land_area,
                    farming_experience, main_crop,
                    irrigation_facility
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, (
                name, contact, address, gender, age,
                alternate_contact, email, door_no, street,
                village, taluk, district, state, pincode,
                farmer_type, total_land_area,
                farming_experience, main_crop,
                irrigation_facility
            ))

            conn.commit()
            flash("Farmer registered successfully!", "success")

        except mysql.connector.Error as err:
            conn.rollback()
            flash("Registration failed. Please check the details.", "error")
            print("Database Error:", err)

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("home"))

    return render_template("add_farmer.html")
if __name__ == "__main__":
    app.run(debug=True)