from aiogram.fsm.state import State, StatesGroup


class DataStates(StatesGroup):
    path = State()  # Состояние для пути, по умолчанию будет использоваться 'C:/Users/%name%/Desktop/'
    coordinates = State()  # Состояние для координат движения мыши
