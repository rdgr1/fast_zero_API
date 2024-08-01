from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='alice', password='secret', email='teste@test')
    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
