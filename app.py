from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reports')
def reports():
    articles = Article.query.all()
    return render_template('reports.html',  articles=reversed(articles))

@app.route('/reports/<int:id>')
def report_detail(id):
    article = Article.query.get(id)
    return render_template('report_detail.html',  article=article)

@app.route('/reports/<int:id>/del')
def report_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/reports')
    except:
        return "Ошибка"



@app.route('/createReport', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = Article(title = title, text = text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/reports')
        except:
            return "Ошибка"
    else:
        return render_template('createReport.html')




if __name__ == "__main__":
    app.run(debug=True)