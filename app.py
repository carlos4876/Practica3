from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'inscritos' in session and len(session['inscritos']) > 0:
        return max(item['id'] for item in session['inscritos']) + 1
    return 1

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'inscritos' not in session:
        session['inscritos'] = []
    
    if request.method == 'POST':
        seminarios_seleccionados = request.form.getlist('seminarios')
        nuevo_inscrito = {
            'id': generar_id(),
            'fecha': request.form['fecha'],
            'nombre': request.form['nombre'],
            'apellidos': request.form['apellidos'],
            'turno': request.form['turno'],
            'seminarios': ', '.join(seminarios_seleccionados)
        }
        
        session['inscritos'].append(nuevo_inscrito)
        session.modified = True
        return redirect(url_for('lista_inscritos'))
    
    return render_template('index.html')

@app.route("/lista")
def lista_inscritos():
    if 'inscritos' not in session:
        session['inscritos'] = []
    inscritos = session.get('inscritos', [])
    return render_template('lista_inscritos.html', inscritos=inscritos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    lista_inscritos = session.get('inscritos', [])
    inscrito = next((i for i in lista_inscritos if i['id'] == id), None)
    
    if not inscrito:
        return redirect(url_for('lista_inscritos'))
    
    if request.method == 'POST':
        seminarios_seleccionados = request.form.getlist('seminarios')
        inscrito['fecha'] = request.form['fecha']
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellidos'] = request.form['apellidos']
        inscrito['turno'] = request.form['turno']
        inscrito['seminarios'] = ', '.join(seminarios_seleccionados)
        session.modified = True
        return redirect(url_for('lista_inscritos'))
    
    return render_template('editar.html', inscrito=inscrito)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    lista_inscritos = session.get('inscritos', [])
    inscrito = next((i for i in lista_inscritos if i['id'] == id), None)
    
    if inscrito:
        session['inscritos'].remove(inscrito)
        session.modified = True
    
    return redirect(url_for('lista_inscritos'))

if __name__ == "__main__":
    app.run(debug=True)