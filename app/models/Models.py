import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class ClientModel():
    __tablename__ = 'clients'

    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[int]
    favorite_products: Mapped[list['ClientFavoriteModel']] = relationship(
        back_populates='clients',
        cascade='all, delete-orphan',
        lazy='selectin',
        init=False,
        default_factory=list
    )
    


@table_registry.mapped_as_dataclass
class ClientFavoriteModel():
    __tablename__ = "client_favorites"

    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('clients.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(primary_key=True)

    clients: Mapped["ClientModel"] = relationship(
        back_populates="favorite_products",
        init=False
    )