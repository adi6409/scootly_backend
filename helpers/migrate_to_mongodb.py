import pandas as pd
from database import get_database, init_db

def migrate_csv_to_mongodb(csv_path):
    # Initialize database and indexes
    init_db()
    collection = get_database()
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')
    print(f"Found {len(records)} records to migrate")
    
    # Transform and upsert records
    inserted_count = 0
    updated_count = 0
    
    for record in records:
        baseurl = record['Auto-Discovery URL'].split('/gbfs.json')[:-1]
        gbfs_url = ''.join(baseurl)
        
        transformed_record = {
            "system_id": record['System ID'],
            "name": record['Name'],
            "location": record['Location'],
            "gbfs_url": gbfs_url,
            "auto_discovery_url": record['Auto-Discovery URL'],
            "add_json": ".json" in record['Auto-Discovery URL']
        }
        
        # Use upsert to handle duplicates
        result = collection.update_one(
            {"system_id": transformed_record["system_id"]},
            {"$set": transformed_record},
            upsert=True
        )
        
        if result.upserted_id:
            inserted_count += 1
            print(f"Inserted record: {transformed_record['system_id']} ({records.index(record)+1}/{len(records)})") # print system id and number of record out of total
        else:
            updated_count += 1
            print(f"Updated record: {transformed_record['system_id']} ({records.index(record)+1}/{len(records)})")
    print(f"Migration completed:")
    print(f"- {inserted_count} new records inserted")
    print(f"- {updated_count} existing records updated")

if __name__ == "__main__":
    migrate_csv_to_mongodb("systems.csv") 