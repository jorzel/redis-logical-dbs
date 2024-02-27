import redis
import time
import random
import string


def populate_db(host, port, db_number, key_prefix, n):
    r = redis.Redis(host=host, port=port, db=db_number)

    # Generate and load random data into Redis
    for i in range(n):
        suffix = ''.join(random.choices(string.ascii_letters, k=5))
        key = f"{key_prefix}{suffix}"
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        r.set(key, value)  # Set key-value pair in Redis

    print("Data loaded into Redis.")


def scan_redis_by_pattern(host, port, db_number, pattern):
    # Connect to Redis
    r = redis.Redis(host=host, port=port, db=db_number)

    num_keys = r.dbsize()
    print("Number of keys:", num_keys)
    # Initialize cursor
    cursor = 0

    # Scan keys matching pattern
    keys = []
    while True:
        cursor, partial_keys = r.scan(cursor, match=pattern)
        keys.extend(partial_keys)
        if cursor == 0:
            break

    return keys


host = 'localhost'
port = 6379
pattern = 'active_user_id:*'
db_number = 0

populate_db(host, port, db_number, "active_user_id:", 1)
populate_db(host, port, db_number, "user_id:", 10)
start = time.time()
keys = scan_redis_by_pattern(host, port, db_number, pattern)
print(f"DB: {db_number}, Keys: {keys}, Duration: {time.time() - start}s")

populate_db(host, port, db_number, "user_id:", 1000)
start = time.time()
keys = scan_redis_by_pattern(host, port, db_number, pattern)
print(f"DB: {db_number}, Keys: {keys}, Duration: {time.time() - start}s")

populate_db(host, port, db_number, "user_id:", 100000)
start = time.time()
keys = scan_redis_by_pattern(host, port, db_number, pattern)
print(f"DB: {db_number}, Keys: {keys}, Duration: {time.time() - start}s")

db_number = 1
populate_db(host, port, db_number, "active_user_id:", 1)
start = time.time()
keys = scan_redis_by_pattern(host, port, db_number, pattern)
print(f"DB: {db_number}, Keys: {keys}, Duration: {time.time() - start}s")