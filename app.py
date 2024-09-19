from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
def home():
    reviews = Review.query.order_by(Review.date_posted.desc()).all()
    return render_template('home.html', reviews=reviews)


@app.route('/post', methods=['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        course_name = request.form['course_name']
        content = request.form['content']
        new_review = Review(course_name=course_name, content=content)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post_review.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = Review.query.filter(Review.course_name.contains(search_term)).all()
        return render_template('search_results.html', results=results)
    return render_template('search.html')


@app.route('/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)