/**
 * utils
 *
 * Random utils because C++ lacks a lot of these functions. Oh well.
 */

#include <string>
#include <vector>

using std::string;
using std::vector;

namespace utils {

string trim(string input);
vector<string> tokenize(string input);

} // namespace utils
