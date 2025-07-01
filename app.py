from flask import Flask,render_template,request,redirect,session,url_for
from models import registeruser, loginuser, listcars, addcar, bookcar, cancel
from utils import calculatedays
from database import initialize_db, connect_db

app=Flask(__name__)
app.secret_key='supersecretkey'

initialize_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email = request.form['email']
        pw = request.form['password']
        registeruser(name, email, pw)
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        user = loginuser(email, pw)
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['is_admin'] = user[4]
            if user[4] == 1:
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        else:
            return "❌ Invalid credentials."
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    message = None

    if request.method == 'POST':
        if 'booking_id' in request.form:
            booking_id = request.form['booking_id']
            cancel(booking_id)
            message = "❌ Booking cancelled successfully"

    cars = listcars()
    return render_template("dashboard.html", cars=cars, user=session['user_name'], message=message)



@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        return redirect('/')
    car_id = int(request.form['car_id'])
    start = request.form['start']
    end = request.form['end']
    days = calculatedays(start, end)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT price_per_day FROM cars WHERE id=?", (car_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        total = row[0] * days
        bookcar(session['user_id'], car_id, start, end, total)
        session['message'] = f"✅ Car booked for {days} days. Total ₹{total}"
        return redirect(url_for('dashboard'))

    session['message'] = "❌ Invalid Car ID"
    return redirect(url_for('dashboard'))


@app.route('/cancel', methods=['POST'])
def cancel_booking():
    bookingid = int(request.form['booking_id'])
    cancel(bookingid)
    return "✅ Booking canceled."


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect('/login')

    conn = connect_db()
    cursor = conn.cursor()

    # POST = add a new car
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = float(request.form['price'])
        cursor.execute("INSERT INTO cars (brand, model, price_per_day) VALUES (?, ?, ?)",
                       (brand, model, price))
        conn.commit()
        session['message'] = "✅ Car added successfully!"
        return redirect(url_for('admin'))
    # Get all bookings
    cursor.execute("""
        SELECT bookings.id, users.name, cars.brand || ' ' || cars.model, start_date, end_date, total_cost 
        FROM bookings 
        JOIN users ON bookings.user_id = users.id 
        JOIN cars ON bookings.car_id = cars.id
    """)
    bookings = cursor.fetchall()
    conn.close()

    return render_template("admin.html", bookings=bookings)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



if __name__ == '__main__':
    app.run(debug=True)