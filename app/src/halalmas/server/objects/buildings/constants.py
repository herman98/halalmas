from halalmas.core.classes import ChoiceConstantBase


class TransportationType(ChoiceConstantBase):
    KRL = 1
    BUSWAY = 2
    MRT = 3
    HALTE = 4
    BANDARA = 5
    TRAIN_STATION = 6
    SEA_PORT = 7
    BUS_TERMINAL = 8
    BUS = 9
    OTHERS = 99

    @classmethod
    def ordering(cls, values):
        last_value = 'OTHERS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values
