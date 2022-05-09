def checksum(data, sum=0):
    #forma as palavras de 16 bits a partir do pacote, e soma elas
    for i in range(0,len(data),2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    #pega somente os 16 bits da soma e adiciona o overflow
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    #faz o complemento do resultado
    sum = ~sum

    #retorna em binário
    return sum & 0xFFFF

