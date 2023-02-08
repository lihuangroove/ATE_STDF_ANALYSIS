// pch.h: 这是预编译标头文件。
// 下方列出的文件仅编译一次，提高了将来生成的生成性能。
// 这还将影响 IntelliSense 性能，包括代码完成和许多代码浏览功能。
// 但是，如果此处列出的文件中的任何一个在生成之间有更新，它们全部都将被重新编译。
// 请勿在此处添加要频繁更新的文件，这将使得性能优势无效。

#ifndef PCH_H
#define PCH_H

// 添加要在此处预编译的标头
#include "framework.h"
#include "stdf_file/stdf_v4_file.h"
#include <vector>
#include <ctime>
#include <string>
#include <windows.h>
#include <sstream>
#include <math.h>

/*
	TODO: 存在一种STDF, 
*/

enum CPLUS_STDF_ERROR :int
{
	CSV_FAIL = 0x8,  // CSV文件生成错误
	SUCCESS = 0x0,
	PATH_FAIL = 0x7, // 路径错误
	TYPE_ERROR = 0x6,  // 类型错误
	NO_NEED_TYPE = 0x5,  // 不懂的类型
	STDF_ERROR = 0x4,  // 没载入STDF
};

class Cplus_stdf
{
public:
	Cplus_stdf();
	~Cplus_stdf();

	bool Clear();
	bool ParserStdfToHdf5(const wchar_t*, const char* cache_path);
	int GetFinishT(void);
private:
	STDF_FILE* stdf_file;

};


#endif //PCH_H
