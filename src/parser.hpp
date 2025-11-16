/**
 * parser module
 *
 * Used for parsing files.
 */

#include <cstdint>
#include <filesystem>
#include <vector>

namespace parser {

std::vector<uint8_t> parse(std::filesystem::path input_file_path);

}
