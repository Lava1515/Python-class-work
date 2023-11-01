import hashlib

target_hash = "EC9C0F7EDCC18A98B1F31853B1813301"
# 0871396884
for i in range(10 ** 10):
    input_string = f"{i:010}"
    print(input_string)

    hash_attempt = hashlib.md5(input_string.encode()).hexdigest()

    # Check if the hash matches the target hash
    if hash_attempt == target_hash:
        print(f"Original input: {input_string}")
        break