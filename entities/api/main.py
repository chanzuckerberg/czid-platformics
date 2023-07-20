import typing
import time
from sqlalchemy import select
from fastapi import FastAPI, Depends
import uvicorn

import strawberry
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from strawberry.fastapi import GraphQLRouter

# from strawberry_sqlalchemy_mapper import strawberry_dataclass_from_model
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper, StrawberrySQLAlchemyLoader

############
# Database #
############
engine = create_engine("sqlite:///")
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()


#####################
# SQLAlchemy Models #
#####################

class SampleModel(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    sequencing_reads = relationship("SequencingReadModel", backref="sample")


class SequencingReadModel(Base):
    __tablename__ = "sequencing_read"
    sequencing_read_id = Column(Integer, primary_key=True, autoincrement=True)

    nucleotide = Column(String, nullable=False)
    sequence = Column(String, nullable=False)
    protocol = Column(String, nullable=False)

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)


######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()

@strawberry_sqlalchemy_mapper.type(SampleModel)
class Sample:
    sequencing_reads: typing.List["SequencingRead"]


@strawberry_sqlalchemy_mapper.type(SequencingReadModel)
class SequencingRead:
    sample: "Sample"


@strawberry.type
class Query:
    @strawberry.field
    def get_sample(self, id: strawberry.ID) -> Sample:
        return session.query(SampleModel).get(id)

    @strawberry.field
    def get_all_samples(self) -> typing.List[Sample]:
        return session.query(SampleModel).all()

    @strawberry.field
    def get_sequencing_read(self, id: strawberry.ID) -> SequencingRead:
        return session.query(SequencingReadModel).get(id)

    @strawberry.field
    def get_all_sequencing_reads(self) -> typing.List[SequencingRead]:
        return session.scalars(select(SequencingReadModel)).all()

def get_context():
    global session
    return {
        "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session),
    }

# Create models
Base.metadata.create_all(bind=engine)

# Fill database with test data
pond = SampleModel(name="Pond Sample", location="San Diego, CA")
nasal = SampleModel(name="Nasal Swab", location="Atlanta, GA")

session.add(pond)
session.add(nasal)
session.flush()  # Makes id available on the model instances

session.add(SequencingReadModel(sequence="ACTGACTGGCTA",
                      nucleotide="dna",
                      protocol="mngs",
                      sample_id=pond.id))
session.add(SequencingReadModel(sequence="GAGAGAGCTGACTGACTGA",
                      nucleotide="dna",
                      protocol="targeted",
                      sample_id=pond.id))
session.add(SequencingReadModel(sequence="CTCTCTTGACTGACTGA",
                      nucleotide="dna",
                      protocol="msspe",
                      sample_id=pond.id))

session.add(SequencingReadModel(sequence="AAAACTGACTGACTGA",
                      nucleotide="rna",
                      protocol="msspe",
                      sample_id=nasal.id))
session.add(SequencingReadModel(sequence="TTTTCTGACTGACTGA",
                      nucleotide="dna",
                      protocol="mngs",
                      sample_id=nasal.id))
session.add(SequencingReadModel(sequence="CCCCTGACTGACTGA",
                      nucleotide="rna",
                      protocol="targeted",
                      sample_id=nasal.id))

session.commit()

# call finalize() before using the schema:
# (note that models that are related to models that are in the schema
# are automatically mapped at this stage
strawberry_sqlalchemy_mapper.finalize()
# only needed if you have polymorphic types
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())
# strawberry graphql schema
# start server with strawberry server app
schema = strawberry.Schema(
    query=Query,
#    mutation=Mutation,
#    extensions=extensions,
    types=additional_types,
)


graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    config = uvicorn.Config(
        "example:app", host="0.0.0.0", port=8008, log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()

