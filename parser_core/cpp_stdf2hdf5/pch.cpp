// pch.cpp: 与预编译标头对应的源文件

#include "pch.h"
// 当使用预编译的头时，需要使用此源文件，编译才能成功。

Cplus_stdf::Cplus_stdf()
{
	stdf_file = nullptr;
}

Cplus_stdf::~Cplus_stdf()
{
	if (stdf_file)
	{
		delete stdf_file;
		stdf_file = nullptr;
	}
}

bool Cplus_stdf::Clear()
{
	if (stdf_file)
	{
		delete stdf_file;
		stdf_file = nullptr;
	}

	return true;
}

int Cplus_stdf::GetFinishT(void)
{
	if (stdf_file)
	{
		return stdf_file->get_mrr_finish();
	}
	return 0;
}


bool Cplus_stdf::ParserStdfToHdf5(const wchar_t* filename,const char* cache_path)
{

	Clear();
	stdf_file = new STDF_FILE();

	int ret = stdf_file->parser_to_hdf5(filename, cache_path);

	delete stdf_file;
	stdf_file = nullptr;
	if (ret != 0)
	{
		return false;
	}
	return true;
}
