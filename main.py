import os
import time
import requests
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
REGION_AMERICAS = "americas"

def obter_puuid(game_name, tag_line):
    url = f"https://{REGION_AMERICAS}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json().get('puuid') if response.status_code == 200 else None

def listar_partidas(puuid, quantidade=40):
    url = f"https://{REGION_AMERICAS}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={quantidade}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def analisar_vitorias(puuid, match_ids, limite_vitorias=10):
    vitorias_encontradas = 0
    campeoes_vitoriosos = Counter()
    rotas_jogadas = Counter()
    meus_duos = Counter()
    
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_farm = 0
    total_duration = 0
    total_vision = 0

    print(f"  Minerando dados ate encontrar {limite_vitorias} vitorias...")

    for m_id in match_ids:
        if vitorias_encontradas >= limite_vitorias:
            break

        url = f"https://{REGION_AMERICAS}.api.riotgames.com/lol/match/v5/matches/{m_id}"
        headers = {"X-Riot-Token": API_KEY}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            participantes = data['info']['participants']
            
            meu_dado = next((p for p in participantes if p['puuid'] == puuid), None)
            
            if meu_dado and meu_dado['win']:
                vitorias_encontradas += 1
                meu_time_id = meu_dado['teamId']
                
                campeoes_vitoriosos[meu_dado['championName']] += 1
                rotas_jogadas[meu_dado.get('teamPosition', 'Desconhecida')] += 1
                
                total_kills += meu_dado['kills']
                total_deaths += meu_dado['deaths']
                total_assists += meu_dado['assists']
                total_farm += (meu_dado['totalMinionsKilled'] + meu_dado['neutralMinionsKilled'])
                total_duration += data['info']['gameDuration']
                total_vision += meu_dado.get('visionScore', 0)
                
                for p in participantes:
                    if p['teamId'] == meu_time_id and p['puuid'] != puuid:
                        nick_aliado = p.get('riotIdGameName') or p.get('summonerName', 'Desconhecido')
                        meus_duos[nick_aliado] += 1
                        
        time.sleep(1)

    metricas_extras = {
        "kda_medio": (total_kills + total_assists) / max(1, total_deaths),
        "farm_minuto": total_farm / (total_duration / 60) if total_duration > 0 else 0,
        "visao_media": total_vision / limite_vitorias if limite_vitorias > 0 else 0
    }

    return campeoes_vitoriosos, rotas_jogadas, meus_duos, vitorias_encontradas, metricas_extras

if __name__ == "__main__":
    NICK = "Maicuu"
    TAG = "3010"

    print(f"\nIniciando Data Analytics para: {NICK}#{TAG}\n")
    meu_puuid = obter_puuid(NICK, TAG)

    if meu_puuid:
        historico_ids = listar_partidas(meu_puuid, quantidade=40)
        
        campeoes, rotas, duos, total_vitorias, metricas = analisar_vitorias(meu_puuid, historico_ids)

        tradutor_rotas = {
            'TOP': 'Top Lane', 
            'JUNGLE': 'Cacador (Jungle)', 
            'MIDDLE': 'Mid Lane', 
            'BOTTOM': 'Atirador (ADC)', 
            'UTILITY': 'Suporte',
            'Desconhecida': 'ARAM / Outros'
        }

        print("\n" + "="*50)
        print(f" RELATORIO DAS ULTIMAS {total_vitorias} VITORIAS ")
        print("="*50)
        
        print("\n TOP 3 CAMPEOES MAIS VITORIOSOS:")
        for campeao, qtd in campeoes.most_common(3):
            print(f"  - {campeao}: {qtd} vitorias")

        if rotas:
            rota_favorita, qtd_rota = rotas.most_common(1)[0]
            nome_rota = tradutor_rotas.get(rota_favorita, rota_favorita)
            print(f"\n ROTA FAVORITA:")
            print(f"  - {nome_rota} ({qtd_rota} partidas)")

        print("\n QUEM MAIS CARREGOU COM VOCE (Top 3 Aliados):")
        for aliado, qtd in duos.most_common(3):
            print(f"  - {aliado}: jogou junto em {qtd} vitorias")

        print("\n METRICAS DE DESEMPENHO (Medias nas Vitorias):")
        print(f"  - KDA Medio: {metricas['kda_medio']:.2f}")
        print(f"  - Farm por Minuto (CS/min): {metricas['farm_minuto']:.1f}")
        print(f"  - Placar de Visao Medio: {metricas['visao_media']:.1f}")
            
        print("\n" + "="*50)