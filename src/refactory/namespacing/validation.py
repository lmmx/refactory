__all__ = ["ValidatorBase"]


class ValidatorBase:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls):
        raise NotImplementedError("Override validate method in ValidatorBase subclass")
