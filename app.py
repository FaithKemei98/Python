from flask import *
import pymysql
app = Flask(__name__)
app.config['SECRET_key'] = "helloworld1"



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']


        if  ' ' not in name :
            return render_template('signup.html', message = 'You should enter two names')
        elif '@' not in email:
            return render_template('signup.html', message='Invalid Email')
        elif len(password) < 4:
            render_template('signup.html', message='Password is too short')
        elif password != confirm:
            return render_template('signup.html', message='Passwords do not match')
        else:
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='female world')
            sql = "INSERT INTO `users`( `Name`, `Email`, `Password`) VALUES (%s,%s,%s)"

            cursor = connection.cursor()

            try:
                cursor.execute(sql, (name, email, password))
                connection.commit()
            except:
                connection.rollback()
                return render_template('signup.html', message='Error occurred')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='female world')
        sql = "SELECT * FROM `users` WHERE email=%s and password=%s"

        cursor = connection.cursor()
        cursor.execute(sql, (email, password))

        if cursor.rowcount == 0:
            return render_template('login.html', message="Invalid Login!")

        elif cursor.rowcount == 1:
            return redirect(url_for('/home'))

        else:
            return render_template('login.html', message="Invalid Login!")
    return render_template('login.html')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()

