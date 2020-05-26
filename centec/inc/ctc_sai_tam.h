/**
 @file ctc_sai_tam.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-04-28

 @version v2.0

\p
 This module defines SAI TAM.
\b
\p
 The TAM Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |   SUPPORT CHIPS LIST   |
\t  |  create_tam                                           |           -            |
\t  |  remove_tam                                           |           -            |
\t  |  set_tam_attribute                                    |           -            |
\t  |  get_tam_attribute                                    |           -            |
\t  |  create_tam_math_func                                 |           -            |
\t  |  remove_tam_math_func                                 |           -            |
\t  |  set_tam_math_func_attribute                          |           -            |
\t  |  get_tam_math_func_attribute                          |           -            |
\t  |  create_tam_report                                    |           -            |
\t  |  remove_tam_report                                    |           -            |
\t  |  set_tam_report_attribute                             |           -            |
\t  |  get_tam_report_attribute                             |           -            |
\t  |  create_tam_event_threshold                           |           -            |
\t  |  remove_tam_event_threshold                           |           -            |
\t  |  set_tam_event_threshold_attribute                    |           -            |
\t  |  get_tam_event_threshold_attribute                    |           -            |
\t  |  create_tam_tel_type                                  |           -            |
\t  |  remove_tam_tel_type                                  |           -            |
\t  |  set_tam_tel_type_attribute                           |           -            |
\t  |  get_tam_tel_type_attribute                           |           -            |
\t  |  create_tam_transport                                 |           -            |
\t  |  remove_tam_transport                                 |           -            |
\t  |  set_tam_transport_attribute                          |           -            |
\t  |  get_tam_transport_attribute                          |           -            |
\t  |  create_tam_telemetry                                 |           -            |
\t  |  remove_tam_telemetry                                 |           -            |
\t  |  set_tam_telemetry_attribute                          |           -            |
\t  |  get_tam_telemetry_attribute                          |           -            |
\t  |  create_tam_collector                                 |           -            |
\t  |  remove_tam_collector                                 |           -            |
\t  |  set_tam_collector_attribute                          |           -            |
\t  |  get_tam_collector_attribute                          |           -            |
\t  |  create_tam_event_action                              |           -            |
\t  |  remove_tam_event_action                              |           -            |
\t  |  set_tam_event_action_attribute                       |           -            |
\t  |  get_tam_event_action_attribute                       |           -            |
\t  |  create_tam_event                                     |           -            |
\t  |  remove_tam_event                                     |           -            |
\t  |  set_tam_event_attribute                              |           -            |
\t  |  get_tam_event_attribute                              |           -            |
\b
\p
 The TAM attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST                  |           -            |
\t  |  SAI_TAM_ATTR_EVENT_OBJECTS_LIST                      |           -            |
\t  |  SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST                |           -            |
\b
\p
 The TAM Math Func attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE        |           -            |
\b
\p
 The TAM Report attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_REPORT_ATTR_TYPE                             |           -            |
\t  |  SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS         |           -            |
\t  |  SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY           |           -            |
\b
\p
 The TAM Event Threshold attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK          |           -            |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK           |           -            |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY                 |           -            |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_RATE                    |           -            |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE               |           -            |
\t  |  SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT                    |           -            |
\b
\p
 The TAM Tel Type attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                       |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE                         |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS                   |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS           |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS            |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS          |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS           |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS                    |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS                 |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS                 |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS   |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q                                   |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE                                  |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE                                 |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC                                  |           -            |
\t  |  SAI_TAM_TEL_TYPE_ATTR_REPORT_ID                                  |           -            |
\b
\p
 The TAM Telemetry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST                 |           -            |
\t  |  SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST                |           -            |
\t  |  SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT            |           -            |
\t  |  SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL            |           -            |
\t  |  SAI_TAM_TRANSPORT_ATTR_MTU                           |           -            |
\b
\p
 The TAM Collector attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_COLLECTOR_ATTR_SRC_IP                        |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_DST_IP                        |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_LOCALHOST                     |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID             |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE                 |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_TRANSPORT                     |           -            |
\t  |  SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE                    |           -            |
\b
\p
 The TAM Microburst attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE                |           -            |
\t  |  SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE            |           -            |
\b
\p
 The TAM Histogram attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_TAM_EVENT_ATTR_TYPE                              |           -            |
\t  |  SAI_TAM_EVENT_ATTR_ACTION_LIST                       |           -            |
\t  |  SAI_TAM_EVENT_ATTR_COLLECTOR_LIST                    |           -            |
\t  |  SAI_TAM_EVENT_ATTR_THRESHOLD                         |           -            |
\t  |  SAI_TAM_EVENT_ATTR_DSCP_VALUE                        |           -            |
\b
*/

#ifndef _CTC_SAI_TAM_H
#define _CTC_SAI_TAM_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/


extern sai_status_t
ctc_sai_tam_api_init();

extern sai_status_t
ctc_sai_tam_db_init(uint8 lchip);

#endif /*_CTC_SAI_TAM_H*/

