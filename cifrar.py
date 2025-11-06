import re
import json

from padroes import encontrar_acordes, limpar_letra, montar_cifra
# na versao mobile, ao digitar . deve subir um menu
# ao mandar pro backend tem q ter algo que indique o acorde acabou,
# como um @ ou #
# no qual seleciona o acorde, que vão ser aqueles do Tom selecionado

letra = """
 .Em@once upon a time .C@not so long .D@ago
"""

acordes = encontrar_acordes(letra)
letra_limpa = limpar_letra(letra)
cifra_montada = montar_cifra(letra)
print(cifra_montada)

# print(json.dumps(composicao, indent=4))