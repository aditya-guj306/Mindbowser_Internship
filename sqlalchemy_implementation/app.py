from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:adi1202@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy()
db.init_app(app)

post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    bio = db.Column(db.Text)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tag "{self.name}">' 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment',backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')
    def __repr__(self):
        return f'<Post "(self.title)">'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'  
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'    


with app.app_context():
    db.create_all()
    

@app.route('/')
def index():
    students = Student.query.all()
    posts = Post.query.all()
    # employees = Employee.query.all()
    # return render_template('index.html', students=students,posts=posts,employees=employees)
    page = request.args.get('page', 1, type=int)
    pagination = Employee.query.order_by(Employee.first_name).paginate(page=page, per_page=1)
    return render_template('index.html', students=students,posts=posts,pagination=pagination)    

      

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(first_name=firstname,
                          last_name=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.first_name = firstname
        student.last_name = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/', methods=('GET', 'POST'))
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment = Comment(content=request.form['content'],post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post',post_id=post.id))
    
    return render_template('post.html',post=post)
@app.route('/comments/')
def comments():
    comments=Comment.query.order_by(Comment.id.desc()).all()
    return render_template('comment.html',comments=comments)

@app.post('/comments/<int:comment_id>/delete')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post',post_id=post_id))

@app.route('/tags/<tag_name>/')
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    return render_template('tag.html', tag=tag)


if __name__ == '__main__':
    app.run(debug=True)