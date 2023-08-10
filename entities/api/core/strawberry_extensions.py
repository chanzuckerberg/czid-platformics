import typing

from fastapi.dependencies import utils as deputils
from fastapi.params import Depends as DependsClass
from strawberry.extensions import FieldExtension
from strawberry.field import StrawberryField
from strawberry.types import Info


class DependencyExtension(FieldExtension):
    def __init__(self):
        self.dependency_args: list[typing.Any] = []
        self.strawberry_field_names = ["self"]

    def apply(self, field: StrawberryField) -> None:
        self.dependant = deputils.get_dependant(
            path="/", call=field.base_resolver.wrapped_func
        )
        # Remove fastapi Depends arguments from the list that strawberry tries to resolve
        field.arguments = [
            item
            for item in field.arguments
            if not isinstance(item.default, DependsClass)
        ]

    async def resolve_async(
        self,
        next_: typing.Callable[..., typing.Any],
        source: typing.Any,
        info: Info,
        **kwargs,
    ) -> typing.Any:
        request = info.context["request"]
        try:
            if "dependency_cache" not in request.context:
                request.context["dependency_cache"] = {}
        except AttributeError:
            request.context = {"dependency_cache": {}}

        solved_result = await deputils.solve_dependencies(
            request=request,
            dependant=self.dependant,
            body={},
            dependency_overrides_provider=request.app,
            dependency_cache=request.context["dependency_cache"],
        )
        (
            solved_values,
            _,  # solver_errors. It shouldn't be possible for it to contain anything relevant to this extension.
            _,  # background tasks
            _,  # the subdependency returns the same response we have
            new_cache,  # sub_dependency_cache
        ) = solved_result

        request.context["dependency_cache"].update(new_cache)
        kwargs.update(solved_values)
        res = await next_(source, info, **kwargs)
        return res
