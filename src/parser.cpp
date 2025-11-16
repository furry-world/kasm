#include "parser.hpp"
#include "strings.hpp"
#include "constants.hpp"
#include "utils.hpp"

#include "pesticide.hpp"

#include <stdexcept>
#include <string>
#include <fstream>
#include <iostream>

namespace parser {

std::vector<std::string> read_file(std::filesystem::path input_file_path) {
    std::ifstream input_file(input_file_path);
    if (!input_file.is_open()) {
        throw std::invalid_argument ("Error while opening file");
    }

    std::vector<std::string> file_contents;

    std::string line;
    while (getline(input_file, line)) {
        file_contents.push_back(line);
    }

    input_file.close();
    return file_contents;
}

std::vector<uint8_t> parse(std::filesystem::path input_file_path) {
    std::vector<std::string> file_lines;
    try {
        file_lines = read_file(input_file_path);
    } catch (std::exception e) {
        std::cerr << STRINGS_ERROR_PREFIX "Unable to open file "
                  << input_file_path << std::endl;
    }

    std::vector<uint8_t> bytes;

    for (int i = 0; i < file_lines.size(); ++i) {
        auto line = file_lines[i];
        std::string::size_type line_end_pos = line.find(COMMENT_INITIATOR);

        if (line_end_pos == std::string::npos) {
            line_end_pos = line.size();
        }

        line = line.substr(0, line_end_pos);
        line = utils::trim(line);

        auto tokens = utils::tokenize(line);
        for (int j = 0; j < tokens.size(); ++j) {
            pesticide_print(tokens[j]);
        }


        for (int j = 0; j < line.size(); ++j) {
            bytes.push_back(line[j]);
        }
        bytes.push_back('\n');
    }

    return bytes;
}

} // namespace parser
