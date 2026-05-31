import turtle
import pandas as pd


def main():
    screen = turtle.Screen()
    screen.title("U.S. States Game")

    image = "blank_states_img.gif"
    screen.addshape(image)
    screen.setup(width=725, height=491)
    turtle.shape(image)

    df = pd.read_csv("50_states.csv")
    states_list = df["state"].str.lower().to_list()

    correct_guesses = []
    while True:
        guess_state = screen.textinput(
            title=f"{len(correct_guesses)}/50 guessed",
            prompt="What's another States name?"
        ).lower()

        if guess_state == 'exit':
            missing_df = pd.DataFrame(columns=df.columns)
            for i, row in df.iterrows():
                if row.state.lower() not in correct_guesses:
                    missing_df.loc[i] = row
            missing_df.to_csv("states_not_guessed.csv")
            break

        # add guess to guessed list
        if guess_state in states_list:
            correct_guesses.append(guess_state)
            coords = df[df.state.str.lower() == guess_state]
            state_name = turtle.Turtle()
            state_name.hideturtle()
            state_name.penup()
            state_name.goto(x=coords.x.iloc[0], y=coords.y.iloc[0])
            state_name.write(f"{coords.state.iloc[0]}")

        # exit if all have been guessed
        if len(correct_guesses) == 50:
            break


if __name__ == '__main__':
    main()
