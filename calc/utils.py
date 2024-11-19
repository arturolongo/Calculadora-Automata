class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolExpresion:
    def __init__(self):
        self.operadores = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def construir_arbol(self, expresion):
        tokens = self._tokenizar(expresion)
        return self._construir_arbol_recursivo(tokens)
    
    def _tokenizar(self, expresion):
        tokens = []
        numero = ''
        for char in expresion:
            if char.isdigit() or char == '.':
                numero += char
            else:
                if numero:
                    tokens.append(numero)
                    numero = ''
                if char in self.operadores:
                    tokens.append(char)
        if numero:
            tokens.append(numero)
        return tokens
    
    def _construir_arbol_recursivo(self, tokens):
        if not tokens:
            return None
        
        # Buscar el operador con menor precedencia
        min_precedencia = float('inf')
        operador_idx = -1
        
        for i, token in enumerate(tokens):
            if token in self.operadores:
                if self.operadores[token] <= min_precedencia:
                    min_precedencia = self.operadores[token]
                    operador_idx = i
        
        if operador_idx == -1:
            # Es un número
            return Nodo(tokens[0])
        
        nodo = Nodo(tokens[operador_idx])
        nodo.izquierda = self._construir_arbol_recursivo(tokens[:operador_idx])
        nodo.derecha = self._construir_arbol_recursivo(tokens[operador_idx + 1:])
        
        return nodo

def generar_arbol_grafico(expresion):
    import graphviz
    
    arbol = ArbolExpresion()
    raiz = arbol.construir_arbol(expresion)
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')
    
    def agregar_nodos(nodo, id_padre=None):
        if not nodo:
            return
        
        id_actual = str(id(nodo))
        dot.node(id_actual, str(nodo.valor))
        
        if id_padre:
            dot.edge(id_padre, id_actual)
        
        agregar_nodos(nodo.izquierda, id_actual)
        agregar_nodos(nodo.derecha, id_actual)
    
    agregar_nodos(raiz)
    return dot 