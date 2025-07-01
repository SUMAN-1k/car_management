import bcrypt
from database import connect_db

def registeruser(name,email,password):
    conn=connect_db()
    cursor=conn.cursor()
    try:
        hashed_pw=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        cursor.execute("insert into users (name,email,password) values (?,?,?)",(name,email,hashed_pw))
        conn.commit()
        print("✅ Registration successful.")
    except Exception as e:
        print("⚠️ Error:", e)
    finally:
        conn.close()


def loginuser(email,password):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id, name, email, password, is_admin FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_hashed_pw=user[3]
        if bcrypt.checkpw(password.encode('utf-8'),stored_hashed_pw):
            return user
        
    return None

def listcars():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE available=1")
    cars = cursor.fetchall()
    conn.close()
    return cars


def addcar(brand,model,price):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("insert into cars (brand,model,price_per_day) values (?,?,?)",(brand,model,price))
    conn.commit()
    cursor.close()

def bookcar(user_id,car_id,start_date,end_date,total_cost):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("insert into bookings (user_id,car_id,start_date,end_date,total_cost) values (?,?,?,?,?)",(user_id,car_id,start_date,end_date,total_cost))
    conn.commit()
    cursor.close()

def cancel(bookingid):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("select car_id from bookings where id=?",(bookingid,))
    result=cursor.fetchone()

    if result:
        car_id=result[0]

        cursor.execute("delete from bookings where id=?",(car_id,))
        conn.commit()
        print("✅ Booking cancelled and car marked available.")
    else:
        print("❌ Booking not found.")
    conn.close()