from halalmas.core.classes import ChoiceConstantBase


class BankAccountType(ChoiceConstantBase):
    BT = 'BanK Transfer'
    VA = 'Virtual Acount'
    OTHERS = 'Others'

    @classmethod
    def ordering(cls, values):
        last_value = 'OTHERS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values
