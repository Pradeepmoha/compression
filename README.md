# Optimizing E-Commerce Latency: A Comparative Performance Analysis of Snappy and DEFLATE

## Overview

This project provides a hands-on benchmark and analysis comparing the high-speed Snappy algorithm against the high-compression DEFLATE (zlib) algorithm. The goal is to determine the best compression strategy for a modern e-commerce platform, where data is "big and fast."

## Problem Statement

Modern e-commerce platforms (like Amazon or Flipkart) must process massive, continuous streams of text-based data, including:

- Large product catalogs (.csv, .json)
- Real-time user session data
- High-velocity transaction logs

Traditional compression algorithms like DEFLATE (used by gzip and .zip) are slow. They are "CPU-bound" and create a performance bottleneck. In e-commerce, this bottleneck translates directly to user-facing lag and lost revenue.

This project proposes Snappy as a solution. Snappy is a modern library from Google designed for extreme speed over raw compression size. We hypothesize that Snappy's speed advantage will make it the superior choice for a latency-sensitive e-commerce backend.

## Key Findings: Benchmark Results

The algorithms were benchmarked on a 349.4 MB `customers-2000000.csv` dataset to simulate a real-world e-commerce product catalog.

**The results are definitive:** Snappy is 3.6x faster at compression and provides the speed needed for a real-time system, while DEFLATE is optimized for storage, not speed.

| Metric | DEFLATE (Python/zlib) | Snappy (C++) | Winner |
|--------|----------------------|--------------|--------|
| Compression Time | 10.62 seconds | 2.93 seconds | **Snappy (3.6x Faster)** |
| Decompression Time | 1.01 seconds | 0.90 seconds | **Snappy (1.1x Faster)** |
| Compression Ratio | 2.13:1 | 1.38:1 | DEFLATE |
| Final File Size | 164.0 MB | 253.4 MB | DEFLATE |

## Visual Results (Benchmark Graphs)

The data clearly shows the fundamental trade-off: DEFLATE wins on file size, but Snappy wins on speed.

**Graph 1: Compression Time (The CPU Bottleneck)**

This graph shows that DEFLATE takes over 10 seconds to compress the file, making it unsuitable for real-time data. Snappy is 3.6 times faster.

**Graph 2: Decompression Time (The "User Lag")**

This graph shows the "read" speed. Snappy is faster, providing a snappier user experience when loading data.

**Graph 3: File Size (The Trade-Off)**

This graph shows the "cost" of using Snappy. The final file is larger, but as the time graphs show, this is the price we pay for speed.

**Graph 4: Compression Ratio**

This graph confirms that DEFLATE is more efficient at compression (2.13:1) than Snappy (1.38:1).

## How They Work: Algorithmic Architecture

The performance difference comes from their fundamental design.

### DEFLATE (Slow, Two-Stage Process)

DEFLATE is "heavy" because it's a two-stage algorithm. It's slow but creates a tiny file.

- **Stage 1 (LZ77):** Finds repeating data.
- **Stage 2 (Huffman Coding):** Takes the result of Stage 1 and re-compresses it using a complex, CPU-heavy bit-stream.

### Snappy (Fast, One-Stage Process)

Snappy is "lightweight" because it's a one-stage algorithm. It's fast but creates a larger file.

- **Stage 1 (Fast LZ77):** Finds repeating data (and ignores small repeats).
- **Stops Here:** It skips the slow Huffman stage and outputs a simple byte-stream that a CPU can read very quickly.

## How to Run This Benchmark

This repository contains the C++ and Python scripts needed to replicate this benchmark.

### Prerequisites

- A macOS or Linux system
- g++ compiler (or clang++)
- python3 and pip3
- The `customers-2000000.csv` dataset (349.4 MB)

### Step 1: Install Dependencies

Install the Snappy C++ library and the Python matplotlib library for your operating system.

#### macOS (using Homebrew)
```bash
brew install snappy
pip3 install matplotlib python-snappy
```

#### Ubuntu/Debian (using apt)
```bash
sudo apt-get update
sudo apt-get install libsnappy-dev
pip3 install matplotlib python-snappy
```


#### Alpine Linux (using apk)
```bash
apk add snappy-dev
pip3 install matplotlib python-snappy
```

#### Windows (using vcpkg or pre-built binaries)

**Option 1: Using vcpkg (Recommended)**
```bash
# Clone vcpkg if you don't have it
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg

# Bootstrap vcpkg
.\bootstrap-vcpkg.bat

# Install Snappy for x64 Windows
.\vcpkg install snappy:x64-windows

# If you need x86 instead
.\vcpkg install snappy:x86-windows

# Integrate vcpkg with Visual Studio (optional)
.\vcpkg integrate install
```

**Option 2: Using pre-built binaries**

1. Download pre-built Snappy binaries from [Google's Snappy GitHub Releases](https://github.com/google/snappy/releases)
2. Extract the binaries to a known location (e.g., `C:\snappy\`)
3. Add the Snappy library path to your compiler flags when building:
   ```bash
   g++ snappy_compress.cpp -o compress_app -IC:\snappy\include -LC:\snappy\lib -lsnappy
   ```

**Option 3: Build from source on Windows (with Visual Studio)**

```bash
# Clone the Snappy repository
git clone https://github.com/google/snappy.git
cd snappy

# Create a build directory
mkdir build
cd build

# Configure with CMake (requires Visual Studio to be installed)
cmake .. -G "Visual Studio 16 2019" -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build . --config Release

# The compiled libraries will be in the Release folder
```

**Install Python dependencies on Windows:**
```bash
pip3 install matplotlib python-snappy
```

### Step 2: Compile the C++ Programs

This benchmark uses C++ for Snappy to test its native speed. Compile the apps:

```bash
# Compile the C++ compressor
g++ snappy_compress.cpp -o compress_app -lsnappy

# Compile the C++ decompressor
g++ snappy_decompress.cpp -o decompress_app -lsnappy

# Make them executable (Fixes "Permission Denied" errors) 
chmod +x compress_app
chmod +x decompress_app
```

### Step 3: Run the Full Benchmark

Make sure your 349.4 MB dataset `customers-2000000.csv` is in the same folder.

The `generate_benchmark_graphs.py` script will automatically run all four C++ and Python scripts, parse their output, and generate four .png graphs.

```bash
python3 generate_benchmark_graphs.py
```

## Conclusion

**For an e-commerce application, speed is more important than storage.**

The benchmark results prove that DEFLATE's 10.6-second compression time is an unacceptable performance bottleneck. The 2.9-second time from Snappy is 3.6 times faster and suitable for a real-time backend.

### Recommendations

We recommend using Snappy for all internal, real-time data, including:

- In-memory cache data (e.g., Redis)
- Database compression (e.g., MongoDB)
- Real-time logging and analytics pipelines (e.g., Kafka, Spark)

The small "cost" of a larger file size (253 MB vs. 164 MB) is a worthwhile trade-off to eliminate latency and provide a fast, responsive experience for the user.

## Repository Structure

```
/Volumes/programming/compression/
├── README.md                          # This file
├── generate_benchmark_graphs.py       # Main benchmark driver
├── DEFLATE/
│   ├── compress_DEFLATE.py
│   └── decompress_DEFLATE.py
├── snappy_compress.cpp                # Snappy C++ implementation
├── snappy_decompress.cpp              # Snappy C++ implementation
├── compress_app                       # Compiled Snappy compressor (after build)
├── decompress_app                     # Compiled Snappy decompressor (after build)
└── customers-2000000.csv              # Test dataset (not included)
```

