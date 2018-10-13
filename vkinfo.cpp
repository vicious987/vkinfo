#include <iostream>
#include <vulkan/vulkan.h>

int main(int argc, char* argv[])
{
	VkApplicationInfo appInfo = {};
	appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
	appInfo.pApplicationName = "Hello";
	appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
	appInfo.pEngineName = "None";
	appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
	appInfo.apiVersion = VK_API_VERSION_1_0;

	VkInstanceCreateInfo createInfo = {};
	createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
	createInfo.pApplicationInfo = &appInfo;
	createInfo.enabledLayerCount = 0;

	VkInstance instance;
	VkResult result = vkCreateInstance(&createInfo, nullptr, &instance);

	if (vkCreateInstance(&createInfo, nullptr, &instance) != VK_SUCCESS) {
		std::cerr << "Failed to create instance!" << std::endl;
		vkDestroyInstance(instance, nullptr);
		return 1;
	}

	uint32_t instance_version = VK_API_VERSION_1_0;
	vkEnumerateInstanceVersion(&instance_version);

	const uint32_t major = VK_VERSION_MAJOR(instance_version);
	const uint32_t minor = VK_VERSION_MINOR(instance_version);
	constexpr uint32_t patch = VK_VERSION_PATCH(VK_HEADER_VERSION);

	std::cout << "Version: " << major << "." << minor << "." << patch << std::endl;

	uint32_t gpu_count = 0;
	const auto err = vkEnumeratePhysicalDevices(instance, &gpu_count, nullptr);

	if (err != VK_SUCCESS) {
		std::cerr << "VK_ERROR_INITIALIZATION_FAILED = " << VK_ERROR_INITIALIZATION_FAILED << std::endl;
		std::cerr << "err: " << err << std::endl;
	} else {
		std::cout << "device count: " << gpu_count << std::endl;
	}

	vkDestroyInstance(instance, nullptr);

	return err;
}
