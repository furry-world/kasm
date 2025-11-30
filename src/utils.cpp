#include "utils.hpp"

#include "pesticide.hpp"

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <string>

namespace utils {

using label::Label;
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
    if (!token.empty()) { tokens.push_back(token); }

    return tokens;
}

vector<uint8_t> number_to_words(uint64_t value, uint16_t num_words,
                                uint8_t word_size, bool is_little_endian) {
    vector<uint8_t> words;
    uint64_t temp_value = value;
    for (uint16_t i = 0; i < num_words; ++i) {
        uint8_t word = temp_value & ((1 << word_size) - 1);
        temp_value >>= word_size;
        words.push_back(word);
    }

    if (is_little_endian) {
        std::reverse(words.begin(), words.end());
    }

    return words;
}

uint64_t decode_value(string token, vector<Label> &labels) {

    bool found = false;
    uint64_t value;
    for (uint16_t i = 0; i < labels.size(); ++i) {
        Label label = labels[i];

        if(label.equals(token)) {
            value = label.get_value();
            found = true;
            break;
        }
    }

    if (!found) {
        try {
            value = decode_number(token);
        } catch (std::exception e) {
            throw std::invalid_argument("unknown value");
        }

    }

    return value;
}

uint64_t decode_number(string token) {
    //TODO: implement number base handling manually
    return (uint64_t) std::stoull(token.c_str(), nullptr, 0);
}

} // namespace utils
