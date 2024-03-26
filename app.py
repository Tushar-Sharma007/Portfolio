from flask import Flask,render_template,request,url_for,redirect
import sqlite3
app = Flask(__name__)

DATABASE = "trips.db"

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/about.html')
def aboutme():
    return render_template("about.html")

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trips (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, source TEXT, destination TEXT)''')
    conn.commit()
    conn.close()

create_table()
@app.route("/trip.html")
def trip():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM trips")
    trips = c.fetchall()
    conn.close()
    return render_template('trip.html', trips=trips)

@app.route("/add", methods=["POST"])
def add_trip():
    date = request.form['date']
    source = request.form['source']
    destination = request.form['destination']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO trips (date, source, destination) VALUES (?, ?, ?)", (date, source, destination))
    conn.commit()
    conn.close()
    return redirect(url_for('trip'))

@app.route('/remove/<int:id>')
def remove_trip(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM trips WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('trip'))
if __name__ == "__main__":
    app.run(debug=True)