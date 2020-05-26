#ifndef __CTC_APP_CFG_FTM_PROFILE__
#define __CTC_APP_CFG_FTM_PROFILE__
#ifdef __cplusplus
extern "C" {
#endif

#include "sal.h"
#include "ctc_ftm.h"

#define PROFILE_PATH_MAX    256

#define UNIT 256
#define IBM_TCAM 0
#define NETLOGIC_9K_TCAM    1
#define MAX_PKT_FILE_NAME_SIZE 256
#define LINE_LEN_MAX   128
#define KEY_LEN_MAX    20
#define MAX_INFO_SIZE  128

#define EMPTY_LINE(C)     ((C) == '\0' || (C) == '\r' || (C) == '\n')
#define WHITE_SPACE(C)    ((C) == '\t' || (C) == ' ')



typedef struct ctc_key_name_value_pair_s
{
    const char* key_name;
    uint32      key_value;

} ctc_key_name_value_pair_t;

typedef struct ctc_key_name_size_pair_s
{
    const char* key_name;
    uint32      key_value;
    uint32      key_size;

} ctc_key_name_size_pair_t;

typedef struct ctc_para_pair_s
{
    const char* para_name;                     /* the parameter name */
    int32 (* fun_ptr)(const int8* line, void* argus); /* get the value from line */
    void* argus;                               /* parameter for fun_ptr */
} ctc_para_pair_t;

int32
ctc_app_read_ftm_profile(const int8* file_name,
                     ctc_ftm_profile_info_t* profile_info);
#ifdef __cplusplus
}
#endif

#endif
