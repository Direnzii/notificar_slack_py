import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from conectar import conectar_db
from querie import alerta_pedidos_combo
import time
import os

slack_token = os.getenv('SLACK_TOKEN')
client = WebClient(token=slack_token)
channel_id = '#pedido-com-combo-hoje'
nome_arquivo = 'resultados_banco.json'


def atualizar_arquivo_e_retorna_se_diferente():
    oficial = True
    cursor = conectar_db(oficial)
    cursor.execute(alerta_pedidos_combo())
    resultado = cursor.fetchall()
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        dados = json.load(file)
        file.close()
    if resultado:
        for item in resultado:
            json_saida = {
                "id_pedido": item[0],
                "id_cotacao": item[1],
                "cote_titulo": item[2],
                "usuario": item[3],
                "cliente_cnpj": item[4],
                "nome_cliente": item[5],
                "forn_cnpj": item[6],
                "nome_forn": item[7],
                "nome_repre": item[8],
                "data_envio_pedido": item[9].strftime('%Y-%m-%d %H:%M:%S')
            }
            situacao = item[10]
            if situacao == 11:
                json_saida['situacao'] = 'Não faturado'
            elif situacao == 12:
                json_saida['situacao'] = 'Faturado parcialmente'
            elif situacao == 6:
                json_saida['situacao'] = 'Faturado'
            else:
                json_saida['situacao'] = situacao
            if dados != json_saida:
                with open(nome_arquivo, 'w', encoding='utf-8') as file:
                    json.dump(json_saida, file, ensure_ascii=False, indent=4)
                    return json_saida
    else:
        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(resultado, file, ensure_ascii=False, indent=4)
    return False


def enviar_mensagem(message):
    message = f"""PEDIDO COM COMBO ENVIADO :warning:\n```{message}```"""
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        print(f"Mensagem enviada com sucesso: {response['ts']}")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem: {e.response['error']}")


if __name__ == '__main__':
    segundos = 60*10
    print(f'Irá esperar {segundos} segundos para cada verificação')
    while True:
        data_e_hora_atual = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            saida = atualizar_arquivo_e_retorna_se_diferente()
            if saida:
                enviar_mensagem(str(saida))
                print(f'{data_e_hora_atual}: Pedido encontrado, saida: {str(saida)}')
            else:
                print(f'{data_e_hora_atual}: Nenhum pedido novo encontrado')
            time.sleep(segundos)
        except Exception as E:
            print(f'{data_e_hora_atual}: ERROR: {E}')
