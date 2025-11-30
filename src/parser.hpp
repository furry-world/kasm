#pragma once
/**
 * parser module
 *
 * Used for parsing files.
 */

#include <cstdint>
#include <filesystem>
#include <vector>

using std::string;
using std::vector;

namespace parser {

vector<uint8_t> parse(std::filesystem::path input_file_path);

} // namespace parser
