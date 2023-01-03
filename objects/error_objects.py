class DBConnectionsExistError(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to remove all DB connections before deleting this item.'
        )
