from flask import Flask, render_template, request
from rules import ExpertSystem
from facts import Component, Result

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    try:
        voltage = float(request.form['voltage'])
        temperature = float(request.form['temperature'])
        resistance = float(request.form['resistance'])
    except ValueError:
        return render_template('index.html', error='Введите числовые значения')

    params = {'voltage': voltage, 'temperature': temperature, 'resistance': resistance}

    engine = ExpertSystem()
    engine.reset()
    engine.declare(Component(**params))
    engine.run()

    results = [f for f in engine.facts.values() if isinstance(f, Result)]

    if not results:
        result = {'status': 'Годен', 'reason': 'Все параметры в норме'}
    else:
        # Приоритет: Брак, затем Требуется доп проверка
        brak = next((r for r in results if r.get('status') == 'Брак'), None)
        if brak:
            result = brak
        else:
            result = results[0]

    return render_template('index.html', result=result, params=params)


if __name__ == '__main__':
    app.run(debug=True)