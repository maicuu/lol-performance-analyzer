# 🎮 LoL Performance Analyzer

Um analisador de estatísticas em tempo real para League of Legends construído em Python. Este script consome a **Riot Games API** (Account-V1 e Match-V5) para transformar dados brutos JSON em um dashboard de métricas focado em performance competitiva.

---

## 🎯 Motivação e Contexto

Este projeto foi desenvolvido como aplicação prática para consolidar os conhecimentos adquiridos nas formações da **Alura**:
- [cite_start]🏅 Python para Dados: Primeiros Passos [cite: 5]
- [cite_start]🏅 Imersão Dados com Python II [cite: 19]

O objetivo principal foi sair da teoria e aplicar lógica de programação, mineração de dados complexos e consumo de APIs REST em um cenário real. O projeto demonstra a capacidade de traduzir regras de negócio (neste caso, de E-sports) em código funcional e limpo, visando a preparação para novos e exigentes desafios no mercado de tecnologia em nível global.

## 🚀 Funcionalidades

- **Integração Real:** Consumo de endpoints oficiais da Riot Games, lidando com paginação e rate limits.
- **Mineração de Dados:** Extração e cálculo de KDA (com tratamento matemático para evitar divisão por zero em *Perfect Games*), Farm por Minuto (CS/min) e Placar de Visão Médio.
- **Agrupamento Avançado:** Uso da biblioteca nativa `collections.Counter` para ranquear rapidamente os campeões mais vitoriosos, rotas favoritas e identificar os aliados (Duos) mais frequentes nas vitórias.
- **Segurança:** Proteção de credenciais sensíveis (API Keys) utilizando variáveis de ambiente.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- `requests` - Para requisições HTTP (GET) na Riot API.
- `python-dotenv` - Para gerenciamento de variáveis de ambiente e segurança.
- `collections.Counter` - Para otimização de contagem e ranqueamento de estruturas de dados.

---

## ⚙️ Como Executar o Projeto Localmente

**1. Clone este repositório:**
```bash
git clone [https://github.com/maicuu/lol-performance-analyzer.git](https://github.com/maicuu/lol-performance-analyzer.git)

2. Acesse a pasta do projeto:


cd lol-performance-analyzer
3. Crie e ative um ambiente virtual:

Windows:


python -m venv venv
venv\Scripts\activate
Linux/Mac:


python3 -m venv venv
source venv/bin/activate
4. Instale as dependências:


pip install requests python-dotenv
5. Configure suas credenciais:
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave de desenvolvedor da Riot Games API:

Snippet de código
RIOT_API_KEY=RGAPI-sua-chave-aqui
6. Execute o script:


python main.py
✒️ Autor
Maicon Wendel

💼 LinkedIn: www.linkedin.com/in/maiconce

🐙 GitHub: www.linkedin.com/in/maiconce

