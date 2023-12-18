""" 
Classes to ensure parity between workflows and entities. 
Used for codegen and python types only
"""


class File:
    """A class to mock the file class in entities"""

    entity_id = None
    entity_field_name = None
    __tablename__ = None
    pass


class FileStatus:
    """A class to mock the file status class in entities"""

    pass
