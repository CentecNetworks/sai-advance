#include "ctc_sai_warmboot_func.h"

#define SAI_WB_DB_SIZE_32      32
#define SAI_WB_DB_SIZE_8192    8192
#define SAI_WB_DB_SIZE_FFFF    0xffff

extern int32
ctc_redis_client_init();

extern int32
ctc_redis_client_deinit();

int32
ctc_redis_client_llen_binary(char *key, uint32* total_num);

extern int32
ctc_redis_client_lpush_binary(char *key, uint8 *value, uint32 value_len);

extern int32
ctc_redis_client_lrange_binary(char *key, int32 start, int32 end, uint8 *out_buf, uint32 *buf_len, uint32 *count);

extern int32
ctc_redis_client_flushdb();

extern int32
ctc_redis_client_save();

int32 ctc_sai_wb_func_init(uint8 lchip, uint8 reloading)
{
    int32 ret = 0;
    if (reloading)
    {
        ret = ctc_redis_client_init();
    }
    return ret;
}

int32 ctc_sai_wb_func_init_done(uint8 lchip)
{
    int32 ret = 0;
    ret = ctc_redis_client_deinit();
    return ret;
}

int32 ctc_sai_wb_func_sync(uint8 lchip)
{
    int32 ret = 0;
    ret = ctc_redis_client_init();
    ret = ret? ret : ctc_redis_client_flushdb();
    return ret;
}

int32 ctc_sai_wb_func_sync_done(uint8 lchip, int32 result)
{
    int32 ret = 0;
    ret = ctc_redis_client_save();
    ret = ret? ret : ctc_redis_client_deinit();
    return ret;
}

int32 ctc_sai_wb_func_add_entry(ctc_wb_data_t *data)
{
    int32 ret = 0;
    char key[SAI_WB_DB_SIZE_32];
    uint32 offset = 0;
    uint8 buffer[SAI_WB_DB_SIZE_FFFF];
    uint32 len = 0;
    uint32 i = 0;


    sal_snprintf(key, SAI_WB_DB_SIZE_32, "SDK_%u", data->app_id);
    len = data->key_len + data->data_len;
    if (SAI_WB_DB_SIZE_FFFF < len)
    {
        return -1;
    }
    for (i = 0; i < data->valid_cnt; i++)
    {
        sal_memcpy(buffer, (uint8*)(data->buffer) + offset, len);
        offset += len;
        ret = ctc_redis_client_lpush_binary(key, buffer, len);
        if (ret)
        {
            return ret;
        }
    }

    return 0;
}

int32 _ctc_sai_wb_func_query_entry_by_key(ctc_wb_query_t *query)
{
    char key[SAI_WB_DB_SIZE_32];
    int32 ret = 0;
    uint32 total_num = 0;
    uint8 i = 0;
    uint32 buffer_len = 0;
    uint32 return_cnt = 0;

    sal_snprintf(key, SAI_WB_DB_SIZE_32, "SDK_%u", query->app_id);
    ret = ctc_redis_client_llen_binary(key, &total_num);
    if (ret)
    {
        return ret;
    }

    query->valid_cnt = 0;
    query->is_end = 1;

    for (i = 0; i < total_num; i++)
    {
        buffer_len = query->buffer_len;
        ret = ctc_redis_client_lrange_binary(key, i, i, (uint8*)query->buffer, &buffer_len, &return_cnt);
        if ((0 == buffer_len) || (0 == return_cnt))
        {
            continue;
        }
        if(0 == sal_memcmp((uint8*)(query->key), (uint8*)(query->buffer), query->key_len))
        {
            query->valid_cnt = 1;
            return 0;
        }
    }

    return -1;
}

int32 ctc_sai_wb_func_query_entry(ctc_wb_query_t *query)
{
    char key[SAI_WB_DB_SIZE_32];
    int32 ret = 0;
    uint32 query_cnt = 0;
    uint32 return_cnt = 0;
    uint32 buffer_len = 0;

    query->valid_cnt = 0;
    query->is_end = 1;
    buffer_len = query->buffer_len;

    if ((0 == query->key_len) || (0 == query->buffer_len))
    {
        return -1;
    }

    if (1 == query->query_type)/*by key*/
    {
        ret = _ctc_sai_wb_func_query_entry_by_key(query);
        return ret;
    }

    sal_snprintf(key, SAI_WB_DB_SIZE_32, "SDK_%u", query->app_id);
    query_cnt = query->buffer_len / (query->key_len + query->data_len);

    ret = ctc_redis_client_lrange_binary(key, query->cursor, (query->cursor + query_cnt -1), (uint8*)query->buffer, &buffer_len, &return_cnt);
    query->valid_cnt = return_cnt;
    if (query_cnt > return_cnt)
    {
        query->cursor = 0;
        query->is_end = 1;
    }
    else
    {
        query->cursor += return_cnt;
        query->is_end = 0;
    }

    return ret;
}

