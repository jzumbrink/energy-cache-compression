#include <set>
#include <string>
#include <chrono>
#include <iostream>
#include <functional>
#include <random>
#include <algorithm>
#include <ips4o.hpp>
#include <thread>
#include <vector>

#include "cli.hpp"

void chase(const size_t size, const long iterations, const int seed) {
    const auto start_generate = std::chrono::high_resolution_clock::now();

    std::vector<uint32_t> next(size / sizeof(uint32_t));
    std::mt19937 rng(seed);
    iota(next.begin(), next.end(), 0);
    std::ranges::shuffle(next, rng);

    volatile uint32_t sink;
    uint32_t idx = 0;

    const auto end_generate = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> elapsed_generate = end_generate - start_generate;
    std::cout << "The initialization of data was done in " << elapsed_generate.count() << " s." << std::endl;

    const auto start_warmup = std::chrono::high_resolution_clock::now();
    // Warmup
    for (size_t i = 0; i < 1'000'000; ++i) {
        idx = next[idx];
    }
    const auto end_warmup = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> elapsed_warmup = end_warmup - start_warmup;
    std::cout << "Warmup was done in " << elapsed_warmup.count() << " s." << std::endl;

    const auto start_access = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < iterations; i++) {
        idx = next[idx];
        sink = idx;
    }

    const auto end_access = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> elapsed_access = end_access - start_access;

    std::cout << iterations << " accesses were done in " << elapsed_access.count() << " s. Last sink was " << sink << std::endl;
}

void allocate(const size_t size) {
    const auto start_allocate = std::chrono::high_resolution_clock::now();

    std::vector<uint32_t> next(size / sizeof(uint32_t));

    const auto end_allocate = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> elapsed_generate = end_allocate - start_allocate;
    std::cout << "The allocation of data was done in " << elapsed_generate.count() << " s." << std::endl;
}

void cpp_builtin_sort(const int duration_in_seconds) {
    const auto start = std::chrono::high_resolution_clock::now();
    constexpr int n = 1000000;

    long iteration = 0;

    while (true) {
        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_int_distribution dist(0, n);
        std::vector<int32_t> a;
        a.reserve(n);

        for (int32_t i = 0; i < n; i++) {
            a.push_back(dist(gen));
        }

        std::ranges::sort(a);

        iteration++;

        auto now = std::chrono::high_resolution_clock::now();
        if (std::chrono::duration<double> elapsed = now - start; elapsed.count() >= duration_in_seconds) {
            break; // 60 seconds reached
        }

    }

    std::cout << "Done " << iteration << " iterations of cpp_builtin_sort." << std::endl;
}

void addition(const int duration_in_seconds) {
    const auto start = std::chrono::high_resolution_clock::now();
    constexpr int n = 1000000;

    long iteration = 0;

    std::random_device rd;
    std::mt19937 gen(rd());

    std::uniform_int_distribution dist(0, n);
    std::vector<int32_t> a;
    a.reserve(n);

    for (int32_t i = 0; i < n; i++) {
        a.push_back(dist(gen));
    }

    while (true) {

        std::sort(a.begin(), a.end());

        iteration++;

        auto now = std::chrono::high_resolution_clock::now();
        if (std::chrono::duration<double> elapsed = now - start; elapsed.count() >= duration_in_seconds) {
            break; // 60 seconds reached
        }

    }

    std::cout << "Done " << iteration << " iterations of cpp_builtin_sort." << std::endl;
}

void ips4o_sort(const int duration_in_seconds) {
    const auto start = std::chrono::high_resolution_clock::now();
    constexpr int n = 1000000;

    long iteration = 0;

    while (true) {
        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_int_distribution dist(0, n);
        std::vector<int32_t> a;
        a.reserve(n);

        for (int32_t i = 0; i < n; i++) {
            a.push_back(dist(gen));
        }

        ips4o::sort(a.begin(), a.end());

        iteration++;

        auto now = std::chrono::high_resolution_clock::now();
        if (std::chrono::duration<double> elapsed = now - start; elapsed.count() >= duration_in_seconds) {
            break; // 60 seconds reached
        }

    }

    std::cout << "Done " << iteration << " iterations of ips4o." << std::endl;
}

void sleep(const int duration_in_seconds) {
    std::this_thread::sleep_for(std::chrono::seconds(duration_in_seconds));
}

void io_intensive(const int duration_in_seconds) {
    const auto start = std::chrono::high_resolution_clock::now();
    constexpr int n = 100;

    long iteration = 0;

    while (true) {

        for (int x = 0; x < n; x++) {
            std::cout << "Hello World" << std::endl;
        }

        iteration++;

        auto now = std::chrono::high_resolution_clock::now();
        if (std::chrono::duration<double> elapsed = now - start; elapsed.count() >= duration_in_seconds) {
            break; // 60 seconds reached
        }

    }

    std::cout << "Done " << iteration << " iterations of ips4o." << std::endl;
}

int main(const int argc, char **argv) {
    std::set<std::string> allowed_value_options;
    std::set<std::string> allowed_literal_options;

    allowed_value_options.insert("-d"); // duration in seconds, standard is 10
    allowed_value_options.insert("-i"); // iterations, standard is 10
    allowed_value_options.insert("--size"); // size of pointer chasing, standard is 256 * 1024 * 1024
    allowed_value_options.insert("--seed");
    allowed_literal_options.insert("chase");
    allowed_literal_options.insert("sort");
    allowed_literal_options.insert("ips4o");
    allowed_literal_options.insert("sleep");
    allowed_literal_options.insert("io");
    allowed_literal_options.insert("allocate");

    CommandLineArguments parsed_args = parse_args(argc, argv, allowed_value_options, allowed_literal_options, 0);

    if (!parsed_args.success) {
        return -1;
    }

    int duration_in_seconds = 10;
    long iterations = 10;
    size_t size = 256 * 1024 * 1024;
    int seed = 42;
    for (const auto&[name, value] : parsed_args.value_options) {
        if (name == "-d") {
            duration_in_seconds = std::stoi(value);
        }
        if (name == "-i") {
            iterations = std::stol(value);
        }
        if (name == "--size") {
            size = std::stol(value);
        }
        if (name == "--size") {
            seed = std::stoi(value);
        }
    }

    // start algorithms
    if (parsed_args.literal_options.contains("chase")) {
        chase(size, iterations, seed);
    }

    if (parsed_args.literal_options.contains("sort")) {
        cpp_builtin_sort(duration_in_seconds);
    }

    if (parsed_args.literal_options.contains("ips4o")) {
        ips4o_sort(duration_in_seconds);
    }

    if (parsed_args.literal_options.contains("sleep")) {
        sleep(duration_in_seconds);
    }

    if (parsed_args.literal_options.contains("io")) {
        io_intensive(duration_in_seconds);
    }

    if (parsed_args.literal_options.contains("allocate")) {
        allocate(size);
    }
}
