#ifndef _CTC_SAI_NAT_H
#define _CTC_SAI_NAT_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

#define CTC_SAI_CNT_DNAT 0 
#define CTC_SAI_CNT_SNAT 1

typedef struct ctc_sai_nat_s
{
    sai_nat_type_t nat_type; 
    uint32 nh_id;
    bool dnat_reroute;
    ip_addr_t new_ipsa;
    uint16    new_l4_src_port; 
} ctc_sai_nat_t;

#endif /*_CTC_SAI_NAT_H*/

extern sai_status_t
ctc_sai_nat_api_init();

extern sai_status_t
ctc_sai_nat_db_init(uint8 lchip);

extern void 
ctc_sai_nat_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);


