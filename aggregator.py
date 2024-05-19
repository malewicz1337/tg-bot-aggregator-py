from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://127.0.0.1:27017"
DB_NAME = "sampleDB"
COLLECTION_NAME = "sample_collection"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


async def aggregate_salaries(dt_from, dt_upto, group_type):
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    if group_type == "hour":
        group_format = "%Y-%m-%dT%H:00:00"
    elif group_type == "day":
        group_format = "%Y-%m-%dT00:00:00"
    elif group_type == "month":
        group_format = "%Y-%m-01T00:00:00"
    else:
        raise ValueError("Invalid group_type")

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {
            "$group": {
                "_id": {"$dateToString": {"format": group_format, "date": "$dt"}},
                "total": {"$sum": "$value"},
            }
        },
        {"$sort": {"_id": 1}},
    ]
    results = await collection.aggregate(pipeline).to_list(length=None)

    dataset = [r["total"] for r in results]
    labels = [r["_id"] for r in results]

    return {"dataset": dataset, "labels": labels}
