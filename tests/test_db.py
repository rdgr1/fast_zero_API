from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fast_zero.models import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            username='test',
            email='test@test.com',
            password='secret',
        )
        session.add(user)
        session.commit()

        result = session.scalar(
            select(User).where(User.email == 'duno@ssauro.com')
        )

    assert result.username == 'test'
