from aiogram.fsm.state import State, StatesGroup


class DataStates(StatesGroup):
    """
    Класс состояний для хранения данных, используемых в боте.

    path (State): Состояние для хранения пути к файлу или папке. По умолчанию используется 'C:/Users/%name%/Desktop/'.
    coordinates (State): Состояние для хранения координат движения мыши.
    """

    path = State()  # Состояние для пути, по умолчанию будет использоваться 'C:/Users/%name%/Desktop/'
    coordinates = State()  # Состояние для координат движения мыши
