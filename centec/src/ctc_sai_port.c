
/*ctc_sai include file*/
#include "ctc_sai_port.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_samplepacket.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_isolation_group.h"
#include "ctc_sai_debug_counter.h"
#include "ctc_sai_es.h"
#include "ctc_sai_ptp.h"

/*sdk include file*/
#include "ctcs_api.h"

typedef struct  ctc_sai_port_wb_s
{
    /*key*/
    sai_object_id_t port_oid;
    uint32 calc_key_len[0];
    /*data*/
    uint16 service_id;

}ctc_sai_port_wb_t;


static sai_status_t
_ctc_sai_port_set_max_frame(uint8 lchip, uint32 gport, uint32 value)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 index = 0;
    uint32 id = 0;
    uint16 value_tmp = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip)) || (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip)))
    {
        for (index = 0; index<CTC_FRAME_SIZE_MAX; index++)
        {
            CTC_SAI_ERROR_RETURN(ctcs_get_max_frame_size(lchip, index, &value_tmp));
            if (value_tmp == value)
            {
                CTC_SAI_LOG_INFO(SAI_API_PORT, "get max frame size %d index %d!", value, index);
                break;
            }
        }

        if (index == CTC_FRAME_SIZE_MAX)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_MAX_FRAME_SIZE, &id));
            CTC_SAI_CTC_ERROR_GOTO(ctcs_set_max_frame_size(lchip, id, value), status, roll_back_0);
            p_switch_master->max_frame_idx_cnt[id] = 1;
        }
        else
        {
            id = index;
            p_switch_master->max_frame_idx_cnt[id]++;
        }
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_max_frame(lchip, gport, value), status, roll_back_1);

    return SAI_STATUS_SUCCESS;
roll_back_1:
    p_switch_master->max_frame_idx_cnt[id]--;
roll_back_0:
    if (index == CTC_FRAME_SIZE_MAX)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_MAX_FRAME_SIZE, id);
    }

    return status;
}

static sai_status_t
_ctc_sai_port_unset_max_frame(uint8 lchip, uint32 gport)
{
    uint32 index = 0;
    uint32 max_frame_size = 0;
    uint16 value_tmp = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_max_frame(lchip, gport, &max_frame_size));
    for (index = 0; index<CTC_FRAME_SIZE_MAX; index++)
    {
        CTC_SAI_ERROR_RETURN(ctcs_get_max_frame_size(lchip, index, &value_tmp));
        if (value_tmp == max_frame_size)
        {
            CTC_SAI_LOG_INFO(SAI_API_PORT, "get max frame size %d index %d!", max_frame_size, index);
            break;
        }
    }

    if (index != CTC_FRAME_SIZE_MAX)
    {
        p_switch_master->max_frame_idx_cnt[index]--;
        if (0 == p_switch_master->max_frame_idx_cnt)
        {
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_MAX_FRAME_SIZE, index);
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_port_get_port_db(sai_object_id_t port_id, ctc_sai_port_db_t** p_port)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};
    ctc_object_id_t ctc_oid;
    ctc_sai_port_db_t* p_port_temp = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_oid);
    if (ctc_oid.type != SAI_OBJECT_TYPE_PORT)
    {
        CTC_SAI_LOG_INFO(SAI_API_PORT, "Invalid Port oid type!");
        return SAI_STATUS_INVALID_OBJECT_TYPE;
    }
    lchip = ctc_oid.lchip;

    p_port_temp = ctc_sai_db_get_object_property(lchip, port_id);
    if (NULL == p_port_temp)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
        if ((CTC_MAP_GPORT_TO_LPORT(ctc_oid.value) & 0xFF) >= capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM])
        {
            CTC_SAI_LOG_INFO(SAI_API_PORT, "Port Exceed Max PhyPort; cur_lport:0x%x, Max_lport:0x%x!\n", CTC_MAP_GPORT_TO_LPORT(ctc_oid.value), capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]-1);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_port_temp = (ctc_sai_port_db_t*)mem_malloc(MEM_PORT_MODULE, sizeof(ctc_sai_port_db_t));
        if (NULL == p_port_temp)
        {
            CTC_SAI_LOG_INFO(SAI_API_PORT, "No Memory!");
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_port_temp, 0, sizeof(ctc_sai_port_db_t));
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, port_id, p_port_temp), status, error_return);

        if(NULL == p_port_temp->service_id_list)
        {
            p_port_temp->service_id_list = ctc_slist_new();
            if (!p_port_temp->service_id_list)
            {
                return SAI_STATUS_NO_MEMORY;
            }
        }
    }



    *p_port = p_port_temp;
    return SAI_STATUS_SUCCESS;

error_return:
    mem_free(p_port_temp);
    return status;
}

sai_status_t _ctc_sai_port_mapping_sai_speed(ctc_port_speed_t speed_mode, uint32* value_out )
{
    switch(speed_mode)
    {
    case CTC_PORT_SPEED_1G:
        *value_out = CTC_SAI_PORT_SPEED_1G;
        break;
    case CTC_PORT_SPEED_100M:
        *value_out =  CTC_SAI_PORT_SPEED_100M;
        break;
    case CTC_PORT_SPEED_10M:
        *value_out =  CTC_SAI_PORT_SPEED_10M;
        break;
    case CTC_PORT_SPEED_2G5:
        *value_out =  CTC_SAI_PORT_SPEED_2G5;
        break;
    case CTC_PORT_SPEED_10G:
        *value_out =   CTC_SAI_PORT_SPEED_10G;
        break;
    case CTC_PORT_SPEED_20G:
        *value_out =  CTC_SAI_PORT_SPEED_20G;
        break;
    case CTC_PORT_SPEED_40G:
        *value_out =  CTC_SAI_PORT_SPEED_40G;
        break;
    case CTC_PORT_SPEED_100G:
        *value_out =  CTC_SAI_PORT_SPEED_100G;
        break;
    case CTC_PORT_SPEED_5G:
        *value_out =  CTC_SAI_PORT_SPEED_5G;
        break;
    case CTC_PORT_SPEED_25G:
        *value_out =  CTC_SAI_PORT_SPEED_25G;
        break;
    case CTC_PORT_SPEED_50G:
        *value_out =  CTC_SAI_PORT_SPEED_50G;
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "error:Unexpected speed mode!");
        return SAI_STATUS_FAILURE;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_port_mapping_sai_fec_mode(ctc_port_fec_type_t fec, sai_port_fec_mode_t* sai_fec_mode )
{
    switch(fec)
    {
    case CTC_PORT_FEC_TYPE_NONE:
        *sai_fec_mode = SAI_PORT_FEC_MODE_NONE;
        break;
    case CTC_PORT_FEC_TYPE_RS:
        *sai_fec_mode =  SAI_PORT_FEC_MODE_RS;
        break;
    case CTC_PORT_FEC_TYPE_BASER:
        *sai_fec_mode =  SAI_PORT_FEC_MODE_FC;
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "error:Unexpected fec mode!");
        return SAI_STATUS_FAILURE;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_port_mapping_ctc_speed_mode(uint32 value_in, ctc_port_speed_t* speed_mode_out )
{
switch(value_in)
    {
    case CTC_SAI_PORT_SPEED_1G :
        *speed_mode_out = CTC_PORT_SPEED_1G;
        break;
    case  CTC_SAI_PORT_SPEED_100M :
        *speed_mode_out = CTC_PORT_SPEED_100M;
        break;
    case CTC_SAI_PORT_SPEED_10M:
        *speed_mode_out = CTC_PORT_SPEED_10M;
        break;
    case CTC_SAI_PORT_SPEED_2G5 :
        *speed_mode_out = CTC_PORT_SPEED_2G5;
        break;
    case CTC_SAI_PORT_SPEED_10G :
        *speed_mode_out = CTC_PORT_SPEED_10G;
        break;
    case CTC_SAI_PORT_SPEED_20G :
        *speed_mode_out = CTC_PORT_SPEED_20G;
        break;
    case CTC_SAI_PORT_SPEED_40G :
        *speed_mode_out = CTC_PORT_SPEED_40G;
        break;
    case CTC_SAI_PORT_SPEED_100G :
        *speed_mode_out = CTC_PORT_SPEED_100G;
        break;
    case CTC_SAI_PORT_SPEED_5G :
        *speed_mode_out = CTC_PORT_SPEED_5G;
        break;
    case CTC_SAI_PORT_SPEED_25G :
        *speed_mode_out = CTC_PORT_SPEED_25G ;
        break;
    case CTC_SAI_PORT_SPEED_50G :
        *speed_mode_out = CTC_PORT_SPEED_50G ;
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "error:Unexpected speed!");
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}






static sai_status_t ctc_sai_port_get_type(  sai_object_key_t   *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint32       gport = 0;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if (CTC_IS_CPU_PORT(gport) || (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN) && (gport == p_switch_master->cpu_eth_port)))
    {
        attr->value.s32 = SAI_PORT_TYPE_CPU;
    }
    else
    {
        attr->value.s32 = SAI_PORT_TYPE_LOGICAL;
    }
    return SAI_STATUS_SUCCESS;
}



static sai_status_t ctc_sai_port_get_basic_info(  sai_object_key_t   *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint32 gport = 0;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint8 gchip = 0;
    int value_link_up = 0;
    uint32 value32 = 0;
    uint32 mode = 0;
    ctc_port_serdes_info_t serdes_port ;
    uint32 mac_id = 0;
    uint32 num = 0;
    uint32 lanes[CTC_PORT_SERDES_MAX_NUM] = {0};
    uint32 speeds[CTC_PORT_SPEED_MAX] = {0};
    uint32 speed = 0;
    uint32 loop = 0;
    uint32 value = 0;
    uint32 fecs[CTC_PORT_FEC_TYPE_MAX];
    uint32 fec = 0;
    uint16 loop1 = 0;
    uint16 loop2 = 0;
    uint16 lport = 0;
    uint16 index = 0;
    ctc_chip_serdes_loopback_t  lb_param;
    ctc_port_fc_prop_t fc_ingress;
    ctc_port_fc_prop_t fc_egress;
    ctc_port_isolation_t port_isolation;
    sai_object_id_t ports[CTC_MAX_PHY_PORT];
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_port_speed_t speed_mode;
    ctc_chip_device_info_t device_info;
    mac_addr_t port_mac;
    sai_object_id_t *p_bounded_oid = NULL;
    ctc_acl_property_t acl_prop;

    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));

    chip_type = ctcs_get_chip_type(lchip);
    switch(attr->id)
    {

    case SAI_PORT_ATTR_OPER_STATUS:
        #if (1 == LINK_STATUS_MODE)
        CTC_SAI_CTC_ERROR_RETURN (ctcs_port_get_mac_link_up(lchip, gport, (void*)&value_link_up));
        #else
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_LINK_UP, (uint32*)&value_link_up));
        #endif
        if (1 == SDK_WORK_PLATFORM)
        {
            attr->value.s32 = SAI_PORT_OPER_STATUS_UP;
        }
        else
        {
            if (value_link_up)
            {
                attr->value.s32 = SAI_PORT_OPER_STATUS_UP;
            }
            else
            {
                attr->value.s32 = SAI_PORT_OPER_STATUS_DOWN;
            }
        }
        break;
    case SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE:
        speeds[0] = SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE;
        speeds[1] = SAI_PORT_BREAKOUT_MODE_TYPE_2_LANE;
        speeds[2] = SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE;
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(int32), speeds, 3, &attr->value.s32list));
        break;

    case SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE:
        sal_memset(&serdes_port, 0, sizeof(serdes_port));
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port), attr_idx);
        if (1 == serdes_port.serdes_num)
        {
            attr->value.s32 = SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE;
        }
        else if (2 == serdes_port.serdes_num)
        {
            attr->value.s32 = SAI_PORT_BREAKOUT_MODE_TYPE_2_LANE;
        }
        else if (4 == serdes_port.serdes_num)
        {
            attr->value.s32 = SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE;
        }
        break;
    case SAI_PORT_ATTR_SPEED:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_speed(lchip, gport, (ctc_port_speed_t*)&value32), attr_idx);
        CTC_SAI_ATTR_ERROR_RETURN(_ctc_sai_port_mapping_sai_speed(value32, &attr->value.u32), attr_idx);
        /* SYSTEM MODIFIED KCAO for UML force to 1G, SAI merge 20200824 */
        if (1 == SDK_WORK_PLATFORM)
        {
            attr->value.u32 = CTC_SAI_PORT_SPEED_1G;
        }
        break;
    case SAI_PORT_ATTR_AUTO_NEG_MODE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_AUTO_NEG_EN, &mode));
        attr->value.booldata  =  (bool)mode;
        break;
    case SAI_PORT_ATTR_ADMIN_STATE:
        /* SYSTEM MODIFIED, duet2 & tsingma SONIC, 20200227, SAI merge 20200824*/
        if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_PHY_EN, &value), attr_idx);
            attr->value.booldata = value ? 1 : 0;
        }
        else
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_mac_en(lchip,gport, &attr->value.booldata), attr_idx);
        }
        break;

    case SAI_PORT_ATTR_PORT_VLAN_ID:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_default_vlan(lchip, gport, &attr->value.u16), attr_idx);
        break;
    case SAI_PORT_ATTR_HW_LANE_LIST:
        /*SYSTEM MODIFIED by jqiu, Bug51934, Sonic does't support multiport map to one serdes lane. In order to support
           Qsgmii port, ctc use mac_id instead of serdes lane.*/
#if 0
        sal_memset(&serdes_port, 0, sizeof(serdes_port));
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port), attr_idx);
        if (CTC_CHIP_DUET2 == chip_type)
        {
            for (num = 0; num < serdes_port.serdes_num; num++)
            {
                lanes[num] = serdes_port.serdes_id_array[num];
            }
        }
        else
        {
            for (num = 0; num < serdes_port.serdes_num; num++)
            {
                lanes[num] = serdes_port.serdes_id+num;
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32), lanes, serdes_port.serdes_num, &attr->value.u32list));
#else
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_MAC_ID, &mac_id), attr_idx);
        lanes[0] = mac_id;
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32), lanes, 1, &attr->value.u32list));
#endif
        break;

    case SAI_PORT_ATTR_SUPPORTED_SPEED:
        if (CTC_CHIP_GOLDENGATE == chip_type)
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port), attr_idx);
            if (((serdes_port.serdes_id >= 40) && (serdes_port.serdes_id <48))
                || ((serdes_port.serdes_id >= 88) && (serdes_port.serdes_id <96)))
            {
                speeds[num++] = CTC_SAI_PORT_SPEED_1G;
                speeds[num++] = CTC_SAI_PORT_SPEED_100M;
                speeds[num++] = CTC_SAI_PORT_SPEED_10M;
                speeds[num++] = CTC_SAI_PORT_SPEED_2G5;
                speeds[num++] = CTC_SAI_PORT_SPEED_10G;
                speeds[num++] = CTC_SAI_PORT_SPEED_20G;
                speeds[num++] = CTC_SAI_PORT_SPEED_40G;
                speeds[num++] = CTC_SAI_PORT_SPEED_100G;
            }
            else
            {
                speeds[num++] = CTC_SAI_PORT_SPEED_1G;
                speeds[num++] = CTC_SAI_PORT_SPEED_100M;
                speeds[num++] = CTC_SAI_PORT_SPEED_10M;
                speeds[num++] = CTC_SAI_PORT_SPEED_2G5;
                speeds[num++] = CTC_SAI_PORT_SPEED_10G;
                speeds[num++] = CTC_SAI_PORT_SPEED_20G;
                speeds[num++] = CTC_SAI_PORT_SPEED_40G;
            }
        }
        else
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SPEED_MODE, &value), attr_idx);
            for (loop = 0; loop < CTC_PORT_SPEED_MAX; loop++)
            {
                if (CTC_IS_BIT_SET(value, loop))
                {
                    CTC_SAI_ATTR_ERROR_RETURN(_ctc_sai_port_mapping_sai_speed(loop, &speed), attr_idx);
                    speeds[num++] = speed;
                }
            }
            /* SYSTEM MODIFIED KCAO for UML force support 1G/10G SAI merge 20200824 */
            if (1 == SDK_WORK_PLATFORM)
            {
                speeds[num++] = CTC_SAI_PORT_SPEED_1G;
                speeds[num++] = CTC_SAI_PORT_SPEED_10G;
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32), speeds, num, &attr->value.u32list));
        break;

    case SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
        // Default cos of vlan tag
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_DEFAULT_PCP, &value), attr_idx);
        attr->value.u8 = (uint8)value;

        break;

    case SAI_PORT_ATTR_FULL_DUPLEX_MODE:
        attr->value.booldata =  true;
        break;

    case SAI_PORT_ATTR_SUPPORTED_FEC_MODE:
        sal_memset(&fecs, 0, sizeof(fecs));
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_FEC_TYPE, &value), attr_idx);

        for (loop = 0; loop < CTC_PORT_FEC_TYPE_MAX; loop++)
        {
            if (CTC_IS_BIT_SET(value, loop))
            {
                CTC_SAI_ATTR_ERROR_RETURN(_ctc_sai_port_mapping_sai_fec_mode(loop, &fec), attr_idx);
                fecs[num++] = fec;
            }
        }

        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32), fecs, num, &attr->value.s32list));
        break;

    case SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED:
        num = 0;
        speeds[num++] = CTC_SAI_PORT_SPEED_100M;
        speeds[num++] = CTC_SAI_PORT_SPEED_10M;
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32), speeds, num, &attr->value.u32list));
        break;

    case SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_AUTO_NEG_EN, &value32));
        attr->value.booldata = (value32)?TRUE:FALSE;
        break;

    case SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
        sal_memset(&fc_ingress, 0, sizeof(ctc_port_fc_prop_t));
        sal_memset(&fc_egress, 0, sizeof(ctc_port_fc_prop_t));
        fc_ingress.gport  = gport;
        fc_ingress.dir    = CTC_INGRESS;
        fc_ingress.is_pfc = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_ingress));
        fc_egress.gport  = gport;
        fc_egress.dir    = CTC_EGRESS;
        fc_egress.is_pfc = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_egress));
        if ((fc_ingress.enable) && (fc_egress.enable))
        {
            attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE;
        }
        else if (fc_ingress.enable)
        {
            attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY;
        }
        else if (fc_egress.enable)
        {
            attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY;
        }
        else
        {
            attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_DISABLE;
        }
        break;

    case SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE:
        attr->value.booldata = FALSE;
        break;

    case SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE:
        attr->value.s32 = SAI_PORT_MEDIA_TYPE_UNKNOWN;
        break;

    case SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE:
        sal_memset(&lb_param, 0, sizeof(lb_param));
        sal_memset(&serdes_port, 0, sizeof(serdes_port));
        /* SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY NOT SUPPORT */
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port), attr_idx);
        lb_param.serdes_id = serdes_port.serdes_id_array[0];
        lb_param.mode = 0;

        CTC_SAI_ATTR_ERROR_RETURN(ctcs_chip_get_property(lchip, CTC_CHIP_PROP_SERDES_LOOPBACK, (void*)&lb_param), attr_idx);
        if (0 == lb_param.enable)
        {
            attr->value.s32 = SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE;
        }
        else
        {
            attr->value.s32 = SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC;
        }
        break;

    case SAI_PORT_ATTR_FEC_MODE:
        attr->value.s32 = SAI_PORT_FEC_MODE_NONE;
        if (CTC_CHIP_GOLDENGATE == chip_type)
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_FEC_EN, &value32), attr_idx);
            if (value32)
            {
                attr->value.s32 = SAI_PORT_FEC_MODE_FC;
            }
        }
        else
        {
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_AUTO_NEG_FEC, &value32), attr_idx);
            if (CTC_PORT_FEC_TYPE_RS == value32)
            {
                attr->value.s32 = SAI_PORT_FEC_MODE_RS;
            }
            else if (CTC_PORT_FEC_TYPE_BASER == value32)
            {
                attr->value.s32 = SAI_PORT_FEC_MODE_FC;
            }
        }
        break;

    case SAI_PORT_ATTR_MTU:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_max_frame(lchip, gport, (ctc_frame_size_t*)&attr->value.u32), attr_idx);
        break;

    case SAI_PORT_ATTR_EEE_ENABLE:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_EEE_EN, &value), attr_idx);
        attr->value.booldata = (bool)value;
        break;
    case SAI_PORT_ATTR_UPDATE_DSCP:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_REPLACE_DSCP_EN, &value), attr_idx);
        attr->value.booldata = (bool)value;
        break;
    case SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_queue_port_get_queue_num(key->key.object_id, &attr->value.u32), attr_idx);
        break;
    case SAI_PORT_ATTR_QOS_QUEUE_LIST:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_queue_port_get_queue_list(key->key.object_id, attr), attr_idx);
        break;
    case SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_buffer_port_get_ingress_pg_num(key->key.object_id, attr), attr_idx);
        break;
    case SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_buffer_port_get_ingress_pg_list(key->key.object_id, attr), attr_idx);
        break;
    case SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_scheduler_group_port_get_sched_group_num(key->key.object_id, attr), attr_idx);
        break;
    case SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
        CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_scheduler_group_port_get_sched_group_list(key->key.object_id, attr), attr_idx);
        break;
    case SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
        {
            ctc_sai_port_db_t* p_port = NULL;
            p_port = ctc_sai_db_get_object_property(lchip, key->key.object_id);
            attr->value.oid = (!p_port || !p_port->sched_id) ?
                        SAI_NULL_OBJECT_ID : ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_port->sched_id);
        }
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE:
        attr->value.s32 = p_port_db->flow_ctl_mode;
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_INGRESS;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            attr->value.u8 = 0;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_prop));
                if (fc_prop.enable)
                {
                    CTC_BIT_SET(attr->value.u8, loop);
                }
            }
        }
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_INGRESS;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            attr->value.u8 = 0;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_prop));
                if (fc_prop.enable)
                {
                    CTC_BIT_SET(attr->value.u8, loop);
                }
            }
        }
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_EGRESS;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            attr->value.u8 = 0;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_prop));
                if (fc_prop.enable)
                {
                    CTC_BIT_SET(attr->value.u8, loop);
                }
            }
        }
        break;
    case SAI_PORT_ATTR_META_DATA:
        sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
        acl_prop.direction = CTC_INGRESS;
        acl_prop.acl_priority = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, gport, &acl_prop));
        attr->value.u32 = CTC_SAI_META_DATA_CTC_TO_SAI(acl_prop.class_id);
        break;
    case SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST:
        sal_memset(&port_isolation, 0, sizeof(port_isolation));
        port_isolation.gport = gport;
        port_isolation.isolation_pkt_type = CTC_PORT_ISOLATION_ALL;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_isolation(lchip, &port_isolation));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
        for (loop1 = 0; loop1 < sizeof(ctc_port_bitmap_t)/sizeof(uint32); loop1++)
        {
            for (loop2 = 0; loop2 < CTC_UINT32_BITS; loop2++)
            {
                if (!CTC_IS_BIT_SET(port_isolation.pbm[loop1], loop2))
                {
                    continue;
                }
                lport = loop1 * CTC_UINT32_BITS + loop2;
                ports[index++] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, CTC_MAP_LPORT_TO_GPORT(gchip, lport));
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), ports, index, &attr->value.objlist));
        break;
    case SAI_PORT_ATTR_PKT_TX_ENABLE:
        CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_TRANSMIT_EN, &value), attr_idx);
        attr->value.booldata = (bool)value;
        break;
    case SAI_PORT_ATTR_ISOLATION_GROUP:
        {
            ctc_port_restriction_t port_restriction;

            sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t));

            port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
            port_restriction.type = CTC_PORT_ISOLATION_ALL;
            port_restriction.dir = CTC_INGRESS;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_restriction(lchip, gport, &port_restriction));
            if (0 != port_restriction.isolated_id)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP, lchip, 0, 0, port_restriction.isolated_id);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
        }
        break;
    case SAI_PORT_ATTR_OPER_SPEED:
        speed_mode = CTC_PORT_SPEED_MAX;
        //#if (1 == LINK_STATUS_MODE)
        bool is_up = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_mac_link_up(lchip, gport, &is_up));
        //#else
        //uint32 is_up = 0;
        //CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_LINK_UP, &is_up));
        //#endif
        if(!is_up)
        {
            attr->value.u32 = 0;
            break;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_speed(lchip, gport, &speed_mode));
        switch (speed_mode)
        {
        case CTC_PORT_SPEED_10M:
            attr->value.u32 = 10;
            break;
        case CTC_PORT_SPEED_100M:
            attr->value.u32 = 100;
            break;
        case CTC_PORT_SPEED_1G:
            attr->value.u32 = 1000;
            break;
        case CTC_PORT_SPEED_2G5:
            attr->value.u32 = 2500;
            break;
        case CTC_PORT_SPEED_10G:
            attr->value.u32 = 10000;
            break;
        case CTC_PORT_SPEED_20G:
            attr->value.u32 = 20000;
            break;
        case CTC_PORT_SPEED_40G:
            attr->value.u32 = 40000;
            break;
        case CTC_PORT_SPEED_100G:
            attr->value.u32 = 100000;
            break;
        case CTC_PORT_SPEED_5G:
            attr->value.u32 = 5000;
            break;
        case CTC_PORT_SPEED_25G:
            attr->value.u32 = 25000;
            break;
        case CTC_PORT_SPEED_50G:
            attr->value.u32 = 50000;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_PORT, "get port wrong port speed\n");
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
        }
        break;
    case SAI_PORT_ATTR_ES:
        ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
        if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
        {
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
        }
        attr->value.oid = p_port_db->ethernet_segment;
        break;
    case SAI_PORT_ATTR_Y1731_ENABLE:
        attr->value.booldata = p_port_db->y1731_oam_en;
        break;
    case SAI_PORT_ATTR_Y1731_LM_ENABLE:
        attr->value.booldata = p_port_db->y1731_lm_en;
        break;
    case SAI_PORT_ATTR_Y1731_MIP_ENABLE:
        if((CTC_CHIP_TSINGMA == chip_type) || (CTC_CHIP_DUET2 == chip_type))
        {
            attr->value.u8 = p_port_db->y1731_mip_bitmap;
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        break;
    case SAI_PORT_ATTR_MAC_ADDRESS:
        sal_memset(&port_mac, 0, sizeof(port_mac));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_port_mac(lchip, gport, &port_mac));
        sal_memcpy(&attr->value.mac, &port_mac, sizeof(sai_mac_t));
        break;

    case SAI_PORT_ATTR_INGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;
    case SAI_PORT_ATTR_EGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "port attribute not implement\n");
        return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;

    }
    return SAI_STATUS_SUCCESS;
}

/* SAI merge 20200824 */
extern int32 sys_usw_peri_get_phy_register_exist(uint8 lchip, uint16 lport);
extern int32 sys_usw_peri_get_phy_id(uint8 lchip, uint16 lport, uint32* phy_id);
extern int32 sys_usw_peri_set_phy_prop(uint8 lchip, uint16 lport, uint16 type, uint32 value);

static sai_status_t ctc_sai_port_set_basic_info(  sai_object_key_t   *key, const sai_attribute_t *attr)
{
    sai_status_t           status;
    uint32      gport = 0;
    uint8 lchip = 0;
    ctc_port_speed_t speed_mode = 0;
    ctc_chip_serdes_loopback_t  lb_param;
    ctc_port_serdes_info_t serdes_port ;
    uint32 loop;
    uint32 num = 0;
    uint32 enable = 0;
    uint32 value = 0;
    uint32 index = 0;
    uint32 gport_temp = 0;
    uint16 lport = 0;
    uint8  i = 0;
    uint8  index_tmp1 = 0;
    uint8  index_tmp2 = 0;
    uint8  ingress_acl_num = 8;
    uint8  egress_acl_num = 3;
    sai_object_id_t port_oid = 0;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_port_isolation_t port_isolation;
    ctc_sai_es_t* p_es = NULL;
    ctc_sai_es_t* p_es_old= NULL;
    ctc_oam_property_t oam_prop;
    ctc_oam_y1731_prop_t* p_eth_prop = NULL;
    uint8 chip_type = 0;
    ctc_chip_device_info_t device_info;
    ctc_port_mac_postfix_t post_mac;
    ctc_acl_property_t acl_prop;

    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));

    chip_type = ctcs_get_chip_type(lchip);

    switch(attr->id)
    {
    case SAI_PORT_ATTR_SPEED:
        /* SYSTEM MODIFIED KCAO for UML not support set speed SAI merge 20200824*/
        if (0 != SDK_WORK_PLATFORM)
        {
            break;
        }

        CTC_SAI_ERROR_RETURN(_ctc_sai_port_mapping_ctc_speed_mode(attr->value.u32, &speed_mode));
        /*SAI merge 20200824 */
        if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
        {
            uint32 phy_id = 0;
            ctc_port_if_mode_t if_mode;
            ctc_port_if_type_t if_type = CTC_PORT_IF_NONE;
            sys_usw_peri_get_phy_id(lchip, CTC_MAP_GPORT_TO_LPORT(gport), &phy_id);
            if ((CTC_E_NONE == sys_usw_peri_get_phy_register_exist(lchip, CTC_MAP_GPORT_TO_LPORT(gport))) && (phy_id != CTC_CHIP_PHY_NULL_PHY_ID))
            {
                CTC_SAI_ERROR_RETURN(sys_usw_peri_set_phy_prop(lchip, CTC_MAP_GPORT_TO_LPORT(gport), CTC_PORT_PROP_SPEED, speed_mode));
                CTC_SAI_ERROR_RETURN(ctcs_port_set_speed(lchip, gport, speed_mode));
            }
            else
            {
                if(speed_mode  == CTC_PORT_SPEED_10G)
                    if_type = CTC_PORT_IF_XFI;
                else if(speed_mode  == CTC_PORT_SPEED_1G)
                    if_type = CTC_PORT_IF_SGMII;
                else if(speed_mode  == CTC_PORT_SPEED_25G)
                    if_type = CTC_PORT_IF_CR;
                else if(speed_mode  == CTC_PORT_SPEED_40G)
                    if_type = CTC_PORT_IF_CR4;
                else if(speed_mode  == CTC_PORT_SPEED_100G)
                    if_type = CTC_PORT_IF_CR4;
                else if(speed_mode  == CTC_PORT_SPEED_50G)
                    if_type = CTC_PORT_IF_CR2;
                else if ((speed_mode  == CTC_PORT_SPEED_100M) && (CTC_CHIP_TSINGMA == chip_type))
                    if_type = CTC_PORT_IF_FX;

                if_mode.speed = speed_mode;
                if_mode.interface_type = if_type;
                CTC_SAI_ERROR_RETURN(ctcs_port_set_interface_mode(lchip, gport, &if_mode));

                if(speed_mode == CTC_PORT_SPEED_1G)
                {
                    CTC_SAI_ERROR_RETURN(ctcs_port_set_speed(lchip, gport, CTC_PORT_SPEED_1G));
                }
            }
        }
        else
        {
            CTC_SAI_ERROR_RETURN(ctcs_port_set_speed(lchip, gport, speed_mode));
        }
        break;

    case SAI_PORT_ATTR_AUTO_NEG_MODE:
        CTC_SAI_CTC_ERROR_RETURN (ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_AUTO_NEG_EN, attr->value.booldata));
        break;

    case SAI_PORT_ATTR_PORT_VLAN_ID:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_default_vlan(lchip, gport, attr->value.u16));
        break;

    case SAI_PORT_ATTR_ADMIN_STATE:
        /* SYSTEM MODIFIED For duet2 & tsingma SONIC, 20200227 SAI merge 20200824*/
        if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_PHY_EN, attr->value.booldata?1:0));
        }
        else
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_mac_en(lchip, gport, attr->value.booldata?1:0));
        }

        if (1 == SDK_WORK_PLATFORM)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_port_en(lchip, gport, attr->value.booldata?1:0));
        }
        break;

    case SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
        status = ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_DEFAULT_PCP, (uint32)attr->value.u8);
        status = ctc_sai_mapping_error_ctc(status);

        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_PORT, "error:set default vlan priority error:%u", status);

            return status;
        }
        break;

    case SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE:
        sal_memset(&lb_param, 0, sizeof(lb_param));
        sal_memset(&serdes_port, 0, sizeof(serdes_port));

        if (SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY == attr->value.s32)
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        else if (SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE == attr->value.s32)
        {
            lb_param.enable = 0;
        }
        else if  (SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC == attr->value.s32)
        {
            lb_param.enable = 1;
        }

        lb_param.mode = 0;

        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port));
        for (num = 0; num < serdes_port.serdes_num; num++)
        {
            lb_param.serdes_id = serdes_port.serdes_id_array[num];
            CTC_SAI_CTC_ERROR_RETURN(ctcs_chip_set_property(lchip, CTC_CHIP_PROP_SERDES_LOOPBACK, (void*)&lb_param));
        }
        break;

    case SAI_PORT_ATTR_FEC_MODE:
        if (SAI_PORT_FEC_MODE_NONE == attr->value.s32)
        {
            enable = 0;
            value = CTC_PORT_FEC_TYPE_NONE;
        }
        else if (SAI_PORT_FEC_MODE_FC == attr->value.s32)
        {
            enable = 1;
            value = CTC_PORT_FEC_TYPE_BASER;
        }
        else if (SAI_PORT_FEC_MODE_RS == attr->value.s32)
        {
            enable = 1;
            value = CTC_PORT_FEC_TYPE_RS;
        }

        if (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
        {
            if (value == CTC_PORT_FEC_TYPE_RS)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_FEC_EN, enable));
        }
        else
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_AUTO_NEG_FEC, value));
        }
        break;

    case SAI_PORT_ATTR_MTU:
        CTC_SAI_CTC_ERROR_RETURN(_ctc_sai_port_unset_max_frame(lchip, gport));
        CTC_SAI_CTC_ERROR_RETURN(_ctc_sai_port_set_max_frame(lchip, gport, attr->value.u32));
        break;

    case SAI_PORT_ATTR_EEE_ENABLE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_EEE_EN, (uint32)attr->value.booldata));
        break;
    case SAI_PORT_ATTR_UPDATE_DSCP:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_REPLACE_DSCP_EN, (uint32)attr->value.booldata));
        #if 0
        {
            if (CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip) || CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
            {
                //D2 and TM need to set l3if
                uint32 rif_value = 0;
                ctc_sai_rif_traverse_param_t rif_param;
                sal_memset(&rif_param, 0, sizeof(ctc_sai_rif_traverse_param_t));
                rif_param.set_type = CTC_SAI_RIF_SET_TYPE_PORT;
                rif_param.cmp_value = &gport;
                rif_param.lchip = lchip;
                rif_param.l3if_prop = CTC_L3IF_PROP_DSCP_SELECT_MODE;
                rif_value = attr->value.booldata ? CTC_DSCP_SELECT_MAP : CTC_DSCP_SELECT_NONE;
                rif_param.p_value = &rif_value;
                CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_traverse_set(&rif_param));
            }
        }
        #endif
        break;
    case SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_port_set_scheduler(key->key.object_id, attr));
        }
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE:
        {
            if(SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == attr->value.s32)
            {
                p_port_db->flow_ctl_mode = SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED;
            }
            if(SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE == attr->value.s32)
            {
                p_port_db->flow_ctl_mode = SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE;
            }
        }
        break;
    case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_BOTH_DIRECTION;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                if (attr->value.u8 & (1 << loop))
                {
                    fc_prop.enable = 1;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
            }
        }
        break;
        case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_INGRESS;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                if (attr->value.u8 & (1 << loop))
                {
                    fc_prop.enable = 1;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
            }
        }
        break;
        case SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX:
        {
            ctc_port_fc_prop_t fc_prop;
            sal_memset(&fc_prop, 0 ,sizeof(fc_prop));
            fc_prop.dir = CTC_EGRESS;
            fc_prop.is_pfc = 1;
            fc_prop.gport = gport;
            if (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == p_port_db->flow_ctl_mode)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            for (loop = 0; loop < 8; loop++)
            {
                fc_prop.enable = 0;
                fc_prop.priority_class = loop;
                if (attr->value.u8 & (1 << loop))
                {
                    fc_prop.enable = 1;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
            }
        }
        break;
    case SAI_PORT_ATTR_META_DATA:
        if (CTC_CHIP_TSINGMA == chip_type)
        {
            ingress_acl_num = 8;
            egress_acl_num = 3;
        }
        else if (CTC_CHIP_TSINGMA_MX == chip_type)
        {
            ingress_acl_num = 16;
            egress_acl_num = 4;
        }

        for (i = 0; i < ingress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_INGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, gport, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, gport, &acl_prop));
        }

        for (i = 0; i < egress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, gport, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, gport, &acl_prop));
        }
        break;
    case SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST:
        sal_memset(&port_isolation, 0, sizeof(port_isolation));
        port_isolation.gport = gport;
        port_isolation.isolation_pkt_type = CTC_PORT_ISOLATION_ALL;
        for (index=0; index<attr->value.objlist.count; index++)
        {
            port_oid = attr->value.objlist.list[index];
            CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(port_oid, &gport_temp));
            lport = CTC_MAP_GPORT_TO_LPORT(gport_temp);
            index_tmp1 = lport/CTC_UINT32_BITS;
            index_tmp2 = lport%CTC_UINT32_BITS;
            CTC_BIT_SET(port_isolation.pbm[index_tmp1], index_tmp2);
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_isolation(lchip, &port_isolation));
        break;
    case SAI_PORT_ATTR_ISOLATION_GROUP:
        {
            ctc_port_restriction_t port_restriction;
            ctc_sai_isolation_group_t* p_ist_grp = NULL;
            ctc_object_id_t ctc_object_id;
            sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
            sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t));

            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                port_restriction.isolated_id = 0; /* SAI_NULL_OBJECT_ID mean disable*/
            }
            else
            {
                p_ist_grp = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if (NULL == p_ist_grp)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr->value.oid, &ctc_object_id);
                port_restriction.isolated_id = ctc_object_id.value;
            }
            port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
            port_restriction.type = CTC_PORT_ISOLATION_ALL;
            port_restriction.dir = CTC_INGRESS;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_restriction(lchip, gport, &port_restriction));
        }
        break;
    case SAI_PORT_ATTR_PKT_TX_ENABLE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_TRANSMIT_EN, attr->value.booldata?1:0));
        break;
    case SAI_PORT_ATTR_ES:
        ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
        if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
        {
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
        }
        if( p_port_db->ethernet_segment != attr->value.oid)
        {
            p_es = ctc_sai_db_get_object_property(lchip, attr->value.oid);
            p_es_old = ctc_sai_db_get_object_property(lchip, p_port_db->ethernet_segment);
            if(NULL != p_es)
            {
                /* need set es on port on tm1.1 and tm2 */
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ESID, (uint32)p_es->local_es_id));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ESLB, (uint32)p_es->esi_label));
                /* need add port-label mapping on tm1.1 and tm2 */


                if(SAI_NULL_OBJECT_ID != p_port_db->ethernet_segment)
                {
                    //old es ref_cnt--
                    p_es_old->ref_cnt--;
                }
                p_port_db->ethernet_segment = attr->value.oid;
                //es ref_cnt++
                p_es->ref_cnt++;
            }
            else if(SAI_NULL_OBJECT_ID == attr->value.oid && SAI_NULL_OBJECT_ID != p_port_db->ethernet_segment)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ESID, 0));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ESLB, 0));
                //old es ref_cnt--
                p_es_old->ref_cnt--;
                p_port_db->ethernet_segment = SAI_NULL_OBJECT_ID;
            }
            else
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
        }
        break;
    case SAI_PORT_ATTR_Y1731_ENABLE:
        sal_memset(&oam_prop, 0, sizeof(ctc_oam_property_t));
        p_eth_prop  = &oam_prop.u.y1731;
        oam_prop.oam_pro_type = CTC_OAM_PROPERTY_TYPE_Y1731;
        p_eth_prop->cfg_type = CTC_OAM_Y1731_CFG_TYPE_PORT_OAM_EN;
        p_eth_prop->gport  = gport;
        p_eth_prop->dir    = CTC_BOTH_DIRECTION;
        p_eth_prop->value = attr->value.booldata;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_oam_set_property(lchip, &oam_prop));
        p_port_db->y1731_oam_en = attr->value.booldata;
        break;
    case SAI_PORT_ATTR_Y1731_LM_ENABLE:
        sal_memset(&oam_prop, 0, sizeof(ctc_oam_property_t));
        p_eth_prop  = &oam_prop.u.y1731;
        oam_prop.oam_pro_type = CTC_OAM_PROPERTY_TYPE_Y1731;
        p_eth_prop->cfg_type = CTC_OAM_Y1731_CFG_TYPE_PORT_LM_EN;
        p_eth_prop->gport  = gport;
        p_eth_prop->value = attr->value.booldata;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_oam_set_property(lchip, &oam_prop));
        p_port_db->y1731_lm_en = attr->value.booldata;
        break;
    case SAI_PORT_ATTR_Y1731_MIP_ENABLE:
        if((CTC_CHIP_TSINGMA == chip_type) || (CTC_CHIP_DUET2 == chip_type))
        {
            sal_memset(&oam_prop, 0, sizeof(ctc_oam_property_t));
            p_eth_prop  = &oam_prop.u.y1731;
            oam_prop.oam_pro_type = CTC_OAM_PROPERTY_TYPE_Y1731;
            p_eth_prop->cfg_type = CTC_OAM_Y1731_CFG_TYPE_CFM_PORT_MIP_EN;
            p_eth_prop->gport  = gport;
            p_eth_prop->value = attr->value.u8;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_oam_set_property(lchip, &oam_prop));
            p_port_db->y1731_mip_bitmap = attr->value.u8;
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        break;
    case SAI_PORT_ATTR_MAC_ADDRESS:
        sal_memset(&post_mac, 0, sizeof(post_mac));
        CTC_SET_FLAG(post_mac.prefix_type, CTC_PORT_MAC_PREFIX_48BIT);
        sal_memcpy(&post_mac.port_mac, &attr->value.mac, sizeof(sai_mac_t));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_port_mac_postfix(lchip, gport, &post_mac));
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "port attribute not implement\n");
        return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;

    }
    return SAI_STATUS_SUCCESS;
}





static sai_status_t ctc_sai_port_get_drop_tags(  sai_object_key_t      *key,   sai_attribute_t *attr, uint32 attr_idx)
{
    uint32_t       gport = 0;
    uint8_t lchip = 0;
    uint32_t val_32 = 0;


    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_vlan_ctl(lchip, gport, (ctc_vlantag_ctl_t*)&val_32));
    switch (attr->id)
    {
        case SAI_PORT_ATTR_DROP_UNTAGGED:
            if (CTC_VLANCTL_DROP_ALL_UNTAGGED == val_32 || CTC_VLANCTL_DROP_ALL == val_32 )
            {
                attr->value.booldata = TRUE;
            }
            else
            {
                attr->value.booldata = FALSE;
            }
            break;

        case SAI_PORT_ATTR_DROP_TAGGED:
            if (CTC_VLANCTL_DROP_ALL_TAGGED == val_32 || CTC_VLANCTL_DROP_ALL == val_32 )
            {
                attr->value.booldata = TRUE;
            }
            else
            {
                attr->value.booldata = FALSE;
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_PORT, "error:Unexpected attribute id:%u", attr->id);
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_port_mapping_tags_mode(ctc_sai_port_drop_type_t drop_type, bool data, ctc_vlantag_ctl_t* mode, ctc_vlantag_ctl_t  mode_old )
{
   switch (drop_type)
    {
    case CTC_SAI_PORT_DROP_UNTAGGED:
        if (data)
        {
            if (CTC_VLANCTL_DROP_ALL_UNTAGGED == mode_old || CTC_VLANCTL_DROP_ALL == mode_old )
            {
                return ;
            }
            else if (CTC_VLANCTL_DROP_ALL_TAGGED == mode_old)
            {
                *mode = CTC_VLANCTL_DROP_ALL;
            }
            else
            {
                *mode = CTC_VLANCTL_DROP_ALL_UNTAGGED;
            }
        }
        else
        {
             if (CTC_VLANCTL_DROP_ALL_UNTAGGED == mode_old  )
            {
                *mode = CTC_VLANCTL_ALLOW_ALL_PACKETS ;
            }
            else if (CTC_VLANCTL_DROP_ALL_TAGGED == mode_old || CTC_VLANCTL_ALLOW_ALL_PACKETS == mode_old)
            {
                return ;
            }
            else
            {
                *mode = CTC_VLANCTL_DROP_ALL_TAGGED;
            }
        }
        break;

    case CTC_SAI_PORT_DROP_TAGGED:
        if (data)
        {
            if (CTC_VLANCTL_DROP_ALL_TAGGED == mode_old || CTC_VLANCTL_DROP_ALL == mode_old )
            {
                return ;
            }
            else if (CTC_VLANCTL_DROP_ALL_UNTAGGED == mode_old)
            {
                *mode = CTC_VLANCTL_DROP_ALL;
            }
            else
            {
                *mode = CTC_VLANCTL_DROP_ALL_TAGGED;
            }
        }
        else
        {
             if (CTC_VLANCTL_DROP_ALL_TAGGED == mode_old  )
            {
                *mode = CTC_VLANCTL_ALLOW_ALL_PACKETS ;
            }
            else if (CTC_VLANCTL_DROP_ALL_UNTAGGED == mode_old || CTC_VLANCTL_ALLOW_ALL_PACKETS == mode_old)
            {
                return ;
            }
            else
            {
                *mode = CTC_VLANCTL_DROP_ALL_UNTAGGED;
            }
        }
        break;
        default :
            return;

    }

}

static sai_status_t ctc_sai_port_set_drop_tags(  sai_object_key_t      *key, const  sai_attribute_t *attr)
{
    uint32      gport = 0;
    uint8 lchip = 0;
    ctc_vlantag_ctl_t mode = 0;
    uint32 val_32 = 0;

    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_vlan_ctl(lchip, gport, (ctc_vlantag_ctl_t*)&val_32));

    switch (attr->id)
    {
    case SAI_PORT_ATTR_DROP_UNTAGGED:
        ctc_sai_port_mapping_tags_mode(CTC_SAI_PORT_DROP_UNTAGGED, attr->value.booldata, &mode, val_32 );
        break;

    case SAI_PORT_ATTR_DROP_TAGGED:
        ctc_sai_port_mapping_tags_mode(CTC_SAI_PORT_DROP_TAGGED, attr->value.booldata, &mode, val_32 );
        break;

    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_vlan_ctl(lchip, gport, mode));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_set_policer(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    uint32 gport = 0;
    uint8  lchip = 0;
    sai_object_id_t policer_id;
    ctc_object_id_t ctc_object_id;
    ctc_sai_port_db_t* p_port_db = NULL;
    bool enable = FALSE;
    bool need_revert = TRUE;
    uint32 old_policer_id = 0;
    uint8 is_strom_ctl = 1;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));
    policer_id = attr->value.oid;
    if (SAI_NULL_OBJECT_ID != policer_id)
    {
        enable = TRUE;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, policer_id, &ctc_object_id);
    switch (attr->id)
    {
        case SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID://need to set unknown uc & unknown mc
            CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip, gport,
                                            enable ? ctc_object_id.value : p_port_db->stmctl_flood_policer_id,
                                            CTC_SAI_STMCTL_TYPE_FLOOD, enable));
            old_policer_id = p_port_db->stmctl_flood_policer_id;
            p_port_db->stmctl_flood_policer_id = ctc_object_id.value;
            if ((old_policer_id == p_port_db->stmctl_bc_policer_id)
                || (old_policer_id == p_port_db->stmctl_mc_policer_id))
            {
                need_revert = FALSE;
            }
            break;
        case SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip, gport,
                                            enable ? ctc_object_id.value : p_port_db->stmctl_bc_policer_id,
                                            CTC_SAI_STMCTL_TYPE_BCAST, enable));
            old_policer_id = p_port_db->stmctl_bc_policer_id;
            p_port_db->stmctl_bc_policer_id = ctc_object_id.value;
            if ((old_policer_id == p_port_db->stmctl_flood_policer_id)
                || (old_policer_id == p_port_db->stmctl_mc_policer_id))
            {
                need_revert = FALSE;
            }
            break;
        case SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_stmctl(lchip, gport,
                                            enable ? ctc_object_id.value : p_port_db->stmctl_mc_policer_id,
                                            CTC_SAI_STMCTL_TYPE_MCAST, enable));
            old_policer_id = p_port_db->stmctl_mc_policer_id;
            p_port_db->stmctl_mc_policer_id = ctc_object_id.value;
            if ((old_policer_id == p_port_db->stmctl_flood_policer_id)
                || (old_policer_id == p_port_db->stmctl_bc_policer_id))
            {
                need_revert = FALSE;
            }
            break;
        case SAI_PORT_ATTR_POLICER_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_policer_port_set_policer(lchip, gport,
                                                        enable ? ctc_object_id.value : p_port_db->policer_id,
                                                        enable));
            old_policer_id = p_port_db->policer_id;
            p_port_db->policer_id = ctc_object_id.value;
            need_revert = TRUE;
            is_strom_ctl = 0;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }

    if (old_policer_id && (old_policer_id != ctc_object_id.value) && need_revert)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_policer_revert_policer(lchip, old_policer_id, gport, is_strom_ctl));
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_port_set_ptp(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    uint32 gport = 0;
    uint8  lchip = 0;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_sai_ptp_db_t* p_ptp_db = NULL;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));

    switch (attr->id)
    {
        case SAI_PORT_ATTR_PTP_MODE:
            p_port_db->ptp_mode = attr->value.s32;
            break;

        case SAI_PORT_ATTR_PTP_DOMAIN_ID://domain id cannot be 0, and only support create one domain
            if(SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_PTP_EN, FALSE));
                p_port_db->ptp_domain_id= 0;
            }
            else
            {
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, attr->value.oid, &ctc_object_id);
                p_ptp_db = ctc_sai_db_get_object_property(lchip,  attr->value.oid);
                if ((NULL == p_ptp_db)||(SAI_OBJECT_TYPE_PTP_DOMAIN != ctc_object_id.type))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "ptp domain not found \n");
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_PTP_EN, TRUE));
                p_port_db->ptp_domain_id= ctc_object_id.value;
            }
            break;

        case SAI_PORT_ATTR_PTP_PATH_DELAY:
            p_port_db->ptp_path_delay= attr->value.u64;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_ptp_set_adjust_delay(lchip, gport, CTC_PTP_ADJUST_DELAY_PATH_DELAY, attr->value.u64));
            break;

        case SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY:
            p_port_db->ptp_egr_asy= attr->value.u64;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_ptp_set_adjust_delay(lchip, gport, CTC_PTP_ADJUST_DELAY_EGRESS_ASYMMETRY, attr->value.u64));
            break;

        case SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY:
            p_port_db->ptp_ingr_asy= attr->value.u64;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_ptp_set_adjust_delay(lchip, gport, CTC_PTP_ADJUST_DELAY_INGRESS_ASYMMETRY, attr->value.u64));
            break;
    }

    return SAI_STATUS_SUCCESS;

}


static sai_status_t
_ctc_sai_port_get_ptp(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint32 gport = 0;
    uint8  lchip = 0;
    uint32 ctc_ptp_domain_id = 0;
    ctc_sai_port_db_t* p_port_db = NULL;


    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    attr->value.oid = SAI_NULL_OBJECT_ID;
    p_port_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);

    if (NULL == p_port_db)
    {
        return SAI_STATUS_SUCCESS;
    }

    switch (attr->id)
    {
        case SAI_PORT_ATTR_PTP_MODE:
            attr->value.s32 = p_port_db->ptp_mode;
            break;

        case SAI_PORT_ATTR_PTP_DOMAIN_ID://domain id cannot be 0
            ctc_ptp_domain_id = p_port_db->ptp_domain_id;
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, lchip, 0, 0, ctc_ptp_domain_id);
            break;

        case SAI_PORT_ATTR_PTP_PATH_DELAY:
            attr->value.u64 = p_port_db->ptp_path_delay;
            break;

        case SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY:
            attr->value.u64 = p_port_db->ptp_egr_asy;
            break;

        case SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY:
            attr->value.u64 = p_port_db->ptp_ingr_asy;
            break;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_port_set_mirror(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    uint32 gport = 0;
    uint8  lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_ERROR_RETURN(ctc_sai_mirror_set_port_mirr(lchip, gport, attr));
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_port_get_mirror(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint32 gport = 0;
    uint8  lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_ERROR_RETURN(ctc_sai_mirror_get_port_mirr(lchip, gport, attr));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_get_policer(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint32 gport = 0;
    uint8  lchip = 0;
    ctc_sai_port_db_t* p_port_db = NULL;
    uint32 ctc_policer_id = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    attr->value.oid= SAI_NULL_OBJECT_ID;
    p_port_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_port_db)
    {
	    /* SAI merge 20200824 */
        return SAI_STATUS_SUCCESS;
    }

    switch (attr->id)
    {
        case SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
            ctc_policer_id = p_port_db->stmctl_flood_policer_id;
            break;
        case SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
            ctc_policer_id = p_port_db->stmctl_bc_policer_id;
            break;
        case SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
            ctc_policer_id = p_port_db->stmctl_mc_policer_id;
            break;
        case SAI_PORT_ATTR_POLICER_ID:
            ctc_policer_id = p_port_db->policer_id;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    if (ctc_policer_id)
    {
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, ctc_policer_id);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_set_qos_map(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    uint8  lchip = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_port_db_t* p_port_db = NULL;
    bool enable = FALSE;
    uint8 chip_type = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));
    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        enable = TRUE;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, attr->value.oid, &ctc_oid);
    chip_type = ctcs_get_chip_type(lchip);
    switch (attr->id)
    {
        case SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->dot1p_to_tc_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->dot1p_to_tc_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[DOT1P_TO_TC_MAP] Already exsit! map_id:%d", p_port_db->dot1p_to_tc_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && (p_port_db->dscp_to_tc_map_id || p_port_db->dscp_to_color_map_id))
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->dot1p_to_tc_map_id,
                                                SAI_QOS_MAP_TYPE_DOT1P_TO_TC, enable));
            p_port_db->dot1p_to_tc_map_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->dot1p_to_color_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->dot1p_to_color_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[DOT1P_TO_COLOR_MAP] Already exsit! map_id:%d", p_port_db->dot1p_to_color_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && (p_port_db->dscp_to_tc_map_id || p_port_db->dscp_to_color_map_id))
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->dot1p_to_color_map_id,
                                                SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, enable));
            p_port_db->dot1p_to_color_map_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->dscp_to_tc_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->dscp_to_tc_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[DSCP_TO_TC_MAP] Already exsit! map_id:%d", p_port_db->dscp_to_tc_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && (p_port_db->dot1p_to_tc_map_id || p_port_db->dot1p_to_color_map_id))
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->dscp_to_tc_map_id,
                                                SAI_QOS_MAP_TYPE_DSCP_TO_TC, enable));
            p_port_db->dscp_to_tc_map_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->dscp_to_color_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->dscp_to_color_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[DSCP_TO_COLOR_MAP] Already exsit! map_id:%d", p_port_db->dscp_to_color_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && (p_port_db->dot1p_to_tc_map_id || p_port_db->dot1p_to_color_map_id))
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->dscp_to_color_map_id,
                                                SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, enable));
            p_port_db->dscp_to_color_map_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->tc_color_to_dot1p_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->tc_color_to_dot1p_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[TC_AND_COLOR_TO_DOT1P_MAP] Already exsit! map_id:%d", p_port_db->tc_color_to_dot1p_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && p_port_db->tc_color_to_dscp_map_id)
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->tc_color_to_dot1p_map_id,
                                                SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, enable));
            p_port_db->tc_color_to_dot1p_map_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
            if (enable)
            {
                if (ctc_oid.value == p_port_db->tc_color_to_dscp_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_port_db->tc_color_to_dscp_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_PORT,"[TC_AND_COLOR_TO_DSCP_MAP] Already exsit! map_id:%d", p_port_db->tc_color_to_dscp_map_id);
                    return SAI_STATUS_FAILURE;
                }
                if ((chip_type == CTC_CHIP_GOLDENGATE) && p_port_db->tc_color_to_dot1p_map_id)
                {
                    //GG not support revert qos domain
                    CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP!\n");
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                                enable ? ctc_oid.value : p_port_db->tc_color_to_dscp_map_id,
                                                SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, enable));
            p_port_db->tc_color_to_dscp_map_id = enable ? ctc_oid.value : 0;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }
    return SAI_STATUS_SUCCESS;
}
static sai_status_t
_ctc_sai_port_get_qos_map(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint8  lchip = 0;
    uint32 value = 0;
    ctc_sai_port_db_t* p_port_db = NULL;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    attr->value.oid = SAI_NULL_OBJECT_ID;
    p_port_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_port_db)
    {
	    /* SAI merge 20200824 */
        return SAI_STATUS_SUCCESS;
    }

    switch (attr->id)
    {
        case SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
            value = p_port_db->dot1p_to_tc_map_id;
            break;
        case SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
            value = p_port_db->dot1p_to_color_map_id;
            break;
        case SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
            value = p_port_db->dscp_to_tc_map_id;
            break;
        case SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
            value = p_port_db->dscp_to_color_map_id;
            break;
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
            value = p_port_db->tc_color_to_dot1p_map_id;
            break;
        case SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
            value = p_port_db->tc_color_to_dscp_map_id;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    if (value)
    {
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, value);
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_set_samplepacket(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    uint32 gport = 0;
    uint8  lchip = 0;
    ctc_sai_port_db_t* p_port_db = NULL;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(key->key.object_id, &p_port_db));
    CTC_SAI_ERROR_RETURN(ctc_sai_samplepacket_set_port_samplepacket(lchip, gport, attr, (void*)p_port_db));
    if (SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE == attr->id)
    {
        p_port_db->ingress_samplepacket_id = attr->value.oid;
    }
    else
    {
        p_port_db->egress_samplepacket_id = attr->value.oid;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_port_get_samplepacket(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    uint8  lchip = 0;
    ctc_sai_port_db_t* p_port_db = NULL;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:0x%x\n", attr->id, attr->value.oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    attr->value.oid = SAI_NULL_OBJECT_ID;
    p_port_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_port_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE:
            attr->value.oid = p_port_db->ingress_samplepacket_id;
            break;
        case SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE:
            attr->value.oid = p_port_db->egress_samplepacket_id;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_set_global_flow_ctl(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    ctc_port_fc_prop_t  fc_prop;
    uint32 gport = 0;
    uint8  lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:%u\n", attr->id, attr->value.s32);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    sal_memset(&fc_prop,0,sizeof(ctc_port_fc_prop_t));

    fc_prop.gport = gport;
    switch(attr->value.s32)
    {
    case SAI_PORT_FLOW_CONTROL_MODE_DISABLE:
        fc_prop.dir = CTC_BOTH_DIRECTION;
        fc_prop.enable= FALSE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        break;
    case SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY:
        fc_prop.dir = CTC_EGRESS;
        fc_prop.enable = TRUE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        fc_prop.dir = CTC_INGRESS;
        fc_prop.enable = FALSE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        break;
    case SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY:
        fc_prop.dir = CTC_EGRESS;
        fc_prop.enable = FALSE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        fc_prop.dir = CTC_INGRESS;
        fc_prop.enable = TRUE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        break;
    case SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE:
        fc_prop.dir = CTC_BOTH_DIRECTION;
        fc_prop.enable= TRUE;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_flow_ctl_en(lchip, &fc_prop));
        break;
    default:
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_port_get_global_flow_ctl(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    ctc_port_fc_prop_t  fc_prop;
    uint32 gport = 0;
    uint8  lchip = 0;
    uint8  igs_en = 0;
    uint8  egs_en = 0;

    CTC_SAI_PTR_VALID_CHECK(key);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_LOG_INFO(SAI_API_PORT, "[PARA] attribute id:%u, value:%u\n", attr->id, attr->value.s32);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(key->key.object_id, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    sal_memset(&fc_prop,0,sizeof(ctc_port_fc_prop_t));

    fc_prop.gport = gport;
    //ingress
    fc_prop.dir = CTC_INGRESS;
    CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_prop), attr_idx);
    igs_en = fc_prop.enable;
    //egress
    fc_prop.dir = CTC_EGRESS;
    CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_get_flow_ctl_en(lchip, &fc_prop), attr_idx);
    egs_en = fc_prop.enable;

    if (igs_en && egs_en)
    {
        attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE;
    }
    else if (igs_en)
    {
        attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY;
    }
    else if (egs_en)
    {
        attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY;
    }
    else
    {
        attr->value.s32 = SAI_PORT_FLOW_CONTROL_MODE_DISABLE;
    }
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t  port_attr_fn_entries[] =
{
    {SAI_PORT_ATTR_TYPE,                                           ctc_sai_port_get_type,  NULL},
    {SAI_PORT_ATTR_OPER_STATUS,                                    ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE,                   ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE,                     ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES,                           ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_QOS_QUEUE_LIST,                                 ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS,                 ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST,                       ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_SPEED,                                ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_FEC_MODE,                             ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED,                    ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE,                        ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE,                    ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE,                ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE,                           ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED,                        NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE,                     NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED,            NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE,                NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE,            NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE,        NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE,                   NULL,  NULL},
    {SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE,                     NULL,  NULL},
    {SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS,              ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST,                    ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_EYE_VALUES,                                     NULL,  NULL},
    {SAI_PORT_ATTR_OPER_SPEED,                                     ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_HW_LANE_LIST,                                   ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_SPEED,                                          ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_FULL_DUPLEX_MODE,                               ctc_sai_port_get_basic_info,  NULL},
    {SAI_PORT_ATTR_AUTO_NEG_MODE,                                  ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_ADMIN_STATE,                                    ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_MEDIA_TYPE ,                                    NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_SPEED,                               NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_FEC_MODE,                            NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED,                   NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE,                       NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE,                   NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE,               NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE,                          NULL,  NULL},
    {SAI_PORT_ATTR_ADVERTISED_OUI_CODE,                            NULL,  NULL},
    {SAI_PORT_ATTR_PORT_VLAN_ID,                                   ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY,                          ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_DROP_UNTAGGED,                                  ctc_sai_port_get_drop_tags,  ctc_sai_port_set_drop_tags},
    {SAI_PORT_ATTR_DROP_TAGGED,                                    ctc_sai_port_get_drop_tags,  ctc_sai_port_set_drop_tags},
    {SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE,                         ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_FEC_MODE,                                       ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_UPDATE_DSCP,                                    ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_MTU,                                            ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID,                 _ctc_sai_port_get_policer,  _ctc_sai_port_set_policer},
    {SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID,             _ctc_sai_port_get_policer,  _ctc_sai_port_set_policer},
    {SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID,             _ctc_sai_port_get_policer,  _ctc_sai_port_set_policer},
    {SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE,                       _ctc_sai_port_get_global_flow_ctl,  _ctc_sai_port_set_global_flow_ctl},
    {SAI_PORT_ATTR_INGRESS_ACL,                                    ctc_sai_port_get_basic_info,  ctc_sai_acl_bind_point_set},
    {SAI_PORT_ATTR_EGRESS_ACL,                                     ctc_sai_port_get_basic_info,  ctc_sai_acl_bind_point_set},
    {SAI_PORT_ATTR_INGRESS_MIRROR_SESSION,                         _ctc_sai_port_get_mirror,  _ctc_sai_port_set_mirror},
    {SAI_PORT_ATTR_EGRESS_MIRROR_SESSION,                          _ctc_sai_port_get_mirror,  _ctc_sai_port_set_mirror},
    {SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE,                    _ctc_sai_port_get_samplepacket, _ctc_sai_port_set_samplepacket},
    {SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE,                     _ctc_sai_port_get_samplepacket, _ctc_sai_port_set_samplepacket},
    {SAI_PORT_ATTR_POLICER_ID,                                     _ctc_sai_port_get_policer,  _ctc_sai_port_set_policer},
    {SAI_PORT_ATTR_QOS_DEFAULT_TC,                                 NULL,  NULL},
    {SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP,                            _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP,                         _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP,                             _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP,                          _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP,                            NULL,  NULL},
    {SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP,                  _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP,                   _ctc_sai_port_get_qos_map,  _ctc_sai_port_set_qos_map},
    {SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP,                   NULL,  NULL},
    {SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP,         NULL,  NULL},
    {SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP,                  NULL,  NULL},
    {SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID,                       ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST,                NULL,  NULL},
    {SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST,                 NULL,  NULL},
    {SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE,                     ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL,                          ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX,                       ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX,                       ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_META_DATA,                                      ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST,                         ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_HW_PROFILE_ID,                                  NULL,  NULL},
    {SAI_PORT_ATTR_EEE_ENABLE,                                     ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_EEE_IDLE_TIME,                                  NULL,  NULL},
    {SAI_PORT_ATTR_EEE_WAKE_TIME,                                  NULL,  NULL},
    {SAI_PORT_ATTR_PORT_POOL_LIST,                                 NULL,  NULL},
    {SAI_PORT_ATTR_ISOLATION_GROUP,                                ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PKT_TX_ENABLE,                                  ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_TAM_OBJECT,                                     NULL,  NULL},
    {SAI_PORT_ATTR_SERDES_PREEMPHASIS,                             NULL,  NULL},
    {SAI_PORT_ATTR_SERDES_IDRIVER,                                 NULL,  NULL},
    {SAI_PORT_ATTR_SERDES_IPREDRIVER,                              NULL,  NULL},
    {SAI_PORT_ATTR_LINK_TRAINING_ENABLE,                           NULL,  NULL},
    {SAI_PORT_ATTR_PORT_SERDES_ID,                                 NULL,  NULL},
    {SAI_PORT_ATTR_ES,                                             ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PTP_MODE,                                       _ctc_sai_port_get_ptp,  _ctc_sai_port_set_ptp},
    {SAI_PORT_ATTR_Y1731_ENABLE,                                   ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_Y1731_LM_ENABLE,                                ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_Y1731_MIP_ENABLE,                               ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY,                    _ctc_sai_port_get_ptp,  _ctc_sai_port_set_ptp},
    {SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY,                     _ctc_sai_port_get_ptp,  _ctc_sai_port_set_ptp},
    {SAI_PORT_ATTR_PTP_PATH_DELAY,                                 _ctc_sai_port_get_ptp,  _ctc_sai_port_set_ptp},
    {SAI_PORT_ATTR_PTP_DOMAIN_ID,                                  _ctc_sai_port_get_ptp,  _ctc_sai_port_set_ptp},
    {SAI_PORT_ATTR_MAC_ADDRESS,                                    ctc_sai_port_get_basic_info,  ctc_sai_port_set_basic_info},
    {CTC_SAI_FUNC_ATTR_END_ID,                                     NULL,NULL}
};

static sai_status_t
ctc_sai_port_key_to_str( sai_object_id_t port_id,  char *key_str)
{
    char        *type_str = "port";
    uint32     gport;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(port_id, &gport));

    if (sai_object_type_query(port_id) == SAI_OBJECT_TYPE_LAG) {
        type_str = "lag";
    }

    snprintf(key_str, MAX_KEY_STR_LEN, "%s 0x%x", type_str, gport);

     return SAI_STATUS_SUCCESS;
}

#define ________WARMBOOT________

static sai_status_t
_ctc_sai_port_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t port_oid = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_port_db_t* p_port_db = (ctc_sai_port_db_t*)data;
    ctc_sai_port_wb_t port_wb;
    ctc_slistnode_t *service_node = NULL;
    ctc_sai_port_service_id_t *p_service_node = NULL;
    uint32 offset = 0;

    sal_memset(&port_wb, 0, sizeof(ctc_sai_port_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_port_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_PORT);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_port_db->service_id_list, service_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_service_node = (ctc_sai_port_service_id_t*)service_node;
        port_wb.port_oid = port_oid;
        port_wb.service_id = p_service_node->service_id;

        sal_memcpy((uint8*)wb_data.buffer + offset, &port_wb, (wb_data.key_len + wb_data.data_len));

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
_ctc_sai_port_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_port_db_t *p_port_db = (ctc_sai_port_db_t *)data;

    p_port_db->service_id_list = ctc_slist_new();
    if (!p_port_db->service_id_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return status;
}


static sai_status_t
_ctc_sai_port_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_sai_port_wb_t port_wb;
    ctc_sai_port_service_id_t *p_service_node = NULL;

    sal_memset(&port_wb, 0, sizeof(ctc_sai_port_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_port_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_PORT);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&port_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_port_wb_t));
        p_port_db = ctc_sai_db_get_object_property(lchip, port_wb.port_oid);
        if (!p_port_db)
        {
            continue;
        }

        p_service_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_port_service_id_t));
        if (!p_service_node)
        {
            continue;
        }
        p_service_node->service_id = port_wb.service_id;

        ctc_slist_add_tail(p_port_db->service_id_list, &(p_service_node->node));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
 }


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_port_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  port_oid_cur = 0;
    ctc_sai_port_db_t    ctc_port_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;

    sal_memset(&ctc_port_cur, 0, sizeof(ctc_port_cur));

    port_oid_cur = bucket_data->oid;
    //ctc_sai_oid_get_sub_type(hash_oid_cur, &hash_type);
    sal_memcpy((ctc_sai_port_db_t*)(&ctc_port_cur), bucket_data->data, sizeof(ctc_sai_port_db_t));

    p_file = (sal_file_t)p_cb_data->value0;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (port_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    CTC_SAI_LOG_DUMP(p_file, "%-26s:0x%016"PRIx64"\n", "Port_oid", port_oid_cur);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "policer_id                :0x%08x     stmctl_flood_policer_id  :0x%08x     stmctl_bc_policer_id  :0x%08x\n",
        ctc_port_cur.policer_id, ctc_port_cur.stmctl_flood_policer_id, ctc_port_cur.stmctl_bc_policer_id);
    CTC_SAI_LOG_DUMP(p_file, "stmctl_mc_policer_id      :0x%08x     dot1p_to_tc_map_id       :0x%08x     dot1p_to_color_map_id :0x%08x\n",
        ctc_port_cur.stmctl_mc_policer_id, ctc_port_cur.dot1p_to_tc_map_id, ctc_port_cur.dot1p_to_color_map_id);
    CTC_SAI_LOG_DUMP(p_file, "tc_color_to_dot1p_map_id  :0x%08x     dscp_to_tc_map_id        :0x%08x     dscp_to_color_map_id  :0x%08x\n",
        ctc_port_cur.tc_color_to_dot1p_map_id, ctc_port_cur.dscp_to_tc_map_id, ctc_port_cur.dscp_to_color_map_id);
    CTC_SAI_LOG_DUMP(p_file, "tc_color_to_dscp_map_id   :0x%08x     sched_id                 :0x%08x\n",
        ctc_port_cur.tc_color_to_dscp_map_id, ctc_port_cur.sched_id);
    CTC_SAI_LOG_DUMP(p_file, "ingress_samplepacket_id   :0x%016"PRIx64"                      egress_samplepacket_id   :0x%016"PRIx64"\n",
        ctc_port_cur.ingress_samplepacket_id, ctc_port_cur.egress_samplepacket_id);
    CTC_SAI_LOG_DUMP(p_file, "sched_id                :0x%08x\n",     ctc_port_cur.sched_id);
    CTC_SAI_LOG_DUMP(p_file, "flow_ctl_mode  :0x%08x\n",    ctc_port_cur.flow_ctl_mode);
    CTC_SAI_LOG_DUMP(p_file, "ethernet_segment  :0x%016"PRIx64"\n", ctc_port_cur.ethernet_segment);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");


    return SAI_STATUS_SUCCESS;
}
void ctc_sai_port_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, "\n");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Port MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_PORT))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Port");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_port_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_PORT,
                                            (hash_traversal_fn)_ctc_sai_port_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________

static sai_status_t
ctc_sai_port_create_port( sai_object_id_t     * port_id,
                         sai_object_id_t        switch_id,
                         uint32_t               attr_count,
                         const sai_attribute_t *attr_list)
{
    ctc_global_panel_ports_t local_panel_ports ;
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *lanes_list        = NULL;
    const sai_attribute_value_t *port_speed        = NULL;
    uint32 speed_index = 0;
    uint32 lane_index = 0;
    uint32 lanes_count = 0;
    uint32 num = 0;
	/*SYSTEM MODIFIED by jqiu, bug http://10.10.25.13/show_bug.cgi?id=51934, start*/
    uint32 mac_id = 0;
    //ctc_port_serdes_info_t serdes_port ;
	/*SYSTEM MODIFIED by jqiu, bug http://10.10.25.13/show_bug.cgi?id=51934, end*/
    ctc_port_speed_t speed_mode = 0;
    const sai_attribute_value_t *attr_value = NULL;
    uint32                   attr_index = 0;
    uint8 i = 0;
    uint8 gchip = 0;
    uint8 lchip = 0;
    uint8 ingress_acl_num = 0;
    uint8 egress_acl_num = 0;
    ctc_sai_port_db_t* p_port_db = NULL;
    uint32 mtu_size = 0;
    uint32 gport = 0;
    uint8 chip_type = 0;
    ctc_sai_es_t* p_es = NULL;
    ctc_port_serdes_info_t serdes_port;
    ctc_acl_property_t  acl_prop;

    sal_memset(&serdes_port, 0, sizeof(serdes_port));

    CTC_SAI_PTR_VALID_CHECK(port_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_HW_LANE_LIST, &lanes_list, &lane_index);
    if (CTC_SAI_ERROR(status))
    {
        goto out;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_SPEED, &port_speed, &speed_index);
    if (CTC_SAI_ERROR(status))
    {
        goto out;
    }

    lanes_count = lanes_list->u32list.count;

    if ((lanes_count == 0) || (lanes_count == 3))
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Port HW lanes count %u is invalid (supported only 1,2,4)\n", lanes_count);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }
    if (lanes_count > MAX_LANES)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Port HW lanes count %u is bigger than %u\n", lanes_count, MAX_LANES);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }

    sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports), status, out);
    ctcs_get_gchip_id(lchip, &gchip);
    for (num = 0; num < local_panel_ports.count; num++)
    {
	/*SYSTEM MODIFIED by jqiu, bug http://10.10.25.13/show_bug.cgi?id=51934, start*/
        //sal_memset(&serdes_port, 0, sizeof(serdes_port));
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
        /*Bug51934, Sonic does't support multi port map to one serdes lane. In order to support
           Qsgmii port, ctc use mac_id instead of serdes lane.*/
        //CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, &serdes_port), status, out);
        //if (serdes_port.serdes_id_array[0] == lanes_list->u32list.list[0])
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_MAC_ID, &mac_id), status, out);
        if (mac_id == lanes_list->u32list.list[0])
	/*SYSTEM MODIFIED by jqiu, bug http://10.10.25.13/show_bug.cgi?id=51934, end*/
        {
            *port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, gport);
            break;
        }
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_port_get_port_db(*port_id, &p_port_db), status, out);

    CTC_SAI_ERROR_GOTO(_ctc_sai_port_mapping_ctc_speed_mode(port_speed->u32, &speed_mode), status, out);

    /*BEGIN: SYSTEM MODIFIED For tsingma 24X2C 100GE port, 20200227*/ /* SAI merge 20200824 */
    chip_type = ctcs_get_chip_type(lchip);
    if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
    {
        uint32 phy_id = 0;
        ctc_port_if_mode_t if_mode;
        ctc_port_if_type_t if_type = CTC_PORT_IF_NONE;

        sys_usw_peri_get_phy_id(lchip, CTC_MAP_GPORT_TO_LPORT(gport), &phy_id);
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "set port speed. chiptype:%u gport:0x%x, phy_id:%u, speed_mode:%u\n", chip_type, gport, phy_id, speed_mode);
        if ((CTC_E_NONE == sys_usw_peri_get_phy_register_exist(lchip, CTC_MAP_GPORT_TO_LPORT(gport))) && (phy_id != CTC_CHIP_PHY_NULL_PHY_ID))
        {
            CTC_SAI_ERROR_RETURN(sys_usw_peri_set_phy_prop(lchip, CTC_MAP_GPORT_TO_LPORT(gport), CTC_PORT_PROP_SPEED, speed_mode));
            CTC_SAI_ERROR_RETURN(ctcs_port_set_speed(lchip, gport, speed_mode));
        }
        else
        {
            if(speed_mode  == CTC_PORT_SPEED_10G)
                if_type = CTC_PORT_IF_XFI;
            else if(speed_mode  == CTC_PORT_SPEED_1G)
                if_type = CTC_PORT_IF_SGMII;
            else if(speed_mode  == CTC_PORT_SPEED_25G)
                if_type = CTC_PORT_IF_CR;
            else if(speed_mode  == CTC_PORT_SPEED_40G)
                if_type = CTC_PORT_IF_CR4;
            else if(speed_mode  == CTC_PORT_SPEED_100G)
                if_type = CTC_PORT_IF_CR4;
            else if(speed_mode  == CTC_PORT_SPEED_50G)
                if_type = CTC_PORT_IF_CR2;
            else if ((speed_mode  == CTC_PORT_SPEED_100M) && (CTC_CHIP_TSINGMA == chip_type))
                if_type = CTC_PORT_IF_FX;

            if_mode.speed = speed_mode;
            if_mode.interface_type = if_type;
            CTC_SAI_ERROR_RETURN(ctcs_port_set_interface_mode(lchip, gport, &if_mode));

            if(speed_mode == CTC_PORT_SPEED_1G)
            {
                CTC_SAI_ERROR_RETURN(ctcs_port_set_speed(lchip, gport, CTC_PORT_SPEED_1G));
            }
        }
    }
    else
	{
    //CTC_SAI_CTC_ERROR_GOTO(ctcs_port_get_capability(lchip, gport, CTC_PORT_CAP_TYPE_SERDES_INFO, (void*)&serdes_port), status, out);

    //if (serdes_port.serdes_mode != CTC_CHIP_SERDES_XFI_MODE)
    //{
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_speed(lchip, gport, speed_mode), status, out);
    }
    /*END: SYSTEM MODIFIED For tsingma 24X2C 100GE port, 20200227*/ /* SAI merge 20200824 END*/

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_FEC_MODE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_FEC_EN, (uint32)attr_value->s32), status, out);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_MTU, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        mtu_size = attr_value->u32;
    }
    else
    {
        mtu_size = 1514;
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_port_set_max_frame(lchip, gport, mtu_size), status, out);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_EEE_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_EEE_EN, (uint32)attr_value->booldata), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PKT_TX_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_TRANSMIT_EN, (uint32)attr_value->booldata), status, out);
    }

    //set policer
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_policer(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_policer(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_policer(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_POLICER_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_policer(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PTP_MODE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_ptp(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PTP_DOMAIN_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_ptp(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PTP_PATH_DELAY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_ptp(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_ptp(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_port_set_ptp(&key, &attr_list[attr_index]), status, out);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_META_DATA, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
        {
            ingress_acl_num = 8;
            egress_acl_num = 3;
        }
        else if (CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
        {
            ingress_acl_num = 16;
            egress_acl_num = 4;
        }

        for (i = 0; i < ingress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_INGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, gport, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[attr_index].value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, gport, &acl_prop));
        }

        for (i = 0; i < egress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, gport, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[attr_index].value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, gport, &acl_prop));
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_ISOLATION_GROUP, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_ERROR_GOTO(ctc_sai_port_set_basic_info(&key, &attr_list[attr_index]), status, out);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_ES, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {

        p_es = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if(NULL != p_es)
        {
            /* need set es on port on tm1.1 and tm2 */
            //CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ES_ID, (uint32)p_es->local_es_id), status, out);
            /* need add port-label mapping on tm1.1 and tm2 */
            p_port_db->ethernet_segment = attr_value->oid;
        }
        else
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PORT_ATTR_MAC_ADDRESS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_object_key_t key = { .key.object_id = *port_id };
        CTC_SAI_CTC_ERROR_GOTO(ctc_sai_port_set_basic_info(&key, &attr_list[attr_index]), status, out);
    }

    status = SAI_STATUS_SUCCESS;
    goto out;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to create port:%d\n", status);
    }
    return status;
}


/**
 * Routine Description:
 *    @brief Remove port
 *
 * Arguments:
 *    @param[in] port_id - port id
 *
 * Return Values:
 *    @return SAI_STATUS_SUCCESS on success
 *            Failure status code on error
 */
sai_status_t
ctc_sai_port_remove_port( sai_object_id_t port_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_port_db_t* p_port_db = NULL;
    sai_object_key_t key;
    sai_attribute_t  attr;
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, port_id, &ctc_object_id);

    if (ctc_object_id.type != SAI_OBJECT_TYPE_PORT)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    lchip= ctc_object_id.lchip;
    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&attr, 0, sizeof(attr));
    key.key.object_id = port_id;

    p_port_db = ctc_sai_db_get_object_property(lchip, port_id);

    if (!p_port_db)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if (p_port_db && p_port_db->policer_id)
    {
        attr.id = SAI_PORT_ATTR_POLICER_ID;
        _ctc_sai_port_set_policer(&key, &attr);
    }
    if (p_port_db && p_port_db->stmctl_flood_policer_id)
    {
        attr.id = SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID;
        _ctc_sai_port_set_policer(&key, &attr);
    }
    if (p_port_db && p_port_db->stmctl_bc_policer_id)
    {
        attr.id = SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID;
        _ctc_sai_port_set_policer(&key, &attr);
    }
    if (p_port_db && p_port_db->stmctl_mc_policer_id)
    {
        attr.id = SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID;
        _ctc_sai_port_set_policer(&key, &attr);
    }

    if (p_port_db && p_port_db->service_id_list)
    {
        if(p_port_db->service_id_list->count)
        {
            status = SAI_STATUS_OBJECT_IN_USE;
        }
        else
        {
            mem_free(p_port_db->service_id_list);
        }
    }

    if (p_port_db)
    {
        mem_free(p_port_db);
        ctc_sai_db_remove_object_property(lchip, port_id);
    }

    out:
        CTC_SAI_DB_UNLOCK(lchip);
        if (SAI_STATUS_SUCCESS != status)
        {
            CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to remove port:%d\n", status);
        }
        return status;
}


/*
 * Routine Description:
 *   Set port attribute value.
 *
 * Arguments:
 *    [in] port_id - port id
 *    [in] attr - attribute
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t
ctc_sai_port_set_port_attribute( sai_object_id_t port_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = port_id };
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    key.key.object_id = port_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
    ctc_sai_port_key_to_str(port_id, key_str);
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key,key_str,
                        SAI_OBJECT_TYPE_PORT,  port_attr_fn_entries,attr), status, error_return);


error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to set port attr id:%d, status:%d\n", attr->id, status);
    }
    return status;
}


/*
 * Routine Description:
 *   Get port attribute value.
 *
 * Arguments:
 *    [in] port_id - port id
 *    [in] attr_count - number of attributes
 *    [inout] attr_list - array of attributes
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t
ctc_sai_port_get_port_attribute( sai_object_id_t     port_id,
                                             uint32_t            attr_count,
                                             sai_attribute_t *attr_list)
{
    sai_object_key_t key = { .key.object_id = port_id };
    char                   key_str[MAX_KEY_STR_LEN];
    uint16    loop = 0;
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    key.key.object_id = port_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
    ctc_sai_port_key_to_str(port_id, key_str);
    CTC_SAI_DB_LOCK(lchip);
    for(loop = 0; loop < attr_count;loop++)
    {

     CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key,key_str,
                    SAI_OBJECT_TYPE_PORT, loop, port_attr_fn_entries,&attr_list[loop]), status, error_return);
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to get port attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}


/*
 * Routine Description:
 *   Get port statistics counters.
 *
 * Arguments:
 *    [in] port_id - port id
 *    [in] number_of_counters - number of counters in the array
 *    [in] counter_ids - specifies the array of counter ids
 *    [out] counters - array of resulting counter values.
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t
ctc_sai_port_get_port_stats( sai_object_id_t        port_id,
                            uint32_t               number_of_counters,
                            const sai_stat_id_t *counter_ids,
                            uint64_t             *counters)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    ctc_mac_stats_t p_stats;
    ctc_mac_stats_t p_stats_out;
    uint32 index = 0;
    uint64 drop_cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);

    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_object_id);

    sal_memset(&p_stats, 0, sizeof(p_stats));
    sal_memset(&p_stats_out, 0, sizeof(p_stats_out));

    p_stats.stats_mode = CTC_STATS_MODE_DETAIL;
    p_stats_out.stats_mode = CTC_STATS_MODE_DETAIL;

    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_INGRESS, &p_stats), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_EGRESS, &p_stats_out), status, out);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if(counter_ids[index] < SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE)
        {
            switch(counter_ids[index])
            {


                case SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_64;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518;
                    break;
                case SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047;
                    break;


                case SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_64;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518;
                    break;
                case SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047;
                    break;


                case SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_64 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_64;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047;
                    break;



                case SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_oversize_pkts;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts + p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts + p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts;
                    break;




                case SAI_PORT_STAT_IF_IN_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_63_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_64 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + \
                                              p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes;
                    break;
                case SAI_PORT_STAT_IF_IN_UCAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts;
                    break;
                case SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_pkts + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_63_pkts + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_64 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_65_to_127 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_128_to_255 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_256_to_511 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_512_to_1023 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_1024_to_1518 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_1519_to_2047 + \
                                              p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes - \
                                              p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts;
                    break;
                case SAI_PORT_STAT_IF_IN_ERRORS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.fcs_error_pkts + p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                    break;
                case SAI_PORT_STAT_IF_IN_MULTICAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts;
                    break;
                case SAI_PORT_STAT_IF_IN_DISCARDS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                    break;
                case SAI_PORT_STAT_IF_IN_BROADCAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts;
                    break;





                case SAI_PORT_STAT_IF_OUT_OCTETS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_63 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_64 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.jumbo_bytes;
                    break;
                case SAI_PORT_STAT_IF_OUT_UCAST_PKTS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts;
                    break;
                case SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.pkts_63 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_64 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_65_to_127 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_128_to_255 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_256_to_511 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_512_to_1023 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_1024_to_1518 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.pkts_1519_to_2047 + \
                                                p_stats_out.u.stats_detail.stats.tx_stats.jumbo_pkts - \
                                                p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts;
                    break;
                case SAI_PORT_STAT_IF_OUT_ERRORS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.fcs_error_pkts;
                    break;
                case SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts;
                    break;
                case SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS:
                    counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                    break;


                case SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                    break;
                case SAI_PORT_STAT_PAUSE_RX_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_normal_pause_pkts + p_stats.u.stats_detail.stats.rx_stats.good_pfc_pause_pkts;
                    break;

                case SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.fcs_error_pkts + p_stats_out.u.stats_detail.stats.tx_stats.fcs_error_pkts;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_OCTETS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_63_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_64 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + \
                                              p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + \
                                              p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_63 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_64 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.jumbo_bytes;
                    break;
                case SAI_PORT_STAT_ETHER_STATS_PKTS:
                    counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_pkts + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_63_pkts + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_64 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_65_to_127 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_128_to_255 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_256_to_511 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_512_to_1023 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_1024_to_1518 + \
                                              p_stats.u.stats_detail.stats.rx_stats.pkts_1519_to_2047 + \
                                              p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                              p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_63 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_64 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_65_to_127 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_128_to_255 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_256_to_511 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_512_to_1023 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_1024_to_1518 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.pkts_1519_to_2047 + \
                                              p_stats_out.u.stats_detail.stats.tx_stats.jumbo_pkts;
                    break;
                default:
                    return SAI_STATUS_NOT_SUPPORTED;
            }
        }
        else if((counter_ids[index] > SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE) && (counter_ids[index] < SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END))
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_debug_counter_get_port_stats(ctc_object_id.lchip, ctc_object_id.value, counter_ids[index], 0, &drop_cnt), status, out);
            counters[index] = drop_cnt;
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }


    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to get port stats ,status = %d\n", status);
    }
    return status;
}

static sai_status_t
ctc_sai_port_get_port_stats_ext( sai_object_id_t        port_id,
                            uint32_t               number_of_counters,
                            const sai_stat_id_t *counter_ids,
                            sai_stats_mode_t mode,
                            uint64_t             *counters)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    ctc_mac_stats_t p_stats;
    ctc_mac_stats_t p_stats_out;
    uint32 index = 0;
    uint64 drop_cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    CTC_SAI_LOG_ENTER(SAI_API_PORT);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_object_id);

    sal_memset(&p_stats, 0, sizeof(p_stats));
    sal_memset(&p_stats_out, 0, sizeof(p_stats_out));

    p_stats.stats_mode = CTC_STATS_MODE_DETAIL;
    p_stats_out.stats_mode = CTC_STATS_MODE_DETAIL;



    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_INGRESS, &p_stats), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_EGRESS, &p_stats_out), status, out);


    for (index = 0; index < number_of_counters; index ++ )
    {
        if(counter_ids[index] < SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE)
        {
            if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
            {
                status = SAI_STATUS_NOT_SUPPORTED;
                goto out;
            }

            switch(counter_ids[index])
            {

            case SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_64;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518;
                break;
            case SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047;
                break;


            case SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_64;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518;
                break;
            case SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047;
                break;


            case SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_64 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_64;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047;
                break;



            case SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_oversize_pkts;
                break;
            case SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                break;
            case SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts + p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts + p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts;
                break;




            case SAI_PORT_STAT_IF_IN_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_63_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_64 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + \
                                          p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes;
                break;
            case SAI_PORT_STAT_IF_IN_UCAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts;
                break;
            case SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_pkts + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_63_pkts + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_64 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_65_to_127 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_128_to_255 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_256_to_511 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_512_to_1023 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_1024_to_1518 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_1519_to_2047 + \
                                          p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes - \
                                          p_stats.u.stats_detail.stats.rx_stats.good_ucast_pkts;
                break;
            case SAI_PORT_STAT_IF_IN_ERRORS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.fcs_error_pkts + p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                break;
            case SAI_PORT_STAT_IF_IN_MULTICAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts;
                break;
            case SAI_PORT_STAT_IF_IN_DISCARDS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                break;
            case SAI_PORT_STAT_IF_IN_BROADCAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts;
                break;





            case SAI_PORT_STAT_IF_OUT_OCTETS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.bytes_63 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_64 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.jumbo_bytes;
                break;
            case SAI_PORT_STAT_IF_OUT_UCAST_PKTS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts;
                break;
            case SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.pkts_63 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_64 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_65_to_127 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_128_to_255 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_256_to_511 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_512_to_1023 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_1024_to_1518 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.pkts_1519_to_2047 + \
                                            p_stats_out.u.stats_detail.stats.tx_stats.jumbo_pkts - \
                                            p_stats_out.u.stats_detail.stats.tx_stats.good_ucast_pkts;
                break;
            case SAI_PORT_STAT_IF_OUT_ERRORS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.fcs_error_pkts;
                break;
            case SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts;
                break;
            case SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS:
                counters[index] = p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                break;


            case SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.mac_overrun_pkts;
                break;
            case SAI_PORT_STAT_PAUSE_RX_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_normal_pause_pkts + p_stats.u.stats_detail.stats.rx_stats.good_pfc_pause_pkts;
                break;

            case SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_mcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_mcast_pkts;
                break;
            case SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_bcast_pkts + p_stats_out.u.stats_detail.stats.tx_stats.good_bcast_pkts;
                break;
            case SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.fcs_error_pkts + p_stats_out.u.stats_detail.stats.tx_stats.fcs_error_pkts;
                break;
            case SAI_PORT_STAT_ETHER_STATS_OCTETS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_63_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_64 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_65_to_127 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_128_to_255 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_256_to_511 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_512_to_1023 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_1024_to_1518 + \
                                          p_stats.u.stats_detail.stats.rx_stats.bytes_1519_to_2047 + \
                                          p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_63 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_64 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_65_to_127 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_128_to_255 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_256_to_511 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_512_to_1023 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_1024_to_1518 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.bytes_1519_to_2047 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.jumbo_bytes;
                break;
            case SAI_PORT_STAT_ETHER_STATS_PKTS:
                counters[index] = p_stats.u.stats_detail.stats.rx_stats.good_63_pkts + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_63_pkts + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_64 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_65_to_127 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_128_to_255 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_256_to_511 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_512_to_1023 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_1024_to_1518 + \
                                          p_stats.u.stats_detail.stats.rx_stats.pkts_1519_to_2047 + \
                                          p_stats.u.stats_detail.stats.rx_stats.good_jumbo_bytes + \
                                          p_stats.u.stats_detail.stats.rx_stats.bad_jumbo_bytes + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_63 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_64 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_65_to_127 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_128_to_255 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_256_to_511 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_512_to_1023 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_1024_to_1518 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.pkts_1519_to_2047 + \
                                          p_stats_out.u.stats_detail.stats.tx_stats.jumbo_pkts;
                break;
            default:
                return SAI_STATUS_NOT_SUPPORTED;

            }
        }
        else if ((counter_ids[index] > SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE) && (counter_ids[index] < SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END))
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_debug_counter_get_port_stats(ctc_object_id.lchip, ctc_object_id.value, counter_ids[index], mode, &drop_cnt), status,out);
            counters[index] = drop_cnt;
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }

    }
/*
    if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
    {
        if (rx_en)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_INGRESS), status, out);
        }
        if (tx_en)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_EGRESS), status, out);
        }
    }
*/
    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to get port stats ,status = %d\n", status);
    }
    return status;
}

/*
 * Routine Description:
 *   Clear port statistics counters.
 *
 * Arguments:
 *    [in] port_id - port id
 *    [in] number_of_counters - number of counters in the array
 *    [in] counter_ids - specifies the array of counter ids
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t
ctc_sai_port_clear_port_stats( sai_object_id_t        port_id,
                                           uint32_t               number_of_counters,
                                           const sai_stat_id_t *counter_ids)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    uint32 index = 0;
    uint64 drop_cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_object_id);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if (SAI_PORT_STAT_IF_IN_OCTETS == counter_ids[index] )
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_STATS_MAC_STATS_RX), status, out);
            continue;
        }

        if (SAI_PORT_STAT_IF_OUT_OCTETS == counter_ids[index])
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_STATS_MAC_STATS_TX), status, out);
            continue;
        }
        if ((counter_ids[index] > SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE) && (counter_ids[index] < SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END))
        {
            /*clear on read */
            CTC_SAI_CTC_ERROR_GOTO(ctc_sai_debug_counter_get_port_stats(ctc_object_id.lchip, ctc_object_id.value, counter_ids[index], 1, &drop_cnt), status, out);
            continue;
        }
    }

    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to clear port stats ,status = %d\n", status);
    }
    return status;
}

/*
 * Routine Description:
 *   Clear port's all statistics counters.
 *
 * Arguments:
 *    [in] port_id - port id
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t
ctc_sai_port_clear_port_all_stats( sai_object_id_t port_id)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    uint64 drop_cnt = 0;
    uint32 stat_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_PORT);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_object_id);

    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_STATS_MAC_STATS_RX), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_mac_stats(ctc_object_id.lchip, ctc_object_id.value, CTC_STATS_MAC_STATS_TX), status, out);

    for(stat_id = SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE; stat_id < SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END; stat_id ++)
    {
        if((stat_id == SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE) || (stat_id == SAI_PORT_STAT_IN_DROP_REASON_RANGE_END)
            ||(stat_id == SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE))
        {
            continue;
        }
        /*clear on read Drop stats*/
        ctc_sai_debug_counter_get_port_stats(ctc_object_id.lchip, ctc_object_id.value, stat_id, 1, &drop_cnt);
    }

    out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Failed to clear port stats ,status = %d\n", status);
    }
    return status;
}


/**
 * @brief Create port pool
 *
 * @param[out] port_pool_id Port pool id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_create_port_pool( sai_object_id_t      *port_pool_id,
                                           sai_object_id_t        switch_id,
                                           uint32_t               attr_count,
                                           const sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

/**
 * @brief Remove port pool
 *
 * @param[in] port_pool_id Port pool id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_remove_port_pool( sai_object_id_t port_pool_id)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}



/**
 * @brief Set port pool attribute value.
 *
 * @param[in] port_pool_id Port pool id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_set_port_pool_attribute( sai_object_id_t port_pool_id,  const sai_attribute_t *attr)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

/**
 * @brief Get port pool attribute value.
 *
 * @param[in] port_pool_id Port pool id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_get_port_pool_attribute( sai_object_id_t     port_pool_id,
                                                  uint32_t            attr_count,
                                                 sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

/**
 * @brief Get port pool statistics counters.
 *
 * @param[in] port_pool_id Port pool id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_get_port_pool_stats( sai_object_id_t             port_pool_id,
                                              uint32_t                    number_of_counters,
                                              const sai_stat_id_t *counter_ids,
                                              uint64_t                  *counters)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

static sai_status_t
ctc_sai_port_get_port_pool_stats_ext( sai_object_id_t             port_pool_id,
                                              uint32_t                    number_of_counters,
                                              const sai_stat_id_t *counter_ids,
                                              sai_stats_mode_t mode,
                                              uint64_t                  *counters)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

/**
 * @brief Clear port pool statistics counters.
 *
 * @param[in] port_pool_id Port pool id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_clear_port_pool_stats( sai_object_id_t             port_pool_id,
                                                uint32_t                    number_of_counters,
                                                const sai_stat_id_t *counter_ids)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}


/**
 * @brief Create port serdes
 *
 * @param[out] port_serdes_id Port serdes id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

static sai_status_t
ctc_sai_port_create_port_serdes(sai_object_id_t *port_serdes_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}



/**
 * @brief Remove port serdes
 *
 * @param[in] port_serdes_id Port serdes id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_remove_port_serdes(sai_object_id_t port_serdes_id)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}


/**
 * @brief Set Port serdes attribute value.
 *
 * @param[in] port_serdes_id Port serdes id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_set_port_serdes_attribute(sai_object_id_t port_serdes_id, const sai_attribute_t *attr)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}


/**
 * @brief Get Port serdes attribute value.
 *
 * @param[in] port_serdes_id Port serdes id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t
ctc_sai_port_get_port_serdes_attribute(sai_object_id_t port_serdes_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}




const sai_port_api_t g_ctc_sai_port_api = {
    ctc_sai_port_create_port,
    ctc_sai_port_remove_port,
    ctc_sai_port_set_port_attribute,
    ctc_sai_port_get_port_attribute,
    ctc_sai_port_get_port_stats,
    ctc_sai_port_get_port_stats_ext,
    ctc_sai_port_clear_port_stats,
    ctc_sai_port_clear_port_all_stats,
    ctc_sai_port_create_port_pool,
    ctc_sai_port_remove_port_pool,
    ctc_sai_port_set_port_pool_attribute,
    ctc_sai_port_get_port_pool_attribute,
    ctc_sai_port_get_port_pool_stats,
    ctc_sai_port_get_port_pool_stats_ext,
    ctc_sai_port_clear_port_pool_stats,
    ctc_sai_port_create_port_serdes,
    ctc_sai_port_remove_port_serdes,
    ctc_sai_port_set_port_serdes_attribute,
    ctc_sai_port_get_port_serdes_attribute
};


sai_status_t
ctc_sai_port_api_init()
{
    ctc_sai_register_module_api(SAI_API_PORT, (void*)&g_ctc_sai_port_api);

    return SAI_STATUS_SUCCESS;
}

extern int32 sys_usw_chip_check_active(uint8 lchip);

void
_ctc_sai_port_polling_thread(void *data)
{
    uint8 lchip = 0;
    uint8 gchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint16 port_idx = 0;
    bool link_status = 0;
    uint32 gport = 0;
    ctc_global_panel_ports_t local_panel_ports;
    sai_port_oper_status_notification_t port_state_event;

    lchip = (uint8)(uintptr)data;
    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
    sal_memset(&port_state_event, 0, sizeof(sai_port_oper_status_notification_t));

    ctcs_get_gchip_id(lchip, &gchip);
    ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return;
    }
    while(true)
    {
        CTC_SAI_DB_LOCK(lchip);
        //chip active check
        if(sys_usw_chip_check_active(lchip) < 0)
        {
            return;
        }

        if (p_switch_master->port_state_change_cb)
        {
            for(port_idx = 0; port_idx < local_panel_ports.count; port_idx++)
            {
                gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[port_idx]);
                //#if (1 == LINK_STATUS_MODE)
                ctcs_port_get_mac_link_up(lchip, gport, &link_status);
                //#else
                //ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_LINK_UP, (uint32*)&link_status);
                //#endif
                

                if (1 == SDK_WORK_PLATFORM)  // UML link_status is by port_en
                {
                    link_status = 0;
                    ctcs_port_get_port_en(lchip, gport, &link_status);
                }

                if(link_status != p_switch_master->lport_link_status[CTC_MAP_GPORT_TO_LPORT(gport)])
                {
                    p_switch_master->lport_link_status[CTC_MAP_GPORT_TO_LPORT(gport)] = link_status;

                    if (link_status)
                    {
                        CTC_SAI_LOG_NOTICE(SAI_API_PORT, "gport 0x%04X Link Up, Port is enabled! \n", gport);
                        port_state_event.port_state = SAI_PORT_OPER_STATUS_UP;
                        ctcs_port_set_port_en(lchip, gport, 1);
                    }
                    else
                    {
                        ctc_object_id_t ctc_bridge_port_id ={0};
                        sai_object_id_t bridge_port_id;
                        sai_attribute_t attr_list;
                        sai_object_id_t switch_id;

                        CTC_SAI_LOG_NOTICE(SAI_API_PORT, "gport 0x%04X Link Down, Port is disabled, please do port enable when linkup again! \n", gport);
                        port_state_event.port_state = SAI_PORT_OPER_STATUS_DOWN;
                        ctcs_port_set_port_en(lchip, gport, 0);

                        /*flush fdb*/
                        switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
                        ctc_bridge_port_id.lchip = lchip;
                        ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
                        ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
                        ctc_bridge_port_id.value = gport;
                        ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, &bridge_port_id);
                        attr_list.id = SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID;
                        attr_list.value.oid = bridge_port_id;
                        ctc_sai_fdb_flush_fdb(switch_id, 1, &attr_list);
                    }

                    port_state_event.port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, gport);
                    p_switch_master->port_state_change_cb(1, &port_state_event);
                }
            }
        }
        CTC_SAI_DB_UNLOCK(lchip);
        sal_task_sleep(1000);
    }
}

sai_status_t
ctc_sai_port_db_init(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint8 gchip = 0;
    ctc_global_panel_ports_t local_panel_ports;
    uint32 port_idx = 0;
    uint32 gport = 0;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_PORT;
    wb_info.data_len = sizeof(ctc_sai_port_db_t);
    wb_info.wb_sync_cb = _ctc_sai_port_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_port_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_port_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_PORT, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    //if (0 == SDK_WORK_PLATFORM)   // actual borad
    {
        sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
        ctcs_get_gchip_id(lchip, &gchip);
        ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);

        for(port_idx = 0; port_idx < local_panel_ports.count; port_idx++)
        {
            gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[port_idx]);
            ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_PORT_EN, 0);
        }

        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }

        sal_task_create(&p_switch_master->port_polling_task, "saiPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
            _ctc_sai_port_polling_thread, (void*)(uintptr)lchip);
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_port_db_deinit(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    if (0 == SDK_WORK_PLATFORM)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }
        sal_task_destroy(p_switch_master->port_polling_task);
    }

    return SAI_STATUS_SUCCESS;
}

/*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/ /* SAI merge 20200824 */
sai_status_t
ctc_sai_port_db_run(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_FAILURE;
    }

    p_switch_master->port_polling_task = NULL;
    sal_task_create(&p_switch_master->port_polling_task, "saiPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
                    _ctc_sai_port_polling_thread, (void*)(uintptr)lchip);

    return SAI_STATUS_SUCCESS;
}

