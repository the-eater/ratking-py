from .generic_repository import GenericRepository
from ..rat import Rat
import json
import sqlite3


class RatkingRepository(GenericRepository):
    path = None
    db = None

    def __init__(self, path=None):
        self.path = path

    def load(self):
        self.db = sqlite3.connect(self.path)

        self.db.execute('CREATE TABLE IF NOT EXISTS rats (name TEXT, version TEXT, rat_json TEXT)')

    def save(self):
        self.db.commit()

    def __del__(self):
        if self.db is not None:
            self.db.close()

    def get(self, name, version):
        result = self.db.execute('SELECT rat_json FROM rats WHERE name=? AND version=?', (name, version)).fetchone()

        return None if result is None else Rat.from_dict(json.loads(result[0]))

    def get_versions(self, name):
        return [Rat.from_dict(json.loads(row[0])) for row in
                self.db.execute('SELECT rat_json FROM rats WHERE name=?', (name,))]

    def put(self, rat):
        self.db.execute('INSERT INTO rats(name, version, rat_json) VALUES (?, ?, ?)',
                        (rat.name, rat.version, json.dumps(rat)))
