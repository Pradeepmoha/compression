#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <snappy.h>
#include <iomanip>      
#include <chrono>       // For the time library

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>" << std::endl;
        return 1;
    }

    std::string input_filename = argv[1];
    std::string output_filename = argv[2];

    // 1. Read the whole input file into a string
    std::ifstream input_file(input_filename.c_str(), std::ios::binary);
    if (!input_file) {
        std::cerr << "Error: Cannot open input file: " << input_filename << std::endl;
        return 1;
    }
    
    std::stringstream buffer;
    buffer << input_file.rdbuf();
    std::string original_data = buffer.str();
    input_file.close();

    // 2. Compress the data
    auto start_time = std::chrono::high_resolution_clock::now(); // Start timer
    
    std::string compressed_data;
    snappy::Compress(original_data.data(), original_data.size(), &compressed_data);
    
    auto end_time = std::chrono::high_resolution_clock::now();   // Stop timer

    // 3. Write the compressed data to the output file
    std::ofstream output_file(output_filename.c_str(), std::ios::binary);
    if (!output_file) {
        std::cerr << "Error: Cannot open output file: " << output_filename << std::endl;
        return 1;
    }
    
    output_file.write(compressed_data.data(), compressed_data.size());
    output_file.close();

    // 4. Calculate compression ratio
    double original_size = original_data.size();
    double compressed_size = compressed_data.size();
    double ratio = (compressed_size > 0) ? (original_size / compressed_size) : 1.0;
    
    // 5. Calculate time taken in seconds <-- MODIFIED
    std::chrono::duration<double> duration_s = end_time - start_time;

    // 6. Print the updated message
    std::cout << "Successfully compressed " << input_filename << std::endl;
    std::cout << "Original Size:    " << original_size << " bytes" << std::endl;
    std::cout << "Compressed Size:  " << compressed_size << " bytes" << std::endl;
    
    // Set precision for ratio and time
    std::cout << std::fixed; 
    std::cout << "Time Taken:         " << std::setprecision(6) << duration_s.count() << " s" << std::endl; // <-- MODIFIED (added precision for small numbers)
    std::cout << "Compression Ratio:  " << std::setprecision(2) << ratio << ":1" << std::endl;

    return 0;
}