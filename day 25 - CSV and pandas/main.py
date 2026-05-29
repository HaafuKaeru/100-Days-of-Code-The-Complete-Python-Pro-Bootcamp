import pandas as pd


def main():

    data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
    fur_colors = set(data["Primary Fur Color"].dropna())



if __name__ == '__main__':
    main()
