import socket
from ModelClr import ModelClr
from ModelScr import ModelScr
from Model import Model
from ModelClr import ModelClr
from ModelScr import ModelScr
from Viewer import Viewer
from Model import Model
import json
import msgpack
from bs4 import BeautifulSoup


MT4_IP = '127.0.0.1'
MT4_PORT = 77

def invia_comando_mt4(comando):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MT4_IP, MT4_PORT))
        s.sendall(comando.encode())
        data = s.recv(1024)
    return data.decode()


def formatString(simbol:str):
    formatted_string_1 = simbol.lower().replace(" ", "-")
    formatted_string_2 = simbol.replace(" ", "") + "=X"
    formatted_string_3 = ''.join(filter(str.isalpha, simbol))
    
    return [formatted_string_1, formatted_string_2, formatted_string_3]


def load_default(ref):
    with open(f"{ref}M1_version.msgpack", "rb") as file:
        groups = file.read()
    with open(f"{ref}M2_version.msgpack", "rb") as file:
        class_cluster = file.read()
    with open(f"{ref}M3_version.msgpack", "rb") as file:
        ranked = file.read()
    with open(f"{ref}M4_version.msgpack", "rb") as file:
        directions = file.read()
      
    class_cluster = msgpack.unpackb(class_cluster, raw=False)
    ranked = msgpack.unpackb(ranked, raw=False)
    directions = msgpack.unpackb(directions, raw=False)
    groups = msgpack.unpackb(groups, raw=False)
        
    with open('simbols.json', 'r') as file:
        lista_stringhe = json.load(file)
    
    simbol = {key:formatString(simbol) for key, simbol in enumerate(lista_stringhe)}
    data_t = {}
    return groups, class_cluster, directions, data_t, ranked, simbol


def checkIfClosePosition() -> bool:
    comando = "GET_OPEN_POSITIONS"  # Comando per ottenere informazioni sulle posizioni aperte
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MT4_IP, MT4_PORT))
        s.sendall(comando.encode())
        data = s.recv(1024)
    return data.decode() if data else None

if __name__ == "__main__":

    simbolVal = input("insert simbol: ")
    groups, class_cluster, directions, data_t, ranked, simbol = load_default("./")
    c = ModelClr(groups, class_cluster, directions, data_t, ranked, simbol, 20, 50)
    s = ModelScr(simbol)
    m = Model(c, s)
    
    while True:
        _, flag, _, data, table, _, minim, maximum = m.predict(simbol)
        soup = BeautifulSoup(table, 'html.parser')
        td_cells = soup.find_all('td')
        testo_celle = [cella.get_text() for cella in td_cells]
        comando:str = f'{"MSG": "QUOTE", "SYMBOL": {simbol[simbolVal][1]}}\r\n'
        risposta:dict = invia_comando_mt4(comando)
        info:str = data.split('\n')[1]
        infos:dict = {str(items.split(":")[0]):int(items.split(":")[1]) for items in list(info.split(" "))}
        buy:bool = float(flag) > float(risposta['BID']) and infos['Buy']>infos['Sell']+infos['Neutral'] and int(testo_celle[2].replace("%", "").replace('\n', '').replace('\r', '')) > int(testo_celle[6].replace("%", "").replace('\n', '').replace('\r', ''))
        sell:bool = float(flag) < float(risposta['BID']) and infos['Sell']>infos['Buy']+infos['Neutral'] and int(testo_celle[2].replace("%", "").replace('\n', '').replace('\r', '')) < int(testo_celle[6].replace("%", "").replace('\n', '').replace('\r', ''))

        status = checkIfClosePosition()

        if status is not None and len(status) == 0:
            if buy:
                comando = f"BUY {simbol[simbolVal][2]} 1 {risposta['BID']} {minim-(abs(minim-float(flag)))*0.25} {float(flag)}"
                risposta = invia_comando_mt4(comando)
                print("Risposta da MT4:", risposta) 
            elif sell:
                comando = f"SELL {simbol[simbolVal][2]} 1 {risposta['BID']} {maximum+(abs(maximum-float(flag)))*0.25} {float(flag)}"
                risposta = invia_comando_mt4(comando)
                print("Risposta da MT4:", risposta) 