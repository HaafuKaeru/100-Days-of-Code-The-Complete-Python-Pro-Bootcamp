import pandas as pd


def main():

    data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
    fur_colors = data["Primary Fur Color"].value_counts()
    fur_colors = fur_colors.reset_index()
    print(fur_colors)
    fur_colors.to_csv("fur_colors.txt")


if __name__ == '__main__':
    main()
