from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User, Book
from forms import LoginForm, RegistrationForm, BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

# Ensure database tables are created
with app.app_context():
    db.create_all()
    
@app.route('/contact')
def contact():
    return render_template('contact_services_events.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form, error="Invalid credentials")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    total_books = Book.query.count()
    total_users = User.query.count()
    return render_template('dashboard.html', total_books=total_books, total_users=total_users)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'role' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, year=form.year.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('view_books'))
    return render_template('add_book.html', form=form)

@app.route('/view_books')
def view_books():
    books = Book.query.all()
    return render_template('view_books.html', books=books)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'role' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        db.session.commit()
        return redirect(url_for('view_books'))
    return render_template('edit_book.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        results = Book.query.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Book.author.ilike(f'%{query}%')) |
            (Book.year.ilike(f'%{query}%'))
        ).all()
        return render_template('view_books.html', books=results)
    return render_template('search.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
# This code is a Flask application that provides a library management system with user authentication, book management, and search functionality.
# It uses SQLAlchemy for database interactions and Flask-WTF for form handling.