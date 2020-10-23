/**
 @file ctc_sai_acl.c

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-01-23

 @version v1.0
*/

/*ctc_sai include file*/
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_samplepacket.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_udf.h"

/*sdk include file*/
#include "ctcs_api.h"

/* be consistent with sai acl key supported actually */
#define CTC_SAI_ACL_KEY_NUM            (CTC_ACL_KEY_UDF+1)
#define SAI_ACL_ATTR_ID2INDEX(ATTR_ID) ((ATTR_ID) <= SAI_ACL_TABLE_ATTR_FIELD_END)    \
                                       ? ((ATTR_ID) - SAI_ACL_TABLE_ATTR_FIELD_START) \
                                       : ((SAI_ACL_TABLE_ATTR_FIELD_END - SAI_ACL_TABLE_ATTR_FIELD_START + 1) + ((ATTR_ID) - SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START))
#define SAI_ACL_ATTR_IS_KEY(ATTR_ID)   ((((ATTR_ID) >= SAI_ACL_TABLE_ATTR_FIELD_START) && ((ATTR_ID) <= SAI_ACL_TABLE_ATTR_FIELD_END)) || ((ATTR_ID) == SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID))

struct acl_table_group_oid_info_s
{
    uint32 count;
    sai_object_id_t group_oid;
    sai_object_id_t *group_member_oid_list;
};
typedef struct acl_table_group_oid_info_s acl_table_group_oid_info_t;

/* for warmboot use */
struct ctc_sai_acl_table_group_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl table group oid */
    sai_object_id_t table_id;
    uint32 calc_key_len[0];

    /*data*/
    uint16 members_prio;
};
typedef struct ctc_sai_acl_table_group_wb_s ctc_sai_acl_table_group_wb_t;

struct ctc_sai_acl_bind_point_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl table group oid */
    sai_object_id_t bind_index;
    uint32 calc_key_len[0];

    /*data*/
    uint8 bind_type;
};
typedef struct ctc_sai_acl_bind_point_wb_s ctc_sai_acl_bind_point_wb_t;

struct ctc_sai_acl_table_member_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl table */
    sai_object_id_t entry_id;
    uint32 calc_key_len[0];

    /*data*/
    uint16 priority;
};
typedef struct ctc_sai_acl_table_member_wb_s ctc_sai_acl_table_member_wb_t;

struct ctc_sai_acl_table_group_list_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl table */
    sai_object_id_t group_id;
    uint32 calc_key_len[0];

};
typedef struct ctc_sai_acl_table_group_list_wb_s ctc_sai_acl_table_group_list_wb_t;

struct ctc_sai_acl_entry_key_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl entry */
    uint32 index;
    uint32 calc_key_len[0];

    sai_attribute_t key;
};
typedef struct ctc_sai_acl_entry_key_wb_s ctc_sai_acl_entry_key_wb_t;

struct ctc_sai_acl_entry_action_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl entry */
    uint32 index;
    uint32 calc_key_len[0];

    sai_attribute_t action;
};
typedef struct ctc_sai_acl_entry_action_wb_s ctc_sai_acl_entry_action_wb_t;

struct ctc_sai_acl_range_wb_s
{
    /*key*/
    sai_object_id_t oid;/* acl entry */
    uint32 calc_key_len[0];

    uint8  stage;
    uint8  group_id;
    uint8  range_type;
    uint16 range_min;
    uint16 range_max;
    uint32 ref_cnt;
};
typedef struct ctc_sai_acl_range_wb_s ctc_sai_acl_range_wb_t;

struct ctc_sai_ctc_key_info_s
{
    uint32 type2key[CTC_ACL_TCAM_LKUP_TYPE_MAX];
    uint32 attr2field[SAI_ACL_KEY_ATTR_NUM][(CTC_FIELD_KEY_NUM-1)/32 + 1];
    uint32 key2field[CTC_SAI_ACL_KEY_NUM][(CTC_FIELD_KEY_NUM-1)/32 + 1];
    uint8  field2packet[CTC_FIELD_KEY_NUM];
    uint8  key2packet[CTC_SAI_ACL_KEY_NUM];
};
typedef struct ctc_sai_ctc_key_info_s ctc_sai_key_info_t;

static ctc_sai_key_info_t ctc_sai_key_info;

#define ________WARMBOOT_PROCESS________

static sai_status_t
_ctc_sai_acl_group_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t ret = 0;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_wb_data_t wb_data;
    ctc_slistnode_t *table_node = NULL;
    ctc_slistnode_t *bind_node = NULL;
    ctc_sai_acl_group_member_t *p_acl_group_member = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;
    sai_object_id_t acl_table_group_id = *(sai_object_id_t*)key;
    ctc_sai_acl_group_t* p_acl_table_group = (ctc_sai_acl_group_t*)data;
    ctc_sai_acl_table_group_wb_t wb_acl_table_group;
    ctc_sai_acl_bind_point_wb_t wb_acl_bind_point;

    sal_memset(&wb_acl_table_group, 0, sizeof(ctc_sai_acl_table_group_wb_t));
    sal_memset(&wb_acl_bind_point, 0, sizeof(ctc_sai_acl_bind_point_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_table_group_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_MEMBER);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_acl_table_group->member_list, table_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_acl_group_member = (ctc_sai_acl_group_member_t*)table_node;
        wb_acl_table_group.oid = acl_table_group_id;
        wb_acl_table_group.members_prio = p_acl_group_member->members_prio;
        wb_acl_table_group.table_id = p_acl_group_member->table_id;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_table_group, (wb_data.key_len + wb_data.data_len));

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

    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_bind_point_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_BIND_POINT_GROUP);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_acl_table_group->bind_points, bind_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
        wb_acl_bind_point.oid = acl_table_group_id;
        wb_acl_bind_point.bind_type = p_bind_point->bind_type;
        wb_acl_bind_point.bind_index = p_bind_point->bind_index;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_bind_point, (wb_data.key_len + wb_data.data_len));

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
_ctc_sai_acl_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_table_group_id = *(sai_object_id_t*)key;
    ctc_sai_acl_group_t* p_acl_table_group = (ctc_sai_acl_group_t*)data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_group_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX, ctc_object_id.value));

    p_acl_table_group->member_list = ctc_slist_new();
    p_acl_table_group->bind_points = ctc_slist_new();

    if ((NULL == p_acl_table_group->member_list) || (NULL == p_acl_table_group->bind_points))
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_group_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_acl_table_group_wb_t wb_acl_table_group;
    ctc_sai_acl_bind_point_wb_t wb_acl_bind_point;
    ctc_sai_acl_group_t *p_acl_table_group = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;

    sal_memset(&wb_acl_table_group, 0, sizeof(ctc_sai_acl_table_group_wb_t));
    sal_memset(&wb_acl_bind_point, 0, sizeof(ctc_sai_acl_bind_point_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_table_group_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_MEMBER);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_table_group, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_table_group_wb_t));
        p_acl_table_group = ctc_sai_db_get_object_property(lchip, wb_acl_table_group.oid);
        if (!p_acl_table_group)
        {
            continue;
        }

        p_group_member = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_acl_group_member_t));
        if (!p_group_member)
        {
            continue;
        }
        p_group_member->table_id = wb_acl_table_group.table_id;
        p_group_member->members_prio = wb_acl_table_group.members_prio;
        ctc_slist_add_tail(p_acl_table_group->member_list, &(p_group_member->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_bind_point_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_BIND_POINT_GROUP);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_bind_point, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_bind_point_wb_t));
        p_acl_table_group = ctc_sai_db_get_object_property(lchip, wb_acl_bind_point.oid);
        if (!p_acl_table_group)
        {
            continue;
        }

        p_bind_point = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_acl_bind_point_info_t));
        if (!p_bind_point)
        {
            continue;
        }
        p_bind_point->bind_type = wb_acl_bind_point.bind_type;
        p_bind_point->bind_index = wb_acl_bind_point.bind_index;
        ctc_slist_add_tail(p_acl_table_group->bind_points, &(p_bind_point->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
 }

static sai_status_t
_ctc_sai_acl_table_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t ret = 0;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_wb_data_t wb_data;
    ctc_slistnode_t *entry_node = NULL;
    ctc_slistnode_t *bind_node = NULL;
    ctc_slistnode_t *group_node = NULL;
    ctc_sai_acl_table_member_t *p_acl_table_member = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;
    ctc_sai_acl_table_group_list_t *p_table_group_list = NULL;
    sai_object_id_t acl_table_id = *(sai_object_id_t*)key;
    ctc_sai_acl_table_t* p_acl_table = (ctc_sai_acl_table_t*)data;
    ctc_sai_acl_table_member_wb_t wb_acl_table_member;
    ctc_sai_acl_bind_point_wb_t wb_acl_bind_point;
    ctc_sai_acl_table_group_list_wb_t wb_acl_table_group_list;

    sal_memset(&wb_acl_table_member, 0, sizeof(ctc_sai_acl_table_member_wb_t));
    sal_memset(&wb_acl_bind_point, 0, sizeof(ctc_sai_acl_bind_point_wb_t));
    sal_memset(&wb_acl_table_group_list, 0, sizeof(ctc_sai_acl_table_group_list_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_table_member_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_MEMBER);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_acl_table_member = (ctc_sai_acl_table_member_t*)entry_node;
        wb_acl_table_member.oid = acl_table_id;
        wb_acl_table_member.entry_id = p_acl_table_member->entry_id;
        wb_acl_table_member.priority = p_acl_table_member->priority;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_table_member, (wb_data.key_len + wb_data.data_len));

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

    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_bind_point_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_BIND_POINT_TABLE);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_acl_table->bind_points, bind_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
        wb_acl_bind_point.oid = acl_table_id;
        wb_acl_bind_point.bind_type = p_bind_point->bind_type;
        wb_acl_bind_point.bind_index = p_bind_point->bind_index;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_bind_point, (wb_data.key_len + wb_data.data_len));

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

    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_table_group_list_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_LIST);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_acl_table->group_list, group_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_table_group_list = (ctc_sai_acl_table_group_list_t*)group_node;
        wb_acl_table_group_list.oid = acl_table_id;
        wb_acl_table_group_list.group_id = p_table_group_list->group_id;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_table_group_list, (wb_data.key_len + wb_data.data_len));

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
_ctc_sai_acl_table_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_table_id = *(sai_object_id_t*)key;
    ctc_sai_acl_table_t *p_acl_table = (ctc_sai_acl_table_t*)data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX, ctc_object_id.value));

    p_acl_table->entry_list = ctc_slist_new();
    p_acl_table->bind_points = ctc_slist_new();
    p_acl_table->group_list = ctc_slist_new();

    if ((NULL == p_acl_table->entry_list) || (NULL == p_acl_table->bind_points) || (NULL == p_acl_table->group_list))
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_table_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_acl_table_member_wb_t wb_acl_table_member;
    ctc_sai_acl_bind_point_wb_t wb_acl_bind_point;
    ctc_sai_acl_table_group_list_wb_t wb_acl_table_group_list;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_table_member_t *p_table_member = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;
    ctc_sai_acl_table_group_list_t *p_acl_table_group_list = NULL;

    sal_memset(&wb_acl_table_member, 0, sizeof(ctc_sai_acl_table_member_wb_t));
    sal_memset(&wb_acl_bind_point, 0, sizeof(ctc_sai_acl_bind_point_wb_t));
    sal_memset(&wb_acl_table_group_list, 0, sizeof(ctc_sai_acl_table_group_list_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_table_member_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_MEMBER);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_table_member, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_table_member_wb_t));
        p_acl_table = ctc_sai_db_get_object_property(lchip, wb_acl_table_member.oid);
        if (!p_acl_table)
        {
            continue;
        }

        p_table_member = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_acl_table_member_t));
        if (!p_table_member)
        {
            continue;
        }
        p_table_member->entry_id = wb_acl_table_member.entry_id;
        p_table_member->priority = wb_acl_table_member.priority;
        ctc_slist_add_tail(p_acl_table->entry_list, &(p_table_member->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_bind_point_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_BIND_POINT_TABLE);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_bind_point, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_bind_point_wb_t));
        p_acl_table = ctc_sai_db_get_object_property(lchip, wb_acl_bind_point.oid);
        if (!p_acl_table)
        {
            continue;
        }

        p_bind_point = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_acl_bind_point_info_t));
        if (!p_bind_point)
        {
            continue;
        }
        p_bind_point->bind_type = wb_acl_bind_point.bind_type;
        p_bind_point->bind_index = wb_acl_bind_point.bind_index;
        ctc_slist_add_tail(p_acl_table->bind_points, &(p_bind_point->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_table_group_list_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_LIST);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_table_group_list, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_table_group_list_wb_t));
        p_acl_table = ctc_sai_db_get_object_property(lchip, wb_acl_table_group_list.oid);
        if (!p_acl_table)
        {
            continue;
        }

        p_acl_table_group_list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_acl_table_group_list_t));
        if (!p_acl_table_group_list)
        {
            continue;
        }
        p_acl_table_group_list->group_id = wb_acl_table_group_list.group_id;
        ctc_slist_add_tail(p_acl_table->group_list, &(p_acl_table_group_list->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_acl_entry_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t ret = 0;
    uint32 loop = 0;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_wb_data_t wb_data;
    sai_object_id_t acl_entry_id = *(sai_object_id_t*)key;
    ctc_sai_acl_entry_t *p_acl_entry = (ctc_sai_acl_entry_t*)data;
    ctc_sai_acl_entry_key_wb_t wb_acl_entry_key;
    ctc_sai_acl_entry_action_wb_t wb_acl_entry_action;

    sal_memset(&wb_acl_entry_key, 0, sizeof(ctc_sai_acl_entry_key_wb_t));
    sal_memset(&wb_acl_entry_action, 0, sizeof(ctc_sai_acl_entry_action_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_entry_key_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_KEY);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    for (loop = 0; loop < SAI_ACL_KEY_ATTR_NUM; loop++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_acl_entry_key.oid = acl_entry_id;
        wb_acl_entry_key.index = loop;
        sal_memcpy(&wb_acl_entry_key.key, &p_acl_entry->key_attr_list[loop], sizeof(sai_attribute_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_entry_key, (wb_data.key_len + wb_data.data_len));

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

    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_entry_action_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_ACTION);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    for (loop = 0; loop < SAI_ACL_ACTION_ATTR_NUM; loop++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_acl_entry_action.oid = acl_entry_id;
        wb_acl_entry_action.index = loop;
        sal_memcpy(&wb_acl_entry_action.action, &p_acl_entry->action_attr_list[loop], sizeof(sai_attribute_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_entry_action, (wb_data.key_len + wb_data.data_len));

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
_ctc_sai_acl_entry_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_entry_id = *(sai_object_id_t*)key;
    ctc_sai_acl_entry_t* p_acl_entry = (ctc_sai_acl_entry_t*)data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_entry_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, ctc_object_id.value));

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_entry->key_attr_list, SAI_ACL_KEY_ATTR_NUM * sizeof(sai_attribute_t));
    if (NULL == p_acl_entry->key_attr_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_entry->action_attr_list, SAI_ACL_ACTION_ATTR_NUM * sizeof(sai_attribute_t));
    if (NULL == p_acl_entry->action_attr_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_acl_entry_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_acl_entry_key_wb_t wb_acl_entry_key;
    ctc_sai_acl_entry_action_wb_t wb_acl_entry_action;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;

    sal_memset(&wb_acl_entry_key, 0, sizeof(ctc_sai_acl_entry_key_wb_t));
    sal_memset(&wb_acl_entry_action, 0, sizeof(ctc_sai_acl_entry_action_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_entry_key_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_KEY);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_entry_key, (uint8*)(wb_query.buffer) + offset,  (wb_query.key_len + wb_query.data_len));
        p_acl_entry = ctc_sai_db_get_object_property(lchip, wb_acl_entry_key.oid);
        if ((NULL == p_acl_entry) || (NULL == p_acl_entry->key_attr_list))
        {
            continue;
        }
        sal_memcpy(&(p_acl_entry->key_attr_list[wb_acl_entry_key.index]), &wb_acl_entry_key.key,  sizeof(sai_attribute_t));
        CTC_WB_QUERY_ENTRY_END((&wb_query));

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_entry_action_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_ACTION);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_entry_action, (uint8*)(wb_query.buffer) + offset,  (wb_query.key_len + wb_query.data_len));
        p_acl_entry = ctc_sai_db_get_object_property(lchip, wb_acl_entry_action.oid);
        if ((NULL == p_acl_entry) || (NULL == p_acl_entry->action_attr_list))
        {
            continue;
        }
        sal_memcpy(&(p_acl_entry->action_attr_list[wb_acl_entry_action.index]), &wb_acl_entry_action.action,  sizeof(sai_attribute_t));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
 }

static sai_status_t
_ctc_sai_acl_table_group_member_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_table_group_member_id = *(sai_object_id_t*)key;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_group_member_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_range_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t ret = 0;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_wb_data_t wb_data;
    sai_object_id_t range_id = *(sai_object_id_t*)key;
    ctc_sai_acl_range_t* p_acl_range = (ctc_sai_acl_range_t*)data;
    ctc_sai_acl_range_wb_t wb_acl_range;

    sal_memset(&wb_acl_range, 0, sizeof(ctc_sai_acl_range_wb_t));
    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_acl_range_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_RANGE);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
    wb_acl_range.oid = range_id;
    wb_acl_range.stage = p_acl_range->stage;
    wb_acl_range.group_id = p_acl_range->group_id;
    wb_acl_range.range_type = p_acl_range->range_type;
    wb_acl_range.range_min = p_acl_range->range_min;
    wb_acl_range.range_max = p_acl_range->range_max;
    wb_acl_range.ref_cnt = p_acl_range->ref_cnt;
    sal_memcpy((uint8*)wb_data.buffer + offset, &wb_acl_range, (wb_data.key_len + wb_data.data_len));

    if (++wb_data.valid_cnt == max_entry_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
        wb_data.valid_cnt = 0;
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
_ctc_sai_acl_range_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    uint8 sub_type = 0;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_range_id = *(sai_object_id_t*)key;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_range_id, &ctc_object_id);
    ctc_sai_oid_get_sub_type(acl_range_id, &sub_type);

    if ((SAI_ACL_RANGE_TYPE_OUTER_VLAN == sub_type) || (SAI_ACL_RANGE_TYPE_INNER_VLAN == sub_type))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX, ctc_object_id.value));
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX, ctc_object_id.value));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_range_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_object_id_t ctc_object_id;
    ctc_sai_acl_range_wb_t wb_acl_range;
    ctc_sai_acl_range_t *p_acl_range = NULL;

    sal_memset(&wb_acl_range, 0, sizeof(ctc_sai_acl_range_wb_t));
    sal_memset(&wb_query, 0, sizeof(wb_query));

    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_acl_range_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_RANGE);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_acl_range, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_acl_range_wb_t));
        p_acl_range = ctc_sai_db_get_object_property(lchip, wb_acl_range.oid);
        if (!p_acl_range)
        {
            continue;
        }

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, wb_acl_range.oid, &ctc_object_id);
        p_acl_range->group_id = ctc_object_id.value;
        p_acl_range->stage = wb_acl_range.stage;
        p_acl_range->range_type = wb_acl_range.range_type;
        p_acl_range->range_min = wb_acl_range.range_min;
        p_acl_range->range_max = wb_acl_range.range_max;
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_acl_counter_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t acl_counter_id = *(sai_object_id_t*)key;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_counter_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

#define ________MAPPING_PROCESS________

static bool
_ctc_sai_acl_port_bmp_is_valid(ctc_port_bitmap_t bmp)
{
    uint8 ii = 0;

    for (ii = 0; ii < CTC_PORT_BITMAP_IN_WORD; ii++)
    {
        if (bmp[ii])
        {
            return true;
        }
    }

    return false;
}

static sai_status_t
_ctc_sai_acl_mapping_ip_frag_info(sai_acl_ip_frag_t sai_ip_frag, ctc_ip_frag_t *p_ctc_ip_frag)
{
    if (NULL == p_ctc_ip_frag)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    switch (sai_ip_frag)
    {
        case SAI_ACL_IP_FRAG_ANY:
            *p_ctc_ip_frag = CTC_IP_FRAG_YES;
            break;
        case SAI_ACL_IP_FRAG_NON_FRAG:
            *p_ctc_ip_frag = CTC_IP_FRAG_NON;
            break;
        case SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD:
            *p_ctc_ip_frag = CTC_IP_FRAG_NON_OR_FIRST;
            break;
        case SAI_ACL_IP_FRAG_HEAD:
            *p_ctc_ip_frag = CTC_IP_FRAG_FIRST;
            break;
        case SAI_ACL_IP_FRAG_NON_HEAD:
            *p_ctc_ip_frag = CTC_IP_FRAG_NOT_FIRST;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_l3_type_info(sai_acl_ip_type_t sai_ip_type, ctc_parser_l3_type_t *p_ctc_ip_type)
{
    if (NULL == p_ctc_ip_type)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    switch (sai_ip_type)
    {
        case SAI_ACL_IP_TYPE_ANY:
            *p_ctc_ip_type = CTC_PARSER_L3_TYPE_NONE;
            break;
        case SAI_ACL_IP_TYPE_IP:
            *p_ctc_ip_type = CTC_PARSER_L3_TYPE_IP;
            break;
        case SAI_ACL_IP_TYPE_IPV4ANY:
            *p_ctc_ip_type = CTC_PARSER_L3_TYPE_IPV4;
            break;
        case SAI_ACL_IP_TYPE_IPV6ANY:
            *p_ctc_ip_type = CTC_PARSER_L3_TYPE_IPV6;
            break;
        case SAI_ACL_IP_TYPE_ARP:
        case SAI_ACL_IP_TYPE_ARP_REQUEST:
        case SAI_ACL_IP_TYPE_ARP_REPLY:
            *p_ctc_ip_type = CTC_PARSER_L3_TYPE_ARP;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "sai ip type:%u is not supported!\n", sai_ip_type);
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_acl_mapping_l4_type_info(uint8 ip_protocol, ctc_parser_l3_type_t ctc_l3_type, ctc_parser_l4_type_t *p_ctc_l4_type)
{
    if (NULL == p_ctc_l4_type)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    *p_ctc_l4_type = CTC_PARSER_L4_TYPE_NONE;
    switch (ip_protocol)
    {
        case 6:
            *p_ctc_l4_type = CTC_PARSER_L4_TYPE_TCP;
            break;
        case 17:
            *p_ctc_l4_type = CTC_PARSER_L4_TYPE_UDP;
            break;
        case 47:
            *p_ctc_l4_type = CTC_PARSER_L4_TYPE_GRE;
            break;
        case 1:
            if (CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_ICMP;
            }
            break;
        case 58:
            if (CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_ICMP;
            }
            break;
        case 2:
            if (CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_IGMP;
            }
            break;
        case 4:
            if (CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_IPINIP;
            }
            else if (CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_IPINV6;
            }
            break;
        case 41:
            if (CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_V6INIP;
            }
            else if (CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_V6INV6;
            }
            break;
        case 27:
            if (CTC_PARSER_L3_TYPE_IP == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_RDP;
            }
            break;
        case 132:
            if (CTC_PARSER_L3_TYPE_IP == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_SCTP;
            }
            break;
        case 33:
            if (CTC_PARSER_L3_TYPE_IP == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV4 == ctc_l3_type || CTC_PARSER_L3_TYPE_IPV6 == ctc_l3_type)
            {
                *p_ctc_l4_type = CTC_PARSER_L4_TYPE_DCCP;
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ip_protocol:%u is not supported!\n", ip_protocol);
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_get_nhid_by_oid(sai_object_id_t oid, uint32* ctc_nh_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, oid, &ctc_object_id);

    if ((SAI_OBJECT_TYPE_PORT == ctc_object_id.type)
        || (SAI_OBJECT_TYPE_LAG == ctc_object_id.type))
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_l2uc(ctc_object_id.lchip, ctc_object_id.value, CTC_NH_PARAM_BRGUC_SUB_TYPE_BASIC, ctc_nh_id));
    }
    else if ((SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
        || (SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type))
    {
        *ctc_nh_id = ctc_object_id.value;
    }
    else if ((SAI_OBJECT_TYPE_L2MC_GROUP == ctc_object_id.type)
        || (SAI_OBJECT_TYPE_IPMC_GROUP == ctc_object_id.type))
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mcast_nh(ctc_object_id.lchip, ctc_object_id.value, ctc_nh_id));
    }
    else if (SAI_OBJECT_TYPE_BRIDGE_PORT == ctc_object_id.type)
    {
        ctc_sai_bridge_port_t* p_bridge_port = NULL;
        p_bridge_port = ctc_sai_db_get_object_property(ctc_object_id.lchip, oid);
        if (NULL == p_bridge_port)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        if (SAI_BRIDGE_PORT_TYPE_PORT == ctc_object_id.sub_type)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_l2uc(ctc_object_id.lchip, p_bridge_port->gport, CTC_NH_PARAM_BRGUC_SUB_TYPE_BASIC, ctc_nh_id));
        }
        else if (SAI_BRIDGE_PORT_TYPE_SUB_PORT == ctc_object_id.sub_type)
        {
            *ctc_nh_id = p_bridge_port->nh_id;
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }
    else
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_find_acl_action_field_in_list(ctc_acl_field_action_t *p_field_action, uint32 action_count, uint32 sdk_action_type, uint32 *p_find_index, bool *p_is_action_type_present)
{
    uint16 ii = 0;

    *p_is_action_type_present = false;
    for (ii = 0; ii < action_count; ii++)
    {
        if (p_field_action[ii].type == sdk_action_type)
        {
            *p_is_action_type_present = true;
            break;
        }
    }

    *p_find_index = ii;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_entry_key_fields(uint8 lchip, sai_object_key_t* key, uint8 group_priority, sai_attribute_t* attr_list, ctc_field_key_t* field_key, uint32* p_key_count, uint8* p_bmp_cnt, uint32* p_bmp_start)
{
    uint8  flag_valid = 0;/* make default equal to zeros */
    uint16 lport = 0;
    uint16 max_num = 0;
    uint16 cnt = 0;
    uint32* p_gports = NULL;
    uint32 i = 0;/* need use uint32 */
    uint32 a = 0;
    uint32 n = 0;
    uint32 loop = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_field_port_t *p_field_port = NULL;
    ctc_field_port_t *p_field_port_mask = NULL;
    ctc_field_port_t *p_field_port_array = NULL;
    ctc_field_port_t *p_field_port_mask_array = NULL;
    sai_object_id_t object_id;
    ctc_object_id_t ctc_object_id;
    ctc_object_id_t ctc_port_object_id;
    ctc_ip_frag_t ctc_ip_frag = CTC_IP_FRAG_NON;
    ctc_parser_l3_type_t ctc_ip_type = CTC_PARSER_L3_TYPE_NONE;
    ctc_parser_l4_type_t ctc_l4_type = CTC_PARSER_L4_TYPE_NONE;
    sai_acl_ip_type_t sai_ip_type = SAI_ACL_IP_TYPE_ANY;
    sai_mac_t *macsa = NULL;
    sai_mac_t *macsa_mask = NULL;
    sai_mac_t *macda = NULL;
    sai_mac_t *macda_mask = NULL;
    ipv6_addr_t *ipv6_sa = NULL;
    ipv6_addr_t *ipv6_sa_mask = NULL;
    ipv6_addr_t *ipv6_da = NULL;
    ipv6_addr_t *ipv6_da_mask = NULL;
    ctc_sai_acl_range_t *p_acl_range = NULL;
    sai_acl_entry_attr_t master_field[] = {SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE, SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL};
    uint32 ctc_udf_group_id = 0;
    uint8 type = SAI_UDF_GROUP_TYPE_GENERIC;
    sai_object_id_t sai_object_id;
    ctc_acl_udf_t* p_acl_udf_data = NULL;
    ctc_acl_udf_t* p_acl_udf_mask = NULL;
    ctc_slistnode_t* p_node = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;

    sal_memset(&object_id, 0, sizeof(sai_object_id_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_port_object_id, 0, sizeof(ctc_object_id_t));

    for (i = 0; i < SAI_ACL_KEY_ATTR_NUM; i++)
    {
        if (((SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6 == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6 == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_TC == attr_list[i].id)
            || (SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META == attr_list[i].id))
            && (attr_list[i].value.aclfield.enable))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Some key fields (need to be matched) do not support\n");
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }

    sai_ip_type = attr_list[SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.s32;
    if ((attr_list[SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        && ((SAI_ACL_IP_TYPE_NON_IP == sai_ip_type)
        || (SAI_ACL_IP_TYPE_NON_IPV4 == sai_ip_type)
        || (SAI_ACL_IP_TYPE_NON_IPV6 == sai_ip_type)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Some acl ip type do not support\n");
        return SAI_STATUS_NOT_SUPPORTED;
    }

    for (i = 0; i < sizeof(master_field)/sizeof(sai_acl_entry_attr_t); i++)
    {
        if (attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        {
            attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable = 0;

            switch (attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].id)
            {
                case SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL:
                    _ctc_sai_acl_mapping_l4_type_info(attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.u8, ctc_ip_type, &ctc_l4_type);

                    field_key[*p_key_count].type = CTC_FIELD_KEY_IP_PROTOCOL;
                    field_key[*p_key_count].data = attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.u8;
                    field_key[*p_key_count].mask = attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.mask.u8;
                    (*p_key_count)++;

                    field_key[*p_key_count].type = CTC_FIELD_KEY_L4_TYPE;
                    field_key[*p_key_count].data = ctc_l4_type;
                    field_key[*p_key_count].mask = 0xF;

                    (*p_key_count)++;
                    break;
                case SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE:
                    /* field mask is not needed */
                    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_l3_type_info(attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.s32, &ctc_ip_type));
                    field_key[*p_key_count].type = CTC_FIELD_KEY_L3_TYPE;
                    field_key[*p_key_count].data = ctc_ip_type;
                    field_key[*p_key_count].mask = 0xF;
                    (*p_key_count)++;
                    if (SAI_ACL_IP_TYPE_ARP_REQUEST == attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.s32)
                    {
                        field_key[*p_key_count].type = CTC_FIELD_KEY_ARP_OP_CODE;
                        field_key[*p_key_count].data = 1;
                        field_key[*p_key_count].mask = 0xFFFF;
                        (*p_key_count)++;
                    }
                    else if (SAI_ACL_IP_TYPE_ARP_REPLY == attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.s32)
                    {
                        field_key[*p_key_count].type = CTC_FIELD_KEY_ARP_OP_CODE;
                        field_key[*p_key_count].data = 2;
                        field_key[*p_key_count].mask = 0xFFFF;
                        (*p_key_count)++;
                    }
                    break;
                case SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE:
                    field_key[*p_key_count].type = CTC_FIELD_KEY_ETHER_TYPE;
                    field_key[*p_key_count].data = attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.data.u16;
                    field_key[*p_key_count].mask = attr_list[master_field[i]-SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.mask.u16;
                    (*p_key_count)++;
                    break;
                default:
                    break;
            }
        }
    }
    for (i = 0; i < SAI_ACL_KEY_ATTR_NUM; i++)
    {
        if (!attr_list[i].value.aclfield.enable)
        {
            continue;
        }

        switch (attr_list[i].id)
        {
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6:
                MALLOC_ZERO(MEM_ACL_MODULE, ipv6_sa, sizeof(ipv6_addr_t));
                if (NULL == ipv6_sa)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry ipv6 sa field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, ipv6_sa_mask, sizeof(ipv6_addr_t));
                if (NULL == ipv6_sa_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry ipv6 sa mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                sal_memcpy(ipv6_sa, attr_list[i].value.aclfield.data.ip6, sizeof(sai_ip6_t));
                sal_memcpy(ipv6_sa_mask, attr_list[i].value.aclfield.mask.ip6, sizeof(sai_ip6_t));
                CTC_SAI_NTOH_V6(*ipv6_sa);
                CTC_SAI_NTOH_V6(*ipv6_sa_mask);
                field_key[*p_key_count].type = CTC_FIELD_KEY_IPV6_SA;
                field_key[*p_key_count].ext_data = (void*)ipv6_sa;
                field_key[*p_key_count].ext_mask = (void*)ipv6_sa_mask;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6:
                MALLOC_ZERO(MEM_ACL_MODULE, ipv6_da, sizeof(ipv6_addr_t));
                if (NULL == ipv6_da)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry ipv6 da field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, ipv6_da_mask, sizeof(ipv6_addr_t));
                if (NULL == ipv6_da_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry ipv6 da mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                sal_memcpy(ipv6_da, attr_list[i].value.aclfield.data.ip6, sizeof(sai_ip6_t));
                sal_memcpy(ipv6_da_mask, attr_list[i].value.aclfield.mask.ip6, sizeof(sai_ip6_t));
                CTC_SAI_NTOH_V6(*ipv6_da);
                CTC_SAI_NTOH_V6(*ipv6_da_mask);
                field_key[*p_key_count].type = CTC_FIELD_KEY_IPV6_DA;
                field_key[*p_key_count].ext_data = (void*)ipv6_da;
                field_key[*p_key_count].ext_mask = (void*)ipv6_da_mask;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC:
                MALLOC_ZERO(MEM_ACL_MODULE, macsa, sizeof(sai_mac_t));
                if (NULL == macsa)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macsa field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, macsa_mask, sizeof(sai_mac_t));
                if (NULL == macsa_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macsa mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                sal_memcpy(macsa, attr_list[i].value.aclfield.data.mac, sizeof(sai_mac_t));
                sal_memcpy(macsa_mask, attr_list[i].value.aclfield.mask.mac, sizeof(sai_mac_t));
                field_key[*p_key_count].type = CTC_FIELD_KEY_MAC_SA;
                field_key[*p_key_count].ext_data = (void*)(macsa);
                field_key[*p_key_count].ext_mask = (void*)(macsa_mask);
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC:
                MALLOC_ZERO(MEM_ACL_MODULE, macda, sizeof(sai_mac_t));
                if (NULL == macda)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macda field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, macda_mask, sizeof(sai_mac_t));
                if (NULL == macda_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macda mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                sal_memcpy(macda, attr_list[i].value.aclfield.data.mac, sizeof(sai_mac_t));
                sal_memcpy(macda_mask, attr_list[i].value.aclfield.mask.mac, sizeof(sai_mac_t));
                field_key[*p_key_count].type = CTC_FIELD_KEY_MAC_DA;
                field_key[*p_key_count].ext_data = (void*)(macda);
                field_key[*p_key_count].ext_mask = (void*)(macda_mask);
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_SA;
                field_key[*p_key_count].data = sal_ntohl(attr_list[i].value.aclfield.data.ip4);
                field_key[*p_key_count].mask = sal_ntohl(attr_list[i].value.aclfield.mask.ip4);
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_IP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_DA;
                field_key[*p_key_count].data = sal_ntohl(attr_list[i].value.aclfield.data.ip4);
                field_key[*p_key_count].mask = sal_ntohl(attr_list[i].value.aclfield.mask.ip4);
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS : /* (mask is not needed) */
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port_array, sizeof(ctc_field_port_t) * 8);
                if (NULL == p_field_port_array)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry field port array memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port_mask_array, sizeof(ctc_field_port_t) * 8);
                if (NULL == p_field_port_mask_array)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry field port mask array memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                for (loop = 0; loop < attr_list[i].value.aclfield.data.objlist.count; loop++)
                {
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_list[i].value.aclfield.data.objlist.list[loop], &ctc_port_object_id);
                    lport = CTC_MAP_GPORT_TO_LPORT(ctc_port_object_id.value);
                    CTC_BMP_SET(p_field_port_array[lport / 16].port_bitmap, lport);
                }
                for (loop = 0; loop < 8; loop++)
                {
                    p_field_port_array[loop].type = CTC_FIELD_PORT_TYPE_PORT_BITMAP;
                    p_field_port_array[loop].lchip = lchip;
                    if (_ctc_sai_acl_port_bmp_is_valid(p_field_port_array[loop].port_bitmap))
                    {
                        field_key[*p_key_count].type = CTC_FIELD_KEY_PORT;
                        field_key[*p_key_count].ext_data = (void*)(p_field_port_array + loop);
                        field_key[*p_key_count].ext_mask = (void*)(p_field_port_mask_array + loop);
                        if (p_bmp_start && !flag_valid)
                        {
                            *p_bmp_start = *p_key_count;/* do this before key_count++ */
                            flag_valid = 1;
                        }
                        (*p_key_count)++;
                        if (p_bmp_cnt)
                        {
                            (*p_bmp_cnt)++;
                        }
                    }
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT:
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT:
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port, sizeof(ctc_field_port_t));
                if (NULL == p_field_port)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port_mask, sizeof(ctc_field_port_t));
                if (NULL == p_field_port_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_list[i].value.aclfield.data.oid, &ctc_object_id);

                p_field_port->type = CTC_FIELD_PORT_TYPE_GPORT;
                p_field_port->gport = ctc_object_id.value;
                p_field_port_mask->gport = 0xFFFFFFFF;
                field_key[*p_key_count].type = CTC_FIELD_KEY_PORT;
                field_key[*p_key_count].ext_data = (void*)p_field_port;
                field_key[*p_key_count].ext_mask = (void*)p_field_port_mask;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID:
                field_key[*p_key_count].type = CTC_FIELD_KEY_SVLAN_ID;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u16;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u16;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI:
                field_key[*p_key_count].type = CTC_FIELD_KEY_STAG_COS;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI:
                field_key[*p_key_count].type = CTC_FIELD_KEY_STAG_CFI;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID:
                field_key[*p_key_count].type = CTC_FIELD_KEY_CVLAN_ID;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u16;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u16;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI:
                field_key[*p_key_count].type = CTC_FIELD_KEY_CTAG_COS;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI:
                field_key[*p_key_count].type = CTC_FIELD_KEY_CTAG_CFI;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT:
                field_key[*p_key_count].type = CTC_FIELD_KEY_L4_SRC_PORT;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u16;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u16;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT:
                field_key[*p_key_count].type = CTC_FIELD_KEY_L4_DST_PORT;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u16;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u16;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE:
                field_key[*p_key_count].type = CTC_FIELD_KEY_ETHER_TYPE;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u16;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u16;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_PROTOCOL;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_DSCP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_DSCP;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ECN:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_ECN;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_TTL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_TTL;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_TOS :    /* tos == dscp(7-2) + ecn(1-0)*/
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_ECN;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8 & 0x3;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8 & 0x3;
                (*p_key_count)++;
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_DSCP;
                field_key[*p_key_count].data = (attr_list[i].value.aclfield.data.u8 >> 2) & 0x3F;
                field_key[*p_key_count].mask = (attr_list[i].value.aclfield.mask.u8 >> 2) & 0x3F;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS:
                field_key[*p_key_count].type = CTC_FIELD_KEY_TCP_FLAGS;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE:
                /* field mask is not needed */
                CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_l3_type_info(attr_list[i].value.aclfield.data.s32, &ctc_ip_type));
                field_key[*p_key_count].type = CTC_FIELD_KEY_L3_TYPE;
                field_key[*p_key_count].data = ctc_ip_type;
                field_key[*p_key_count].mask = 0xF;
                (*p_key_count)++;
                if (SAI_ACL_IP_TYPE_ARP_REQUEST == attr_list[i].value.aclfield.data.s32)
                {
                    field_key[*p_key_count].type = CTC_FIELD_KEY_ARP_OP_CODE;
                    field_key[*p_key_count].data = 1;
                    field_key[*p_key_count].mask = 0xFFFF;
                    (*p_key_count)++;
                }
                else if (SAI_ACL_IP_TYPE_ARP_REPLY == attr_list[i].value.aclfield.data.s32)
                {
                    field_key[*p_key_count].type = CTC_FIELD_KEY_ARP_OP_CODE;
                    field_key[*p_key_count].data = 2;
                    field_key[*p_key_count].mask = 0xFFFF;
                    (*p_key_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG:
                /* field mask is not needed */
                CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_ip_frag_info(attr_list[i].value.aclfield.data.s32, &ctc_ip_frag));
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_FRAG;
                field_key[*p_key_count].data = ctc_ip_frag;
                field_key[*p_key_count].mask = 0x3; /* mask is meanless as sdk will support mask */
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IPV6_FLOW_LABEL;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u32;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE:
            case SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE:
                field_key[*p_key_count].type = CTC_FIELD_KEY_ICMP_TYPE;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE:
            case SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE:
                field_key[*p_key_count].type = CTC_FIELD_KEY_ICMP_CODE;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN : /* only acl support */
                if (SAI_PACKET_VLAN_SINGLE_OUTER_TAG == attr_list[i].value.aclfield.data.s32)
                {
                    field_key[*p_key_count].type = CTC_FIELD_KEY_STAG_VALID;
                    field_key[*p_key_count].data = 1;
                    field_key[*p_key_count].mask = 1;
                    (*p_key_count)++;
                }
            case SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG:
                field_key[*p_key_count].type = CTC_FIELD_KEY_VLAN_NUM;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.s32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.s32;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_LABEL0;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u32;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_TTL0;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_EXP0;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_SBIT0;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.booldata;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_LABEL1;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u32;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_TTL1;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_EXP1;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_SBIT1;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.booldata;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_LABEL2;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u32;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_TTL2;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_EXP2;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS:
                field_key[*p_key_count].type = CTC_FIELD_KEY_MPLS_SBIT2;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.booldata;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META:
            case SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META:
                field_key[*p_key_count].type = CTC_FIELD_KEY_DST_CID;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u32;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u32;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META:
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port, sizeof(ctc_field_port_t));
                if (NULL == p_field_port)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port_mask, sizeof(ctc_field_port_t));
                if (NULL == p_field_port_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }

                p_field_port->type = CTC_FIELD_PORT_TYPE_PORT_CLASS;
                p_field_port->port_class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[i].value.aclfield.data.u32);
                p_field_port_mask->port_class_id = 0xFFFF;
                field_key[*p_key_count].type = CTC_FIELD_KEY_PORT;
                field_key[*p_key_count].ext_data = (void*)p_field_port;
                field_key[*p_key_count].ext_mask = (void*)p_field_port_mask;
                (*p_key_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META:
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port, sizeof(ctc_field_port_t));
                if (NULL == p_field_port)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                MALLOC_ZERO(MEM_ACL_MODULE, p_field_port_mask, sizeof(ctc_field_port_t));
                if (NULL == p_field_port_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry port mask field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                p_field_port->type = CTC_FIELD_PORT_TYPE_VLAN_CLASS;
                p_field_port->vlan_class_id = attr_list[i].value.aclfield.data.u32 + 1;
                p_field_port_mask->vlan_class_id = 0xFFFF;
                field_key[*p_key_count].type = CTC_FIELD_KEY_PORT;
                field_key[*p_key_count].ext_data = (void*)p_field_port;
                field_key[*p_key_count].ext_mask = (void*)p_field_port_mask;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META:
            case SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT:
            case SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT:
            case SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT:
            case SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE:
            case SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME:
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE:
                for (loop = 0; loop < attr_list[i].value.aclfield.data.objlist.count; loop++)
                {
                    object_id = attr_list[i].value.aclfield.data.objlist.list[loop];
                    p_acl_range = ctc_sai_db_get_object_property(lchip, object_id);/* the p_acl_range can not be NULL as we have check this situation in creating entry */
                    switch (p_acl_range->range_type)
                    {
                        case SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE:
                            field_key[*p_key_count].type = CTC_FIELD_KEY_L4_SRC_PORT_RANGE;
                            break;
                        case SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE:
                            field_key[*p_key_count].type = CTC_FIELD_KEY_L4_DST_PORT_RANGE;
                            break;
                        case SAI_ACL_RANGE_TYPE_OUTER_VLAN:
                            field_key[*p_key_count].type = CTC_FIELD_KEY_SVLAN_RANGE;
                            break;
                        case SAI_ACL_RANGE_TYPE_INNER_VLAN:
                            field_key[*p_key_count].type = CTC_FIELD_KEY_CVLAN_RANGE;
                            break;
                        case SAI_ACL_RANGE_TYPE_PACKET_LENGTH:
                            field_key[*p_key_count].type = CTC_FIELD_KEY_IP_PKT_LEN_RANGE;
                            break;
                    }

                    if ((SAI_ACL_RANGE_TYPE_OUTER_VLAN == p_acl_range->range_type) || (SAI_ACL_RANGE_TYPE_INNER_VLAN == p_acl_range->range_type))
                    {
                        ctc_vlan_range_info_t vrange_info;

                        sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
                        sal_memset(&vrange_info, 0, sizeof(ctc_vlan_range_info_t));
                        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_RANGE, object_id, &ctc_object_id);
                        MALLOC_ZERO(MEM_ACL_MODULE, field_key[*p_key_count].ext_data, sizeof(uint32));
                        if (NULL == field_key[*p_key_count].ext_data)
                        {
                            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry vlan range field memory\n");
                            status =  SAI_STATUS_NO_MEMORY;
                            goto error0;
                        }
                        MALLOC_ZERO(MEM_ACL_MODULE, field_key[*p_key_count].ext_mask, sizeof(uint32));
                        if (NULL == field_key[*p_key_count].ext_mask)
                        {
                            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry vlan range field memory\n");
                            status =  SAI_STATUS_NO_MEMORY;
                            goto error0;
                        }
                        ((uint32*)field_key[*p_key_count].ext_data)[0] = ctc_object_id.value;

                        vrange_info.direction = (SAI_ACL_STAGE_INGRESS == p_acl_range->stage) ? CTC_INGRESS : CTC_EGRESS;
                        vrange_info.vrange_grpid = ctc_object_id.value;

                        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_object_id);
                        if (SAI_OBJECT_TYPE_PORT == ctc_object_id.type)
                        {
                            CTC_SAI_ERROR_GOTO(ctcs_port_set_vlan_range(lchip, ctc_object_id.value, &vrange_info, 1), status, error0);
                        }
                        else if (SAI_OBJECT_TYPE_LAG == ctc_object_id.type)
                        {
                            ctcs_linkagg_get_max_mem_num(lchip, &max_num);
                            MALLOC_ZERO(MEM_ACL_MODULE, p_gports, sizeof(uint32)* max_num);
                            ctcs_linkagg_get_member_ports(lchip, (ctc_object_id.value & 0xFF), p_gports, &cnt);
                            for (n = 0; n < cnt; n++)
                            {
                                CTC_SAI_ERROR_GOTO(ctcs_port_set_vlan_range(lchip, p_gports[n], &vrange_info, 1), status, error0);
                            }
                        }
                        else
                        {
                            for (a = 0; a < SAI_ACL_KEY_ATTR_NUM; a++)
                            {
                                if (attr_list[a].value.aclfield.enable)
                                {
                                    if ((SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT == attr_list[a].id) || (SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT == attr_list[a].id))
                                    {
                                        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_list[a].value.aclfield.data.oid, &ctc_object_id);
                                        CTC_SAI_ERROR_GOTO(ctcs_port_set_vlan_range(lchip, ctc_object_id.value, &vrange_info, 1), status, error0);
                                    }
                                    else if (SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS == attr_list[a].id)
                                    {
                                        for (n = 0; n < attr_list[a].value.aclfield.data.objlist.count; n++)
                                        {
                                            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_list[a].value.aclfield.data.oid, &ctc_object_id);
                                            CTC_SAI_ERROR_GOTO(ctcs_port_set_vlan_range(lchip, ctc_object_id.value, &vrange_info, 1), status, error0);
                                        }
                                    }
                                    else
                                    {
                                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to set acl vlan range!\n");
                                        status =  SAI_STATUS_INVALID_PARAMETER;
                                        goto error0;
                                    }
                                }
                            }
                        }
                    }
                    field_key[*p_key_count].data = p_acl_range->range_min;
                    field_key[*p_key_count].mask = p_acl_range->range_max;
                    (*p_key_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER:
                field_key[*p_key_count].type = CTC_FIELD_KEY_IP_PROTOCOL;
                field_key[*p_key_count].data = attr_list[i].value.aclfield.data.u8;
                field_key[*p_key_count].mask = attr_list[i].value.aclfield.mask.u8;
                (*p_key_count)++;
                break;

            case SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI:
                field_key[*p_key_count].type = CTC_FIELD_KEY_DOT1AE_SCI;

                field_key[*p_key_count].ext_data = mem_malloc(MEM_ACL_MODULE, 8);
                if (NULL == field_key[*p_key_count].ext_data)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macsec sci field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;;
                }
                field_key[*p_key_count].ext_mask = mem_malloc(MEM_ACL_MODULE, 8);
                if (NULL == field_key[*p_key_count].ext_mask)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry macsec sci field memory\n");
                    status =  SAI_STATUS_NO_MEMORY;
                    goto error0;;
                }
                sal_memcpy(field_key[*p_key_count].ext_data, attr_list[i].value.aclfield.data.u8list.list, 8);
                sal_memcpy(field_key[*p_key_count].ext_mask, attr_list[i].value.aclfield.mask.u8list.list, 8);
                (*p_key_count)++;
                break;

            default:
                if (attr_list[i].id >= SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN
                    && attr_list[i].id < (SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN + CTC_SAI_UDF_GROUP_MAX_NUM(lchip)))
                {
                    p_acl_udf_data = (ctc_acl_udf_t*)mem_malloc(MEM_ACL_MODULE, sizeof(ctc_acl_udf_t));
                    if (NULL == p_acl_udf_data)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry udf field memory\n");
                        status =  SAI_STATUS_NO_MEMORY;
                        goto error0;
                    }

                    p_acl_udf_mask = (ctc_acl_udf_t*)mem_malloc(MEM_ACL_MODULE, sizeof(ctc_acl_udf_t));
                    if (NULL == p_acl_udf_mask)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry udf field memory\n");
                        status =  SAI_STATUS_NO_MEMORY;
                        goto error0;
                    }

                    ctc_udf_group_id = attr_list[i].id-SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN;
                    sai_object_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF_GROUP, lchip, type, 0, ctc_udf_group_id);

                    ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_UDF_GROUP, &ctc_object_id, &sai_object_id);
                    p_udf_group = ctc_sai_db_get_object_property(lchip, sai_object_id);
                    if (NULL == p_udf_group)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to add udf field, invalid udf_group_id 0x%"PRIx64"!\n", sai_object_id);
                        status = SAI_STATUS_ITEM_NOT_FOUND;
                        goto error0;
                    }

                    CTC_SLIST_LOOP(p_udf_group->member_list, p_node)
                    {
                        p_udf_group_member = (ctc_sai_udf_group_member_t*)p_node;
                        p_udf_entry = ctc_sai_db_get_object_property(lchip, p_udf_group_member->udf_id);

                        if (NULL == p_udf_entry)
                        {
                            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to add acl udf filed of group_id 0x%"PRIx64"'s udf member udf_id 0x%"PRIx64"!\n", attr_list[i].id-SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN, p_udf_group_member->udf_id);
                            status = SAI_STATUS_ITEM_NOT_FOUND;
                            goto error0;
                        }
                        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF, p_udf_group_member->udf_id, &ctc_object_id);
                        p_acl_udf_data->udf_id = ctc_object_id.value;
                        p_acl_udf_mask->udf_id = ctc_object_id.value;
                        break;
                    }
                    sal_memcpy(p_acl_udf_data->udf, attr_list[i].value.aclfield.data.u8list.list, attr_list[i].value.aclfield.data.u8list.count);
                    sal_memcpy(p_acl_udf_mask->udf, attr_list[i].value.aclfield.mask.u8list.list, attr_list[i].value.aclfield.mask.u8list.count);

                    field_key[*p_key_count].type = CTC_FIELD_KEY_UDF;
                    field_key[*p_key_count].ext_data = p_acl_udf_data;
                    field_key[*p_key_count].ext_mask = p_acl_udf_mask;
                    (*p_key_count)++;
                    break;
                }
                else
                {
                    /* all not support key fields has been checked */
                    break;
                }
        }
    }

    return SAI_STATUS_SUCCESS;

error0:
    if (ipv6_sa)
    {
        mem_free(ipv6_sa);
    }
    if (ipv6_sa_mask)
    {
        mem_free(ipv6_sa_mask);
    }
    if (ipv6_da)
    {
        mem_free(ipv6_da);
    }
    if (ipv6_da_mask)
    {
        mem_free(ipv6_da_mask);
    }
    if (macsa)
    {
        mem_free(macsa);
    }
    if (macsa_mask)
    {
        mem_free(macsa_mask);
    }
    if (macda)
    {
        mem_free(macda);
    }
    if (macda_mask)
    {
        mem_free(macda_mask);
    }
    if (p_field_port)
    {
        mem_free(p_field_port);
    }
    if (p_field_port_mask)
    {
        mem_free(p_field_port_mask);
    }

    if (p_field_port_array)
    {
        mem_free(p_field_port_array);
    }

    if (p_field_port_mask_array)
    {
        mem_free(p_field_port_mask_array);
    }

    if (p_acl_udf_data)
    {
        mem_free(p_acl_udf_data);
    }

    if (p_acl_udf_mask)
    {
        mem_free(p_acl_udf_mask);
    }

    return status;
}

static sai_status_t
_ctc_sai_acl_mapping_acl_entry_action_fields(uint8 lchip, sai_object_key_t* key, uint8 group_priority, sai_object_id_t entry_object_id, sai_attribute_t *attr_list,
                                             ctc_acl_field_action_t *field_action, uint32 *p_action_count)
{
    uint32 i = 0;
    uint32 temp_index1 = 0;
    uint32 temp_index2 = 0;
    uint8  drop_action = 0;
    uint8  copy_to_cpu = 0;
    uint32 find_index  = 0;
    uint32 ctc_nh_id = 0;
    int32  ret = SAI_STATUS_SUCCESS;
    bool is_copy_action = false;
    bool is_action_type_present = false;
    ctc_object_id_t trap_id;
    ctc_object_id_t ctc_object_id;
    ctc_object_id_t ctc_entry_object_id;
    ctc_object_id_t ctc_policer_object_id;
    sai_packet_action_t packet_action_type = SAI_PACKET_ACTION_DROP;
    ctc_acl_to_cpu_t    *p_acl_to_cpu = NULL;
    ctc_acl_inter_cn_t  *p_acl_ecn = NULL;
    ctc_acl_vlan_edit_t *p_vlan_edit = NULL;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    uint8 igs_radom_log_ismirror = 0;
    uint8 egs_radom_log_ismirror = 0;
    uint32 mirror_sample_rate = 0;

    sal_memset(&trap_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_entry_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_policer_object_id, 0, sizeof(ctc_object_id_t));

    p_acl_entry = ctc_sai_db_get_object_property(lchip, entry_object_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL entry is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    /* check the not support sai action */
    for (i = 0; i < SAI_ACL_ACTION_ATTR_NUM; i++)
    {
        if ((SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_FLOOD == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6 == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6 == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT == attr_list[i].id ||
            SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST == attr_list[i].id) && (attr_list[i].value.aclaction.enable))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        if(SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS == attr_list[i].id)
        {
            igs_radom_log_ismirror = 1;
        }
        if(SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS == attr_list[i].id)
        {
            egs_radom_log_ismirror = 1;
        }
    }
    for (i = 0; i < SAI_ACL_ACTION_ATTR_NUM; i++)
    {
        if(igs_radom_log_ismirror && (SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE == attr_list[i].id))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        if(egs_radom_log_ismirror && (SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE == attr_list[i].id))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }

    /* check the dependency relationship between copy action and trap id */
    temp_index1 = SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION    - SAI_ACL_ENTRY_ATTR_ACTION_START;
    temp_index2 = SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID - SAI_ACL_ENTRY_ATTR_ACTION_START;
    is_copy_action = attr_list[temp_index1].value.aclaction.enable && (attr_list[temp_index1].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_COPY
    || attr_list[temp_index1].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_TRAP
    || attr_list[temp_index1].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_LOG);
    if (attr_list[temp_index2].value.aclaction.enable && !is_copy_action)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    for (i = 0; i < SAI_ACL_ACTION_ATTR_NUM; i++)
    {
        if (!attr_list[i].value.aclaction.enable)
        {
            continue;
        }
        switch (attr_list[i].id)
        {
            case SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT:
                CTC_SAI_ERROR_RETURN(_ctc_sai_acl_get_nhid_by_oid(attr_list[i].value.aclaction.parameter.oid, &ctc_nh_id));
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_REDIRECT;
                field_action[*p_action_count].data0 = ctc_nh_id;
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION:
                /* means add action field */
                packet_action_type = attr_list[i].value.aclaction.parameter.s32;
                switch (packet_action_type)
                {
                    case SAI_PACKET_ACTION_DROP : /** Drop Packet in data plane */
                    case SAI_PACKET_ACTION_TRAP : /** This is a combination of SAI packet action COPY and DROP. */
                    case SAI_PACKET_ACTION_DENY : /** This is a combination of SAI packet action COPY_CANCEL and DROP */
                        drop_action = 1;
                        break;
                    default:
                        drop_action = 0;
                        break;
                }
                switch (packet_action_type)
                {
                    case SAI_PACKET_ACTION_COPY : /** Copy Packet to CPU. */
                    case SAI_PACKET_ACTION_TRAP : /** This is a combination of SAI packet action COPY and DROP. */
                    case SAI_PACKET_ACTION_LOG : /** This is a combination of SAI packet action COPY and FORWARD. */
                        copy_to_cpu = 1;
                        break;
                    default:
                        copy_to_cpu = 0;
                        break;
                }

                if (drop_action)
                {
                    field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_DISCARD;
                    field_action[*p_action_count].data0 = CTC_QOS_COLOR_NONE;
                    (*p_action_count)++;
                }

                if (copy_to_cpu)
                {
                    /* if already config copy action, must config trap id */
                    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_to_cpu, sizeof(ctc_acl_to_cpu_t));
                    if (NULL == p_acl_to_cpu)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl to cpu memory!\n");
                        ret = SAI_STATUS_NO_MEMORY;
                        goto error0;
                    }

                    p_acl_to_cpu->mode = CTC_ACL_TO_CPU_MODE_TO_CPU_NOT_COVER;

                    field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                    field_action[*p_action_count].ext_data = p_acl_to_cpu;
                    (*p_action_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_COUNTER:
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr_list[i].value.aclaction.parameter.oid, &ctc_object_id);
                if (SAI_OBJECT_TYPE_ACL_COUNTER == ctc_object_id.type)
                {
                    p_acl_counter = ctc_sai_db_get_object_property(lchip, attr_list[i].value.aclaction.parameter.oid);
                    if ((NULL == p_acl_counter) || (0 == p_acl_counter->stats_id))
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
                        return SAI_STATUS_ITEM_NOT_FOUND;
                    }
                    p_acl_counter = ctc_sai_db_get_object_property(lchip, attr_list[i].value.aclaction.parameter.oid);
                    field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_STATS;
                    field_action[*p_action_count].data0 = p_acl_counter->stats_id;
                    (*p_action_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS:
            case SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS:
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_mirror_set_acl_mirr(lchip, group_priority, &p_acl_entry->ctc_mirror_id, &mirror_sample_rate, &attr_list[i]));
                    if(0xFFFFFFFF != mirror_sample_rate)
                    {
                        field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_RANDOM_LOG;
                        field_action[*p_action_count].data0 = p_acl_entry->ctc_mirror_id;
                        field_action[*p_action_count].data1 = mirror_sample_rate;
                        (*p_action_count)++;
                    }
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER:
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_ENTRY, entry_object_id, &ctc_entry_object_id);
                if (attr_list[i].value.aclaction.parameter.oid)
                {
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_POLICER, attr_list[i].value.aclaction.parameter.oid, &ctc_policer_object_id);
                    ctc_sai_policer_acl_set_policer(lchip, ctc_entry_object_id.value, ctc_policer_object_id.value, true);
                }
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_MICRO_FLOW_POLICER;
                field_action[*p_action_count].data0 = ctc_policer_object_id.value;
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_TC:
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_PRIORITY;
                field_action[*p_action_count].data0 = CTC_QOS_COLOR_NONE;
                field_action[*p_action_count].data1 = attr_list[i].value.aclaction.parameter.u8;
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR:
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_COLOR;
                if (SAI_PACKET_COLOR_GREEN == attr_list[i].value.aclaction.parameter.s32)
                {
                    field_action[*p_action_count].data0 = CTC_QOS_COLOR_GREEN;
                }
                else if (SAI_PACKET_COLOR_YELLOW == attr_list[i].value.aclaction.parameter.s32)
                {
                    field_action[*p_action_count].data0 = CTC_QOS_COLOR_YELLOW;
                }
                else if (SAI_PACKET_COLOR_RED == attr_list[i].value.aclaction.parameter.s32)
                {
                    field_action[*p_action_count].data0 = CTC_QOS_COLOR_RED;
                }
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID:
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI:
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID:
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI:
                /* first one to set action vlan edit */
                if (NULL == p_vlan_edit)
                {
                    MALLOC_ZERO(MEM_ACL_MODULE, p_vlan_edit, sizeof(ctc_acl_vlan_edit_t));
                    if (NULL == p_vlan_edit)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl vlan edit memory!\n");
                        ret = SAI_STATUS_NO_MEMORY;
                        goto error0;
                    }
                }
                if (SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID == attr_list[i].id)
                {
                    p_vlan_edit->svid_new = attr_list[i].value.aclaction.parameter.u16;
                    p_vlan_edit->svid_sl = CTC_VLAN_TAG_SL_NEW;
                    p_vlan_edit->stag_op = CTC_VLAN_TAG_OP_REP_OR_ADD;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI == attr_list[i].id)
                {
                    p_vlan_edit->scos_new = attr_list[i].value.aclaction.parameter.u8;
                    p_vlan_edit->scos_sl = CTC_VLAN_TAG_SL_NEW;
                    p_vlan_edit->stag_op = CTC_VLAN_TAG_OP_REP_OR_ADD;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID == attr_list[i].id)
                {
                    p_vlan_edit->cvid_new = attr_list[i].value.aclaction.parameter.u16;
                    p_vlan_edit->cvid_sl = CTC_VLAN_TAG_SL_NEW;
                    p_vlan_edit->ctag_op = CTC_VLAN_TAG_OP_REP_OR_ADD;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI == attr_list[i].id)
                {
                    p_vlan_edit->ccos_new = attr_list[i].value.aclaction.parameter.u8;
                    p_vlan_edit->ccos_sl = CTC_VLAN_TAG_SL_NEW;
                    p_vlan_edit->ctag_op = CTC_VLAN_TAG_OP_REP_OR_ADD;
                }

                /* must check the vlan edit action has already exist or not in the current established field action array */
                _ctc_sai_acl_find_acl_action_field_in_list(field_action, *p_action_count, CTC_ACL_FIELD_ACTION_VLAN_EDIT, &find_index, &is_action_type_present);
                if (!is_action_type_present)
                {
                    field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_VLAN_EDIT;
                    field_action[*p_action_count].ext_data = p_vlan_edit;
                    (*p_action_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP:
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_DSCP;
                field_action[*p_action_count].data0 = attr_list[i].value.aclaction.parameter.u8;
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN:
                MALLOC_ZERO(MEM_ACL_MODULE, p_acl_ecn, sizeof(ctc_acl_inter_cn_t));
                if (NULL == p_acl_ecn)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl ecn memory!\n");
                    ret = SAI_STATUS_NO_MEMORY;
                    goto error0;
                }
                p_acl_ecn->inter_cn = attr_list[i].value.aclaction.parameter.u8;
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_INTER_CN;
                field_action[*p_action_count].ext_data = p_acl_ecn;
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE:
                {
                    uint32 acl_log_id = 0;
                    uint32 log_rate = 0;
                    ctc_sai_samplepacket_set_acl_samplepacket(lchip, CTC_INGRESS, group_priority, entry_object_id, &attr_list[i], &acl_log_id, &log_rate);
                    field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_RANDOM_LOG;
                    field_action[*p_action_count].data0 = acl_log_id;
                    field_action[*p_action_count].data1 = log_rate;
                    (*p_action_count)++;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE:
                return SAI_STATUS_NOT_SUPPORTED;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA:
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_METADATA;
                field_action[*p_action_count].data0 = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[i].value.aclaction.parameter.u32);
                (*p_action_count)++;
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID:
                /* if go to this branch, packet action must be copy action */
                _ctc_sai_acl_find_acl_action_field_in_list(field_action, *p_action_count, CTC_ACL_FIELD_ACTION_CP_TO_CPU, &find_index, &is_action_type_present);
                if (is_action_type_present)
                {
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, attr_list[temp_index2].value.aclaction.parameter.oid, &trap_id);
                    p_acl_to_cpu->mode = CTC_ACL_TO_CPU_MODE_TO_CPU_COVER;
                    p_acl_to_cpu->cpu_reason_id = trap_id.value;
                }
                else
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "config trap id but packet action is not copy !\n");
                    ret = SAI_STATUS_NOT_SUPPORTED;
                    goto error0;
                }
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN:
                field_action[*p_action_count].type = CTC_ACL_FIELD_ACTION_DENY_LEARNING;
                (*p_action_count)++;
                break;
            default:
                /* All not support actions have been checked out */
                break;
        }

    }

    return SAI_STATUS_SUCCESS;

error0:
    for (i = 0; i < *p_action_count; i++)
    {
        if(field_action[i].ext_data)
        {
            mem_free(field_action[i].ext_data);
        }
    }

    return ret;
}

static sai_status_t
_ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(sai_attr_id_t attr_id, sai_acl_bind_point_type_t *p_bind_point_type, sai_acl_stage_t *p_bind_point_stage)
{
    switch (attr_id)
    {
        case SAI_PORT_ATTR_INGRESS_ACL:
        case SAI_PORT_ATTR_EGRESS_ACL:
            *p_bind_point_type = SAI_ACL_BIND_POINT_TYPE_PORT;
            break;
        case SAI_LAG_ATTR_INGRESS_ACL:
        case SAI_LAG_ATTR_EGRESS_ACL:
            *p_bind_point_type = SAI_ACL_BIND_POINT_TYPE_LAG;
            break;
        case SAI_VLAN_ATTR_INGRESS_ACL:
        case SAI_VLAN_ATTR_EGRESS_ACL:
            *p_bind_point_type = SAI_ACL_BIND_POINT_TYPE_VLAN;
            break;
        case SAI_SWITCH_ATTR_INGRESS_ACL:
        case SAI_SWITCH_ATTR_EGRESS_ACL:
            *p_bind_point_type = SAI_ACL_BIND_POINT_TYPE_SWITCH;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }

    switch (attr_id)
    {
        case SAI_PORT_ATTR_INGRESS_ACL:
        case SAI_LAG_ATTR_INGRESS_ACL:
        case SAI_VLAN_ATTR_INGRESS_ACL:
        case SAI_SWITCH_ATTR_INGRESS_ACL:
            *p_bind_point_stage = SAI_ACL_STAGE_INGRESS;
            break;
        case SAI_PORT_ATTR_EGRESS_ACL :
        case SAI_LAG_ATTR_EGRESS_ACL:
        case SAI_VLAN_ATTR_EGRESS_ACL:
        case SAI_SWITCH_ATTR_EGRESS_ACL:
            *p_bind_point_stage = SAI_ACL_STAGE_EGRESS;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_check_acl_entry_key_field(uint32* sai_key_field_bmp, uint32 attr_count, const sai_attribute_t* attr_list)
{
    uint16 ii = 0;

    for (ii = 0; ii < attr_count; ii++)
    {
        if (SAI_ACL_ATTR_IS_KEY(attr_list[ii].id) && !CTC_BMP_ISSET(sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(attr_list[ii].id)))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The entry's table key field attr_list[%u].id:%u is not configure, but entry use!\n", ii, attr_list[ii].id);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_check_master_key_field(uint32* p_sai_key_field_bmp, sai_acl_stage_t sai_acl_stage, uint32 bind_point_list)
{
    uint32 ii = 0;
    uint32 count = 0;

    for (ii = SAI_ACL_BIND_POINT_TYPE_PORT; ii <= SAI_ACL_BIND_POINT_TYPE_SWITCH; ii++)
    {
        if (bind_point_list & (1<<ii))
        {
            if (SAI_ACL_BIND_POINT_TYPE_PORT == ii)
            {
                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT)))
                {
                    count++;
                }

                if ((SAI_ACL_STAGE_INGRESS == sai_acl_stage) && (1 != count))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                if ((SAI_ACL_STAGE_EGRESS == sai_acl_stage) && (0 != count))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                count = 0;

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT)))
                {
                    count++;
                }

                if ((SAI_ACL_STAGE_INGRESS == sai_acl_stage) && (0 != count))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                if ((SAI_ACL_STAGE_EGRESS == sai_acl_stage) && (count > 1))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }
            }

            if (SAI_ACL_BIND_POINT_TYPE_LAG == ii)
            {
                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT)))
                {
                    count++;
                }

                if ((SAI_ACL_STAGE_INGRESS == sai_acl_stage) && (count > 1))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                if ((SAI_ACL_STAGE_EGRESS == sai_acl_stage) && (0 != count))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                count = 0;

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS)))
                {
                    count++;
                }

                if ((SAI_ACL_STAGE_INGRESS == sai_acl_stage) && (0 != count))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }

                if ((SAI_ACL_STAGE_EGRESS == sai_acl_stage) && (count > 1))
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }
            }

            if (SAI_ACL_BIND_POINT_TYPE_VLAN == ii)
            {
                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID)))
                {
                    count++;
                }

                if (CTC_BMP_ISSET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID)))
                {
                    count++;
                }

                if (count == 0)
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_check_group_key_field(uint8 lchip, ctc_sai_acl_group_t* p_acl_group)
{
    uint32 ii = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 sai_key_field_bmp[(SAI_ACL_KEY_ATTR_NUM-1)/32 + 1] = {0};
    ctc_slistnode_t* table_node = NULL;
    ctc_sai_acl_table_t* p_acl_table = NULL;
    ctc_sai_acl_group_member_t* p_group_member = NULL;

    CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
    {
        p_group_member = (ctc_sai_acl_group_member_t*)table_node;
        p_acl_table = ctc_sai_db_get_object_property(lchip, p_group_member->table_id);
        if (NULL == p_acl_table)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table is not exist\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        for (ii = SAI_ACL_TABLE_ATTR_FIELD_START; ii <= SAI_ACL_TABLE_ATTR_FIELD_END; ii++)
        {
            if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(ii)))
            {
                CTC_BMP_SET(sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(ii));
            }
        }

        /* Check the master key field of group's member table, e.g. IN_PORTS, IN_PORT or SRC_PORT, OUT_PORTS, OUT_PORT, select one and only one. */
        status = _ctc_sai_acl_check_master_key_field(sai_key_field_bmp, p_acl_group->group_stage, p_acl_group->bind_point_list);
        if (SAI_STATUS_SUCCESS != status)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Check group member's bind point key field fail!\n");
            return status;
        }
        sal_memset(sai_key_field_bmp, 0, sizeof(sai_key_field_bmp));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_check_member_priority(ctc_sai_acl_group_t* p_acl_group, uint32 member_priority)
{
    uint32 count = 0;
    ctc_slistnode_t* p_table_node = NULL;
    ctc_sai_acl_group_member_t* p_group_member = NULL;

    CTC_SLIST_LOOP(p_acl_group->member_list, p_table_node)
    {
        p_group_member = (ctc_sai_acl_group_member_t*)p_table_node;
        count++;
        if ((SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == p_acl_group->group_type)
           && (p_group_member->members_prio == member_priority))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Sequential group member priority:%u already exist.\n", member_priority);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
    {
        if (SAI_ACL_STAGE_INGRESS == p_acl_group->group_stage)
        {
            if (ACL_INGRESS_PARAELL_TCAM_BLOCK_NUM == count)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ACL, "Exceed ingress ACL parallel group max member num %d.\n", ACL_INGRESS_PARAELL_TCAM_BLOCK_NUM);
                return SAI_STATUS_NOT_SUPPORTED;
            }
        }
        else
        {
            if (ACL_EGRESS_PARAELL_TCAM_BLOCK_NUM == count)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ACL, "Exceed egress ACL parallel group max member num %d.\n", ACL_EGRESS_PARAELL_TCAM_BLOCK_NUM);
                return SAI_STATUS_NOT_SUPPORTED;
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_sai_table_field(uint8 lchip, ctc_sai_acl_table_t* p_acl_table, uint32* p_ctc_master_field, uint32* p_ctc_slave_field, uint32* p_sai_key_field_bmp)
{
    uint32 ii = 0, jj = 0;
    uint32 sai_master_field[(SAI_ACL_KEY_ATTR_NUM-1)/32 + 1] = {0};

    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_check_master_key_field(p_acl_table->table_key_bmp, p_acl_table->table_stage, p_acl_table->bind_point_list));
    for (ii = SAI_ACL_BIND_POINT_TYPE_PORT; ii <= SAI_ACL_BIND_POINT_TYPE_SWITCH; ii++)
    {
        if (p_acl_table->bind_point_list & (1<<ii))
        {
            if (SAI_ACL_STAGE_INGRESS == p_acl_table->table_stage && SAI_ACL_BIND_POINT_TYPE_PORT == ii)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT));
                }
            }

            if (SAI_ACL_STAGE_EGRESS == p_acl_table->table_stage && SAI_ACL_BIND_POINT_TYPE_PORT == ii)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT));
                }
            }

            if (SAI_ACL_STAGE_INGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_LAG)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT));
                }
            }

            if (SAI_ACL_STAGE_EGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_LAG)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS));
                }
            }

            if (SAI_ACL_STAGE_INGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_VLAN)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID));
                }
            }

            if (SAI_ACL_STAGE_EGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_VLAN)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID));
                }

                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID));
                }
            }

            if (SAI_ACL_STAGE_INGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID));
                }
            }

            if (SAI_ACL_STAGE_EGRESS == p_acl_table->table_stage && ii == SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE)
            {
                if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID)))
                {
                    CTC_BMP_SET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID));
                }
            }
        }
    }

    for (ii = SAI_ACL_TABLE_ATTR_FIELD_START; ii < SAI_ACL_TABLE_ATTR_FIELD_END; ii++)
    {
        if (CTC_BMP_ISSET(sai_master_field, SAI_ACL_ATTR_ID2INDEX(ii)))
        {
            for (jj = 0; jj < CTC_FIELD_KEY_NUM; jj++)
            {
                if (CTC_BMP_ISSET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(ii)], jj))
                {
                    CTC_BMP_SET(p_ctc_master_field, jj);
                }
            }
        }
    }

    for (ii = SAI_ACL_TABLE_ATTR_FIELD_START; ii < SAI_ACL_TABLE_ATTR_FIELD_END; ii++)
    {
        if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(ii)))
        {
            CTC_BMP_SET(p_sai_key_field_bmp, SAI_ACL_ATTR_ID2INDEX(ii));

            if (SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE == ii)
            {
                for (jj = SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE; jj <= SAI_ACL_RANGE_TYPE_PACKET_LENGTH; jj++)
                {
                    if (!CTC_IS_BIT_SET(p_acl_table->range_type_bmp, jj))
                    {
                        continue;
                    }
                    switch (jj)
                    {
                        case SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE:
                            CTC_BMP_SET(p_ctc_slave_field, CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
                            break;

                        case SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE:
                            CTC_BMP_SET(p_ctc_slave_field, CTC_FIELD_KEY_L4_DST_PORT_RANGE);
                            break;

                        case SAI_ACL_RANGE_TYPE_OUTER_VLAN:
                            CTC_BMP_SET(p_ctc_slave_field, CTC_FIELD_KEY_SVLAN_RANGE);
                            break;

                        case SAI_ACL_RANGE_TYPE_INNER_VLAN:
                            CTC_BMP_SET(p_ctc_slave_field, CTC_FIELD_KEY_CVLAN_RANGE);
                            break;

                        case SAI_ACL_RANGE_TYPE_PACKET_LENGTH:
                            CTC_BMP_SET(p_ctc_slave_field, CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
                            break;

                        default:
                            break;
                    }
                }
            }
            else
            {
                for (jj = 0; jj < CTC_FIELD_KEY_NUM; jj++)
                {
                    if (CTC_BMP_ISSET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(ii)], jj) && !CTC_BMP_ISSET(p_ctc_master_field, jj))
                    {
                        CTC_BMP_SET(p_ctc_slave_field, jj);
                    }
                }
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_fields_lookup_type(uint32* p_ctc_master_filed, uint32* p_ctc_slave_field, uint32* p_ctc_lookup_type)
{
    uint32 ii = 0, jj = 0, nn = 0;
    uint32 ctc_mask_field[(CTC_FIELD_KEY_NUM - 1) / 32 + 1] = {0};

    for (ii = CTC_ACL_TCAM_LKUP_TYPE_L2; ii < CTC_ACL_TCAM_LKUP_TYPE_MAX; ii++)
    {
        if (0 == ctc_sai_key_info.type2key[ii])
        {
            continue;
        }

        for (jj = 0; jj < CTC_SAI_ACL_KEY_NUM; jj++)
        {
            if (!CTC_IS_BIT_SET(ctc_sai_key_info.type2key[ii], jj))
            {
                continue;
            }

            for (nn = 0; nn < CTC_FIELD_KEY_NUM; nn++)
            {
                if ((!CTC_BMP_ISSET(ctc_sai_key_info.key2field[jj], nn)) && CTC_BMP_ISSET(p_ctc_master_filed, nn))
                {
                    goto CTC_SAI_MAPPING_LOOKUP_LOOKUP_KEY_DISSATISFY;
                }
            }

            sal_memset(ctc_mask_field, 0, sizeof(ctc_mask_field));
            for (nn = 0; nn < CTC_FIELD_KEY_NUM; nn++)
            {
                if (CTC_BMP_ISSET(ctc_sai_key_info.key2field[jj], nn) && CTC_BMP_ISSET(p_ctc_slave_field, nn))
                {
                    CTC_BMP_SET(ctc_mask_field, nn);
                }
            }

            for (nn = 0; nn < CTC_FIELD_KEY_NUM; nn++)
            {
                if (!CTC_BMP_ISSET(ctc_mask_field, nn) && CTC_BMP_ISSET(p_ctc_slave_field, nn))
                {
                   if ((PKT_TYPE_RESERVED != ctc_sai_key_info.key2packet[jj])
                      && (PKT_TYPE_RESERVED != ctc_sai_key_info.field2packet[nn])
                      && (ctc_sai_key_info.field2packet[nn] != ctc_sai_key_info.key2packet[jj]))
                    {
                        goto CTC_SAI_MAPPING_LOOKUP_TCAM_KEY_NEXT;
                    }
                    else
                    {
                        goto CTC_SAI_MAPPING_LOOKUP_LOOKUP_KEY_DISSATISFY;
                    }
                }
            }
            break;
CTC_SAI_MAPPING_LOOKUP_TCAM_KEY_NEXT:
            continue;
        }
        break;
CTC_SAI_MAPPING_LOOKUP_LOOKUP_KEY_DISSATISFY:
        continue;
    }
    *p_ctc_lookup_type = ii;

    if (CTC_ACL_TCAM_LKUP_TYPE_MAX == ii)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_table_lookup_type(uint8 lchip, ctc_sai_acl_table_t* p_acl_table)
{
    uint32 lookup_type = 0;
    uint32 ctc_slave_field[(CTC_FIELD_KEY_NUM-1)/32 + 1] = {0};
    uint32 ctc_master_filed[(CTC_FIELD_KEY_NUM-1)/32 + 1] = {0};
    uint32 sai_key_field_bmp[(SAI_ACL_KEY_ATTR_NUM-1)/32 + 1] = {0};

    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_sai_table_field(lchip, p_acl_table, ctc_master_filed, ctc_slave_field, sai_key_field_bmp));
    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_fields_lookup_type(ctc_master_filed, ctc_slave_field, &lookup_type));
    p_acl_table->lookup_type = lookup_type;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_group_lookup_type(uint8 lchip, ctc_sai_acl_group_t* p_acl_group)
{
    int32  status = SAI_STATUS_SUCCESS;
    uint32 lookup_type = CTC_ACL_TCAM_LKUP_TYPE_L2;
    uint32 sai_key_field_bmp[(SAI_ACL_KEY_ATTR_NUM-1)/32 + 1] = {0};
    uint32 ctc_slave_field[(CTC_FIELD_KEY_NUM-1)/32 + 1] = {0};
    uint32 ctc_master_filed[(CTC_FIELD_KEY_NUM-1)/32 + 1] = {0};
    ctc_slistnode_t* table_node = NULL;
    ctc_sai_acl_table_t* p_acl_table = NULL;
    ctc_sai_acl_group_member_t* p_group_member = NULL;

    if (!CTC_SLIST_ISEMPTY(p_acl_group->member_list))
    {
        /* check group's each table key field satisfy group's bind point or not */
        CTC_SAI_ERROR_RETURN(_ctc_sai_acl_check_group_key_field(lchip, p_acl_group));
        CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
        {
            p_group_member = (ctc_sai_acl_group_member_t*)table_node;
            p_acl_table = ctc_sai_db_get_object_property(lchip, p_group_member->table_id);
            _ctc_sai_acl_mapping_sai_table_field(lchip, p_acl_table, ctc_master_filed, ctc_slave_field, sai_key_field_bmp);
        }
        /* Check all master key field which selected by its member, e.g. IN_PORTS, IN_PORT or SRC_PORT, OUT_PORTS, OUT_PORT, be consistent with each other. */
        status = _ctc_sai_acl_check_master_key_field(sai_key_field_bmp, p_acl_group->group_stage, p_acl_group->bind_point_list);
        if (SAI_STATUS_SUCCESS != status)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The group's table master field is inconsistent!\n");
        }

        CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_fields_lookup_type(ctc_master_filed, ctc_slave_field, &lookup_type));
    }
    p_acl_group->lookup_type = lookup_type;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_mapping_entry_tcam_type(uint32 attr_count, const sai_attribute_t *attr_list, ctc_acl_tcam_lkup_type_t tcam_lkup_type, uint32* p_key_type)
{
    uint8  is_ipv6 = 0;
    uint32 index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t* attr_value = NULL;

    *p_key_type = CTC_ACL_KEY_NUM;

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        is_ipv6 = 1;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        is_ipv6 = 1;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        is_ipv6 = 1;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        is_ipv6 = 1;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        if (SAI_ACL_IP_TYPE_IPV6ANY == attr_value->aclfield.data.s32)
        {
            is_ipv6 = 1;
        }
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        if (0x86DD == attr_value->aclfield.data.u16)
        {
            is_ipv6 = 1;
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable && is_ipv6)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_DST_IP, &attr_value, &index));
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable && is_ipv6)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (CTC_ACL_TCAM_LKUP_TYPE_L2 == tcam_lkup_type)
    {
        *p_key_type = CTC_ACL_KEY_MAC;
    }
    else if (CTC_ACL_TCAM_LKUP_TYPE_L2_L3 == tcam_lkup_type)
    {
        if (is_ipv6)
        {
            *p_key_type = CTC_ACL_KEY_MAC_IPV6;
        }
        else
        {
            *p_key_type = CTC_ACL_KEY_MAC_IPV4;
        }

    }
    else if (CTC_ACL_TCAM_LKUP_TYPE_L3 == tcam_lkup_type)
    {
        if (is_ipv6)
        {
            *p_key_type = CTC_ACL_KEY_IPV6;

        }
        else
        {
            *p_key_type = CTC_ACL_KEY_IPV4;
        }
    }
    else if (CTC_ACL_TCAM_LKUP_TYPE_L3_EXT == tcam_lkup_type)
    {
        if (is_ipv6)
        {
            *p_key_type = CTC_ACL_KEY_IPV6_EXT;
        }
        else
        {
            *p_key_type = CTC_ACL_KEY_IPV4_EXT;
        }
    }
    else if (CTC_ACL_TCAM_LKUP_TYPE_L2_L3_EXT == tcam_lkup_type)
    {
        if (is_ipv6)
        {
            *p_key_type = CTC_ACL_KEY_MAC_IPV6;
        }
        else
        {
            *p_key_type = CTC_ACL_KEY_MAC_IPV4_EXT;
        }
    }
    else if (CTC_ACL_TCAM_LKUP_TYPE_UDF == tcam_lkup_type)
    {
        *p_key_type = CTC_ACL_KEY_UDF;
    }

    return SAI_STATUS_SUCCESS;
}

static void
_ctc_sai_acl_get_entry_combined_priority(sai_acl_table_group_type_t group_type,
                                         uint16 group_mem_priority,
                                         uint16 entry_priority,
                                         uint16 pipeline_stage,
                                         uint32 table_id,
                                         uint32 *p_combined_priority)
{
    if (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == group_type)
    {
        /* entry priority format as: s/p type(1bit) + bind point type(stage)(3bit) + group member priority(12bit) + entry priority (16 bit) */
        *p_combined_priority = 0x00000000 | (SAI_ACL_BIND_POINT_TYPE_SWITCH - pipeline_stage) << 28 | group_mem_priority << 16 | entry_priority;
    }
    else if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == group_type)
    {
        /* entry priority format as: s/p type(1bit) + bind point type(stage)(3bit) + table id(12bit) + entry priority (16 bit)*/
        *p_combined_priority = 0x80000000 | (SAI_ACL_BIND_POINT_TYPE_SWITCH - pipeline_stage) << 28 | table_id << 16 | entry_priority;
    }

    return;
}

static sai_status_t
_ctc_sai_acl_table_group_db_deinit_cb(void* bucket_data, void* user_data)
{
    ctc_slistnode_t *cur_node = NULL;
    ctc_slistnode_t *next_node = NULL;
    ctc_sai_oid_property_t *p_oid_property = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_group_member_t *p_acl_group_member = NULL;
    ctc_sai_acl_bind_point_info_t *p_acl_bind_point = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_acl_group = (ctc_sai_acl_group_t*)(p_oid_property->data);

    CTC_SLIST_LOOP_DEL(p_acl_group->member_list, cur_node, next_node)
    {
        p_acl_group_member = (ctc_sai_acl_group_member_t*)cur_node;
        mem_free(p_acl_group_member);
    }
    ctc_slist_free(p_acl_group->member_list);

    CTC_SLIST_LOOP_DEL(p_acl_group->bind_points, cur_node, next_node)
    {
        p_acl_bind_point = (ctc_sai_acl_bind_point_info_t*)cur_node;
        mem_free(p_acl_bind_point);
    }
    ctc_slist_free(p_acl_group->bind_points);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_table_db_deinit_cb(void* bucket_data, void* user_data)
{
    ctc_slistnode_t *cur_node = NULL;
    ctc_slistnode_t *next_node = NULL;
    ctc_sai_oid_property_t *p_oid_property = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_table_member_t *p_acl_table_member = NULL;
    ctc_sai_acl_table_group_list_t *p_acl_table_group_list = NULL;
    ctc_sai_acl_bind_point_info_t *p_acl_bind_point = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_acl_table = (ctc_sai_acl_table_t*)(p_oid_property->data);

    CTC_SLIST_LOOP_DEL(p_acl_table->entry_list, cur_node, next_node)
    {
        p_acl_table_member = (ctc_sai_acl_table_member_t*)cur_node;
        mem_free(p_acl_table_member);
    }
    ctc_slist_free(p_acl_table->entry_list);

    CTC_SLIST_LOOP_DEL(p_acl_table->group_list, cur_node, next_node)
    {
        p_acl_table_group_list = (ctc_sai_acl_table_group_list_t*)cur_node;
        mem_free(p_acl_table_group_list);
    }
    ctc_slist_free(p_acl_table->group_list);

    CTC_SLIST_LOOP_DEL(p_acl_table->bind_points, cur_node, next_node)
    {
        p_acl_bind_point = (ctc_sai_acl_bind_point_info_t*)cur_node;
        mem_free(p_acl_bind_point);
    }
    ctc_slist_free(p_acl_table->bind_points);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_entry_db_deinit_cb(void* bucket_data, void* user_data)
{
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    ctc_sai_oid_property_t *p_oid_property = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_acl_entry = (ctc_sai_acl_entry_t*)(p_oid_property->data);

    mem_free(p_acl_entry->key_attr_list);
    mem_free(p_acl_entry->action_attr_list);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_add_bind_point_key_field_usw(uint8 lchip, sai_object_id_t bind_point_oid, uint32 entry_id)
{
    uint32 bind_point_value = 0;
    sai_acl_bind_point_type_t bind_point_type = 0;
    ctc_object_id_t ctc_object_id = {0};
    ctc_field_key_t field_key;
    ctc_field_port_t field_port;
    ctc_field_port_t field_port_mask;

    sal_memset(&field_key, 0, sizeof(ctc_field_key_t));
    sal_memset(&field_port, 0, sizeof(ctc_field_port_t));
    sal_memset(&field_port_mask, 0, sizeof(ctc_field_port_t));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, bind_point_oid, &ctc_object_id);
    bind_point_value = ctc_object_id.value;
    if (SAI_OBJECT_TYPE_PORT == ctc_object_id.type)
    {
        bind_point_type = SAI_ACL_BIND_POINT_TYPE_PORT;
    }
    else if (SAI_OBJECT_TYPE_LAG == ctc_object_id.type)
    {
        bind_point_type = SAI_ACL_BIND_POINT_TYPE_LAG;
    }
    else if (SAI_OBJECT_TYPE_VLAN == ctc_object_id.type)
    {
        bind_point_type = SAI_ACL_BIND_POINT_TYPE_VLAN;
    }
    else if (SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type)
    {
        bind_point_type = SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE;
    }
    else if (SAI_OBJECT_TYPE_SWITCH == ctc_object_id.type)
    {
        bind_point_type = SAI_ACL_BIND_POINT_TYPE_SWITCH;
    }

    switch (bind_point_type)
    {
        case SAI_ACL_BIND_POINT_TYPE_PORT:
        case SAI_ACL_BIND_POINT_TYPE_LAG:
            field_port.type = CTC_FIELD_PORT_TYPE_GPORT;
            field_port.gport = bind_point_value;
            field_port_mask.gport = 0xFFFFFFFF;
            field_key.type  = CTC_FIELD_KEY_PORT;
            field_key.ext_data = &field_port;
            field_key.ext_mask = &field_port_mask;
            ctcs_acl_add_key_field(lchip, entry_id, &field_key);
            break;
        case SAI_ACL_BIND_POINT_TYPE_VLAN:
            ctc_sai_vlan_get_vlan_id(bind_point_oid, (uint16*)(&bind_point_value));
            field_key.type  = CTC_FIELD_KEY_SVLAN_ID;
            field_key.data = bind_point_value;
            field_key.mask = 0xFFF;
            ctcs_acl_add_key_field(lchip, entry_id, &field_key);
            break;
        case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
            ctc_sai_oid_get_l3if_id(bind_point_oid, (uint16*)(&bind_point_value));
            field_key.type  = CTC_FIELD_KEY_INTERFACE_ID;
            field_key.data = bind_point_value;
            field_key.mask = 0x1FFF;
            ctcs_acl_add_key_field(lchip, entry_id, &field_key);
            break;
        case SAI_ACL_BIND_POINT_TYPE_SWITCH:
            /* do nothing */
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_store_entry_key_and_action_attributes(uint8 lchip, uint32 attr_count, const sai_attribute_t *attr_list, ctc_sai_acl_entry_t *p_acl_entry)
{
    uint32 ii = 0;    /* need use uint32 */

    /* pay attention to the list struct in the aclfield and aclaction which may cause bug */

    /* mapping key attribute list */
    for (ii = 0; ii < attr_count; ii++)
    {
        if ((attr_list[ii].id < SAI_ACL_ENTRY_ATTR_FIELD_START) || (SAI_ACL_ENTRY_ATTR_FIELD_END < attr_list[ii].id))
        {
            continue;
        }

        sal_memcpy(&p_acl_entry->key_attr_list[attr_list[ii].id - SAI_ACL_ENTRY_ATTR_FIELD_START], &attr_list[ii], sizeof(sai_attribute_t));
    }

    /* mapping action attribute list */
    for (ii = 0; ii < attr_count; ii++)
    {
        if ((attr_list[ii].id < SAI_ACL_ENTRY_ATTR_ACTION_START) || (SAI_ACL_ENTRY_ATTR_ACTION_END < attr_list[ii].id))
        {
            continue;
        }

        sal_memcpy(&p_acl_entry->action_attr_list[attr_list[ii].id - SAI_ACL_ENTRY_ATTR_ACTION_START], &attr_list[ii], sizeof(sai_attribute_t));
    }

    return SAI_STATUS_SUCCESS;
}

static void
_ctc_sai_acl_mapping_tcam_block_base(sai_acl_stage_t acl_stage, sai_acl_bind_point_type_t bind_point_type, sai_acl_table_group_type_t table_group_type, uint8* p_tcam_block_base)
{
    if (SAI_ACL_STAGE_INGRESS == acl_stage)
    {
        *p_tcam_block_base = (SAI_ACL_BIND_POINT_TYPE_SWITCH == bind_point_type)
                             ? ACL_INGRESS_GLOBAL_TCAM_BLOCK_BASE
                             : ((SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == table_group_type)
                             ? ACL_INGRESS_SEQUENT_TCAM_BLOCK_BASE : ACL_INGRESS_PARAELL_TCAM_BLOCK_BASE);
    }
    else
    {
        *p_tcam_block_base = ACL_EGRESS_PARAELL_TCAM_BLOCK_BASE;
    }

    return;
}

#define ________COMMON_ACL_PROCESS________
static sai_status_t
_ctc_sai_acl_add_acl_entry_to_sdk_usw(uint8 lchip, sai_object_key_t *key, uint32 ctc_group_id, uint8 group_priority, sai_object_id_t entry_object_id, uint32 ctc_entry_id, uint32 entry_priority,
                                      ctc_sai_acl_entry_t *p_acl_entry, const sai_attribute_t *update_attr)
{
    uint8  first_free = 1;
    //uint8  is_add_operation = 0;
    uint8  bmp_count = 0;
    int32  status = SAI_STATUS_SUCCESS;
    uint32 bmp_start = 0;
    uint32 ii = 0;
    uint32 rr = 0;
    uint32 loop = 0;
    uint32 key_count = 0;
    uint32 action_count = 0;
    uint32 temp_index = 0;
    bool   trap_enable = false;
    bool   is_copy_action = false;
    ctc_object_id_t trap_id;
    ctc_object_id_t ctc_entry_object_id;
    ctc_object_id_t ctc_policer_object_id;
    ctc_acl_to_cpu_t acl_cpu;
    ctc_acl_entry_t acl_entry;
    ctc_acl_field_action_t acl_field_action;
    ctc_field_key_t key_fields_array[CTC_FIELD_KEY_NUM];
    ctc_acl_field_action_t acl_action_fields_array[CTC_ACL_FIELD_ACTION_NUM];
    sai_attribute_t key_attr_list[SAI_ACL_KEY_ATTR_NUM];
    sai_attribute_t action_attr_list[SAI_ACL_ACTION_ATTR_NUM];

    sal_memset(&trap_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_entry_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_policer_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&acl_cpu, 0, sizeof(ctc_acl_to_cpu_t));
    sal_memset(&acl_entry, 0, sizeof(ctc_acl_entry_t));
    sal_memset(key_fields_array, 0, sizeof(key_fields_array));
    /* key and action must be memory set to zero */
    sal_memset(acl_action_fields_array, 0, sizeof(acl_action_fields_array));
    sal_memset(key_attr_list, 0, sizeof(key_attr_list));
    sal_memset(action_attr_list, 0, sizeof(action_attr_list));

    if (update_attr)
    {
        if (update_attr->id >= SAI_ACL_ENTRY_ATTR_FIELD_START && update_attr->id <= SAI_ACL_ENTRY_ATTR_FIELD_END)
        {
            /* update key field */
            if (update_attr->id == SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS)
            {
                /* special process for SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS */
                for (ii = 0; ii < 8; ii++)
                {
                    /* do not need care remove entry operation fail or not */
                    ctcs_acl_uninstall_entry(lchip, ctc_entry_id + ii);
                    ctcs_acl_remove_entry(lchip, ctc_entry_id + ii);
                }
                sal_memcpy(key_attr_list, p_acl_entry->key_attr_list, sizeof(key_attr_list));
                sal_memcpy(&key_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START], update_attr, sizeof(sai_attribute_t));
                sal_memcpy(action_attr_list, p_acl_entry->action_attr_list, sizeof(action_attr_list));

                status = status?:_ctc_sai_acl_mapping_entry_key_fields(lchip, key, group_priority, key_attr_list, key_fields_array, &key_count, &bmp_count, &bmp_start);
                status = status?:_ctc_sai_acl_mapping_acl_entry_action_fields(lchip, key, group_priority, entry_object_id, action_attr_list, acl_action_fields_array, &action_count);

                for (ii = 0; ii < bmp_count; ii++)
                {
                    acl_entry.key_type = p_acl_entry->key_type;
                    acl_entry.mode = 1;
                    acl_entry.entry_id = ctc_entry_id + ii;
                    acl_entry.priority_valid = 1;
                    acl_entry.priority = entry_priority;
                    status = status?:ctcs_acl_add_entry(lchip, ctc_group_id, &acl_entry);
                }

                for (ii = 0; ii < bmp_count; ii++)
                {
                    for (loop = 0; loop < key_count; loop++)
                    {
                        status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id + ii, &key_fields_array[loop]);
                    }
                }

                /* need re-add port field for each entry */
                for (ii = 0; ii < bmp_count; ii++)
                {
                    status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id + ii, &key_fields_array[bmp_start + ii]);
                }

                for (ii = 0; ii < bmp_count; ii++)
                {
                    status = status?:_ctc_sai_acl_add_bind_point_key_field_usw(lchip, key->key.object_id, ctc_entry_id + ii);
                }

                for (ii = 0; ii < bmp_count; ii++)
                {
                    for (loop = 0; loop < action_count; loop++)
                    {
                        status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id + ii, &acl_action_fields_array[loop]);
                    }
                }

                if (p_acl_entry->entry_valid)
                {
                    for (ii = 0; ii < bmp_count; ii++)
                    {
                        status = status?:ctcs_acl_install_entry(lchip, ctc_entry_id + ii);
                    }
                }
                if (CTC_E_NONE != status)
                {
                    for (rr = 0; rr < (bmp_count?:1); rr++)
                    {
                        ctcs_acl_uninstall_entry(lchip, ctc_entry_id + rr);
                        ctcs_acl_remove_entry(lchip, ctc_entry_id + rr);
                    }
                    goto error0;
                }
            }
            else
            {
                status = status?:ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                if (update_attr->value.aclfield.enable)
                {
                    sal_memcpy(&key_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START], update_attr, sizeof(sai_attribute_t));
                    status = _ctc_sai_acl_mapping_entry_key_fields(lchip, key, group_priority, key_attr_list, key_fields_array, &key_count, NULL, NULL);

                    for (ii = 0; ii < key_count; ii++)
                    {
                        status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id, &key_fields_array[ii]);
                    }
                    status = status?:ctcs_acl_install_entry(lchip, ctc_entry_id);
                }
                else
                {
                    sal_memcpy(&key_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START], update_attr, sizeof(sai_attribute_t));
                    key_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable = 1;
                    status = _ctc_sai_acl_mapping_entry_key_fields(lchip, key, group_priority, key_attr_list, key_fields_array, &key_count, NULL, NULL);

                    for (ii = 0; ii < key_count; ii++)
                    {
                        status = status?:ctcs_acl_remove_key_field(lchip, ctc_entry_id, &key_fields_array[ii]);
                    }
                }
                if (CTC_E_NONE != status)
                {
                    ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                    ctcs_acl_remove_entry(lchip, ctc_entry_id);
                    goto error0;
                }
            }
        }
        else if (update_attr->id >= SAI_ACL_ENTRY_ATTR_ACTION_START && update_attr->id <= SAI_ACL_ENTRY_ATTR_ACTION_END)
        {
            /* update action field */
            if (update_attr->value.aclaction.enable)
            {
                if (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI == update_attr->id)
                {
                    sal_memcpy(&action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], update_attr, sizeof(sai_attribute_t));
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    trap_enable = p_acl_entry->action_attr_list[temp_index].value.aclaction.enable;
                    if (trap_enable && (update_attr->value.aclaction.parameter.s32 == SAI_PACKET_ACTION_COPY_CANCEL
                        || update_attr->value.aclaction.parameter.s32 == SAI_PACKET_ACTION_DENY
                        || update_attr->value.aclaction.parameter.s32 == SAI_PACKET_ACTION_TRANSIT))
                    {
                        return SAI_STATUS_NOT_SUPPORTED;
                    }

                    if (trap_enable)
                    {
                        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.oid, &trap_id);
                    }
                    acl_cpu.mode = trap_enable ? CTC_ACL_TO_CPU_MODE_TO_CPU_COVER : CTC_ACL_TO_CPU_MODE_TO_CPU_NOT_COVER;
                    acl_cpu.cpu_reason_id = trap_enable ? trap_id.value : 0;

                    if (SAI_PACKET_ACTION_DROP == update_attr->value.aclaction.parameter.s32)
                    {
                        /* add discard */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        acl_field_action.data0 = CTC_QOS_COLOR_NONE;
                        status = ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_FORWARD == update_attr->value.aclaction.parameter.s32)
                    {
                        /* remove discard */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_COPY == update_attr->value.aclaction.parameter.s32)
                    {
                        /* add copy to cpu */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        acl_field_action.ext_data = &acl_cpu;
                        status = ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_COPY_CANCEL == update_attr->value.aclaction.parameter.s32)
                    {
                        /** Cancel copy the packet to CPU. */
                        /* remove copy the packet to CPU */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_TRAP == update_attr->value.aclaction.parameter.s32)
                    {
                        /** This is a combination of SAI packet action COPY and DROP. */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        acl_field_action.ext_data = &acl_cpu;
                        status = ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        acl_field_action.data0 = CTC_QOS_COLOR_NONE;
                        status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_LOG == update_attr->value.aclaction.parameter.s32)
                    {
                        /** This is a combination of SAI packet action COPY and FORWARD. */
                        /* remove discard and copy to cpu */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        acl_field_action.ext_data = &acl_cpu;
                        status = ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        acl_field_action.data0 = CTC_QOS_COLOR_NONE;
                        status = status?:ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_DENY == update_attr->value.aclaction.parameter.s32)
                    {
                        /** This is a combination of SAI packet action COPY_CANCEL and DROP */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        acl_field_action.data0 = CTC_QOS_COLOR_NONE;
                        status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    else if (SAI_PACKET_ACTION_TRANSIT == update_attr->value.aclaction.parameter.s32)
                    {
                        /** This is a combination of SAI packet action COPY_CANCEL and FORWARD */
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                        status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                        sal_memset(&acl_field_action, 0, sizeof(ctc_acl_field_action_t));
                        acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                        status = status?:ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    }
                    if (CTC_E_NONE != status)
                    {
                        ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                        ctcs_acl_remove_entry(lchip, ctc_entry_id);
                    }

                    /* finish updating and return directly */
                    return status;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    is_copy_action = p_acl_entry->action_attr_list[temp_index].value.aclaction.enable && (p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_COPY
                    || p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_TRAP
                    || p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.s32 == SAI_PACKET_ACTION_LOG);
                    if (!is_copy_action)
                    {
                        return SAI_STATUS_NOT_SUPPORTED;
                    }
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, update_attr->value.aclaction.parameter.oid, &trap_id);
                    acl_cpu.mode = CTC_ACL_TO_CPU_MODE_TO_CPU_COVER;
                    acl_cpu.cpu_reason_id = trap_id.value;
                    acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                    acl_field_action.ext_data = &acl_cpu;
                    status = ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_field_action);
                    if (CTC_E_NONE != status)
                    {
                        ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                        ctcs_acl_remove_entry(lchip, ctc_entry_id);
                    }
                    return status;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    if (p_acl_entry->action_attr_list[temp_index].value.aclaction.enable)
                    {
                        return SAI_STATUS_ITEM_ALREADY_EXISTS;
                    }

                    sal_memcpy(&action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], update_attr, sizeof(sai_attribute_t));

                }
                else
                {
                    sal_memcpy(&action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], update_attr, sizeof(sai_attribute_t));
                }

                if (SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER == update_attr->id && p_acl_entry->action_attr_list[SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.enable)
                {
                    /* disable old policer id */
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_ENTRY, entry_object_id, &ctc_entry_object_id);
                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_POLICER, p_acl_entry->action_attr_list[SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.parameter.oid, &ctc_policer_object_id);
                    status = status?:ctc_sai_policer_acl_set_policer(lchip, ctc_entry_object_id.value, ctc_policer_object_id.value, false);
                }

                status = status?:_ctc_sai_acl_mapping_acl_entry_action_fields(lchip, key, group_priority, entry_object_id, action_attr_list, acl_action_fields_array, &action_count);
                for (ii = 0; ii < action_count; ii++)
                {
                    if (acl_action_fields_array[ii].data0)
                    {
                        status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_action_fields_array[ii]);
                    }
                }

                if (CTC_E_NONE != status)
                {
                    ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                    ctcs_acl_remove_entry(lchip, ctc_entry_id);
                }
                return status;
            }
            else
            {
                if (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID == update_attr->id
                    || SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI == update_attr->id)
                {
                    sal_memcpy(&action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], update_attr, sizeof(sai_attribute_t));
                    action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.enable = 1;

                    status = _ctc_sai_acl_mapping_acl_entry_action_fields(lchip, key, group_priority, entry_object_id, action_attr_list, acl_action_fields_array, &action_count);

                    for (ii = 0; ii < action_count; ii++)
                    {
                        status = status?:ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_action_fields_array[ii]);
                    }
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    trap_enable = p_acl_entry->action_attr_list[temp_index].value.aclaction.enable;
                    if (trap_enable)
                    {
                        return SAI_STATUS_NOT_SUPPORTED;
                    }
                    acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                    status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    acl_field_action.type = CTC_ACL_FIELD_ACTION_DISCARD;
                    status = status?:ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);
                    if (CTC_E_NONE != status)
                    {
                        ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                        ctcs_acl_remove_entry(lchip, ctc_entry_id);
                    }
                    return status;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    if (!p_acl_entry->action_attr_list[temp_index].value.aclaction.enable)
                    {
                        return SAI_STATUS_SUCCESS;
                    }

                    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP, p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.oid, &trap_id);

                    acl_cpu.mode = CTC_ACL_TO_CPU_MODE_TO_CPU_COVER;
                    acl_cpu.cpu_reason_id = trap_id.value;
                    acl_field_action.type = CTC_ACL_FIELD_ACTION_CP_TO_CPU;
                    acl_field_action.ext_data = &acl_cpu;
                    status = ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_field_action);

                    if (CTC_E_NONE != status)
                    {
                        ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                        ctcs_acl_remove_entry(lchip, ctc_entry_id);
                    }
                    return status;
                }
                else if (SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE == update_attr->id)
                {
                    temp_index = SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE - SAI_ACL_ENTRY_ATTR_ACTION_START;
                    action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.parameter.oid = p_acl_entry->action_attr_list[temp_index].value.aclaction.parameter.oid;
                    action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.enable = 1;
                }
                else
                {
                    sal_memcpy(&action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], update_attr, sizeof(sai_attribute_t));
                    action_attr_list[update_attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START].value.aclaction.enable = 1;
                }

                status = _ctc_sai_acl_mapping_acl_entry_action_fields(lchip, key, group_priority, entry_object_id, action_attr_list, acl_action_fields_array, &action_count);
                for (ii = 0; ii < action_count; ii++)
                {
                    status = status?:ctcs_acl_remove_action_field(lchip, ctc_entry_id, &acl_action_fields_array[ii]);
                }
            }

            if (CTC_E_NONE != status)
            {
                ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
                ctcs_acl_remove_entry(lchip, ctc_entry_id);
            }
            return status;
        }
        else if (SAI_ACL_ENTRY_ATTR_PRIORITY == update_attr->id)
        {
            status = ctcs_acl_set_entry_priority(lchip, ctc_entry_id, entry_priority);
        }
        else if (SAI_ACL_ENTRY_ATTR_ADMIN_STATE == update_attr->id)
        {
            if (update_attr->value.booldata)
            {
                status = ctcs_acl_install_entry(lchip, ctc_entry_id);
            }
            else
            {
                ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
            }
        }
        if (CTC_E_NONE != status)
        {
            ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
            ctcs_acl_remove_entry(lchip, ctc_entry_id);
        }
        return status;
    }
    else
    {
        sal_memcpy(key_attr_list, p_acl_entry->key_attr_list, sizeof(key_attr_list));
        sal_memcpy(action_attr_list, p_acl_entry->action_attr_list, sizeof(action_attr_list));

        status = _ctc_sai_acl_mapping_entry_key_fields(lchip, key, group_priority, key_attr_list, key_fields_array, &key_count, &bmp_count, &bmp_start);
        status = status?:_ctc_sai_acl_mapping_acl_entry_action_fields(lchip, key, group_priority, entry_object_id, action_attr_list, acl_action_fields_array, &action_count);

        /* first add one entry */
        acl_entry.key_type = p_acl_entry->key_type;
        acl_entry.mode = 1;
        acl_entry.entry_id = ctc_entry_id;
        acl_entry.priority_valid = 1;
        acl_entry.priority = entry_priority;
        status = status?:ctcs_acl_add_entry(lchip, ctc_group_id, &acl_entry);

        /* enable port bitmap */
        if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        {
            for (ii = 1; ii < bmp_count; ii++)
            {
                acl_entry.entry_id = ctc_entry_id + ii;
                status = status?:ctcs_acl_add_entry(lchip, ctc_group_id, &acl_entry);
            }
        }

        /* second add key field */
        for (ii = 0; ii < key_count; ii++)
        {
            status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id, &key_fields_array[ii]);
        }

        if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        {
            for (ii = 1; ii < bmp_count; ii++)
            {
                for (loop = 0; loop < key_count; loop++)
                {
                    status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id + ii, &key_fields_array[loop]);
                }
            }

            /* need re-add port field for each entry */
            for (ii = 0; ii < bmp_count; ii++)
            {
                status = status?:ctcs_acl_add_key_field(lchip, ctc_entry_id + ii, &key_fields_array[bmp_start + ii]);
            }
        }

        /* entry must include bind point info */
        _ctc_sai_acl_add_bind_point_key_field_usw(lchip, key->key.object_id, ctc_entry_id);
        if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        {
            for (ii = 1; ii < bmp_count; ii++)
            {
                status = status?:_ctc_sai_acl_add_bind_point_key_field_usw(lchip, key->key.object_id, ctc_entry_id + ii);
            }
        }

        /* third add action field */
        for (ii = 0; ii < action_count; ii++)
        {
            status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id, &acl_action_fields_array[ii]);
        }
        if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
        {
            for (ii = 1; ii < bmp_count; ii++)
            {
                for (loop = 0; loop < action_count; loop++)
                {
                    status = status?:ctcs_acl_add_action_field(lchip, ctc_entry_id + ii, &acl_action_fields_array[loop]);
                }
            }
        }

        /* fourth install entry */
        if (p_acl_entry->entry_valid)
        {
            status = status?:ctcs_acl_install_entry(lchip, ctc_entry_id);
            if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
            {
                for (ii = 1; ii < bmp_count; ii++)
                {
                    status = status?:ctcs_acl_install_entry(lchip, ctc_entry_id + ii);
                }
            }
        }
    
        if (CTC_E_NONE != status)
        {
            for (rr = 0; rr < (bmp_count?:1); rr++)
            {
                ctcs_acl_uninstall_entry(lchip, ctc_entry_id + rr);
                ctcs_acl_remove_entry(lchip, ctc_entry_id + rr);
            }
        }
        return status;
    }

error0:
    /* need free the memory generated by mapping sai key and action attribute to sdk key and action field, sdk will store these fields in its own sw table */
    for (ii = 0; ii < key_count; ii++)
    {
        if (key_fields_array[ii].ext_data && key_fields_array[ii].ext_mask && key_fields_array[ii].type != CTC_FIELD_KEY_PORT)
        {
            mem_free(key_fields_array[ii].ext_data);
            mem_free(key_fields_array[ii].ext_mask);
        }
        else if (key_fields_array[ii].ext_data && key_fields_array[ii].ext_mask && key_fields_array[ii].type == CTC_FIELD_KEY_PORT && first_free)
        {
            mem_free(key_fields_array[ii].ext_data);
            mem_free(key_fields_array[ii].ext_mask);
            first_free = 0;
        }
    }

    for (ii = 0; ii < action_count; ii++)
    {
        if (acl_action_fields_array[ii].ext_data)
        {
            mem_free(acl_action_fields_array[ii].ext_data);
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_acl_add_acl_entry_to_sdk(uint8 lchip, sai_object_key_t *key, uint32 ctc_group_id, uint8 group_priority, sai_object_id_t entry_object_id, uint32 ctc_entry_id, uint32 entry_priority,
                                  ctc_sai_acl_entry_t *p_acl_entry, const sai_attribute_t *update_attr)
{
    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_add_acl_entry_to_sdk_usw(lchip, key, ctc_group_id, group_priority, entry_object_id, ctc_entry_id, entry_priority, p_acl_entry, update_attr));

    return SAI_STATUS_SUCCESS;
}

#define ________BIND_ACL_PROCESS________

static sai_status_t
_ctc_sai_acl_bind_point_acl_entry_remove(sai_object_key_t *key, const sai_attribute_t *attr, sai_object_id_t entry_object_id)
{
    uint8 lchip = 0;
    uint8 loop = 0;
    uint8 entry_count = 0;
    uint32 entry_index = 0;
    uint32 bind_point_value = 0;
    uint32 *p_ctc_entry_id = NULL;
    uint64 hw_entry_id = 0;
    sai_attr_id_t attr_id = 0;
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    ctc_object_id_t ctc_entry_object_id = {0};
    ctc_object_id_t ctc_key_object_id = {0};
    ctc_sai_acl_entry_t *p_acl_entry = NULL;

    attr_id = attr->id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr_id, &bind_point_type, &bind_point_stage);

    p_acl_entry = ctc_sai_db_get_object_property(lchip, entry_object_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL entry is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, entry_object_id, &ctc_entry_object_id);
    entry_index = ctc_entry_object_id.value;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    bind_point_value = ctc_key_object_id.value;
    hw_entry_id = (uint64)1 << 63 | (uint64)bind_point_type << 60 | bind_point_value << 28 | entry_index;

    p_ctc_entry_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_entry_id));
    if (NULL == p_ctc_entry_id)
    {
        /* no such entry in sdk, may have not created already */
        return SAI_STATUS_SUCCESS;
    }

    if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
    {
        entry_count = 8;
    }
    else
    {
        entry_count = 1;
    }

    for (loop = 0; loop < entry_count; loop++)
    {
        ctcs_acl_uninstall_entry(lchip, *p_ctc_entry_id + loop);
        ctcs_acl_remove_entry(lchip, *p_ctc_entry_id + loop);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, *p_ctc_entry_id + loop);
    }
    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_entry_id));
    mem_free(p_ctc_entry_id);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_bind_point_acl_entry_add(sai_object_key_t *key, const sai_attribute_t *attr,
                                      uint32 ctc_group_id, uint8 group_priority, sai_object_id_t entry_object_id, uint32 entry_priority)
{
    uint8 lchip = 0;
    uint8 loop = 0;
    uint32 entry_index = 0;
    uint32 bind_point_value = 0;
    uint32 ctc_entry_id = 0;
    uint32 rsv_entry_id = 0;
    uint32 *p_ctc_entry_id = NULL;
    uint64 hw_entry_id = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_entry_object_id = {0};
    ctc_object_id_t ctc_key_object_id = {0};
    ctc_acl_entry_t acl_entry;
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;

    sal_memset(&acl_entry, 0, sizeof(ctc_acl_entry_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(entry_object_id, &lchip));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, entry_object_id, &ctc_entry_object_id);
    entry_index = ctc_entry_object_id.value;
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr->id, &bind_point_type, &bind_point_stage);
    p_acl_entry = ctc_sai_db_get_object_property(lchip, entry_object_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL entry is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    bind_point_value = ctc_key_object_id.value;

    hw_entry_id = (uint64)1 << 63 | (uint64)bind_point_type << 60 | bind_point_value << 28 | entry_index;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, &ctc_entry_id), status, error0);
    if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
    {
        for (loop = 0; loop < 7; loop++)
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, &rsv_entry_id), status, error1);
        }
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_add_acl_entry_to_sdk(lchip, key, ctc_group_id, group_priority, entry_object_id, ctc_entry_id, entry_priority, p_acl_entry, NULL), status, error1);

    /* after all these operation succeed, store the hw_entry_id and sdk entry id into db */
    MALLOC_ZERO(MEM_ACL_MODULE, p_ctc_entry_id, sizeof(uint32));
    if (NULL == p_ctc_entry_id)
    {
        status = SAI_STATUS_NO_MEMORY;
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry memory\n");
        goto error2;
    }
    *p_ctc_entry_id = ctc_entry_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_entry_id), (void*)(p_ctc_entry_id)), status, error3);

    return status;

error3:
    mem_free(p_ctc_entry_id);
error2:
    ctcs_acl_uninstall_entry(lchip, ctc_entry_id);
    ctcs_acl_remove_entry(lchip, ctc_entry_id);
error1:
    if (p_acl_entry->key_attr_list[SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS - SAI_ACL_ENTRY_ATTR_FIELD_START].value.aclfield.enable)
    {
        for (loop = 1; loop <= 7; loop++)
        {
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, ctc_entry_id + loop);
        }
    }
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID, ctc_entry_id);
error0:
    return status;
}

static sai_status_t
_ctc_sai_acl_bind_point_acl_remove(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint32 table_index = 0;
    uint32 bind_point_value = 0;
    uint32 *p_ctc_group_id = NULL;
    uint64 hw_table_id = 0;
    sai_attr_id_t attr_id = 0;
    sai_object_id_t object_id = {0};
    ctc_object_id_t ctc_counter_id = {0};
    ctc_object_id_t ctc_object_id = {0};
    ctc_object_id_t ctc_table_object_id = {0};
    ctc_object_id_t ctc_key_object_id = {0};
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_counter_t* p_acl_counter = NULL;
    ctc_slistnode_t *table_node = NULL;
    ctc_slistnode_t *entry_node = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_sai_acl_table_member_t *p_table_member = NULL;

    /* reserved for bounded object */
    attr_id = attr->id;
    object_id = attr->value.oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, object_id, &ctc_object_id);
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr_id, &bind_point_type, &bind_point_stage);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    bind_point_value = ctc_key_object_id.value;

    if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        p_acl_group = ctc_sai_db_get_object_property(lchip, object_id);

        CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
        {
            p_group_member = (ctc_sai_acl_group_member_t*)table_node;
            p_acl_table = ctc_sai_db_get_object_property(lchip, p_group_member->table_id);

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_acl_table->counter_id, &ctc_counter_id);
            if (SAI_OBJECT_TYPE_ACL_COUNTER == ctc_counter_id.type)
            {
                p_acl_counter = ctc_sai_db_get_object_property(lchip, p_acl_table->counter_id);
                if (NULL == p_acl_counter)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }

                p_acl_counter->ref_cnt--;
                if (0 == p_acl_counter->ref_cnt)
                {
                    CTC_SAI_ERROR_RETURN(ctcs_stats_destroy_statsid(lchip, p_acl_counter->stats_id));
                }
            }

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_group_member->table_id, &ctc_table_object_id);
            table_index = ctc_table_object_id.value;

            hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;

            p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
            if (NULL == p_ctc_group_id)
            {
                /* may not create at all */
                continue;
            }

            CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
            {
                /* for each entry in table */
                p_table_member = (ctc_sai_acl_table_member_t*)entry_node;

                _ctc_sai_acl_bind_point_acl_entry_remove(key, attr, p_table_member->entry_id);
            }

            /* after all entry in sdk group have been removed, destroy the group */
            ctcs_acl_destroy_group(lchip, *p_ctc_group_id);
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, *p_ctc_group_id);
            ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));

            mem_free(p_ctc_group_id);
        }
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        p_acl_table = ctc_sai_db_get_object_property(lchip, object_id);

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_acl_table->counter_id, &ctc_counter_id);
        if (SAI_OBJECT_TYPE_ACL_COUNTER == ctc_counter_id.type)
        {
            p_acl_counter = ctc_sai_db_get_object_property(lchip, p_acl_table->counter_id);
            if (NULL == p_acl_counter)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }

            p_acl_counter->ref_cnt--;
            if (0 == p_acl_counter->ref_cnt)
            {
                CTC_SAI_ERROR_RETURN(ctcs_stats_destroy_statsid(lchip, p_acl_counter->stats_id));
            }
        }
        table_index = ctc_object_id.value;

        hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;

        p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
        if (NULL == p_ctc_group_id)
        {
            /* sdk group may not be crerated */
            return SAI_STATUS_SUCCESS;
        }
        CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
        {
            p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
            _ctc_sai_acl_bind_point_acl_entry_remove(key, attr, p_table_member->entry_id);
        }

        ctcs_acl_destroy_group(lchip, *p_ctc_group_id);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, *p_ctc_group_id);
        ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
        mem_free(p_ctc_group_id);
    }

    return SAI_STATUS_SUCCESS;

}

static sai_status_t
_ctc_sai_acl_bind_point_acl_add(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8  lchip = 0;
    uint8  block_base = 0;
    uint32 gm = 0;
    uint32 bind_point_value = 0;
    uint32 ctc_group_id = 0;
    uint32 table_index = 0;
    uint32 combined_priority = 0;
    uint32 *p_ctc_group_id = NULL;
    uint64 hw_table_id = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_attr_id_t attr_id = 0;
    sai_object_id_t object_id = {0};
    ctc_object_id_t ctc_object_id = {0};
    ctc_object_id_t ctc_key_object_id = {0};
    ctc_object_id_t ctc_table_object_id = {0};
    ctc_acl_group_info_t group_info;
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    ctc_sai_acl_table_t* p_acl_table = NULL;
    ctc_sai_acl_group_t* p_acl_group = NULL;
    ctc_sai_acl_counter_t* p_acl_counter = NULL;
    ctc_slistnode_t *table_node = NULL;
    ctc_slistnode_t *entry_node = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_sai_acl_table_member_t *p_table_member = NULL;
    ctc_stats_statsid_t statsid;

    sal_memset(&group_info, 0, sizeof(ctc_acl_group_info_t));

    /* reserved for bounded object */
    attr_id = attr->id;
    object_id = attr->value.oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    bind_point_value = ctc_key_object_id.value;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, object_id, &ctc_object_id);
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr_id, &bind_point_type, &bind_point_stage);

    /* traverse each table in group and traverse each entry in table */
    if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        p_acl_group = ctc_sai_db_get_object_property(lchip, object_id);
        _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, bind_point_type, p_acl_group->group_type, &block_base);

        group_info.dir = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
        group_info.type = CTC_ACL_GROUP_TYPE_NONE;
        group_info.lchip = lchip;

        gm = 0;
        CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
        {
            p_group_member = (ctc_sai_acl_group_member_t*)table_node;
            p_acl_table = ctc_sai_db_get_object_property(lchip, p_group_member->table_id);
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_group_member->table_id, &ctc_table_object_id);
            table_index = ctc_table_object_id.value;

            group_info.priority = (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type) ? block_base + gm : block_base;

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_acl_table->counter_id, &ctc_object_id);
            if (SAI_OBJECT_TYPE_ACL_COUNTER == ctc_object_id.type)
            {
                p_acl_counter = ctc_sai_db_get_object_property(lchip, p_acl_table->counter_id);
                if (NULL == p_acl_counter)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }

                if (0 == p_acl_counter->stats_id)
                {
                    sal_memset(&statsid, 0, sizeof(ctc_stats_statsid_t));
                    statsid.type = CTC_STATS_STATSID_TYPE_ACL;
                    statsid.dir = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
                    statsid.statsid.acl_priority = group_info.priority;

                    /* create stats with CTC_STATS_MODE_DEFINE mode */
                    CTC_SAI_ERROR_GOTO(ctcs_stats_create_statsid(lchip, &statsid), status, error0);
                    p_acl_counter->stats_id = statsid.stats_id;
                    p_acl_counter->ref_cnt++;
                }
            }

            /* each table in SAI group correspond to a group in Centec SDK */
            hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;

            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &ctc_group_id), status, error0);
            CTC_SAI_ERROR_GOTO(ctcs_acl_create_group(lchip, ctc_group_id, &group_info), status, error0);

            /* only after all operation on this table succeed, add hw_table_id and sdk group id relationship into db */
            MALLOC_ZERO(MEM_ACL_MODULE, p_ctc_group_id, sizeof(uint32));
            *p_ctc_group_id = ctc_group_id;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id), (void*)(p_ctc_group_id)), status, error0);

            CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
            {
                p_table_member = (ctc_sai_acl_table_member_t*)entry_node;

                _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_entry_add(key, attr, ctc_group_id, group_info.priority, p_table_member->entry_id, combined_priority), status, error0);
            }
            gm++;
        }
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        /* for table directly bound */
        p_acl_table = ctc_sai_db_get_object_property(lchip, object_id);
        table_index = ctc_object_id.value;

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, bind_point_type, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &group_info.priority);
        group_info.dir = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
        group_info.type = CTC_ACL_GROUP_TYPE_NONE;
        group_info.lchip = lchip;

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_acl_table->counter_id, &ctc_object_id);
        if (SAI_OBJECT_TYPE_ACL_COUNTER == ctc_object_id.type)
        {
            p_acl_counter = ctc_sai_db_get_object_property(lchip, p_acl_table->counter_id);
            if (NULL == p_acl_counter)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }

            if (0 == p_acl_counter->stats_id)
            {
                sal_memset(&statsid, 0, sizeof(ctc_stats_statsid_t));
                statsid.type = CTC_STATS_STATSID_TYPE_ACL;
                statsid.dir = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS) ? CTC_INGRESS : CTC_EGRESS;
                statsid.statsid.acl_priority = group_info.priority;

                /* create stats with CTC_STATS_MODE_DEFINE mode */
                CTC_SAI_ERROR_GOTO(ctcs_stats_create_statsid(lchip, &statsid), status, error0);
                p_acl_counter->stats_id = statsid.stats_id;
                p_acl_counter->ref_cnt++;
            }
        }

        /* in this situation, make all group priority equal to 0 */
        hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID, &ctc_group_id), status, error0);

        CTC_SAI_ERROR_GOTO(ctcs_acl_create_group(lchip, ctc_group_id, &group_info), status, error0);

        /* only after all operation on this table succeed, add the relationship into db */
        MALLOC_ZERO(MEM_ACL_MODULE, p_ctc_group_id, sizeof(uint32));
        *p_ctc_group_id = ctc_group_id;
        CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id), (void*)p_ctc_group_id), status, error0);

        CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
        {
            p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
            _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, p_table_member->priority, bind_point_type, table_index, &combined_priority);
            CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_entry_add(key, attr, ctc_group_id, group_info.priority, p_table_member->entry_id, combined_priority), status, error0);
        }
    }

    return SAI_STATUS_SUCCESS;

error0:
    _ctc_sai_acl_bind_point_acl_remove(key, attr);
    return status;
}

#define ________BIND_OPERATION________
void _ctc_sai_acl_lag_member_change_cb_fn(uint8 lchip, uint32 linkagg_id, uint32 mem_port, bool change)
{
    uint8  count = 0;
    uint8  loop = 0;
    uint8  acl_priority = 0;
    bool   is_enable = false;
    sai_object_id_t lag_oid;
    sai_object_id_t *p_old_bounded_oid = NULL;
    ctc_object_id_t ctc_object_id;
    ctc_acl_property_t acl_prop[ACL_TCAM_LOOKUP_NUM] = {{0}};
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_slistnode_t *table_node = NULL;

    sal_memset(&lag_oid, 0, sizeof(sai_object_id_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(acl_prop, 0, sizeof(acl_prop));

    lag_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, linkagg_id);
    p_old_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, (void*)(&lag_oid));
    if (NULL == p_old_bounded_oid)
    {
        return;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, *p_old_bounded_oid, &ctc_object_id);
    is_enable = change;

    if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        /* In table directly bind situation, there is no group concept, all the entry(entries) in this table will be installed into tcam0 */
        p_acl_table = (ctc_sai_acl_table_t*)ctc_sai_db_get_object_property(lchip, *p_old_bounded_oid);

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, SAI_ACL_BIND_POINT_TYPE_LAG, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &acl_prop[count].acl_priority);
        acl_prop[count].acl_en = is_enable ? 1 : 0;
        acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == p_acl_table->table_stage) ? CTC_INGRESS : CTC_EGRESS;
        acl_prop[count].tcam_lkup_type = is_enable ? p_acl_table->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_L2;
        count++;
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        p_acl_group = (ctc_sai_acl_group_t*)ctc_sai_db_get_object_property(lchip, *p_old_bounded_oid);
        _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, SAI_ACL_BIND_POINT_TYPE_LAG, p_acl_group->group_type, &acl_priority);

        if (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == p_acl_group->group_type)
        {
            acl_prop[count].acl_en = is_enable ? 1 : 0;
            acl_prop[count].acl_priority = acl_priority;
            acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == p_acl_group->group_stage) ? CTC_INGRESS : CTC_EGRESS;
            acl_prop[count].tcam_lkup_type = is_enable ? p_acl_group->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_L2;
            count++;
        }
        else if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
        {
            /* for parallel */
            CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
            {
                acl_prop[count].acl_en = is_enable ? 1 : 0;
                acl_prop[count].acl_priority = acl_priority + count;
                acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == p_acl_group->group_stage) ? CTC_INGRESS : CTC_EGRESS;
                acl_prop[count].tcam_lkup_type = is_enable ? p_acl_group->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_L2;
                count++;
            }
        }
    }

    for (loop = 0; loop < count; loop++)
    {
        ctcs_port_set_acl_property(lchip, mem_port, &acl_prop[loop]);
    }

    return;
}

/* When this function is used for unbind operation, one should pass the old attribute (That is the attribute used for bind operation)*/
static sai_status_t
_ctc_sai_acl_sdk_lookup_enable_set(sai_object_key_t *key, const sai_attribute_t *attr, uint8 is_enable)
{
    uint8  lchip  = 0;
    uint8  loop   = 0;
    uint8  count  = 0;
    uint8  gchip  = 0;
    uint8  is_bmp = 0;
    uint8  block_base = 0;
    uint16 ii = 0;
    uint16 max_num = 0;
    uint16 cnt = 0;
    uint32 *p_gports = NULL;
    ctc_acl_property_t acl_property;
    ctc_acl_property_t acl_prop[ACL_TCAM_LOOKUP_NUM] = {{0}};
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    sai_object_id_t object_id = {0};
    ctc_object_id_t ctc_object_id = {0};
    ctc_object_id_t ctc_key_object_id = {0};
    ctc_global_panel_ports_t local_panel_ports;
    ctc_vlan_direction_property_t vlan_prop;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_slistnode_t *table_node = NULL;

    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
    sal_memset(&vlan_prop, 0, sizeof(ctc_vlan_direction_property_t));

    object_id = attr->value.oid;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, object_id, &ctc_object_id);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    CTC_SAI_CTC_ERROR_RETURN(_ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr->id, &bind_point_type, &bind_point_stage));

    /* In Centec SDK, there are eight acl look up in each port.
     * Enable how many look up on port depends on the bounded oid type (group or table) and group type (sequential and parallel).
     * As sequential group's members store prioritized in respect to member priority,
     * while parallel group's members are in different tcams reguardless of its priority.
     */

    /* Before attach sai table/group to bind point, table/group must be created. */
    if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        p_acl_table = (ctc_sai_acl_table_t*)ctc_sai_db_get_object_property(lchip, object_id);
        if (NULL == p_acl_table)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        if ((bind_point_stage != p_acl_table->table_stage) || (0 == (p_acl_table->bind_point_list&(1U<<bind_point_type))))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        is_bmp = CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS)) ? 1 : 0;

        /* In table directly bind situation, there is no group concept, all the entry(entries) in this table will be installed into tcam0 */
        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, bind_point_type, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &acl_prop[0].acl_priority);
        acl_prop[count].acl_en = 1;
        acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == bind_point_stage) ? CTC_INGRESS : CTC_EGRESS;
        acl_prop[count].tcam_lkup_type = is_enable ? p_acl_table->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_MAX;
        if (is_bmp)
        {
            CTC_SET_FLAG(acl_prop[0].flag, CTC_ACL_PROP_FLAG_USE_PORT_BITMAP);
        }
        count++;
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        p_acl_group = (ctc_sai_acl_group_t*)ctc_sai_db_get_object_property(lchip, object_id);
        if (p_acl_group->member_list->count != 0)
        {
            p_acl_table = (ctc_sai_acl_table_t*)(p_acl_group->member_list->head);
            is_bmp = CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS)) ? 1 : 0;
        }

        if ((bind_point_stage != p_acl_group->group_stage) || (0 == (p_acl_group->bind_point_list&(1U<<bind_point_type))))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, bind_point_type, p_acl_group->group_type, &block_base);
        if (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == p_acl_group->group_type)
        {
            /* for sequential  */
            acl_prop[count].acl_en = 1;
            acl_prop[count].acl_priority = block_base;
            acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == bind_point_stage) ? CTC_INGRESS : CTC_EGRESS;
            acl_prop[count].tcam_lkup_type = is_enable ? p_acl_group->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_MAX;
            if (is_bmp)
            {
                CTC_SET_FLAG(acl_prop[count].flag, CTC_ACL_PROP_FLAG_USE_PORT_BITMAP);
            }
            count++;
        }
        else if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
        {
            /* for parallel */
            CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
            {
                acl_prop[count].acl_en = 1;
                acl_prop[count].acl_priority = block_base + count;
                acl_prop[count].direction = (SAI_ACL_STAGE_INGRESS == bind_point_stage) ? CTC_INGRESS : CTC_EGRESS;
                acl_prop[count].tcam_lkup_type = is_enable ? p_acl_group->lookup_type : CTC_ACL_TCAM_LKUP_TYPE_MAX;
                if (is_bmp)
                {
                    CTC_SET_FLAG(acl_prop[count].flag, CTC_ACL_PROP_FLAG_USE_PORT_BITMAP);
                }
                count++;
            }
        }
    }

    switch (bind_point_type)
    {
        case SAI_ACL_BIND_POINT_TYPE_PORT:
            for (loop = 0; loop < count; loop++)
            {
                sal_memset(&acl_property, 0, sizeof(ctc_acl_property_t));
                acl_property.direction = acl_prop[loop].direction;
                acl_property.acl_priority = acl_prop[loop].acl_priority;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, ctc_key_object_id.value, &acl_property));

                acl_prop[loop].class_id = acl_property.class_id;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, ctc_key_object_id.value, &acl_prop[loop]));
            }
            break;
        case SAI_ACL_BIND_POINT_TYPE_LAG:
            ctcs_linkagg_get_max_mem_num(lchip, &max_num);
            MALLOC_ZERO(MEM_ACL_MODULE, p_gports, sizeof(uint32)* max_num);
            ctcs_linkagg_get_member_ports(lchip, (ctc_key_object_id.value & 0xFF), p_gports, &cnt);
            for (ii = 0; ii < cnt; ii++)
            {
                for (loop = 0; loop < count; loop++)
                {
                    sal_memset(&acl_property, 0, sizeof(ctc_acl_property_t));
                    acl_property.direction = acl_prop[loop].direction;
                    acl_property.acl_priority = acl_prop[loop].acl_priority;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, p_gports[ii], &acl_property));

                    acl_prop[loop].class_id = acl_property.class_id;
                    ctcs_port_set_acl_property(lchip, p_gports[ii], &acl_prop[loop]);
                }
            }
            ctc_sai_lag_register_member_change_cb(lchip, CTC_SAI_LAG_MEM_CHANGE_TYPE_ACL, ctc_key_object_id.value, is_enable?_ctc_sai_acl_lag_member_change_cb_fn:NULL);
            if (p_gports)
            {
                mem_free(p_gports);
            }
            break;
        case SAI_ACL_BIND_POINT_TYPE_VLAN:
            ctcs_get_gchip_id(lchip, &gchip);
            for (loop = 0; loop < count; loop++)
            {
                sal_memset(&acl_property, 0, sizeof(ctc_acl_property_t));
                acl_property.direction = acl_prop[loop].direction;
                acl_property.acl_priority = acl_prop[loop].acl_priority;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, ctc_key_object_id.value, &acl_property));

                acl_prop[loop].class_id = acl_property.class_id;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_acl_property(lchip, ctc_key_object_id.value, &acl_prop[loop]));
            }
            break;
        case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
            ctcs_get_gchip_id(lchip, &gchip);
            for (loop = 0; loop < count; loop++)
            {
                sal_memset(&acl_property, 0, sizeof(ctc_acl_property_t));
                acl_property.direction = acl_prop[loop].direction;
                acl_property.acl_priority = acl_prop[loop].acl_priority;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_acl_property(lchip, ctc_key_object_id.value, &acl_property));

                acl_prop[loop].class_id = acl_property.class_id;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_acl_property(lchip, ctc_key_object_id.value, &acl_prop[loop]));
            }
            break;
        case SAI_ACL_BIND_POINT_TYPE_SWITCH:
            ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)(&local_panel_ports));
            ctcs_get_gchip_id(lchip, &gchip);
            for (ii = 0; ii < local_panel_ports.count; ii++)
            {
                /* enable/disable acl look up on all plane ports */
                for (loop = 0; loop < count; loop++)
                {
                    sal_memset(&acl_property, 0, sizeof(ctc_acl_property_t));
                    acl_property.direction = acl_prop[loop].direction;
                    acl_property.acl_priority = acl_prop[loop].acl_priority;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[ii]), &acl_property));

                    acl_prop[loop].class_id = acl_property.class_id;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_acl_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[ii]), &acl_prop[loop]));
                }
            }
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

/******************************************************************************************************/
/* There are four situation to deal with:
----------------------------------
|   prev   |   next   |  comment |
----------------------------------
|   NULL   |   valid  |  enable  |
----------------------------------
|   NULL   |   NULL   |do-nothing|
----------------------------------
|   valid  |   NULL   |  disable |
----------------------------------
|   valid  |   valid  |  update  |
----------------------------------
*/

static sai_status_t
_ctc_sai_acl_bound_oid_check(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    sai_attr_id_t attr_id = 0;
    sai_object_id_t object_id = 0;
    ctc_object_id_t ctc_object_id = {0};
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;

    attr_id = attr->id;
    object_id = attr->value.oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, object_id, &ctc_object_id);

    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr_id, &bind_point_type, &bind_point_stage);

    if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        /* bind unit is acl table group */
        p_acl_group = (ctc_sai_acl_group_t*)ctc_sai_db_get_object_property(lchip, object_id);
        if (NULL == p_acl_group)
        {
            /* check group exist or not */
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Group to be bound is not exist\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        /* check group bind point list */
        if (0 == (p_acl_group->bind_point_list & (1 << bind_point_type)))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL group bind point list is 0x%X\n", p_acl_group->bind_point_list);
            return SAI_STATUS_NOT_SUPPORTED;
        }

        /* check stage */
        if (p_acl_group->group_stage != bind_point_stage)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL stage (%d) is not the same as bind point stage (%d)\n", p_acl_group->group_stage, bind_point_stage);
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        /* bind unit is acl table, object id is acl table id */
        /* check bounded acl table exist or not */
        p_acl_table = (ctc_sai_acl_table_t*)ctc_sai_db_get_object_property(lchip, object_id);
        if (NULL == p_acl_table)
        {
            /* check group exist or not */
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Table to be bound is not exist\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        /* check acl table bind point list */
        if (0 == (p_acl_table->bind_point_list & (1 << bind_point_type)))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Table bind point list is 0x%X\n", p_acl_table->bind_point_list);
            return SAI_STATUS_NOT_SUPPORTED;
        }

        /* check acl table stage with bind point acl stage */
        if (bind_point_stage != p_acl_table->table_stage)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL stage (%d) is not the same as bind point stage (%d)\n", p_acl_table->table_stage, bind_point_stage);
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }
    else if (SAI_NULL_OBJECT_ID == ctc_object_id.type)
    {
        /* do nothing */
    }
    else
    {
        /* make sure bind unit is acl group or acl table */
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Expected object %d or %d got %d\n", SAI_OBJECT_TYPE_ACL_TABLE_GROUP, SAI_OBJECT_TYPE_ACL_TABLE, ctc_object_id.type);
        return SAI_STATUS_INVALID_PARAMETER;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_add_bind(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_attr_id_t attr_id = 0;
    sai_object_id_t object_id = 0;
    sai_object_id_t *p_bounded_oid = NULL;
    ctc_object_id_t ctc_object_id = {0};
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_points_info = NULL;

    /* check the legality of bounded object id */
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_bound_oid_check(key, attr));

    attr_id = attr->id; /* SAI_PORT_ATTR_XXX SAI_VLAN_ATTR_XXX, SAI_PORT_ATTR_INGRESS_ACL */
    object_id = attr->value.oid;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, object_id, &ctc_object_id);
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr_id, &bind_point_type, &bind_point_stage);

    /* As in add operation, we must update sw table: 1. table or group's bind point 2. the relation between key and bounded oid */
    MALLOC_ZERO(MEM_ACL_MODULE, p_bind_points_info, sizeof(ctc_sai_acl_bind_point_info_t));
    if (NULL == p_bind_points_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate bind point info\n");
        return SAI_STATUS_NO_MEMORY;
    }
    MALLOC_ZERO(MEM_ACL_MODULE, p_bounded_oid, sizeof(sai_object_id_t));
    if (NULL == p_bounded_oid)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate bounded oid memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    /* enable acl look up on the correspond oid in sdk */
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_sdk_lookup_enable_set(key, attr, 1), status, error1);

    /* add acl entry in sdk */
    switch (bind_point_type)
    {
        case SAI_ACL_BIND_POINT_TYPE_PORT:
        case SAI_ACL_BIND_POINT_TYPE_LAG:
        case SAI_ACL_BIND_POINT_TYPE_VLAN:
        case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
        case SAI_ACL_BIND_POINT_TYPE_SWITCH:
            CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(key, attr), status, error2);
            break;
        default:
            break;
    }

    /* common sw operation regardless of bind point type */
    p_bind_points_info->bind_index = key->key.object_id;
    p_bind_points_info->bind_type = bind_point_type;

    if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_object_id.type)
    {
        p_acl_group = ctc_sai_db_get_object_property(lchip, object_id);

        ctc_slist_add_tail(p_acl_group->bind_points, &p_bind_points_info->head);
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_object_id.type)
    {
        p_acl_table = ctc_sai_db_get_object_property(lchip, object_id);

        ctc_slist_add_tail(p_acl_table->bind_points, &p_bind_points_info->head);
    }

    *p_bounded_oid = object_id;
    ctc_sai_db_entry_property_add(lchip, (SAI_ACL_STAGE_INGRESS==bind_point_stage)?CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS:CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id), (void*)p_bounded_oid);

    return status;

error2:
    _ctc_sai_acl_sdk_lookup_enable_set(key, attr, 0);
error1:
    mem_free(p_bounded_oid);
error0:
    mem_free(p_bind_points_info);
    return status;
}

static sai_status_t
_ctc_sai_acl_remove_bind(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_attribute_t attr_old;
    ctc_object_id_t ctc_old_object_id = {0};
    sai_acl_bind_point_type_t bind_point_type = 0;
    sai_acl_stage_t bind_point_stage = 0;
    sai_object_id_t *p_old_bounded_oid = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_points_info = NULL;
    ctc_slistnode_t *bind_node = NULL;

    sal_memset(&attr_old, 0, sizeof(sai_attribute_t));

    /* check the legality of bounded object id */
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr->id, &bind_point_type, &bind_point_stage);

    p_old_bounded_oid = ctc_sai_db_entry_property_get(lchip, (SAI_ACL_STAGE_INGRESS==bind_point_stage)?CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS:CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&(key->key.object_id)));
    attr_old.id = attr->id;
    attr_old.value.oid = *p_old_bounded_oid;

    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_sdk_lookup_enable_set(key, &attr_old, 0));

    switch (bind_point_type)
    {
        case SAI_ACL_BIND_POINT_TYPE_PORT:
        case SAI_ACL_BIND_POINT_TYPE_LAG:
        case SAI_ACL_BIND_POINT_TYPE_VLAN:
        case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
        case SAI_ACL_BIND_POINT_TYPE_SWITCH:
            CTC_SAI_ERROR_RETURN(_ctc_sai_acl_bind_point_acl_remove(key, &attr_old));
            break;
        default:
            break;
    }

    /* common sw operation regardless of bind point type */
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, *p_old_bounded_oid, &ctc_old_object_id);

    if (SAI_OBJECT_TYPE_ACL_TABLE_GROUP == ctc_old_object_id.type)
    {
        p_acl_group = ctc_sai_db_get_object_property(lchip, *p_old_bounded_oid);

        CTC_SLIST_LOOP(p_acl_group->bind_points, bind_node)
        {
            p_bind_points_info = (ctc_sai_acl_bind_point_info_t*)bind_node;
            if (p_bind_points_info->bind_index == key->key.object_id)
            {
                break;
            }
        }
        ctc_slist_delete_node(p_acl_group->bind_points, bind_node);
        mem_free(p_bind_points_info);
    }
    else if (SAI_OBJECT_TYPE_ACL_TABLE == ctc_old_object_id.type)
    {
        p_acl_table = ctc_sai_db_get_object_property(lchip, *p_old_bounded_oid);

        CTC_SLIST_LOOP(p_acl_table->bind_points, bind_node)
        {
            p_bind_points_info = (ctc_sai_acl_bind_point_info_t*)bind_node;
            if (p_bind_points_info->bind_index == key->key.object_id)
            {
                break;
            }
        }
        ctc_slist_delete_node(p_acl_table->bind_points, bind_node);
        mem_free(p_bind_points_info);
    }

    ctc_sai_db_entry_property_remove(lchip, (SAI_ACL_STAGE_INGRESS==bind_point_stage)?CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS:CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&(key->key.object_id)));
    mem_free(p_old_bounded_oid);

    return status;
}

static sai_status_t
_ctc_sai_acl_update_bind(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_attribute_t attr_old;
    sai_acl_bind_point_type_t bind_point_type;
    sai_acl_stage_t bind_point_stage;
    sai_object_id_t *p_old_bounded_oid = NULL;

    sal_memset(&attr_old, 0, sizeof(sai_attribute_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr->id, &bind_point_type, &bind_point_stage);
    p_old_bounded_oid = ctc_sai_db_entry_property_get(lchip, (SAI_ACL_STAGE_INGRESS==bind_point_stage)?CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS:CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id));

    attr_old.id = attr->id;
    attr_old.value.oid = *p_old_bounded_oid;

    /* remove old */
    _ctc_sai_acl_remove_bind(key, &attr_old);

    /* add new */
    _ctc_sai_acl_add_bind(key, attr);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_acl_bind_point_set(sai_object_key_t *key, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_id_t object_id = 0;
    sai_object_id_t *p_old_bounded_oid = NULL;
    sai_acl_stage_t bind_point_stage;
    sai_acl_bind_point_type_t bind_point_type;

    /* acl_table_id */
    object_id = attr->value.oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    _ctc_sai_acl_mapping_attr_id_to_bind_point_type_and_stage(attr->id, &bind_point_type, &bind_point_stage);
    p_old_bounded_oid = ctc_sai_db_entry_property_get(lchip, (SAI_ACL_STAGE_INGRESS==bind_point_stage)?CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS:CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id));

    if (NULL == p_old_bounded_oid && SAI_NULL_OBJECT_ID == object_id)
    {
        /* do nothing */
        return SAI_STATUS_SUCCESS;
    }
    else if (NULL == p_old_bounded_oid && SAI_NULL_OBJECT_ID != object_id)
    {
        /* enable */
        CTC_SAI_ERROR_RETURN(_ctc_sai_acl_add_bind(key, attr));
    }
    else if (NULL != p_old_bounded_oid && SAI_NULL_OBJECT_ID != object_id)
    {
        /* update */
        if (*p_old_bounded_oid == object_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        CTC_SAI_ERROR_RETURN(_ctc_sai_acl_update_bind(key, attr));
    }
    else if (NULL != p_old_bounded_oid && SAI_NULL_OBJECT_ID == object_id)
    {
        /* disable */
        CTC_SAI_ERROR_RETURN(_ctc_sai_acl_remove_bind(key, attr));
    }

    return SAI_STATUS_SUCCESS;
}

#define ________GROUP_GET________

static sai_status_t
_ctc_sai_acl_traverse_group_member_hash_func(void* bucket_data, void* user_data)
{
    ctc_sai_oid_property_t *p_oid_property = NULL;
    acl_table_group_oid_info_t * p_table_group_oid_info = NULL;
    ctc_sai_acl_table_group_member_t *p_acl_table_group_member = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_table_group_oid_info = (acl_table_group_oid_info_t*)user_data;
    p_acl_table_group_member = (ctc_sai_acl_table_group_member_t*)(p_oid_property->data);

    if (p_acl_table_group_member->group_id == p_table_group_oid_info->group_oid)
    {
        p_table_group_oid_info->group_member_oid_list[p_table_group_oid_info->count++] = p_oid_property->oid;
    }

    return SAI_STATUS_SUCCESS;
}
sai_status_t
ctc_sai_acl_get_acl_table_group_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 ii = 0;
    uint8 lchip = 0;
    uint8 count = 0;
    uint8 need_free_memory = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t group_object_id = 0;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    sai_object_id_t *group_member_list = NULL;
    acl_table_group_oid_info_t table_group_oid_info;

    sal_memset(&table_group_oid_info, 0 , sizeof(acl_table_group_oid_info_t));
    group_object_id = key->key.object_id;

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(group_object_id, &lchip);

    p_acl_group = ctc_sai_db_get_object_property(lchip, group_object_id);
    if (NULL == p_acl_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Group is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE:
            attr->value.s32 = p_acl_group->group_stage;
            break;
        case SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST:
            for (ii = SAI_ACL_BIND_POINT_TYPE_PORT; ii <= SAI_ACL_BIND_POINT_TYPE_SWITCH; ii++)
            {
                if (p_acl_group->bind_point_list & (1 << ii))
                {
                    attr->value.s32list.list[count++] = ii;
                }
            }
            attr->value.s32list.count = count;
            break;
        case SAI_ACL_TABLE_GROUP_ATTR_TYPE:
            attr->value.s32 = p_acl_group->group_type;
            break;
        case SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST:
            group_member_list = mem_malloc(MEM_ACL_MODULE, attr->value.objlist.count * sizeof(sai_object_id_t));
            if (NULL == group_member_list)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            need_free_memory = 1;

            table_group_oid_info.group_oid = group_object_id;
            table_group_oid_info.group_member_oid_list = group_member_list;
            table_group_oid_info.count = 0;
            /* traverse acl table group member hash, at every node judge if the table group member's group id equals to the needed group id */
            ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER, _ctc_sai_acl_traverse_group_member_hash_func, (void*)(&table_group_oid_info));
            count = table_group_oid_info.count;
            ctc_sai_fill_object_list(sizeof(sai_object_id_t), (void*)group_member_list, count, (void*)(&(attr->value.objlist)));
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    if (need_free_memory)
    {
        mem_free(group_member_list);
    }
    return status;
}

#define ________MEMBER_GET________
sai_status_t
ctc_sai_acl_get_acl_table_group_member_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t object_id = 0;
    ctc_sai_acl_table_group_member_t *p_acl_table_group_member = NULL;

    object_id = key->key.object_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));

    p_acl_table_group_member = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_table_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table group member is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID:
            attr->value.oid = p_acl_table_group_member->group_id;
            break;
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID:
            attr->value.oid = p_acl_table_group_member->table_id;
            break;
        case SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY:
            attr->value.u32 = p_acl_table_group_member->member_priority;
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return status;
}

#define ________TABLE_GET________
sai_status_t
ctc_sai_acl_get_acl_table_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 ii = 0;
    uint32 count = 0;
    sai_object_id_t object_id = 0;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_slistnode_t *entry_node = NULL;
    ctc_sai_acl_table_member_t *p_table_member = NULL;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    sai_object_id_t *entry_oid_list = NULL;

    object_id = key->key.object_id;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));

    p_acl_table = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_ACL_TABLE_ATTR_ACL_STAGE:
            attr->value.s32 = p_acl_table->table_stage;
            break;

        case SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST:
            for (ii = SAI_ACL_BIND_POINT_TYPE_PORT; ii <= SAI_ACL_BIND_POINT_TYPE_SWITCH; ii++)
            {
                if (p_acl_table->bind_point_list & (1 << ii))
                {
                    attr->value.s32list.list[count++] = ii;
                }
            }
            attr->value.s32list.count = count;
            break;

        case SAI_ACL_TABLE_ATTR_SIZE:
            attr->value.u32 = (ACL_DEFAULT_TABLE_SIZE == p_acl_table->table_size) ? 0 : p_acl_table->table_size;
            break;

        case SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST:
            break;

        case SAI_ACL_TABLE_ATTR_ENTRY_LIST:
            MALLOC_ZERO(MEM_ACL_MODULE, entry_oid_list, (attr->value.objlist.count) * sizeof(sai_object_id_t));
            if (NULL == entry_oid_list)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
            {
                p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
                entry_oid_list[count++] = p_table_member->entry_id;
            }
            ctc_sai_fill_object_list(sizeof(sai_object_id_t), (void*)entry_oid_list, count, (void*)(&(attr->value.objlist)));
            mem_free(entry_oid_list);
            break;

        case SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY:
            CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
            {
                p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
                p_acl_entry = ctc_sai_db_get_object_property(lchip, p_table_member->entry_id);
                if (NULL == p_acl_entry)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL entry is not exist\n");
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                /* only care about the admin state, not entries in Centec SDK */
                if (p_acl_entry->entry_valid)
                {
                    count++;
                }
            }
            attr->value.u32 = count;
            break;

        case SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER:
            break;

        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_acl_get_acl_table_field(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t object_id = 0;
    ctc_sai_acl_table_t *p_acl_table = NULL;

    object_id = key->key.object_id;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));
    p_acl_table = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    /* Set default value */
    attr->value.booldata = FALSE;
    if (CTC_BMP_ISSET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(attr->id)))
    {
        attr->value.booldata = TRUE;
    }

    return SAI_STATUS_SUCCESS;
}

#define ________ENTRY_SET________

sai_status_t
ctc_sai_acl_set_acl_entry_info(sai_object_key_t *key,  const sai_attribute_t *attr)
{
    uint8  lchip = 0;
    uint8  bind_point_type = 0;
    uint8  block_base = 0;
    uint16 entry_priority = 0;
    int32  status = SAI_STATUS_SUCCESS;
    uint32 gm = 0;
    uint32 entry_index = 0;
    uint32 table_index = 0;
    uint32 bind_point_value = 0;
    uint32 *p_ctc_entry_id = NULL;
    uint32 *p_ctc_group_id = NULL;
    uint32 new_priority = 0;
    uint64 hw_entry_id = 0;
    uint64 hw_table_id = 0;
    sai_object_key_t bind_point_key;
    ctc_object_id_t ctc_table_object_id;
    ctc_object_id_t ctc_key_object_id;
    ctc_object_id_t ctc_bind_point_object_id;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_slistnode_t *table_node = NULL;
    ctc_slistnode_t *group_node = NULL;
    ctc_slistnode_t *bind_node  = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_sai_acl_table_group_list_t *p_acl_table_group_list = NULL;
    ctc_sai_acl_bind_point_info_t  *p_bind_point = NULL;

    sal_memset(&bind_point_key, 0, sizeof(sai_object_key_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_acl_entry = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL entry is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, p_acl_entry->table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_acl_entry->table_id, &ctc_table_object_id);
    table_index = ctc_table_object_id.value;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, key->key.object_id, &ctc_key_object_id);
    entry_index = ctc_key_object_id.value;

    CTC_SLIST_LOOP(p_acl_table->group_list, group_node)
    {
        p_acl_table_group_list = (ctc_sai_acl_table_group_list_t*)group_node;
        p_acl_group = ctc_sai_db_get_object_property(lchip, p_acl_table_group_list->group_id);

        gm = 0;
        if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
        {
            CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
            {
                p_group_member = (ctc_sai_acl_group_member_t*)table_node;
                if (p_group_member->table_id != p_acl_entry->table_id)
                {
                    gm++;
                }
                else
                {
                    break;
                }
            }
        }

        /* one sai table correspond to a sdk group, the sdk group priority is associated with group type and group member priority, but not with bind times */
        CTC_SLIST_LOOP(p_acl_group->bind_points, bind_node)
        {
            p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_bind_point->bind_index, &ctc_bind_point_object_id);
            bind_point_value = ctc_bind_point_object_id.value;
            bind_point_type = p_bind_point->bind_type;
            bind_point_key.key.object_id = p_bind_point->bind_index;

            _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, bind_point_type, p_acl_group->group_type, &block_base);
            hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
            p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
            hw_entry_id = (uint64)1 << 63 | (uint64)bind_point_type << 60 | bind_point_value << 28 | entry_index;
            p_ctc_entry_id =  ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_entry_id));

            entry_priority = (SAI_ACL_ENTRY_ATTR_PRIORITY == attr->id) ? attr->value.u32 : p_acl_entry->priority;
            _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, entry_priority, bind_point_type, table_index, &new_priority);
            CTC_SAI_ERROR_GOTO(_ctc_sai_acl_add_acl_entry_to_sdk(lchip, &bind_point_key, *p_ctc_group_id, block_base + gm, key->key.object_id, *p_ctc_entry_id, new_priority, p_acl_entry, attr), status, error0);
        }
    }

    CTC_SLIST_LOOP(p_acl_table->bind_points, bind_node)
    {
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_bind_point->bind_index, &ctc_bind_point_object_id);
        bind_point_value = ctc_bind_point_object_id.value;
        bind_point_type = p_bind_point->bind_type;
        bind_point_key.key.object_id = p_bind_point->bind_index;

        hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
        p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
        hw_entry_id = (uint64)1 << 63 | (uint64)bind_point_type << 60 | bind_point_value << 28 | entry_index;
        p_ctc_entry_id =  ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_entry_id));

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, bind_point_type, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &block_base);

        entry_priority = (SAI_ACL_ENTRY_ATTR_PRIORITY == attr->id) ? attr->value.u32 : p_acl_entry->priority;
        /* additional operation only valid for SAI_ACL_ENTRY_ATTR_PRIORITY */
        _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, entry_priority, bind_point_type, table_index, &new_priority);
        CTC_SAI_ERROR_GOTO(_ctc_sai_acl_add_acl_entry_to_sdk(lchip, &bind_point_key, *p_ctc_group_id, block_base, key->key.object_id, *p_ctc_entry_id, new_priority, p_acl_entry, attr), status, error0);
    }

    /* the sai sw table need update */
    if (attr->id >= SAI_ACL_ENTRY_ATTR_FIELD_START && attr->id <= SAI_ACL_ENTRY_ATTR_FIELD_END)
    {
        sal_memcpy(&p_acl_entry->key_attr_list[attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START], attr, sizeof(sai_attribute_t));
    }
    else if (attr->id >= SAI_ACL_ENTRY_ATTR_ACTION_START && attr->id <= SAI_ACL_ENTRY_ATTR_ACTION_END)
    {
        sal_memcpy(&p_acl_entry->action_attr_list[attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], attr, sizeof(sai_attribute_t));
    }
    else if (SAI_ACL_ENTRY_ATTR_PRIORITY == attr->id)
    {
        p_acl_entry->priority = attr->value.u32;
    }
    else if (SAI_ACL_ENTRY_ATTR_ADMIN_STATE == attr->id)
    {
        p_acl_entry->entry_valid = attr->value.booldata;
    }

error0:
    return status;
}

#define ________ENTRY_GET________

sai_status_t
ctc_sai_acl_get_acl_entry_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t object_id = {0};
    ctc_sai_acl_entry_t *p_acl_entry = NULL;

    object_id = key->key.object_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));
    p_acl_entry = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL entry is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (attr->id >= SAI_ACL_ENTRY_ATTR_FIELD_START && attr->id <= SAI_ACL_ENTRY_ATTR_FIELD_END)
    {
        sal_memcpy(attr, &p_acl_entry->key_attr_list[attr->id - SAI_ACL_ENTRY_ATTR_FIELD_START], sizeof(sai_attribute_t));
    }
    else if (attr->id >= SAI_ACL_ENTRY_ATTR_ACTION_START && attr->id <= SAI_ACL_ENTRY_ATTR_ACTION_END)
    {
        sal_memcpy(attr, &p_acl_entry->action_attr_list[attr->id - SAI_ACL_ENTRY_ATTR_ACTION_START], sizeof(sai_attribute_t));
    }
    else if (SAI_ACL_ENTRY_ATTR_TABLE_ID == attr->id)
    {
        attr->value.oid = p_acl_entry->table_id;
    }
    else if (SAI_ACL_ENTRY_ATTR_PRIORITY == attr->id)
    {
        attr->value.u32 = p_acl_entry->priority;
    }
    else if (SAI_ACL_ENTRY_ATTR_ADMIN_STATE == attr->id)
    {
        attr->value.booldata = p_acl_entry->entry_valid;
    }

    return SAI_STATUS_SUCCESS;
}

#define ________RANGE_GET________
sai_status_t
ctc_sai_acl_get_acl_range_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t object_id = 0;
    ctc_sai_acl_range_t *p_acl_range = NULL;

    object_id = key->key.object_id;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));

    p_acl_range = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_range)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Range is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_ACL_RANGE_ATTR_TYPE:
            attr->value.s32 = p_acl_range->range_type;
            break;
        case SAI_ACL_RANGE_ATTR_LIMIT:
            attr->value.u32range.min = p_acl_range->range_min;
            attr->value.u32range.max = p_acl_range->range_max;
            break;
        case SAI_ACL_RANGE_ATTR_STAGE:
            attr->value.s32 = p_acl_range->stage;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}
#define ________COUNTER_SET________
sai_status_t
ctc_sai_acl_set_acl_counter_info(sai_object_key_t *key,  const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_id_t object_id;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;

    object_id = key->key.object_id;
    ctc_sai_oid_get_lchip(object_id, &lchip);
    p_acl_counter = ctc_sai_db_get_object_property(lchip, object_id);

    if (NULL == p_acl_counter)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_ACL_COUNTER_ATTR_PACKETS:
        case SAI_ACL_COUNTER_ATTR_BYTES:
            if (attr->value.u64 == 0)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_clear_stats(lchip, p_acl_counter->stats_id));
            }
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}
#define ________COUNTER_GET________
sai_status_t
ctc_sai_acl_get_acl_counter_info(sai_object_key_t *key,  sai_attribute_t *attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t object_id = 0;
    ctc_stats_basic_t stats_acl;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;

    sal_memset(&stats_acl, 0, sizeof(ctc_stats_basic_t));

    object_id = key->key.object_id;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id, &lchip));

    p_acl_counter = ctc_sai_db_get_object_property(lchip, object_id);
    if (NULL == p_acl_counter)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Counter is not exist\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_ACL_COUNTER_ATTR_TABLE_ID:
            attr->value.oid = p_acl_counter->table_id;
            break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT:
            attr->value.booldata = p_acl_counter->enable_pkt_cnt;
            break;
        case SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT:
            attr->value.booldata = p_acl_counter->enable_byte_cnt;
            break;
        case SAI_ACL_COUNTER_ATTR_PACKETS:
            CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_stats(lchip, p_acl_counter->stats_id, &stats_acl));
            attr->value.u64 = stats_acl.packet_count;
            break;
        case SAI_ACL_COUNTER_ATTR_BYTES:
            CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_stats(lchip, p_acl_counter->stats_id, &stats_acl));
            attr->value.u64 = stats_acl.byte_count;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

#define ________FUNCTION_REGISTER________
/* table group attribute */
static ctc_sai_attr_fn_entry_t acl_table_group_attr_fn_entries[] = {
    { SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE,
      ctc_sai_acl_get_acl_table_group_info,
      NULL },
    { SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST,
      ctc_sai_acl_get_acl_table_group_info,
      NULL },
    { SAI_ACL_TABLE_GROUP_ATTR_TYPE,
      ctc_sai_acl_get_acl_table_group_info,
      NULL },
    { SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST,
      ctc_sai_acl_get_acl_table_group_info,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/* table group member attribute */
static ctc_sai_attr_fn_entry_t acl_table_group_member_attr_fn_entries[] = {
    { SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID,
      ctc_sai_acl_get_acl_table_group_member_info,
      NULL },
    { SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID,
      ctc_sai_acl_get_acl_table_group_member_info,
      NULL },
    { SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY,
      ctc_sai_acl_get_acl_table_group_member_info,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/* table attribute */
static ctc_sai_attr_fn_entry_t acl_table_attr_fn_entries[] = {
    { SAI_ACL_TABLE_ATTR_ACL_STAGE,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_SIZE,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IPV6,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IPV6,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_DST_MAC,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_SRC_IP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_DST_IP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IP,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IP,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IN_PORT,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_SRC_PORT,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_DST_PORT,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_ETHER_TYPE,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_INNER_IP_PROTOCOL,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IP_IDENTIFICATION,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_DSCP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ECN,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TTL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TOS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TC,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TUNNEL_VNI,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_LABEL,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_DST_USER_META,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META,
      ctc_sai_acl_get_acl_table_field,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_FDB_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ROUTE_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_BTH_OPCODE,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_AETH_SYNDROME,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MAX,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_FIELD_TAM_INT_TYPE,
      NULL,
      NULL },
    { SAI_ACL_TABLE_ATTR_ENTRY_LIST,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY,
      ctc_sai_acl_get_acl_table_info,
      NULL },
    { SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER,
      NULL,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/* entry attribute */
static ctc_sai_attr_fn_entry_t acl_entry_attr_fn_entries[] = {
    { SAI_ACL_ENTRY_ATTR_TABLE_ID,
      ctc_sai_acl_get_acl_entry_info,
      NULL },
    { SAI_ACL_ENTRY_ATTR_PRIORITY,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ADMIN_STATE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_DST_IP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT,
      ctc_sai_acl_get_acl_entry_info,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_DSCP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ECN,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_TTL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_TOS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE,
      ctc_sai_acl_get_acl_entry_info,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL,
      ctc_sai_acl_get_acl_entry_info,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_TC,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_TUNNEL_VNI,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_LABEL,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MAX,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_FLOOD,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_COUNTER,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_TC,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST,
      NULL,
      NULL },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN,
      ctc_sai_acl_get_acl_entry_info,
      ctc_sai_acl_set_acl_entry_info },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static ctc_sai_attr_fn_entry_t acl_range_attr_fn_entries[] = {
    { SAI_ACL_RANGE_ATTR_TYPE,
      ctc_sai_acl_get_acl_range_info,
      NULL },
    { SAI_ACL_RANGE_ATTR_LIMIT,
      ctc_sai_acl_get_acl_range_info,
      NULL },
    { SAI_ACL_RANGE_ATTR_STAGE,
      ctc_sai_acl_get_acl_range_info,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};




static ctc_sai_attr_fn_entry_t acl_counter_attr_fn_entries[] = {
    { SAI_ACL_COUNTER_ATTR_TABLE_ID,
      ctc_sai_acl_get_acl_counter_info,
      NULL },
    { SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT,
      ctc_sai_acl_get_acl_counter_info,
      NULL },
    { SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT,
      ctc_sai_acl_get_acl_counter_info,
      NULL },
    { SAI_ACL_COUNTER_ATTR_PACKETS,
      ctc_sai_acl_get_acl_counter_info,
      ctc_sai_acl_set_acl_counter_info },
    { SAI_ACL_COUNTER_ATTR_BYTES,
      ctc_sai_acl_get_acl_counter_info,
      ctc_sai_acl_set_acl_counter_info },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static sai_status_t
_ctc_sai_acl_table_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_acl_table_t*    p_acl_table = (ctc_sai_acl_table_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_slistnode_t *entry_node = NULL;
    uint8 count = 0;
    uint32 i = 0;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%s%-20d%s:0x%016"PRIx64"\n", "No.", num_cnt, "acl_table_id", bucket_data->oid);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "table_stage:%-8dbind_point_list:0x%-8xtable_size:%-12dentry_count:%d\n",
                     p_acl_table->table_stage, p_acl_table->bind_point_list, p_acl_table->table_size, p_acl_table->created_entry_count);

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "table_key_bmp:");
    for (i = 0; i < ((SAI_ACL_KEY_ATTR_NUM-1)/32 + 1); i++)
    {
        CTC_SAI_LOG_DUMP(p_file, "0x%08x  ", p_acl_table->table_key_bmp[i]);
        if (count++ >= 9)
        {
            CTC_SAI_LOG_DUMP(p_file, "\n");
        }
    }
    if (p_acl_table->entry_list)
    {
        ctc_sai_acl_table_member_t* p_table_member = NULL;
        entry_node = NULL;
        count = 0;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "entry_list:");
        CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
        {
            p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
            CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_table_member->entry_id);
            if (count++ >= 5)
            {
                CTC_SAI_LOG_DUMP(p_file, "\n");
            }
        }
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }
    if (p_acl_table->group_list)
    {
        ctc_sai_acl_table_group_list_t* p_acl_table_group_member = NULL;
        entry_node = NULL;
        count = 0;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "group_list:");
        CTC_SLIST_LOOP(p_acl_table->group_list, entry_node)
        {
            p_acl_table_group_member = (ctc_sai_acl_table_group_list_t*)entry_node;
            CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_acl_table_group_member->group_id);
            if (count++ >= 5)
            {
                CTC_SAI_LOG_DUMP(p_file, "\n");
            }
        }
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }
    if (p_acl_table->bind_points)
    {
        ctc_sai_acl_bind_point_info_t* p_bind_point_info = NULL;
        entry_node = NULL;
        count = 0;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "bind_points:");
        CTC_SLIST_LOOP(p_acl_table->bind_points, entry_node)
        {
            p_bind_point_info = (ctc_sai_acl_bind_point_info_t*)entry_node;
            CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_bind_point_info->bind_index);
            if (count++ >= 5)
            {
                CTC_SAI_LOG_DUMP(p_file, "\n");
            }
        }
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_entry_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_acl_entry_t*    p_acl_entry = (ctc_sai_acl_entry_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint32 i = 0;
    uint32 j = 0;
    uint32 cnt = 0;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "No.%d  entry_id:0x%016"PRIx64"  table_id:0x%016"PRIx64"  priority:%d  entry_valid%d\n",
                             num_cnt, bucket_data->oid, p_acl_entry->table_id, p_acl_entry->priority, p_acl_entry->entry_valid);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    for (i = 0; i < SAI_ACL_KEY_ATTR_NUM; i++)
    {
        if (p_acl_entry->key_attr_list[i].value.aclfield.enable)
        {
            cnt++;
        }
    }
    CTC_SAI_LOG_DUMP(p_file, ">>>>Keys(total %d)\n", cnt);
    for (i = 0; i < SAI_ACL_KEY_ATTR_NUM; i++)
    {
        sai_acl_field_data_t* aclfield = NULL;
        sai_ip_address_t ip_addr_data;
        sai_ip_address_t ip_addr_mask;
        char data[64] = {0};
        char mask[64] = {0};
        if (!p_acl_entry->key_attr_list[i].value.aclfield.enable)
        {
            continue;
        }
        sal_memset(&ip_addr_data, 0, sizeof(sai_ip_address_t));
        sal_memset(&ip_addr_mask, 0, sizeof(sai_ip_address_t));
        aclfield = &(p_acl_entry->key_attr_list[i].value.aclfield);
        switch (p_acl_entry->key_attr_list[i].id)
        {
            case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS:
                for (j = 0; j < aclfield->data.objlist.count; j++)
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%016"PRIx64, "IN_PORTS", aclfield->data.objlist.list[j]);
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%016"PRIx64, "IN_PORT", aclfield->data.oid);
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC:
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC:
                ctc_sai_get_mac_str(aclfield->data.mac, data);
                ctc_sai_get_mac_str(aclfield->mask.mac, mask);
                if (SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC == p_acl_entry->key_attr_list[i].id)
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%18s%18s", "SRC_MAC", data, mask);
                }
                else
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%18s%18s", "DST_MAC", data, mask);
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%08x0x%08x", "OUTER_VLAN_ID", aclfield->data.u16, aclfield->mask.u16);
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%08x0x%08x", "ETHER_TYPE", aclfield->data.u16, aclfield->mask.u16);
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP:
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_IP:
                sal_memcpy(&ip_addr_data.addr.ip4, &aclfield->data.ip4, sizeof(sai_ip4_t));
                sal_memcpy(&ip_addr_mask.addr.ip4, &aclfield->mask.ip4, sizeof(sai_ip4_t));
                ctc_sai_get_ip_str(&ip_addr_data, data);
                ctc_sai_get_ip_str(&ip_addr_mask, mask);
                if (SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP == p_acl_entry->key_attr_list[i].id)
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%18s%18s", "SRC_IP", data, mask);
                }
                else
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%18s%18s", "DST_IP", data, mask);
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6:
            case SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6:
                ip_addr_data.addr_family = SAI_IP_ADDR_FAMILY_IPV6;
                ip_addr_mask.addr_family = SAI_IP_ADDR_FAMILY_IPV6;
                sal_memcpy(&ip_addr_data.addr.ip6, &aclfield->data.ip6, sizeof(sai_ip6_t));
                sal_memcpy(&ip_addr_mask.addr.ip6, &aclfield->mask.ip6, sizeof(sai_ip6_t));
                ctc_sai_get_ip_str(&ip_addr_data, data);
                ctc_sai_get_ip_str(&ip_addr_mask, mask);
                if (SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6 == p_acl_entry->key_attr_list[i].id)
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%42s%42s", "SRC_IPV6", data, mask);
                }
                else
                {
                    CTC_SAI_LOG_DUMP(p_file, "  %20s:%42s%42s", "DST_IPV6", data, mask);
                }
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%08x0x%08x", "L4_SRC_PORT", aclfield->data.u16, aclfield->mask.u16);
                break;
            case SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%08x0x%08x", "L4_DST_PORT", aclfield->data.u16, aclfield->mask.u16);
                break;
            default:
                break;
        }
    }

    cnt = 0;
    for (i = 0; i < SAI_ACL_ACTION_ATTR_NUM; i++)
    {
        if (p_acl_entry->action_attr_list[i].value.aclaction.enable)
        {
            cnt++;
        }
    }
    CTC_SAI_LOG_DUMP(p_file, ">>>>Actions(total %d)\n", cnt);
    for (i = 0; i < SAI_ACL_ACTION_ATTR_NUM; i++)
    {
        sai_acl_action_data_t* aclaction = NULL;
        if (!p_acl_entry->action_attr_list[i].value.aclaction.enable)
        {
            continue;
        }
        aclaction = &(p_acl_entry->action_attr_list[i].value.aclaction);
        switch (p_acl_entry->key_attr_list[i].id)
        {
            case SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%016"PRIx64, "REDIRECT", aclaction->parameter.oid);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "PACKET_ACTION", aclaction->parameter.s32);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_TC:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_TC", aclaction->parameter.u8);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_PACKET_COLOR", aclaction->parameter.s32);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_INNER_VLAN_ID", aclaction->parameter.u32);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_INNER_VLAN_PRI", aclaction->parameter.u8);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_OUTER_VLAN_ID", aclaction->parameter.u32);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_OUTER_VLAN_PRI", aclaction->parameter.u8);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_DSCP", aclaction->parameter.u8);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_ECN", aclaction->parameter.u8);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_ACL_META_DATA", aclaction->parameter.u32);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:0x%016"PRIx64, "SET_USER_TRAP_ID", aclaction->parameter.oid);
                break;
            case SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN:
                CTC_SAI_LOG_DUMP(p_file, "  %20s:%d", "SET_DO_NOT_LEARN", aclaction->parameter.u32);
                break;
            default:
                break;
        }
    }


    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_table_group_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_acl_group_t*    p_acl_group = (ctc_sai_acl_group_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_slistnode_t *entry_node = NULL;
    uint8 count = 0;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%s%-20d%s:0x%016"PRIx64"\n", "No.", num_cnt, "acl_table_group_id", bucket_data->oid);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "group_stage:%-8dgroup_type:%-12dbind_point_list:0x%-8x\n",
               p_acl_group->group_stage, p_acl_group->group_type, p_acl_group->bind_point_list);

    if (p_acl_group->member_list)
    {
        ctc_sai_acl_group_member_t* p_group_member = NULL;
        entry_node = NULL;
        count = 0;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "member_list:");
        CTC_SLIST_LOOP(p_acl_group->member_list, entry_node)
        {
            p_group_member = (ctc_sai_acl_group_member_t*)entry_node;
            CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_group_member->table_id);
            if (count++ >= 5)
            {
                CTC_SAI_LOG_DUMP(p_file, "\n");
            }
        }
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }
    if (p_acl_group->bind_points)
    {
        ctc_sai_acl_bind_point_info_t* p_bind_point_info = NULL;
        entry_node = NULL;
        count = 0;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "bind_points:");
        CTC_SLIST_LOOP(p_acl_group->bind_points, entry_node)
        {
            p_bind_point_info = (ctc_sai_acl_bind_point_info_t*)entry_node;
            CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_bind_point_info->bind_index);
            if (count++ >= 5)
            {
                CTC_SAI_LOG_DUMP(p_file, "\n");
            }
        }
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_acl_table_group_member_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_acl_table_group_member_t*    p_acl_table_group_member = (ctc_sai_acl_table_group_member_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char group_member_id[64] = {0};
    char acl_table_id[64] = {0};
    char acl_table_group_id[64] = {0};

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(group_member_id, "0x%016"PRIx64, bucket_data->oid);
    sal_sprintf(acl_table_id, "0x%016"PRIx64, p_acl_table_group_member->table_id);
    sal_sprintf(acl_table_group_id, "0x%016"PRIx64, p_acl_table_group_member->group_id);
    CTC_SAI_LOG_DUMP(p_file, "%-8d%-20s%-20s%-20s%-10d\n", num_cnt,
                        group_member_id, acl_table_id, acl_table_group_id, p_acl_table_group_member->member_priority);
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}


sai_status_t
_ctc_sai_acl_set_mirror_sample_rate_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    uint32 loop_i = 0;
    uint32 index = 0;
    sai_object_id_t mirror_oid_set = 0;
    sai_attribute_t acl_entry_attr;
    sai_object_key_t key;
    ctc_sai_acl_entry_t*    p_acl_entry = (ctc_sai_acl_entry_t*)(bucket_data->data);

    mirror_oid_set = *((sai_object_id_t*)p_cb_data->value0);
    sal_memset(&acl_entry_attr, 0, sizeof(sai_attribute_t));
    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    key.key.object_id = bucket_data->oid;
    index = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS - SAI_ACL_ENTRY_ATTR_ACTION_START;
    if (p_acl_entry->action_attr_list[index].value.aclaction.enable)
    {
        for (loop_i = 0; loop_i < p_acl_entry->action_attr_list[index].value.aclaction.parameter.objlist.count; loop_i++)
        {
            if (mirror_oid_set == p_acl_entry->action_attr_list[index].value.aclaction.parameter.objlist.list[loop_i])
            {
                sal_memcpy(&acl_entry_attr, &(p_acl_entry->action_attr_list[index]), sizeof(sai_attribute_t));
                ctc_sai_acl_set_acl_entry_info(&key, &acl_entry_attr);
                break;
            }
        }
    }
    index = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS - SAI_ACL_ENTRY_ATTR_ACTION_START;
    if (p_acl_entry->action_attr_list[index].value.aclaction.enable)
    {
        for (loop_i = 0; loop_i < p_acl_entry->action_attr_list[index].value.aclaction.parameter.objlist.count; loop_i++)
        {
            if (mirror_oid_set == p_acl_entry->action_attr_list[index].value.aclaction.parameter.objlist.list[loop_i])
            {
                sal_memcpy(&acl_entry_attr, &(p_acl_entry->action_attr_list[index]), sizeof(sai_attribute_t));
                ctc_sai_acl_set_acl_entry_info(&key, &acl_entry_attr);
                break;
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
void ctc_sai_acl_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# ACL MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ACL_TABLE))
    {
        CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "ACL Table");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_acl_table_t");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE,
                                            (hash_traversal_fn)_ctc_sai_acl_table_dump_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ACL_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "ACL Entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_acl_entry_t");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_ENTRY,
                                            (hash_traversal_fn)_ctc_sai_acl_entry_dump_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ACL_TABLE_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "ACL Table Group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_acl_group_t");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE_GROUP,
                                            (hash_traversal_fn)_ctc_sai_acl_table_group_dump_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER))
    {
        CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "ACL Table Group Member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_acl_table_group_member_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-20s%-20s%-20s%-10s\n", "No.", "group_member_id", "table_id", "group_id", "member_priority");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER,
                                            (hash_traversal_fn)_ctc_sai_acl_table_group_member_dump_print_cb, (void*)(&sai_cb_data));
    }
}

sai_status_t
ctc_sai_acl_set_mirror_sample_rate(uint8 lchip,sai_object_id_t mirror_oid)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;

    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.lchip = lchip;
    sai_cb_data.value0 = &mirror_oid;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_ENTRY,
                    (hash_traversal_fn)_ctc_sai_acl_set_mirror_sample_rate_cb, (void*)(&sai_cb_data));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_acl_init_resource(uint8 lchip)
{
    ctc_acl_league_t league;
    ctc_global_flow_property_t global_flow_property;

    sal_memset(&global_flow_property, 0, sizeof(ctc_global_flow_property_t));
    global_flow_property.igs_vlan_range_mode = CTC_GLOBAL_VLAN_RANGE_MODE_SHARE;
    global_flow_property.egs_vlan_range_mode = CTC_GLOBAL_VLAN_RANGE_MODE_SHARE;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_FLOW_PROPERTY, &global_flow_property));

    sal_memset(&league, 0, sizeof(ctc_acl_league_t));
    league.dir = CTC_INGRESS;
    league.auto_move_en = 0;
    league.acl_priority = 5;
    league.lkup_level_bitmap = 0x60;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_set_league_mode(lchip, &league));

    return SAI_STATUS_SUCCESS;
}

#define ________SAI_ACL_API________

#define ________SAI_ACL_TABLE_GROUP_MEMBER________

/**
 * @brief Create an ACL Table Group Member
 *
 * @param[out] acl_table_group_member_id The ACL table group member id
 * @param[in] switch_id Switch ID
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_table_group_member(sai_object_id_t *acl_table_group_member_id,
                                          sai_object_id_t switch_id,
                                          uint32 attr_count,
                                          const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 i = 0;
    uint8 group_bit = 0;
    uint8 table_bit = 0;
    uint32 member_priority = 0;
    uint32 index = 0;
    uint32 member_index = 0;
    uint32 member_num = 0;
    sai_attribute_t attr;
    sai_object_key_t key;
    sai_object_id_t group_id = 0;
    sai_object_id_t table_id = 0;
    ctc_slistnode_t* bind_point_node = NULL;
    const sai_attribute_value_t* attr_value = NULL;
    ctc_sai_acl_group_t* p_acl_group = NULL;
    ctc_sai_acl_table_t* p_acl_table = NULL;
    ctc_sai_acl_group_member_t* p_group_member = NULL;
    ctc_sai_acl_table_group_member_t* p_acl_table_group_member = NULL;
    ctc_sai_acl_table_group_list_t* p_group_list = NULL;
#if 0
    ctc_sai_acl_bind_point_info_t* p_bind_point_info = NULL;
#endif

    sal_memset(&attr, 0, sizeof(sai_attribute_t));
    sal_memset(&key,  0, sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_table_group_member_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl table group member parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Must provide ACL table group id\n");
        goto error0;
    }

    group_id = attr_value->oid;

    /* check group exist or not */
    p_acl_group = ctc_sai_db_get_object_property(lchip, group_id);
    if (NULL == p_acl_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table group is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if ((!CTC_SLIST_ISEMPTY(p_acl_group->bind_points)) || CTC_LIST_POINTER_COUNT(p_acl_group->bind_points))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The group already be bound\n");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID, &attr_value, &index);
    if(CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Must provide ACL table id\n");
        goto error0;
    }

    table_id = attr_value->oid;

    /* check table exist or not */
    p_acl_table = ctc_sai_db_get_object_property(lchip, table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == p_acl_group->group_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY, &attr_value, &index);
        if(CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The table group type of sequential must provide ACL member priority\n");
            goto error0;
        }
    }

    if (p_acl_table->table_stage != p_acl_group->group_stage)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Group stage (%d) is not equal to ACl Table stage (%d)\n", p_acl_group->group_stage, p_acl_table->table_stage);
        status = SAI_STATUS_FAILURE;
        goto error0;
    }
    member_priority = attr_value->u32;
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_check_member_priority(p_acl_group, member_priority), status, error0);

    if (p_acl_group->member_list)
    {
        CTC_SLIST_LOOP(p_acl_group->member_list, bind_point_node)
        {
            member_num++;
            p_group_member = (ctc_sai_acl_group_member_t*)bind_point_node;

            if (p_group_member->table_id == table_id)
            {
                status = SAI_STATUS_ITEM_ALREADY_EXISTS;
                goto error0;
            }
        }
    }

    if ((SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type) && (member_num >= 1)
        && ((p_acl_group->bind_point_list>>SAI_ACL_BIND_POINT_TYPE_SWITCH)&0x01))
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error0;
    }

    /* compare acl table group bind list with acl table bind list */
    for (i = SAI_ACL_BIND_POINT_TYPE_PORT; i < SAI_ACL_BIND_POINT_TYPE_SWITCH; i++)
    {
        group_bit = (p_acl_group->bind_point_list >> i) & 0x01;
        table_bit = (p_acl_table->bind_point_list >> i) & 0x01;

        if (group_bit == table_bit)
        {
            continue;
        }

        if (0 == table_bit && 0 != group_bit)
        {
            /* means table may not satsify group's key point field */
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL Group bind point list 0x%X is not a subset of ACl Table bind point list 0x%X\n", p_acl_group->bind_point_list, p_acl_table->bind_point_list);
            status = SAI_STATUS_FAILURE;
            goto error0;
        }
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX, &member_index), status, error0);
    *acl_table_group_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER, lchip, 0, 0, member_index);

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_table_group_member, sizeof(ctc_sai_acl_table_group_member_t));
    if (NULL == p_acl_table_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate member memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }
    p_acl_table_group_member->group_id = group_id;
    p_acl_table_group_member->table_id = table_id;
    p_acl_table_group_member->member_priority = member_priority;

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_table_group_member_id, p_acl_table_group_member), status, error2);

    /* add member to group's member list, keep this after all operation has been successfully excuted */
    MALLOC_ZERO(MEM_ACL_MODULE, p_group_member, sizeof(ctc_sai_acl_group_member_t));
    if (NULL == p_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate group member memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }

    p_group_member->members_prio = member_priority;
    p_group_member->table_id = table_id;

    ctc_slist_add_tail(p_acl_group->member_list, &(p_group_member->head));

    /* add group to table's list, keep this after all operation has been successfully excuted */
    MALLOC_ZERO(MEM_ACL_MODULE, p_group_list, sizeof(ctc_sai_acl_table_group_list_t));
    if (NULL == p_group_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate table's group node\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error4;
    }

    p_group_list->group_id = group_id;
    ctc_slist_add_tail(p_acl_table->group_list, &(p_group_list->head));

    /* update sai group tcam lookup type */
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_mapping_group_lookup_type(lchip, p_acl_group), status, error5);

#if 0
    /* after bind, not support add */
    /* need check the group -- which this table added into -- currently is bound to how many bind points, install all the entry in the table at the every above bind poins */
    CTC_SLIST_LOOP(p_acl_group->bind_points, bind_point_node)
    {
        p_bind_point_info = (ctc_sai_acl_bind_point_info_t*)bind_point_node;
        key.key.object_id = p_bind_point_info->bind_index;

        switch (p_bind_point_info->bind_type)
        {
            case SAI_ACL_BIND_POINT_TYPE_PORT:
                attr.id = p_acl_group->group_stage ? SAI_PORT_ATTR_EGRESS_ACL : SAI_PORT_ATTR_INGRESS_ACL;    /* the SAI_PORT_ATTR_EGRESS_ACL has to be considered */
                attr.value.oid = group_id;  /* oid has been processed as group oid */
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(&key, &attr), status, error5);
                break;
            case SAI_ACL_BIND_POINT_TYPE_LAG:
                attr.id = p_acl_group->group_stage ? SAI_LAG_ATTR_EGRESS_ACL : SAI_LAG_ATTR_INGRESS_ACL;
                attr.value.oid = group_id;  /* oid has been processed as group oid */
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(&key, &attr), status, error5);
            case SAI_ACL_BIND_POINT_TYPE_VLAN:
                attr.id = p_acl_group->group_stage ? SAI_VLAN_ATTR_EGRESS_ACL : SAI_VLAN_ATTR_INGRESS_ACL;
                attr.value.oid = group_id;  /* oid has been processed as group oid */
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(&key, &attr), status, error5);
                break;
            case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                attr.id = p_acl_group->group_stage ? SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL : SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL;
                attr.value.oid = group_id;  /* oid has been processed as group oid */
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(&key, &attr), status, error5);
                break;
            case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                attr.id = p_acl_group->group_stage ? SAI_SWITCH_ATTR_EGRESS_ACL : SAI_SWITCH_ATTR_INGRESS_ACL;
                attr.value.oid = group_id;  /* oid has been processed as group oid */
                CTC_SAI_ERROR_GOTO(_ctc_sai_acl_bind_point_acl_add(&key, &attr), status, error5);
                break;
            default:
                break;
        }
    }
#endif

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error5:
    ctc_slist_delete_node(p_acl_table->group_list, &(p_group_list->head));
    mem_free(p_group_list);
error4:
    ctc_slist_delete_node(p_acl_group->member_list, &(p_group_member->head));
    mem_free(p_group_member);
error3:
    ctc_sai_db_remove_object_property(lchip, *acl_table_group_member_id);
error2:
    mem_free(p_acl_table_group_member);
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX, member_index);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Delete an ACL Group Member
 *
 * @param[in] acl_table_group_member_id The ACL table group member id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_remove_acl_table_group_member(sai_object_id_t acl_table_group_member_id)
{
    uint8 lchip = 0;
    uint32 group_member_index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;
    sai_attribute_t attr;
    ctc_object_id_t ctc_group_member_object_id = {0};
    ctc_sai_acl_group_t* p_acl_group = NULL;
    ctc_sai_acl_table_t* p_acl_table = NULL;
    ctc_sai_acl_table_group_member_t* p_group_member = NULL;
#if 0
    ctc_slistnode_t* bind_node = NULL;
#endif
    ctc_slistnode_t* group_node = NULL;
    ctc_slistnode_t* table_node = NULL;
#if 0
    ctc_sai_acl_bind_point_info_t* p_bind_point = NULL;
#endif
    ctc_sai_acl_group_member_t* p_acl_group_member = NULL;
    ctc_sai_acl_table_group_list_t* p_acl_table_group_list = NULL;

    sal_memset(&key, 0, sizeof(sai_object_key_t));
    sal_memset(&attr, 0, sizeof(sai_attribute_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(acl_table_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_group_member_id, &ctc_group_member_object_id);
    group_member_index = ctc_group_member_object_id.value;

    p_group_member = ctc_sai_db_get_object_property(lchip, acl_table_group_member_id);
    if (NULL == p_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table group member to be removed is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_acl_group = ctc_sai_db_get_object_property(lchip, p_group_member->group_id);
    if (NULL == p_acl_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table group is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if ((!CTC_SLIST_ISEMPTY(p_acl_group->bind_points)) || CTC_LIST_POINTER_COUNT(p_acl_group->bind_points))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The group already be bound\n");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto out;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, p_group_member->table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

#if 0
    /* after bind, not support remove */
    CTC_SLIST_LOOP(p_acl_group->bind_points, bind_node)
    {
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
        key.key.object_id = p_bind_point->bind_index;
        switch (p_bind_point->bind_type)
        {
            case SAI_ACL_BIND_POINT_TYPE_PORT:
                attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS)? SAI_PORT_ATTR_INGRESS_ACL : SAI_PORT_ATTR_EGRESS_ACL;
                attr.value.oid = p_group_member->table_id;
                _ctc_sai_acl_bind_point_acl_remove(&key, &attr);
                break;
            case SAI_ACL_BIND_POINT_TYPE_LAG:
                attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS)? SAI_LAG_ATTR_INGRESS_ACL : SAI_LAG_ATTR_EGRESS_ACL;
                attr.value.oid = p_group_member->table_id;
                _ctc_sai_acl_bind_point_acl_remove(&key, &attr);
                break;
            case SAI_ACL_BIND_POINT_TYPE_VLAN:
                attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS)? SAI_VLAN_ATTR_INGRESS_ACL : SAI_VLAN_ATTR_EGRESS_ACL;
                attr.value.oid = p_group_member->table_id;
                _ctc_sai_acl_bind_point_acl_remove(&key, &attr);
                break;
            case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS)? SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL : SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL;
                attr.value.oid = p_group_member->table_id;
                _ctc_sai_acl_bind_point_acl_remove(&key, &attr);
                break;
            case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS)? SAI_SWITCH_ATTR_INGRESS_ACL : SAI_SWITCH_ATTR_EGRESS_ACL;
                attr.value.oid = p_group_member->table_id;
                _ctc_sai_acl_bind_point_acl_remove(&key, &attr);
                break;
            default:
                break;
        }
    }
#endif

    /* Process software table in SAI layer */
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX, group_member_index);

    CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
    {
        p_acl_group_member = (ctc_sai_acl_group_member_t*)table_node;
        if (p_acl_group_member->table_id == p_group_member->table_id)
        {
            break;
        }
    }
    ctc_slist_delete_node(p_acl_group->member_list, table_node);
    mem_free(p_acl_group_member);

    CTC_SLIST_LOOP(p_acl_table->group_list, group_node)
    {
        p_acl_table_group_list = (ctc_sai_acl_table_group_list_t*)group_node;
        if (p_acl_table_group_list->group_id == p_group_member->group_id)
        {
            break;
        }
    }
    ctc_slist_delete_node(p_acl_table->group_list, group_node);
    mem_free(p_acl_table_group_list);

    ctc_sai_db_remove_object_property(lchip, acl_table_group_member_id);
    mem_free(p_group_member);

    /* update sai group tcam lookup type */
    CTC_SAI_ERROR_RETURN(_ctc_sai_acl_mapping_group_lookup_type(lchip, p_acl_group));

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Set ACL table group member attribute
 *
 * @param[in] acl_table_group_member_id The ACL table group member id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_set_acl_table_group_member_attribute(sai_object_id_t acl_table_group_member_id,
                                                  const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));
    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_group_member_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_group_member_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER, acl_table_group_member_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl table group member attr: %u\n", attr->id);
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL table group member attribute
 *
 * @param[in] acl_table_group_member_id ACL table group member id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_get_acl_table_group_member_attribute(sai_object_id_t acl_table_group_member_id,
                                                  uint32 attr_count,
                                                  sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t     status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_group_member_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_group_member_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER, loop, acl_table_group_member_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl table group attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_ACL_ENTRY________

/**
 * @brief Create an ACL entry
 *
 * @param[out] acl_entry_id The ACL entry id
 * @param[in] switch_id The Switch Object id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_entry(sai_object_id_t *acl_entry_id,
                             sai_object_id_t switch_id,
                             uint32 attr_count,
                             const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    bool entry_valid = TRUE;

    uint8  lchip = 0;
    uint8  block_base = 0;
    uint32 ii = 0;
    uint32 gm = 0;
    uint32 priority = 0;
    uint32 index = 0;
    uint32 entry_index = 0;
    uint32 combined_priority = 0;
    uint32 table_index = 0;
    uint32 bind_point_value = 0;
    uint32 key_type = 0;
    uint32 *p_ctc_group_id = NULL;
    uint64 hw_table_id = 0;
    sai_object_id_t table_id = 0;
    sai_object_id_t group_id = 0;
    sai_object_id_t range_id = 0;
    sai_object_key_t key;
    sai_attribute_t attr;
    ctc_object_id_t ctc_table_object_id = {0};
    ctc_object_id_t ctc_bind_point_object_id = {0};
    sai_acl_bind_point_type_t bind_point_type = 0;
    ctc_sai_acl_range_t* p_acl_range = NULL;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_slistnode_t *table_node = NULL;
    ctc_slistnode_t *group_node = NULL;
    ctc_slistnode_t *bind_point_node = NULL;
    const sai_attribute_value_t *attr_value = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    ctc_sai_acl_table_member_t *p_table_member = NULL;
    ctc_sai_acl_table_group_list_t *p_table_group_list = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_entry_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl entry parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&attr, 0, sizeof(sai_attribute_t));
    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_TABLE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        table_id = attr_value->oid;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Must provide table id\n");
        goto error0;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table id is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_check_acl_entry_key_field(p_acl_table->table_key_bmp, attr_count, attr_list), status, error0);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, table_id, &ctc_table_object_id);
    table_index = ctc_table_object_id.value;

    /* check the acl table is full or not */
    if (p_acl_table->table_size == p_acl_table->created_entry_count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table is full\n");
        status = SAI_STATUS_TABLE_FULL;
        goto error0;
    }

    priority = ACL_DEFAULT_ENTRY_PRIORITY;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_PRIORITY, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        priority = attr_value->u32;
        if (priority < ACL_MIN_ENTRY_PRIORITY || priority > ACL_MAX_ENTRY_PRIORITY)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL entry priority is 0x%X, out of range [0x%X, 0x%X]\n", priority, ACL_MIN_ENTRY_PRIORITY, ACL_MAX_ENTRY_PRIORITY);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
    }

    entry_valid = TRUE;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_ADMIN_STATE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        entry_valid = attr_value->booldata;
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_mapping_entry_tcam_type(attr_count, attr_list, p_acl_table->lookup_type, &key_type), status, error0);

    /* add check for acl range type */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        for (ii = 0; ii < attr_value->aclfield.data.objlist.count; ii++)
        {
            range_id = attr_value->aclfield.data.objlist.list[ii];
            p_acl_range = ctc_sai_db_get_object_property(lchip, range_id);
            if (NULL == p_acl_range)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ACL, "The needed ACL range object id is Not exist\n");
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error0;
            }
        }
    }

    /* add check for acl counter */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_ACTION_COUNTER, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
    {
        p_acl_counter = ctc_sai_db_get_object_property(lchip, attr_value->aclaction.parameter.oid);
        if (NULL == p_acl_counter)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "The needed ACL Counter object id is Not exist\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error0;
        }
    }

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_entry, sizeof(ctc_sai_acl_entry_t));
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate acl entry memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    p_acl_entry->table_id = table_id;
    p_acl_entry->priority = priority;
    p_acl_entry->entry_valid = entry_valid;
    p_acl_entry->key_type = key_type;
    p_acl_entry->ctc_mirror_id = 0xFF;

    /* allocate memory for storing acl entry's key and action attribute list */
    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_entry->key_attr_list, SAI_ACL_KEY_ATTR_NUM * sizeof(sai_attribute_t));
    if (NULL == p_acl_entry->key_attr_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate memory for storing acl entry's key attribute list\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_entry->action_attr_list, SAI_ACL_ACTION_ATTR_NUM * sizeof(sai_attribute_t));
    if (NULL == p_acl_entry->action_attr_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate memory for storing acl entry's action attribute list\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error2;
    }

    /* store upper-level key and action attribute list in the sai software table */
    _ctc_sai_acl_store_entry_key_and_action_attributes(lchip, attr_count, attr_list, p_acl_entry);

    /* create acl entry object id */
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, &entry_index), status, error3);
    *acl_entry_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_ENTRY, lchip, 0, 0, entry_index);

    CTC_SAI_LOG_ERROR(SAI_API_ACL, "acl_entry_id = 0x%"PRIx64"\n", *acl_entry_id);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_entry_id, (void*)p_acl_entry), status, error4);

    /* add to acl table entry list after the acl entry has been successfully created */
    MALLOC_ZERO(MEM_ACL_MODULE, p_table_member, sizeof(ctc_sai_acl_table_member_t));
    if(NULL == p_table_member)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error5;
    }
    p_table_member->entry_id = *acl_entry_id;
    p_table_member->priority = priority;

    ctc_slist_add_tail(p_acl_table->entry_list, &(p_table_member->head));

    /* need check the current entry corresponded table bound situations, there two situations: 1.table directly bound to points; 2.table as a member of groups */
    CTC_SLIST_LOOP(p_acl_table->group_list, group_node)
    {
        p_table_group_list = (ctc_sai_acl_table_group_list_t*)group_node;
        group_id = p_table_group_list->group_id;
        p_acl_group = ctc_sai_db_get_object_property(lchip, group_id);

        gm = 0;
        CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
        {
            p_group_member = (ctc_sai_acl_group_member_t*)table_node;
            if (p_group_member->table_id != p_acl_entry->table_id)
            {
                if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
                {
                    gm++;
                }
            }
            else
            {
                break;
            }
        }

        CTC_SLIST_LOOP(p_acl_group->bind_points, bind_point_node)
        {
            p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_point_node;
            key.key.object_id = p_bind_point->bind_index;
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_bind_point->bind_index, &ctc_bind_point_object_id);
            bind_point_value = ctc_bind_point_object_id.value;

            _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, bind_point_type, p_acl_group->group_type, &block_base);
            switch (p_bind_point->bind_type)
            {
                case SAI_ACL_BIND_POINT_TYPE_PORT:
                    bind_point_type = SAI_ACL_BIND_POINT_TYPE_PORT;
                    attr.id = p_acl_group->group_stage ? SAI_PORT_ATTR_EGRESS_ACL : SAI_PORT_ATTR_INGRESS_ACL;
                    attr.value.oid = group_id;     /* group as bind unit */
                    /*add a entry to a table, the table corresponded sdk group has already been added, so do not need create sdk group again */
                    hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                    p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                    _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                    _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base + gm, *acl_entry_id, combined_priority);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_LAG:
                    bind_point_type = SAI_ACL_BIND_POINT_TYPE_LAG;
                    attr.id = p_acl_group->group_stage ? SAI_LAG_ATTR_EGRESS_ACL : SAI_LAG_ATTR_INGRESS_ACL;
                    attr.value.oid = group_id;     /* group as bind unit */
                    /*add a entry to a table, the table corresponded sdk group has already been added, so do not need create sdk group again */
                    hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                    p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                    _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                    _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base + gm, *acl_entry_id, combined_priority);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_VLAN:
                    bind_point_type = SAI_ACL_BIND_POINT_TYPE_VLAN;
                    attr.id = p_acl_group->group_stage ? SAI_VLAN_ATTR_EGRESS_ACL : SAI_VLAN_ATTR_INGRESS_ACL;
                    attr.value.oid = group_id;     /* group as bind unit */
                    /*add a entry to a table, the table corresponded sdk group has already been added, so do not need create sdk group again */
                    hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                    p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                    _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                    _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base + gm, *acl_entry_id, combined_priority);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                    bind_point_type = SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE;
                    attr.id = p_acl_group->group_stage ? SAI_VLAN_ATTR_EGRESS_ACL : SAI_VLAN_ATTR_INGRESS_ACL;
                    attr.value.oid = group_id;     /* group as bind unit */
                    /*add a entry to a table, the table corresponded sdk group has already been added, so do not need create sdk group again */
                    hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                    p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                    _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                    _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base + gm, *acl_entry_id, combined_priority);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                    bind_point_type = SAI_ACL_BIND_POINT_TYPE_SWITCH;
                    attr.id = p_acl_group->group_stage ? SAI_SWITCH_ATTR_EGRESS_ACL : SAI_SWITCH_ATTR_INGRESS_ACL;
                    attr.value.oid = group_id;     /* group as bind unit */
                    /*add a entry to a table, the table corresponded sdk group has already been added, so do not need create sdk group again */
                    hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                    p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                    _ctc_sai_acl_get_entry_combined_priority(p_acl_group->group_type, p_group_member->members_prio, p_table_member->priority, bind_point_type, table_index, &combined_priority);
                    _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base + gm, *acl_entry_id, combined_priority);
                    break;
                default:
                    break;
            }
        }
    }

    /* table directly bound */
    CTC_SLIST_LOOP(p_acl_table->bind_points, bind_point_node)
    {
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_point_node;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, p_bind_point->bind_index, &ctc_bind_point_object_id);
        bind_point_value = ctc_bind_point_object_id.value;
        key.key.object_id = p_bind_point->bind_index;

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, p_bind_point->bind_type, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &block_base);
        switch (p_bind_point->bind_type)
        {
            case SAI_ACL_BIND_POINT_TYPE_PORT:
                bind_point_type = SAI_ACL_BIND_POINT_TYPE_PORT;
                attr.id = p_acl_table->table_stage ? SAI_PORT_ATTR_EGRESS_ACL : SAI_PORT_ATTR_INGRESS_ACL;
                attr.value.oid = table_id;
                hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, priority, bind_point_type, table_index, &combined_priority);
                _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base, *acl_entry_id, combined_priority);
                break;
            case SAI_ACL_BIND_POINT_TYPE_LAG:
                bind_point_type = SAI_ACL_BIND_POINT_TYPE_LAG;
                attr.id = p_acl_table->table_stage ? SAI_LAG_ATTR_EGRESS_ACL : SAI_LAG_ATTR_INGRESS_ACL;
                attr.value.oid = table_id;
                hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, priority, bind_point_type, table_index, &combined_priority);
                _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base, *acl_entry_id, combined_priority);
                break;
            case SAI_ACL_BIND_POINT_TYPE_VLAN:
                bind_point_type = SAI_ACL_BIND_POINT_TYPE_VLAN;
                attr.id = p_acl_table->table_stage ? SAI_VLAN_ATTR_EGRESS_ACL : SAI_VLAN_ATTR_INGRESS_ACL;
                attr.value.oid = table_id;
                hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, priority, bind_point_type, table_index, &combined_priority);
                _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base, *acl_entry_id, combined_priority);
                break;
            case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                bind_point_type = SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE;
                attr.id = p_acl_table->table_stage ? SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL : SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL;
                attr.value.oid = table_id;
                hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, priority, bind_point_type, table_index, &combined_priority);
                _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base, *acl_entry_id, combined_priority);
                break;
            case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                bind_point_type = SAI_ACL_BIND_POINT_TYPE_SWITCH;
                attr.id = p_acl_table->table_stage ? SAI_SWITCH_ATTR_EGRESS_ACL : SAI_SWITCH_ATTR_INGRESS_ACL;
                attr.value.oid = table_id;
                hw_table_id = (uint64)bind_point_type << 60 | bind_point_value << 28 | table_index;
                p_ctc_group_id = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&hw_table_id));
                _ctc_sai_acl_get_entry_combined_priority(SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, 0, priority, bind_point_type, table_index, &combined_priority);
                _ctc_sai_acl_bind_point_acl_entry_add(&key, &attr, *p_ctc_group_id, block_base, *acl_entry_id, combined_priority);
                break;
            default:
                break;
        }
    }

    p_acl_table->created_entry_count++;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        for (ii = 0; ii < attr_value->aclfield.data.objlist.count; ii++)
        {
            range_id = attr_value->aclfield.data.objlist.list[ii];
            p_acl_range = ctc_sai_db_get_object_property(lchip, range_id);
            p_acl_range->ref_cnt++;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_ENTRY_ATTR_ACTION_COUNTER, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
    {
        p_acl_counter = ctc_sai_db_get_object_property(lchip, attr_value->aclaction.parameter.oid);
        p_acl_counter->ref_cnt++;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;
error5:
    ctc_sai_db_remove_object_property(lchip, *acl_entry_id);
error4:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, entry_index);
error3:
    mem_free(p_acl_entry->action_attr_list);
error2:
    mem_free(p_acl_entry->key_attr_list);
error1:
    mem_free(p_acl_entry);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


/**
 * @brief Delete an ACL entry
 *
 * @param[in] acl_entry_id The ACL entry id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_remove_acl_entry(sai_object_id_t acl_entry_id)
{
    uint8  lchip = 0;
    uint8  block_base = 0;
    uint32 ii = 0;
    uint32 gm = 0;
    uint32 index = 0;
    uint32 entry_index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_entry_object_id = {0};
    sai_object_id_t range_id = 0;
    sai_object_key_t key;
    sai_attribute_t attr;
    const sai_attribute_value_t *attr_value = NULL;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;
    ctc_sai_acl_range_t *p_acl_range = NULL;
    ctc_sai_acl_entry_t *p_acl_entry = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;
    ctc_slistnode_t *group_node = NULL;
    ctc_slistnode_t *entry_node = NULL;
    ctc_slistnode_t *bind_node = NULL;
    ctc_sai_acl_table_group_list_t *p_acl_table_group = NULL;
    ctc_sai_acl_bind_point_info_t *p_bind_point = NULL;
    ctc_sai_acl_table_member_t* p_table_member = NULL;
    ctc_sai_acl_group_member_t *p_group_member = NULL;
    ctc_slistnode_t *table_node = NULL;

    sal_memset(&key, 0, sizeof(sai_object_key_t));
    sal_memset(&attr, 0, sizeof(sai_attribute_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(acl_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_entry_id, &ctc_entry_object_id);
    entry_index = ctc_entry_object_id.value;

    p_acl_entry = ctc_sai_db_get_object_property(lchip, acl_entry_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL entry to be removed is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, p_acl_entry->table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SLIST_LOOP(p_acl_table->group_list, group_node)
    {
        p_acl_table_group = (ctc_sai_acl_table_group_list_t*)group_node;
        p_acl_group = ctc_sai_db_get_object_property(lchip, p_acl_table_group->group_id);

        gm = 0;
        if (SAI_ACL_TABLE_GROUP_TYPE_PARALLEL == p_acl_group->group_type)
        {
            CTC_SLIST_LOOP(p_acl_group->member_list, table_node)
            {
                p_group_member = (ctc_sai_acl_group_member_t*)table_node;

                if (p_group_member->table_id != p_acl_entry->table_id)
                {
                    gm++;
                }
                else
                {
                    break;
                }
            }
        }

        CTC_SLIST_LOOP(p_acl_group->bind_points, bind_node)
        {
            p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
            /* remove the corresponded sdk entry at every bind point */
            key.key.object_id = p_bind_point->bind_index;
            switch (p_bind_point->bind_type)
            {
                case SAI_ACL_BIND_POINT_TYPE_PORT:
                    attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? SAI_PORT_ATTR_INGRESS_ACL : SAI_PORT_ATTR_EGRESS_ACL;
                    attr.value.oid = p_acl_table_group->group_id;
                    _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_LAG:
                    attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? SAI_LAG_ATTR_INGRESS_ACL : SAI_LAG_ATTR_EGRESS_ACL;
                    attr.value.oid = p_acl_table_group->group_id;
                    _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_VLAN:
                    attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? SAI_VLAN_ATTR_INGRESS_ACL : SAI_VLAN_ATTR_EGRESS_ACL;
                    attr.value.oid = p_acl_table_group->group_id;
                    _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                    attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? SAI_VLAN_ATTR_INGRESS_ACL : SAI_VLAN_ATTR_EGRESS_ACL;
                    attr.value.oid = p_acl_table_group->group_id;
                    _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                    break;
                case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                    attr.id = (p_acl_group->group_stage == SAI_ACL_STAGE_INGRESS) ? SAI_SWITCH_ATTR_INGRESS_ACL : SAI_SWITCH_ATTR_EGRESS_ACL;
                    attr.value.oid = p_acl_table_group->group_id;
                    _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                    break;
                default:
                    break;
            }

            _ctc_sai_acl_mapping_tcam_block_base(p_acl_group->group_stage, p_bind_point->bind_type, p_acl_group->group_type, &block_base);
            status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE, &attr_value, &index);
            if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
            {
                sal_memcpy(&attr, attr_value, sizeof(attr));
                attr.value.aclaction.enable = FALSE;
                ctc_sai_samplepacket_set_acl_samplepacket(lchip, CTC_INGRESS, block_base + gm, acl_entry_id, &attr, NULL, NULL);
            }

            status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS, &attr_value, &index);
            if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
            {
                attr.id = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS;
                attr.value.aclaction.parameter.objlist.count = 0;
                ctc_sai_mirror_set_acl_mirr(lchip, block_base + gm, &(p_acl_entry->ctc_mirror_id), NULL, &attr);

            }

            status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS, &attr_value, &index);
            if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
            {
                attr.id = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS;
                attr.value.aclaction.parameter.objlist.count = 0;
                ctc_sai_mirror_set_acl_mirr(lchip, block_base + gm, &(p_acl_entry->ctc_mirror_id), NULL, &attr);
            }
        }
    }

    CTC_SLIST_LOOP(p_acl_table->bind_points, bind_node)
    {
        p_bind_point = (ctc_sai_acl_bind_point_info_t*)bind_node;
        /* remove the corresponded sdk entry at every bind point */
        key.key.object_id = p_bind_point->bind_index;

        switch (p_bind_point->bind_type)
        {
            case SAI_ACL_BIND_POINT_TYPE_PORT:
                attr.id = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS)? SAI_PORT_ATTR_INGRESS_ACL : SAI_PORT_ATTR_EGRESS_ACL;
                attr.value.oid = p_acl_entry->table_id;
                _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                break;
            case SAI_ACL_BIND_POINT_TYPE_LAG:
                attr.id = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS)? SAI_LAG_ATTR_INGRESS_ACL : SAI_LAG_ATTR_EGRESS_ACL;
                attr.value.oid = p_acl_entry->table_id;
                _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                break;
            case SAI_ACL_BIND_POINT_TYPE_VLAN:
                attr.id = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS)? SAI_VLAN_ATTR_INGRESS_ACL : SAI_VLAN_ATTR_EGRESS_ACL;
                attr.value.oid = p_acl_entry->table_id;
                _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                break;
            case SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE:
                attr.id = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS)? SAI_VLAN_ATTR_INGRESS_ACL : SAI_VLAN_ATTR_EGRESS_ACL;
                attr.value.oid = p_acl_entry->table_id;
                _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                break;
            case SAI_ACL_BIND_POINT_TYPE_SWITCH:
                attr.id = (p_acl_table->table_stage == SAI_ACL_STAGE_INGRESS)? SAI_SWITCH_ATTR_INGRESS_ACL : SAI_SWITCH_ATTR_EGRESS_ACL;
                attr.value.oid = p_acl_entry->table_id;
                _ctc_sai_acl_bind_point_acl_entry_remove(&key, &attr, acl_entry_id);
                break;
            default:
                break;
        }

        _ctc_sai_acl_mapping_tcam_block_base(p_acl_table->table_stage, p_bind_point->bind_type, SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL, &block_base);
        status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE, &attr_value, &index);
        if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
        {
            sal_memcpy(&attr, attr_value, sizeof(attr));
            attr.value.aclaction.enable = FALSE;
            ctc_sai_samplepacket_set_acl_samplepacket(lchip, CTC_INGRESS, block_base, acl_entry_id, &attr, NULL, NULL);
        }

        status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS, &attr_value, &index);
        if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
        {
            attr.id = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS;
            attr.value.aclaction.parameter.objlist.count = 0;
            ctc_sai_mirror_set_acl_mirr(lchip, block_base, &(p_acl_entry->ctc_mirror_id), NULL, &attr);
        }

        status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS, &attr_value, &index);
        if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
        {
            attr.id = SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS;
            attr.value.aclaction.parameter.objlist.count = 0;
            ctc_sai_mirror_set_acl_mirr(lchip, block_base, &(p_acl_entry->ctc_mirror_id), NULL, &attr);
        }
    }

    /* Process software table in SAI layer */
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX, entry_index);
    CTC_SLIST_LOOP(p_acl_table->entry_list, entry_node)
    {
        p_table_member = (ctc_sai_acl_table_member_t*)entry_node;
        if (p_table_member->entry_id == acl_entry_id)
        {
            break;
        }
    }
    ctc_slist_delete_node(p_acl_table->entry_list, entry_node);
    mem_free(p_table_member);

    status = ctc_sai_find_attrib_in_list(SAI_ACL_KEY_ATTR_NUM, p_acl_entry->key_attr_list, SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclfield.enable)
    {
        for (ii = 0; ii < attr_value->aclfield.data.objlist.count; ii++)
        {
            range_id = attr_value->aclfield.data.objlist.list[ii];
            p_acl_range = ctc_sai_db_get_object_property(lchip, range_id);
            p_acl_range->ref_cnt--;
        }
    }

    status = ctc_sai_find_attrib_in_list(SAI_ACL_ACTION_ATTR_NUM, p_acl_entry->action_attr_list, SAI_ACL_ENTRY_ATTR_ACTION_COUNTER, &attr_value, &index);
    if ((!CTC_SAI_ERROR(status)) && attr_value->aclaction.enable)
    {
        p_acl_counter = ctc_sai_db_get_object_property(lchip, attr_value->aclaction.parameter.oid);
        p_acl_counter->ref_cnt--;
    }

    /* free key attribute list */
    mem_free(p_acl_entry->key_attr_list);

    /* free action attribute list */
    mem_free(p_acl_entry->action_attr_list);

    ctc_sai_db_remove_object_property(lchip, acl_entry_id);

    mem_free(p_acl_entry);

    p_acl_table->created_entry_count--;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Set ACL entry attribute
 *
 * @param[in] acl_entry_id The ACL entry id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_set_acl_entry_attribute(sai_object_id_t acl_entry_id,
                                    const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;
    ctc_sai_acl_entry_t* p_acl_entry = NULL;
    ctc_sai_acl_table_t* p_acl_table = NULL;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_entry_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    p_acl_entry = ctc_sai_db_get_object_property(lchip, acl_entry_id);
    if (NULL == p_acl_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL entry is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto done;
    }

    if ((((SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6 == attr->id) && attr->value.aclfield.enable)
        ||((SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6 == attr->id) && attr->value.aclfield.enable)
        ||((SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL == attr->id) && attr->value.aclfield.enable)
        ||((SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER == attr->id) && attr->value.aclfield.enable))
        && (CTC_ACL_KEY_MAC_IPV6 != p_acl_entry->key_type) && (CTC_ACL_KEY_IPV6 != p_acl_entry->key_type)
        && (CTC_ACL_KEY_IPV6_EXT != p_acl_entry->key_type) && (CTC_ACL_KEY_MAC_IPV6 != p_acl_entry->key_type))
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto done;
    }
    if ((((SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP == attr->id) && attr->value.aclfield.enable)
        ||((SAI_ACL_ENTRY_ATTR_FIELD_DST_IP == attr->id) && attr->value.aclfield.enable))
        && ((CTC_ACL_KEY_MAC_IPV6 == p_acl_entry->key_type) || (CTC_ACL_KEY_IPV6 == p_acl_entry->key_type)
        || (CTC_ACL_KEY_IPV6_EXT == p_acl_entry->key_type) || (CTC_ACL_KEY_MAC_IPV6 == p_acl_entry->key_type)))
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto done;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, p_acl_entry->table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "ACL table id is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto done;
    }
    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_check_acl_entry_key_field(p_acl_table->table_key_bmp, 1, attr), status, done);

    key.key.object_id = acl_entry_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_ENTRY, acl_entry_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl entry attr: %u\n", attr->id);
    }
done:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL entry attribute
 *
 * @param[in] acl_entry_id ACL entry id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_get_acl_entry_attribute(sai_object_id_t acl_entry_id,
                                    uint32 attr_count,
                                    sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t     status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_entry_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_entry_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_ENTRY, loop, acl_entry_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl entry attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


#define ________SAI_ACL_TABLE________

/**
 * @brief Create an ACL Table
 *
 * @param[out] acl_table_id The ACL table id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_table(sai_object_id_t *acl_table_id,
                             sai_object_id_t switch_id,
                             uint32 attr_count,
                             const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 table_stage = 0;
    uint8 bind_bmp = 0;
    uint32 ii = 0;
    uint32 jj = 0;
    uint32 table_size = 0;
    uint32 table_index = 0;
    uint32 index = 0;
    const sai_attribute_value_t *attr_value = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;

    uint32 lookup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_table_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl table parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_ATTR_ACL_STAGE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        table_stage = attr_value->s32;
        if ((table_stage != SAI_ACL_STAGE_EGRESS) && (table_stage != SAI_ACL_STAGE_INGRESS))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Invalid table stage value: %d\n", table_stage);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide acl table stage\n");
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        for (ii = 0; ii < attr_value->s32list.count; ii++)
        {
            bind_bmp |= 1 << (attr_value->s32list.list[ii]);
        }
    }
    else
    {
        /* set default bind point list when fail */
        bind_bmp = 0x07;
    }

    if (0 == bind_bmp)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide acl table bind point\n");
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_ATTR_SIZE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if (0 == attr_value->u32)
        {
            table_size = ACL_DEFAULT_TABLE_SIZE;
        }
        else
        {
            table_size = attr_value->u32;
        }
    }
    else
    {
        /* if table size is not present, use default */
        table_size = ACL_DEFAULT_TABLE_SIZE;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX, &table_index), status, error0);
    *acl_table_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_TABLE, lchip, 0, 0, table_index);

    CTC_SAI_LOG_ERROR(SAI_API_ACL, "acl_table_id = 0x%"PRIx64"\n", *acl_table_id);

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_table, sizeof(ctc_sai_acl_table_t));
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate table db memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }

    /* the table match field has to be processed */
    for (ii = SAI_ACL_TABLE_ATTR_FIELD_START; ii <= SAI_ACL_TABLE_ATTR_FIELD_END; ii++)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, ii, &attr_value, &index);
        if ((!CTC_SAI_ERROR(status)) && attr_value->booldata)
        {
            CTC_BMP_SET(p_acl_table->table_key_bmp, SAI_ACL_ATTR_ID2INDEX(ii));
            if (SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE == ii)
            {
                for (jj = 0; jj < attr_value->s32list.count; jj++)
                {
                    switch (attr_value->s32list.list[jj])
                    {
                        case SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE:
                        case SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE:
                        case SAI_ACL_RANGE_TYPE_OUTER_VLAN:
                        case SAI_ACL_RANGE_TYPE_INNER_VLAN:
                        case SAI_ACL_RANGE_TYPE_PACKET_LENGTH:
                            CTC_BIT_SET(p_acl_table->range_type_bmp, attr_value->s32list.list[jj]);
                            break;
                        default:
                            return SAI_STATUS_INVALID_PARAMETER;
                    }
                }
            }
        }
        /* do nothing if not find */
    }

    p_acl_table->table_stage =  table_stage;
    p_acl_table->table_size = table_size;
    p_acl_table->lookup_type = lookup_type;
    p_acl_table->bind_point_list = bind_bmp;
    p_acl_table->created_entry_count = 0;
    p_acl_table->entry_list = ctc_slist_new();

    CTC_SAI_ERROR_GOTO(_ctc_sai_acl_mapping_table_lookup_type(lchip, p_acl_table), status, error1);

    if (NULL == p_acl_table->entry_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to create table's entry list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error2;
    }
    p_acl_table->group_list = ctc_slist_new();
    if (NULL == p_acl_table->group_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to create table's group list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error3;
    }
    p_acl_table->bind_points = ctc_slist_new();
    if (NULL == p_acl_table->bind_points)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to create table's bind points list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error4;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_table_id, (void*)p_acl_table), status, error5);

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error5:
    ctc_slist_free(p_acl_table->bind_points);
error4:
    ctc_slist_free(p_acl_table->group_list);
error3:
    ctc_slist_free(p_acl_table->entry_list);
error2:
    mem_free(p_acl_table);
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX, table_index);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Delete an ACL table
 *
 * @param[in] acl_table_id The ACL table id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_remove_acl_table(sai_object_id_t acl_table_id)
{
    uint8 lchip = 0;
    uint32 table_index = 0;
    ctc_object_id_t ctc_table_object_id = {0};
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_acl_table_t *p_acl_table = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(acl_table_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_id, &ctc_table_object_id);
    table_index = ctc_table_object_id.value;

    p_acl_table = ctc_sai_db_get_object_property(lchip, acl_table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table to be removed is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if (NULL != p_acl_table->entry_list->head)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table to be removed is not empty\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    if (NULL != p_acl_table->group_list->head)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table to be removed is a member of other group(s)\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    if (NULL != p_acl_table->bind_points->head)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table to be removed is bound\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    ctc_slist_free(p_acl_table->entry_list);
    ctc_slist_free(p_acl_table->group_list);
    ctc_slist_free(p_acl_table->bind_points);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX, table_index), status, out);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_remove_object_property(lchip, acl_table_id), status, out);
    mem_free(p_acl_table);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


/**
 * @brief Set ACL table attribute
 *
 * @param[in] acl_table_id The ACL table id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_set_acl_table_attribute(sai_object_id_t acl_table_id,
                                    const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_TABLE, acl_table_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl table attr: %u\n", attr->id);
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL table attribute
 *
 * @param[in] acl_table_id ACL table id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_get_acl_table_attribute(sai_object_id_t acl_table_id,
                                    uint32 attr_count,
                                    sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t     status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_TABLE, loop, acl_table_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl table attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_ACL_TABLE_GROUP________

/**
 * @brief Create an ACL Table Group
 *
 * @param[out] acl_table_group_id The ACL group id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_table_group(sai_object_id_t *acl_table_group_id,
                                   sai_object_id_t switch_id,
                                   uint32 attr_count,
                                   const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 group_type = 0;
    uint8 group_stage = 0;
    uint8 i = 0;
    uint8 bind_bmp = 0;
    uint32 index = 0;
    uint32 group_index = 0;
    const sai_attribute_value_t *attr_value = NULL;
    ctc_sai_acl_group_t *p_acl_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_table_group_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl table group parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    /* set default value when not mandatory */
    group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_ATTR_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        group_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        group_stage = attr_value->s32;
        if ((SAI_ACL_STAGE_EGRESS != group_stage) && (SAI_ACL_STAGE_INGRESS != group_stage))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ACL, "Invalid group stage value: %d\n", group_stage);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide table group stage\n");
        goto error0;
    }

    if (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL == group_type && SAI_ACL_STAGE_EGRESS == group_stage)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Egress stage not support sequential\n");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        /* bit0 <--> SAI_ACL_BIND_POINT_TYPE_PORT  and  bit1 <--> SAI_ACL_BIND_POINT_TYPE_LAG */
        for (i = 0; i < attr_value->s32list.count; i++)
        {
            bind_bmp |= 1 << (attr_value->s32list.list[i]);
        }
    }
    else
    {
        /* set default bind point list when fail */
        bind_bmp = 0x07;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX, &group_index), status, error0);
    *acl_table_group_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_TABLE_GROUP, lchip, 0, 0, group_index);

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_group, sizeof(ctc_sai_acl_group_t));
    if (NULL == p_acl_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate group db memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }

    p_acl_group->group_stage = group_stage;
    p_acl_group->group_type = group_type;
    p_acl_group->bind_point_list = bind_bmp;
    p_acl_group->member_list = ctc_slist_new();
    if (NULL == p_acl_group->member_list)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to create group's member list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error2;
    }
    p_acl_group->bind_points = ctc_slist_new();
    if (NULL == p_acl_group->bind_points)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to create group's bind points list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error3;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_table_group_id, (void*)p_acl_group), status, error4);

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;
error4:
    ctc_slist_free(p_acl_group->bind_points);
error3:
    ctc_slist_free(p_acl_group->member_list);
error2:
    mem_free(p_acl_group);
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX, group_index);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Delete an ACL Group
 *
 * @param[in] acl_table_group_id The ACL group id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_remove_acl_table_group(sai_object_id_t acl_table_group_id)
{
    uint8 lchip = 0;
    uint32 group_index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_group_object_id = {0};
    ctc_sai_acl_group_t *p_acl_group = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(acl_table_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, acl_table_group_id, &ctc_group_object_id);
    group_index = ctc_group_object_id.value;

    p_acl_group = ctc_sai_db_get_object_property(lchip, acl_table_group_id);
    if (NULL == p_acl_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table group to be removed is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if (NULL != p_acl_group->member_list->head)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table group to be removed is not empty\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    if (NULL != p_acl_group->bind_points->head)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL table group to be removed is bound\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    ctc_slist_free(p_acl_group->member_list);
    ctc_slist_free(p_acl_group->bind_points);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX, group_index), status, out);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_remove_object_property(lchip, acl_table_group_id), status, out);
    mem_free(p_acl_group);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Set ACL table group attribute
 *
 * @param[in] acl_table_group_id The ACL table group id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_set_acl_table_group_attribute(sai_object_id_t acl_table_group_id,
                                           const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_group_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_group_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_TABLE_GROUP, acl_table_group_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl table group attr: %u\n", attr->id);
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL table group attribute
 *
 * @param[in] acl_table_group_id ACL table group id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_get_acl_table_group_attribute(sai_object_id_t acl_table_group_id,
                                          uint32 attr_count,
                                          sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t     status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_table_group_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_table_group_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_TABLE_GROUP, loop, acl_table_group_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl table group attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_ACL_COUNTER________
/**
 * @brief Create an ACL counter
 *
 * @param[out] acl_counter_id The ACL counter id
 * @param[in] switch_id The switch Object id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_counter(sai_object_id_t *acl_counter_id,
                               sai_object_id_t switch_id,
                               uint32 attr_count,
                               const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    bool enable_pkt_cnt = false;
    bool enable_byte_cnt = false;
    uint32 counter_index = 0;
    uint32 index = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t table_id;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;
    const sai_attribute_value_t *attr_value = NULL;
    ctc_sai_acl_table_t *p_acl_table = NULL;

    sal_memset(&table_id, 0, sizeof(sai_object_id_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_counter_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl counter id parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_COUNTER_ATTR_TABLE_ID, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide ACL Table id\n");
        goto error0;
    }
    else
    {
        table_id = attr_value->oid;
    }

    p_acl_table = ctc_sai_db_get_object_property(lchip, table_id);
    if (NULL == p_acl_table)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL Table id is not Exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    /* Not Mandatory */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        enable_pkt_cnt = attr_value->booldata;
    }

    /* Not Mandatory */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        enable_byte_cnt = attr_value->booldata;
    }

    if (!enable_pkt_cnt && !enable_byte_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failure to create Counter as both counter types [byte & packet] are false.\n ");
        status = SAI_STATUS_FAILURE;
        goto error0;
    }

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_counter, sizeof(ctc_sai_acl_counter_t));
    if (NULL == p_acl_counter)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Fail to allocate ACL counter memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX, &counter_index), status, error1);
    *acl_counter_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_COUNTER, lchip, 0, 0, counter_index);

    p_acl_counter->table_id = table_id;
    p_acl_counter->enable_pkt_cnt = enable_pkt_cnt;
    p_acl_counter->enable_byte_cnt = enable_byte_cnt;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_counter_id, (void*)p_acl_counter), status, error2);

    p_acl_table->counter_id = *acl_counter_id;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX, counter_index);
error1:
    mem_free(p_acl_counter);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Delete an ACL counter
 *
 * @param[in] acl_counter_id The ACL counter id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_remove_acl_counter(sai_object_id_t acl_counter_id)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_acl_counter_t *p_acl_counter = NULL;

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));

    ctc_sai_oid_get_lchip(acl_counter_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_RANGE, acl_counter_id, &ctc_object_id);

    p_acl_counter = ctc_sai_db_get_object_property(lchip, acl_counter_id);
    if (NULL == p_acl_counter)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if (p_acl_counter->ref_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL counter is in use\n");
        status = SAI_STATUS_FAILURE;
        goto error0;
    }

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX, ctc_object_id.value);
    ctc_sai_db_remove_object_property(lchip, acl_counter_id);
    ctcs_stats_destroy_statsid(lchip, p_acl_counter->stats_id);
    mem_free(p_acl_counter);

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Set ACL counter attribute
 *
 * @param[in] acl_counter_id The ACL counter id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_set_acl_counter_attribute(sai_object_id_t acl_counter_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_counter_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_counter_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_COUNTER, acl_counter_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl counter attr: %u\n", attr->id);
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL counter attribute
 *
 * @param[in] acl_counter_id ACL counter id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_get_acl_counter_attribute(sai_object_id_t acl_counter_id,
                                      uint32 attr_count,
                                      sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_counter_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_counter_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_COUNTER, loop, acl_counter_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl counter attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_ACL_RANGE________

sai_status_t
_ctc_sai_acl_create_acl_vlan_range(uint8 lchip, sai_acl_range_type_t type, sai_acl_stage_t stage, uint16 min, uint16 max, sai_object_id_t* p_range_id, ctc_sai_acl_range_t* p_acl_range)
{
    uint8  count = 0;
    int32  status = SAI_STATUS_SUCCESS;
    uint32 range_index = 0;
    sai_object_id_t acl_range_id = 0;
    ctc_vlan_range_info_t vrange_info;
    ctc_vlan_range_group_t vrange_group;
    ctc_vlan_range_t vlan_range;
    ctc_sai_acl_range_t* p_acl_range_old = NULL;

    sal_memset(&vrange_info, 0 , sizeof(ctc_vlan_range_info_t));

    for (range_index = ACL_VLAN_RANGE_NUM/2; range_index < ACL_VLAN_RANGE_NUM; range_index++)
    {
        acl_range_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_RANGE, lchip, type, 0, range_index);
        p_acl_range_old = ctc_sai_db_get_object_property(lchip, acl_range_id);

        if (NULL != p_acl_range_old)
        {
            vrange_info.direction = (SAI_ACL_STAGE_INGRESS == stage) ? CTC_INGRESS : CTC_EGRESS;
            vrange_info.vrange_grpid = p_acl_range_old->group_id;

            status = ctcs_vlan_get_vlan_range(lchip, &vrange_info, &vrange_group, &count);
            if (CTC_E_NOT_EXIST == status)
            {
                continue;
            }
            else if (CTC_E_NONE == status)
            {
                if ((1 == count) && (vrange_group.vlan_range[0].vlan_start == min) && (vrange_group.vlan_range[0].vlan_end == max))
                {
                    return SAI_STATUS_ITEM_ALREADY_EXISTS;
                }
            }
            else
            {
                return SAI_STATUS_FAILURE;
            }
        }
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX, &range_index), status, error0);
    vrange_info.direction = (SAI_ACL_STAGE_INGRESS == stage) ? CTC_INGRESS : CTC_EGRESS;
    vrange_info.vrange_grpid = range_index;
    CTC_SAI_ERROR_GOTO(ctcs_vlan_create_vlan_range_group(lchip, &vrange_info, (type == SAI_ACL_RANGE_TYPE_OUTER_VLAN)), status, error1);

    vlan_range.is_acl = 1;
    vlan_range.vlan_start = min;
    vlan_range.vlan_end = max;
    CTC_SAI_ERROR_GOTO(ctcs_vlan_add_vlan_range(lchip, &vrange_info, &vlan_range), status, error2);

    acl_range_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_RANGE, lchip, type, 0, range_index);

    p_acl_range->group_id = range_index;

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, acl_range_id, p_acl_range), status, error3);

    *p_range_id = acl_range_id;
    return status;


error3:
    ctcs_vlan_remove_vlan_range(lchip, &vrange_info, &vlan_range);
error2:
    ctcs_vlan_destroy_vlan_range_group(lchip, &vrange_info);
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX, range_index);
error0:
    return status;
}

sai_status_t
_ctc_sai_acl_remove_acl_vlan_range(uint8 lchip, sai_object_id_t acl_range_id)
{
    ctc_vlan_range_info_t vrange_info;
    ctc_sai_acl_range_t* p_acl_range = NULL;
    ctc_vlan_range_t vlan_range;
    ctc_object_id_t ctc_object_id;

    sal_memset(&vrange_info, 0 , sizeof(ctc_vlan_range_info_t));

    p_acl_range = ctc_sai_db_get_object_property(lchip, acl_range_id);
    if (NULL != p_acl_range)
    {
        vrange_info.vrange_grpid = p_acl_range->group_id;
        vrange_info.direction = (SAI_ACL_STAGE_INGRESS == p_acl_range->stage) ? CTC_INGRESS : CTC_EGRESS;

        vlan_range.is_acl = 1;
        vlan_range.vlan_start = p_acl_range->range_min;
        vlan_range.vlan_end = p_acl_range->range_max;

        CTC_SAI_ERROR_RETURN(ctcs_vlan_remove_vlan_range(lchip, &vrange_info, &vlan_range));
        CTC_SAI_ERROR_RETURN(ctcs_vlan_destroy_vlan_range_group(lchip, &vrange_info));

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_RANGE, acl_range_id, &ctc_object_id);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX, ctc_object_id.value);
        ctc_sai_db_remove_object_property(lchip, acl_range_id);
        mem_free(p_acl_range);
    }
    else
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Create an ACL Range
 *
 * @param[out] acl_range_id The ACL range id
 * @param[in] switch_id The Switch object id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_create_acl_range(sai_object_id_t* acl_range_id,
                             sai_object_id_t switch_id,
                             uint32 attr_count,
                             const sai_attribute_t *attr_list)
{
    uint8  lchip = 0;
    int32  range_type = 0;
    uint32 range_index = 0;
    uint32 index = 0;
    sai_acl_stage_t acl_stage;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_acl_range_t* p_acl_range = NULL;

    const sai_attribute_value_t *attr_value = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    if (NULL == acl_range_id)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL pointer\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if ((0 == attr_count) || (NULL == attr_list))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "NULL acl range id parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_RANGE_ATTR_TYPE, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide ACL range type\n");
        goto error0;
    }
    else
    {
        range_type = attr_value->s32;
    }


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_RANGE_ATTR_STAGE, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide ACL stage\n");
        goto error0;
    }
    else
    {
        acl_stage = attr_value->s32;
    }


    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ACL_RANGE_ATTR_LIMIT, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide ACL range Limit\n");
        goto error0;
    }

    if (attr_value->u32range.min > attr_value->u32range.max)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Invalid range value - min[%d] > max[%d]\n", attr_value->u32range.min, attr_value->u32range.max);
        goto error0;
    }

    MALLOC_ZERO(MEM_ACL_MODULE, p_acl_range, sizeof(ctc_sai_acl_range_t));
    if (NULL == p_acl_range)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Need provide ACL range Limit\n");
        goto error0;
    }

    p_acl_range->range_type = range_type;
    p_acl_range->stage = acl_stage;
    p_acl_range->range_min = attr_value->u32range.min;
    p_acl_range->range_max = attr_value->u32range.max;

    if ((SAI_ACL_RANGE_TYPE_OUTER_VLAN == range_type) || (SAI_ACL_RANGE_TYPE_INNER_VLAN == range_type))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_acl_create_acl_vlan_range(lchip, range_type, acl_stage, attr_value->u32range.min, attr_value->u32range.max, acl_range_id, p_acl_range), status, error1);
    }
    else
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX, &range_index), status, error1);
        *acl_range_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ACL_RANGE, lchip, 0, 0, range_index);
        p_acl_range->group_id = range_index;
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *acl_range_id, (void*)p_acl_range), status, error2);

        /* port and packet length range allocate when add key field */
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX, range_index);
error1:
    mem_free(p_acl_range);
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Remove an ACL Range
 *
 * @param[in] acl_range_id The ACL range id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_remove_acl_range(sai_object_id_t acl_range_id)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_acl_range_t* p_acl_range = NULL;

    ctc_sai_oid_get_lchip(acl_range_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ACL_RANGE, acl_range_id, &ctc_object_id);
    p_acl_range = ctc_sai_db_get_object_property(lchip, acl_range_id);
    if (NULL == p_acl_range)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL Range is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if (p_acl_range->ref_cnt >= 1)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "The ACL Range is in use\n");
        status = SAI_STATUS_FAILURE;
        goto error0;
    }

    if ((SAI_ACL_RANGE_TYPE_OUTER_VLAN == p_acl_range->range_type) || (SAI_ACL_RANGE_TYPE_INNER_VLAN == p_acl_range->range_type))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_acl_remove_acl_vlan_range(lchip, acl_range_id), status, error0);
    }
    else
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX, ctc_object_id.value);
        ctc_sai_db_remove_object_property(lchip, acl_range_id);
        mem_free(p_acl_range);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Set ACL range attribute
 *
 * @param[in] acl_range_id The ACL range id
 * @param[in] attr Attribute
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */

sai_status_t
ctc_sai_acl_set_acl_range_attribute(sai_object_id_t acl_range_id,
                                    const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_object_key_t key;
    sai_status_t     status = SAI_STATUS_SUCCESS;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_range_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_range_id;
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_ACL_RANGE, acl_range_attr_fn_entries, attr);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to set acl range attr: %u\n", attr->id);
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

/**
 * @brief Get ACL range attribute
 *
 * @param[in] acl_range_id ACL range id
 * @param[in] attr_count Number of attributes
 * @param[out] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
sai_status_t
ctc_sai_acl_get_acl_range_attribute(sai_object_id_t acl_range_id,
                                    uint32 attr_count,
                                    sai_attribute_t *attr_list)
{
    uint8 loop  = 0;
    uint8 lchip = 0;
    char  key_str[MAX_KEY_STR_LEN];
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;

    sal_memset(&key, 0 , sizeof(sai_object_key_t));

    CTC_SAI_LOG_ENTER(SAI_API_ACL);
    ctc_sai_oid_get_lchip(acl_range_id, &lchip);
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = acl_range_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_ACL_RANGE, loop, acl_range_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_ACL, "Failed to get acl range attr: %u\n", attr_list[loop].id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_acl_api_t ctc_sai_acl_api = {
    ctc_sai_acl_create_acl_table,
    ctc_sai_acl_remove_acl_table,
    ctc_sai_acl_set_acl_table_attribute,
    ctc_sai_acl_get_acl_table_attribute,
    ctc_sai_acl_create_acl_entry,
    ctc_sai_acl_remove_acl_entry,
    ctc_sai_acl_set_acl_entry_attribute,
    ctc_sai_acl_get_acl_entry_attribute,
    ctc_sai_acl_create_acl_counter,
    ctc_sai_acl_remove_acl_counter,
    ctc_sai_acl_set_acl_counter_attribute,
    ctc_sai_acl_get_acl_counter_attribute,
    ctc_sai_acl_create_acl_range,
    ctc_sai_acl_remove_acl_range,
    ctc_sai_acl_set_acl_range_attribute,
    ctc_sai_acl_get_acl_range_attribute,
    ctc_sai_acl_create_acl_table_group,
    ctc_sai_acl_remove_acl_table_group,
    ctc_sai_acl_set_acl_table_group_attribute,
    ctc_sai_acl_get_acl_table_group_attribute,
    ctc_sai_acl_create_acl_table_group_member,
    ctc_sai_acl_remove_acl_table_group_member,
    ctc_sai_acl_set_acl_table_group_member_attribute,
    ctc_sai_acl_get_acl_table_group_member_attribute
};

sai_status_t
ctc_sai_acl_api_init()
{
    ctc_sai_register_module_api(SAI_API_ACL, (void*)&ctc_sai_acl_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_acl_db_init(uint8 lchip)
{
    uint32 ii = 0;
    ctc_sai_db_wb_t wb_info;

    /* the tcam key type of tcam lookup type, suppose the simplest condition, reguardless of flex global key control */
    sal_memset(&ctc_sai_key_info, 0, sizeof(ctc_sai_key_info_t));

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L2],        CTC_ACL_KEY_MAC);

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L2_L3],     CTC_ACL_KEY_MAC_IPV4);
    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L2_L3],     CTC_ACL_KEY_MAC_IPV6);

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L3],        CTC_ACL_KEY_IPV4);
    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L3],        CTC_ACL_KEY_IPV6);

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L3_EXT],    CTC_ACL_KEY_IPV4_EXT);
    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L3_EXT],    CTC_ACL_KEY_IPV6_EXT);

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L2_L3_EXT], CTC_ACL_KEY_MAC_IPV4_EXT);
    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_L2_L3_EXT], CTC_ACL_KEY_MAC_IPV6);

    CTC_BIT_SET(ctc_sai_key_info.type2key[CTC_ACL_TCAM_LKUP_TYPE_UDF],       CTC_ACL_KEY_UDF);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_DST_CID);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_MAC_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_MAC_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_STAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_STAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_SVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_STAG_VALID);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CTAG_CFI);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CTAG_COS);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CVLAN_ID);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CTAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_SVLAN_RANGE);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_VLAN_XLATE_HIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC], CTC_FIELD_KEY_CLASS_ID);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_RARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IP_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_VN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_PROTOCOL_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_SENDER_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_TARGET_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_MAC_DA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_MAC_SA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_SENDERIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ARP_TARGETIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_GARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_INTERFACE_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_LABEL_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_LABEL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_EXP0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_SBIT0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_TTL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_LABEL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_EXP1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_SBIT1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_TTL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_LABEL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_EXP2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_SBIT2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_MPLS_TTL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_FCOE_DST_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_FCOE_SRC_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_EGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_INGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IS_ESADI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_IS_TRILL_CHANNEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_INNER_VLANID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_INNER_VLANID_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_LENGTH);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_MULTIHOP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_MULTICAST);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_TRILL_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ETHER_OAM_LEVEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ETHER_OAM_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ETHER_OAM_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_PTP_MESSAGE_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_PTP_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SATPDU_MEF_OUI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SATPDU_OUI_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_SATPDU_PDU_BYTE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_AN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_ES);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_PN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_SC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_SCI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_SL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_UNKNOW_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_EBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_SCB);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_DOT1AE_VER);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4], CTC_FIELD_KEY_CLASS_ID);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IPV6_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IPV6_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IPV6_FLOW_LABEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_VN_ID);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_IP_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_VRFID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6], CTC_FIELD_KEY_ETHER_TYPE);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_RARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NSH_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NSH_NEXT_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NSH_OBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NSH_SI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NSH_SPI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MCAST_RPF_CHECK_FAIL);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VXLAN_RSV1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VXLAN_RSV2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IP_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_PROTOCOL_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_SENDER_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_TARGET_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_MAC_DA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_MAC_SA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_SENDERIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ARP_TARGETIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_GARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_LEVEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IS_Y1731_OAM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_INTERFACE_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_LABEL_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_FCOE_DST_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_FCOE_SRC_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_EGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_INGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IS_ESADI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_IS_TRILL_CHANNEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_INNER_VLANID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_INNER_VLANID_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_LENGTH);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_MULTIHOP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_MULTICAST);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_TRILL_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_PTP_MESSAGE_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_PTP_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SATPDU_MEF_OUI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SATPDU_OUI_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_SATPDU_PDU_BYTE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_AN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_ES);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_PN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SCI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_UNKNOW_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_EBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SCB);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_VER);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_WLAN_RADIO_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_WLAN_RADIO_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_WLAN_CTL_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_VRFID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_AWARE_TUNNEL_INFO);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV4_EXT], CTC_FIELD_KEY_FID);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NSH_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NSH_NEXT_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NSH_OBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NSH_SI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NSH_SPI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IPV6_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IPV6_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IPV6_FLOW_LABEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_MCAST_RPF_CHECK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VXLAN_RSV1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VXLAN_RSV2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VN_ID);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_IP_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_WLAN_RADIO_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_WLAN_RADIO_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_WLAN_CTL_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_VRFID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_AWARE_TUNNEL_INFO);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_L3_TYPE);
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_UDF);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_FID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_IPV6_EXT], CTC_FIELD_KEY_ETHER_TYPE);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_RARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CTAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CTAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CTAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MCAST_RPF_CHECK_FAIL);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MAC_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MAC_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_STAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_STAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_STAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_VN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_PROTOCOL_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_SENDER_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_TARGET_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SENDER_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TARGET_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_MAC_DA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_MAC_SA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_SENDERIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ARP_TARGETIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_GARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ETHER_OAM_LEVEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ETHER_OAM_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ETHER_OAM_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IS_Y1731_OAM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_INTERFACE_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_LABEL_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_LABEL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_EXP0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_SBIT0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_TTL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_LABEL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_EXP1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_SBIT1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_TTL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_LABEL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_EXP2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_SBIT2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_MPLS_TTL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_FCOE_DST_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_FCOE_SRC_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_EGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_INGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IS_ESADI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_IS_TRILL_CHANNEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_INNER_VLANID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_INNER_VLANID_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_LENGTH);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_MULTIHOP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_MULTICAST);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_TRILL_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SLOW_PROTOCOL_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_PTP_MESSAGE_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_PTP_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SATPDU_MEF_OUI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SATPDU_OUI_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_SATPDU_PDU_BYTE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_AN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_ES);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_PN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_SC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_SCI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_SL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_UNKNOW_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_EBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_SCB);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_DOT1AE_VER);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_AWARE_TUNNEL_INFO);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_CPU_REASON_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4], CTC_FIELD_KEY_FID);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_RARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CTAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CTAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CTAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MCAST_RPF_CHECK_FAIL);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MAC_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MAC_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_STAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_STAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_STAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_VN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_PROTOCOL_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_SENDER_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_TARGET_IP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SENDER_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TARGET_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_MAC_DA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_MAC_SA_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_SENDERIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ARP_TARGETIP_CHK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_GARP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_LEVEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_OP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ETHER_OAM_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IS_Y1731_OAM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_INTERFACE_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_LABEL_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL0);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_LABEL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_EXP2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_SBIT2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_MPLS_TTL2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_FCOE_DST_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_FCOE_SRC_FCID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_EGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_INGRESS_NICKNAME);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IS_ESADI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_IS_TRILL_CHANNEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_INNER_VLANID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_INNER_VLANID_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_LENGTH);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_MULTIHOP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_MULTICAST);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_TRILL_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SLOW_PROTOCOL_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_PTP_MESSAGE_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_PTP_VERSION);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SATPDU_MEF_OUI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SATPDU_OUI_SUB_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_SATPDU_PDU_BYTE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_AN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_ES);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_PN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SCI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_UNKNOW_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_CBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_EBIT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_SCB);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_DOT1AE_VER);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_AWARE_TUNNEL_INFO);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_CPU_REASON_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV4_EXT], CTC_FIELD_KEY_L4_USER_TYPE);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CTAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CTAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CTAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_PRECEDENCE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CPU_REASON_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_SRC_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IPV6_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IPV6_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IPV6_FLOW_LABEL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_DECAP);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_ELEPHANT_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_MCAST_RPF_CHECK_FAIL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_INTERFACE_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IGMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_GRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_NVGRE_KEY);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VXLAN_RSV1);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VXLAN_RSV2);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VXLAN_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VN_ID);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_USER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_MAC_DA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_MAC_SA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_ROUTED_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_STAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_STAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_STAG_VALID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_SVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_SVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_CVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_TCP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_IP_TTL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_WLAN_RADIO_MAC);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_WLAN_RADIO_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_WLAN_CTL_PKT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_VRFID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_AWARE_TUNNEL_INFO);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_MAC_IPV6], CTC_FIELD_KEY_ETHER_TYPE);

    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_CLASS_ID);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_IP_HDR_ERROR);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_IP_OPTIONS);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_L4_SRC_PORT);
    /* layer2 type used as vlan num */
    //CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_L2_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_L4_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_GEM_PORT);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_METADATA);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_UDF);
    CTC_BMP_SET(ctc_sai_key_info.key2field[CTC_ACL_KEY_UDF], CTC_FIELD_KEY_UDF_ENTRY_VALID);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC)],             CTC_FIELD_KEY_MAC_SA);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_DST_MAC)],             CTC_FIELD_KEY_MAC_DA);
    //CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN)],         CTC_FIELD_KEY_VLAN_NUM);
    //CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN)],         CTC_FIELD_KEY_STAG_VALID);
    //CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG)],        CTC_FIELD_KEY_VLAN_NUM);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID)],       CTC_FIELD_KEY_SVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI)],      CTC_FIELD_KEY_STAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI)],      CTC_FIELD_KEY_STAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID)],       CTC_FIELD_KEY_CVLAN_ID);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI)],      CTC_FIELD_KEY_CTAG_COS);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI)],      CTC_FIELD_KEY_CTAG_CFI);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE)],      CTC_FIELD_KEY_SVLAN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE)],      CTC_FIELD_KEY_CVLAN_RANGE);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE)],      CTC_FIELD_KEY_IP_PKT_LEN_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE)],          CTC_FIELD_KEY_ETHER_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE)],         CTC_FIELD_KEY_L3_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_IP)],              CTC_FIELD_KEY_IP_SA);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_DST_IP)],              CTC_FIELD_KEY_IP_DA);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6)],            CTC_FIELD_KEY_IPV6_SA);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6)],            CTC_FIELD_KEY_IPV6_DA);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL)],     CTC_FIELD_KEY_IPV6_FLOW_LABEL);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL)],         CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER)],    CTC_FIELD_KEY_IP_PROTOCOL);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_DSCP)],                CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_TOS)],                 CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_TOS)],                 CTC_FIELD_KEY_IP_DSCP);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG)],         CTC_FIELD_KEY_IP_FRAG);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_TTL)],                 CTC_FIELD_KEY_IP_TTL);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT)],         CTC_FIELD_KEY_L4_DST_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT)],         CTC_FIELD_KEY_L4_SRC_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE)],      CTC_FIELD_KEY_L4_SRC_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE)],      CTC_FIELD_KEY_L4_DST_PORT_RANGE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ECN)],                 CTC_FIELD_KEY_IP_ECN);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS)],           CTC_FIELD_KEY_TCP_FLAGS);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE)],           CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE)],         CTC_FIELD_KEY_ICMP_CODE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE)],           CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE)],         CTC_FIELD_KEY_ICMP_TYPE);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI)],          CTC_FIELD_KEY_DOT1AE_SCI);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META)],      CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META)],      CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT)],            CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORT)],             CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS)],            CTC_FIELD_KEY_PORT);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META)],   CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META)], CTC_FIELD_KEY_DST_CID);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META)],       CTC_FIELD_KEY_METADATA);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL)],   CTC_FIELD_KEY_MPLS_LABEL0);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL)],     CTC_FIELD_KEY_MPLS_TTL0);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP)],     CTC_FIELD_KEY_MPLS_EXP0);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS)],     CTC_FIELD_KEY_MPLS_SBIT0);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL)],   CTC_FIELD_KEY_MPLS_LABEL1);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL)],     CTC_FIELD_KEY_MPLS_TTL1);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP)],     CTC_FIELD_KEY_MPLS_EXP1);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS)],     CTC_FIELD_KEY_MPLS_SBIT1);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL)],   CTC_FIELD_KEY_MPLS_LABEL2);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL)],     CTC_FIELD_KEY_MPLS_TTL2);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP)],     CTC_FIELD_KEY_MPLS_EXP2);
    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS)],     CTC_FIELD_KEY_MPLS_SBIT2);

    CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID)],        CTC_FIELD_KEY_INTERFACE_ID);

    for (ii = 0; ii < CTC_FIELD_KEY_NUM; ii++)
    {
        if ((CTC_FIELD_KEY_IPV6_SA == ii) || (CTC_FIELD_KEY_IPV6_DA == ii) || (CTC_FIELD_KEY_IPV6_FLOW_LABEL == ii))
        {
            ctc_sai_key_info.field2packet[ii] = PKT_TYPE_IPV6;
        }
        else if ((CTC_FIELD_KEY_IP_SA == ii) || (CTC_FIELD_KEY_IP_DA == ii))
        {
            ctc_sai_key_info.field2packet[ii] = PKT_TYPE_IPV4;
        }
        else
        {
            ctc_sai_key_info.field2packet[ii] = PKT_TYPE_RESERVED;
        }
    }

    for (ii = 0; ii < CTC_ACL_KEY_NUM; ii++)
    {
        if ((CTC_ACL_KEY_IPV4 == ii) || (CTC_ACL_KEY_IPV4_EXT == ii) || (CTC_ACL_KEY_MAC_IPV4 == ii) || (CTC_ACL_KEY_MAC_IPV4_EXT == ii))
        {
            ctc_sai_key_info.key2packet[ii] = PKT_TYPE_IPV4;
        }
        else if ((CTC_ACL_KEY_IPV6 == ii) || (CTC_ACL_KEY_IPV6_EXT == ii) || (CTC_ACL_KEY_MAC_IPV6 == ii))
        {
            ctc_sai_key_info.key2packet[ii] = PKT_TYPE_IPV6;
        }
        else
        {
            ctc_sai_key_info.key2packet[ii] = PKT_TYPE_RESERVED;
        }
    }

    for (ii = 0; ii < CTC_SAI_UDF_GROUP_MAX_NUM(lchip); ii++)
    {
        CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+ii)], CTC_FIELD_KEY_UDF);
        CTC_BMP_SET(ctc_sai_key_info.attr2field[SAI_ACL_ATTR_ID2INDEX(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+ii)], CTC_FIELD_KEY_UDF_ENTRY_VALID);
    }

    /* group */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_group_t);
    wb_info.wb_sync_cb = _ctc_sai_acl_group_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_acl_group_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_acl_group_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_TABLE_GROUP, (void*)(&wb_info));

    /* table */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_table_t);
    wb_info.wb_sync_cb = _ctc_sai_acl_table_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_acl_table_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_acl_table_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_TABLE, (void*)(&wb_info));

    /* entry */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_entry_t);
    wb_info.wb_sync_cb = _ctc_sai_acl_entry_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_acl_entry_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_acl_entry_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_ENTRY, (void*)(&wb_info));

    /* table group member */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_table_group_member_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_acl_table_group_member_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER, (void*)(&wb_info));

    /* range */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_range_t);
    wb_info.wb_sync_cb = _ctc_sai_acl_range_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_acl_range_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_acl_range_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_RANGE, (void*)(&wb_info));

     /* counter */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(ctc_sai_acl_counter_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_acl_counter_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ACL_COUNTER, (void*)(&wb_info));

    /* acl entry type */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(uint32);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_ACL, (void*)(&wb_info));

    /* acl entry type */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(sai_object_id_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, (void*)(&wb_info));

    /* acl entry type */
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ACL;
    wb_info.data_len = sizeof(sai_object_id_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&wb_info));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_acl_db_deinit(uint8 lchip)
{
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE_GROUP, (hash_traversal_fn)_ctc_sai_acl_table_group_db_deinit_cb, NULL);
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_TABLE, (hash_traversal_fn)_ctc_sai_acl_table_db_deinit_cb, NULL);
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ACL_ENTRY, (hash_traversal_fn)_ctc_sai_acl_entry_db_deinit_cb, NULL);
    return SAI_STATUS_SUCCESS;
}

