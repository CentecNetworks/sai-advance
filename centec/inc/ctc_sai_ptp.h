
/**
 @file ctc_sai_ptp.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-06-21

 @version v2.0

\p
 This module defines SAI Ptp.
\b
\p
 The PTP Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\e  |  create_ptp_domain;                                       |    CTC7132，CTC8180     |
\e  |  remove_ptp_domain;                                       |    CTC7132，CTC8180     |
\e  |  set_ptp_domain_attribute;                                |    CTC7132，CTC8180     |
\e  |  get_ptp_domain_attribute;                                |    CTC7132，CTC8180     |
\b
\p
 The PTP Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\e  |  SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE                |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE                          |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_OFFSET                 |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE                 |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE                      |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE                        |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND                 |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS                  |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY                |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP                        |    CTC7132，CTC8180     |
\e  |  SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP                   |    CTC7132，CTC8180     |
\b
*/

#ifndef _CTC_SAI_PTP_H
#define _CTC_SAI_PTP_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

typedef struct ctc_sai_ptp_db_s
{
    sai_ptp_enable_based_type_t enable_type;    
    sai_ptp_device_type_t device_type;
    bool is_drift_offset;
    bool is_time_offset; 
    sai_timeoffset_t drift_offset;
    sai_timeoffset_t time_offset;
    sai_ptp_tod_interface_format_type_t tod_format;
    bool tod_enable;
    sai_ptp_tod_intf_mode_t tod_mode;
    int8 leap_second;
    uint8 pps_status;
    uint8 pps_accuracy;
        
} ctc_sai_ptp_db_t;

extern sai_status_t
ctc_sai_ptp_api_init();

extern sai_status_t
ctc_sai_ptp_db_init(uint8 lchip);

extern void
ctc_sai_ptp_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_PTP_H*/