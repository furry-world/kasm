/**
 * utils
 *
 * Random utils because C++ lacks a lot of these functions. Oh well.
 */

#include <cstdint>
#include <string>
#include <vector>

using std::string;
using std::vector;

namespace utils {

string trim(string input);
vector<string> tokenize(string input);
vector<uint8_t> number_to_words(uint64_t value, uint16_t num_words, uint8_t word_size, bool is_little_endian);
//uint64_t decode_value(string token, vector<)

} // namespace utils
