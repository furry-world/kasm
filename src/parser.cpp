#include "parser.hpp"
#include "instruction.hpp"
#include "strings.hpp"
#include "constants.hpp"
#include "utils.hpp"

#include "arch/k8.hpp"

#include "pesticide.hpp"

#include <exception>
#include <stdexcept>
#include <string>
#include <fstream>
#include <iostream>

namespace parser {

using std::exception;
using std::ifstream;
using std::string;
using std::vector;

vector<string> read_file(std::filesystem::path input_file_path) {
    ifstream input_file(input_file_path);
    if (!input_file.is_open()) {
        throw std::invalid_argument ("Error while opening file");
    }

    vector<string> file_contents;

    string line;
    while (getline(input_file, line)) {
        file_contents.push_back(line);
    }

    input_file.close();
    return file_contents;
}

vector<uint8_t> parse(std::filesystem::path input_file_path) {
    vector<string> file_lines;
    try {
        file_lines = read_file(input_file_path);
    } catch (exception e) {
        std::cerr << STRINGS_ERROR_PREFIX "Unable to open file "
                  << input_file_path << std::endl;
    }

    vector<uint8_t> bytes;
    auto isa_holder = K8_instruction();

    for (uint32_t i = 0; i < file_lines.size(); ++i) {
        auto line = file_lines[i];
        string::size_type line_end_pos = line.find(COMMENT_INITIATOR);

        if (line_end_pos == string::npos) {
            line_end_pos = line.size();
        }

        line = line.substr(0, line_end_pos);
        line = utils::trim(line);

        auto tokens = utils::tokenize(line);
        auto bytes_to_add = isa_holder.assemble(tokens);
        for (uint16_t j = 0; j < bytes_to_add.size(); ++j) {
            bytes.push_back(bytes_to_add[j]);
        }
    }

    return bytes;
}

} // namespace parser
