import requests
import matplotlib.pyplot as plt
from datetime import datetime

BASE_URL = "https://min-api.cryptocompare.com/"


def main():
    show_info()
    while True:
        choice = check_int(input("Choix : "), 0)
        if choice == 0:
            print(get_list_crypto())
        elif choice == 1:
            generate_file_list_crypto(input("Chemin complet du fichier : "))
        elif choice == 2:
            devise = check_str(input("Devise (EUR) : "), "EUR")
            quantity = check_int(input("Quantité (1): "), 1)
            crypto = check_str(input("Crypto (BTC) : "), "BTC")
            print("{} {} = {} {}".format(quantity, crypto, quantity * get_current_price(devise, crypto), devise))
        elif choice == 3:
            lenght = input("Unité [day, hour, minute] : ")
            devise = check_str(input("Devise (EUR) : "), "EUR")
            crypto = check_str(input("Crypto (BTC) : "), "BTC")
            limit = check_int(input("Durée en unité (200) : "), 200)
            show_historic_graph(lenght, devise, crypto, limit)
        elif choice == 4:
            devise = check_str(input("Devise (EUR) : "), "EUR")
            crypto = check_str(input("Crypto (BTC,ETH,BCH,NEO,LTC,DASH,DGD,ZEH,XRM,REP) : "),
                               "ETH,BCH,NEO,LTC,DASH,DGD,ZEH,XRM,REP")
            show_histogram_graph(devise, crypto)
        else:
            quite()


def show_info():
    print("============================", end="\n")
    print("--- === Crypto Check === ---", end="\n")
    print("============================", end=2 * "\n")

    text = {0: get_list_crypto,
            1: generate_file_list_crypto,
            2: get_current_price,
            3: show_historic_graph,
            4: show_histogram_graph,
            5: quite}

    for key, value in text.items():
        print(key, value.__doc__, sep=" : ")


def get_current_price(devise, crypto):
    """Prix actuel de la cyptomonnaie"""
    extra_url = "data/price?fsym={}&tsyms={}".format(crypto, devise)

    return requests.get(BASE_URL + extra_url).json()[devise]


def show_historic_graph(unit, devise, crypto, limit):
    """Graphique du prix d'une cryptomonnaie en fonction du temps"""
    extra_url = "data/histo{}?fsym={}&tsym={}&limit={}".format(unit, crypto, devise, limit)
    req = requests.get(BASE_URL + extra_url).json()["Data"]
    time = []
    price = []
    for i in req:
        time.append(datetime.fromtimestamp(i['time']))
        price.append(i['close'])
    plt.figure(figsize=(17, 6))
    plt.plot(time, price)

    return plt.show()


def show_histogram_graph(devise, crypto):
    """Histogramme du prix actuel des cryptomonnais souhaitées"""
    extra_url = "data/pricemulti?fsyms={}&tsyms={}".format(crypto, devise)
    req = requests.get(BASE_URL + extra_url).json()
    price = []
    crypto = []
    for key, value in req.items():
        price.append(value[devise])
        crypto.append(key)
    plt.figure(figsize=(17, 6))
    plt.bar(crypto, price)

    return plt.show()


def get_list_crypto():
    """Liste de toutes les cryptomonnaies disponibles"""
    extra_url = "data/all/coinlist"
    req = requests.get(BASE_URL + extra_url).json()["Data"]
    fullname = ""
    for value in req.values():
        fullname += value["FullName"] + "\n"

    return fullname


def generate_file_list_crypto(fullpath):
    """Génére un fichier de toutes les cryptomonnaies disponibles"""
    try:
        mon_fichier = open(fullpath, "w")
        mon_fichier.write(get_list_crypto())
        print("File create at {}".format(fullpath))
    except PermissionError:
        exit("PermissionError: we have no right on {0}".format(fullpath))
    except IsADirectoryError:
        exit("IsADirectoryError: The destination path is a folder not a file")
    except FileNotFoundError:
        exit("FileNotFoundError: No such file or directory :{}".format(fullpath))


def quite():
    """Quitter le programme"""
    exit()


def check_str(input, default):
    if not input:
        input = default
    return input.upper()


def check_int(input, default):
    if not input:
        input = default
    try:
        input = int(input)
    except ValueError:
        exit('ErrorValue: invalid character')
    return input


if __name__ == '__main__':
    main()
