from halalmas.core.classes import ChoiceConstantBase


class LoginWith(ChoiceConstantBase):
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'
    INSTAGRAM = 'INSTAGRAM'
    TWITTER = 'TWITTER'
    NORMAL = 'NORMAL'

    @classmethod
    def ordering(cls, values):
        last_value = 'NORMAL'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values


class LoginFrom(ChoiceConstantBase):
    ANDROID = 'ANDROID'
    IOS = 'IOS'
    WEBSITE = 'WEBSITE'

    @classmethod
    def ordering(cls, values):
        last_value = 'OTHERS'
        ordered_values = sorted(values)
        if last_value in ordered_values:
            ordered_values.remove(last_value)
            ordered_values.append(last_value)
        return ordered_values

    # @staticmethod
    # def translate(value):
    #     if value == 1:
    #         text = "ANDROID"
    #     elif value == 2:
    #         text = "IOS"
    #     elif value == 3:
    #         text = "WEBSITE"
    #     else:  # value == 99:
    #         text = "OTHERS"
    #     return text
