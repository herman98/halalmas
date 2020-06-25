from halalmas.core.classes import ChoiceConstantBase


class CalendarDateType(ChoiceConstantBase):
    WEEKDAY = 'WEEKDAY'
    WEEKEND = 'GOOGLE'
    HOLIDAY = 'WEEKEND'
    DAY_OFF = 'DAY_OFF'
    SPECIAL = 'SPECIAL'

    @classmethod
    def ordering(cls, values):
        last_value = 'WEEKDAY'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values
