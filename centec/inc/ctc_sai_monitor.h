
/**
 @file ctc_sai_monitor.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-06-21

 @version v2.0

\p
 This module defines SAI Monitor.
\b
\p
 The Monitor Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\t  |  create_monitor_buffer;                                   |        CTC7132         |
\t  |  remove_monitor_buffer;                                   |        CTC7132         |
\t  |  set_monitor_buffer_attribute;                            |        CTC7132         |
\t  |  get_monitor_buffer_attribute;                            |        CTC7132         |
\t  |  create_monitor_latency;                                  |        CTC7132         |
\t  |  remove_monitor_latency;                                  |        CTC7132         |
\t  |  set_monitor_latency_attribute;                           |        CTC7132         |
\t  |  get_monitor_latency_attribute;                           |        CTC7132         |
\b
\p
 The monitor buffer attributes supported by centec devices:
\p
\b
\t  |   Monitor Buffer  ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT                                     |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN                    |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX                    |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE     |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE      |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK            |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK          |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK              |        CTC7132         |
\t  |  SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK             |        CTC7132         |
\b
\p
 The monitor latency attributes supported by centec devices:
\p
\b
\t  |   Monitor latency  ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT                                     |        CTC7132         |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE                                   |        CTC7132         |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT                     |        CTC7132         |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE                  |        CTC7132         |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD                            |        CTC7132         |
\t  |  SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK                           |        CTC7132         |
\b
*/

#ifndef _CTC_SAI_MONITOR_H
#define _CTC_SAI_MONITOR_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

#define BUFFER_MB_TOTAL_THRD_MAX 5000000
#define BUFFER_MB_TOTAL_THRD_MIN 2000000
#define BUFFER_MB_PORT_THRD_MAX 10000
#define BUFFER_MB_PORT_THRD_MIN  3000
#define MB_LEVEL 8

#define LATENCY_MB_TOTAL_THRD_MAX 5000000
#define LATENCY_MB_TOTAL_THRD_MIN 2000000

#define CHANNEL_ID_MAX 64
#define TM_CELL_TO_BYTE 288

typedef struct ctc_sai_monitor_buffer_db_s
{
    sai_object_id_t port_id;
    bool buffer_mb_enable;
    bool mb_overthreshold_event;
    uint32 mb_port_thrd_min;
    uint32 mb_port_thrd_max;
    bool ingress_perio_monitor_enable;
    bool egress_perio_monitor_enable;
    bool ingress_port_perio_monitor_enable;
    bool egress_port_perio_monitor_enable;
    uint32 perio_monitor_interval;
               
} ctc_sai_monitor_buffer_db_t;


typedef struct ctc_sai_monitor_latency_db_s
{
    sai_object_id_t port_id;
    uint32 perio_monitor_interval;
    bool latency_mb_enable;
    uint8 overthreshold_event_bmp;
    bool perio_monitor_enable;
    uint8 discard_bmp;
        
} ctc_sai_monitor_latency_db_t;

extern sai_status_t
ctc_sai_monitor_api_init();

extern sai_status_t
ctc_sai_monitor_buffer_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_monitor_latency_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_monitor_mapping_to_byte(uint8 lchip, uint32 cell, uint32 byte );

extern sai_status_t
ctc_sai_monitor_mapping_from_byte(uint8 lchip,uint32 cell, uint32 byte );

extern void
ctc_sai_monitor_buffer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_monitor_latency_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_MONITOR_H*/
