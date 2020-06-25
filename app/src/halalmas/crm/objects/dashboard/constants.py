from halalmas.core.classes import ChoiceConstantBase


class TMPUserRoles(ChoiceConstantBase):
    ADMIN = 'admin'
    FINANCE = 'finance'
    CRA_TEAM = 'cra_team'
    HOST_TEAM = 'host_team'
    MARKETING = 'marketing'
    GUESTS = 'guests'

    @classmethod
    def ordering(cls, values):
        last_value = 'GUESTS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values
