files	= src/*.cpp src/*.hpp
opts	=

kasm: $(files)
	g++ -o kasm -std=c++23 $(files) $(opts)
