import os
import yaml

with open(os.path.join(os.path.dirname(__file__), "resources", "responses.yaml")) as f:
    CONFIG_YAML = yaml.safe_load(f)

MAIN_YAML_SECTION = "responses"


class _YAMLStringsGetter(type):

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.section is not None:
                return CONFIG_YAML[MAIN_YAML_SECTION][cls.section][name]
            else:
                raise KeyError("Can not access the values without providing a \"section\" key")
        except KeyError:
            dotted_path = '.'.join((cls.section, name))
            print(f"Tried accessing configuration variable at `{dotted_path}`, but it could not be found.")
            raise

    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        for name in cls.__annotations__:
            yield name, getattr(cls, name)


class Hello(metaclass=_YAMLStringsGetter):
    section = "hello"
    hello: str


class Help(metaclass=_YAMLStringsGetter):
    section = "help"
    hello: str
    # talk: str
    emotion: str
    games: str
    game: str
    descriptions: str
    description: str
    joke: str
    addJoke: str
    clear: str
    # date: str


class Emotion(metaclass=_YAMLStringsGetter):
    section = "emotion"
    intense: str
    normal: str
    mild: str


class Talk(metaclass=_YAMLStringsGetter):
    section = "talk"
    question: str
    wait: str
    answer_first: str
    answer_existing: str
    answer_chatbot: str


class Topics:
    topics = ["Movie", "Colour"]


class Games(metaclass=_YAMLStringsGetter):
    section = "games"
    game: str
    noted: str


class Description(metaclass=_YAMLStringsGetter):
    section = "descriptions"
    description: str
    noted: str


class Jokes(metaclass=_YAMLStringsGetter):
    section = "jokes"
    noted: str


class Clear(metaclass=_YAMLStringsGetter):
    section = "clear"
    clear: str


class Date(metaclass=_YAMLStringsGetter):
    section = "date"
    now: str
