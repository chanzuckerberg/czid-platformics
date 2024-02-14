from pydantic import BaseModel
from strawberry.field import StrawberryField
from pydantic.errors import ValidationError
import strawberry


@strawberry.type
class PlatformicsFieldValidationError:
    loc: list[str]
    error: str
    type: str

@strawberry.type
class PlatformicsValidationException:
    errors: list[PlatformicsFieldValidationError]

def convert_validation_exception(err: ValidationError):
    errors = []
    for err in err.errors():
        errors.append(PlatformicsValidationException(loc=err["loc"], error=err["msg"], type=err["type"]))
    return PlatformicsValidationException(errors=errors)