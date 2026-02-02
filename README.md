# 🌌 Haze Nexus Bot

O **Haze Nexus** é um bot de entretenimento e utilidade para Discord, desenvolvido em Python. Ele integra um sistema de economia robusto (Hazium), jogos interativos com punições de tempo real e inteligência artificial via Google Gemini.

---

## 🚀 Funcionalidades Principal

* **💰 Economia (Hazium):** Sistema de saldo salvo em banco de dados SQLite, com ranking global e comandos de administração.
* **🎮 Jogos Interativos:** * **Pedra, Papel e Tesoura:** Desafie o bot e ganhe moedas ou sofra um *timeout* de 1 minuto se perder.
    * **Roleta Russa:** Um jogo de alto risco onde a derrota resulta em perda de saldo e silenciamento automático.
* **🤖 Inteligência Artificial:** Integração com o Google Gemini para conversas naturais via comando `hz!chat`.
* **🧹 Moderação:** Comandos para limpeza de chat e gerenciamento de mensagens.
* **⚡ Punições Dinâmicas:** Sistema automático de `timeout` (castigo) integrado aos resultados dos jogos.

---

## 🛠️ Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [Discord.py](https://discordpy.readthedocs.io/) - API para interação com o Discord.
* [SQLite3](https://www.sqlite.org/) - Banco de dados relacional leve para armazenamento local.
* [Google Generative AI](https://ai.google.dev/) - Motor de IA (Gemini).
* [Dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente.

---

## 📋 Comandos Disponíveis

| Comando | Descrição | Permissão |
| :--- | :--- | :--- |
| `hz!help` | Exibe o menu de ajuda interativo. | Todos |
| `hz!status` | Mostra o saldo de Hazium do usuário. | Todos |
| `hz!top` | Ranking dos 10 usuários mais ricos. | Todos |
| `hz!games [1/2]` | Inicia jogos (1: PPT, 2: Roleta Russa). | Todos |
| `hz!chat [msg]` | Conversa com a IA do bot. | Todos |
| `hz!clean [qtd]` | Apaga mensagens do canal. | Gerenciar Mensagens |
| `hz!doar [user] [v]` | Adiciona/Remove Hazium de um usuário. | Administrador |
| `hz!mention [n] [u]` | Realiza spam de menções (uso moderado). | Administrador |

---

## 🔧 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/haze-nexus-bot.git](https://github.com/seu-usuario/haze-nexus-bot.git)
   ```
2.  **Crie e ative o ambiente virtual:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # venv\Scripts\activate   # Windows
  ```

3. **Instale as dependências:
Bash**
```bash
pip install -r requirements.txt
```

4. **Configure o arquivo .env: Crie um arquivo chamado .env na raiz e adicione suas chaves:**
Snippet de código
```env
DISCORD_TOKEN=seu_token_aqui
GIMINI_TOKEN=sua_chave_gemini_aqui
```

**Execute o bot:** Bash
```bash
python main.py
```

# ⚖️ Licença

- Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes.

- Desenvolvido com ☕ e Python por Rubens.# bot
