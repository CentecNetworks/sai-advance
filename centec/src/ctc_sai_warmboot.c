#include "ctc_sai_db.h"
#include "ctc_sai_warmboot.h"
#include "ctc_sai_warmboot_func.h"

typedef struct  ctc_sai_wb_traverse_param_s
{
    uint8 lchip;
    uint8 wb_type;
    uint8 wb_sub_type;
    void* data;
}ctc_sai_wb_traverse_param_t;

uint8 g_wb_status[CTC_SAI_MAX_CHIP_NUM] = {CTC_WB_STATUS_DONE};
extern ctc_sai_db_t* g_sai_db[CTC_SAI_MAX_CHIP_NUM];
/*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/ /* SAI merge 20200824 */
extern sai_status_t ctc_sai_platform_db_run(uint8 lchip);
extern sai_status_t ctc_sai_port_db_run(uint8 lchip);
extern sai_status_t ctc_sai_hostif_db_run(uint8 lchip);

sai_status_t
ctc_sai_warmboot_sync_version(uint8 lchip, uint8 wb_type, uint8 wb_sub_type)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_wb_data_t wb_data;
    uint32 buffer[2] = {0};/*key and data*/
    sal_memset(&wb_data, 0, sizeof(wb_data));
    wb_data.app_id = (lchip << 16) | ( CTC_SAI_WB_TYPE_VERSION << 8) | 0;
    wb_data.key_len = sizeof(uint32);
    wb_data.data_len = sizeof(uint32);
    wb_data.valid_cnt = 1;
    wb_data.buffer_len = sizeof(buffer);
    buffer[0] = (wb_type<< 16) + wb_sub_type;
    buffer[1] = g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].version;
    wb_data.buffer = (ctc_wb_key_data_t*)buffer;
    status = ctc_wb_add_entry(&wb_data);
    return status;
}

sai_status_t
ctc_sai_warmboot_reload_version_check(uint8 lchip, uint8 wb_type, uint8 wb_sub_type)
{
    uint32 version = 0;
    uint32 key = (wb_type<< 16) + wb_sub_type;
    ctc_wb_query_t wb_query;
    uint32 buffer[2] = {0};/*key and data*/
    version = g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].version;
    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.query_type = 1; /*query by key*/
    wb_query.app_id = (lchip << 16) | ( CTC_SAI_WB_TYPE_VERSION << 8) | 0;
    wb_query.key_len = sizeof(uint32);
    wb_query.data_len = sizeof(uint32);
    wb_query.key = (uint8*)(&key);
    wb_query.cursor = 0;
    wb_query.valid_cnt = 0;
    wb_query.buffer_len = sizeof(buffer);
    wb_query.buffer = (ctc_wb_key_data_t*)buffer;
    CTC_SAI_ERROR_RETURN(ctc_wb_query_entry(&wb_query));
    if ((0 == wb_query.valid_cnt) || (CTC_WB_VERSION_CHECK(version, buffer[1])))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "WarmBoot version check fail!!!, wb_type = %d, wb_sub_type = %d\n", wb_type, wb_sub_type);
        return SAI_STATUS_SW_UPGRADE_VERSION_MISMATCH;
    }
    return SAI_STATUS_SUCCESS;
}

int32
ctc_sai_warmboot_sync_cb(void* db, void* user_data)
{
    uint32  max_entry_cnt = 0;
    uint32 offset = 0;
    uint8 lchip = ((ctc_sai_wb_traverse_param_t*)user_data)->lchip;
    ctc_wb_data_t* wb_data = ((ctc_sai_wb_traverse_param_t*)user_data)->data;
    uint8 wb_type = ((ctc_sai_wb_traverse_param_t*)user_data)->wb_type;
    uint8 wb_sub_type = ((ctc_sai_wb_traverse_param_t*)user_data)->wb_sub_type;
    void* data = NULL;

    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data->key_len + wb_data->data_len);
    offset = wb_data->valid_cnt * (wb_data->data_len + wb_data->key_len);
    if (CTC_SAI_WB_TYPE_OID == wb_type)
    {
        data = ((ctc_sai_oid_property_t*)db)->data;
    }
    else if (CTC_SAI_WB_TYPE_ENTRY == wb_type)
    {
        data = ((ctc_sai_entry_property_t*)db)->data;
    }
    else if(CTC_SAI_WB_TYPE_VECTOR == wb_type)
    {
        data = ((ctc_sai_vector_property_t*)db)->data;
    }
    sal_memcpy((uint8*)wb_data->buffer + offset,  (uint8*)db, wb_data->key_len);
    if (wb_data->data_len)
    {
        sal_memcpy((uint8*)wb_data->buffer + offset + wb_data->key_len,  (uint8*)(data), wb_data->data_len);
    }
    if (++wb_data->valid_cnt == max_entry_cnt)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctc_wb_add_entry(wb_data));
        wb_data->valid_cnt = 0;
    }

    if (g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb)/*sync by module when the data have pointer field*/
    {
        g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb(lchip, db, data);
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_warmboot_sync(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    ctc_sai_wb_traverse_param_t wb_param;
    uint32 wb_type = 0;
    uint32 wb_sub_type = 0;
    uint32 sub_type_max[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1] = {SAI_OBJECT_TYPE_MAX, CTC_SAI_DB_ENTRY_TYPE_MAX, CTC_SAI_DB_VECTOR_TYPE_MAX};
    uint32 key_len[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1]  =    {
        CTC_OFFSET_OF(ctc_sai_oid_property_t, calc_key_len),
        CTC_OFFSET_OF(ctc_sai_entry_property_t, calc_key_len),
        CTC_OFFSET_OF(ctc_sai_vector_property_t, calc_key_len)};
    uint8 type_index = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    if (lchip >= CTC_SAI_MAX_CHIP_NUM)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if(NULL == g_sai_db[lchip])
    {
        return SAI_STATUS_UNINITIALIZED;
    }

    sal_memset(&wb_data, 0, sizeof(wb_data));
    sal_memset(&wb_param, 0, sizeof(wb_param));

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    
    g_wb_status[lchip] = CTC_WB_STATUS_SYNC;
    
    if(!CTC_FLAG_ISSET(p_switch_master->flag, SAI_SWITCH_ATTR_PRE_SHUTDOWN))
    {
        ctc_wb_set_cpu_rx_en(lchip, 0);
    }
    ctc_wb_sync(lchip);

    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Sync Data to RedisDB start\n");
    for (wb_type = CTC_SAI_WB_TYPE_OID; wb_type <= CTC_SAI_WB_TYPE_VECTOR; wb_type++)
    {
        type_index = wb_type - CTC_SAI_WB_TYPE_OID;
        for (wb_sub_type = 0; wb_sub_type < sub_type_max[type_index]; wb_sub_type++)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_sai_warmboot_sync_version(lchip, wb_type, wb_sub_type), status, done);
            CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_oid_property_t, wb_type, wb_sub_type);
            wb_data.key_len = key_len[type_index];
            wb_data.data_len = g_sai_db[lchip]->wb_info[type_index][wb_sub_type].data_len;
            sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
            wb_param.wb_type = wb_type;
            wb_param.wb_sub_type = wb_sub_type;
            wb_param.data = &wb_data;
            CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Sync: wb_type = %d, wb_sub_type = %d, key_len = %d, data_len = %d\n", wb_type, wb_sub_type, wb_data.key_len, wb_data.data_len);
            if ((CTC_SAI_WB_TYPE_OID == wb_type)&&g_sai_db[lchip]->oid_hash[wb_sub_type])
            {
                CTC_SAI_CTC_ERROR_GOTO(ctc_hash_traverse_through(g_sai_db[lchip]->oid_hash[wb_sub_type], (hash_traversal_fn)ctc_sai_warmboot_sync_cb, (void *)&wb_param), status, done);
                /* SAI merge 20200824 */
                //ctc_hash_free(g_sai_db[lchip]->oid_hash[wb_sub_type]);
                //g_sai_db[lchip]->oid_hash[wb_sub_type] = NULL;
            }
            else if ((CTC_SAI_WB_TYPE_ENTRY == wb_type)&&g_sai_db[lchip]->entry_hash[wb_sub_type])
            {
                CTC_SAI_CTC_ERROR_GOTO(ctc_hash_traverse_through(g_sai_db[lchip]->entry_hash[wb_sub_type], (hash_traversal_fn)ctc_sai_warmboot_sync_cb, (void *)&wb_param), status, done);
                /* SAI merge 20200824 */
                //ctc_hash_free(g_sai_db[lchip]->entry_hash[wb_sub_type]);
                //g_sai_db[lchip]->entry_hash[wb_sub_type] = NULL;
            }
            else if ((CTC_SAI_WB_TYPE_VECTOR == wb_type)&&g_sai_db[lchip]->vector[wb_sub_type])
            {
                CTC_SAI_CTC_ERROR_GOTO(ctc_vector_traverse(g_sai_db[lchip]->vector[wb_sub_type], (hash_traversal_fn)ctc_sai_warmboot_sync_cb, (void *)&wb_param), status, done);
                /* SAI merge 20200824 */
                //ctc_vector_release(g_sai_db[lchip]->vector[wb_sub_type]);
                //g_sai_db[lchip]->vector[wb_sub_type] = NULL;
            }
            if (wb_data.valid_cnt > 0)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, done);
                wb_data.valid_cnt = 0;
            }

            if (g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb1)/*sync by module global mastre */
            {
                g_sai_db[lchip]->wb_info[wb_type - CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb1(lchip);
            }
        }
    }

    ctc_wb_sync_done(lchip, 0);
    ctc_wb_set_cpu_rx_en(lchip, 1);
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Sync Data to RedisDB end\n");

done:
    if (wb_data.buffer)
    {
        mem_free(wb_data.buffer);
    }
    g_wb_status[lchip] = CTC_WB_STATUS_DONE;
    return status;
}

sai_status_t
ctc_sai_warmboot_reload(uint8 lchip)
{
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    uint32 wb_type = 0;
    uint32 wb_sub_type = 0;
    uint32 sub_type_max[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1] = {SAI_OBJECT_TYPE_MAX, CTC_SAI_DB_ENTRY_TYPE_MAX, CTC_SAI_DB_VECTOR_TYPE_MAX};
    uint32 key_len[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1]  =    {
        CTC_OFFSET_OF(ctc_sai_oid_property_t, calc_key_len),
        CTC_OFFSET_OF(ctc_sai_entry_property_t, calc_key_len),
        CTC_OFFSET_OF(ctc_sai_vector_property_t, calc_key_len)};
    uint32 db_len[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1] = {sizeof(ctc_sai_oid_property_t),sizeof(ctc_sai_entry_property_t),sizeof(ctc_sai_vector_property_t)};
    uint8 type_index = 0;
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    void* data = NULL;
    void* db = NULL;

    if (lchip >= CTC_SAI_MAX_CHIP_NUM)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if(NULL == g_sai_db[lchip])
    {
        return SAI_STATUS_UNINITIALIZED;
    }

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    g_wb_status[lchip] = CTC_WB_STATUS_RELOADING;

    /*SYSTEM MODIFIED by yoush for warm reboot in 2020-08-14*/ /* SAI merge 20200824 */
    /*
    It must reload object SAI_OBJECT_TYPE_SWITCH firstly,
    because other object would use p_switch_master when reloading data with wb_reload_cb or wb_reload_cb1
    */
    wb_type = CTC_SAI_WB_TYPE_OID;
    wb_sub_type = SAI_OBJECT_TYPE_SWITCH;
    type_index = wb_type - CTC_SAI_WB_TYPE_OID;
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload Switch Master Data from RedisDB start\n");
    if (SAI_STATUS_SUCCESS == ctc_sai_warmboot_reload_version_check(lchip, wb_type, wb_sub_type) && wb_sub_type < sub_type_max[type_index])
    {
        CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_oid_property_t, wb_type, wb_sub_type);
        wb_query.key_len = key_len[type_index];
        wb_query.data_len = g_sai_db[lchip]->wb_info[type_index][wb_sub_type].data_len;
        CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload: wb_type = %d, wb_sub_type = %d, key_len = %d, data_len = %d\n", wb_type, wb_sub_type, wb_query.key_len, wb_query.data_len);
        CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        if (wb_query.data_len)
        {
            data = mem_malloc(MEM_SYSTEM_MODULE,  wb_query.data_len);
            if (NULL == data)
            {
                ret = CTC_E_NO_MEMORY;
                goto done;
            }
            sal_memcpy((uint8*)data, (uint8*)(wb_query.buffer) + offset + wb_query.key_len, wb_query.data_len);
        }
        db = mem_malloc(MEM_SYSTEM_MODULE,  db_len[type_index]);
        if (NULL == db)
        {
            ret = CTC_E_NO_MEMORY;
            goto done;
        }
        sal_memcpy((uint8*)db, (uint8*)(wb_query.buffer) + offset, wb_query.key_len);

        if (CTC_SAI_WB_TYPE_OID == wb_type)
        {
            ((ctc_sai_oid_property_t*)db)->data = data;
            ctc_hash_insert(g_sai_db[lchip]->oid_hash[wb_sub_type], db);
        }
        else if (CTC_SAI_WB_TYPE_ENTRY == wb_type)
        {
            ((ctc_sai_entry_property_t*)db)->data = data;
            ctc_hash_insert(g_sai_db[lchip]->entry_hash[wb_sub_type], db);
        }
        else if (CTC_SAI_WB_TYPE_VECTOR == wb_type)
        {
            ((ctc_sai_vector_property_t*)db)->data = data;
            ctc_vector_add(g_sai_db[lchip]->vector[wb_sub_type], ((ctc_sai_vector_property_t*)db)->index, db);
        }

        if (g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb)
        {
            g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb(lchip, db, data);
        }
        entry_cnt++;
        CTC_WB_QUERY_ENTRY_END((&wb_query));
        if (g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb1)
        {
            g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb1(lchip);
        }

        data = NULL;
    }
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload Switch Master Data from RedisDB end\n");
    /*end*/

    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload Data from RedisDB start\n");
    for (wb_type = CTC_SAI_WB_TYPE_OID; wb_type <= CTC_SAI_WB_TYPE_VECTOR; wb_type++)
    {
        type_index = wb_type - CTC_SAI_WB_TYPE_OID;
        for (wb_sub_type = 0; wb_sub_type < sub_type_max[type_index]; wb_sub_type++)
        {
            /*SYSTEM MODIFIED by yoush for warm reboot in 2020-08-14*/ /* SAI merge 20200824 */
            /*Object SAI_OBJECT_TYPE_SWITCH is reloaded firstly, it should skip reloading SAI_OBJECT_TYPE_SWITCH*/
            if (CTC_SAI_WB_TYPE_OID == wb_type && SAI_OBJECT_TYPE_SWITCH == wb_sub_type)
            {
                continue;
            }
            /*end*/
            if (SAI_STATUS_SUCCESS != ctc_sai_warmboot_reload_version_check(lchip, wb_type, wb_sub_type))
            {
                continue;
            }
            CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_oid_property_t, wb_type, wb_sub_type);
            wb_query.key_len = key_len[type_index];
            wb_query.data_len = g_sai_db[lchip]->wb_info[type_index][wb_sub_type].data_len;
            CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload: wb_type = %d, wb_sub_type = %d, key_len = %d, data_len = %d\n", wb_type, wb_sub_type, wb_query.key_len, wb_query.data_len);
            CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
            CTC_SAI_LOG_INFO(SAI_API_SWITCH, "WarmBoot Reload wb_type = %d, wb_sub_type = %d, key_len = %d, data_len = %d\n", wb_type, wb_sub_type, wb_query.key_len, wb_query.data_len);
            offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
            if (wb_query.data_len)
            {
                data = mem_malloc(MEM_SYSTEM_MODULE,  wb_query.data_len);
                if (NULL == data)
                {
                    ret = SAI_STATUS_NO_MEMORY;
                    goto done;
                }
                sal_memcpy((uint8*)data, (uint8*)(wb_query.buffer) + offset + wb_query.key_len, wb_query.data_len);
            }
            db = mem_malloc(MEM_SYSTEM_MODULE,  db_len[type_index]);
            if (NULL == db)
            {
                ret = SAI_STATUS_NO_MEMORY;
                goto done;
            }
            sal_memcpy((uint8*)db, (uint8*)(wb_query.buffer) + offset, wb_query.key_len);

            if (CTC_SAI_WB_TYPE_OID == wb_type)
            {
                ((ctc_sai_oid_property_t*)db)->data = data;
                ctc_hash_insert(g_sai_db[lchip]->oid_hash[wb_sub_type], db);
            }
            else if (CTC_SAI_WB_TYPE_ENTRY == wb_type)
            {
                ((ctc_sai_entry_property_t*)db)->data = data;
                ctc_hash_insert(g_sai_db[lchip]->entry_hash[wb_sub_type], db);
            }
            else if (CTC_SAI_WB_TYPE_VECTOR == wb_type)
            {
                ((ctc_sai_vector_property_t*)db)->data = data;
                ctc_vector_add(g_sai_db[lchip]->vector[wb_sub_type], ((ctc_sai_vector_property_t*)db)->index, db);
            }

            if (g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb)
            {
                g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb(lchip, db, data);
            }
            entry_cnt++;
            CTC_WB_QUERY_ENTRY_END((&wb_query));
            if (g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb1)
            {
                g_sai_db[lchip]->wb_info[type_index][wb_sub_type].wb_reload_cb1(lchip);
            }

            data = NULL;
        }
    }

    g_wb_status[lchip] = CTC_WB_STATUS_DONE;
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "WarmBoot Reload Data from RedisDB end\n");

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
    return ret;
}

/*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/ /* SAI merge 20200824 */
sai_status_t 
ctc_sai_switch_run_thread(uint8 lchip)
{
#ifdef CTC_PLATFORM
    if (0 == SDK_WORK_PLATFORM)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_platform_db_run(lchip));
    }
#endif
    CTC_SAI_ERROR_RETURN(ctc_sai_port_db_run(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_hostif_db_run(lchip));
    
    return SAI_STATUS_SUCCESS;
}
/*end*/

uint8
ctc_sai_warmboot_get_status(uint8 lchip)
{
    if (lchip >= CTC_SAI_MAX_CHIP_NUM)
    {
        return CTC_WB_STATUS_DONE;
    }
    return g_wb_status[lchip];
}

sai_status_t
ctc_sai_warmboot_init(uint8 lchip, uint8 reloading)
{
    ctc_wb_api_t wb_api;
    sal_memset(&wb_api, 0, sizeof(wb_api));
    wb_api.init = ctc_sai_wb_func_init;
    wb_api.init_done = ctc_sai_wb_func_init_done;
    wb_api.sync = ctc_sai_wb_func_sync;
    wb_api.sync_done = ctc_sai_wb_func_sync_done;
    wb_api.add_entry = ctc_sai_wb_func_add_entry;
    wb_api.query_entry = ctc_sai_wb_func_query_entry;
    wb_api.enable = 1;  /* always is 1 */
    wb_api.mode = 0; /* db mode */
    if (reloading)
    {
        wb_api.reloading = 1;
        g_wb_status[lchip] = CTC_WB_STATUS_RELOADING;
    }
    ctc_wb_init(lchip, &wb_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_warmboot_init_done(uint8 lchip, uint8 reloading)
{
    if (reloading)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_warmboot_reload(lchip));
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_run_thread(lchip));
        CTC_SAI_CTC_ERROR_RETURN(ctc_wb_init_done(lchip));
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_warmboot_register_cb(uint8 lchip, uint32 wb_type, uint32 wb_sub_type, void* wb_info)
{
    if (lchip >= CTC_SAI_MAX_CHIP_NUM)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if (NULL == g_sai_db[lchip])
    {
        return SAI_STATUS_UNINITIALIZED;
    }
    if ((wb_type < CTC_SAI_WB_TYPE_OID) || (wb_type > CTC_SAI_WB_TYPE_VECTOR)
        || (wb_sub_type >= SAI_OBJECT_TYPE_MAX))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb = ((ctc_sai_db_wb_t*)wb_info)->wb_sync_cb;
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_sync_cb1 = ((ctc_sai_db_wb_t*)wb_info)->wb_sync_cb1;
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_reload_cb = ((ctc_sai_db_wb_t*)wb_info)->wb_reload_cb;
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].wb_reload_cb1 = ((ctc_sai_db_wb_t*)wb_info)->wb_reload_cb1;
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].data_len = ((ctc_sai_db_wb_t*)wb_info)->data_len;
    g_sai_db[lchip]->wb_info[wb_type-CTC_SAI_WB_TYPE_OID][wb_sub_type].version = ((ctc_sai_db_wb_t*)wb_info)->version;
    return SAI_STATUS_SUCCESS;
}

