from django.conf import settings
from django.shortcuts import render
from .utils import generar_arbol_grafico
from .lexer import CalculadoraLexer
from .models import Operacion
import os
import re
import json

def calcular(expresion):
    try:
        # Limpiamos la expresión de espacios y validamos caracteres permitidos
        expresion = expresion.replace(' ', '')
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s]*$', expresion):
            return "Error: Caracteres no válidos"
        
        resultado = eval(expresion)
        
        if isinstance(resultado, float):
            if resultado.is_integer():
                return str(int(resultado))
            return f"{resultado:.2f}"
        return str(resultado)
    except Exception as e:
        return "Error"

def calculadora(request):
    resultado = None
    imagen_arbol = None
    tokens_info = None
    
    if request.method == 'POST':
        expresion = request.POST.get('expresion', '')
        accion = request.POST.get('accion', 'calcular')
        
        if accion == 'ms':
            # Guardar en memoria
            try:
                valor = float(expresion)
                Operacion.objects.create(
                    expresion='MS',
                    resultado=valor,
                    memoria=valor
                )
                resultado = expresion
            except ValueError:
                resultado = "Error"
        else:
            # Procesar expresión
            lexer = CalculadoraLexer()
            lexer.build()
            tokens = lexer.tokenize(expresion)
            
            # Modificar esta parte para dar formato a los tokens
            lista_tokens = []
            for token in tokens:
                tipo = "Número" if token.type == 'NUMERO' else "Operador"
                lista_tokens.append({
                    'valor': token.value,
                    'tipo': tipo
                })
            
            tokens_info = {
                'lista_tokens': lista_tokens,
                'total_numeros': lexer.contador_tokens['numeros'],
                'total_operadores': lexer.contador_tokens['operadores']
            }
            
            # Agregar este print para debug
            print("Tokens Info:", json.dumps(tokens_info, indent=2))
            
            resultado = calcular(expresion)
            
            if resultado != "Error":
                try:
                    dot = generar_arbol_grafico(expresion)
                    nombre_archivo = f'arbol_{hash(expresion)}'
                    imagen_arbol = f'calc/{nombre_archivo}.png'
                    dot.render(f'calc/static/calc/{nombre_archivo}', format='png', cleanup=True)
                except Exception as e:
                    print(f"Error al generar árbol: {e}")
    
    return render(request, 'calc/calculadora.html', {
        'resultado': resultado,
        'imagen_arbol': imagen_arbol,
        'tokens_info': json.dumps(tokens_info) if tokens_info else None
    })
