from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import strawberry
from graphql.error import GraphQLError
from platformics.api.core.errors import PlatformicsException
from pydantic import ValidationError
from strawberry.extensions.base_extension import SchemaExtension


@strawberry.type
class PlatformicsValidationError(GraphQLError):
    message: str
    nodes: Any
    stack: Optional[Any] = None
    source: Optional[Any] = None
    positions: Optional[Any] = None  # type: Optional[Any]
    path: Union[List[Union[int, str]], List[str], None] = None
    extensions: Optional[Dict[str, Any]] = None
    original_error: Optional[Exception] = None


class NoOpHandler:
    def convert_exception(self, err: PlatformicsException) -> PlatformicsException:
        return [err]


class ValidationExceptionHandler:
    def convert_exception(self, err: GraphQLError) -> PlatformicsValidationError:
        validation_error = err.original_error
        errors = []
        for field_err in validation_error.errors():
            errors.append(
                GraphQLError(
                    message=f"Validation Error: {'.'.join(field_err['loc'])} - {field_err['msg']}",
                    nodes=err.nodes,
                    source=err.source,
                    positions=err.positions,
                    path=err.path,
                    original_error=None,
                )
            )
        return errors


class DefaultExceptionHandler:
    error_message: str = "Unexpected error."

    def convert_exception(self, err: GraphQLError) -> list[GraphQLError]:
        return [
            GraphQLError(
                message=self.error_message,
                nodes=err.nodes,
                source=err.source,
                positions=err.positions,
                path=err.path,
                original_error=None,
            )
        ]


class HandleErrors(SchemaExtension):
    def __init__(self):
        self.handlers = {
            ValidationError: ValidationExceptionHandler(),
            PlatformicsException: NoOpHandler(),
        }
        self.default_handler = DefaultExceptionHandler()

    def process_error(self, error: GraphQLError) -> GraphQLError:
        handler = self.handlers.get(type(error.original_error), self.default_handler)
        return handler.convert_exception(error)

    def on_operation(self) -> Iterator[None]:
        yield
        result = self.execution_context.result
        if result and result.errors:
            processed_errors: List[GraphQLError] = []
            for error in result.errors:
                processed_errors.extend(self.process_error(error))

            result.errors = processed_errors
