import subprocess
import re
import matplotlib.pyplot as plt
import os
import sys

SNAPPY_COMPRESS_APP = "./compress_app"
SNAPPY_DECOMPRESS_APP = "./decompress_app"

DEFLATE_COMPRESS_SCRIPT = "/Volumes/programming/compression/DEFLATE/compress_DEFLATE.py"
DEFLATE_DECOMPRESS_SCRIPT = "/Volumes/programming/compression/DEFLATE/decompress_DEFLATE.py"

# The large dataset file
TEST_FILE = "customers-2000000.csv" 

SNAPPY_OUT_FILE = "compressed.snappy"
DEFLATE_OUT_FILE = "compressed.zlib"
RESTORED_FILE = "restored.csv"


def parse_output(output):
    """Parses all four metrics from the script's stdout."""
    try:
        time_match = re.search(r"Time Taken:.*?([\d\.]+)", output)
        size_match = re.search(r"Compressed Size:.*?(\d+)", output)
        ratio_match = re.search(r"Compression Ratio:.*?([\d\.]+)", output)

        time_taken = float(time_match.group(1)) if time_match else None
        size_bytes = float(size_match.group(1)) if size_match else None
        ratio = float(ratio_match.group(1)) if ratio_match else None
        
        return {
            "time": time_taken,
            "size": size_bytes,
            "ratio": ratio
        }
    except Exception as e:
        print(f"CRITICAL PARSING ERROR: {e}\nCould not parse output:\n{output}")
        return None

def run_benchmark(command_array):
    """Runs a command, captures its output, and parses the metrics."""
    try:
        print(f"--- Running: {' '.join(command_array)} ---")
        
        result = subprocess.run(command_array, capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        parsed_data = parse_output(result.stdout)
        
        if parsed_data and parsed_data['time'] is not None:
            print(f"--- Parsed Results: {parsed_data} --- \n")
            return parsed_data
        else:
            print(f"ERROR: Could not parse 'Time Taken' from output:\n{result.stdout}")
            return None

    except subprocess.CalledProcessError as e:
        print(f"ERROR running command: {' '.join(command_array)}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None
    except FileNotFoundError:
        print(f"ERROR: File not found. Make sure '{command_array[0]}' exists and is executable.")
        print("If it's your C++ app, did you compile it with 'g++'?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def create_charts(comp_results, decomp_results):
    """Uses matplotlib to create and save all four bar charts."""
    
    labels = ['DEFLATE (Python/zlib)', 'Snappy (C++)']

    try:
        original_size = os.path.getsize(TEST_FILE)
        original_size_mb = original_size / 1e6
        title_suffix = f"({original_size_mb:.1f} MB File)"
    except Exception:
        original_size = 1 
        original_size_mb = 0
        title_suffix = ""

    # Chart 1: Compression Time 
    times = [comp_results['deflate']['time'], comp_results['snappy']['time']]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=['#d62728', '#1f77b4'])
    plt.ylabel('Time (Seconds)')
    plt.title(f'Compression Time {title_suffix}')
    plt.yscale('log') # Use a log scale if times are very different
    plt.bar_label(bars, fmt='%.4f s')
    
    comp_graph_file = 'compression_time_graph.png'
    plt.savefig(comp_graph_file)
    print(f"Saved graph: {comp_graph_file}")
    plt.close()

    #  Chart 2: Decompression Time 
    times = [decomp_results['deflate']['time'], decomp_results['snappy']['time']]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=['#d62728', '#1f77b4'])
    plt.ylabel('Time (Seconds)')
    plt.title(f'Decompression Time {title_suffix}')
    plt.yscale('log') 
    plt.bar_label(bars, fmt='%.4f s')
    
    decomp_graph_file = 'decompression_time_graph.png'
    plt.savefig(decomp_graph_file)
    print(f"Saved graph: {decomp_graph_file}")
    plt.close()

    # Chart 3: Compressed File Size 
    labels_size = ['Original File', 'DEFLATE (Python/zlib)', 'Snappy (C++)']
    sizes = [
        original_size / 1e6,  
        comp_results['deflate']['size'] / 1e6, 
        comp_results['snappy']['size'] / 1e6  
    ]
    colors = ['#2ca02c', '#d62728', '#1f77b4'] 
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels_size, sizes, color=colors)
    plt.ylabel('File Size (Megabytes)')
    plt.title(f'File Size Comparison {title_suffix}')
    plt.bar_label(bars, fmt='%.2f MB')
    
    size_graph_file = 'compression_size_graph.png'
    plt.savefig(size_graph_file)
    print(f"Saved graph: {size_graph_file}")
    plt.close()

    # Chart 4: Compression Ratio 
    snappy_ratio = original_size / comp_results['snappy']['size']
    deflate_ratio = original_size / comp_results['deflate']['size']
    
    ratios = [deflate_ratio, snappy_ratio]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, ratios, color=['#d62728', '#1f77b4'])
    plt.ylabel('Compression Ratio (X:1)')
    plt.title(f'Compression Ratio {title_suffix}')
    plt.bar_label(bars, fmt='%.2f : 1')
    
    ratio_graph_file = 'compression_ratio_graph.png'
    plt.savefig(ratio_graph_file)
    print(f"Saved graph: {ratio_graph_file}")
    plt.close()


def main():
    required_files = [
        SNAPPY_COMPRESS_APP, SNAPPY_DECOMPRESS_APP,
        DEFLATE_COMPRESS_SCRIPT, DEFLATE_DECOMPRESS_SCRIPT,
        TEST_FILE
    ]
    
    for f in required_files:
        if not os.path.exists(f):
            print(f"Error: Missing required file: {f}")
            if f == TEST_FILE:
                print(f"Please download '{TEST_FILE}' or change the TEST_FILE variable in this script.")
            elif '.py' not in f:
                print(f"Did you compile the C++ app? (e.g., g++ snappy_compress.cpp -o {f} -lsnappy)")
            sys.exit(1)

    comp_results = {}
    decomp_results = {}

    comp_results['snappy'] = run_benchmark([SNAPPY_COMPRESS_APP, TEST_FILE, SNAPPY_OUT_FILE])
    comp_results['deflate'] = run_benchmark(["python3", DEFLATE_COMPRESS_SCRIPT, TEST_FILE, DEFLATE_OUT_FILE])
    
    decomp_results['snappy'] = run_benchmark([SNAPPY_DECOMPRESS_APP, SNAPPY_OUT_FILE, RESTORED_FILE])
    decomp_results['deflate'] = run_benchmark(["python3", DEFLATE_DECOMPRESS_SCRIPT, DEFLATE_OUT_FILE, RESTORED_FILE])

    # --- Create Charts ---
    if (comp_results.get('snappy') and comp_results.get('deflate') and
        decomp_results.get('snappy') and decomp_results.get('deflate') and
        comp_results['snappy'].get('size') and comp_results['deflate'].get('size')):
        
        create_charts(comp_results, decomp_results)
    else:
        print("Could not generate charts because one or more benchmark steps failed or metrics were not parsed.")
        print("Please check for errors above.")

    print("Benchmark complete.")

if __name__ == "__main__":
    main()