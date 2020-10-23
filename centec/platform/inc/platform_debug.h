#ifndef _PLATFORM_DEBUG_H_
#define _PLATFORM_DEBUG_H_

#include "sai.h"
#include "ctc_sai.h"

typedef enum
{
    PLATFORM_BUS_I2C,
    PLATFORM_DEV_FIBER,
} E_PLATFORM_DEBUG_TYPE;

#ifndef S_SPLINT_S
#define PLATFORM_LOG_EMERG(typeenum, fmt, ...)                                                          \
    do { ctc_sai_log(SAI_LOG_LEVEL_CRITICAL, SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_ALERT(typeenum, fmt, ...)                                                          \
    do { ctc_sai_log(SAI_LOG_LEVEL_CRITICAL, SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_CRIT(typeenum, fmt, ...)                                                           \
    do { ctc_sai_log(SAI_LOG_LEVEL_CRITICAL, SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_ERR(typeenum, fmt, ...)                                                            \
    do { ctc_sai_log(SAI_LOG_LEVEL_ERROR,    SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_WARN(typeenum, fmt, ...)                                                           \
    do { ctc_sai_log(SAI_LOG_LEVEL_WARN,     SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_NOTICE(typeenum, fmt, ...)                                                         \
    do { ctc_sai_log(SAI_LOG_LEVEL_NOTICE,   SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#define PLATFORM_LOG_INFO(typeenum, fmt, ...)                                                           \
    do { ctc_sai_log(SAI_LOG_LEVEL_INFO,     SAI_API_UNSPECIFIED,                                       \
        "[Line:%d Func:%s type:" #typeenum"] " fmt, __LINE__, __func__, ##__VA_ARGS__); } while (0)
#else
#define PLATFORM_LOG_EMERG(typeenum, fmt, ...)  do {} while (0)
#define PLATFORM_LOG_ALERT(typeenum, fmt, ...)  do {} while (0)
#define PLATFORM_LOG_CRIT(typeenum, fmt, ...)   do {} while (0)
#define PLATFORM_LOG_ERR(typeenum, fmt, ...)    do {} while (0)
#define PLATFORM_LOG_WARN(typeenum, fmt, ...)   do {} while (0)
#define PLATFORM_LOG_NOTICE(typeenum, fmt, ...) do {} while (0)
#define PLATFORM_LOG_INFO(typeenum, fmt, ...)   do {} while (0)
#endif

#define PLATFORM_CTC_CHK_PTR(typeenum, ptr)                                \
do {                                                                       \
    if ((ptr) == NULL)                                                     \
    {                                                                      \
        PLATFORM_LOG_ERR(typeenum, "%s NULL pointer", __FUNCTION__);       \
        return -1;                                                         \
    }                                                                      \
} while(0)

#define PLATFORM_CTC_CHK_PTR_NULL(typeenum, ptr)                           \
do {                                                                       \
    if ((ptr) == NULL)                                                     \
    {                                                                      \
        PLATFORM_LOG_ERR(typeenum, "%s NULL pointer", __FUNCTION__);       \
        return NULL;                                                       \
    }                                                                      \
} while(0)

#endif
