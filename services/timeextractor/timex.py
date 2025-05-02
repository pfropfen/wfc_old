import mysql.connector
import csv
import os

def export_database_to_csv(host, user, password, database, port=3306, output_dir="output"):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    cursor = conn.cursor()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    for (table_name,) in tables:
        print(f"Exporting {table_name}...")
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        column_names = [desc[0] for desc in cursor.description]
        
        csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
        
        # write data to CSV
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # headers
            writer.writerows(rows)         # data
        
        print(f"{table_name} exported successfully to {csv_file_path}")
    
    # close connection
    cursor.close()
    conn.close()
    print("Database export completed.")

# connection to DB
export_database_to_csv(host="192.168.178.56", 
                       user="root", 
                       password="root", 
                       database="times", 
                       port=31006)