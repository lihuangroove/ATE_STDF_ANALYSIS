// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

// 临时使用CSV, 后续使用pybind11_numpy(easy) / hdf5
extern "C"  _declspec(dllexport) Cplus_stdf * NewStdf() { return new Cplus_stdf(); }; // 新类
extern "C"  _declspec(dllexport) void DeleteStdf(Cplus_stdf * stdf) { stdf->Clear(); delete stdf; stdf = nullptr; }; // 删除类
extern "C"  _declspec(dllexport) bool ParserStdfToHdf5(Cplus_stdf * stdf, wchar_t* filename, const char* file_path) { return stdf->ParserStdfToHdf5(filename, file_path); };
extern "C"  _declspec(dllexport) int GetFinishT(Cplus_stdf * stdf) { return stdf->GetFinishT(); };
