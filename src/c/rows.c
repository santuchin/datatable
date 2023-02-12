#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef unsigned int uint;

bool any(uint* nums, uint len)
{
	for (uint i = 0; i < len; i++)
	{
		if (nums[i])
			return true;
	}

	return false;
}

uint encode(uint* nums, uint len)
{
	uint bit = 0;
	uint num = 0;

	while (any(nums, len))
	{
		for (uint i = 0; i < len; i++)
		{
			num |= (1 & nums[i]) << bit;
			nums[i] >>= 1;
			bit++;
		}
	}

	return num;
}

uint* decode(uint num, uint len)
{
	uint bit = 0;
	uint* nums = malloc(sizeof(uint) * len);

	while (num)
	{
		for (uint i = 0; i < len; i++)
		{
			nums[i] |= (1 & num) << bit;
			num >>= 1;
		}

		bit++;
	}

	return nums;
}

