#include <stdio.h>
#include <stdlib.h>

typedef unsigned int uint;

typedef struct
{
	uint len;
	uint rows;
	char* data;
}
table;

table open(char* path);

void save(table self, char* path)
{
	FILE* fp = fopen(path, "wb");
	
	uint row = 0;

	for (uint i = 0; row < self.rows; i++)
	{
		putc(self.data[i], fp);	

		if ('\0' == self.data[i])
			row++;
	}

	fclose(fp);
}

void add(table self, char* row);

void set(table self, uint index, char* row);
void ins(table self, uint index, char* row);
void del(table self, uint index);

char* get(table self, uint index)
{
	uint row = 0;

	for (uint i = 0; row < self.rows; i++)
	{
		if (row == index)
			return &(self.data[i]);

		else if (!(self.data[i]))
			row++;
	}

	exit(1);
}

int main()
{
	table db = {3, 3, "hello world\0dojaaan\0a2\0addd"};
	
	save(db, "./table.db");	

	return 0;
}

