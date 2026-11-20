
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD"),
        database="agriculture_db"
    )

    print("Database Connected Successfully!")

    query = """
    SELECT
        c.crop_name,
        cu.cultivated_area,
        h.quantity_harvested,
        h.selling_price,
        h.quality_category,
        (h.quantity_harvested / cu.cultivated_area) AS yield_per_acre,
        (h.quantity_harvested * h.selling_price) AS total_revenue
    FROM harvest h
    JOIN cultivation cu ON h.cultivation_id = cu.cultivation_id
    JOIN crop c ON cu.crop_id = c.crop_id
    """

    df = pd.read_sql(query, connection)

    print("\n===== AGRICULTURE DATA ANALYSIS =====")
    print(df.to_string(index=False))

    # Export analysis data
    df.to_csv("harvest_analysis.csv", index=False)
    print("\nCSV file created successfully!")

    # Crop-wise Yield Chart
    plt.figure(figsize=(9, 5))
    plt.bar(df["crop_name"], df["yield_per_acre"])
    plt.title("Crop-wise Yield Comparison")
    plt.xlabel("Crop Name")
    plt.ylabel("Yield (kg per acre)")
    plt.tight_layout()
    plt.savefig("yield_comparison.png")
    plt.show()

    # Crop-wise Revenue Chart
    plt.figure(figsize=(9, 5))
    plt.bar(df["crop_name"], df["total_revenue"])
    plt.title("Crop-wise Revenue Comparison")
    plt.xlabel("Crop Name")
    plt.ylabel("Revenue (Rupees)")
    plt.tight_layout()
    plt.savefig("revenue_comparison.png")
    plt.show()

    print("\nBoth charts saved successfully!")

except mysql.connector.Error as error:
    print("Database Error:", error)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
