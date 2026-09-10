from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    service = State()
    name = State()
    contact = State()