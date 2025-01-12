from abc import abstractmethod
from typing import Protocol


class User:
    pass


class UserNotFoundError(Exception):
    pass


class UserGateway(Protocol):
    @abstractmethod
    def get_user(self, user_id: int) -> User:
        raise NotImplementedError


class ProductGateway(Protocol):
    @abstractmethod
    def add_product(self, user_id: int, product: str) -> None:
        raise NotImplementedError


class UnitOfWork(Protocol):
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError


class WarehouseClient(Protocol):
    @abstractmethod
    def next_product(self) -> str:
        raise NotImplementedError


class AddProductsInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            product_gateway: ProductGateway,
            unit_of_work: UnitOfWork,
            warehouse_client: WarehouseClient,
    ) -> None:
        self.user_gateway = user_gateway
        self.product_gateway = product_gateway
        self.unit_of_work = unit_of_work
        self.warehouse_client = warehouse_client

    def __call__(self, user_id: int):
        user = self.user_gateway.get_user(user_id)
        if user is None:
            raise UserNotFoundError
        self.product_gateway.add_product(
            user_id, self.warehouse_client.next_product(),
        )
        self.product_gateway.add_product(
            user_id, self.warehouse_client.next_product(),
        )
        self.unit_of_work.commit()
