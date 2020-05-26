#ifndef __CTC_APP_CFG_PARSE__
#define __CTC_APP_CFG_PARSE__
#ifdef __cplusplus
extern "C" {
#endif

#include <sal_types.h>
#include <sal_file.h>

typedef struct ctc_app_parse_file_s
{
    sal_file_t p_file;
    void* mem_addr;
    int32 pos;
    int32 len;
}ctc_app_parse_file_t;


#define ctc_app_parse_file_init(p_ctc_parsr_file) \
{                                                 \
    (p_ctc_parsr_file)->p_file   = NULL;          \
    (p_ctc_parsr_file)->mem_addr = NULL;          \
    (p_ctc_parsr_file)->pos      = 0;             \
    (p_ctc_parsr_file)->len      = 0;             \
}

#define LETTER_NUMBER_MIX "lettermixnum"

int32
ctc_app_parse_open_file(const char* file_name, ctc_app_parse_file_t* p_file);

int32
ctc_app_parse_close_file(ctc_app_parse_file_t* p_file);

int32
ctc_app_parse_file(ctc_app_parse_file_t* p_file,
                      const char* field,
                      const char* field_sub,
                      void* value,
                      uint8 *p_entry_num);


#ifdef __cplusplus
}
#endif

#endif
