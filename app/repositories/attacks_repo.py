from bson.objectid import ObjectId


def insert_many(collection, data: list):
    collection.insert_many(data)


def create_document(collection, data: dict) -> str:
    result = collection.insert_one(data)
    return str(result.inserted_id)


def get_document_by_id(collection, doc_id: str) -> dict:
    return collection.find_one({"_id": ObjectId(doc_id)})


def get_all_documents(collection, start_date=None, end_date=None) -> list:
    if start_date and end_date:
        filter_by = {
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        print(filter_by)
    else:
        filter_by = {}
    return list(collection.find(filter_by))


def update_document_by_id(collection, doc_id: str, updates: dict) -> bool:
    result = collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": updates}
    )
    return result.modified_count > 0


def delete_document_by_id(collection, doc_id: str) -> bool:
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    return result.deleted_count > 0


def count_documents(collection, filter: dict = None) -> int:
    if filter is None:
        filter = {}
    return collection.count_documents(filter)
