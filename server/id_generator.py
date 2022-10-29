class IdGenerator:
    last_id = 0

    def get_id(self):
        self.last_id += 1
        return self.last_id


id_generator = IdGenerator()
