import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()


class BancoDados:
    SALDO_INICIAL = 20

    def __init__(self):
        self.uri = os.getenv("DATABASE_URL")
        self.client = MongoClient(self.uri)
        self.db = self.client["haze_nexus"]
        self.collection = self.db["usuarios"]

    def alterar_hazium(self, user_id, quantidade):
        self.collection.update_one(
            {"_id": user_id},
            {"$setOnInsert": {"hazium": self.SALDO_INICIAL}},
            upsert=True,
        )
        self.collection.update_one({"_id": user_id}, {"$inc": {"hazium": quantidade}})

    def ver_saldo(self, user_id):
        usuario = self.collection.find_one({"_id": user_id})
        if usuario:
            return usuario.get("hazium", self.SALDO_INICIAL)
        return self.SALDO_INICIAL

    def pegar_ranking(self):
        ranking = self.collection.find().sort("hazium", -1).limit(10)
        return [(u["_id"], u["hazium"]) for u in ranking]

    def resgatar_daily(self, user_id):
        agora = datetime.now(timezone.utc)
        usuario = self.collection.find_one({"_id": user_id})

        if usuario and "ultimo_daily" in usuario:
            ultimo_resgate = usuario["ultimo_daily"]
            if ultimo_resgate.tzinfo is None:
                ultimo_resgate = ultimo_resgate.replace(tzinfo=timezone.utc)

            if agora < ultimo_resgate + timedelta(hours=24):
                tempo_restante = (ultimo_resgate + timedelta(hours=24)) - agora
                return False, tempo_restante

        self.collection.update_one(
            {"_id": user_id},
            {"$inc": {"hazium": 20}, "$set": {"ultimo_daily": agora}},
            upsert=True,
        )
        return True, None


db = BancoDados()
