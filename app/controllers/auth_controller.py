from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import User
from app.utils import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../views')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.authenticate(username, password)
        if user:
            session['user'] = user.username
            return redirect(url_for('auth.index'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Preencha todos os campos.', 'danger')
        else:
            # Utiliza a orientação a objetos instanciando a classe e chamando save()
            new_user = User(id=None, username=username, password_hash=password)
            new_user.save()

    return render_template('register.html')

@auth_bp.route('/listadestaque', methods = ['GET', 'POST'])
def listar():
    if 'user' in session:
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        filme = request.form.get('filme')
        filme2 = request.form.get('filme2')

        new_filme = User(id=None, filme=filme, filme2=filme2)
        new_filme.save()
        return redirect(url_for('auth.index'))
        
@auth_bp.route('/index')
@login_required
def index():
    return render_template('index.html', username=session.get('user'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))