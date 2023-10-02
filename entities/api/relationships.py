from api.types.samples import SampleWhereClause
import typing
import strawberry

@strawberry.input
class kapow:
    id: str

def finalize():
    pass
    #print(SampleWhereClause.__strawberry_definition__)

    #SampleWhereClause.kapow = None
    #SampleWhereClause.__annotations__["kapow"] = typing.Optional[kapow]
    #SampleWhereClause.__strawberry_definition__.fields.append(kapow)
    #SampleWhereClause.kapow = strawberry.input()
    #SampleWhereClause.__annotations__["kapow"] = typing.Optional[str]
# how to add a field to an input
# how to add a field to an output
