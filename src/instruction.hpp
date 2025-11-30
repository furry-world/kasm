#pragma once
/**
 * instruction intermediary class
 *
 * An intermediary class that defines what an instruction class needs to
 * contain. This is so we can support multiple architectures.
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

  public:

    vector<uint8_t> assemble(vector<string> tokens);

    Instruction() {}
};

} // namespace instruction
