class Validator:
    def validate(self, message, user=None):
        raise NotImplementedError


class EditedValidator(Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, message, user=None):
        pass


class MediaValidator(Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, message, user=None):
        pass


Validators = Validator | EditedValidator | MediaValidator
