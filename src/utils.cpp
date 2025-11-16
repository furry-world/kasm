#include "pesticide.hpp"

#include <string>
#include <cctype>

namespace utils {
    std::string trim(std::string input) {
        if (input.size() == 0) {
            return "";
        }

        std::string::size_type begin = 0;
        std::string::size_type end = 0;
        for (std::string::size_type i = 0; i < input.size(); ++i) {
            if (!std::isspace(input[i])) {
                begin = i;
                break;
            }
        }

        for (std::string::size_type i = input.size() - 1; i > 0; --i) {
            if (!std::isspace(input[i])) {
                end = i + 1;
                break;
            }
        }

        return input.substr(begin, end - begin);
    }

    std::vector<std::string> tokenize(std::string input) {
        std::string token;
        std::vector<std::string> tokens;
        for (std::string::size_type i = 0; i < input.size(); ++i) {
            if (!std::isspace(input[i])) {
                token += input[i];
            } else if (!token.empty()) {
                tokens.push_back(token);
                token = "";
            }
        }

        return tokens;
    }
}
