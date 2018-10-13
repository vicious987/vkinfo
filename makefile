.PHONY: clean

vkinfo: vkinfo.cpp
	g++ $< -ldl -lvulkan -o $@

clean:
	rm -f vkinfo
