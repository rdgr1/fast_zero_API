from sqlachemy.orm import registry

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    id: int
    username: str
    password: str
    email: str