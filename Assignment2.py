import mysql.connector
import re

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='change-me',
            database='test_database'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySql: {e}")
        return None

def ViewOutOfStock():
    print("Out of Stock Products")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductName FROM Products WHERE UnitsInStock = 0")
    for row in cursor:
        print(row)
    conn.close()

def ViewOrderNumPerCustomer():
    print("CustomerID, CustomerName, TotalOrders")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT c.CustomerID, c.CustomerName, COUNT(o.OrderID) AS TotalOrders FROM Customers c JOIN Orders o ON c.CustomerID = o.CustomerID GROUP BY c.CustomerID, c.CustomerName")
    for row in cursor:
        print(row)
    conn.close()

def ViewMostExpPerOrder():
    print("OrderID, ProductName, MaxUnitPrice")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT o.OrderID, p.ProductName, MAX(od.UnitPrice) AS MaxUnitPrice FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID JOIN Products p ON p.ProductID = od.ProductID GROUP BY o.OrderID, p.ProductName")
    for row in cursor:
        print(row)
    conn.close()

def ViewNeverOrdered():
    print("Never Ordered Product")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductName FROM Products LEFT JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID WHERE OrderDetails.ProductID IS NULL")
    for row in cursor:
        print(row)
    conn.close()

def ViewTotalRevPerSupplier():
    print("SupplierID, SupplierName, TotalRevenue")
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT s.SupplierID, s.SupplierName, SUM(od.UnitPrice * od.Quantity) AS TotalRevenue FROM Suppliers s JOIN Products p ON s.SupplierID = p.SupplierID JOIN OrderDetails od ON p.ProductID = od.ProductID GROUP BY s.SupplierID, s.SupplierName")
    for row in cursor:
        print(row)
    conn.close()

def AddNewOrder(CustomerID, OrderDate, ShipDate, ShipAddress, ShipCity, ShipPostalCode, ShipCountry, ProductID, Quantity, UnitPrice):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.callproc("AddNewOrder", (CustomerID, OrderDate, ShipDate, ShipAddress, ShipCity, ShipPostalCode, ShipCountry, ProductID, Quantity, UnitPrice))
    cursor.callproc("UpdateStockQuantity", (ProductID, Quantity))
    conn.commit()

# The program
while True:
    print("\nOptions")
    print("1. View Out of Stock Products")
    print("2. View Total Number of Orders Per Customer")
    print("3. View Most Expensive Product Details Per Order")
    print("4. View Products that have Never Been Ordered")
    print("5. View Total Revenue Per Supplier")
    print("6: Add New Order")
    print("7: Quit")
    try:
        option = float(input("Select an option: "))

        if option == 1:
            ViewOutOfStock()
        elif option == 2:
            ViewOrderNumPerCustomer()
        elif option == 3:
            ViewMostExpPerOrder()
        elif option == 4:
            ViewNeverOrdered()
        elif option == 5:
            ViewTotalRevPerSupplier()
        elif option == 6:
            customer_id = input("Enter Customer ID: ")
            while not re.match("^\d+$", customer_id):
                print("Customer ID should be a positive integer.")
                customer_id = input("Enter Customer ID: ")

            order_date = input("Enter Order Date (YYYY-MM-DD): ")
            while not re.match("^\d{4}-\d{2}-\d{2}$", order_date):
                print("Order Date should be in the format YYYY-MM-DD.")
                order_date = input("Enter Order Date (YYYY-MM-DD): ")

            ship_date = input("Enter Ship Date (YYYY-MM-DD): ")
            while not re.match("^\d{4}-\d{2}-\d{2}$", ship_date):
                print("Ship Date should be in the format YYYY-MM-DD.")
                ship_date = input("Enter Order Date (YYYY-MM-DD): ")

            ship_address = input("Enter Ship Address: ")
            while not re.match("^[a-zA-Z0-9\s,'-]*$", ship_address):
                print("Ship Address should only contain letters, numbers, spaces, commas, apostrophes, and hyphens.")
                ship_address = input("Enter Ship Address: ")

            ship_city = input("Enter Ship City: ")
            while not re.match("^[a-zA-Z\s]*$", ship_city):
                print("Ship City should only contain letters and spaces.")
                ship_city = input("Enter Ship City: ")

            ship_postal_code = input("Enter Ship Postal Code: ")
            while not re.match("^[a-zA-Z0-9\s]*$", ship_postal_code):
                print("Ship Postal Code should only contain letters, numbers, and spaces.")
                ship_postal_code = input("Enter Ship Postal Code: ")

            ship_country = input("Enter Ship Country: ")
            while not re.match("^[a-zA-Z\s]*$", ship_country):
                print("Ship Country should only contain letters and spaces.")
                ship_country = input("Enter Ship Country: ")

            product_id = input("Enter Product ID: ")
            while not re.match("^\d+$", product_id):
                print("Product ID should be a positive integer.")
                product_id = input("Enter Product ID: ")

            quantity = input("Enter Quantity: ")
            while not re.match("^\d+$", quantity):
                print("Quantity should be a positive integer.")
                quantity = input("Enter Quantity: ")

            unit_price = input("Enter Unit Price: ")
            while not re.match("^\d+(\.\d{1,2})?$", unit_price):
                print("Unit Price should be a positive decimal number with up to 2 decimal places.")
                unit_price = input("Enter Unit Price: ")

            AddNewOrder(customer_id, order_date, ship_date, ship_address, ship_city, ship_postal_code, ship_country, product_id, quantity, unit_price)
        elif option == 7:
            print("Goodbye")
            quit()
        else:
            print("Invalid Input")

    except ValueError:
        print("Invalid Input")

