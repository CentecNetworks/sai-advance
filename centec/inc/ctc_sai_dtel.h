/**
 @file ctc_sai_dtel.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-06-21

 @version v2.0

\p
 This module defines SAI Dtel.
\b
\p
 The DTEL Module APIs supported by centec devices:
\p
\b
\t  |   API                                             |   SUPPORT CHIPS LIST   |
\t  |  create_dtel                                      |           -            |
\t  |  remove_dtel                                      |           -            |
\t  |  set_dtel_attribute                               |           -            |
\t  |  get_dtel_attribute                               |           -            |
\t  |  create_dtel_queue_report                         |           -            |
\t  |  remove_dtel_queue_report                         |           -            |
\t  |  set_dtel_queue_report_attribute                  |           -            |
\t  |  get_dtel_queue_report_attribute                  |           -            |
\t  |  create_dtel_int_session                          |           -            |
\t  |  remove_dtel_int_session                          |           -            |
\t  |  set_dtel_int_session_attribute                   |           -            |
\t  |  get_dtel_int_session_attribute                   |           -            |
\t  |  create_dtel_report_session                       |           -            |
\t  |  remove_dtel_report_session                       |           -            |
\t  |  set_dtel_report_session_attribute                |           -            |
\t  |  get_dtel_report_session_attribute                |           -            |
\t  |  create_dtel_event                                |           -            |
\t  |  remove_dtel_event                                |           -            |
\t  |  set_dtel_event_attribute                         |           -            |
\t  |  get_dtel_event_attribute                         |           -            |
\b
\p
 The DTEL attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                       |   SUPPORT CHIPS LIST   |
\t  |  SAI_DTEL_ATTR_INT_ENDPOINT_ENABLE                |           -            |
\t  |  SAI_DTEL_ATTR_INT_TRANSIT_ENABLE                 |           -            |
\t  |  SAI_DTEL_ATTR_POSTCARD_ENABLE                    |           -            |
\t  |  SAI_DTEL_ATTR_DROP_REPORT_ENABLE                 |           -            |
\t  |  SAI_DTEL_ATTR_QUEUE_REPORT_ENABLE                |           -            |
\t  |  SAI_DTEL_ATTR_SWITCH_ID                          |           -            |
\t  |  SAI_DTEL_ATTR_FLOW_STATE_CLEAR_CYCLE             |           -            |
\t  |  SAI_DTEL_ATTR_LATENCY_SENSITIVITY                |           -            |
\t  |  SAI_DTEL_ATTR_SINK_PORT_LIST                     |           -            |
\t  |  SAI_DTEL_ATTR_INT_L4_DSCP                        |           -            |
\b
\p
 The DTEL Queue Report attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                       |   SUPPORT CHIPS LIST   |
\t  |  SAI_DTEL_QUEUE_REPORT_ATTR_QUEUE_ID              |           -            |
\t  |  SAI_DTEL_QUEUE_REPORT_ATTR_DEPTH_THRESHOLD       |           -            |
\t  |  SAI_DTEL_QUEUE_REPORT_ATTR_LATENCY_THRESHOLD     |           -            |
\t  |  SAI_DTEL_QUEUE_REPORT_ATTR_BREACH_QUOTA          |           -            |
\t  |  SAI_DTEL_QUEUE_REPORT_ATTR_TAIL_DROP             |           -            |
\b
\p
 The DTEL Int Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_DTEL_INT_SESSION_ATTR_MAX_HOP_COUNT              |           -            |
\t  |  SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_ID          |           -            |
\t  |  SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_PORTS       |           -            |
\t  |  SAI_DTEL_INT_SESSION_ATTR_COLLECT_INGRESS_TIMESTAMP  |           -            |
\t  |  SAI_DTEL_INT_SESSION_ATTR_COLLECT_EGRESS_TIMESTAMP   |           -            |
\t  |  SAI_DTEL_INT_SESSION_ATTR_COLLECT_QUEUE_INFO         |           -            |
\b
\p
 The DTEL Report Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_DTEL_REPORT_SESSION_ATTR_SRC_IP                  |           -            |
\t  |  SAI_DTEL_REPORT_SESSION_ATTR_DST_IP_LIST             |           -            |
\t  |  SAI_DTEL_REPORT_SESSION_ATTR_VIRTUAL_ROUTER_ID       |           -            |
\t  |  SAI_DTEL_REPORT_SESSION_ATTR_TRUNCATE_SIZE           |           -            |
\t  |  SAI_DTEL_REPORT_SESSION_ATTR_UDP_DST_PORT            |           -            |
\b
\p
 The DTEL Report Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_DTEL_EVENT_ATTR_TYPE                             |           -            |
\t  |  SAI_DTEL_EVENT_ATTR_REPORT_SESSION                   |           -            |
\t  |  SAI_DTEL_EVENT_ATTR_DSCP_VALUE                       |           -            |
\b
*/

#ifndef _CTC_SAI_DTEL_H
#define _CTC_SAI_DTEL_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/


extern sai_status_t
ctc_sai_dtel_api_init();

extern sai_status_t
ctc_sai_dtel_db_init(uint8 lchip);

#endif /*_CTC_SAI_DTEL_H*/

