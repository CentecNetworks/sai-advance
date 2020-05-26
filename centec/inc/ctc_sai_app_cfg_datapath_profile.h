#ifndef __CTC_APP_CFG_DATAPATH_PROFILE__
#define __CTC_APP_CFG_DATAPATH_PROFILE__
#ifdef __cplusplus
extern "C" {
#endif

#include "sal.h"
#include "ctc_chip.h"


extern int32
ctc_app_get_datapath_profile(uint8* file_name, ctc_datapath_global_cfg_t* p_datapath_cfg);
#ifdef __cplusplus
}
#endif

#endif
