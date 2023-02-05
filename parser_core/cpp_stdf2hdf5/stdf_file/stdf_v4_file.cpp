#include "stdf_v4_file.h"
#include <string>

const char* REC_NAME[STDF_V4_RECORD_COUNT] =
{
	"FAR(File Attributes Record)",
	"ATR(Audit Trail Record)",
	"MIR(Master Information Record)",
	"MRR(Master Results Record)",
	"PCR(Part Count Record)",
	"HBR(Hardware Bin Record)",
	"SBR(Software Bin Record)",
	"PMR(Pin Map Record)",
	"PGR(Pin Group Record)",
	"PLR(Pin List Record)",
	"RDR(Retest Data Record)",
	"SDR(Site Description Record)",
	"WIR(Wafer Information Record)",
	"WRR(Wafer Results Record)",
	"WCR(Wafer Configuration Record)",
	"PIR(Part Information Record)",
	"PRR(Part Results Record)",
	"TSR(Test Synopsis Record)",
	"PTR(Parametric Test Record)",
	"MPR(Multiple-Result Parametric Record)",
	"FTR(Functional Test Record)",
	"BPS(Begin Program Section Record)",
	"EPS(End Program Section Record)",
	"GDR(Generic Data Record)",
	"DTR(Datalog Text Record)"
};

template<typename T>
bool is_infinite(const T& value)
{
	// Since we're a template, it's wise to use std::numeric_limits<T>
	//
	// Note: std::numeric_limits<T>::min() behaves like DBL_MIN, and is the smallest absolute value possible.
	//

	T max_value = std::numeric_limits<T>::max();
	T min_value = -max_value;

	return !(min_value <= value && value <= max_value);
}

template<typename T>
bool is_nan(const T& value)
{
	// True if NAN
	return value != value;
}

template<typename T>
bool is_valid(const T& value)
{
	// True if inf
	return !is_infinite(value) && !is_nan(value);
}


PartTestMethod::PartTestMethod()
{
	TEST_ID = U4(0);
	TEST_NUM = U4(0);
	PARM_FLG = B1("11000000");;
	OPT_FLAG = B1("11111110");;
	RES_SCAL = I1(0);
	LLM_SCAL = I1(0);
	HLM_SCAL = I1(0);
	LO_LIMIT = R4(0);
	HI_LIMIT = R4(0);
	LO_SPEC = R4(0);
	HI_SPEC = R4(0);
}


DataTableParametric::DataTableParametric()
{
	TEST_ID = U4(0);
	TEST_FLG = B1("00000000");
	RESULT = R4(0);
	LO_LIMIT = R4(0);
	HI_LIMIT = R4(0);
}


LiPTMD::LiPTMD()
{
	impl = new PartTestMethod();
#ifdef _DEBUG_API_H_
	if (impl == nullptr)
	{
		SHOW_MEMORY_ERROR();
		throw MEMORY_ALLOCATED_ERROR();
	}
#endif
}

LiPTMD::~LiPTMD()
{
	delete impl;
	impl = nullptr;
}

//PARM_FLG
void LiPTMD::param_scale_error(bool flag)
{
	impl->PARM_FLG[0] = flag;
}

void LiPTMD::param_drift_error(bool flag)
{
	impl->PARM_FLG[1] = flag;
}

void LiPTMD::param_oscillation(bool flag)
{
	impl->PARM_FLG[2] = flag;
}

void LiPTMD::result_higher_limit(bool flag)
{
	impl->PARM_FLG[3] = flag;
}

void LiPTMD::result_lower_limit(bool flag)
{
	impl->PARM_FLG[4] = flag;
}

void LiPTMD::passed_alternate_limit(bool flag)
{
	impl->PARM_FLG[5] = flag;
}

void LiPTMD::equal_lowlimit_pass(bool flag)
{
	impl->PARM_FLG[6] = flag;
}

void LiPTMD::equal_highlimit_pass(bool flag)
{
	impl->PARM_FLG[7] = flag;
}

//OPT_FLAG
void LiPTMD::set_result_exponent(signed char exponent)
{
	impl->RES_SCAL = exponent;
	impl->OPT_FLAG[0] = false;
}

void LiPTMD::set_low_limit(float limit)
{
	impl->LO_LIMIT = limit;
	impl->OPT_FLAG[6] = false;
	impl->OPT_FLAG[4] = false;
}

void LiPTMD::set_high_limit(float limit)
{
	impl->HI_LIMIT = limit;
	impl->OPT_FLAG[5] = false;
	impl->OPT_FLAG[7] = false;
}

void LiPTMD::result_exponent_invalid(bool flag)
{
	impl->OPT_FLAG[0] = flag;
}

void LiPTMD::no_low_spec(bool flag)
{
	impl->OPT_FLAG[2] = flag;
}

void LiPTMD::no_high_spec(bool flag)
{
	impl->OPT_FLAG[3] = flag;
}

void LiPTMD::low_limit_invalid(bool flag)
{
	impl->OPT_FLAG[4] = flag;
}

void LiPTMD::high_limit_invalid(bool flag)
{
	impl->OPT_FLAG[5] = flag;
}

void LiPTMD::no_low_limit(bool flag)
{
	impl->OPT_FLAG[6] = flag;
}

void LiPTMD::no_high_limit(bool flag)
{
	impl->OPT_FLAG[7] = flag;
}


LiDPT::LiDPT()
{
	impl = new DataTableParametric();
#ifdef _DEBUG_API_H_
	if (impl == nullptr)
	{
		SHOW_MEMORY_ERROR();
		throw MEMORY_ALLOCATED_ERROR();
	}
#endif
}

LiDPT::~LiDPT()
{
	delete impl;
	impl = nullptr;
}


// TEST_FLG
void LiDPT::alarm_detected(bool flag)
{
	impl->TEST_FLG[0] = flag;
}

void LiDPT::result_invalid(bool flag)
{
	impl->TEST_FLG[1] = flag;
}

void LiDPT::result_unreliable(bool flag)
{
	impl->TEST_FLG[2] = flag;
}

void LiDPT::timeout_occured(bool flag)
{
	impl->TEST_FLG[3] = flag;
}

void LiDPT::test_unexecuted(bool flag)
{
	impl->TEST_FLG[4] = flag;
}

void LiDPT::test_aborted(bool flag)
{
	impl->TEST_FLG[5] = flag;
}

void LiDPT::test_pfflag_invalid(bool flag)
{
	impl->TEST_FLG[6] = flag;
}

void LiDPT::test_failed(bool flag)
{
	impl->TEST_FLG[7] = flag;
}

void LiDPT::set_result(float value)
{
	impl->RESULT = value;
	// result is useful
	impl->TEST_FLG[0] = false;
	impl->TEST_FLG[1] = false;
	impl->TEST_FLG[2] = false;
	impl->TEST_FLG[3] = false;
	impl->TEST_FLG[4] = false;
	impl->TEST_FLG[5] = false;
}

//////////////////////////////////////////////////////////////////////////
static std::string to_string(STDF_TYPE type)
{
	switch (type)
	{
	case FAR_TYPE: return "\nFAR----File Attributes Record           ";  break;
	case ATR_TYPE: return "\nATR----Audit Trail Record               ";  break;
	case MIR_TYPE: return "\nMIR----Master Information Record        ";  break;
	case MRR_TYPE: return "\nMRR----Master Result Record             ";  break;
	case PCR_TYPE: return "\nPCR----Part Count Record                ";  break;
	case HBR_TYPE: return "\nHBR----Hardware Bin Record              ";  break;
	case SBR_TYPE: return "\nSBR----Software Bin Record              ";  break;
	case PMR_TYPE: return "\nPMR----Pin Map Record                   ";  break;
	case PGR_TYPE: return "\nPGR----Pin Group Record                 ";  break;
	case PLR_TYPE: return "\nPLR----Pin List Record                  ";  break;
	case RDR_TYPE: return "\nRDR----Reset Data Record                ";  break;
	case SDR_TYPE: return "\nSDR----Site Description Record          ";  break;
	case WIR_TYPE: return "\nWIR----Wafer Information Record         ";  break;
	case WRR_TYPE: return "\nWRR----Wafer Result Record              ";  break;
	case WCR_TYPE: return "\nWCR----Wafer Configuration Record       ";  break;
	case PIR_TYPE: return "\nPIR----Part Information Record          ";  break;
	case PRR_TYPE: return "\nPRR----Part Result Record               ";  break;
	case TSR_TYPE: return "\nTSR----Test Synopsis Record             ";  break;
	case PTR_TYPE: return "\nPTR----Parametric Test Record           ";  break;
	case MPR_TYPE: return "\nMPR----Multiple-Result Parametric Record";  break;
	case FTR_TYPE: return "\nFTR----Functional Test Record           ";  break;
	case BPS_TYPE: return "\nBPS----Begin Program Section Record     ";  break;
	case EPS_TYPE: return "\nEPS----End Program Section Record       ";  break;
	case GDR_TYPE: return "\nGDR----Generic Data Record              ";  break;
	case DTR_TYPE: return "\nDTR----Datalog Text Record              ";  break;
	default:   return "\nUNKONWN----Unkown Record Type"; break;
	}
}

STDF_FILE::STDF_FILE()
{
}

STDF_FILE::~STDF_FILE()
{
	for (unsigned int i = 0; i < Record_Vector.size(); i++)
	{
		if (Record_Vector[i] == nullptr)
		{
			continue;
		}
		delete Record_Vector[i];
		Record_Vector[i] = nullptr;
	}
	Record_Vector.clear();

	for (unsigned int i = 0; i < LiPTMD_Vector.size(); i++)
	{
		if (LiPTMD_Vector[i] == nullptr)
		{
			continue;
		}
		delete LiPTMD_Vector[i];
		LiPTMD_Vector[i] = nullptr;
	}
	LiPTMD_Vector.clear();

	for (unsigned int i = 0; i < LiDPT_Vector.size(); i++)
	{
		if (LiDPT_Vector[i] == nullptr)
		{
			continue;
		}
		delete LiDPT_Vector[i];
		LiDPT_Vector[i] = nullptr;
	}
	LiDPT_Vector.clear();
}


void STDF_FILE::data_write(std::ofstream& csv_dtp, std::ofstream& csv_ptmd, std::ofstream& csv_prr)
{
	for (std::vector<LiDPT*>::iterator it = LiDPT_Vector.begin(); it != LiDPT_Vector.end(); it++)
	{
		LiDPT* temp_dpt = *it;
		csv_dtp << temp_dpt->impl->PART_ID.c_str() << delimiter;
		csv_dtp << temp_dpt->impl->TEST_ID << delimiter;
		csv_dtp << temp_dpt->impl->RESULT << delimiter;
		csv_dtp << temp_dpt->impl->TEST_FLG.to_ulong() << delimiter;
		csv_dtp << temp_dpt->impl->PARM_FLG.to_ulong() << delimiter;
		csv_dtp << temp_dpt->impl->OPT_FLAG.to_ulong() << delimiter;
		csv_dtp << temp_dpt->impl->LO_LIMIT << delimiter;
		csv_dtp << temp_dpt->impl->HI_LIMIT << linefeed;
		delete temp_dpt; temp_dpt = nullptr;
	}
	LiDPT_Vector.clear();
	for (std::vector<LiPTMD*>::iterator it = LiPTMD_Vector.begin(); it != LiPTMD_Vector.end(); it++)
	{
		// 这个数据太难用hdf5写进去了, 就先用csv写进来后, 再用pandas读取后写到hdf5中
		LiPTMD* temp_ptmd = *it;
		csv_ptmd << temp_ptmd->impl->TEST_ID << delimiter;
		csv_ptmd << temp_ptmd->impl->DATAT_TYPE << delimiter;
		csv_ptmd << temp_ptmd->impl->TEST_NUM << delimiter;
		csv_ptmd << temp_ptmd->impl->TEST_TXT << delimiter;
		csv_ptmd << temp_ptmd->impl->PARM_FLG.to_ulong() << delimiter;
		csv_ptmd << temp_ptmd->impl->OPT_FLAG.to_ulong() << delimiter;
		// 在数据载入的时候提示是否需要做单位的格式转换
		csv_ptmd << (I4)temp_ptmd->impl->RES_SCAL << delimiter;
		csv_ptmd << (I4)temp_ptmd->impl->LLM_SCAL << delimiter;
		csv_ptmd << (I4)temp_ptmd->impl->HLM_SCAL << delimiter;
		csv_ptmd << temp_ptmd->impl->LO_LIMIT << delimiter;
		csv_ptmd << temp_ptmd->impl->HI_LIMIT << delimiter;
		csv_ptmd << temp_ptmd->impl->UNITS << delimiter;
		// 基本用不到的
		csv_ptmd << temp_ptmd->impl->C_RESFMT << delimiter;
		csv_ptmd << temp_ptmd->impl->C_LLMFMT << delimiter;
		csv_ptmd << temp_ptmd->impl->C_HLMFMT << delimiter;
		csv_ptmd << temp_ptmd->impl->LO_SPEC << delimiter;
		csv_ptmd << temp_ptmd->impl->HI_SPEC << linefeed;

		delete temp_ptmd; temp_ptmd = nullptr;
	}
	LiPTMD_Vector.clear();

	for (std::vector<StdfPRR*>::iterator it = StdfPRR_Vector.begin(); it != StdfPRR_Vector.end(); it++)
	{
		StdfPRR* temp_prr = *it;
		csv_prr << temp_prr->impl->PART_ID.c_str() << delimiter;
		csv_prr << temp_prr->impl->PART_TXT.c_str() << delimiter; // 后面用作类似teststand的的UUT NAME, 待都Ready后
		csv_prr << (U2)temp_prr->impl->HEAD_NUM << delimiter;
		csv_prr << (U2)temp_prr->impl->SITE_NUM << delimiter;
		csv_prr << temp_prr->impl->X_COORD << delimiter;
		csv_prr << temp_prr->impl->Y_COORD << delimiter;
		csv_prr << temp_prr->impl->HARD_BIN << delimiter;
		csv_prr << temp_prr->impl->SOFT_BIN << delimiter;
		csv_prr << temp_prr->impl->PART_FLG.to_ulong() << delimiter;
		csv_prr << temp_prr->impl->NUM_TEST << delimiter;
		csv_prr << (temp_prr->part_failed_flag() ? Fail : Pass) << delimiter;  // FAIL_FLAG
		csv_prr << temp_prr->impl->TEST_T << linefeed;
		delete temp_prr; temp_prr = nullptr;
	}
	StdfPRR_Vector.clear();
	
}


STDF_FILE_ERROR STDF_FILE::parser_to_hdf5(const wchar_t* filename)
{
	/*
		TODO:
			0. 依然使用安全一点的笨方法, 先扫描一部分数据, 数据安全放在第一位
			1. DIFF ONLY TEST_NO -> 有一种ATE为了省内存,只有第一次生成的数据是完整的,第二次生成的数据可能只有TEST_NO,也有可能有TEST_NO&TEST_TEXT
			2. 
	*/
	std::string temp = std::string(getenv("TEMP"));

	std::ofstream csv_prr(temp + "\\StdfTempPrr.csv", std::ios::binary);
	if (!csv_prr)
		return WRITE_ERROR;
	std::ofstream csv_dtp(temp + "\\StdfTempDtp.csv", std::ios::binary);
	if (!csv_dtp)
		return WRITE_ERROR;
	std::ofstream csv_ptmd(temp + "\\StdfTempPtmd.csv", std::ios::binary);
	if (!csv_ptmd)
		return WRITE_ERROR;

	// 按需要, 感觉只需要存一下BIN和NAME的关系就行了
	std::ofstream csv_bin(temp + "\\BinName.csv", std::ios::binary);
	if (!csv_bin)
		return WRITE_ERROR;

	std::ifstream in(filename, std::ios::in | std::ios::binary);
	if (!in)
		return READ_ERROR;

	StdfHeader header;
	STDF_TYPE type = header.read(in);
	if (type != FAR_TYPE)
		return FORMATE_ERROR;

	StdfFAR* far_record = new StdfFAR();
	far_record->parse(header);

	unsigned char cpu_type = far_record->get_cpu_type();
	if (cpu_type != 2)
		return STDF_CPU_TYPE_NOT_SUPPORT;

	unsigned char stdf_version = far_record->get_stdf_version();
	if (stdf_version != 4)
		return STDF_VERSION_NOT_SUPPORT;

	delete far_record;
	far_record = nullptr;

	// ============================================= 检测TEST_NO是否唯一
	/*
	TODO: test_no_only 来判断TESTNO的设置是不是唯一的
		  如果在一个周期内，有重复的TESTNO, 就设置为True
		  如果 test_no_only == true > 则使用TESTNO作为键
		  否则，使用 TESTNO:TESTTEXT作为键
		  如果有重复的TESTNO, 而测试机第二次测试的时候不写入TESTTEXT, 那就是SB测试机
	*/
	bool test_no_only = true;  // TEST_NO是唯一的
	bool have_pmr = false;
	int scan_test_no_only_time = 500;
	int scan_test_no_only_times = 0;
	std::map <std::string, int> test_no_map;
	bool is_new_record = true;
	while (!in.eof())
	{
		type = header.read(in);
		if (type == PTR_TYPE)
		{
			scan_test_no_only_times += 1;
			if (scan_test_no_only_times > scan_test_no_only_time) break;
			if (is_new_record)
			{
				test_no_map.erase(test_no_map.begin(), test_no_map.end());
				is_new_record = false;
			}
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			if (record->type() != PTR_TYPE) continue;
			StdfPTR* temp_ptr = static_cast<StdfPTR*>(record);
			int pir_vector_key = temp_ptr->get_head_number() * 1E6 + temp_ptr->get_site_number();
			std::string key = std::to_string(temp_ptr->get_test_number()) + ':' + std::to_string(pir_vector_key);
			if (test_no_map.count(key))
			{
				test_no_only = false;
			}
			else
			{
				test_no_map.insert(std::pair<std::string, int>(key, Pass));
			}

			delete temp_ptr;
			temp_ptr = nullptr;

			if (test_no_only == false) break;
		}
		if (type == PRR_TYPE) is_new_record = true;

	}
	in.close();
	std::cout << "TESTNO是唯一?:" << test_no_only << std::endl;

	/*
	 * 提早准备H5文件, PRR 50个TD转换OK后就写入 -> 避免写入次数太多了
	 * DTP文件最后导入
	 * PTMD每一个TD转换OK后写入
	 */
	// ===================================================== H5 Ready $ WAIT UPDATE


	// ===================================================== Read STDF
	StdfMRR* mrr_record = nullptr;

	std::map <std::string, int> TestKey_TestId;  // 用来区分不同的测试类型
	/*
	TestKey = str(TEST_NO) if test_no_only else str(TEST_NO) + str(TEST_TEXT)
	*/
	is_new_record = true;
	unsigned int part_id_int = 0;
	std::map <int, int> key_part_id; // 缓存单个TD中的每个Dut的PartId
	std::map <U2, Cn> pin_index_name;
	std::map <std::string, kxU2> only_key_pin_index; // 用于缓存MPR的pin_index

	// bin name 生成
	std::map <U2, bool> soft_bin_name;
	std::map <U2, bool> hard_bin_name;

	std::ifstream in2(filename, std::ios::in | std::ios::binary);
	while (!in2.eof())
	{
		type = header.read(in2);

		if (type == PMR_TYPE)
		{
			have_pmr = true;
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfPMR* temp_pmr = static_cast<StdfPMR*>(record);
			pin_index_name.insert(std::pair<U2, Cn>(temp_pmr->impl->PMR_INDX, temp_pmr->impl->CHAN_NAM));
			delete record; // 这个数据用不上, 早点删除
			record = nullptr;
			if (is_new_record) continue;
		}

		if (type == PIR_TYPE)
		{
			part_id_int++;
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			// if (record->type() != PIR_TYPE) continue;
			if (!is_new_record) key_part_id.erase(key_part_id.begin(), key_part_id.end());  // key_part_id 在每个TD处理完成后清空一下
			StdfPIR* temp_pir = static_cast<StdfPIR*>(record);
			int dut_key = temp_pir->get_head_number() << 8 | temp_pir->get_site_number();
			key_part_id.insert(std::pair<int, int>(dut_key, part_id_int));
			delete record; // 这个数据用不上, 早点删除
			record = nullptr;
			if (is_new_record) continue;
			// ======================================= H5数据写入 & 先用CSV来做测试
			data_write(csv_dtp, csv_ptmd, csv_prr);
			// ======================================= 
			
			is_new_record = true;
			continue;
		}
		if (type == MPR_TYPE)
		{
			/*
			* MPR也转为PTR类似的数据，这样解析起来比较简单和方便，也不那么绕
			*/
			is_new_record = false;
			if (!have_pmr) continue;
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfMPR* temp_mpr = static_cast<StdfMPR*>(record);
			int dut_key = temp_mpr->get_head_number() << 8 | temp_mpr->get_site_number();
			if (!key_part_id.count(dut_key))
			{
				delete record;
				record = nullptr;
				continue;
			}
			std::string only_key = test_no_only ? std::to_string(temp_mpr->get_test_number()) : std::to_string(temp_mpr->get_test_number()) + ":" + temp_mpr->get_test_text();
			unsigned int part_id = key_part_id.at(dut_key);
			// only_key + "@" + pin_name
			kxU2 pin_index_list;
			if (!only_key_pin_index.count(only_key))
			{
				only_key_pin_index.insert(std::pair<std::string, kxU2>(only_key, temp_mpr->impl->RTN_INDX));
				pin_index_list = temp_mpr->impl->RTN_INDX;
			}
			else
			{
				pin_index_list = only_key_pin_index.at(only_key);
			}
			int test_id;
			U2 pin_count = temp_mpr->get_pin_count();
			for (U2 i = 0; i < pin_count; i++)
			{
				// U2 pin_index = temp_mpr->get_pin_index(i);
				U2 pin_index = pin_index_list[i];
				Cn pin_name = pin_index_name.at(pin_index);
				only_key = only_key + "@" + pin_name.c_str();
				if (!TestKey_TestId.count(only_key))
				{
					test_id = TestKey_TestId.size();
					TestKey_TestId.insert(std::pair<std::string, int>(only_key, test_id));

					LiPTMD* temp_ptmd = new LiPTMD();
					temp_ptmd->impl->PARM_FLG = temp_mpr->impl->PARM_FLG;
					temp_ptmd->impl->OPT_FLAG = temp_mpr->impl->OPT_FLAG;
					temp_ptmd->impl->RES_SCAL = temp_mpr->impl->RES_SCAL;
					temp_ptmd->impl->LLM_SCAL = temp_mpr->impl->LLM_SCAL;
					temp_ptmd->impl->HLM_SCAL = temp_mpr->impl->HLM_SCAL;
					temp_ptmd->impl->LO_LIMIT = temp_mpr->impl->LO_LIMIT;
					temp_ptmd->impl->HI_LIMIT = temp_mpr->impl->HI_LIMIT;
					temp_ptmd->impl->UNITS = temp_mpr->impl->UNITS;
					temp_ptmd->impl->C_RESFMT = temp_mpr->impl->C_RESFMT;
					temp_ptmd->impl->C_LLMFMT = temp_mpr->impl->C_LLMFMT;
					temp_ptmd->impl->C_HLMFMT = temp_mpr->impl->C_HLMFMT;
					temp_ptmd->impl->LO_SPEC = temp_mpr->impl->LO_SPEC;
					temp_ptmd->impl->HI_SPEC = temp_mpr->impl->HI_SPEC;
					temp_ptmd->impl->DATAT_TYPE = "MPR";
					temp_ptmd->impl->TEST_ID = test_id;
					temp_ptmd->impl->TEST_NUM = temp_mpr->impl->TEST_NUM;
					temp_ptmd->impl->TEST_TXT = temp_mpr->impl->TEST_TXT + "@" + pin_name;

					LiPTMD_Vector.push_back(temp_ptmd);
				}
				else
				{
					test_id = TestKey_TestId.at(only_key);
				}
				LiDPT* temp_dtp = new LiDPT();
				temp_dtp->set_part_id(std::to_string(part_id).c_str());
				temp_dtp->impl->TEST_ID = test_id;
				temp_dtp->impl->TEST_FLG = temp_mpr->impl->TEST_FLG;
				temp_dtp->impl->PARM_FLG = temp_mpr->impl->PARM_FLG;
				temp_dtp->impl->OPT_FLAG = temp_mpr->impl->OPT_FLAG;
				temp_dtp->impl->RESULT = temp_mpr->get_return_result(i);
				temp_dtp->impl->LO_LIMIT = temp_mpr->impl->LO_LIMIT;
				temp_dtp->impl->HI_LIMIT = temp_mpr->impl->HI_LIMIT;
				LiDPT_Vector.push_back(temp_dtp);
			}
			delete record;
			record = nullptr;
			continue;
		}
		if (type == PTR_TYPE)
		{
			/*
			* 
			*/
			is_new_record = false;
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfPTR* temp_ptr = static_cast<StdfPTR*>(record);
			int dut_key = temp_ptr->get_head_number() << 8 | temp_ptr->get_site_number();
			if (!key_part_id.count(dut_key))
			{
				delete record;
				record = nullptr;
				continue;
			}
			std::string only_key = test_no_only? std::to_string(temp_ptr->get_test_number()): std::to_string(temp_ptr->get_test_number()) + ":" + temp_ptr->get_test_text();
			unsigned int part_id = key_part_id.at(dut_key);
			int test_id;
			if (!TestKey_TestId.count(only_key))
			{
				test_id = TestKey_TestId.size();
				TestKey_TestId.insert(std::pair<std::string, int>(only_key, test_id));
				LiPTMD* temp_ptmd = new LiPTMD();
				temp_ptmd->impl->PARM_FLG = temp_ptr->impl->PARM_FLG;
				temp_ptmd->impl->OPT_FLAG = temp_ptr->impl->OPT_FLAG;
				temp_ptmd->impl->RES_SCAL = temp_ptr->impl->RES_SCAL;
				temp_ptmd->impl->LLM_SCAL = temp_ptr->impl->LLM_SCAL;
				temp_ptmd->impl->HLM_SCAL = temp_ptr->impl->HLM_SCAL;
				temp_ptmd->impl->LO_LIMIT = temp_ptr->impl->LO_LIMIT;
				temp_ptmd->impl->HI_LIMIT = temp_ptr->impl->HI_LIMIT;
				temp_ptmd->impl->UNITS = temp_ptr->impl->UNITS;
				temp_ptmd->impl->C_LLMFMT = temp_ptr->impl->C_LLMFMT;
				temp_ptmd->impl->C_HLMFMT = temp_ptr->impl->C_HLMFMT;
				temp_ptmd->impl->LO_SPEC = temp_ptr->impl->LO_SPEC;
				temp_ptmd->impl->HI_SPEC = temp_ptr->impl->HI_SPEC;
				temp_ptmd->impl->DATAT_TYPE = "PTR";
				temp_ptmd->impl->TEST_ID = test_id;
				temp_ptmd->impl->TEST_NUM = temp_ptr->impl->TEST_NUM;
				temp_ptmd->impl->TEST_TXT = temp_ptr->impl->TEST_TXT;

				LiPTMD_Vector.push_back(temp_ptmd);
			}
			else
			{
				test_id = TestKey_TestId.at(only_key);
			}
			LiDPT* temp_dtp = new LiDPT();
			temp_dtp->set_part_id(std::to_string(part_id).c_str());
			temp_dtp->impl->TEST_ID = test_id;
			temp_dtp->impl->TEST_FLG = temp_ptr->impl->TEST_FLG;
			temp_dtp->impl->PARM_FLG = temp_ptr->impl->PARM_FLG;
			temp_dtp->impl->OPT_FLAG = temp_ptr->impl->OPT_FLAG;
			temp_dtp->impl->RESULT = temp_ptr->impl->RESULT;
			temp_dtp->impl->LO_LIMIT = temp_ptr->impl->LO_LIMIT;
			temp_dtp->impl->HI_LIMIT = temp_ptr->impl->HI_LIMIT;
			LiDPT_Vector.push_back(temp_dtp);

			delete record;
			record = nullptr;
			continue;
		}
		if (type == FTR_TYPE)
		{
			// @20200820填FTR的坑
			is_new_record = false;  // TODO: 注意, 这个是必要的
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			// if (record->type() != FTR_TYPE) continue;
			StdfFTR* temp_ftr = static_cast<StdfFTR*>(record);
			if (!temp_ftr->test_pfflag_invalid())
			{
				// 不需要的FTR数据
				delete record;
				record = nullptr;
				continue;
			}
			int dut_key = temp_ftr->get_head_number() << 8 | temp_ftr->get_site_number();
			if (!key_part_id.count(dut_key))
			{
				delete record;
				record = nullptr;
				continue;
			}
			std::string only_key = test_no_only ? std::to_string(temp_ftr->get_test_number()) : std::to_string(temp_ftr->get_test_number()) + ":" + temp_ftr->get_test_text();
			unsigned int part_id = key_part_id.at(dut_key);
			int test_id;
			if (!TestKey_TestId.count(only_key))
			{
				test_id = TestKey_TestId.size();
				TestKey_TestId.insert(std::pair<std::string, int>(only_key, test_id));
				LiPTMD* temp_ptmd = new LiPTMD();
				temp_ptmd->impl->OPT_FLAG[1] = 1;
				temp_ptmd->set_high_limit(1.1);
				temp_ptmd->set_low_limit(0.1);
				temp_ptmd->equal_highlimit_pass(true);
				temp_ptmd->equal_lowlimit_pass(false);
				temp_ptmd->set_result_exponent(0);
				temp_ptmd->impl->UNITS = "PAT";
				temp_ptmd->impl->DATAT_TYPE = "FTR";
				temp_ptmd->impl->TEST_ID = test_id;
				temp_ptmd->impl->TEST_NUM = temp_ftr->impl->TEST_NUM;
				temp_ptmd->impl->TEST_TXT = temp_ftr->impl->TEST_TXT;

				LiPTMD_Vector.push_back(temp_ptmd);
			}
			else
			{
				test_id = TestKey_TestId.at(only_key);
			}
			LiDPT* temp_dtp = new LiDPT();
			temp_dtp->set_part_id(std::to_string(part_id).c_str());
			temp_dtp->impl->TEST_ID = test_id;
			if (temp_ftr->test_failed())
			{
				temp_dtp->set_result(Fail);
				temp_dtp->test_failed(true);
			}
			else
			{
				temp_dtp->set_result(Pass);
				temp_dtp->test_failed(false);
			}
			LiDPT_Vector.push_back(temp_dtp);

			delete record;
			record = nullptr;
			continue;
		}
		if (type == PRR_TYPE)
		{
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfPRR* temp_prr = static_cast<StdfPRR*>(record);
			int dut_key = temp_prr->get_head_number() << 8 | temp_prr->get_site_number();
			if (!key_part_id.count(dut_key))
			{
				delete record;
				record = nullptr;
				continue;
			}
			unsigned int part_id = key_part_id.at(dut_key);
			temp_prr->set_part_id(std::to_string(part_id).c_str());
			StdfPRR_Vector.push_back(temp_prr);
			continue;
		}
		if (type == HBR_TYPE)
		{
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfHBR* temp_hbr = static_cast<StdfHBR*>(record);
			// StdfHBR_Vector.push_back(temp_hbr);
			if (!hard_bin_name.count(temp_hbr->impl->HBIN_NUM))
			{
				csv_bin << "HBR" << delimiter;
				csv_bin << temp_hbr->impl->HBIN_NUM << delimiter;
				csv_bin << temp_hbr->get_hardbin_indication() << delimiter;
				csv_bin << temp_hbr->get_hardbin_name() << linefeed;
				hard_bin_name.insert(std::pair<U2, bool>(temp_hbr->impl->HBIN_NUM, true));
			}
			delete record;
			record = nullptr;
			continue;
		}
		if (type == SBR_TYPE)
		{
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			StdfSBR* temp_sbr = static_cast<StdfSBR*>(record);
			// StdfSBR_Vector.push_back(temp_sbr);
			if (!soft_bin_name.count(temp_sbr->impl->SBIN_NUM))
			{
				csv_bin << "SBR" << delimiter;
				csv_bin << temp_sbr->impl->SBIN_NUM << delimiter;
				csv_bin << temp_sbr->get_softbin_indication() << delimiter;
				csv_bin << temp_sbr->get_softbin_name() << linefeed;
				soft_bin_name.insert(std::pair<U2, bool>(temp_sbr->impl->SBIN_NUM, true));
			}
			delete record;
			record = nullptr;
			continue;
		}
		if (type == MRR_TYPE)
		{
			/* 退出解析 */
			StdfRecord* record = header.create_record(type);
			record->parse(header);
			mrr_record = static_cast<StdfMRR*>(record);
			break;
		}
		if (type == PCR_TYPE)
		{
			// 不需要, 用pandas
			continue;
		}
		if (type == TSR_TYPE)
		{
			// 需要否, 感觉不需要, 自己算
			continue;
		}
	}
	in2.close();

	// ===================================== 处理未写入到H5的数据
	data_write(csv_dtp, csv_ptmd, csv_prr);
	csv_dtp.close(); csv_ptmd.close(); csv_prr.close();
	// ===================================== 处理可以在最后写入的数据
	if (mrr_record == nullptr)
	{
		FINISH_T = 0;
	}
	else
	{
		FINISH_T = mrr_record->impl->FINISH_T;
		delete mrr_record;
		mrr_record = nullptr;
	}

	//for (std::vector<StdfSBR*>::iterator it = StdfSBR_Vector.begin(); it != StdfSBR_Vector.end(); it++)
	//{
	//	StdfSBR* temp_sbr = *it;
	//	csv_bin << "SBR" << delimiter;
	//	csv_bin << temp_sbr->get_softbin_number() << delimiter;
	//	csv_bin << temp_sbr->get_softbin_count() << delimiter;
	//	csv_bin << temp_sbr->get_softbin_indication() << delimiter;
	//	csv_bin << temp_sbr->get_softbin_name() << linefeed;
	//}
	//for (std::vector<StdfHBR*>::iterator it = StdfHBR_Vector.begin(); it != StdfHBR_Vector.end(); it++)
	//{
	//	StdfHBR* temp_sbr = *it;
	//	csv_bin << "HBR" << delimiter;
	//	csv_bin << temp_sbr->get_head_number() << delimiter;
	//	csv_bin << temp_sbr->get_site_number() << delimiter;
	//	csv_bin << temp_sbr->get_hardbin_number() << delimiter;
	//	csv_bin << temp_sbr->get_hardbin_count() << delimiter;
	//	csv_bin << temp_sbr->get_hardbin_indication() << delimiter;
	//	csv_bin << temp_sbr->get_hardbin_name() << linefeed;
	//}
	return STDF_OPERATE_OK;
}

STDF_FILE_ERROR STDF_FILE::read(const char* filename)
{
	std::ifstream in(filename, std::ios::in | std::ios::binary);
	if (!in) return READ_ERROR;

	StdfHeader header;
	STDF_TYPE type = header.read(in);
	if (type != FAR_TYPE) return FORMATE_ERROR;

	StdfFAR* far_record = new StdfFAR();
	far_record->parse(header);

	unsigned char cpu_type = far_record->get_cpu_type();
	if (cpu_type != 2) return STDF_CPU_TYPE_NOT_SUPPORT;

	unsigned char stdf_version = far_record->get_stdf_version();
	if (stdf_version != 4) return STDF_VERSION_NOT_SUPPORT;

	Record_Vector.push_back(far_record);
	append_record_by_type(far_record);

	while (!in.eof())
	{
		type = header.read(in);
		StdfRecord* record = header.create_record(type);
		if (record)
		{
			record->parse(header);
			Record_Vector.push_back(record);
			append_record_by_type(record);
		}
		if (type == MRR_TYPE) break;
	}
	in.close();
	return STDF_OPERATE_OK;
}

STDF_FILE_ERROR STDF_FILE::write(const char* filename)
{
	std::ofstream out(filename, std::ios::out);
	if (!out) return WRITE_ERROR;

	for (unsigned int i = 0; i < Record_Vector.size(); i++)
	{
		StdfRecord* record = Record_Vector[i];
		out << to_string(record->type()) << "\n";
		//record->print(out);
		out << (*record);
	}
	out.close();
	return STDF_OPERATE_OK;
}

STDF_FILE_ERROR STDF_FILE::save(const char* filename)
{
	std::ofstream out(filename, std::ios::binary);
	if (!out) return WRITE_ERROR;

	StdfHeader header;
	for (unsigned int i = 0; i < Record_Vector.size(); i++)
	{
		if (i == 1)
		{
			StdfATR* atr = new StdfATR();
			atr->set_command_line("Save As By STDF Reader");
			atr->set_modify_time(time(NULL));
			atr->unparse(header);
			header.write(out);
		}
		StdfRecord* record = Record_Vector[i];
		record->unparse(header);
		header.write(out);
	}
	out.close();
	return STDF_OPERATE_OK;
}


STDF_FILE_ERROR STDF_FILE::write(const char* filename, STDF_TYPE type)
{
	std::ofstream out(filename, std::ios::out);
	if (!out) return WRITE_ERROR;

	unsigned int count = get_count(type);
	for (unsigned int i = 0; i < count; i++)
	{
		StdfRecord* record = get_record(type, i);
		if (record)
		{
			out << to_string(type) << "\n";
			out << (*record);
		}
	}
	return STDF_OPERATE_OK;
}

const char* STDF_FILE::get_name(STDF_TYPE type)
{
	if (type >= STDF_V4_RECORD_COUNT) return nullptr;
	else return REC_NAME[type];
}

unsigned int STDF_FILE::get_count(STDF_TYPE type)
{
	unsigned int count = 0;
	switch (type)
	{
	case FAR_TYPE: count = StdfFAR_Vector.size(); break;
	case ATR_TYPE: count = StdfATR_Vector.size(); break;
	case MIR_TYPE: count = StdfMIR_Vector.size(); break;
	case MRR_TYPE: count = StdfMRR_Vector.size(); break;
	case PCR_TYPE: count = StdfPCR_Vector.size(); break;
	case HBR_TYPE: count = StdfHBR_Vector.size(); break;
	case SBR_TYPE: count = StdfSBR_Vector.size(); break;
	case PMR_TYPE: count = StdfPMR_Vector.size(); break;
	case PGR_TYPE: count = StdfPGR_Vector.size(); break;
	case PLR_TYPE: count = StdfPLR_Vector.size(); break;
	case RDR_TYPE: count = StdfRDR_Vector.size(); break;
	case SDR_TYPE: count = StdfSDR_Vector.size(); break;
	case WIR_TYPE: count = StdfWIR_Vector.size(); break;
	case WRR_TYPE: count = StdfWRR_Vector.size(); break;
	case WCR_TYPE: count = StdfWCR_Vector.size(); break;
	case PIR_TYPE: count = StdfPIR_Vector.size(); break;
	case PRR_TYPE: count = StdfPRR_Vector.size(); break;
	case TSR_TYPE: count = StdfTSR_Vector.size(); break;
	case PTR_TYPE: count = StdfPTR_Vector.size(); break;
	case MPR_TYPE: count = StdfMPR_Vector.size(); break;
	case FTR_TYPE: count = StdfFTR_Vector.size(); break;
	case BPS_TYPE: count = StdfBPS_Vector.size(); break;
	case EPS_TYPE: count = StdfEPS_Vector.size(); break;
	case GDR_TYPE: count = StdfGDR_Vector.size(); break;
	case DTR_TYPE: count = StdfDTR_Vector.size(); break;
	default: count = 0; break;
	}
	return count;
}

unsigned int STDF_FILE::get_total_count()
{
	return Record_Vector.size();
}

StdfRecord* STDF_FILE::get_record(unsigned int index)
{
	StdfRecord* record = nullptr;
	if (index < Record_Vector.size()) record = Record_Vector[index];
	return record;
}

StdfRecord* STDF_FILE::get_record(STDF_TYPE type, unsigned int index)
{
	StdfRecord* record = nullptr;
	switch (type)
	{
	case FAR_TYPE: if (index < StdfFAR_Vector.size()) record = StdfFAR_Vector[index]; break;
	case ATR_TYPE: if (index < StdfATR_Vector.size()) record = StdfATR_Vector[index]; break;
	case MIR_TYPE: if (index < StdfMIR_Vector.size()) record = StdfMIR_Vector[index]; break;
	case MRR_TYPE: if (index < StdfMRR_Vector.size()) record = StdfMRR_Vector[index]; break;
	case PCR_TYPE: if (index < StdfPCR_Vector.size()) record = StdfPCR_Vector[index]; break;
	case HBR_TYPE: if (index < StdfHBR_Vector.size()) record = StdfHBR_Vector[index]; break;
	case SBR_TYPE: if (index < StdfSBR_Vector.size()) record = StdfSBR_Vector[index]; break;
	case PMR_TYPE: if (index < StdfPMR_Vector.size()) record = StdfPMR_Vector[index]; break;
	case PGR_TYPE: if (index < StdfPGR_Vector.size()) record = StdfPGR_Vector[index]; break;
	case PLR_TYPE: if (index < StdfPLR_Vector.size()) record = StdfPLR_Vector[index]; break;
	case RDR_TYPE: if (index < StdfRDR_Vector.size()) record = StdfRDR_Vector[index]; break;
	case SDR_TYPE: if (index < StdfSDR_Vector.size()) record = StdfSDR_Vector[index]; break;
	case WIR_TYPE: if (index < StdfWIR_Vector.size()) record = StdfWIR_Vector[index]; break;
	case WRR_TYPE: if (index < StdfWRR_Vector.size()) record = StdfWRR_Vector[index]; break;
	case WCR_TYPE: if (index < StdfWCR_Vector.size()) record = StdfWCR_Vector[index]; break;
	case PIR_TYPE: if (index < StdfPIR_Vector.size()) record = StdfPIR_Vector[index]; break;
	case PRR_TYPE: if (index < StdfPRR_Vector.size()) record = StdfPRR_Vector[index]; break;
	case TSR_TYPE: if (index < StdfTSR_Vector.size()) record = StdfTSR_Vector[index]; break;
	case PTR_TYPE: if (index < StdfPTR_Vector.size()) record = StdfPTR_Vector[index]; break;
	case MPR_TYPE: if (index < StdfMPR_Vector.size()) record = StdfMPR_Vector[index]; break;
	case FTR_TYPE: if (index < StdfFTR_Vector.size()) record = StdfFTR_Vector[index]; break;
	case BPS_TYPE: if (index < StdfBPS_Vector.size()) record = StdfBPS_Vector[index]; break;
	case EPS_TYPE: if (index < StdfEPS_Vector.size()) record = StdfEPS_Vector[index]; break;
	case GDR_TYPE: if (index < StdfGDR_Vector.size()) record = StdfGDR_Vector[index]; break;
	case DTR_TYPE: if (index < StdfDTR_Vector.size()) record = StdfDTR_Vector[index]; break;
	default: record = nullptr; break;
	}
	return record;
}

void STDF_FILE::append_record_by_type(StdfRecord* record)
{
	STDF_TYPE type = record->type();
	switch (type)
	{
	case FAR_TYPE: StdfFAR_Vector.push_back(static_cast<StdfFAR*>(record)); break;
	case ATR_TYPE: StdfATR_Vector.push_back(static_cast<StdfATR*>(record)); break;
	case MIR_TYPE: StdfMIR_Vector.push_back(static_cast<StdfMIR*>(record)); break;
	case MRR_TYPE: StdfMRR_Vector.push_back(static_cast<StdfMRR*>(record)); break;
	case PCR_TYPE: StdfPCR_Vector.push_back(static_cast<StdfPCR*>(record)); break;
	case HBR_TYPE: StdfHBR_Vector.push_back(static_cast<StdfHBR*>(record)); break;
	case SBR_TYPE: StdfSBR_Vector.push_back(static_cast<StdfSBR*>(record)); break;
	case PMR_TYPE: StdfPMR_Vector.push_back(static_cast<StdfPMR*>(record)); break;
	case PGR_TYPE: StdfPGR_Vector.push_back(static_cast<StdfPGR*>(record)); break;
	case PLR_TYPE: StdfPLR_Vector.push_back(static_cast<StdfPLR*>(record)); break;
	case RDR_TYPE: StdfRDR_Vector.push_back(static_cast<StdfRDR*>(record)); break;
	case SDR_TYPE: StdfSDR_Vector.push_back(static_cast<StdfSDR*>(record)); break;
	case WIR_TYPE: StdfWIR_Vector.push_back(static_cast<StdfWIR*>(record)); break;
	case WRR_TYPE: StdfWRR_Vector.push_back(static_cast<StdfWRR*>(record)); break;
	case WCR_TYPE: StdfWCR_Vector.push_back(static_cast<StdfWCR*>(record)); break;
	case PIR_TYPE: StdfPIR_Vector.push_back(static_cast<StdfPIR*>(record)); break;
	case PRR_TYPE: StdfPRR_Vector.push_back(static_cast<StdfPRR*>(record)); break;
	case TSR_TYPE: StdfTSR_Vector.push_back(static_cast<StdfTSR*>(record)); break;
	case PTR_TYPE: StdfPTR_Vector.push_back(static_cast<StdfPTR*>(record)); break;
	case MPR_TYPE: StdfMPR_Vector.push_back(static_cast<StdfMPR*>(record)); break;
	case FTR_TYPE: StdfFTR_Vector.push_back(static_cast<StdfFTR*>(record)); break;
	case BPS_TYPE: StdfBPS_Vector.push_back(static_cast<StdfBPS*>(record)); break;
	case EPS_TYPE: StdfEPS_Vector.push_back(static_cast<StdfEPS*>(record)); break;
	case GDR_TYPE: StdfGDR_Vector.push_back(static_cast<StdfGDR*>(record)); break;
	case DTR_TYPE: StdfDTR_Vector.push_back(static_cast<StdfDTR*>(record)); break;
	default: break;
	}
}

