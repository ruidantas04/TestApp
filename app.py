import os
from flask import Flask, render_template, request
app = Flask(__name__)


def calcular_contraposta(aposta_inicial, odd_inicial, odd_contra):
    potencial_ganho = aposta_inicial * odd_inicial
    aposta_contra = potencial_ganho / odd_contra
    total_apostado = aposta_inicial + aposta_contra
    lucro_inicial = potencial_ganho - total_apostado
    lucro_contra = (aposta_contra * odd_contra) - total_apostado
    return round(aposta_contra, 2), round(lucro_inicial, 2), round(lucro_contra, 2)

def calcular_melhor_odd_contra(aposta_inicial, odd_inicial):
    potencial_ganho = aposta_inicial * odd_inicial
    melhor_odd = None
    melhor_lucro = float("-inf")
    melhor_aposta_contra = 0

    for odd_contra in [x / 100 for x in range(101, 401)]:  # Odds de 1.01 a 4.00
        aposta_contra = potencial_ganho / odd_contra
        total_apostado = aposta_inicial + aposta_contra
        lucro = (aposta_contra * odd_contra) - total_apostado

        if lucro > melhor_lucro:
            melhor_lucro = lucro
            melhor_odd = odd_contra
            melhor_aposta_contra = aposta_contra

    return round(melhor_odd, 2), round(melhor_aposta_contra, 2), round(melhor_lucro, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    melhor = None
    if request.method == "POST":
        aposta_inicial = float(request.form["aposta_inicial"])
        odd_inicial = float(request.form["odd_inicial"])
        odd_contra = request.form.get("odd_contra")

        if odd_contra:
            odd_contra = float(odd_contra)
            aposta_contra, lucro_inicial, lucro_contra = calcular_contraposta(
                aposta_inicial, odd_inicial, odd_contra)
            resultado = {
                "aposta_contra": aposta_contra,
                "lucro_inicial": lucro_inicial,
                "lucro_contra": lucro_contra
            }

        melhor_odd, melhor_aposta_contra, melhor_lucro = calcular_melhor_odd_contra(
            aposta_inicial, odd_inicial)
        melhor = {
            "melhor_odd": melhor_odd,
            "melhor_aposta": melhor_aposta_contra,
            "melhor_lucro": melhor_lucro
        }

    return render_template("index.html", resultado=resultado, melhor=melhor)

app.run(debug=False, host='0.0.0.0', port=10000)
