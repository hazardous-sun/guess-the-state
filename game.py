import json
import easygui
import random


class State:
    """
    Contains the data of each state.

    :param str acronym: the acronym of the state
    :param str name: the full name of the state
    :param str image_path: the path to the image of the state under imgs/
    """

    def __init__(self, acronym, name, image_path):
        self.acronym = acronym
        self.name = name
        self.image_path = image_path


def load_json(filename) -> dict[str, str]:
    with open(filename, 'r') as f:
        return json.load(f)


def get_states() -> list[State]:
    states: list[State] = []
    file_dict = load_json('states.json')
    for key, value in file_dict.items():
        states.append(State(key, value, f"imgs/{key}.jpg"))
    return states


class Game:
    """
    Contains the game logic of the game.
    """

    def __init__(self):
        self.states: list[State] = []
        self.valid_states: list[State] = []
        self.options_amount = 0
        self.rounds = 0
        self.score = 0

    def set_states(self):
        self.states = get_states()
        self.valid_states = get_states()

    def set_options_amount(self):
        match int(easygui.indexbox(
            title="Options amount per round",
            msg="How many options do you wish to have at each phase?",
            choices=["3 option", "9 options", "All 27 options"]
        )):
            case 0:
                self.options_amount = 3
            case 1:
                self.options_amount = 9
            case 2:
                self.options_amount = 27
            case _:
                pass

    def set_rounds(self):
        """
        Defines the number of rounds of the game.
        :return:
        """
        match int(easygui.indexbox(
            title="Define rounds",
            msg="How many round do you wish to play?",
            choices=["3 states", "9 states", "All 27 states"]
        )):
            case 0:
                self.rounds = 3
            case 1:
                self.rounds = 9
            case 2:
                self.rounds = 27
            case _:
                pass

    def set_score(self):
        self.score = 0

    def randomize_states(self):
        random.shuffle(self.states)

    def remove_state(self, removed_state: State):
        """
        Removes one valid state from states.

        :param removed_state:
        :return:
        """
        for state in self.states:
            if state.acronym == removed_state.acronym:
                self.states.remove(state)

    def get_options(self) -> (list[State], State):
        """
        Returns a list of all possible options that the player can choose from based on self.options_amount value.

        :return:
        """
        # Initializes temporary variables for storing the options that will be returned along
        options: list[State] = []

        answer: State = random.choice(self.valid_states)
        self.valid_states.remove(answer)
        self.remove_state(answer)

        options.append(answer)
        for _ in range(self.options_amount - 1):
            new_state = random.choice(self.states)
            options.append(new_state)
            self.states.remove(new_state)

        # Re-insert the removed values from self.states
        for state in options:
            self.states.append(state)

        random.shuffle(options)

        return options, answer

    def choice_screen(self):
        options, answer = self.get_options()
        index = easygui.indexbox(
            msg=f"Which is the acronym of the red state?\tYour current score is {self.score}/{self.rounds}",
            choices=list(map(lambda x: x.acronym.upper(), options)),
            image=answer.image_path
        )
        print(index)
        print(answer.acronym.upper())
        if options[index].acronym == answer.acronym:
            self.score += 1

    def start(self):
        self.set_states()
        while True:
            self.set_rounds()
            self.set_options_amount()
            self.set_score()

            for _ in range(self.rounds):
                self.choice_screen()

            if not easygui.boolbox(
                    msg=f"Your score was: {self.score}/{self.rounds}\nWould you like to play again?",
                    choices=["Yes", "No"]
            ):
                break


if __name__ == "__main__":
    quit(1)
