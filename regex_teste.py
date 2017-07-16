import re
texto = 'qual avenida Recife, ein ? , teste'
rua_regex = re.search('rua (\w|\s)+', texto)
avenida_regex = re.search('avenida (\w|\s)+', texto)
avenida = avenida_regex.group()
print(avenida)
