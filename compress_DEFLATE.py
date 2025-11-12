import zlib
import sys
import os
import time    # <-- for measuring time

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# 1. Read file
with open(input_filename, "rb") as f:
    original_data = f.read()

# Start timer
start_time = time.time()

# 2. Compress using DEFLATE (zlib wrapper stream)
compressed_data = zlib.compress(original_data, level=9)

# Stop timer
end_time = time.time()
compression_time = end_time - start_time

# 3. Write output
with open(output_filename, "wb") as f:
    f.write(compressed_data)

# 4. Print compression ratio
original_size = len(original_data)
compressed_size = len(compressed_data)
ratio = (original_size / compressed_size) if compressed_size > 0 else 1.0

print(f"Successfully compressed: {input_filename}")
print(f"Original Size:       {original_size} bytes")
print(f"Compressed Size:     {compressed_size} bytes")
print(f"Compression Ratio:   {ratio:.2f}:1")
print(f"Time Taken:          {compression_time:.4f} seconds")