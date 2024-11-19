from django.conf import settings
from django.shortcuts import render
from .utils import generar_arbol_grafico
import os
import re

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
    
    if request.method == 'POST':
        expresion = request.POST.get('expresion', '')
        resultado = calcular(expresion)
        
        if resultado != "Error":
            try:
                dot = generar_arbol_grafico(expresion)
                # Crear nombre único para la imagen
                nombre_archivo = f'arbol_{hash(expresion)}'
                # Ruta absoluta para guardar la imagen
                ruta_static = os.path.join(settings.BASE_DIR, 'calc', 'static', 'calc')
                # Asegurarse de que el directorio existe
                os.makedirs(ruta_static, exist_ok=True)
                # Ruta completa del archivo
                ruta_imagen = os.path.join(ruta_static, f'{nombre_archivo}')
                # Generar la imagen
                dot.render(ruta_imagen, format='png', cleanup=True)
                # URL para la plantilla
                imagen_arbol = f'calc/{nombre_archivo}.png'
                print(f"Imagen generada en: {ruta_imagen}.png")
            except Exception as e:
                print(f"Error al generar árbol: {e}")
    
    return render(request, 'calc/calculadora.html', {
        'resultado': resultado,
        'imagen_arbol': imagen_arbol
    })
