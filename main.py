import mysql.connector
from datetime import datetime

# Connect to your MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="calorie_counter"
)
cursor = db.cursor()

def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("INSERT INTO user_list (username, password) VALUES (%s, %s)", (username, password))
    db.commit()

    cursor.execute(f"CREATE TABLE {username} (id INT AUTO_INCREMENT PRIMARY KEY, food VARCHAR(255), timestamp DATETIME, calorie INT)")
    db.commit()

    print("Sign up successful")

def signin():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM user_list WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone():
        return username
    else:
        print("Invalid username or password")
        return None

def add_food(username):
    food_item = input("Enter the food item: ")

    cursor.execute("SELECT * FROM food WHERE food_name = %s", (food_item,))
    food_record = cursor.fetchone()
    if food_record:
        calorie = food_record[2]

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"INSERT INTO {username} (food, timestamp, calorie) VALUES (%s, %s, %s)", (food_item, timestamp, calorie))
        db.commit()
        print("Food added successfully")
    else:
        print("Food item not found")

def see_table(username):
    cursor.execute(f"SELECT * FROM {username}")
    user_table = cursor.fetchall()

    print("User's Table:")
    for row in user_table:
        print(row)

    while True:
        print("\nOptions:")
        print("1. See maximum food with calories")
        print("2. See average calories consumed")
        print("3. See total calories consumed")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            cursor.execute(f"SELECT food, calorie FROM {username} WHERE calorie = (SELECT MAX(calorie) FROM {username})")
            max_min_food = cursor.fetchall()
            print("Food with maximum and minimum calories:")
            for food, calorie in max_min_food:
                print(f"{food}: {calorie} calories")
            pass
        elif choice == 2:
            cursor.execute(f"SELECT AVG(calorie) FROM {username}")
            average_calorie = cursor.fetchone()[0]
            print(f"Average calories consumed: {average_calorie:.2f} calories")
            pass
        elif choice == 3:
            cursor.execute(f"SELECT SUM(calorie) FROM {username}")
            total_calorie = cursor.fetchone()[0]
            print(f"Total calories consumed: {total_calorie} calories")
            pass
        elif choice == 4:
            break
        else:
            print("Invalid choice")

# Main program loop
while True:
    print("\nOptions:")
    print("1. Sign Up")
    print("2. Sign In")
    print("3. Exit")
    option = int(input("Enter your choice: "))

    if option == 1:
        signup()
    elif option == 2:
        username = signin()
        if username:
            while True:
                print("\nOptions:")
                print("1. Add food item")
                print("2. See your table")
                print("3. Log out")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    add_food(username)
                elif choice == 2:
                    see_table(username)
                elif choice == 3:
                    print("Logging out")
                    break
                else:
                    print("Invalid choice")
    elif option == 3:
        break
    else:
        print("Invalid choice")

# Close the database connection
cursor.close()
db.close()
