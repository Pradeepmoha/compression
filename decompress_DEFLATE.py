import zlib
import sys
import time  

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <compressed_file> <output_file>")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# 1. Read compressed data
with open(input_filename, "rb") as f:
    compressed_data = f.read()

start_time = time.time()

# 2. Decompress
try:
    decompressed_data = zlib.decompress(compressed_data)
except:
    print("Error: File is not a valid DEFLATE compressed file.")
    sys.exit(1)

end_time = time.time()
decompression_time = end_time - start_time

# 3. Write output
with open(output_filename, "wb") as f:
    f.write(decompressed_data)

# 4. Print result details
print(f"Successfully decompressed to: {output_filename}")
print(f"Output Size: {len(decompressed_data)} bytes")
print(f"Time Taken:  {decompression_time:.4f} seconds")