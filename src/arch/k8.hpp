#pragma once
/**
 * K8 instruction class
 *
 * Used to assemble K8 code.
 */

#include "../instruction.hpp"
#include "../constants.hpp"
#include "../utils.hpp"
#include <cctype>
#include <cstdint>

using std::string;
using std::vector;

class K8_instruction : public instruction::Instruction {
    // vector<uint8_t> instruction_words(uint8_t opcode, vector<string> tokens, uint8_t num_words) {
    //     vector<uint8_t> words;
    //     words.push_back(opcode);
    //
    //     //uint8_t value = utils::
    // }

public:

    vector<uint8_t> assemble(vector<string> tokens) {
        vector<uint8_t> bytes;
        for(uint16_t i = 0; i < tokens.size(); ++i) {
            auto token = tokens[i];
            transform(token.begin(), token.end(), token.begin(), ::toupper);
            bytes.push_back(
                token == "CLL" ? 0b00000000 :
                token == "RET" ? 0b00000001 :
                token == "JMP" ? 0b00000010 :
                token == "RJP" ? 0b00000011 :
                token == "INT" ? 0b00001000 :
                token == "POP" ? 0b00100000 :
                token == "PSH" ? 0b00101000 :
                token == "NLD" ? 0b00010000 :
                token == "NST" ? 0b00011000 :

                token == "MOV" ? 0b01000000 :
                token == "ILD" ? 0b01010000 :
                token == "IST" ? 0b01011000 :
                token == "LDI" ? 0b01100000 :
                token == "LDA" ? 0b01110000 :
                token == "STR" ? 0b01111000 :

                token == "ADD" ? 0b10001000 :
                token == "SUB" ? 0b10001001 :
                token == "IOR" ? 0b10001100 :
                token == "AND" ? 0b10001110 :
                token == "XOR" ? 0b10001111 :
                token == "SRL" ? 0b10010000 :
                token == "SRR" ? 0b10011000 :

                token == "REQ" ? 0b11000000 :
                token == "RNE" ? 0b11001000 :
                token == "EQA" ? 0b11100000 :
                token == "EQI" ? 0b11110000 :
                token == "NEA" ? 0b11101000 :
                token == "NEI" ? 0b11111000 :

                utils::decode_number(token)
            );
        }

        return bytes;
    }

    K8_instruction() {}
};
