/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
/*sdk include file*/
#include "ctcs_api.h"
#include "ctc_sai_db.h"
#include "ctc_sai_hostif.h"
#include "ctc_sai_twamp.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_acl.h"
#include "ctc_init.h"

#define CTC_SAI_MIRROR_SESSION_CNT 4
#define CTC_SAI_MIRROR_SAMPLE_RATE_MAX (2<<14)

enum ctc_sai_mirr_op_type_e
{
    CTC_SAI_MIRROR_UPDATE_SESSION,
    CTC_SAI_MIRROR_ALLOC_NH,
    CTC_SAI_MIRROR_UPDATE_NH,     /**< hash application for ecmp */
    CTC_SAI_MIRROR_FREE_NH,       /**< hash application for ecmp */
    CTC_SAI_MIRROR_MAX_NUM,       /**< hash application num */
};
typedef enum ctc_sai_mirr_op_type_e ctc_sai_mirr_op_type_t;

enum ctc_sai_mirr_lkup_result_e
{
    CTC_SAI_MIRROR_LKUP_HIT,
    CTC_SAI_MIRROR_LKUP_ALLOC_NEW,
    CTC_SAI_MIRROR_LKUP_NO_RESOURCE,
    CTC_SAI_MIRROR_LKUP_NUM,
};
typedef enum ctc_sai_mirr_lkup_result_e ctc_sai_mirr_lkup_result_t;

enum ctc_sai_mirr_binding_module_e
{
    CTC_SAI_MIRROR_BINDING_PORT,
    CTC_SAI_MIRROR_BINDING_ACL,      /**< hash application for ecmp */
    CTC_SAI_MIRROR_BINDING_NUM,      /**< hash application num */
};
typedef enum ctc_sai_mirr_binding_module_e ctc_sai_mirr_binding_module_t;

enum ctc_sai_mirr_acl_pri_e
{
    CTC_SAI_MIRROR_ACL_PRI0,
    CTC_SAI_MIRROR_ACL_PRI1,        /**< hash application for ecmp */
    CTC_SAI_MIRROR_ACL_PRI2,
    CTC_SAI_MIRROR_ACL_PRI3,
    CTC_SAI_MIRROR_ACL_PRI4,
    CTC_SAI_MIRROR_ACL_PRI5,
    CTC_SAI_MIRROR_ACL_PRI6,
    CTC_SAI_MIRROR_ACL_PRI7,

    CTC_SAI_MIRROR_ACL_PRI_NUM,     /**< hash application num */
};
typedef enum ctc_sai_mirr_acl_pri_e ctc_sai_mirr_acl_pri_t;

enum ctc_sai_mirr_operate_type_e
{
    CTC_SAI_MIRROR_ADD,
    CTC_SAI_MIRROR_REMOVE,
    CTC_SAI_MIRROR_OPERATE_NUM,      /*  */
};
typedef enum ctc_sai_mirr_operate_type_e ctc_sai_mirr_operate_type_t;

/* mirror_session db */
typedef struct ctc_sai_mirror_session_s
{
    uint64                   dst_port;           /* dst_port */
    uint16                   truncated_size;     /* truncated_size */
    uint32                   sample_rate;        /* sample_rate */
    uint16                   vlan_tpid;          /* vlan_tpid */
    uint16                   vlan_id;            /* vlan_id */
    uint16                   vlan_pri;           /* vlan_pri */
    uint16                   vlan_cfi;           /* vlan_cfi */
    bool                     vlan_hdr_valid;     /* vlan_hdr_valid */
    uint32                   erspan_encap_type;  /* erspan_encap_type */
    uint8                    ip_hdr_ver;         /* ip_hdr_ver */
    uint8                    tos;                /* tos */
    uint8                    ttl;                /* ttl */
    sai_ip_address_t         src_ip_addr;        /* ipv4 or ipv6; src_ip_addr */
    sai_ip_address_t         dst_ip_addr;        /* ipv4 or ipv6; dst_ip_addr */
    mac_addr_t               src_mac_addr;       /* src_mac_addr */
    mac_addr_t               dst_mac_addr;       /* dst_mac_addr */
    uint16                   gre_pro_type;       /* gre_pro_type */
    bool                     dst_port_list_valid;/* dst port list valid */
    uint32                   dst_port_cnt;       /* dst port count */
    uint64                   *dst_port_list;     /* dst port list */

}ctc_sai_mirror_session_t;

typedef struct  ctc_sai_mirr_sess_wb_s
{
    /*key*/
    sai_object_id_t oid;  /* mirror session oid */
    uint32 index;
    uint32 calc_key_len[0];

    /*data*/
    uint64 port_id;
}ctc_sai_mirr_sess_wb_t;

/* mirror session resource management */
typedef struct ctc_sai_mirr_sess_s
{
    sai_object_id_t mirr_session_id;
    uint32 nh_id;
} ctc_sai_mirr_sess_t;

typedef struct ctc_sai_mirr_sess_res_s
{
    uint8  session_ref_cnt;
    ctc_sai_mirr_sess_t* p_mirr_sess;
    uint8  session_list_cnt;
    uint32 mc_nh_id;
    uint32 mc_grp_id;
    uint8  vec_node_index;
} ctc_sai_mirr_sess_res_t;

/* mirror session resource wb db */
typedef struct  ctc_sai_mirr_sess_res_wb_s
{
    /*key*/
    uint8  vec_node_index;
    uint32 index;
    uint32 calc_key_len[0];

    /*data*/
    ctc_sai_mirr_sess_t mirr_sess;
}ctc_sai_mirr_sess_res_wb_t;

typedef struct _ctc_sai_mirr_cb_para_s
{
    uint8              lchip;
    uint64             mirr_session_id;
    ctc_sai_mirror_session_t*  p_mirr_session_old;
    ctc_sai_mirror_session_t*  p_mirr_session_new;
    const sai_attribute_t* attr;
    uint8              op_type;        /*refer to ctc_sai_mirr_op_type_t */
    uint8              vec_index;
    uint8              lkup_result;    /*refer to ctc_sai_mirr_lkup_result_t */
}_ctc_sai_mirr_cb_para_t;

void _ctc_sai_mirror_bubble_sort (uint64 r[], int n)
{
    int low = 0;
    int high = n - 1;                 /* set the initial value of the variable */
    int tmp, j;
    while (low < high)
    {
        for (j = low; j < high; ++j)  /* forward bubble,find the maximum */
            if (r[j] > r[j + 1])
        {
            tmp = r[j];
            r[j] = r[j + 1];
            r[j + 1] = tmp;
        }
        --high;                       /* modifile the value of high, move one ahead */
        for ( j = high; j > low; --j) /* backward bubble,find the minimum */
            if (r[j] < r[j - 1])
        {
            tmp = r[j];
            r[j] = r[j - 1];
            r[j - 1] = tmp;
        }
        ++low;                        /* modifile the value of low, move one back */
    }
}

static int32
_ctc_sai_oid_get_mirror_id(sai_object_id_t oid, uint32* mirr_id)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MIRROR_SESSION, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_MIRROR_SESSION)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Invalid mirror session object type 0x%"PRIx64" \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    *mirr_id = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_lkup_session_alloced(ctc_sai_vector_property_t* bucket_data, sai_object_id_t mirror_session_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    ctc_sai_mirr_sess_res_t* mirr_sess_res = bucket_data->data;

    for (loop_i = 0; loop_i < mirr_sess_res->session_list_cnt; loop_i++)
    {
        if (mirror_session_id == ((mirr_sess_res->p_mirr_sess + loop_i)->mirr_session_id))
        {
            status = SAI_STATUS_OBJECT_IN_USE;
            break;
        }
    }
    return status;
}

static int32
_ctc_sai_mirror_vec_node_index_to_module_dir(uint8 vec_node_index, uint8* module_type, bool* dir, uint8* priority)
{
    if (CTC_SAI_DB_MIRROR_IGS_PORT == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_PORT;
        *dir         = CTC_INGRESS;
    }
    else if(CTC_SAI_DB_MIRROR_EGS_PORT == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_PORT;
        *dir         = CTC_EGRESS;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL0 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI0;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL1 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI1;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL2 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI2;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL3 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI3;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL4 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI4;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL5 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI5;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL6 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI6;
    }
    else if(CTC_SAI_DB_MIRROR_IGS_ACL7 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_INGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI7;
    }
    else if(CTC_SAI_DB_MIRROR_EGS_ACL0 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_EGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI0;
    }
    else if(CTC_SAI_DB_MIRROR_EGS_ACL1 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_EGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI1;
    }
    else if(CTC_SAI_DB_MIRROR_EGS_ACL2 == (vec_node_index / 4))
    {
        *module_type = CTC_SAI_MIRROR_BINDING_ACL;
        *dir         = CTC_EGRESS;
        *priority    = CTC_SAI_MIRROR_ACL_PRI2;
    }

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_operate_nh_mcast(uint8 lchip, uint8 operate_type, const sai_attribute_t *attr, ctc_sai_mirr_sess_res_t* p_mirr_sess_res)
{
    uint32 nh_id_mcast = 0;
    uint32 mc_grp_id = 0;
    uint32 gport = 0;
    uint8 loop_i = 0, loop_j = 0;
    uint8 mirr_type = 0;
    ctc_mcast_nh_param_group_t nh_mcast_group;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;

    sal_memset(&nh_mcast_group, 0, sizeof(ctc_mcast_nh_param_group_t));

    if(CTC_SAI_MIRROR_ALLOC_NH == operate_type)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id_mcast));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, &mc_grp_id));
        nh_mcast_group.is_mirror = 1;
        nh_mcast_group.mc_grp_id = mc_grp_id;

        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_add_mcast(lchip, nh_id_mcast, &nh_mcast_group));

        sal_memset(&nh_mcast_group, 0, sizeof(ctc_mcast_nh_param_group_t));
        for (loop_i = 0; loop_i < p_mirr_sess_res->session_list_cnt; loop_i++)
        {
            p_mirr_session = ctc_sai_db_get_object_property(lchip, p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id);
            ctc_sai_oid_get_sub_type(p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id, &mirr_type);
            nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
            if (SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_type)
            {
                if(!p_mirr_session->dst_port_list_valid)
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port, &gport));
                    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
                    nh_mcast_group.mem_info.destid = gport;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(lchip, nh_id_mcast, &nh_mcast_group));
                }
                else
                {
                    for(loop_j = 0; loop_j < p_mirr_session->dst_port_cnt; loop_j++)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port_list[loop_j], &gport));
                        nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
                        nh_mcast_group.mem_info.destid = gport;
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(lchip, nh_id_mcast, &nh_mcast_group));
                    }
                }


            }
            else if((SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type) || (SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_type))
            {
                nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_LOCAL_WITH_NH;
                nh_mcast_group.mem_info.ref_nhid = p_mirr_sess_res->p_mirr_sess[loop_i].nh_id;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(lchip, nh_id_mcast, &nh_mcast_group));
            }
            p_mirr_sess_res->mc_nh_id = nh_id_mcast;
            p_mirr_sess_res->mc_grp_id = mc_grp_id;
        }
    }
    else if(CTC_SAI_MIRROR_FREE_NH == operate_type)
    {
        nh_id_mcast = p_mirr_sess_res->mc_nh_id;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_mcast(lchip, nh_id_mcast));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id_mcast));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_mirr_sess_res->mc_grp_id));
        p_mirr_sess_res->mc_nh_id = 0;  /* 0 is invalid nexthop id */
        p_mirr_sess_res->mc_grp_id = 0;
    }

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_operate_nh_rspan(uint8 lchip, uint8 operate_type, ctc_sai_mirror_session_t* p_mirr_session, uint8 session_index, ctc_sai_mirr_sess_res_t* p_mirr_sess_res)
{
    uint32 nh_id_xlate = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_vlan_egress_edit_info_t edit_info;
    ctc_vlan_edit_nh_param_t ctc_vlan_edit_nh_param;

    sal_memset(&edit_info, 0, sizeof(ctc_vlan_egress_edit_info_t));
    sal_memset(&ctc_vlan_edit_nh_param, 0, sizeof(ctc_vlan_edit_nh_param_t));

    if(CTC_SAI_MIRROR_ALLOC_NH == operate_type)
    {
        edit_info.svlan_edit_type = CTC_VLAN_EGRESS_EDIT_INSERT_VLAN;
        edit_info.cvlan_edit_type = CTC_VLAN_EGRESS_EDIT_KEEP_VLAN_UNCHANGE;
        CTC_SET_FLAG(edit_info.edit_flag, CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID);
        edit_info.output_svid = p_mirr_session->vlan_id;
        if(p_mirr_session->vlan_pri)
        {
            CTC_SET_FLAG(edit_info.edit_flag, CTC_VLAN_EGRESS_EDIT_REPLACE_SVLAN_COS);
            edit_info.stag_cos = p_mirr_session->vlan_pri;
        }
        ctc_sai_oid_get_gport(p_mirr_session->dst_port, &ctc_vlan_edit_nh_param.gport_or_aps_bridge_id);
        ctc_vlan_edit_nh_param.vlan_edit_info = edit_info;
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id_xlate));
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_xlate(lchip, nh_id_xlate, &ctc_vlan_edit_nh_param), status, error1);

        p_mirr_sess_res->p_mirr_sess[session_index].nh_id = nh_id_xlate;
    }
    else if(CTC_SAI_MIRROR_UPDATE_NH == operate_type)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    else if(CTC_SAI_MIRROR_FREE_NH == operate_type)
    {
        nh_id_xlate = p_mirr_sess_res->p_mirr_sess[session_index].nh_id;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_xlate(lchip, nh_id_xlate));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id_xlate));
        p_mirr_sess_res->p_mirr_sess[session_index].nh_id = 0;  /* 0 is invalid nexthop id */
    }

    return SAI_STATUS_SUCCESS;
    error1:
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id_xlate);
        return status;
}

static int32
_ctc_sai_mirror_operate_nh_iptunnel(uint8 lchip, uint8 operate_type, ctc_sai_mirror_session_t* p_mirr_session, uint8 session_index, ctc_sai_mirr_sess_res_t* p_mirr_sess_res)
{
    uint32 nh_id_iptunnel = 0;
    uint32 gport = 0;
    ctc_ip_tunnel_nh_param_t ctc_ip_tu_nh_param;
    uint8 mirr_type = 0;

    if (CTC_SAI_MIRROR_FREE_NH == operate_type)
    {
        nh_id_iptunnel = p_mirr_sess_res->p_mirr_sess[session_index].nh_id;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_ip_tunnel(lchip, nh_id_iptunnel));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id_iptunnel));
        p_mirr_sess_res->p_mirr_sess[session_index].nh_id = 0;
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&ctc_ip_tu_nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));

    ctc_ip_tu_nh_param.tunnel_info.flag = (CTC_IP_NH_TUNNEL_FLAG_MIRROR | CTC_IP_NH_TUNNEL_FLAG_XERSPN_WITH_EXT_HDR); //0x8080
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port, &gport));
    ctc_ip_tu_nh_param.oif.gport = gport;
    ctc_ip_tu_nh_param.oif.is_l2_port = 1;
    ctc_ip_tu_nh_param.tunnel_info.ttl = p_mirr_session->ttl;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_sub_type(p_mirr_sess_res->p_mirr_sess[session_index].mirr_session_id, &mirr_type));
    ctc_ip_tu_nh_param.tunnel_info.span_id = (p_mirr_sess_res->p_mirr_sess[session_index].mirr_session_id & 0xFF) | ((mirr_type & 3) << 8); /**< [GG.D2] span_id: Assign span_id for erspan session, <0-1023>
                                                                                                                                    1023 -> 256 bit8-9:mirr_type*/
    ctc_ip_tu_nh_param.tunnel_info.dscp_or_tos = p_mirr_session->tos;
    sal_memcpy(&(ctc_ip_tu_nh_param.mac), &(p_mirr_session->dst_mac_addr), sizeof(mac_addr_t));
    sal_memcpy(&(ctc_ip_tu_nh_param.mac_sa), &(p_mirr_session->src_mac_addr), sizeof(mac_addr_t));
    ctc_ip_tu_nh_param.tunnel_info.tunnel_type = (SAI_IP_ADDR_FAMILY_IPV4 == p_mirr_session->dst_ip_addr.addr_family)?
    CTC_TUNNEL_TYPE_GRE_IN4: CTC_TUNNEL_TYPE_GRE_IN6;

    sal_memcpy(&(ctc_ip_tu_nh_param.tunnel_info.ip_sa.ipv6), &(p_mirr_session->src_ip_addr.addr.ip6), sizeof(sai_ip6_t));
    sal_memcpy(&(ctc_ip_tu_nh_param.tunnel_info.ip_da.ipv6), &(p_mirr_session->dst_ip_addr.addr.ip6), sizeof(sai_ip6_t));
    CTC_SAI_NTOH_V6(ctc_ip_tu_nh_param.tunnel_info.ip_sa.ipv6);
    CTC_SAI_NTOH_V6(ctc_ip_tu_nh_param.tunnel_info.ip_da.ipv6);

    ctc_ip_tu_nh_param.tunnel_info.gre_info.protocol_type = p_mirr_session->gre_pro_type;
    if (p_mirr_session->vlan_hdr_valid)
    {
        ctc_ip_tu_nh_param.oif.vid = p_mirr_session->vlan_id;
    }

    if(CTC_SAI_MIRROR_ALLOC_NH == operate_type)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id_iptunnel));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_add_ip_tunnel(lchip, nh_id_iptunnel, &ctc_ip_tu_nh_param));
        p_mirr_sess_res->p_mirr_sess[session_index].nh_id = nh_id_iptunnel;
    }
    else if(CTC_SAI_MIRROR_UPDATE_NH == operate_type)
    {
        ctc_ip_tu_nh_param.upd_type = CTC_NH_UPD_FWD_ATTR;
        nh_id_iptunnel = p_mirr_sess_res->p_mirr_sess[session_index].nh_id;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_ip_tunnel(lchip, nh_id_iptunnel, &ctc_ip_tu_nh_param));
    }

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_operate_session(uint8 lchip, uint8 operate_type, ctc_sai_mirr_sess_res_t*  p_mirr_sess_res)
{
    ctc_mirror_dest_t      ctc_mirr_dst;
    uint8 mirr_session_type = 0;
    uint8 module_type = 0;
    bool dir = 0;
    uint8 priority = 0;
    uint32 gport = 0;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;

    sal_memset(&ctc_mirr_dst, 0, sizeof(ctc_mirror_dest_t));
    ctc_mirr_dst.session_id = (p_mirr_sess_res->vec_node_index)%4;
    p_mirr_session = ctc_sai_db_get_object_property(lchip, p_mirr_sess_res->p_mirr_sess[0].mirr_session_id);
    ctc_mirr_dst.truncated_len = p_mirr_session->truncated_size;

    _ctc_sai_mirror_vec_node_index_to_module_dir(p_mirr_sess_res->vec_node_index, &module_type, &dir, &priority);
    ctc_mirr_dst.dir = dir;
    if (CTC_SAI_MIRROR_BINDING_ACL == module_type)
    {
        ctc_mirr_dst.acl_priority = priority;
        ctc_mirr_dst.type = CTC_MIRROR_ACLLOG_SESSION;
    }
    else if(CTC_SAI_MIRROR_BINDING_PORT == module_type)
    {
        ctc_mirr_dst.type = CTC_MIRROR_L2SPAN_SESSION;
    }

    if (CTC_SAI_MIRROR_ADD == operate_type)
    {
        if (p_mirr_sess_res->mc_nh_id)
        {
            ctc_mirr_dst.is_rspan = 1;
            ctc_mirr_dst.rspan.nh_id = p_mirr_sess_res->mc_nh_id; /* 1:N; mcast nexthop */
        }
        else
        {
            ctc_sai_oid_get_sub_type(p_mirr_sess_res->p_mirr_sess[0].mirr_session_id, &mirr_session_type);
            if (SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_session_type)
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port, &gport));
                ctc_mirr_dst.dest_gport = gport;
            }
            else if(SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_session_type)
            {
                ctc_mirr_dst.is_rspan = 1;
                ctc_mirr_dst.rspan.nh_id = p_mirr_sess_res->p_mirr_sess[0].nh_id; /* rsapn: rspan nexthop */
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port, &gport));
                ctc_mirr_dst.dest_gport = gport;
            }
            else if(SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_session_type)
            {
                ctc_mirr_dst.is_rspan = 1;
                ctc_mirr_dst.rspan.nh_id = p_mirr_sess_res->p_mirr_sess[0].nh_id; /* ersapn: iptunnel nexthop */
            }
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mirror_add_session(lchip, &ctc_mirr_dst));
    }
    else if(CTC_SAI_MIRROR_REMOVE == operate_type)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mirror_remove_session(lchip, &ctc_mirr_dst));
    }

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_lkup_set_attr(ctc_sai_vector_property_t* bucket_data, _ctc_sai_mirr_cb_para_t* cb_para)
{
    uint8 loop_i = 0, loop_j = 0;
    uint8 module_type =0;
    uint8 mirr_type =0;
    bool  dir = 0;
    uint8 priority =0;
    uint32 gport = 0;
    uint8 is_mcast = 0, is_port_list_old = 0;
    ctc_mcast_nh_param_group_t nh_mcast_group;
    ctc_sai_mirror_session_t* p_mirr_session = cb_para->p_mirr_session_old;
    ctc_sai_mirror_session_t* p_mirr_session_new = cb_para->p_mirr_session_new;
    ctc_sai_mirr_sess_res_t* mirr_sess_res = bucket_data->data;

    if (NULL == mirr_sess_res)
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&nh_mcast_group,0,sizeof(ctc_mcast_nh_param_group_t));

    ctc_sai_oid_get_sub_type(cb_para->mirr_session_id, &mirr_type);
    _ctc_sai_mirror_vec_node_index_to_module_dir(mirr_sess_res->vec_node_index, &module_type, &dir, &priority);


    is_mcast = (mirr_sess_res->session_list_cnt > 1)?1:0;
    is_port_list_old = p_mirr_session->dst_port_list_valid;
    for (loop_i = 0; loop_i < mirr_sess_res->session_list_cnt; loop_i++)
    {
        if (mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id != cb_para->mirr_session_id)
        {
            continue;
        }

        if (SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_type)
        {
            if(is_mcast || is_port_list_old)
            {
                if (!is_port_list_old)
                {
                    /*  first: del old member */
                    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
                    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
                    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port, &gport));
                    nh_mcast_group.mem_info.destid = gport;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));

                    /*  second: add new member */
                    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
                    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session_new->dst_port, &gport));
                    nh_mcast_group.mem_info.destid = gport;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));
                }
                else
                {
                    for(loop_j = 0; loop_j < p_mirr_session->dst_port_cnt; loop_j++)
                    {

                        /*  first: del old member */
                        nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
                        nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
                        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session->dst_port_list[loop_j], &gport));
                        nh_mcast_group.mem_info.destid = gport;
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));
                    }
                    for(loop_j = 0; loop_j < p_mirr_session_new->dst_port_cnt; loop_j++)
                    {
                        /* second: add new member */
                        nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
                        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(p_mirr_session_new->dst_port_list[loop_j], &gport));
                        nh_mcast_group.mem_info.destid = gport;
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));
                    }
                    mem_free(p_mirr_session->dst_port_list);

                }
            }
        }
        else if(SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type)
        {  /* only support SAI_MIRROR_SESSION_ATTR_VLAN_ID ctcs_nh_remove_rspan ctcs_nh_add_rspan ==>>update, cutoff flow */
            /*In order to agree, rspan which is binded not support set*/
            return SAI_STATUS_NOT_SUPPORTED;  /* not binding should support update */
        }
        else if(SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_type)
        {

            CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_nh_iptunnel(cb_para->lchip,
                                                                     CTC_SAI_MIRROR_UPDATE_NH, p_mirr_session_new, loop_i, mirr_sess_res));
            if(is_mcast)
            {
                nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_LOCAL_WITH_NH;
                nh_mcast_group.mem_info.ref_nhid = mirr_sess_res->p_mirr_sess[loop_i].nh_id;

                nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));
                nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(cb_para->lchip, mirr_sess_res->mc_nh_id, &nh_mcast_group));
            }
        }
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_session(cb_para->lchip, CTC_SAI_MIRROR_ADD, mirr_sess_res));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirror_build_db(uint8 lchip, sai_object_id_t mirr_session_obj_id, ctc_sai_mirror_session_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;

    p_mirr_session = mem_malloc(MEM_MIRROR_MODULE, sizeof(ctc_sai_mirror_session_t));
    if (NULL == p_mirr_session)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_mirr_session, 0, sizeof(ctc_sai_mirror_session_t));
    status = ctc_sai_db_add_object_property(lchip, mirr_session_obj_id, (void*)p_mirr_session);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_mirr_session);
    }
    *oid_property = p_mirr_session;

    return status;
}

static sai_status_t
_ctc_sai_mirror_remove_db(uint8 lchip, sai_object_id_t mirr_session_obj_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);
    //CTC_SAI_DB_LOCK(lchip);
    p_mirr_session = ctc_sai_db_get_object_property(lchip, mirr_session_obj_id);
    if (NULL == p_mirr_session)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "The MIRROR session to be removed is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (p_mirr_session->dst_port_list_valid)
    {
        if (NULL == p_mirr_session->dst_port_list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The MIRROR session dst_port_list to be removed is empty\n");
            status = SAI_STATUS_OBJECT_IN_USE;
            goto out;
        }
        else
        {
            mem_free(p_mirr_session->dst_port_list);
        }
    }

    ctc_sai_db_remove_object_property(lchip, mirr_session_obj_id);
    mem_free(p_mirr_session);
out:
    //CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
_ctc_sai_mirror_create_mirr_session_attr_chk(uint32_t attr_count, const sai_attribute_t *attr_list, uint8* mirr_session_type)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint8 mirr_type;
    uint32 attr_index = 0;
    uint8  loop_i = 0;
    uint8 port_list_valid = 0;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        mirr_type = attr_value->s32;
    }
    else
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        port_list_valid = 1;
    }

    if(port_list_valid)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST, &attr_value, &attr_index);
        if (status != SAI_STATUS_SUCCESS )
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }
    else
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, &attr_value, &attr_index);
        if (status != SAI_STATUS_SUCCESS )
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if(CTC_SAI_MIRROR_SAMPLE_RATE_MAX < attr_value->s32)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if ((SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_type) || (SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type))
        {
            CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to create mirror session, mirror type is not match with the attr; mirror type: % d, attr id: % d !\n", mirr_type, SAI_MIRROR_SESSION_ATTR_VLAN_ID);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

#if 0
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_ID, &attr_value, &attr_index);
    if (status != SAI_STATUS_SUCCESS )
    {
        if ( (SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type) || (vlan_valid) )
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }
    else
    {
        if (SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_type)
        {
            CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to create mirror session, mirror type is not match with the attr; mirror type: % d, attr id: % d !\n", mirr_type, SAI_MIRROR_SESSION_ATTR_VLAN_ID);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }
#endif

    for (loop_i = SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE; loop_i < SAI_MIRROR_SESSION_ATTR_END; loop_i++)
    {
        if ((loop_i >= SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID) || (loop_i == SAI_MIRROR_SESSION_ATTR_TTL))
        {
            continue;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, loop_i, &attr_value, &attr_index);
        if (status != SAI_STATUS_SUCCESS )
        {
            if (SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_type)
            {
                return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            }
        }
        else
        {
            if ((SAI_MIRROR_SESSION_TYPE_LOCAL == mirr_type) || (SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type))
            {
                CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to create mirror session, mirror type is not match with the attr; mirror type: % d, attr id: % d !\n", mirr_type, SAI_MIRROR_SESSION_ATTR_VLAN_ID);
                return SAI_STATUS_INVALID_PARAMETER;
            }
        }

    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_TPID, &attr_value, &attr_index);
    if(status == SAI_STATUS_SUCCESS)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }


    *mirr_session_type = mirr_type;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirror_build_mirr_session_attr(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list,
                                        ctc_sai_mirror_session_t* p_mir_session)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32 attr_index = 0;
    uint32 i = 0;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->dst_port_list_valid = attr_value->booldata;
    }

    if(p_mir_session->dst_port_list_valid)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST, &attr_value, &attr_index);
        if (status == SAI_STATUS_SUCCESS )
        {
            p_mir_session->dst_port_list_valid = TRUE;
            p_mir_session->dst_port_cnt = attr_value->objlist.count;
            p_mir_session->dst_port_list = mem_malloc(MEM_MIRROR_MODULE, p_mir_session->dst_port_cnt*sizeof(uint64));
            for (i = 0; i<attr_value->objlist.count; i++)
            {
                p_mir_session->dst_port_list[i] = attr_value->objlist.list[i];
            }
        }
    }
    else
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, &attr_value, &attr_index);
        if (status == SAI_STATUS_SUCCESS )
        {
            p_mir_session->dst_port = attr_value->oid;
        }
    }


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->truncated_size = attr_value->u16;
    }

    p_mir_session->sample_rate = 1;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->sample_rate = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_TC, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "_ctc_sai_mirror_build_mirr_session_attr :: SAI_MIRROR_SESSION_ATTR_TC isn't supported, ignore it !\n");
// TODO:         return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
    }
    p_mir_session->vlan_tpid = 0x8100;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_TPID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->vlan_tpid = attr_value->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->vlan_id = attr_value->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_PRI, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->vlan_pri = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_CFI, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->vlan_cfi = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->vlan_hdr_valid = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->erspan_encap_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->ip_hdr_ver = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_TOS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->tos = attr_value->u8;
    }

    p_mir_session->ttl = 255;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_TTL, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->ttl = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->src_ip_addr.addr_family = attr_value->ipaddr.addr_family;
        if ( SAI_IP_ADDR_FAMILY_IPV4 == p_mir_session->src_ip_addr.addr_family)
        {
            p_mir_session->src_ip_addr.addr.ip4 = attr_value->ipaddr.addr.ip4;
        }
        else
        {
            sal_memcpy(p_mir_session->src_ip_addr.addr.ip6, attr_value->ipaddr.addr.ip6, sizeof(sai_ip6_t));
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->dst_ip_addr.addr_family = attr_value->ipaddr.addr_family;
        if ( SAI_IP_ADDR_FAMILY_IPV4 == p_mir_session->dst_ip_addr.addr_family)
        {
            p_mir_session->dst_ip_addr.addr.ip4 = attr_value->ipaddr.addr.ip4;
        }
        else
        {
            sal_memcpy(p_mir_session->dst_ip_addr.addr.ip6, attr_value->ipaddr.addr.ip6, sizeof(sai_ip6_t));
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        sal_memcpy(p_mir_session->src_mac_addr, attr_value->mac, sizeof(sai_mac_t));
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        sal_memcpy(p_mir_session->dst_mac_addr, attr_value->mac, sizeof(sai_mac_t));
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_mir_session->gre_pro_type = attr_value->u16;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirr_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 sample_rate_old = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t mirr_session_old;
    ctc_sai_mirror_session_t*       p_mirr_session = NULL;
    _ctc_sai_mirr_cb_para_t mirr_cb_parm;
    uint32 i = 0;
    uint8 port_list_set = 0;

    sal_memset(&mirr_cb_parm, 0, sizeof(_ctc_sai_mirr_cb_para_t));
    mirr_cb_parm.mirr_session_id = key->key.object_id;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_mirr_session = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_mirr_session)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to set mirror session, invalid mirror session id 0x%"PRIx64"!\n", key->key.object_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&mirr_session_old, 0, sizeof(mirr_session_old));
    sal_memcpy(&mirr_session_old, p_mirr_session, sizeof(mirr_session_old));

    mirr_cb_parm.lchip = lchip;
    mirr_cb_parm.p_mirr_session_old = &mirr_session_old;
    mirr_cb_parm.p_mirr_session_new = p_mirr_session;
    mirr_cb_parm.attr = attr;

    switch(attr->id)
    {
    case SAI_MIRROR_SESSION_ATTR_MONITOR_PORT:
        p_mirr_session->dst_port = attr->value.oid;
        break;
    case SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE:
        p_mirr_session->truncated_size = attr->value.u16;
        break;
    case SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE:
        {
            sample_rate_old = p_mirr_session->sample_rate;
            p_mirr_session->sample_rate = attr->value.u32;
            status = ctc_sai_acl_set_mirror_sample_rate(lchip, key->key.object_id);
            if (SAI_STATUS_SUCCESS != status)
            {
                p_mirr_session->sample_rate = sample_rate_old;
                CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to set mirror session sample rate, mirror session id: 0x%"PRIx64"!\n", key->key.object_id);
            }
            return SAI_STATUS_SUCCESS;
        }
        break;
    case SAI_MIRROR_SESSION_ATTR_VLAN_ID:
        p_mirr_session->vlan_id = attr->value.u16;
        break;
    case SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION:
        p_mirr_session->ip_hdr_ver = attr->value.u8;
        break;
    case SAI_MIRROR_SESSION_ATTR_TOS:
        p_mirr_session->tos = attr->value.u8;
        break;
    case SAI_MIRROR_SESSION_ATTR_TTL:
        p_mirr_session->ttl = attr->value.u8;
        break;
    case SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS:
        {
            p_mirr_session->src_ip_addr.addr_family = attr->value.ipaddr.addr_family;
            if (SAI_IP_ADDR_FAMILY_IPV4 == p_mirr_session->src_ip_addr.addr_family)
            {
                p_mirr_session->src_ip_addr.addr.ip4 = attr->value.ipaddr.addr.ip4;
            }
            else
            {
                sal_memcpy(p_mirr_session->src_ip_addr.addr.ip6, attr->value.ipaddr.addr.ip6, sizeof(sai_ip6_t));
            }
            break;
        }
    case SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS:
        {
            p_mirr_session->dst_ip_addr.addr_family = attr->value.ipaddr.addr_family;
            if ( SAI_IP_ADDR_FAMILY_IPV4 == p_mirr_session->dst_ip_addr.addr_family)
            {
                p_mirr_session->dst_ip_addr.addr.ip4 = attr->value.ipaddr.addr.ip4;
            }
            else
            {
                sal_memcpy(p_mirr_session->dst_ip_addr.addr.ip6, attr->value.ipaddr.addr.ip6, sizeof(sai_ip6_t));
            }
            break;
        }
    case SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS:
        sal_memcpy(p_mirr_session->src_mac_addr, attr->value.mac, sizeof(sai_mac_t));
        break;
    case SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS:
        sal_memcpy(p_mirr_session->dst_mac_addr, attr->value.mac, sizeof(sai_mac_t));
        break;
    case SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE:
        p_mirr_session->gre_pro_type = attr->value.u16;
        break;
    case SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID:
        p_mirr_session->vlan_hdr_valid = attr->value.booldata;
        break;
    case SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE:
        {
            if(attr->value.u8 != SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT)
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
        }
        break;
    case SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID:
        //CREATE_ONLY
        return SAI_STATUS_INVALID_ATTRIBUTE_0;
        break;
    case SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST:
        if(p_mirr_session->dst_port_list_valid)
        {
            p_mirr_session->dst_port_cnt = attr->value.objlist.count;
            p_mirr_session->dst_port_list = mem_malloc(MEM_MIRROR_MODULE, p_mirr_session->dst_port_cnt*sizeof(uint64));

            for (i = 0; i<attr->value.objlist.count; i++)
            {
                p_mirr_session->dst_port_list[i] = attr->value.objlist.list[i];
            }

            port_list_set = 1;
        }
        else
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0;
        }
        break;
    default:
        return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_vector_traverse   /* if traverse hit, it means bindinged */
             (lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (vector_traversal_fn) _ctc_sai_mirror_lkup_set_attr, &mirr_cb_parm), status, out);

    return SAI_STATUS_SUCCESS;

out:
    if(port_list_set)
    {
        mem_free(p_mirr_session->dst_port_list);
    }
    sal_memcpy(p_mirr_session,&mirr_session_old, sizeof(mirr_session_old));
    return status;
}

static sai_status_t
_ctc_sai_mirr_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t*         p_mirr_sess = NULL;
    uint8 mirr_sess_type = 0;
    uint32 i = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_mirr_sess = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_mirr_sess)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_MIRROR_SESSION_ATTR_TYPE:
            CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_sub_type(key->key.object_id, &mirr_sess_type));
            attr->value.s32 = mirr_sess_type;
            break;
        case SAI_MIRROR_SESSION_ATTR_MONITOR_PORT:
            attr->value.oid = p_mirr_sess->dst_port;
            break;
        case SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE:
            attr->value.u16 = p_mirr_sess->truncated_size;
            break;
        case SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE:
            attr->value.u32 = p_mirr_sess->sample_rate;
            break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_TPID:
            attr->value.u16 =  p_mirr_sess->vlan_tpid;
            break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_ID:
            attr->value.u16 =  p_mirr_sess->vlan_id;
            break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_PRI:
            attr->value.u8 =  p_mirr_sess->vlan_pri;
            break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_CFI:
            attr->value.u8 =  p_mirr_sess->vlan_cfi;
            break;
        case SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID:
            attr->value.booldata =  p_mirr_sess->vlan_hdr_valid;
            break;
        case SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE:
            attr->value.s32 =  p_mirr_sess->erspan_encap_type;
            break;
        case SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION:
            attr->value.u8 =  p_mirr_sess->ip_hdr_ver;
            break;
        case SAI_MIRROR_SESSION_ATTR_TOS:
            attr->value.u8 =  p_mirr_sess->tos;
            break;
        case SAI_MIRROR_SESSION_ATTR_TTL:
            attr->value.u8 =  p_mirr_sess->ttl;
            break;
        case SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS:
            {
                attr->value.ipaddr.addr_family = p_mirr_sess->src_ip_addr.addr_family;
                if ( SAI_IP_ADDR_FAMILY_IPV4 == p_mirr_sess->src_ip_addr.addr_family)
                {
                    attr->value.ipaddr.addr.ip4 = p_mirr_sess->src_ip_addr.addr.ip4;
                }
                else
                {
                    sal_memcpy(attr->value.ipaddr.addr.ip6, p_mirr_sess->src_ip_addr.addr.ip6, sizeof(sai_ip6_t));
                }
            }
            break;
        case SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS:
            {
                attr->value.ipaddr.addr_family = p_mirr_sess->src_ip_addr.addr_family;
                if ( SAI_IP_ADDR_FAMILY_IPV4 == p_mirr_sess->src_ip_addr.addr_family)
                {
                    attr->value.ipaddr.addr.ip4 = p_mirr_sess->dst_ip_addr.addr.ip4;
                }
                else
                {
                    sal_memcpy(attr->value.ipaddr.addr.ip6, p_mirr_sess->dst_ip_addr.addr.ip6, sizeof(sai_ip6_t));
                }
            }
            break;
        case SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS:
            sal_memcpy(attr->value.mac, p_mirr_sess->src_mac_addr, sizeof(sai_mac_t));
            break;
        case SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS:
            sal_memcpy(attr->value.mac, p_mirr_sess->dst_mac_addr, sizeof(sai_mac_t));
            break;
        case SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE:
            attr->value.u16 =  p_mirr_sess->gre_pro_type;
            break;
        case SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE:
            attr->value.u8 = SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT;
            break;
        case SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID:
            attr->value.booldata = p_mirr_sess->dst_port_list_valid;
            break;
        case SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST:
            if(p_mirr_sess->dst_port_list_valid)
            {
                if (NULL == p_mirr_sess->dst_port_list)
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
                }
                attr->value.objlist.count = p_mirr_sess->dst_port_cnt;
                for (i = 0; i<p_mirr_sess->dst_port_cnt; i++)
                {
                    attr->value.objlist.list[i] = p_mirr_sess->dst_port_list[i];
                }
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }
            break;
        default: /* SAI_MIRROR_SESSION_ATTR_TC */
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }
    return status;
}

static  ctc_sai_attr_fn_entry_t mirr_session_attr_fn_entries[] =
{
    { SAI_MIRROR_SESSION_ATTR_TYPE, _ctc_sai_mirr_get_attr, NULL},
    { SAI_MIRROR_SESSION_ATTR_MONITOR_PORT,  _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_TC, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_VLAN_TPID, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_VLAN_ID, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_VLAN_PRI,  _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_VLAN_CFI, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_TOS, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_TTL, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID, _ctc_sai_mirr_get_attr, NULL},
    { SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST, _ctc_sai_mirr_get_attr, _ctc_sai_mirr_set_attr},
    { CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL }
};

sai_status_t
ctc_sai_mirror_free_sess_res_index(uint8 lchip, uint8 ctc_dir, uint8 priority, uint8 ctc_session_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    uint8 mirror_db_type =0;
    uint8 ctc_log_id = 0;
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;

    ctc_sai_mirror_mapping_acl_mirror_log_id(lchip, ctc_dir, priority, &ctc_log_id);
    if (ctc_dir)
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_EGS_ACL0 + ctc_log_id;
    }
    else
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_IGS_ACL0 + ctc_log_id;
    }

    p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, ctc_session_id+mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT);
    if (NULL == p_mirr_sess_res)
    {
        return SAI_STATUS_SUCCESS;;
    }

    ctc_sai_db_vector_remove(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i);
    mem_free(p_mirr_sess_res);

    return status;
}

sai_status_t
ctc_sai_mirror_alloc_sess_res_index(uint8 lchip, uint8 ctc_dir, uint8 priority, uint8* ctc_log_id, uint8* ctc_session_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    uint8 mirror_db_type = 0;
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;

    ctc_sai_mirror_mapping_acl_mirror_log_id(lchip, ctc_dir, priority, ctc_log_id);
    if (ctc_dir)
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_EGS_ACL0 + *ctc_log_id;
    }
    else
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_IGS_ACL0 + *ctc_log_id;
    }

    for (loop_i = mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT; loop_i < (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + CTC_SAI_MIRROR_SESSION_CNT); loop_i++)
    {
        p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i);
        if (p_mirr_sess_res)
        {
            continue;
        }
        p_mirr_sess_res = mem_malloc(MEM_MIRROR_MODULE, sizeof(ctc_sai_mirr_sess_res_t));
        if (NULL == p_mirr_sess_res)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_mirr_sess_res, 0, sizeof(ctc_sai_mirr_sess_res_t));

        CTC_SAI_ERROR_GOTO(ctc_sai_db_vector_add(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i, p_mirr_sess_res), status, roll_back_0);
        p_mirr_sess_res->vec_node_index = loop_i;
        p_mirr_sess_res->session_ref_cnt++;
    }
    *ctc_session_id = loop_i%CTC_SAI_MIRROR_SESSION_CNT;

    return SAI_STATUS_SUCCESS;

roll_back_0:

    mem_free(p_mirr_sess_res);

    return status;
}


static sai_status_t
_ctc_sai_mirror_free_sess_res(uint8 lchip, uint8 mirror_db_type, uint8 session_id)
{
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;
    uint8 loop_i = 0;
    uint8 mirr_type =0;

    p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + session_id));
    if(!p_mirr_sess_res)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_mirr_sess_res->session_ref_cnt--;
    if (0 == p_mirr_sess_res->session_ref_cnt)
    {
        /*free nexthop*/
        for (loop_i = 0; loop_i < p_mirr_sess_res->session_list_cnt; loop_i++)
        {
            ctc_sai_oid_get_sub_type(p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id, &mirr_type);
            if (SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type)
            {
                CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_nh_rspan(lchip, CTC_SAI_MIRROR_FREE_NH, NULL, loop_i, p_mirr_sess_res));
            }
            else if(SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_type)
            {
                CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_nh_iptunnel(lchip, CTC_SAI_MIRROR_FREE_NH, NULL, loop_i, p_mirr_sess_res));
            }
        }

        /* Remove mirror session first, then remove nexthop, 2020-02-17 */
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_session(lchip, CTC_SAI_MIRROR_REMOVE, p_mirr_sess_res));

        if (p_mirr_sess_res->mc_nh_id != 0) /* free mcast nexthop */
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_operate_nh_mcast(lchip, CTC_SAI_MIRROR_FREE_NH, NULL, p_mirr_sess_res));
        }

        mem_free(p_mirr_sess_res->p_mirr_sess);
        CTC_SAI_ERROR_RETURN(ctc_sai_db_vector_remove(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + session_id)));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
 _ctc_sai_mirror_alloc_sess_res(uint8 lchip, uint8 mirror_db_type, const sai_attribute_t *attr, uint8* session_id)
{
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    uint8 loop_j = 0;
    sai_object_id_t* p_mirr_oid_list = NULL;
    uint32 count;
    uint64  mirr_oid = 0;
    uint8   mirr_type =0;
    uint8 hit = 0;
    ctc_sai_mirror_session_t*  p_mirr_session = NULL;

    if((CTC_SAI_DB_MIRROR_IGS_PORT == mirror_db_type) || (CTC_SAI_DB_MIRROR_EGS_PORT == mirror_db_type))
    {
        p_mirr_oid_list = attr->value.objlist.list;
        count = attr->value.objlist.count;
    }
    else
    {
        p_mirr_oid_list = attr->value.aclaction.parameter.objlist.list;
        count = attr->value.aclaction.parameter.objlist.count;
    }

    /* First: lkup resource share */
    for (loop_i = mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT; loop_i < (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + CTC_SAI_MIRROR_SESSION_CNT); loop_i++)
    {
        p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i);
        if ((NULL == p_mirr_sess_res)
            || (count != p_mirr_sess_res->session_list_cnt))
        {
            continue;
        }
        _ctc_sai_mirror_bubble_sort(p_mirr_oid_list, count);  /* for lkup compare, need sort */
        hit = 1;
        for (loop_j = 0; loop_j < count; loop_j++)
        {
            if (p_mirr_oid_list[loop_j] != p_mirr_sess_res->p_mirr_sess[loop_j].mirr_session_id)
            {
                hit = 0;
                break;
            }
        }
        if (hit)
        {
            p_mirr_sess_res->session_ref_cnt++;
            goto sucess ;
        }
    }

    /* Second: lkup not alloced resource */
    for (loop_i = mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT; loop_i < (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + CTC_SAI_MIRROR_SESSION_CNT); loop_i++)
    {
        p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i);
        if (p_mirr_sess_res)
        {
            continue;
        }
        p_mirr_sess_res = mem_malloc(MEM_MIRROR_MODULE, sizeof(ctc_sai_mirr_sess_res_t));
        if (NULL == p_mirr_sess_res)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_mirr_sess_res, 0, sizeof(ctc_sai_mirr_sess_res_t));

        p_mirr_sess_res->p_mirr_sess = mem_malloc(MEM_MIRROR_MODULE, sizeof(ctc_sai_mirr_sess_t)*(count));
        if (NULL == p_mirr_sess_res->p_mirr_sess)
        {
            mem_free(p_mirr_sess_res);
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_mirr_sess_res->p_mirr_sess, 0, sizeof(ctc_sai_mirr_sess_t)*count);

        _ctc_sai_mirror_bubble_sort(p_mirr_oid_list, count);  /* for lkup compare, need sort */

        /* add nexthop: rsapn, erspan */
        for (loop_j = 0; loop_j < count; loop_j++) /* nh edit */
        {
            mirr_oid = p_mirr_oid_list[loop_j];
            p_mirr_sess_res->p_mirr_sess[loop_j].mirr_session_id = mirr_oid;

            CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_sub_type(mirr_oid, &mirr_type), status, error0);
            p_mirr_session = ctc_sai_db_get_object_property(lchip, mirr_oid);

            if (SAI_MIRROR_SESSION_TYPE_REMOTE == mirr_type)
            {
                /* rspan, do not support port list */
                if(p_mirr_session->dst_port_list_valid)
                {
                    status = SAI_STATUS_NOT_SUPPORTED;
                    goto error0;
                }
                CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_operate_nh_rspan(lchip, CTC_SAI_MIRROR_ALLOC_NH, p_mirr_session, loop_j, p_mirr_sess_res), status, error0);
            }
            else if(SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE == mirr_type)
            {
                /* espan, do not support port list */
                if(p_mirr_session->dst_port_list_valid)
                {
                    status = SAI_STATUS_NOT_SUPPORTED;
                    goto error0;
                }
                CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_operate_nh_iptunnel(lchip, CTC_SAI_MIRROR_ALLOC_NH, p_mirr_session, loop_j, p_mirr_sess_res), status, error0);
            }
        }
        p_mirr_sess_res->session_list_cnt = count;

        if ((count > 1) || (p_mirr_session->dst_port_list_valid)) /* mcast */
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_operate_nh_mcast(lchip, CTC_SAI_MIRROR_ALLOC_NH, attr, p_mirr_sess_res), status, error0);
        }

        CTC_SAI_ERROR_GOTO(ctc_sai_db_vector_add(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i, p_mirr_sess_res), status, error0);
        p_mirr_sess_res->vec_node_index = loop_i;
        p_mirr_sess_res->session_ref_cnt++;
        CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_operate_session(lchip, CTC_SAI_MIRROR_ADD, p_mirr_sess_res), status, error1);

        goto sucess;
    }

    return SAI_STATUS_INSUFFICIENT_RESOURCES;

sucess:
    *session_id = (loop_i%CTC_SAI_MIRROR_SESSION_CNT);
    return SAI_STATUS_SUCCESS;

error1:
    ctc_sai_db_vector_remove(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, loop_i);

error0:
    if (p_mirr_sess_res->p_mirr_sess)
    {
        mem_free(p_mirr_sess_res->p_mirr_sess);
    }
    if (p_mirr_sess_res)
    {
        mem_free(p_mirr_sess_res);
    }
    return status;
}

static sai_status_t
_ctc_sai_mirror_binding_mirr_param_chk(uint8 lchip, uint8 binding_module, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t* p_mir_session = NULL;
    uint32                   truncated_size_fst = 0xFFFFFFFF;
    uint8 loop_i = 0;
    sai_object_list_t objlist;
    char* print_str = NULL;

    print_str = binding_module == CTC_SAI_MIRROR_BINDING_PORT ? "port" :"acl";

    sal_memset(&objlist, 0, sizeof(sai_object_list_t));

    if(CTC_SAI_MIRROR_BINDING_PORT == binding_module)
    {
        objlist.count = attr->value.objlist.count;
        objlist.list = attr->value.objlist.list;
    }
    else if(CTC_SAI_MIRROR_BINDING_ACL == binding_module)
    {
        objlist.count = attr->value.aclaction.parameter.objlist.count;
        objlist.list = attr->value.aclaction.parameter.objlist.list;
    }

    if (objlist.count >= 1) /* enable */
    {
        for (loop_i = 0; loop_i < objlist.count; loop_i++)
        {
            p_mir_session = ctc_sai_db_get_object_property(lchip, objlist.list[loop_i]);
            if (NULL == p_mir_session)
            {
                CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to binding mirror session to %s, invalid mirror_session_id 0x%"PRIx64"!\n",\
                     print_str, attr->value.aclaction.parameter.objlist.list[loop_i]);
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if(0xFFFFFFFF == truncated_size_fst)
            {
                truncated_size_fst = p_mir_session->truncated_size;
            }
            else if (truncated_size_fst != p_mir_session->truncated_size)
            {
                CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to binding mirror session to %s, truncated_size is not same;\
                    session_id: 0x%"PRIx64"!\n", print_str, objlist.list[loop_i]);
                status = SAI_STATUS_INVALID_PARAMETER;
            }
            if((CTC_SAI_MIRROR_BINDING_PORT == binding_module) && (1 != p_mir_session->sample_rate))
            {
                CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to binding mirror session to %s, port mirror is not support sample rate;", \
                    print_str);
                status = SAI_STATUS_NOT_SUPPORTED;
            }
        }
    }
    return status;
}

static sai_status_t
_ctc_sai_mirror_session_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t mirror_session_id = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_mirror_session_t* p_mir_session = (ctc_sai_mirror_session_t*)data;
    ctc_sai_mirr_sess_wb_t mirror_session_wb;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_mirr_sess_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_SESSION);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    for (index = 0; index < p_mir_session->dst_port_cnt; index++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        mirror_session_wb.oid = mirror_session_id;
        mirror_session_wb.index = index;
        sal_memcpy(&mirror_session_wb.port_id, &(p_mir_session->dst_port_list[index]), sizeof(uint64_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &mirror_session_wb, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }


done:
out:
    CTC_WB_FREE_BUFFER(wb_data.buffer);

    return status;
}

static sai_status_t
_ctc_sai_mirror_session_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t obj_id = *(sai_object_id_t*)key;
    ctc_sai_mirror_session_t* p_mirr_session = (ctc_sai_mirror_session_t*)data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));

    if(p_mirr_session->dst_port_cnt)
    {
        p_mirr_session->dst_port_list = mem_malloc(MEM_MIRROR_MODULE, p_mirr_session->dst_port_cnt*sizeof(uint64));

        if(NULL == p_mirr_session->dst_port_list)
        {
            return SAI_STATUS_NO_MEMORY;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirror_session_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t* p_mir_session = NULL;
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    ctc_sai_mirr_sess_wb_t mirror_session_wb;
    ctc_wb_query_t wb_query;
    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_mirr_sess_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_SESSION);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
    offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
    entry_cnt++;
    sal_memcpy(&mirror_session_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_mirr_sess_wb_t));
    p_mir_session = ctc_sai_db_get_object_property(lchip, mirror_session_wb.oid);

    if ((NULL == p_mir_session) || (NULL == p_mir_session->dst_port_list))
    {
        continue;
    }

    sal_memcpy(&(p_mir_session->dst_port_list[mirror_session_wb.index]), &mirror_session_wb.port_id,  sizeof(uint64_t));
    CTC_WB_QUERY_ENTRY_END((&wb_query));
done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
    return ret;
}

static sai_status_t
_ctc_sai_mirror_session_res_wb_sync_cb(uint8 lchip, void* key, void* data) /* no need void* key */
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int ret = 0;
    ctc_wb_data_t wb_data;
    uint32  max_entry_cnt = 0;
    ctc_sai_mirr_sess_res_t* p_mirr_sess = (ctc_sai_mirr_sess_res_t*)data;
    ctc_sai_mirr_sess_res_wb_t mirr_sess_res_wb;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_mirr_sess_res_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_VEC);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    for (index = 0; index < p_mirr_sess->session_list_cnt; index++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        mirr_sess_res_wb.vec_node_index = p_mirr_sess->vec_node_index;
        mirr_sess_res_wb.index = index;
        sal_memcpy(&mirr_sess_res_wb.mirr_sess, &(p_mirr_sess->p_mirr_sess[index]), sizeof(ctc_sai_mirr_sess_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &mirr_sess_res_wb, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }

out:
done:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return ret;
}

static sai_status_t
_ctc_sai_mirror_session_res_wb_reload_cb(uint8 lchip, void* key, void* data)  /* no need void* key */
{
    ctc_sai_mirr_sess_res_t* p_mirr_sess = (ctc_sai_mirr_sess_res_t*)data;

    p_mirr_sess->p_mirr_sess = (ctc_sai_mirr_sess_t*)mem_malloc(MEM_MIRROR_MODULE, p_mirr_sess->session_list_cnt * sizeof(ctc_sai_mirr_sess_t));
    if (NULL ==  p_mirr_sess->p_mirr_sess)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_mirr_sess->p_mirr_sess, 0, p_mirr_sess->session_list_cnt * sizeof(ctc_sai_mirr_sess_t));

    if (0 != p_mirr_sess->mc_nh_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_mirr_sess->mc_nh_id));
    }

    if (0 != p_mirr_sess->mc_grp_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_mirr_sess->mc_grp_id));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirror_session_res_wb_reload_cb1(uint8 lchip)
{
    ctc_sai_mirr_sess_res_t* p_mirr_sess = NULL;
    uint16 entry_cnt = 0;
    ctc_sai_mirr_sess_res_wb_t mirr_sess_res_wb;
    ctc_wb_query_t wb_query;
    uint32 offset = 0;
    sai_status_t           ret = SAI_STATUS_SUCCESS;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_mirr_sess_res_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_VEC);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&mirr_sess_res_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_mirr_sess_res_wb_t));
        p_mirr_sess = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, mirr_sess_res_wb.vec_node_index);
        if (!p_mirr_sess)
        {
            continue;
        }
        sal_memcpy(&(p_mirr_sess->p_mirr_sess[mirr_sess_res_wb.index]), &mirr_sess_res_wb.mirr_sess,  sizeof(ctc_sai_mirr_sess_t));
        if (0 != mirr_sess_res_wb.mirr_sess.nh_id)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, mirr_sess_res_wb.mirr_sess.nh_id));
        }
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mirror_db_deinit_cb(ctc_sai_vector_property_t* bucket_data, void* user_data)
{
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = (ctc_sai_mirr_sess_res_t*)bucket_data->data;

    if (NULL == bucket_data)
    {
        return SAI_STATUS_SUCCESS;
    }
    if (p_mirr_sess_res && p_mirr_sess_res->p_mirr_sess)
    {
        if (p_mirr_sess_res->p_mirr_sess)
        {
            mem_free(p_mirr_sess_res->p_mirr_sess);
        }
    }
    return SAI_STATUS_SUCCESS;
}

#define ________SAI_DUMP________

static
sai_status_t _ctc_sai_mirror_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  mirror_oid_cur = 0;
    ctc_sai_mirror_session_t    mirror_cur;
    sal_file_t p_file = NULL;
    uint8 mirror_type = 0, loop_i = 0;
    uint32 num_cnt = 0;
    char ipsa_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char ipda_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char src_mac_buf[20] = {0};
    char dst_mac_buf[20] = {0};
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&mirror_cur, 0, sizeof(ctc_sai_mirror_session_t));

    mirror_oid_cur = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (mirror_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    ctc_sai_oid_get_sub_type(mirror_oid_cur, &mirror_type);
    sal_memcpy((ctc_sai_mirror_session_t*)(&mirror_cur), bucket_data->data, sizeof(ctc_sai_mirror_session_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "No.%-6d %-16s 0x%016"PRIx64"\n", num_cnt, "Mirror_oid     :", mirror_oid_cur);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    CTC_SAI_LOG_DUMP(p_file, "Mirror_Type :%-6d dst_port:0x%016"PRIx64 " tos     :%-4d ttl     :%-4d truncated_size:%-4d\n",
        mirror_type, mirror_cur.dst_port, mirror_cur.tos, mirror_cur.ttl,mirror_cur.truncated_size);
    CTC_SAI_LOG_DUMP(p_file, "vlan_tpid   :%-6d vlan_hdr_valid   :%-9d vlan_pri:%-4d vlan_cfi:%-4d\n",
         mirror_cur.vlan_tpid, mirror_cur.vlan_hdr_valid, mirror_cur.vlan_pri,mirror_cur.vlan_cfi);
    CTC_SAI_LOG_DUMP(p_file, "gre_pro_type:%-6d erspan_encap_type:%-9d\n",
         mirror_cur.gre_pro_type, mirror_cur.erspan_encap_type);

    CTC_SAI_LOG_DUMP(p_file, "dst_port_list_valid:%-6d dst_port_cnt:%-9d\n",
         mirror_cur.dst_port_list_valid, mirror_cur.dst_port_cnt);
    if (mirror_cur.dst_port_list_valid)
    {
        for(loop_i = 0; loop_i<mirror_cur.dst_port_cnt; mirror_cur.dst_port_cnt++)
        {
            CTC_SAI_LOG_DUMP(p_file, "dst_port_list %-6d dst_port:0x%016"PRIx64 "\n",
                loop_i, mirror_cur.dst_port_list[loop_i]);
        }
    }

    ctc_sai_get_mac_str(mirror_cur.src_mac_addr, src_mac_buf);
    ctc_sai_get_mac_str(mirror_cur.dst_mac_addr, dst_mac_buf);
    CTC_SAI_LOG_DUMP(p_file, "src_mac_addr:%-14s\n", src_mac_buf);
    CTC_SAI_LOG_DUMP(p_file, "dst_mac_addr:%-14s\n", dst_mac_buf);

    ctc_sai_get_ip_str(&mirror_cur.src_ip_addr, ipsa_buf);
    ctc_sai_get_ip_str(&mirror_cur.dst_ip_addr, ipda_buf);

    CTC_SAI_LOG_DUMP(p_file, "src_ip_addr :%-39s\n",ipsa_buf);
    CTC_SAI_LOG_DUMP(p_file, "dst_ip_addr :%-39s\n",ipda_buf);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_mirror_dump_print_vector_cb(ctc_sai_vector_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    bool is_mirr_vector_tmp = 0;
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = (ctc_sai_mirr_sess_res_t*)bucket_data->data;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32*)(p_cb_data->value1));
    is_mirr_vector_tmp = *((bool*)(p_cb_data->value3));

    if(is_mirr_vector_tmp)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d %-15d %-16d %-10d %-14d Mirror_%-16p\n",
             num_cnt, p_mirr_sess_res->session_ref_cnt, p_mirr_sess_res->session_list_cnt,\
             p_mirr_sess_res->mc_nh_id, p_mirr_sess_res->vec_node_index, p_mirr_sess_res->p_mirr_sess);
    }
    else
    {
        if (NULL != p_mirr_sess_res->p_mirr_sess)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-4d Mirror_%-21p 0x%016"PRIx64 " %-10d\n",
                num_cnt, p_mirr_sess_res->p_mirr_sess, p_mirr_sess_res->p_mirr_sess[0].mirr_session_id, p_mirr_sess_res->p_mirr_sess[0].nh_id);
        }
        for (loop_i = 1; loop_i < p_mirr_sess_res->session_list_cnt; loop_i++)
        {
            if (NULL != p_mirr_sess_res->p_mirr_sess)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-33s 0x%016"PRIx64 " %-10d\n", " ", \
                    p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id, p_mirr_sess_res->p_mirr_sess[loop_i].nh_id);
            }
        }
    }
    (*((uint32 *)(p_cb_data->value1)))++;

    return status;
}

void _ctc_sai_mirror_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    bool is_mirr_vector = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "MIRROR");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mirror_session_t");

    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_MIRROR_SESSION,
                                        (hash_traversal_fn)_ctc_sai_mirror_dump_print_cb, (void*)(&sai_cb_data));

    num_cnt = 1;
    is_mirr_vector = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mirr_sess_res_t");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%-4s %-15s %-16s %-10s %-14s p_mirr_sess_name\n", \
        "No.", "session_ref_cnt", "session_list_cnt", "mc_nh_id", "vec_node_index");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;
    sai_cb_data.value3 = &is_mirr_vector;

    ctc_sai_db_vector_traverse(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR,
                               (vector_traversal_fn)_ctc_sai_mirror_dump_print_vector_cb, (void*)(&sai_cb_data));

    num_cnt = 1;
    is_mirr_vector = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, ">>>>DUMP p_mirr_sess List Table(ctc_sai_mirr_sess_t):");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mirr_sess_t");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%-4s %-28s %-18s %-10s\n", \
        "No.", "p_mirr_sess_name", "mirr_session_id", "nh_id");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;
    sai_cb_data.value3 = &is_mirr_vector;

    ctc_sai_db_vector_traverse(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR,
                               (vector_traversal_fn)_ctc_sai_mirror_dump_print_vector_cb, (void*)(&sai_cb_data));
}

#define ________INTERNAL_API________

sai_status_t
ctc_sai_mirror_set_port_mirr(uint8 lchip, uint32 gport, const sai_attribute_t *attr)
{
    bool enable = FALSE;
    uint8 session_id = 0;
    uint8 dir = 0;
    uint8 mirror_db_type = 0;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_binding_mirr_param_chk(lchip,CTC_SAI_MIRROR_BINDING_PORT, attr));
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);

    if ((SAI_PORT_ATTR_INGRESS_MIRROR_SESSION != attr->id)
        && (SAI_PORT_ATTR_EGRESS_MIRROR_SESSION != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    dir = (attr->id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION) ? CTC_INGRESS : CTC_EGRESS;
    mirror_db_type = (attr->id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION) ? CTC_SAI_DB_MIRROR_IGS_PORT : CTC_SAI_DB_MIRROR_EGS_PORT;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mirror_get_port_info(lchip, gport, dir, &enable, &session_id));
    if (enable)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_free_sess_res(lchip, mirror_db_type, session_id));
    }
    enable = FALSE;
    if (attr->value.objlist.count) /* want to enable */
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_alloc_sess_res(lchip, mirror_db_type, attr, &session_id));
        enable = TRUE;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mirror_set_port_en(lchip, gport, dir, enable, session_id));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_mirror_get_port_mirr(uint8 lchip, uint32 gport, sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;
    bool enable = FALSE;
    uint8 session_id;
    uint8 loop_i = 0;
    uint8 dir = 0;
    uint8 mirror_db_type = 0;
    sai_attribute_t attr_temp;

    sal_memset(&attr_temp, 0, sizeof(sai_attribute_t));

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);

    if ((SAI_PORT_ATTR_INGRESS_MIRROR_SESSION != attr->id)
        && (SAI_PORT_ATTR_EGRESS_MIRROR_SESSION != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    dir = (attr->id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION ? CTC_INGRESS : CTC_EGRESS);
    mirror_db_type = (attr->id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION ? CTC_SAI_DB_MIRROR_IGS_PORT : CTC_SAI_DB_MIRROR_EGS_PORT);
    CTC_SAI_ERROR_RETURN(ctcs_mirror_get_port_info(lchip, gport, dir, &enable, &session_id));
    if (FALSE == enable)
    {
        attr->value.objlist.count = 0;
        return SAI_STATUS_SUCCESS;
    }
    p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + session_id));
    attr_temp.value.objlist.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*p_mirr_sess_res->session_list_cnt);
    if (NULL == attr_temp.value.objlist.list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(attr_temp.value.objlist.list, 0, sizeof(sai_object_id_t)*p_mirr_sess_res->session_list_cnt);

    for (loop_i = 0; loop_i < p_mirr_sess_res->session_list_cnt; loop_i++)
    {
        attr_temp.value.objlist.list[loop_i] = p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id;
    }
    status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), attr_temp.value.objlist.list, p_mirr_sess_res->session_list_cnt, &(attr->value.objlist));
    mem_free(attr_temp.value.objlist.list);

    return status;
}

sai_status_t
ctc_sai_mirror_set_acl_mirr(uint8 lchip, uint8 priority, uint8* ctc_log_id, uint8* ctc_session_id, uint32* ctc_sample_rate, sai_attribute_t *attr)
{   /* called by acl SAI_ACL_ACTION_TYPE_MIRROR_INGRESS SAI_ACL_ACTION_TYPE_MIRROR_EGRESS */
    /* priority & dir ==> which tcam; */
    /* ctc_session_id IN_OUT , save it to acl entry db */
    uint8 mirror_db_type = 0;
    uint8 devide_result = 0xFF;
    uint8 devide_cnt = 0;
    uint8 devide_remainder = 0;
    uint8 log_id = 0;
    ctc_direction_t dir = CTC_INGRESS;
    sai_object_list_t objlist;
    ctc_sai_mirror_session_t* p_mir_session = NULL;

    sal_memset(&objlist, 0, sizeof(sai_object_list_t));

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_binding_mirr_param_chk(lchip,CTC_SAI_MIRROR_BINDING_ACL, attr));
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);

    if ((SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS != attr->id)
        && (SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    dir = (attr->id == SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
    ctc_sai_mirror_mapping_acl_mirror_log_id(lchip, dir, priority, &log_id);

    if (attr->id == SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS)
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_EGS_ACL0 + log_id;
    }
    else
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_IGS_ACL0 + log_id;
    }

    if (*ctc_session_id != 0xFF)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_free_sess_res(lchip, mirror_db_type, *ctc_session_id));
    }

    if (attr->value.aclaction.parameter.objlist.count)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_alloc_sess_res(lchip, mirror_db_type, attr, ctc_session_id));
    }

    objlist.count = attr->value.aclaction.parameter.objlist.count;
    objlist.list = attr->value.aclaction.parameter.objlist.list;

    if (NULL == ctc_sample_rate)
    {
        return SAI_STATUS_SUCCESS;
    }
    if (objlist.count >= 1)  /* enable */
    {
        p_mir_session = ctc_sai_db_get_object_property(lchip, objlist.list[0]);
        if (NULL == p_mir_session)
        {
            CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to binding mirror session to acl, invalid mirror_session_id 0x%"PRIx64"!\n", \
                attr->value.aclaction.parameter.objlist.list[0]);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if (0 == p_mir_session->sample_rate) /*invalid value 0xFFFFFFFF represents not sample rate*/
        {
            *ctc_sample_rate = 0xFFFFFFFF;
        }
        else if(1 == p_mir_session->sample_rate)
        {
            *ctc_sample_rate = CTC_LOG_PERCENT_POWER_NEGATIVE_0;
        }
        else
        {
            devide_result = p_mir_session->sample_rate;
            while (devide_result > 1)
            {
                devide_remainder = devide_result%2;
                devide_result = devide_result/2;
                devide_cnt++;
            }
            *ctc_sample_rate = CTC_LOG_PERCENT_MAX - (devide_cnt + devide_remainder)-1;
        }
    }

    if (NULL != ctc_log_id)
    {
        *ctc_log_id = log_id;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_mirror_get_acl_mirr(uint8 lchip, uint8 priority, uint8 ctc_session_id, sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mirr_sess_res_t* p_mirr_sess_res = NULL;
    uint8 loop_i = 0;
    uint8 mirror_db_type = 0;
    uint8 ctc_log_id = 0;
    ctc_direction_t dir = CTC_INGRESS;
    sai_attribute_t attr_temp;

    sal_memset(&attr_temp, 0, sizeof(sai_attribute_t));

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);

    if ((SAI_ACL_ACTION_TYPE_MIRROR_INGRESS != attr->id)
        || (SAI_ACL_ACTION_TYPE_MIRROR_EGRESS != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    dir = (attr->id == SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
    ctc_sai_mirror_mapping_acl_mirror_log_id(lchip, dir, priority, &ctc_log_id);

    if (attr->id == SAI_ACL_ACTION_TYPE_MIRROR_INGRESS)
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_IGS_ACL0 + ctc_log_id;
    }
    else
    {
        mirror_db_type = CTC_SAI_DB_MIRROR_EGS_ACL0 + ctc_log_id;
    }

    if (ctc_session_id == 0xFF)
    {
        attr->value.objlist.count = 0;
        return SAI_STATUS_SUCCESS;
    }
    p_mirr_sess_res = ctc_sai_db_vector_get(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (mirror_db_type*CTC_SAI_MIRROR_SESSION_CNT + ctc_session_id));
    attr_temp.value.objlist.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*p_mirr_sess_res->session_list_cnt);
    if (NULL == attr_temp.value.objlist.list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(attr_temp.value.objlist.list, 0, sizeof(sai_object_id_t)*p_mirr_sess_res->session_list_cnt);
    for (loop_i = 0; loop_i < p_mirr_sess_res->session_list_cnt; loop_i++)
    {
        attr_temp.value.objlist.list[loop_i] = p_mirr_sess_res->p_mirr_sess[loop_i].mirr_session_id;
    }
    status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), attr_temp.value.objlist.list, p_mirr_sess_res->session_list_cnt, &(attr->value.objlist));
    mem_free(attr_temp.value.objlist.list);

    return status;
}

sai_status_t
ctc_sai_mirror_mapping_acl_mirror_log_id(uint8 lchip, ctc_direction_t ctc_dir, uint8 priority, uint8* ctc_log_id)
{
    uint8 chip_type = 0;

    chip_type = ctcs_get_chip_type(lchip);

    if (CTC_CHIP_TSINGMA == chip_type)
    {
        *ctc_log_id = priority;
    }
    else if (CTC_CHIP_TSINGMA_MX == chip_type)
    {
        if (CTC_INGRESS == ctc_dir)
        {
            if (TWAMP_PORT_ACL_LOOKUP_PRIORITY == priority)
            {
                *ctc_log_id = 0;
            }
            else if (CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY == priority)
            {
                *ctc_log_id = 1;
            }
            else if (ACL_INGRESS_PARAELL_TCAM_BLOCK_BASE == priority)
            {
                *ctc_log_id = 2;
            }
            else if (ACL_INGRESS_PARAELL_TCAM_BLOCK_BASE + ACL_INGRESS_PER_BLOCK_TCAM_SLICE == priority)
            {
                *ctc_log_id = 3;
            }
            else if (ACL_INGRESS_SEQUENT_TCAM_BLOCK_BASE == priority)
            {
                *ctc_log_id = 4;
            }
            else if (ACL_INGRESS_GLOBAL_TCAM_BLOCK_BASE == priority)
            {
                *ctc_log_id = 5;
            }
        }
        else
        {
            *ctc_log_id = priority;
        }
    }

    return SAI_STATUS_SUCCESS;
}

void
ctc_sai_mirror_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    CTC_SAI_LOG_DUMP(p_file, "\n");
    CTC_SAI_LOG_DUMP(p_file, "# SAI MIRROR MODULE\n");

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_MIRROR_SESSION))
    {
        _ctc_sai_mirror_dump(lchip, p_file, dump_grep_param);
    }
}

#define ________SAI_API________

static sai_status_t
ctc_sai_mirror_create_mirror_session(sai_object_id_t *mirror_session_id,
                                     sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_mir_session_id = 0;
    sai_object_id_t mir_session_obj_id = 0;
    uint8 lchip = 0;
    uint8 mir_session_type = 0;
    ctc_sai_mirror_session_t* p_mir_session = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);
    CTC_SAI_PTR_VALID_CHECK(mirror_session_id);

    CTC_SAI_ERROR_RETURN(_ctc_sai_mirror_create_mirr_session_attr_chk(attr_count, attr_list, &mir_session_type)); /* param chk */

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_mir_session_id),status,out);

    /* sub_type is mirror session type;  0:SAI_MIRROR_SESSION_TYPE_LOCAL;
                                         1: SAI_MIRROR_SESSION_TYPE_REMOTE;
                                         2: SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE;    */
    mir_session_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_MIRROR_SESSION, lchip, mir_session_type, 0, ctc_mir_session_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_build_db(lchip, mir_session_obj_id, &p_mir_session),status,error1);
    CTC_SAI_ERROR_GOTO(_ctc_sai_mirror_build_mirr_session_attr(lchip, attr_count, attr_list, p_mir_session), status, error2);

    *mirror_session_id = mir_session_obj_id;
     goto out;

error2:
    CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "rollback to error2\n");
    _ctc_sai_mirror_remove_db(lchip, mir_session_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_mir_session_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mirror_remove_mirr_session(sai_object_id_t mirror_session_id)
{
    uint8 lchip = 0;
    sai_status_t               status = SAI_STATUS_SUCCESS;
    ctc_sai_mirror_session_t*  p_mirr_session = NULL;
    uint32 ctc_mirr_session_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mirror_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);
    p_mirr_session = ctc_sai_db_get_object_property(lchip, mirror_session_id);
    if (NULL == p_mirr_session)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to remove mirror session, invalid mirror_session_id 0x%"PRIx64"!\n", mirror_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    /* check mirror_session_id is or not binding to port or acl; traverse vector compare session list with current session id */
    CTC_SAI_ERROR_GOTO(ctc_sai_db_vector_traverse
            (lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (vector_traversal_fn) _ctc_sai_mirror_lkup_session_alloced, (void*)&mirror_session_id), status, out);

    _ctc_sai_mirror_remove_db(lchip, mirror_session_id);

    _ctc_sai_oid_get_mirror_id(mirror_session_id, &ctc_mirr_session_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_mirr_session_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mirror_set_mirr_session_attribute(sai_object_id_t mirror_session_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mirror_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    p_mirr_session = ctc_sai_db_get_object_property(lchip, mirror_session_id);
    if (NULL == p_mirr_session)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MIRROR, "Failed to set mirror session, invalid mirror_session_id 0x%"PRIx64"!\n", mirror_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    key.key.object_id = mirror_session_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_MIRROR_SESSION, mirr_session_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mirror_get_mirr_session_attribute(sai_object_id_t mirror_session_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    ctc_sai_mirror_session_t* p_mirr_session = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mirror_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);

    p_mirr_session = ctc_sai_db_get_object_property(lchip, mirror_session_id);
    if (NULL == p_mirr_session)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    key.key.object_id = mirror_session_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_MIRROR_SESSION, loop, mirr_session_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_mirror_api_t ctc_sai_mirror_api =
{
    ctc_sai_mirror_create_mirror_session,
    ctc_sai_mirror_remove_mirr_session,
    ctc_sai_mirror_set_mirr_session_attribute,
    ctc_sai_mirror_get_mirr_session_attribute
}
;

sai_status_t
ctc_sai_mirror_api_init()
{
    ctc_sai_register_module_api(SAI_API_MIRROR, (void*)&ctc_sai_mirror_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_mirror_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(ctc_sai_db_wb_t));
    wb_info.version = SYS_WB_VERSION_MIRROR;
    wb_info.data_len = sizeof(ctc_sai_mirror_session_t);
    wb_info.wb_sync_cb = _ctc_sai_mirror_session_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_mirror_session_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_mirror_session_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_MIRROR_SESSION, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(ctc_sai_db_wb_t));
    wb_info.version = SYS_WB_VERSION_MIRROR;
    wb_info.data_len = sizeof(ctc_sai_mirr_sess_res_t);
    wb_info.wb_sync_cb = _ctc_sai_mirror_session_res_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_mirror_session_res_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_mirror_session_res_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_VECTOR, CTC_SAI_DB_VECTOR_TYPE_MIRROR, (void*)(&wb_info));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_mirror_db_deinit(uint8 lchip)
{
    ctc_sai_db_vector_traverse(lchip, CTC_SAI_DB_VECTOR_TYPE_MIRROR, \
        (vector_traversal_fn) _ctc_sai_mirror_db_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

