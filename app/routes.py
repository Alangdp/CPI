from flask import request, redirect, flash ,url_for, render_template, g, session, make_response
import sqlite3, GetData, fundamentus
from Registro import *
from extras import *
from .controllers.userController import *

# Controllers
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)

def routes(app):
    @app.route('/home')
    def main():
        return render_template('main.html')

    @app.route('/', methods=['GET','POST'])
    @app.route('/ranking', methods=['GET','POST'])
    def ranking():
        return render_template('ranking.html',stock = Acoes, qt = quantidade, user = session['user'])
        
    # Registro
    @app.route('/registrar', methods=['GET'])
    def registrarIndex():
        return render_template('register.html', csrf_token = session['csrfToken'])

    @app.route('/registrar', methods=['POST'])
    def registrar():    
        json_dados = request.get_json()
        print(json_dados['action'] == 'registro', 'aki o print do action')
        if validaCSR(json_dados['csrfToken']):
            user = json_dados['usuario']
            email = json_dados['email']
            senha = json_dados['senha']
            cpf = json_dados['cpf']
            registrarDB(user,senha,email,cpf)

            return redirect('/login', code=302)
        else:
            redirect('/registrarIndex', code=304)

    #Login/Logout
    @app.route('/login', methods=['GET'])
    def loginPage():
        print(session['csrfToken'])
        return render_template('login.html', csrf_token = session['csrfToken'])

    @app.route('/login', methods=['POST'])
    def login():
        json_dados = request.get_json()
        if json_dados['action'] == 'login' and validaCSR(json_dados['csrfToken']):
            email = json_dados['email']
            senha = json_dados['senha']

            if logar(email, senha): return redirect('/ranking', code=302)
            else: return redirect(url_for('loginPage'), code=304)
        return redirect(url_for('loginPage'), code=304)

    @app.route('/logout', methods=['POST'])
    def logout():
        session['logged'] = 'False'
        session['user'] = None
        return redirect('login')

    @app.route('/home')
    def home():
        return render_template('home.html', user = session['user'])

    @app.route('/user', methods=['POST'])
    def userConfig():
        form = request.form
        if form['action'] == 'password':
            atualizarSenha(form['inputPasswordN'], form['inputPasswordA'], form['id'])
            return redirect('/user')
        if form['action'] == 'email':
            atualizarEmail(form['inputEmailN'], form['inputEmailA'],  form['id'] )
        return redirect('/user')

    @app.route('/user', methods=['GET'])
    def userIndexR():
        return userIndex()
    
    @app.route('/detalhes', methods=['GET','POST'])
    def detalhes():
        # valida ticker
        ticker = request.args.get('ticker')
        if ticker == None or ticker == '': validTicker =  "False"
        else: validTicker = isTicker(ticker)

        # coleta os dados para a página
        if validTicker == "True":
            stock = GetData.BasicData(ticker)
            datas = stock.Datas()
            tickerImg = stock.getImageDetalhes()
            fundamentalDatas = stock.fundamentalDatas()
            dy = stock.Dy()
            acoesEmitidas = fundamentalDatas['acoesEmitidas'].split('.')
            acoesEmitidas = float(fundamentalDatas['lucroLiquido']) / float(''.join(acoesEmitidas))
            fundamentalDatas['lucroLiquidoPorAcao'] = f'{acoesEmitidas:.2f}'
            print('FundamentalData',fundamentalDatas)
            print('Data',datas)
            print('Dy', dy)

        else:
            dy = []
            datas = []
            fundamentalDatas = []
            tickerImg = []

        return render_template('details.html', user = session['user'], valid = validTicker, ticker = ticker, data = datas, fundamentalData = fundamentalDatas, img = tickerImg, dy = dy)

    # Admin
    @app.route('/admin', methods=['GET', 'Post'])
    def admin():
        if request.method == 'POST':
            json_dados = request.get_json()

            if json_dados['action'] == 'admin':
                email = json_dados['email']
                senha = json_dados['senha']

                if email != 'admin@gmail.com' and senha != '(Alant34t)': return make_response(304)
                else:
                    session['admin'] = 'True'
                    return redirect(url_for('admin'))

            if json_dados['action'] == 'logoutAdmin':
                session['admin'] = 'False'
                return redirect(url_for('admin'))

        else:
            data = usuariosRegistrados()
            return render_template('admin.html', admin = session['admin'], data = data, qtd = len(data), permissoes = "Banido")

    @app.route('/error')
    def erroPage():
        { 'code': 'CSRFToken Inválido', 'message': 'CSRFToken Inválido'}
        erro = session['erro']['code']
        mensagem = session['erro']['message']

        return render_template('errorPage.html', erro = erro , mensagem = mensagem)

def init_routes(app):
    routes(app)