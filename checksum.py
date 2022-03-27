
def checksumSend(file, cs):
    #le 2 bytes da file para formar palavras de 16 bits e as soma
    for i in range(0,len(file),2):
        if i + 1 >= len(file):
            cs += ord(file[i]) & 0xFF
        else:
            w = ((ord(file[i]) << 8) & 0xFF00) + (ord(file[i+1]) & 0xFF)
            cs += w

    #transforma a soma de 32 bits em 16 bits e lida com overflow
    while (cs >> 16) > 0:
        cs = (cs & 0xFFFF) + (cs >> 16)

    #faz o complemento do resultado
    cs = ~cs

    return cs & 0xFFFF

def checksumRecive(file, cs):
    for i in range(0,len(file),2):
        if i + 1 >= len(file):
            cs += ord(file[i]) & 0xFF
        else:
            w = ((ord(file[i]) << 8) & 0xFF00) + (ord(file[i+1]) & 0xFF)
            cs += w

    while (cs >> 16) > 0:
        cs = (cs & 0xFFFF) + (cs >> 16)

    #compara se a soma bateu (so tem numeros 1 no resultado em bit)
    if (cs == 0xFFFF):
        retorno = "Mensagem recebida por completo"
    else:
        retorno = "Dados perdidos no envio"
    return retorno


checksum = checksumSend('list\n', 0)
print (checksum)
recive = checksumRecive('list\n', checksum)
print (recive)

