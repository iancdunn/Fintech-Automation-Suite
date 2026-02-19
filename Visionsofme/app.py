from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import check_password_hash, generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'visionsofme.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'visionsofmeasaquant'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)

    needs_bal = db.Column(db.Float, default = 0.0)
    savings_bal = db.Column(db.Float, default = 0.0)
    wants_bal = db.Column(db.Float, default = 0.0)

    needs_pct = db.Column(db.Float, default = 50.0)
    savings_pct = db.Column(db.Float, default = 30.0)
    wants_pct = db.Column(db.Float, default = 20.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    type = db.Column(db.String(10))
    category = db.Column(db.String(7))
    amount = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime, default = datetime.now())

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username = username).first():
            flash('Username already exists.')
            return redirect(url_for('signup'))
        
        new_user = User(username = username, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username = username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        
        flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    transactions = Transaction.query.filter_by(user_id = current_user.id).order_by(Transaction.date.desc()).limit(10).all()
    return render_template('index.html', transactions = transactions)

@app.route('/update_settings', methods = ['POST'])
@login_required
def update_settings():
    if not request.form.get('needs_bal'):
        pass
    else:
        current_user.needs_bal = float(request.form.get('needs_bal'))
    if not request.form.get('savings_bal'):
        pass
    else:
        current_user.savings_bal = float(request.form.get('savings_bal'))
    if not request.form.get('wants_bal'):
        pass
    else:
        current_user.wants_bal = float(request.form.get('wants_bal'))

    if not request.form.get('needs_pct'):
        pass
    else:
        current_user.needs_pct = float(request.form.get('needs_pct'))
    if not request.form.get('savings_pct'):
        pass
    else:
        current_user.savings_pct = float(request.form.get('savings_pct'))
    if not request.form.get('wants_pct'):
        pass
    else:
        current_user.wants_pct = float(request.form.get('wants_pct'))

    if(current_user.needs_bal < 0 or current_user.savings_bal < 0 or current_user.wants_bal < 0):
        flash('Balances must not be negative.')
    elif(not (0 <= current_user.needs_pct <= 100) or not (0 <= current_user.savings_pct <= 100) or not 
         (0 <= current_user.wants_pct <= 100)):
        flash('Percentages must be between 0% and 100%.')
    elif(current_user.needs_pct + current_user.savings_pct + current_user.wants_pct != 100):
        flash('Percentages must add up to 100%.')
    else:
        db.session.commit()
        flash('Successfully updated settings.')
        
    return redirect(url_for('home'))

@app.route('/add_transaction', methods = ['POST'])
@login_required
def add_transaction():
    t_type = request.form.get('type')
    category = request.form.get('category')

    if not request.form.get('amount'):
        flash('Please enter a transaction amount.')
        return redirect(url_for('home'))
    else:
        amount = float(request.form.get('amount'))

    if amount <= 0:
        flash('Transaction amounts must be positive.')
        return redirect(url_for('home'))
    elif t_type == 'Deposit':
        current_user.needs_bal += round(amount * current_user.needs_pct / 100, 2)
        current_user.savings_bal += round(amount * current_user.savings_pct / 100, 2)
        #Ensures no money is lost or gained from rounding
        current_user.wants_bal += (amount - round(amount * current_user.needs_pct / 100, 2) - 
                                   round(amount * current_user.savings_pct / 100, 2))
        new_tx = Transaction(user_id = current_user.id, type = 'Deposit', category = '', amount = amount)
    else:
        if category == 'Needs':
            current_user.needs_bal -= amount
        elif category == 'Savings':
            current_user.savings_bal -= amount
        elif category == 'Wants':
            current_user.wants_bal -= amount
        new_tx = Transaction(user_id = current_user.id, type = 'Withdrawal', category = category, amount = amount)

    db.session.add(new_tx)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete_transaction/<int:id>')
@login_required
def delete_transaction(id):
    tx = Transaction.query.get_or_404(id)
    
    if tx.user_id != current_user.id:
        return redirect(url_for('home'))
    
    if tx.type == 'Deposit':
        current_user.needs_bal -= round(tx.amount * current_user.needs_pct / 100, 2)
        current_user.savings_bal -= round(tx.amount * current_user.savings_pct / 100, 2)
        current_user.wants_bal -= (tx.amount - round(tx.amount * current_user.needs_pct / 100, 2) - 
                                   round(tx.amount * current_user.savings_pct / 100, 2))
    else:
        if tx.category == 'Needs':
            current_user.needs_bal += tx.amount
        elif tx.category == 'Savings':
            current_user.savings_bal += tx.amount
        elif tx.category == 'Wants':
            current_user.wants_bal += tx.amount

    db.session.delete(tx)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/reset_data', methods = ['POST'])
@login_required
def reset_data():
    current_user.needs_bal = 0
    current_user.savings_bal = 0
    current_user.wants_bal = 0
    current_user.needs_pct = 50
    current_user.savings_pct = 30
    current_user.wants_pct = 20
    Transaction.query.filter_by(user_id = current_user.id).delete()

    db.session.commit()
    return {"status": "success"}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)