# ifndef CLI_HPP
# define CLI_HPP

#include <vector>
#include <iostream>
#include <set>

struct Option {
    std::string name;
    std::string value;
};

struct CommandLineArguments {
    std::string command;
    std::vector<std::string> last_parameter;
    std::vector<Option> value_options;
    std::set<std::string> literal_options;
    bool success;
};

const CommandLineArguments FAILURE = {std::string(), std::vector<std::string>(), std::vector<Option>(), std::set<std::string>(), false};

inline CommandLineArguments parse_args(const int argc, char** argv, std::set<std::string> const &allowed_value_options, std::set<std::string> const &allowed_literal_options, const int fixed_parameter_count) {
    if (argc < fixed_parameter_count + 1) {
        return FAILURE;
    }

    const std::string command = argv[0];
    std::vector<Option> value_options;
    std::set<std::string> literal_options;

    std::set<std::string> found;
    int i = 1;
    while(i < argc - fixed_parameter_count) { // parse options
        std::string option = argv[i++];

        if (found.count(option) == 1) {
            std::cout << "Error: duplicate occurrence of option " << option << "." << std::endl;
            return FAILURE;
        }

        if (allowed_value_options.count(option) == 1) {
            if (i > argc - 1) {
                std::cout << "Error: missing parameter after the " << option << " option." << std::endl;
                return FAILURE;
            }
            const std::string value = argv[i++];
            value_options.push_back({option, value});
            found.insert(option);
        } else if (allowed_literal_options.count(option) == 1) {
            literal_options.insert(option);
            found.insert(option);
        } else { // unknown option provided
            std::cout << "Error: unknown option " << option << "." << std::endl;
            return FAILURE;
        }
    }

    if (i >= argc && fixed_parameter_count > 0) {
        std::cout << "Error: missing parameter" << std::endl;
        return FAILURE;
    }

    std::vector<std::string> last_parameter;
    last_parameter.reserve(fixed_parameter_count);
    while(i < argc) {
        last_parameter.emplace_back(argv[i++]);
    }

    return {command, last_parameter, value_options, literal_options, true};
}

# endif