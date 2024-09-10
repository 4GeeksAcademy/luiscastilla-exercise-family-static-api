from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []

    def _generarId(self):
        return randint(0, 99999999)

    def agregar_member(self, member):
        if not member.get("id"):
            member["id"] = self._generarId()
        self._members.append(member)

    def eliminar_member(self, id):
        for index, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(index)
                return True
        return False

    def optener_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def optener_all_members(self):
        return self._members
