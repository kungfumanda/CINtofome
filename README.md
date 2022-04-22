# CINtofome
Projeto referente à disciplina Infraestrutura de Comunicações.

*Objetivo* \
\
Chatbot temático para restaurantes, implementado com programação básica para redes usando socket. Funcionando como um gerenciador de mesas, cliente faz o pedido diretamente pela conexão, pulando a necessidade um garçom e burocracia de pagamentos.

*Entregas*
- [X] Implementação de comunicação UDP comum e de uma função checksum.
- [X] Implementação de confiabilidade segundo o canal de transmissão confiável rdt3.0.
- [ ] Implementação do chatbot, exibido por linha de comando.

*Tecnologias:*
- Python
  - Biblioteca Socket
  - Módulo time

*Estrutura*
```
├── server.py
├── client.py
└── rdt
    ├── rdt.py
└── utils
    ├── checksum.py
```