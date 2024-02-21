import psycopg2
# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost", port="5432", database="test_3", 
    user="postgres", password="808as808")
cursor = connection.cursor()


def print_all_data():
    cursor.execute("SELECT * FROM PRODUCT;")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM PART;")
    parts = cursor.fetchall()
    
    print("PRODUCT table data:")
    for prod in products:
        print(prod)
    print("\nPART table data:")
    for part in parts:
        print(part)

def update_quantities(n):
    cursor.execute("UPDATE PRODUCT SET PROD_QOH = PROD_QOH + %s WHERE PROD_CODE = 'ABC';", (n,))
    cursor.execute("UPDATE PART SET PART_QOH = GREATEST(PART_QOH - %s, 0) WHERE PART_CODE IN ('A', 'B', 'C');", (n,))
    connection.commit()
    print("Quantities updated.")

def modify_product():
    new_qoh = int(input("Enter new quantity for PRODUCT 'ABC': "))
    if new_qoh >= 0:
        cursor.execute("UPDATE PRODUCT SET PROD_QOH = %s WHERE PROD_CODE = 'ABC';", (new_qoh,))
        connection.commit()
        print("PRODUCT 'ABC' quantity updated.")
    else:
        print("Quantity must be non-negative.")

def modify_part():
    part_code = input("Enter part code (A, B, or C): ").upper()
    if part_code in ['A', 'B', 'C']:
        new_qoh = int(input(f"Enter new quantity for PART '{part_code}': "))
        if new_qoh >= 0:
            cursor.execute("UPDATE PART SET PART_QOH = %s WHERE PART_CODE = %s;", (new_qoh, part_code))
            connection.commit()
            print(f"PART '{part_code}' quantity updated.")
        else:
            print("Quantity must be non-negative.")
    else:
        print("Invalid part code.")

def manage_part_table():
    choice = input("Enter 'add' to insert a new part or 'delete' to remove a part: ").lower()
    if choice == 'add':
        part_code = input("Enter new part code: ")
        part_qoh = int(input("Enter quantity on hand for the new part: "))
        cursor.execute("INSERT INTO PART (PART_CODE, PART_QOH) VALUES (%s, %s);", (part_code, part_qoh))
        connection.commit()
        print("New part added.")
    elif choice == 'delete':
        part_code = input("Enter part code to delete: ")
        cursor.execute("DELETE FROM PART WHERE PART_CODE = %s;", (part_code,))
        connection.commit()
        print("Part deleted.")
    else:
        print("Invalid option.")

def main():
    while True:
        print("\n1. Print PRODUCT and PART data")
        print("2. Update quantities")
        print("3. Modify a quantity")
        print("4. Manage PART table")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print_all_data()
        elif choice == '2':
            n = int(input("Enter a positive integer: "))
            update_quantities(n)
        elif choice == '3':
            print("1. Modify PRODUCT 'ABC'")
            print("2. Modify PART 'A', 'B', or 'C'")
            sub_choice = input("Enter your choice: ")
            if sub_choice == '1':
                modify_product()
            elif sub_choice == '2':
                modify_part()
            else:
                print("Invalid choice.")
        elif choice == '4':
            manage_part_table()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
cursor.close()
connection.close()
