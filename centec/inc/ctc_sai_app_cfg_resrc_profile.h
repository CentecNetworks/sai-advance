#ifndef __CTC_APP_CFG_RESRC_PROFILE__
#define __CTC_APP_CFG_RESRC_PROFILE__
#ifdef __cplusplus
extern "C" {
#endif

#include "sal.h"
#include "ctc_qos.h"

int32
ctc_app_get_resrc_profile(const uint8* file_name,
                     ctc_qos_resrc_pool_cfg_t* profile_info);
#ifdef __cplusplus
}
#endif

#endif
