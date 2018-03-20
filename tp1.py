import requests
import matplotlib.pyplot as plt
from datetime import datetime

BASE_URL = "https://min-api.cryptocompare.com/"


def main():
    print("============================", end="\n")
    print("--- === Crypto Check === ---", end="\n")
    print("============================", end=2*"\n")

    text = "0 : " + str(get_list_crypto.__doc__) + "\n" \
           "1 : " + str(generate_list_crypto.__doc__) + "\n" \
           "2 : " + str(get_current_price.__doc__) + "\n" \
           "3 : " + str(show_historic_graph.__doc__) + "\n" \

    print(text)

    while True:
        try:
            choice = int(input("Choix : "))
        except:
            break
        if choice == 0:
            print(get_list_crypto())
        elif choice == 1:
            generate_list_crypto(input("Chemin complet du fichier : "))
        elif choice == 2:
            devise = input("Devise : ").upper()
            crypto = input("Crypto : ").upper()
            print("1 {} = {} {}".format(crypto, get_current_price(devise, crypto), devise))
        elif choice == 3:
            lenght = input("Unité (day, hour, minute) : ")
            devise = input("Devise : ").upper()
            crypto = input("Crypto : ").upper()
            limit = input("Durée en unité : ").upper()
            show_historic_graph(lenght, devise, crypto, limit)
        else:
            break

    print("Process end")


def get_current_price(devise, crypto):
    """Prix actuel de la cyptomonnaie"""
    extra_url = "data/price?fsym={}&tsyms={}".format(crypto, devise)

    return requests.get(BASE_URL + extra_url).json()[devise]


def show_historic_graph(lenght, devise, crypto, limit):
    """Graphique du prix d'une cryptomonnaie en fonction du temps"""
    extra_url = "data/histo{}?fsym={}&tsym={}&limit={}".format(lenght, crypto, devise, limit)
    req = requests.get(BASE_URL + extra_url).json()["Data"]
    time = []
    price = []
    for i in req:
        time.append(datetime.fromtimestamp(i['time']))
        price.append(i['close'])
    plt.figure(figsize=(17, 6))
    plt.plot(time, price)

    return plt.show()


def get_list_crypto():
    """Liste de toutes les cryptomonnaies disponibles"""
    extra_url = "data/all/coinlist"
    req = requests.get(BASE_URL + extra_url).json()["Data"]
    fullname = ""
    for value in req.values():
        fullname += value["FullName"] + "\n"

    mon_fichier = open("listCrypto.txt", "w")
    mon_fichier.write(fullname)

    return fullname


def generate_list_crypto(fullpath):
    """Génére un fichier de toutes les cryptomonnaies disponibles"""
    try:
        mon_fichier = open(fullpath, "w")
        mon_fichier.write(get_list_crypto())
        print(f"File create at {fullpath}")
    except PermissionError:
        exit("PermissionError: we have no right on {0}".format(fullpath))
    except IsADirectoryError:
        exit("IsADirectoryError: The destination path is a folder not a file")


if __name__ == '__main__':
    main()
