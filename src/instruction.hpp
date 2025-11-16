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
class Instruction {
  private:
    std::string mnemonic;
    std::function<std::vector<uint8_t>(std::vector<std::string>)> assemble_function;

  public:
    bool operator==(const Instruction& other) const {
        return mnemonic == other.mnemonic;
    }

    std::string get_mnemonic() {
        return mnemonic;
    };

    std::vector<uint8_t> assemble(std::vector<std::string> tokens) {
        return assemble_function(tokens);
    };

    Instruction(
        std::string _mnemonic,
        std::function<std::vector<uint8_t>(std::vector<std::string>)> _assemble) {
            mnemonic = _mnemonic;
            assemble_function = _assemble;
        }
};

} // namespace instruction
