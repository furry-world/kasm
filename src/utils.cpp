#include "pesticide.hpp"

#include <cctype>
#include <string>

namespace utils {

using std::string;
using std::vector;

string trim(string input) {
    if (input.size() == 0) {
        return "";
    }

    string::size_type begin = 0;
    string::size_type end = 0;
    for (string::size_type i = 0; i < input.size(); ++i) {
        if (!isspace(input[i])) {
            begin = i;
            break;
        }
    }

    for (string::size_type i = input.size() - 1; i > 0; --i) {
        if (!isspace(input[i])) {
            end = i + 1;
            break;
        }
    }

    return input.substr(begin, end - begin);
}

vector<string> tokenize(string input) {
    string token;
    vector<string> tokens;
    for (string::size_type i = 0; i < input.size(); ++i) {
        if (!isspace(input[i])) {
            token += input[i];
        } else if (!token.empty()) {
            tokens.push_back(token);
            token = "";
        }
    }

    return tokens;
}
} // namespace utils
