/****************************************************************************

****************************************************************************/
#include <pch.h>


int main()
{

	Cplus_stdf* new_stdf = new Cplus_stdf();
	// new_stdf->ParserStdfToHdf5(TEXT("D:\\SWAP\\TEST_DATA.std"));
	new_stdf->ParserStdfToHdf5(TEXT("D:\\SWAP\\TE\\DEMO_CP1.stdf"), "D:\\1_STDF\\STDF_CACHE\\DEMO_CP1");
	std::cout << new_stdf->GetFinishT() << std::endl;
	delete new_stdf;
	new_stdf = nullptr;

	return 0;
}
