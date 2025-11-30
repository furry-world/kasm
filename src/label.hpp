#pragma once
/**
 * label class
 *
 * For values represented by labels.
 *
 */

#include <cstdint>
#include <stdexcept>
#include <string>

using std::string;

namespace label {

class Label {
  private:
    string name;
    uint64_t value;
    bool unpopulated;

  public:
    string get_name() {
        return name;
    }

    uint64_t get_value() {
        return value;
    }

    void set_value(uint64_t _value) {
        if(is_unpopulated()) {
            value = _value;
        } else {
            throw std::invalid_argument("tried to redefine a value");
        }
    }

    bool is_unpopulated() {
        return unpopulated;
    }

    bool operator==(const Label& other) const {
        return name == other.name;
    }

    bool equals(string _name) {
        return _name == get_name();
    }


    Label(string _name) {
        name = _name;
        value = 0;
        unpopulated = true;
    }

    Label(string _name, uint64_t _value) {
        name = _name;
        value = _value;
        unpopulated = false;
    }
};

} // namespace label
