/**
 * utils
 *
 * Random utils because C++ lacks a lot of these functions. Oh well.
 */

#include <string>
#include <vector>

namespace utils {
    std::string trim(std::string input);
    std::vector<std::string> tokenize(std::string input);
}
