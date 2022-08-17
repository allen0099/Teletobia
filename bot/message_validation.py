from typing import List, Type

from pyrogram import types

from bot.errors import ValidationError
from bot.validators import Validator, EditedValidator, Validators

DEFAULT_VALIDATORS: List[Type[Validator]] = [EditedValidator]


def get_default_validators() -> list[Validators]:
    return get_validators(DEFAULT_VALIDATORS)


def get_validators(validator_configs: List[Type[Validator]]) -> list[Validators]:
    """
    Get validators from group settings.

    Args:
        group:

    Returns:

    """

    validators: list[Validators] = []

    for validator in validator_configs:
        validators.append(validator())

    return validators


def validate_message(
    message: types.Message, message_validators: list[Validator] = None
) -> None:
    errors = []

    if message_validators is None:
        message_validators: list[Validator] = get_default_validators()

    for validator in message_validators:
        try:
            validator.validate(message)
        except ValidationError as error:
            errors.append(error)

    if errors:
        raise ValidationError(errors)
