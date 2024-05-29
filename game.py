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
        states.append(State(key, value, f"imgs/{value}.jpg"))
    return states


class Game:
    """
    Contains the game logic of the game.

    :param states: the list of states. If not provided, the game will use the data under "states.json".
    """

    def __init__(self, states=None):
        if states is None:
            states = get_states()
        self.states: list[State] = states
        self.rounds = 0
        self.options_amount = 0
        self.score = 0

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

    def set_options_amount(self):
        match int(easygui.indexbox(
            title="Options amount per round",
            msg="How many options do you wish to have at each phase?",
            choices=["3 option", "9 options", "All 27 options"]
        )):
            case 0:
                self.rounds = 3
            case 1:
                self.rounds = 9
            case 2:
                self.rounds = 27
            case _:
                pass

    def randomize_states(self):
        random.shuffle(self.states)

    def get_options(self) -> list[State]:
        """
        Returns a list of all possible options that the player can choose from based on self.options_amount value.

        :return:
        """
        options: list[State] = []
        temp_removed_states: list[State] = []

        for _ in range(self.rounds):
            new_state = random.choice(self.states)
            temp_removed_states.append(new_state)
            self.states.remove(new_state)
            options.append(new_state)

        for state in temp_removed_states:
            self.states.append(state)

        return options

    def get_correct_answer(self) -> (list[State], int):
        self.randomize_states()
        options = self.get_options()
        answer_index = random.randint(0, len(options) - 1)
        return options, answer_index

    def choice_screen(self):
        options, answer_index = self.get_correct_answer()
        value = easygui.ccbox(
            msg="Which is the acronym of the red state?",
            choices=list(map(lambda x: x.acronym.upper(), options)),
            image=options[answer_index].image_path
        )
        if value == self.states[answer_index].acronym.upper():
            self.score += 1

    def start(self):
        while True:
            self.set_rounds()
            self.set_options_amount()

            for _ in range(self.rounds):
                self.choice_screen()

            if easygui.boolbox(
                msg="Would you like to play again?",
                choices=["Yes", "No"]
            ):
                break


if __name__ == "__main__":
    quit(1)
