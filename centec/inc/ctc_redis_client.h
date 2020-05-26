
#ifndef _CTC_REDIS_CLIENT_H_
#define _CTC_REDIS_CLIENT_H_

typedef struct
{
    char                    address[64];
    uint32                  port;
    uint32                  count;
    redisContext           *p_context;
} ctc_redis_client_master_t;

ctc_redis_client_master_t *g_db_master = NULL;

#endif /* !_CTC_REDIS_CLIENT_H_ */

