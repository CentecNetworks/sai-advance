#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_route.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_y1731.h"


typedef struct  ctc_sai_y1731_session_wb_s
{
    /*key*/
    sai_object_id_t oid;
    sai_object_id_t rmep_oid;
    uint32 calc_key_len[0];
    /*data*/
    
}ctc_sai_y1731_session_wb_t;


static sai_status_t
_ctc_sai_y1731_meg_build_db(uint8 lchip, sai_object_id_t y1731_obj_id, ctc_sai_y1731_meg_t** oid_property)
{
    sai_status_t   status = SAI_STATUS_SUCCESS;
    ctc_sai_y1731_meg_t* p_y1731_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    p_y1731_info = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_y1731_meg_t));
    if (NULL == p_y1731_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_y1731_info, 0, sizeof(ctc_sai_y1731_meg_t));
    status = ctc_sai_db_add_object_property(lchip, y1731_obj_id, (void*)p_y1731_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_y1731_info);
        return status;
    }

    *oid_property = p_y1731_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_session_build_db(uint8 lchip, sai_object_id_t y1731_obj_id, ctc_sai_y1731_session_t** oid_property)
{
    sai_status_t   status = SAI_STATUS_SUCCESS;
    ctc_sai_y1731_session_t* p_y1731_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    p_y1731_info = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_y1731_session_t));
    if (NULL == p_y1731_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_y1731_info, 0, sizeof(ctc_sai_y1731_session_t));
    status = ctc_sai_db_add_object_property(lchip, y1731_obj_id, (void*)p_y1731_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_y1731_info);
        return status;
    }

    *oid_property = p_y1731_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_rmep_build_db(uint8 lchip, sai_object_id_t y1731_obj_id, ctc_sai_y1731_rmep_t** oid_property)
{
    sai_status_t   status = SAI_STATUS_SUCCESS;
    ctc_sai_y1731_rmep_t* p_y1731_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    p_y1731_info = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_y1731_rmep_t));
    if (NULL == p_y1731_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_y1731_info, 0, sizeof(ctc_sai_y1731_rmep_t));
    status = ctc_sai_db_add_object_property(lchip, y1731_obj_id, (void*)p_y1731_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_y1731_info);
        return status;
    }

    *oid_property = p_y1731_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_remove_db(uint8 lchip, sai_object_id_t y1731_obj_id)
{
    void* p_y1731_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    p_y1731_info = ctc_sai_db_get_object_property(lchip, y1731_obj_id);
    if (NULL == p_y1731_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, y1731_obj_id);
    mem_free(p_y1731_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_build_maid(sai_y1731_meg_type_t meg_type, char* meg_name, ctc_oam_maid_t* oam_maid)
{
    uint8 meg_id_len = 0;
    uint8 maid_len = 0;
    
    switch (meg_type)
    {
        case SAI_Y1731_MEG_TYPE_ETHER_VLAN:
        case SAI_Y1731_MEG_TYPE_L2VPN_VLAN:
        case SAI_Y1731_MEG_TYPE_L2VPN_VPLS:
        case SAI_Y1731_MEG_TYPE_L2VPN_VPWS:
            oam_maid->mep_type = CTC_OAM_MEP_TYPE_ETH_Y1731;
            break;
        case SAI_Y1731_MEG_TYPE_MPLS_TP:
            oam_maid->mep_type = CTC_OAM_MEP_TYPE_MPLS_TP_Y1731;
            break;
    }

    oam_maid->maid[0] = 0x1; /* MD name format 1 */
    oam_maid->maid[1] = 32;  /* ICC based format */

    meg_id_len = sal_strlen(meg_name);
    if (meg_id_len > 13)  /* 16 bytes total for Y.1731*/
    {
        return SAI_STATUS_FAILURE;
    }
    else
    {
        maid_len = meg_id_len + 3;
        oam_maid->maid_len = maid_len;
    }

    oam_maid->maid[2] = 13; /* megid len */
    
    sal_memcpy(&oam_maid->maid[3], meg_name, meg_id_len);
    //oam_maid->maid_len = SAI_Y1731_MEG_NAME_SIZE;

    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_y1731_session_traverse_get_session_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    ctc_sai_y1731_session_t* p_y1731_session_info = bucket_data->data;

    if (p_y1731_session_info->lmep_index == *(uint32*)user_data->value0)        
    {
        *(uint64*)(user_data->value4) = bucket_data->oid;

        return -1;
    }

    return 0;
}

static int32
_ctc_sai_y1731_rmep_traverse_get_rmep_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    ctc_sai_y1731_rmep_t* p_y1731_rmep_info = bucket_data->data;

    if (p_y1731_rmep_info->rmep_index == *(uint32*)user_data->value0)        
    {
        *(uint64*)(user_data->value4) = bucket_data->oid;

        return -1;
    }

    return 0;
}

static sai_status_t
_ctc_sai_y1731_session_db_deinit_cb(void* bucket_data, void* user_data)
{
    ctc_slistnode_t *cur_node = NULL;
    ctc_slistnode_t *next_node = NULL;
    ctc_sai_y1731_session_t *p_y1731_session = NULL;
    ctc_sai_oid_property_t *p_oid_property = NULL;
    ctc_sai_y1731_rmep_id_t *p_rmep_node_info = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_y1731_session = (ctc_sai_y1731_session_t*)(p_oid_property->data);

    CTC_SLIST_LOOP_DEL(p_y1731_session->rmep_head, cur_node, next_node)
    {
        p_rmep_node_info = (ctc_sai_y1731_rmep_id_t*)cur_node;
        mem_free(p_rmep_node_info);
    }
    ctc_slist_free(p_y1731_session->rmep_head);

    return SAI_STATUS_SUCCESS;
}

#define ________SAI_DUMP________
static sai_status_t
_ctc_sai_y1731_dump_meg_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  y1731_meg_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_y1731_meg_t y1731_meg_cur;

    sal_memset(&y1731_meg_cur, 0, sizeof(ctc_sai_y1731_meg_t));

    y1731_meg_oid = bucket_data->oid;
    sal_memcpy((ctc_sai_y1731_meg_t*)(&y1731_meg_cur), bucket_data->data, sizeof(ctc_sai_y1731_meg_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (y1731_meg_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
   
    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-12d %-12d %-16s\n", \
        num_cnt, y1731_meg_oid, y1731_meg_cur.meg_type, y1731_meg_cur.level, y1731_meg_cur.meg_name);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_dump_session_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  y1731_session_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_y1731_session_t y1731_session_cur;

    sal_memset(&y1731_session_cur, 0, sizeof(ctc_sai_y1731_session_t));

    y1731_session_oid = bucket_data->oid;
    sal_memcpy((ctc_sai_y1731_session_t*)(&y1731_session_cur), bucket_data->data, sizeof(ctc_sai_y1731_session_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (y1731_session_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
   
    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" 0x%016"PRIx64" %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d 0x%016"PRIx64" 0x%016"PRIx64" %-12d\n", \
        num_cnt, y1731_session_oid, y1731_session_cur.meg_oid, y1731_session_cur.meg_type, y1731_session_cur.dir, y1731_session_cur.lmep_id, \
        y1731_session_cur.ccm_period, y1731_session_cur.ccm_en, y1731_session_cur.lm_offload_type, y1731_session_cur.dm_offload_type, \
        y1731_session_cur.lm_en, y1731_session_cur.lm_type, y1731_session_cur.dm_en, y1731_session_cur.without_gal, y1731_session_cur.mpls_ttl, \
        y1731_session_cur.exp_or_cos, y1731_session_cur.tp_rif_oid, y1731_session_cur.nh_oid, y1731_session_cur.lmep_index);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_dump_rmep_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  y1731_rmep_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_y1731_rmep_t y1731_rmep_cur;

    sal_memset(&y1731_rmep_cur, 0, sizeof(ctc_sai_y1731_rmep_t));

    y1731_rmep_oid = bucket_data->oid;
    sal_memcpy((ctc_sai_y1731_rmep_t*)(&y1731_rmep_cur), bucket_data->data, sizeof(ctc_sai_y1731_rmep_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (y1731_rmep_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
   
    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" 0x%016"PRIx64" %-12d %-12d \n", \
        num_cnt, y1731_rmep_oid, y1731_rmep_cur.y1731_session_oid, y1731_rmep_cur.rmep_id, y1731_rmep_cur.rmep_index);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}


#define ________INTERNAL_API________
void ctc_sai_y1731_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Y1731 MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_Y1731_MEG))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Y1731 MEG");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_y1731_meg_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------- Y1731 MEG ----------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-12s %-16s \n", \
            "No.", "meg_oid", "MEG Type", "Level", "MEG Name");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;

        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_MEG,
                                            (hash_traversal_fn)_ctc_sai_y1731_dump_meg_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_Y1731_SESSION))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Y1731 Session");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_y1731_meg_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------- Y1731 Session ----------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-18s %-18s %-12s\n", \
            "No.", "session_oid", "Meg oid", "MEG Type", "Dir", "lmep Id", "ccm period", "ccm Enable", \
            "lm offload", "dm offload", "lm En", "Lm Type", "Dm En", "without gal", "mpls ttl", "mpls exp", "tp rif", "NH Oid", "lmep Index");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_SESSION,
                                            (hash_traversal_fn)_ctc_sai_y1731_dump_session_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_Y1731_REMOTE_MEP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Y1731 Reomte Mep");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_y1731_rmep_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------- Y1731 Remote Mep ----------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-12s %-12s \n", \
            "No.", "rmep_oid", "Session Oid", "Rmep Id", "Rmep Index");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;

        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_REMOTE_MEP,
                                            (hash_traversal_fn)_ctc_sai_y1731_dump_rmep_print_cb, (void*)(&sai_cb_data));
    }
}

sai_status_t
ctc_sai_y1731_traverse_get_oid_by_mepindex(uint8 lchip, uint32 mepindex, uint8 isremote, sai_object_id_t* obj_id)
{
    ctc_sai_db_traverse_param_t bfd_cb;

    sal_memset(&bfd_cb, 0, sizeof(ctc_sai_db_traverse_param_t));

    bfd_cb.lchip = lchip;
    bfd_cb.value0 = (void*)&mepindex;
    bfd_cb.value4 = (void*)obj_id;

    if(!isremote)
    {
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_SESSION, (hash_traversal_fn)_ctc_sai_y1731_session_traverse_get_session_cb, (void*)&bfd_cb);
    }
    else
    {
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_REMOTE_MEP, (hash_traversal_fn)_ctc_sai_y1731_rmep_traverse_get_rmep_cb, (void*)&bfd_cb);
    }
    return SAI_STATUS_SUCCESS;
}

#define ________SAI_Y1731_MEG________

static sai_status_t
_ctc_sai_y1731_meg_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_TYPE, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_NAME, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_LEVEL, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_y1731_meg_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_y1731_meg_t* p_y1731_meg_info = NULL; 

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_Y1731_MEG, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_y1731_meg_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_y1731_meg_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_Y1731_MEG_ATTR_TYPE:
            attr->value.s32 = p_y1731_meg_info->meg_type;
            break;
        case SAI_Y1731_MEG_ATTR_NAME:
            sal_memcpy(attr->value.chardata, p_y1731_meg_info->meg_name, SAI_Y1731_MEG_NAME_SIZE);
            break;
        case SAI_Y1731_MEG_ATTR_LEVEL:
            attr->value.u8 = p_y1731_meg_info->level;
            break;
        default:
            break;
    }

    return status;
}

sai_status_t
ctc_sai_y1731_meg_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    
    return status;
}

static ctc_sai_attr_fn_entry_t  y1731_meg_attr_fn_entries[] =
{
    { SAI_Y1731_MEG_ATTR_TYPE,
      ctc_sai_y1731_meg_get_info,
      NULL},
    { SAI_Y1731_MEG_ATTR_NAME,
      ctc_sai_y1731_meg_get_info,
      NULL},
    { SAI_Y1731_MEG_ATTR_LEVEL,
      ctc_sai_y1731_meg_get_info,
      NULL},      
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};      

#define ________SAI_Y1731_SESSION________
static sai_status_t
_ctc_sai_y1731_session_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    ctc_sai_y1731_meg_t* p_y1731_meg_info = NULL;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_MEG, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    else
    {
        p_y1731_meg_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_y1731_meg_info)
        {
            CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 meg, invalid sai_y1731_meg_id %d!\n", attr_value->oid);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_DIR, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_VLAN_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        if((SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_meg_info->meg_type))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_BRIDGE_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        if((SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_meg_info->meg_type))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_PORT_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        if((SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_meg_info->meg_type))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        if(SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_meg_info->meg_type)
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    //status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_IS_P2P_MODE, &attr_value, &index);
    //if (CTC_SAI_ERROR(status))
    //{        
    //    return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    //}

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if(SAI_Y1731_MEG_TYPE_MPLS_TP != p_y1731_meg_info->meg_type)
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, attr_value->oid, &ctc_object_id);
        if( SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
        {
            p_next_hop_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if(NULL == p_next_hop_info)
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
            }
        }
        else if( SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
        {
            //TODO
        }
        else
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_y1731_session_get_rmep_list(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL; 
    ctc_sai_y1731_rmep_id_t *p_rmep_node = NULL;
    ctc_slistnode_t *node = NULL;
    uint32 output_cnt = 0;
    sai_object_id_t *rmep_oid;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_Y1731_SESSION, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_y1731_session_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    rmep_oid = mem_malloc(MEM_SYSTEM_MODULE, attr->value.objlist.count * sizeof(sai_object_id_t));
    if (!rmep_oid)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    CTC_SLIST_LOOP(p_y1731_session_info->rmep_head, node)
    {
        p_rmep_node = _ctc_container_of(node, ctc_sai_y1731_rmep_id_t, node);
        if (output_cnt < attr->value.objlist.count)
        {            
            rmep_oid[output_cnt++] = p_rmep_node->rmep_oid;
        }
        else
        {
            status = SAI_STATUS_BUFFER_OVERFLOW;
            break;
        }
    }

    ctc_sai_fill_object_list(sizeof(sai_object_id_t), rmep_oid, output_cnt, (void*)&attr->value.objlist);
    mem_free(rmep_oid);

    return status;    
}



sai_status_t
ctc_sai_y1731_session_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL; 
    ctc_oam_mep_info_t  mep_info;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_Y1731_SESSION, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_y1731_session_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset((void*)&mep_info, 0, sizeof(ctc_oam_mep_info_t));
    mep_info.mep_index = p_y1731_session_info->lmep_index;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info(lchip, &mep_info), status, out);

    switch(attr->id)
    {
        case SAI_Y1731_SESSION_ATTR_MEG:
            attr->value.oid = p_y1731_session_info->meg_oid;
            break;
        case SAI_Y1731_SESSION_ATTR_DIR:
            attr->value.s32 = p_y1731_session_info->dir;
            break;
        case SAI_Y1731_SESSION_ATTR_VLAN_ID:
            if(( SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_session_info->meg_type)
                || ( SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_session_info->meg_type))
            {
                attr->value.u32 = p_y1731_session_info->oam_key.u.eth.vlan_id;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }
            break;
        case SAI_Y1731_SESSION_ATTR_BRIDGE_ID:
            attr->value.oid = p_y1731_session_info->bridge_id;
            break;
        case SAI_Y1731_SESSION_ATTR_PORT_ID:
            if(( SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_session_info->meg_type)
                || ( SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_session_info->meg_type)
                || ( SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_session_info->meg_type)
                || ( SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_session_info->meg_type))
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, p_y1731_session_info->oam_key.u.eth.gport);
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }            
            break;
        case SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL:
            if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
            {
                attr->value.u32 = p_y1731_session_info->oam_key.u.tp.label;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }
            break;
        case SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
            attr->value.u32 = p_y1731_session_info->lmep_id;
            break;
        case SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
            attr->value.s32 = p_y1731_session_info->ccm_period;
            break;
        case SAI_Y1731_SESSION_ATTR_CCM_ENABLE:
            attr->value.booldata = p_y1731_session_info->ccm_en;
            break;
        //case SAI_Y1731_SESSION_ATTR_IS_P2P_MODE:
        //    attr->value.booldata = p_y1731_session_info->is_p2p_mode;
        //    break;
        case SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE:
            attr->value.s32 = p_y1731_session_info->lm_offload_type;
            break;
        case SAI_Y1731_SESSION_ATTR_LM_ENABLE:
            attr->value.booldata = p_y1731_session_info->lm_en;
            break;
        case SAI_Y1731_SESSION_ATTR_LM_TYPE:
            attr->value.s32 = p_y1731_session_info->lm_type;
            break;
        case SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE:
            attr->value.s32 = p_y1731_session_info->dm_offload_type;
            break;
        case SAI_Y1731_SESSION_ATTR_DM_ENABLE:
            attr->value.booldata = p_y1731_session_info->dm_en;
            break;
        case SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
            attr->value.u8 = mep_info.lmep.y1731_lmep.present_rdi;
            break;
        case SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID:
            if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
            {
                attr->value.oid = p_y1731_session_info->tp_rif_oid;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }            
            break;
        case SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL:
            if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
            {
                attr->value.booldata = p_y1731_session_info->without_gal;
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }   
            break;
        case SAI_Y1731_SESSION_ATTR_TTL:
            attr->value.u8 = p_y1731_session_info->mpls_ttl;
            break;
        case SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
            attr->value.u8 = p_y1731_session_info->exp_or_cos;
            break;
        case SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID:
            attr->value.oid = p_y1731_session_info->nh_oid;
            break;
        default:
            break;
    }

out:
    return status;
}

sai_status_t
ctc_sai_y1731_session_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_id_t y1731_session_id = 0;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    
    //ctc_oam_mep_info_t  mep_info;
    ctc_oam_update_t  update_lmep;
    
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;

    //sal_memset(&mep_info, 0, sizeof(ctc_oam_mep_info_t));
    sal_memset(&update_lmep, 0, sizeof(ctc_oam_update_t));

    y1731_session_id = key->key.object_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "y1731_session_id = %llu\n", y1731_session_id);

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, y1731_session_id);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 session, invalid y1731_session_id %d!\n", y1731_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    //mep_info.mep_index = p_y1731_session_info->lmep_index;
    //CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info(lchip, &mep_info), status, out); 

    sal_memcpy(&(update_lmep.key), &(p_y1731_session_info->oam_key), sizeof(ctc_oam_key_t));
    update_lmep.is_local = 1;

    switch(attr->id)
    {
         case SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_MEP_ID;
            update_lmep.update_value = attr->value.u32;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
         
            p_y1731_session_info->lmep_id = attr->value.u32;
        case SAI_Y1731_SESSION_ATTR_CCM_PERIOD:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_CCM_INTERVAL;
            update_lmep.update_value = attr->value.s32;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->ccm_period = attr->value.s32;
            break;
        case SAI_Y1731_SESSION_ATTR_CCM_ENABLE:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_CCM_EN;
            update_lmep.update_value = attr->value.booldata;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->ccm_en = attr->value.booldata;
            break;
        case SAI_Y1731_SESSION_ATTR_LM_ENABLE:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_LM_EN;
            update_lmep.update_value = attr->value.booldata;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->lm_en = attr->value.booldata;
            break;
        case SAI_Y1731_SESSION_ATTR_LM_TYPE:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_LM_TYPE;
            if(SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED == attr->value.s32)
            {
                update_lmep.update_value = CTC_OAM_LM_TYPE_DUAL;
            }
            else
            {
                update_lmep.update_value = CTC_OAM_LM_TYPE_SINGLE;
            }

            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
        
            p_y1731_session_info->lm_type = attr->value.s32;
            break;
        case SAI_Y1731_SESSION_ATTR_DM_ENABLE:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_DM_EN;
            update_lmep.update_value = attr->value.booldata;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->dm_en = attr->value.booldata;
            break;
        case SAI_Y1731_SESSION_ATTR_LOCAL_RDI:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_RDI;
            update_lmep.update_value = attr->value.booldata;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->lm_en = attr->value.booldata;
            break;
        case SAI_Y1731_SESSION_ATTR_TTL:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_TTL;
            update_lmep.update_value = attr->value.u8;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->mpls_ttl = attr->value.u8;
            break;
        case SAI_Y1731_SESSION_ATTR_EXP_OR_COS:            
            update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_TX_COS_EXP;
            update_lmep.update_value = attr->value.u8;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
            p_y1731_session_info->exp_or_cos = attr->value.u8;
            break;
        case SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID:  
            if(SAI_Y1731_MEG_TYPE_MPLS_TP != p_y1731_session_info->meg_type)
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0;
            }

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, attr->value.oid, &ctc_object_id);
            if( SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
            {
                p_next_hop_info = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if(NULL == p_next_hop_info)
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0;
                }
                update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_NHOP;
                update_lmep.update_value = ctc_object_id.value;
                CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
            
                p_y1731_session_info->nh_oid = attr->value.oid;                
            }
            else if( SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
            {
                //TODO
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0;
            }                    
            break;
        default:
            break;        
    }
    
out:
    return status;
}

static ctc_sai_attr_fn_entry_t  y1731_session_attr_fn_entries[] =
{
    { SAI_Y1731_SESSION_ATTR_MEG,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_DIR,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_VLAN_ID,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_BRIDGE_ID,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_PORT_ID,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_CCM_PERIOD,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_CCM_ENABLE,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    //{ SAI_Y1731_SESSION_ATTR_IS_P2P_MODE,
    //  ctc_sai_y1731_session_get_info,
    //  NULL},
    { SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST,
      ctc_sai_y1731_session_get_rmep_list,
      NULL},
    { SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_LM_ENABLE,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_LM_TYPE,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_DM_ENABLE,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_LOCAL_RDI,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL,
      ctc_sai_y1731_session_get_info,
      NULL},
    { SAI_Y1731_SESSION_ATTR_TTL,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_EXP_OR_COS,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID,
      ctc_sai_y1731_session_get_info,
      ctc_sai_y1731_session_set_info},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

#define ________SAI_Y1731_RMEP________
static sai_status_t
_ctc_sai_y1731_rmep_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    else
    {
        p_y1731_session_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_y1731_session_info)
        {
            CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 session, invalid p_y1731_session_info %d!\n", attr_value->oid);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    return status;
}

sai_status_t
ctc_sai_y1731_rmep_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL; 
    ctc_sai_y1731_rmep_t* p_y1731_rmep_info = NULL; 
    ctc_oam_mep_info_with_key_t  mep_info;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_Y1731_REMOTE_MEP, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_y1731_rmep_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_y1731_rmep_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, p_y1731_rmep_info->y1731_session_oid);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 rmep, invalid sai_y1731_session_id %d!\n", p_y1731_rmep_info->y1731_session_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    sal_memset((void*)&mep_info, 0, sizeof(ctc_oam_mep_info_with_key_t));

    sal_memcpy(&mep_info.key, &p_y1731_session_info->oam_key, sizeof(ctc_oam_key_t));
    mep_info.rmep_id = p_y1731_rmep_info->rmep_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info_with_key(lchip, &mep_info), status, out);    

    switch(attr->id)
    {
        case SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
            attr->value.oid = p_y1731_rmep_info->y1731_session_oid;
            break;
        case SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
            attr->value.u32 = p_y1731_rmep_info->rmep_id;
            break;
        case SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
            sal_memcpy(&attr->value.mac, mep_info.rmep.y1731_rmep.mac_sa, sizeof(sai_mac_t));
            break;
        case SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
            attr->value.booldata = mep_info.rmep.y1731_rmep.first_pkt_rx;
            break;
        default:
            break;
    }

out:
    return status;
}

sai_status_t
ctc_sai_y1731_rmep_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_id_t y1731_rmep_id = 0;
    ctc_sai_y1731_rmep_t* p_y1731_rmep_info = NULL;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;

    ctc_oam_update_t  update_rmep;   

    sal_memset(&update_rmep, 0, sizeof(ctc_oam_update_t));

    y1731_rmep_id = key->key.object_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "y1731_rmep_id = %llu\n", y1731_rmep_id);

    p_y1731_rmep_info = ctc_sai_db_get_object_property(lchip, y1731_rmep_id);
    if (NULL == p_y1731_rmep_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 rmep, invalid p_y1731_rmep_info %d!\n", p_y1731_rmep_info);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, p_y1731_rmep_info->y1731_session_oid);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 session, invalid y1731_session_id %d!\n", p_y1731_rmep_info->y1731_session_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    sal_memcpy(&(update_rmep.key), &(p_y1731_session_info->oam_key), sizeof(ctc_oam_key_t));

    switch(attr->id)
    {
        case SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:            
            update_rmep.update_type = CTC_OAM_Y1731_RMEP_UPDATE_TYPE_RMEP_MACSA;
            update_rmep.p_update_value = (void*)&attr->value.mac;
         
            CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_rmep(lchip, &update_rmep), status, out);         
            break;
        default:
            break;
    }
    
out:
    return status;
}

static ctc_sai_attr_fn_entry_t  y1731_rmep_attr_fn_entries[] =
{
    { SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID,
      ctc_sai_y1731_rmep_get_info,
      NULL},
    { SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID,
      ctc_sai_y1731_rmep_get_info,
      NULL},
    { SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS,
      ctc_sai_y1731_rmep_get_info,
      ctc_sai_y1731_rmep_set_info},
    { SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED,
      ctc_sai_y1731_rmep_get_info,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

#define ________WARMBOOT________

static sai_status_t
_ctc_sai_y1731_session_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t y1731_session_id = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_y1731_session_t* p_y1731_session_info = (ctc_sai_y1731_session_t*)data;
    ctc_sai_y1731_session_wb_t y1731_session_wb;
    ctc_slistnode_t *rmep_node = NULL;
    ctc_sai_y1731_rmep_id_t *p_rmep_node_info = NULL;
    uint32 offset = 0;

    sal_memset(&y1731_session_wb, 0, sizeof(ctc_sai_y1731_session_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_y1731_session_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_Y1731);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    
    CTC_SLIST_LOOP(p_y1731_session_info->rmep_head, rmep_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_rmep_node_info = (ctc_sai_y1731_rmep_id_t*)rmep_node;
        y1731_session_wb.oid = y1731_session_id;
        y1731_session_wb.rmep_oid = p_rmep_node_info->rmep_oid;
        
        sal_memcpy((uint8*)wb_data.buffer + offset, &y1731_session_wb, (wb_data.key_len + wb_data.data_len));

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
_ctc_sai_y1731_meg_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t meg_obj_id = *(sai_object_id_t*)key;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, meg_obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_Y1731_MEG, ctc_object_id.value));  

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_session_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t session_obj_id = *(sai_object_id_t*)key;
    ctc_sai_y1731_session_t* p_y1731_session_info = (ctc_sai_y1731_session_t*)data;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, session_obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_Y1731_SESSION, ctc_object_id.value));  

    p_y1731_session_info->rmep_head = ctc_slist_new();
    
    if (NULL == p_y1731_session_info->rmep_head)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_y1731_session_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    ctc_sai_y1731_session_wb_t y1731_session_wb;
    ctc_sai_y1731_rmep_id_t *p_rmep_node_info = NULL;

    sal_memset(&y1731_session_wb, 0, sizeof(ctc_sai_y1731_session_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_y1731_session_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_Y1731);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&y1731_session_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_y1731_session_wb_t));
        p_y1731_session_info = ctc_sai_db_get_object_property(lchip, y1731_session_wb.oid);
        if (!p_y1731_session_info)
        {
            continue;
        }

        p_rmep_node_info = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_y1731_rmep_id_t));
        if (!p_rmep_node_info)
        {
            continue;
        }
        p_rmep_node_info->rmep_oid = y1731_session_wb.rmep_oid;

        ctc_slist_add_tail(p_y1731_session_info->rmep_head, &(p_rmep_node_info->node));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
 }

static sai_status_t
_ctc_sai_y1731_rmep_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t session_obj_id = *(sai_object_id_t*)key;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, session_obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP, ctc_object_id.value));  

    return SAI_STATUS_SUCCESS;
}


#define ________SAI_API________

sai_status_t ctc_sai_y1731_create_y1731_meg( sai_object_id_t *sai_y1731_meg_id,
                                      sai_object_id_t        switch_id,
                                      uint32_t               attr_count,
                                      const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 meg_id = 0;
    const sai_attribute_value_t *attr_value;
    uint32 index = 0;
    sai_object_id_t meg_obj_id = 0;
    ctc_oam_maid_t oam_maid;
    ctc_sai_y1731_meg_t* p_y1731_meg_info = NULL; 

    sal_memset(&oam_maid, 0, sizeof(ctc_oam_maid_t));

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_PTR_VALID_CHECK(sai_y1731_meg_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_y1731_meg_create_attr_check(lchip, attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_MEG, &meg_id), status, out);
    
    meg_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_Y1731_MEG, lchip, 0, 0, meg_id);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "create meg_obj_id = 0x%"PRIx64"\n", meg_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_y1731_meg_build_db(lchip, meg_obj_id, &p_y1731_meg_info), status, error1);
    
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        p_y1731_meg_info->meg_type = attr_value->s32;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_NAME, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        sal_memcpy(p_y1731_meg_info->meg_name, attr_value->chardata, SAI_Y1731_MEG_NAME_SIZE);
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_MEG_ATTR_LEVEL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        p_y1731_meg_info->level = attr_value->u8;
    }

    _ctc_sai_y1731_build_maid(p_y1731_meg_info->meg_type, p_y1731_meg_info->meg_name, &oam_maid);
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_add_maid(lchip, &oam_maid), status, error2);

    *sai_y1731_meg_id = meg_obj_id;

    goto out;

error2:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error2\n");
    _ctc_sai_y1731_remove_db(lchip, meg_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_MEG, meg_id);    

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t ctc_sai_y1731_remove_y1731_meg( sai_object_id_t sai_y1731_meg_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 meg_id = 0;
    ctc_sai_y1731_meg_t* p_y1731_meg_info = NULL; 
    ctc_oam_maid_t oam_maid;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_meg_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_LOG_INFO(SAI_API_Y1731, "remove sai_y1731_meg_id = %llu\n", sai_y1731_meg_id);
    
    p_y1731_meg_info = ctc_sai_db_get_object_property(lchip, sai_y1731_meg_id);
    if (NULL == p_y1731_meg_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to remove y1731 meg, invalid sai_y1731_meg_id %d!\n", sai_y1731_meg_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    
    _ctc_sai_y1731_build_maid(p_y1731_meg_info->meg_type, p_y1731_meg_info->meg_name, &oam_maid);
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_remove_maid(lchip, &oam_maid), status, out);    
    
    ctc_sai_oid_get_value(sai_y1731_meg_id, &meg_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_MEG, meg_id);
    
    _ctc_sai_y1731_remove_db(lchip, sai_y1731_meg_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t ctc_sai_y1731_set_y1731_meg_attribute( sai_object_id_t sai_y1731_meg_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_y1731_meg_id };
    sai_status_t           status = SAI_STATUS_SUCCESS;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_meg_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_Y1731_MEG,  y1731_meg_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 meg attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_y1731_get_y1731_meg_attribute( 
    sai_object_id_t sai_y1731_meg_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_y1731_meg_id
    }
    ;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_meg_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_Y1731_MEG, loop, y1731_meg_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 meg attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}
    
sai_status_t ctc_sai_y1731_create_y1731_session( sai_object_id_t *sai_y1731_session_id,
                                      sai_object_id_t        switch_id,
                                      uint32_t               attr_count,
                                      const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value;
    uint32 index = 0;
    uint32 session_id = 0;
    sai_object_id_t session_obj_id = 0;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    ctc_sai_y1731_meg_t* p_y1731_meg_info = NULL;
    ctc_oam_lmep_t oam_lmep;
    ctc_oam_key_t oam_key;
    uint8 need_update_en = 0;
    ctc_oam_update_t update_lmep;    
    ctc_object_id_t ctc_object_id;

    sal_memset(&oam_lmep, 0, sizeof(ctc_oam_lmep_t));
    sal_memset(&oam_key, 0, sizeof(ctc_oam_key_t));
    sal_memset(&update_lmep, 0, sizeof(ctc_oam_update_t));

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    
    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_PTR_VALID_CHECK(sai_y1731_session_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_y1731_session_create_attr_check(lchip, attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_SESSION, &session_id), status, out);
    
    session_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_Y1731_SESSION, lchip, 0, 0, session_id);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "create session_obj_id = 0x%"PRIx64"\n", session_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_y1731_session_build_db(lchip, session_obj_id, &p_y1731_session_info), status, error1);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_MEG, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_y1731_meg_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_y1731_meg_info)
        {
            CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 meg, invalid sai_y1731_meg_id %d!\n", attr_value->oid);
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error2;
        }
        else
        {
            _ctc_sai_y1731_build_maid(p_y1731_meg_info->meg_type, p_y1731_meg_info->meg_name, &oam_lmep.maid);

            oam_key.mep_type = oam_lmep.maid.mep_type;

            p_y1731_session_info->meg_oid = attr_value->oid;
            p_y1731_session_info->meg_type = p_y1731_meg_info->meg_type;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_DIR, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if(SAI_Y1731_SESSION_DIR_UPMEP == attr_value->s32)
        {
            oam_key.flag |= CTC_OAM_KEY_FLAG_UP_MEP;
        }

        p_y1731_session_info->dir = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_VLAN_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if((SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_meg_info->meg_type)
            || (SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_meg_info->meg_type))
        {
            oam_key.u.eth.vlan_id = attr_value->u32;
        }        
    }
    else
    {
        if( SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_session_info->meg_type)
        {
            oam_key.flag |= CTC_OAM_KEY_FLAG_LINK_SECTION_OAM;
            p_y1731_session_info->is_link_oam = 1;
        }        
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_BRIDGE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if(SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_session_info->meg_type)
        {
            /* get fid from 1.D bridge */
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, attr_value->oid, &ctc_object_id);
            if(SAI_BRIDGE_TYPE_1D != ctc_object_id.sub_type)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                goto error2;
            }
            /*FID */
            oam_key.u.eth.l2vpn_oam_id = ctc_object_id.value;
        }
        else if(SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_session_info->meg_type)
        {
            /* get fid from 1.D bridge */
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, attr_value->oid, &ctc_object_id);
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != ctc_object_id.sub_type)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                goto error2;
            }
            /*FID */
            oam_key.u.eth.l2vpn_oam_id = ctc_object_id.value;
        }
        p_y1731_session_info->bridge_id = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_PORT_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if(( SAI_Y1731_MEG_TYPE_ETHER_VLAN == p_y1731_session_info->meg_type)
            || ( SAI_Y1731_MEG_TYPE_L2VPN_VLAN == p_y1731_session_info->meg_type)
            || ( SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_session_info->meg_type)
            || ( SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_session_info->meg_type))
        {
            ctc_sai_oid_get_gport(attr_value->oid, &oam_key.u.eth.gport);
            oam_key.u.eth.md_level = p_y1731_meg_info->level;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
        {
            oam_key.u.tp.label = attr_value->u32;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
        {
            ctc_sai_oid_get_value(attr_value->oid, &oam_key.u.tp.gport_or_l3if_id);

            p_y1731_session_info->tp_rif_oid = attr_value->oid;
            
            oam_key.flag |= CTC_OAM_KEY_FLAG_LINK_SECTION_OAM;
            p_y1731_session_info->is_link_oam = 1;
        }
    }

    if( SAI_Y1731_MEG_TYPE_L2VPN_VPLS == p_y1731_session_info->meg_type)
    {
        oam_key.flag |= CTC_OAM_KEY_FLAG_L2VPN;
        oam_key.flag |= CTC_OAM_KEY_FLAG_VPLS;
    }
    else if( SAI_Y1731_MEG_TYPE_L2VPN_VPWS == p_y1731_session_info->meg_type)
    {
        oam_key.flag |= CTC_OAM_KEY_FLAG_L2VPN;
        oam_key.flag &=( ~CTC_OAM_KEY_FLAG_VPLS);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        oam_lmep.u.y1731_lmep.mep_id = attr_value->u32;
        p_y1731_session_info->lmep_id = attr_value->u32;
    }

    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_CCM_PERIOD, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        /* ccminterval 1-7 refer to 3.3ms/10ms/100ms/1s/10s/1min/10min */
        oam_lmep.u.y1731_lmep.ccm_interval = attr_value->s32;
        p_y1731_session_info->ccm_period = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_CCM_ENABLE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        /* need update ccm en */
        p_y1731_session_info->ccm_en = attr_value->booldata;
        need_update_en = 1;
    }

    //status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_IS_P2P_MODE, &attr_value, &index);
    //if (!CTC_SAI_ERROR(status))
    //{
    //    oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_P2P_MODE;
    //    p_y1731_session_info->is_p2p_mode = attr_value->booldata;
    //}

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_y1731_session_info->lm_offload_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_LM_ENABLE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if(attr_value->booldata)
        {
            oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_LM_EN;
        }
        p_y1731_session_info->lm_en = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_LM_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if(SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED == attr_value->s32)
        {
            oam_lmep.u.y1731_lmep.lm_type = CTC_OAM_LM_TYPE_DUAL;
        }
        else
        {
            oam_lmep.u.y1731_lmep.lm_type = CTC_OAM_LM_TYPE_SINGLE;
        }
        
        p_y1731_session_info->lm_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_y1731_session_info->dm_offload_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_DM_ENABLE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        if(attr_value->booldata)
        {
            oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_DM_EN;
        }
        p_y1731_session_info->dm_en = attr_value->booldata;
    }

    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if(attr_value->booldata)
        {
            oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_WITHOUT_GAL;
        }
        p_y1731_session_info->without_gal = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_TTL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        oam_lmep.u.y1731_lmep.mpls_ttl = attr_value->u8;
        p_y1731_session_info->mpls_ttl = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_EXP_OR_COS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        oam_lmep.u.y1731_lmep.tx_cos_exp = attr_value->u8;
        p_y1731_session_info->exp_or_cos = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, attr_value->oid, &ctc_object_id);
        if( SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
        {
            p_y1731_session_info->nh_oid = attr_value->oid;
            oam_lmep.u.y1731_lmep.nhid = ctc_object_id.value;
        }
        else if( SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
        {
            //TODO
        }
        else
        {
            //ERROR, checked in _ctc_sai_y1731_session_create_attr_check
        }
    }

    //Only TP use p2p mode
    if( SAI_Y1731_MEG_TYPE_MPLS_TP == p_y1731_session_info->meg_type)
    {
        oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_P2P_MODE;
    }    
    
    oam_lmep.u.y1731_lmep.flag |= CTC_OAM_Y1731_LMEP_FLAG_MEP_EN;
    oam_lmep.u.y1731_lmep.tpid_index = CTC_PARSER_L2_TPID_SVLAN_TPID_0;
    sal_memcpy(&oam_lmep.key, &oam_key, sizeof(ctc_oam_key_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_add_lmep(lchip, &oam_lmep), status, error2);
    
    p_y1731_session_info->lmep_index = oam_lmep.lmep_index;
    
    if(need_update_en)
    {        
        sal_memcpy(&update_lmep.key, &oam_key, sizeof(ctc_oam_key_t));
        update_lmep.update_type = CTC_OAM_Y1731_LMEP_UPDATE_TYPE_CCM_EN;
        update_lmep.update_value = p_y1731_session_info->ccm_en;
        update_lmep.is_local = 1;
        
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, error3);
    }
    
    sal_memcpy(&p_y1731_session_info->oam_key, &oam_key, sizeof(ctc_oam_key_t));
    
    p_y1731_session_info->rmep_head = ctc_slist_new();
    if (!p_y1731_session_info->rmep_head)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }

    *sai_y1731_session_id = session_obj_id;

    goto out;
    
error3:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error3\n");
    ctcs_oam_remove_lmep(lchip, &oam_lmep);
error2:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error2\n");
    _ctc_sai_y1731_remove_db(lchip, session_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_SESSION, session_id);   
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t ctc_sai_y1731_remove_y1731_session(sai_object_id_t sai_y1731_session_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_oam_lmep_t lmep;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    uint32 session_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_session_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "sai_y1731_session_id = %llu\n", sai_y1731_session_id);

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, sai_y1731_session_id);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to remove y1731 session, invalid sai_y1731_session_id %d!\n", sai_y1731_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if(p_y1731_session_info->rmep_head && p_y1731_session_info->rmep_head->count)
    {
        /* should clear rmep all first */
        status = SAI_STATUS_FAILURE;
        goto out;
    }
    sal_memcpy(&lmep.key, &p_y1731_session_info->oam_key, sizeof(ctc_oam_key_t));

    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_remove_lmep(lchip, &lmep), status, out);
    
    ctc_sai_oid_get_value(sai_y1731_session_id, &session_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_SESSION, session_id);

    mem_free(p_y1731_session_info->rmep_head);
    
    _ctc_sai_y1731_remove_db(lchip, sai_y1731_session_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t ctc_sai_y1731_set_y1731_session_attribute( sai_object_id_t sai_y1731_session_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_y1731_session_id };
    sai_status_t           status = SAI_STATUS_SUCCESS;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_Y1731_SESSION,  y1731_session_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 session attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_y1731_get_y1731_session_attribute( 
    sai_object_id_t sai_y1731_session_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_y1731_session_id
    }
    ;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_Y1731_MEG, loop, y1731_session_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 session attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}

sai_status_t ctc_sai_y1731_create_y1731_remote_mep( sai_object_id_t *sai_y1731_rmep_id,
                                      sai_object_id_t        switch_id,
                                      uint32_t               attr_count,
                                      const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value;
    uint32 index = 0;
    uint32 session_id = 0;
    sai_object_id_t rmep_obj_id = 0;
    ctc_sai_y1731_rmep_t* p_y1731_rmep_info = NULL;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    ctc_oam_rmep_t oam_rmep;
    ctc_slistnode_t *node = NULL;
    ctc_sai_y1731_rmep_id_t *p_rmep_node_data = NULL;
    ctc_sai_y1731_rmep_id_t *p_rmep_node = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_PTR_VALID_CHECK(sai_y1731_rmep_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_y1731_rmep_create_attr_check(lchip, attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP, &session_id), status, out);
    
    rmep_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_Y1731_REMOTE_MEP, lchip, 0, 0, session_id);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "create rmep_obj_id = 0x%"PRIx64"\n", rmep_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_y1731_rmep_build_db(lchip, rmep_obj_id, &p_y1731_rmep_info), status, error1);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        /*checked in _ctc_sai_y1731_rmep_create_attr_check */
        p_y1731_session_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);

        p_y1731_rmep_info->y1731_session_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        oam_rmep.u.y1731_rmep.rmep_id = attr_value->u32;
        p_y1731_rmep_info->rmep_id = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&oam_rmep.u.y1731_rmep.rmep_mac, &attr_value->mac, sizeof(sai_mac_t));
    }

    sal_memcpy(&oam_rmep.key, &p_y1731_session_info->oam_key, sizeof(ctc_oam_key_t));
    oam_rmep.u.y1731_rmep.flag |= CTC_OAM_Y1731_RMEP_FLAG_MEP_EN;
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_add_rmep(lchip, &oam_rmep), status, error2);

    p_y1731_rmep_info->rmep_index = oam_rmep.rmep_index;
    
    /* add rmep into session list */
    CTC_SLIST_LOOP(p_y1731_session_info->rmep_head, node)
    {
        p_rmep_node_data = _ctc_container_of(node, ctc_sai_y1731_rmep_id_t, node);
        if (p_y1731_rmep_info->y1731_session_oid == p_rmep_node_data->rmep_oid)
        {
            status = SAI_STATUS_ITEM_ALREADY_EXISTS;
            goto error3;
        }        
    }

    p_rmep_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_y1731_rmep_id_t));
    if (!p_rmep_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    p_rmep_node->rmep_oid = rmep_obj_id;
    ctc_slist_add_tail(p_y1731_session_info->rmep_head, &(p_rmep_node->node));

    *sai_y1731_rmep_id = rmep_obj_id;

    goto out;

error3:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error3\n");
    ctcs_oam_remove_rmep(lchip, &oam_rmep);        
error2:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error2\n");
    _ctc_sai_y1731_remove_db(lchip, rmep_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_Y1731, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP, session_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t ctc_sai_y1731_remove_y1731_remote_mep( sai_object_id_t sai_y1731_rmep_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_oam_rmep_t rmep;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    ctc_sai_y1731_rmep_t* p_y1731_rmep_info = NULL;
    uint32 session_id = 0;    
    ctc_slistnode_t *node = NULL;
    ctc_sai_y1731_rmep_id_t *p_rmep_node = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_rmep_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_LOG_INFO(SAI_API_Y1731, "sai_y1731_rmep_id = %llu\n", sai_y1731_rmep_id);

    p_y1731_rmep_info = ctc_sai_db_get_object_property(lchip, sai_y1731_rmep_id);
    if (NULL == p_y1731_rmep_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to remove y1731 rmep, invalid sai_y1731_rmep_id %d!\n", sai_y1731_rmep_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, p_y1731_rmep_info->y1731_session_oid);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to remove y1731 rmep, invalid sai_y1731_session_id %d!\n", p_y1731_rmep_info->y1731_session_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    sal_memcpy(&rmep.key, &p_y1731_session_info->oam_key, sizeof(ctc_oam_key_t));
    rmep.u.y1731_rmep.rmep_id = p_y1731_rmep_info->rmep_id;

    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_remove_rmep(lchip, &rmep), status, out);

    /* del from session list */
    CTC_SLIST_LOOP(p_y1731_session_info->rmep_head, node)
    {
        p_rmep_node = _ctc_container_of(node, ctc_sai_y1731_rmep_id_t, node);        

        if (sai_y1731_rmep_id == p_rmep_node->rmep_oid)
        {
            ctc_slist_delete_node(p_y1731_session_info->rmep_head, node);
            mem_free(p_rmep_node);
            break;
        }
    }
    
    ctc_sai_oid_get_value(sai_y1731_rmep_id, &session_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP, session_id);
    
    _ctc_sai_y1731_remove_db(lchip, sai_y1731_rmep_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;    
}

static sai_status_t ctc_sai_y1731_set_y1731_remote_mep_attribute( sai_object_id_t sai_y1731_rmep_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_y1731_rmep_id };
    sai_status_t           status = SAI_STATUS_SUCCESS;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_rmep_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_Y1731_REMOTE_MEP,  y1731_rmep_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to set y1731 remote mep attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_y1731_get_y1731_remote_mep_attribute( 
    sai_object_id_t sai_y1731_rmep_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_y1731_rmep_id
    }
    ;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_Y1731);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_rmep_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_Y1731_REMOTE_MEP, loop, y1731_rmep_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 remote mep attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}    

static sai_status_t ctc_sai_y1731_get_y1731_session_lm_stats( sai_object_id_t sai_y1731_session_id,
                                                uint32_t               number_of_stats,
                                                const sai_stat_id_t *lm_stats_ids,
                                                uint64_t             *stats)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_oam_stats_info_t stat_info;
    ctc_sai_y1731_session_t* p_y1731_session_info = NULL;
    uint32 loop_i = 0;

    sal_memset(&stat_info, 0, sizeof(stat_info));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_y1731_session_id, &lchip));
    
    p_y1731_session_info = ctc_sai_db_get_object_property(lchip, sai_y1731_session_id);
    if (NULL == p_y1731_session_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_Y1731, "Failed to get y1731 lm stats, invalid sai_y1731_session_id %d!\n", sai_y1731_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
        
    sal_memcpy(&stat_info.key, &p_y1731_session_info->oam_key, sizeof(ctc_oam_key_t));

    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_stats(lchip, &stat_info), status, out);

    if (((stat_info.lm_type == CTC_OAM_LM_TYPE_NONE)
        || (stat_info.lm_type == CTC_OAM_LM_TYPE_SINGLE))
        || (CTC_OAM_LM_COS_TYPE_ALL_COS != stat_info.lm_cos_type))
    {
        status = SAI_STATUS_FAILURE;
        goto out;
    }

    for(loop_i = 0;loop_i < number_of_stats;loop_i++)
    {
        if(SAI_Y1731_SESSION_LM_STAT_TX_FCF == lm_stats_ids[loop_i])
        {
            stats[loop_i] = stat_info.lm_info[0].tx_fcf;
        }
        else if(SAI_Y1731_SESSION_LM_STAT_RX_FCB == lm_stats_ids[loop_i])
        {
            stats[loop_i] = stat_info.lm_info[0].rx_fcb;
        }
        else if(SAI_Y1731_SESSION_LM_STAT_TX_FCB == lm_stats_ids[loop_i])
        {
            stats[loop_i] = stat_info.lm_info[0].tx_fcb;
        }
        else /* SAI_Y1731_SESSION_LM_STAT_RX_FCL */
        {
            stats[loop_i] = stat_info.lm_info[0].rx_fcl;
        }
        CTC_SAI_LOG_INFO(SAI_API_Y1731, "stats[%d] = %llu\n", loop_i, stats[loop_i]);
    }

out:    
    return status;
}



const sai_y1731_api_t ctc_sai_y1731_api = {
    ctc_sai_y1731_create_y1731_meg,
    ctc_sai_y1731_remove_y1731_meg,
    ctc_sai_y1731_set_y1731_meg_attribute,
    ctc_sai_y1731_get_y1731_meg_attribute,

    ctc_sai_y1731_create_y1731_session,
    ctc_sai_y1731_remove_y1731_session,
    ctc_sai_y1731_set_y1731_session_attribute,
    ctc_sai_y1731_get_y1731_session_attribute,

    ctc_sai_y1731_create_y1731_remote_mep,
    ctc_sai_y1731_remove_y1731_remote_mep,
    ctc_sai_y1731_set_y1731_remote_mep_attribute,
    ctc_sai_y1731_get_y1731_remote_mep_attribute,

    ctc_sai_y1731_get_y1731_session_lm_stats,
};

sai_status_t
ctc_sai_y1731_db_init(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    
    ctc_sai_db_wb_t wb_info;
    
    sal_memset(&wb_info, 0, sizeof(wb_info));    
    wb_info.version = SYS_WB_VERSION_Y1731;
    wb_info.data_len = sizeof(ctc_sai_y1731_meg_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_y1731_meg_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_Y1731_MEG, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));    
    wb_info.version = SYS_WB_VERSION_Y1731;
    wb_info.data_len = sizeof(ctc_sai_y1731_session_t);
    wb_info.wb_sync_cb = _ctc_sai_y1731_session_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_y1731_session_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_y1731_session_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_Y1731_SESSION, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));    
    wb_info.version = SYS_WB_VERSION_Y1731;
    wb_info.data_len = sizeof(ctc_sai_y1731_rmep_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_y1731_rmep_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_Y1731_REMOTE_MEP, (void*)(&wb_info));
               
    return status;
}

sai_status_t
ctc_sai_y1731_db_deinit(uint8 lchip)
{
     ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_Y1731_SESSION, (hash_traversal_fn)_ctc_sai_y1731_session_db_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_y1731_api_init()
{
    ctc_sai_register_module_api(SAI_API_Y1731, (void*)&ctc_sai_y1731_api);

    return SAI_STATUS_SUCCESS;
}

