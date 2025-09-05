from sqlalchemy import select

from app.models.Models import ClientModel


def test_create_client(session):
    new_client = ClientModel(
        name='João Victor',
        email='joao_victor@gmail.com'
    )
    session.add(new_client)
    session.commit()

    client = session.scalar(
        select(ClientModel).where(ClientModel.email == 'joao_victor@gmail.com')
    )

    assert client.email == 'joao_victor@gmail.com'
