
# Jogo de Quebra-Cabeça em Python

Este é um simples jogo de quebra-cabeça desenvolvido em Python usando a biblioteca Pygame. O jogador pode selecionar o nível de dificuldade e completar o quebra-cabeça movendo as peças até restaurar a imagem original.

## Funcionalidades

- **Seleção de Dificuldade:** Fácil (3x3), Normal (4x4), Difícil (5x5).
- **Temporizador:** Mostra o tempo decorrido durante o jogo.
- **Comemoração:** Mensagem e som de vitória ao completar o quebra-cabeça.
- **Botões de Controle na Tela de Vitória:**
  - **Jogar Novamente:** Reinicia o jogo com o mesmo nível de dificuldade.
  - **Voltar ao Menu:** Retorna à tela de seleção de dificuldade para escolher um novo nível.

## Como Jogar

1. Execute o script `puzzle.py`.
2. Selecione o nível de dificuldade clicando em "Fácil", "Normal" ou "Difícil".
3. Clique nas peças adjacentes ao espaço em branco para movê-las e tente restaurar a imagem original.
4. Ao completar o quebra-cabeça, a imagem será ocultada e uma mensagem de vitória será exibida junto com o tempo total decorrido.
5. Use os botões "Jogar Novamente" para tentar novamente ou "Voltar ao Menu" para escolher um novo nível de dificuldade.

## Requisitos

- Python 3.x
- Pygame
- Numpy

## Instalação

1. Clone este repositório para o seu ambiente local.
2. Instale os requisitos usando o comando:

```bash
pip install -r requirements.txt
```

## Executar o Jogo

Após instalar os requisitos, execute o jogo com o comando:

```bash
python puzzle.py
```

## Estrutura do Repositório

- `puzzle.py`: Código-fonte do jogo.
- `imagem.jpg`: Imagem utilizada para o quebra-cabeça.
- `README.md`: Instruções e informações sobre o jogo.
- `requirements.txt`: Lista de dependências do projeto.

## Créditos

Este jogo foi desenvolvido como uma demonstração de uso básico da biblioteca Pygame para criação de jogos em Python.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
