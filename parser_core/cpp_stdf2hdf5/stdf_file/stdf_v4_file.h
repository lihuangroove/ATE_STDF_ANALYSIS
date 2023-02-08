/*************************************************************************
 * For testing stdf files.
*************************************************************************/
#ifndef _STDF_V4_AUX_FILE_H_
#define _STDF_V4_AUX_FILE_H_

#include "../stdf_api/stdf_v4_api.h"
#include "../stdf_api/stdf_v4_internal.h"
#include <vector>
#include <sstream>
#include <map>
#include <string.h>
#include <math.h>
#include <float.h>

#define STDF_V4_RECORD_COUNT 25

#define OP_ERROR 0x00

enum STDF_FILE_ERROR : int
{
    STDF_OPERATE_OK = OP_ERROR | 0,
	READ_ERROR = OP_ERROR | -1,
	FORMATE_ERROR = OP_ERROR | -2,
    STDF_CPU_TYPE_NOT_SUPPORT = OP_ERROR | -3,
	STDF_VERSION_NOT_SUPPORT = OP_ERROR | -4,
	WRITE_ERROR = OP_ERROR | -5,
	STDF_OPERATE_OK_PAT = OP_ERROR | 0x10, // PAT数据
};


/*
 * 定义用于数据链接的结构体
 */

class PartTestMethod //: PTMD
{
public:
	U4 TEST_ID; // use to connect PTMD And DTP
	Cn DATAT_TYPE; // [PTR, FTR, MPR[->PTR]] 考虑将MPR的数据转为PTR

	U4 TEST_NUM;
	Cn TEST_TXT;

	// 沿用类似PTR的FLG, 找到用的上的
	B1 PARM_FLG; // need
	B1 OPT_FLAG; // need

	I1 RES_SCAL;
	I1 LLM_SCAL;
	I1 HLM_SCAL;
	R4 LO_LIMIT;
	R4 HI_LIMIT;
	Cn UNITS;

	// 基本用不到的
	Cn C_RESFMT;
	Cn C_LLMFMT;
	Cn C_HLMFMT;
	R4 LO_SPEC;
	R4 HI_SPEC;
public:
	PartTestMethod();
	~PartTestMethod() {};

private:
	PartTestMethod(const PartTestMethod&);
	PartTestMethod& operator=(const PartTestMethod&);
};

class DataTableParametric //: DTP
{
public:
	U4 TEST_ID; // use to connect PTMD And DTP
	Cn PART_ID; // connect PRR
	B1 TEST_FLG; // need
	B1 PARM_FLG;  // keep
	R4 RESULT;
	// Cn ALARM_ID;  // not need
	B1 OPT_FLAG;  // USE TO Pat

	// PAT
	R4 LO_LIMIT;
	R4 HI_LIMIT;

	// PAT?
	// R4 LO_SPEC;
	// R4 HI_SPEC;
public:
	DataTableParametric();
	~DataTableParametric() {};

private:
	DataTableParametric(const DataTableParametric&);
	DataTableParametric& operator=(const DataTableParametric&);
};

class LiPTMD
{
public:
	LiPTMD();
	~LiPTMD();

	//PARM_FLG
	void param_scale_error(bool flag);
	void param_drift_error(bool flag);
	void param_oscillation(bool flag);
	void result_higher_limit(bool flag);
	void result_lower_limit(bool flag);
	void passed_alternate_limit(bool flag);
	void equal_lowlimit_pass(bool flag);
	void equal_highlimit_pass(bool flag);
	//OPT_FLAG
	void set_result_exponent(signed char exponent);
	void set_low_limit(float limit);
	void set_high_limit(float limit);
	void result_exponent_invalid(bool flag);
	void no_low_spec(bool flag);
	void no_high_spec(bool flag);
	void low_limit_invalid(bool flag);
	void high_limit_invalid(bool flag);
	void no_low_limit(bool flag);
	void no_high_limit(bool flag);

// private:
	typedef class PartTestMethod Impl;
	Impl* impl;

};


class LiDPT
{
public:
	LiDPT();
	~LiDPT();

	void set_part_id(const char* id)
	{
		if (id) impl->PART_ID.assign(id);
	}
	void set_result(float value);

	// TEST_FLG
	void alarm_detected(bool flag);
	void result_invalid(bool flag);
	void result_unreliable(bool flag);
	void timeout_occured(bool flag);
	void test_unexecuted(bool flag);
	void test_aborted(bool flag);
	void test_pfflag_invalid(bool flag);
	void test_failed(bool flag);
// private:
	typedef class DataTableParametric Impl;
	Impl* impl;

};

class STDF_FILE
{
public:
	STDF_FILE();
	~STDF_FILE();

	STDF_FILE_ERROR read(const char* filename);
	STDF_FILE_ERROR parser_to_hdf5(const wchar_t* filename, const char* file_path);  // chinese path
	STDF_FILE_ERROR write(const char* filename, STDF_TYPE type);
	STDF_FILE_ERROR write(const char* filename);
	STDF_FILE_ERROR save(const char* filename);
	const char* get_name(STDF_TYPE type);
	unsigned int get_count(STDF_TYPE type);
	StdfRecord* get_record(STDF_TYPE type, unsigned int index);
	unsigned int get_total_count();
	StdfRecord* get_record(unsigned int index);
	int get_mrr_finish(void) { return FINISH_T; };

private:
	void append_record_by_type(StdfRecord* record);
	void data_write(std::ofstream& csv_dtp, std::ofstream& csv_ptmd, std::ofstream& csv_prr);
	STDF_FILE(const STDF_FILE& src);
	STDF_FILE& operator=(const STDF_FILE& src);

	int Pass = 1;
	int Fail = 0;
	const char delimiter = ',';
	const char linefeed = '\n';
	const char none_char = '\0';
	const char quatotion = '\"';
	U4 FINISH_T = U4(0);

private:
	std::vector<StdfRecord*> Record_Vector;
	std::vector<StdfFAR*> StdfFAR_Vector;
	std::vector<StdfATR*> StdfATR_Vector;
	std::vector<StdfMIR*> StdfMIR_Vector;
	std::vector<StdfMRR*> StdfMRR_Vector;
	std::vector<StdfPCR*> StdfPCR_Vector;
	std::vector<StdfHBR*> StdfHBR_Vector;
	std::vector<StdfSBR*> StdfSBR_Vector;
	std::vector<StdfPMR*> StdfPMR_Vector;
	std::vector<StdfPGR*> StdfPGR_Vector;
	std::vector<StdfPLR*> StdfPLR_Vector;
	std::vector<StdfRDR*> StdfRDR_Vector;
	std::vector<StdfSDR*> StdfSDR_Vector;
	std::vector<StdfWIR*> StdfWIR_Vector;
	std::vector<StdfWRR*> StdfWRR_Vector;
	std::vector<StdfWCR*> StdfWCR_Vector;
	std::vector<StdfPIR*> StdfPIR_Vector;
	std::vector<StdfPRR*> StdfPRR_Vector;
	std::vector<StdfTSR*> StdfTSR_Vector;
	std::vector<StdfPTR*> StdfPTR_Vector;
	std::vector<StdfMPR*> StdfMPR_Vector;
	std::vector<StdfFTR*> StdfFTR_Vector;
	std::vector<StdfBPS*> StdfBPS_Vector;
	std::vector<StdfEPS*> StdfEPS_Vector;
	std::vector<StdfGDR*> StdfGDR_Vector;
	std::vector<StdfDTR*> StdfDTR_Vector;

	std::vector<LiPTMD*> LiPTMD_Vector;
	std::vector<LiDPT*> LiDPT_Vector;
};

#endif//_STDF_V4_AUX_FILE_H_
