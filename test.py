import requests
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import pandas
from datetime import datetime

BASE_URL = "https://min-api.cryptocompare.com/data/histoday?"
NBR_TEST = 70


def predict(limite):
    req = requests.get(BASE_URL + "fsym=ETC&tsym=EUR&limit={}".format(limite)).json()["Data"]
    df = pandas.DataFrame.from_dict(req)

    df.drop(['time'], axis=1, inplace=True)
    size = df.close.size
    df['id'] = [x for x in range(size)]

    df_train = df.loc[df.id < size - NBR_TEST - 1]
    df_test = df.loc[df.id >= size - NBR_TEST - 1]
    del df

    x_test = df_test.drop(['close', 'id'], axis=1)
    y_test = df_test['close']

    x_train = df_train.drop(['close', 'id'], axis=1)
    y_train = df_train['close']
    print(df_train)

    random_forest = RandomForestRegressor(n_estimators=100, n_jobs=4, verbose=True)
    random_forest.fit(x_train, y_train)
    print("Score : {}".format(random_forest.score(x_test, y_test)*100))
    return random_forest.predict(x_test)


def compare(prediction):
    req = requests.get(BASE_URL + "fsym=ETC&tsym=EUR&limit={}".format(NBR_TEST)).json()["Data"]
    df = pandas.DataFrame.from_dict(req)

    date = []
    for value in df['time'].values:
        date.append(datetime.fromtimestamp(value))

    plt.figure(figsize=(10, 4))
    plt.plot(date, df['close'])
    plt.plot(date, prediction)
    plt.show()


if __name__ == "__main__":
    pre = predict(600)
    compare(pre)
