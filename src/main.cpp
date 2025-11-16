#include "pesticide.hpp"

#include "strings.hpp"
#include "parser.hpp"

#include <iostream>
#include <fstream>
#include <filesystem>
#include <args.hxx>

int main(int argc, char **argv)
{
    args::ArgumentParser argument_parser(PROJECT_DESCRIPTION_LONG);
    args::HelpFlag help(argument_parser, "help", "Display this help menu", {'h', "help"});
    args::ValueFlag<std::string> output_filename(argument_parser, "output", "Set output file name", {'o', "output"});
    args::Positional<std::string> input_filename(argument_parser, "input", "Set input file name");
    args::CompletionFlag completion(argument_parser, {"complete"});
    try
    {
        argument_parser.ParseCLI(argc, argv);
    }
    catch (const args::Completion& e)
    {
        std::cout << e.what();
        return 0;
    }
    catch (const args::Help&)
    {
        std::cout << argument_parser;
        return 0;
    }
    catch (const args::ParseError& e)
    {
        std::cerr << e.what() << std::endl;
        std::cerr << argument_parser;
        return 1;
    }

    std::filesystem::path input_file_path;
    std::filesystem::path output_file_path;

    if (input_filename) {
        input_file_path = std::filesystem::path(args::get(input_filename).c_str());
    } else {
        std::cerr << STRINGS_ERROR_PREFIX "You need to specify an input file." << std::endl;
        std::cout << argument_parser;
        return 1;
    }

    if (output_filename) {
        output_file_path = std::filesystem::path(args::get(output_filename).c_str());
    } else {
        output_file_path = std::filesystem::path(args::get(input_filename).c_str());
        output_file_path.replace_extension(".out");
    }

    std::ofstream output_file (output_file_path);
    if (output_file) {
        auto data = parser::parse(input_file_path);
        for (int i = 0; i < data.size(); ++i) {
            output_file << data[i];
        }
        output_file.close();
    } else {
        std::cerr << STRINGS_ERROR_PREFIX "Unable to open output file for writing." << std::endl;
        return 1;
    }

    return 0;
}
