/**
 @file ctc_app_cfg.h

 @author  Copyright (C) 2011 Centec Networks Inc.  All rights reserved.

 @date 2010-7-5

 @version v2.0

  This file contains chip profile related data structure.
*/

#ifndef _CTC_APP_CFG_H
#define _CTC_APP_CFG_H
#ifdef __cplusplus
extern "C" {
#endif
#include "ctc_const.h"
#include "ctc_init.h"

extern int32
ctc_app_get_config(uint8 lchip, char* init_config, char* data_cfg, ctc_init_cfg_t * p_init_config);

#ifdef __cplusplus
}
#endif

#endif

