# The script provided calculates the SHA-256 hash value of a given ROM file.
import hashlib

def sha256_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

rom_file_path = "ROM/sf2sc.bin"
hash_value = sha256_checksum(rom_file_path)
print(f"The SHA-256 hash value of the ROM file is: {hash_value}")
