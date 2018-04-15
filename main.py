from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "ad6495c8da"
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1200))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route("/")
def home():
    return redirect("/blog")

@app.route('/blog', methods=['POST', 'GET'])
def index():


    posts = Blog.query.all()
    return render_template('index.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
        error = ""
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if len(title) != 0 and len(content) != 0:
                new_blog = Blog(title, content)
                db.session.add(new_blog)
                db.session.commit()
                flash("Post successful!")
                return redirect("/")
            else:
                if len(title) == 0:
                    error += " You must include a title!"
                if len(content) == 0:
                    error += " You must include a blog post!"
                return render_template("newpost.html", error=error, content=content, title=title)
        return render_template("newpost.html")

if __name__ == '__main__':
    app.run()
