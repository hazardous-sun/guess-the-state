import json


def load_json(filename) -> dict[str, str]:
    with open(filename, 'r') as f:
        return json.load(f)


class State:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_states() -> list[State]:
    states: list[State] = []
    file_dict = load_json('states.json')
    for key, value in file_dict.items():
        states.append(State(key, value))
    return states


if __name__ == "__main__":
    quit(1)
