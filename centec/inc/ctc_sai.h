/**
 @file ctc_sai.h

 @date 2017-12-20

 @version v2.0

*/

#ifndef _CTC_SAI_H
#define _CTC_SAI_H
#ifdef __cplusplus
extern "C" {
#endif
/*sai include file*/
#include "saistatus.h"
#include "saitypes.h"
#include "saiobject.h"
#include "sai.h"

#include "ctc_sai_oid.h"

/*can't include API include*/

#define FDB_NOTIF_ATTRIBS_NUM           3

#define MAX_KEY_STR_LEN        100
#define MAX_VALUE_STR_LEN      100
#define MAX_LIST_VALUE_STR_LEN 1000

#define CTC_SAI_FUNC_ATTR_END_ID   0xFFFFFFFF

#define CTC_SAI_DUMP_LINE_LEN 120
#define IN_LINE_CNT 20

//#ifdef CONFIG_SYSLOG
#define CTC_SAI_LOG(level, sai_api_id, fmt, arg...) \
  do {                                          \
    ctc_sai_log(level,                              \
            sai_api_id,                         \
            "[L:%d Func:%s] " fmt,              \
            __LINE__,                           \
            __func__,                           \
            ##arg);                             \
  } while (0);
 #if 0
//#else
#define CTC_SAI_LOG(level,sai_api_id, fmt, arg...) printf(fmt, ##arg)
#endif

#ifndef S_SPLINT_S
#define CTC_SAI_LOG_ENTER(SAI_API_ID) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_DEBUG, SAI_API_ID, "Entering %s", __FUNCTION__)

#define CTC_SAI_LOG_DEBUG(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_DEBUG, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_INFO(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_INFO, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_NOTICE(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_NOTICE, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_WARN(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_WARN, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_ERROR(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_ERROR, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_CRITICAL(SAI_API_ID, fmt, arg...) \
  CTC_SAI_LOG(SAI_LOG_LEVEL_CRITICAL, SAI_API_ID, fmt, ##arg)

#define CTC_SAI_LOG_DUMP(p_file, fmt, arg...) \
  do {                                    \
    if(NULL == p_file)                    \
    {                                     \
        sal_printf(fmt, ##arg);          \
    }                                     \
    else                                  \
    {                                     \
        sal_fprintf(p_file, fmt, ##arg); \
    }                                     \
  } while (0)

#else
#define CTC_SAI_LOG_ENTER(SAI_API_ID)
#define CTC_SAI_LOG_DEBUG(SAI_API_ID, fmt, arg...)

#define CTC_SAI_LOG_INFO(SAI_API_ID, fmt, arg...)
#define CTC_SAI_LOG_NOTICE(SAI_API_ID, fmt, arg...)
#define CTC_SAI_LOG_WARN(SAI_API_ID, fmt, arg...)
#define CTC_SAI_LOG_ERROR(SAI_API_ID, fmt, arg...)
#define CTC_SAI_LOG_CRITICAL(SAI_API_ID, fmt, arg...)
#define CTC_SAI_LOG_DUMP(p_file, fmt, arg...)
#endif
#define CTC_SAI_STR_LENTH(str)  (int32)sal_strlen(str)
#define CTC_SAI_STR_OID_FMT "%-16""PRIx64"

#define CTC_SAI_STR_OID_LENTH(str)  (int32)(sal_strlen(str)>16?sal_strlen(str):16)
#define CTC_SAI_STR_8BYTE_LENTH(str)  (int32)(sal_strlen(str)>8?sal_strlen(str):8)
#define CTC_SAI_STR_4BYTE_LENTH(str)  (int32)sal_strlen(str)>4?sal_strlen(str):4)

/*check api id*/
#define CTC_SAI_API_ID_CHECK(val)                                       \
    do {                                                            \
        if ((val) >= SAI_API_MAX){                                  \
            return SAI_STATUS_INVALID_PARAMETER; }                  \
    } while(0)

#define CTC_SAI_OBJECT_TYPE_CHECK(type)                                             \
    do {                                                                        \
        if ((type) >= SAI_OBJECT_TYPE_MAX) {   \
            return SAI_STATUS_INVALID_OBJECT_TYPE; }                            \
    } while(0)
#define CTC_SAI_ERROR(status) ((status) != SAI_STATUS_SUCCESS)

#define CTC_SAI_PTR_VALID_CHECK(ptr) \
{\
    if ((ptr) == NULL) \
    { \
        return SAI_STATUS_INVALID_PARAMETER; \
    }\
}

/* max value is max valid value */
#define CTC_SAI_MAX_VALUE_CHECK(var, max_value) \
    { \
        if ((var) > (max_value)){return SAI_STATUS_INVALID_PARAMETER; } \
    }

#define CTC_SAI_MIN_VALUE_CHECK(var, min_value)   \
    { \
        if ((var) < (min_value)){return SAI_STATUS_INVALID_PARAMETER; } \
    }

#ifdef _WIN32
#define CTC_SAI_ERROR_RETURN(op) \
    { \
        sai_status_t rv = (op); \
        if (rv > 0) \
        { \
             return (rv); \
        } \
    }
#define CTC_SAI_ERROR_GOTO(op, ret, label) \
    { \
        ret = (op); \
        if (ret > 0) \
        { \
             goto label; \
        } \
    }
#define CTC_SAI_CTC_ERROR_RETURN(op) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        if (rv > 0) \
        { \
            return (rv); \
        } \
    }
#define CTC_SAI_CTC_ERROR_GOTO(op, ret, label) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        ret = (rv); \
        if (ret > 0) \
        { \
            goto label; \
        } \
    }
#define CTC_SAI_ATTR_ERROR_RETURN(op, attr_idx) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        if (rv > 0) \
        { \
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx; \
        } \
    }
#else

#define CTC_SAI_ERROR_RETURN(op) \
    { \
        sai_status_t rv = (op); \
        if (rv < 0) \
        { \
             return (rv); \
        } \
    }
#define CTC_SAI_ERROR_GOTO(op, ret, label) \
    { \
        ret = (op); \
        if (ret < 0) \
        { \
             goto label; \
        } \
    }
#define CTC_SAI_CTC_ERROR_RETURN(op) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        if (rv < 0) \
        { \
            return (rv); \
        } \
    }
#define CTC_SAI_CTC_ERROR_GOTO(op, ret, label) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        ret = (rv); \
        if (ret < 0) \
        { \
            goto label; \
        } \
    }
#define CTC_SAI_ATTR_ERROR_RETURN(op, attr_idx) \
    { \
        sai_status_t rv = ctc_sai_mapping_error_ctc(op); \
        if (rv < 0) \
        { \
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx; \
        } \
    }
#endif


struct sai_api_master_s
{
    void*           module_api[SAI_API_MAX];    /*sai module api*/
    sai_service_method_table_t  services;
    uint32_t         log_level[SAI_API_MAX];
    bool             api_status;

};
typedef struct sai_api_master_s sai_api_master_t;

typedef sai_status_t (*ctc_sai_attribute_set_fn)(sai_object_key_t *key,  const sai_attribute_t *attr);
typedef sai_status_t (*ctc_sai_attribute_get_fn)(sai_object_key_t *key,  sai_attribute_t*attr, sai_uint32_t attr_index);

typedef struct  ctc_sai_attr_func_entry_s
{
  uint32_t        id;

  ctc_sai_attribute_get_fn get;
  ctc_sai_attribute_set_fn set;

} ctc_sai_attr_fn_entry_t;

#define CTC_SAI_NTOH_V6(addr)\
{\
    uint8 i = 0;\
    for (i = 0; i < 4; i++){\
        (addr)[i] = sal_ntohl((addr)[i]);}\
}

#define CTC_SAI_HTON_V6(addr)\
{\
    uint8 i = 0;\
    for (i = 0; i < 4; i++){\
        (addr)[i] = sal_htonl((addr)[i]);}\
}

#define CTC_SAI_NTOH_V4(addr)\
{\
    (addr) = sal_ntohl(addr);\
}

#define CTC_SAI_HTON_V4(addr)\
{\
     (addr) = sal_htonl(addr);\
}


typedef struct  ctc_sai_dump_grep_param_s
{
   sai_uint8_t  lchip;
   sai_uint32_t api_bmp[(SAI_API_MAX-1)/32+1];
   sai_uint32_t object_bmp[(SAI_OBJECT_TYPE_MAX-1)/32+1];
   sai_object_key_t key;
}ctc_sai_dump_grep_param_t;

/****************************************************************************
 *
* Defines and Macros
*
*****************************************************************************/


extern void
ctc_sai_log(int level, sai_api_t api, char *fmt, ...);
extern sai_status_t
ctc_sai_mapping_error_ctc(int32_t ctc_error);

extern sai_status_t
ctc_sai_get_mac_str(sai_mac_t in_mac, char out_mac[]);

extern sai_status_t
ctc_sai_get_ip_str(sai_ip_address_t* ip_addr, char* ip_str_buf);

extern sai_status_t
ctc_sai_get_ipv4_str(sai_ip4_t* ip_addr, char* ip_str_buf);

extern sai_status_t
ctc_sai_get_packet_action_desc(uint8 action_type, char* action_str);

extern sai_status_t
ctc_sai_find_attrib_in_list(uint32_t attr_count,
                                 const sai_attribute_t        *attr_list,
                                 sai_attr_id_t          attrib_id,
                                 const sai_attribute_value_t **attr_value,
                                 uint32_t              *index);


extern sai_status_t
ctc_sai_set_attribute( sai_object_key_t   *key,
                                  char                *key_str,
                                  sai_object_type_t   object_type,
                                 ctc_sai_attr_fn_entry_t *attr_func_list,
                                const  sai_attribute_t       *attr);
extern sai_status_t
ctc_sai_get_attribute(  sai_object_key_t   *key,
                                  char                *key_str,
                                  sai_object_type_t   object_type,
                                  sai_uint32_t attr_idx,
                                 ctc_sai_attr_fn_entry_t *attr_func_list,
                                 sai_attribute_t       *attr);

extern sai_status_t
ctc_sai_register_module_api(sai_api_t sai_api_id, void* module_api);


extern sai_status_t
ctc_sai_get_services_fn(sai_service_method_table_t** p_service_method);

extern sai_status_t
ctc_sai_fill_object_list(uint32_t element_size, void *data, uint32_t count, void *list);

#define MIN_ctc_sai_bridge_ID 4096
#define FDB_NOTIF_ATTRIBS_NUM           3


#ifdef __cplusplus
}
#endif
#endif /*_CTC_SAI_H*/

