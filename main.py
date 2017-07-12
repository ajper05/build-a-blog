from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog():
    
    id = request.args.get('id')
    if id == None:
        ids = Blog.query.all()
        return render_template('blogmain.html', pagetitle="Build A Blog", pagename="Build a Blog", ids=ids)
    else:
        post = Blog.query.get(id)
        return render_template('singlepost.html', pagetitle="B", pagename="Build a Blog", post=post)



@app.route('/newpost', methods=['GET', 'POST'])
def add_post():
    body_error = ""
    title_error = ""

    if request.method == 'POST':
        body = request.form['body']
        title = request.form['title']
        if len(body) == 0:
            body_error = "Please Enter Text"
        if len(title) == 0:
            title_error = "Please Add a Title"
        if title_error or body_error:
            return render_template('newposts.html',pagename="Create a New Post",title="Create a New Post",title_error=title_error,body_error=body_error)
        
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit() 

        return redirect('/blog')

    return render_template('newposts.html', pagename="Create a New Post", title="Create a New Post")


if __name__ == '__main__':
    app.run()
