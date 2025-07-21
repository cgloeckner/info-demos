class State:
    def __init__(self, name: str):
        self.__name = name
        self.final = False
        self.__transitions: dict[str, State] = {}

    def link(self, input: str, state: 'State') -> None:
        if input in self.__transitions:
            raise ValueError('Input transitions must be unique.')
        
        self.__transitions[input] = state

    def __call__(self, input: str) -> 'State':
        return self.__transitions[input]


class StateMachine:
    def __init__(self):
        self.__states: dict[str, State] = {}

    def add(self, name: str) -> 'State':
        if name in self.__states:
            raise ValueError('State names must be unique')
    
        self.__states[name] = State(name)
        return self.__states[name]

    def __call__(self, start: State, word: str) -> bool:
        for input in word:
            try:
                start = start(input)
            except KeyError:
                return False
        return start.final
