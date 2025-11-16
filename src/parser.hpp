/**
 * parser module
 *
 * Used for parsing files.
 */

#include <cstdint>
#include <vector>
#include <filesystem>

namespace parser {
    std::vector<std::uint8_t> parse(std::filesystem::path input_file_path);
}
