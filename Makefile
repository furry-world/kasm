files	= src/*.cpp src/*.hpp
opts	= -std=c++23

kasm: $(files)
	g++ -o kasm $(files) $(opts)
