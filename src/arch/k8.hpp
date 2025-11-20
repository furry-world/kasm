/**
 * K8 instruction class
 *
 * Used to assemble K8 code.
 */

#include "../instruction.hpp"
#include <cstdint>

using std::string;
using std::vector;

class K8_instruction : instruction::Instruction {
    vector<uint8_t> instruction_words(uint8_t opcode, vector<string> tokens, uint8_t num_words) {
        vector<uint8_t> words;
        words.push_back(opcode);

        //uint8_t value = utils::
    }
};
