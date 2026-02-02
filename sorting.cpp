#include <set>
#include <string>
#include <chrono>
#include <iostream>
#include <random>
#include <algorithm>
#include <ips4o.hpp>

#include "cli.hpp"

template<typename SortFunc>
void execute_sort_algorithm(const int n, const int seed, const int iterations, SortFunc sort_func) {
    const auto start_generate = std::chrono::high_resolution_clock::now();

    // generates the same arrays as the python version
    std::mt19937 rng(seed);

    std::vector<int> a(n);
    for (int i = 0; i < n; i++) {
        const uint32_t r = rng();
        a[i] = static_cast<int>(r % static_cast<uint32_t>(n));
    }

    const auto end_generate = std::chrono::high_resolution_clock::now();

    const std::chrono::duration<double> elapsed_generate = end_generate - start_generate;
    std::cout << "The random generation of the array a (size=" << n << ") was done in " << elapsed_generate.count() << " s." << std::endl;

    const auto start_sort = std::chrono::high_resolution_clock::now();

    for (int x = 0; x < iterations; x++) {
        auto b = a;
        sort_func(b);
    }

    const auto end_sort = std::chrono::high_resolution_clock::now();

    const std::chrono::duration<double> elapsed_sort = end_sort - start_sort;
    std::cout << "The array a was sorted in " << elapsed_sort.count() << " s." << std::endl;
}

int main(const int argc, char **argv) {
    std::set<std::string> allowed_value_options;
    std::set<std::string> allowed_literal_options;

    allowed_value_options.insert("-n"); // size of array
    allowed_value_options.insert("-s"); // seed
    allowed_value_options.insert("-i"); // iterations
    allowed_literal_options.insert("sort");
    allowed_literal_options.insert("ips4o");

    const CommandLineArguments parsed_args = parse_args(argc, argv, allowed_value_options, allowed_literal_options, 0);

    if (!parsed_args.success) {
        return -1;
    }

    int n = 1024;
    int seed = 1;
    int iterations = 10;
    for (const auto&[name, value] : parsed_args.value_options) {
        if (name == "-n") {
            n = std::stoi(value);
        }
        if (name == "-s") {
            seed = std::stoi(value);
        }
        if (name == "-i") {
            iterations = std::stoi(value);
        }
    }

    if (parsed_args.literal_options.contains("sort")) {
        execute_sort_algorithm(n, seed, iterations, [](auto& v){std::sort(v.begin(), v.end());});
    }

    if (parsed_args.literal_options.contains("ips4o")) {
        execute_sort_algorithm(n, seed, iterations, [](auto& v){ips4o::sort(v.begin(), v.end());});
    }
}