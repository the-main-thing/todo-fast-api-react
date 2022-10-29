class FakeDb:
    store = {}

    def set_todos(self, user_id: int, value: list):
        self.store[user_id] = value
        return value

    def get_todos(self, user_id: int):
        return self.store[user_id]


db = FakeDb()
