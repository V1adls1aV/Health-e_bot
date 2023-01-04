from pytest import fixture


class UserMock:  # Mock of User class
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        
    def get_additives_names(self) -> list[str]:
        return ['сахар', 'молоко']


@fixture
def user() -> UserMock:
    # Creating Mock
    return UserMock(5148021085)
