from datetime import datetime, timedelta

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
        boundaries = [
            dt_from + timedelta(hours=i)
            for i in range(
                (dt_upto - dt_from).days * 24 + (dt_upto - dt_from).seconds // 3600 + 2
            )
        ]
    elif group_type == "day":
        group_format = "%Y-%m-%dT00:00:00"
        boundaries = [
            dt_from + timedelta(days=i) for i in range((dt_upto - dt_from).days + 2)
        ]
    elif group_type == "month":
        group_format = "%Y-%m-01T00:00:00"
        boundaries = []
        current = dt_from
        while current <= dt_upto:
            boundaries.append(current)
            current += timedelta(days=30)
        boundaries.append(dt_upto + timedelta(days=1))
    else:
        raise ValueError("Invalid group_type")

    bucket_boundaries = [boundary.isoformat() for boundary in boundaries]

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {
            "$bucket": {
                "groupBy": "$dt",
                "boundaries": boundaries,
                "default": "Other",
                "output": {"total": {"$sum": "$value"}},
            }
        },
        {"$sort": {"_id": 1}},
    ]
    results = await collection.aggregate(pipeline).to_list(length=None)

    dataset = [0] * (len(bucket_boundaries) - 1)
    labels = [boundary.strftime(group_format) for boundary in boundaries[:-1]]

    for result in results:
        if result["_id"] != "Other":
            index = bucket_boundaries.index(result["_id"].isoformat())
            dataset[index] = result["total"]

    return {"dataset": dataset, "labels": labels}
