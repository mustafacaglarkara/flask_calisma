from flask import Flask,session,redirect,url_for,render_template,request,flash
from .helpers import sessionHelpers
from .models import db,User,Question

app= Flask(__name__)
app.secret_key = 'kdmdfsdfR45345^+_TTRE='  # Flash mesajlar için gerekli
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kodlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#@app.before_request
#def create_tables():
#    db.create_all()
#    print("Veritabanı tabloları oluşturuldu.")

@app.route("/", methods=['GET', 'POST'])
def index():
    context = {}
    if sessionHelpers.checkSession():
        user = User.query.filter_by(username=session['user_id']).first()
        questions = Question.query.all()
        context["user"] = user
        context["questions"] = questions

        if request.method == 'POST':
            score = 0
            for question in questions:
                selected_option = request.form.get(f'question_{question.id}')
                if selected_option and int(selected_option) == question.correct_option:
                    score += 1

            context["score"] = score
            context["total_questions"] = len(questions)
            print(score)
            return render_template("index.html", **context)

        return render_template("index.html", **context)
    else:
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Veritabanından kullanıcıyı bul
        user = User.query.filter_by(username=username,password=password).first()

        # Kullanıcıyı kontrol et ve şifreyi doğrula
        if user :
            session['user_id'] = user.id
            session['username'] = user.username
            # Giriş başarılıysa index sayfasına yönlendir
            return redirect(url_for('index'))
        else:
            # Giriş başarısızsa hata mesajı göster
            flash('Yanlış kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')  # GET isteği için login sayfasını render et
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()  # Session'ı temizle
    return redirect(url_for('login'))  # Login sayfasına yönlendir

@app.route("/test")
def test_prog():

    # Kullanıcı eklemek
    new_user = User(username='testuser', email='testuser@example.com',password="kodland")
    db.session.add(new_user)
    db.session.commit()

    # Soru eklemek
    new_question = Question(question_text='What is Flask?', option1='A web framework', option2='A database',
                            option3='An API', correct_option=1)
    db.session.add(new_question)
    db.session.commit()
    return "First records installed"

if __name__ == "__main__":
    #with app.app_context():
        #db.create_all()  # Veritabanı tablolarını oluşturur
    app.run(debug=True)