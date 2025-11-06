# Explicando o regex
# \. → começa com ponto
# [A-G] → primeira letra do acorde (C, D, E, etc.)
# [#b]? → opcional sustenido ou bemol
# [a-zA-Z0-9]* → aceita sufixos tipo m, maj7, sus4...
# @ → final obrigatório (delimitador seguro)
import re

padrao_acorde = r"\.[A-G][#b]?[a-zA-Z0-9]*@"

def encontrar_acordes(letra):
    acordes = re.findall(padrao_acorde, letra)
    return acordes

def limpar_letra(letra):
    letra_limpa =  re.sub(padrao_acorde, "", letra)
    return letra_limpa
    
def montar_cifra(letra):
    linha_acordes = ""
    linha_letra = ""
    pos = 0  # posição atual na string

    for match in re.finditer(padrao_acorde, letra):
        acorde = match.group()[1:-1]  # remove "." e "@"
        start = match.start()

        # adiciona espaços até o ponto onde o acorde aparece
        linha_acordes += " " * (start - pos) + acorde
        pos = match.end()
    linha_letra = re.sub(padrao_acorde, "", letra).strip()

    return f"{linha_acordes}\n{linha_letra}"


