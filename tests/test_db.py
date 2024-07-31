from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):

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
