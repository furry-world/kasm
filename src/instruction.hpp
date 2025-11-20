/**
 * instruction abstract class
 *
 * An abstract class that defines what an instruction class needs to contain.
 * This is so we can support multiple architectures.
 *
 */

#include <bits/stdc++.h>
#include <cstdint>
#include <string>
#include <vector>

namespace instruction {

using std::function;
using std::string;
using std::vector;

class Instruction {

  private:
    string mnemonic;
    function<vector<uint8_t>(vector<string>)> assemble_function;

  public:
    bool operator==(const Instruction& other) const {
        return mnemonic == other.mnemonic;
    }

    string get_mnemonic() {
        return mnemonic;
    };

    vector<uint8_t> assemble(vector<string> tokens) {
        return assemble_function(tokens);
    };

    Instruction(
        string _mnemonic,
        function<vector<uint8_t>(vector<string>)> _assemble) {
            mnemonic = _mnemonic;
            assemble_function = _assemble;
        }
};

} // namespace instruction
