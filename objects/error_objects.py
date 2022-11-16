class DBConnectionsExistError(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to remove all DB connections before deleting this item.'
        )


class IncorrectArgumentsError(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to give e_number or e_name to init EAdditive. This item does not exist.'
        )
