from halalmas.core.classes import ChoiceConstantBase


class OrganizationType(ChoiceConstantBase):
    PT = 'PT'
    CV = 'CV'
    NGO = 'NGO'
    INDIVIDUAL = 'Individual'
    OTHERS = 'Others'

    @classmethod
    def ordering(cls, values):
        last_value = 'OTHERS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values


class GroupType(ChoiceConstantBase):
    HOST = 1
    CUSTOMER = 2
    HOST_AND_CUSTOMER = 3
    FNB_PROVIDER = 4
    FACILITY_PROVIDER = 5
    OTHERS = 99

    @classmethod
    def ordering(cls, values):
        last_value = 'OTHERS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values

    @staticmethod
    def translate(value):
        if value == 1:
            text = "HOST"
        elif value == 2:
            text = "CUSTOMER"
        elif value == 3:
            text = "HOST_AND_CUSTOMER"
        elif value == 4:
            text = "FNB_PROVIDER"
        elif value == 5:
            text = "FACILITY_PROVIDER"
        else:  # value == 99:
            text = "OTHERS"
        return text
