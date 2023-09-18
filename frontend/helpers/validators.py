import re


class Validators:
    @staticmethod
    def validations(context, validator):
        matches = re.findall(validator, context)
        return (len(matches) > 0) and matches[0] == context

    def validate_input(inp):
        validator = "[A-Za-z \s]+"
        return Validators.validations(context=inp, validator=validator)
