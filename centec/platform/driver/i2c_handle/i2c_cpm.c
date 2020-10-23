#include "sal.h"
#include "ctc_sai.h"
#include "platform_debug.h"
#include "i2c_handle.h"
#include <linux/ioctl.h>

/******************************************************************************/

#define I2C_WRITE_OP    0
#define I2C_READ_OP     1
#define I2C_RDWR        0x0707

#define I2C_CPM_ADDR_LEN_MAX 4

/******************************************************************************/

struct ctc_i2c_msg {
    uint16 addr;     
    uint16 flags;           
    uint16 len;              
    uint8 *buf;              
};

struct i2c_rdwr_ioctl_data {
    struct ctc_i2c_msg *msgs; /* pointers to i2c_msgs */
    int32 nmsgs;              /* number of i2c_msgs */
};

/* TODO: mutex can optimize */
struct i2c_cpm_mutex_s {
    sal_mutex_t* mutex;
};
typedef struct i2c_cpm_mutex_s i2c_cpm_mutex_t;

/******************************************************************************/

i2c_cpm_mutex_t g_i2c_cpm_mutex = { NULL };

/******************************************************************************/

int32 i2c_cpm_open(i2c_handle_t *p_i2c_hdl)
{
    char devname_format[] = "/dev/i2c-%d";
    char devname[64] = "";

    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);

    if (p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd < 0)
    {
        sal_snprintf(devname, 64,
                     devname_format, p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.bus_idx);
        p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd = open(devname, O_RDWR);
        if (p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd < 0)
        {
            return -1;
        }
    }

    return 0;
}

int32 i2c_cpm_close(i2c_handle_t *p_i2c_hdl)
{
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);

    if (p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd >= 0)
    {
        close(p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd);
    }
    mem_free(p_i2c_hdl);
    p_i2c_hdl = NULL;

    return 0;
}

int32 i2c_transfer(const i2c_handle_t *p_i2c_hdl, struct i2c_rdwr_ioctl_data *msgset)
{
    int32 ret = 0;

    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, msgset);

    if (p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd < 0)
        return -1;

    ret = ioctl(p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd, I2C_RDWR, msgset);    

    return ret;
}

int32 _i2c_offset_rebuild(uint8 *offset_buf, uint32 offset, uint8 alen)
{
    if(offset_buf == NULL)
    {
        PLATFORM_LOG_ERR(PLATFORM_BUS_I2C, "_i2c_offset_rebuild buf is NULL!\n");
        return -1;
    }
    if(sizeof(offset_buf) / sizeof(uint8) < alen)
    {
        PLATFORM_LOG_ERR(PLATFORM_BUS_I2C, "_i2c_offset_rebuild buf size %d is not enough for offset %d\n",
                         sizeof(offset_buf) / sizeof(uint8), alen);
        return -1;
    }

    if(alen == 1)
    {
        offset_buf[0] = (uint8)(offset & 0xff);        
    }
    else if(alen == 2)
    {
        offset_buf[0] = (uint8)((offset >> 8) & 0xff);
        offset_buf[1] = (uint8)(offset & 0xff);  
    }
    else if(alen == 3)
    { 
        offset_buf[0] = (uint8)((offset >> 16) & 0xff);
        offset_buf[1] = (uint8)((offset >> 8) & 0xff);
        offset_buf[2] = (uint8)(offset & 0xff);  
    }
    else if(alen == 4)
    {
        offset_buf[0] = (uint8)((offset >> 24) & 0xff);  
        offset_buf[1] = (uint8)((offset >> 16) & 0xff);
        offset_buf[2] = (uint8)((offset >> 8) & 0xff);
        offset_buf[3] = (uint8)(offset & 0xff);  
    }
    else
    {
        PLATFORM_LOG_ERR(PLATFORM_BUS_I2C, "Unsupport address len %d\n", alen);
        return -1;
    }

    return 0;
}

int32 i2c_switch_msg(struct ctc_i2c_msg *msg, uint16 addr, uint8 *p_buf, uint16 flag, int32 len)
{
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, msg);
    
    msg->addr = addr;
    msg->buf = p_buf;
    msg->flags = flag;
    msg->len = len;

    return 0;
}

int32 i2c_cpm_read(const i2c_handle_t *p_i2c_hdl, i2c_op_para_t *ppara)
{
    struct i2c_rdwr_ioctl_data msgset;    
    struct ctc_i2c_msg msgs[2];
    i2c_gen_t *i2c_pgen = NULL;
    i2c_op_para_t *i2c_ppara = NULL;
    uint8 buf[I2C_CPM_ADDR_LEN_MAX];
    int32 ret = 0;
    int32 result = 0;

    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, ppara);
    
    i2c_pgen = (i2c_gen_t *)(&(p_i2c_hdl->i2c_gen));
    i2c_ppara = ppara;

    _i2c_offset_rebuild(buf, i2c_ppara->offset, i2c_pgen->gen.i2c_cpm_gen.alen);

    i2c_switch_msg(msgs, i2c_pgen->gen.i2c_cpm_gen.addr, buf, I2C_WRITE_OP, 
                   i2c_pgen->gen.i2c_cpm_gen.alen);
    i2c_switch_msg(msgs+1, i2c_pgen->gen.i2c_cpm_gen.addr, i2c_ppara->p_val,
                   I2C_READ_OP, i2c_ppara->len);
    msgset.msgs = msgs;
    msgset.nmsgs = 2;

    sal_mutex_lock(g_i2c_cpm_mutex.mutex);   
    ret = i2c_transfer(p_i2c_hdl, &msgset);              
    if (ret < 0)
    {
        result--;
        goto exit;
    }    

exit:
    sal_mutex_unlock(g_i2c_cpm_mutex.mutex);  
    return result;
}

int32 i2c_cpm_write(const i2c_handle_t *p_i2c_hdl, i2c_op_para_t *ppara)
{
    struct i2c_rdwr_ioctl_data msgset;    
    struct ctc_i2c_msg msgs[1];
    i2c_gen_t *i2c_pgen = NULL;
    i2c_op_para_t *i2c_ppara = NULL;    
    uint8 *buf;
    int32 buf_len;
    int32 ret = 0;
    
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, ppara);
    
    i2c_pgen = (i2c_gen_t *)(&(p_i2c_hdl->i2c_gen));
    i2c_ppara = ppara;

    buf_len = i2c_ppara->len + i2c_pgen->gen.i2c_cpm_gen.alen;
    
    buf = (uint8 *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(uint8) * buf_len);
    _i2c_offset_rebuild(buf,i2c_ppara->offset,i2c_pgen->gen.i2c_cpm_gen.alen);
    sal_memcpy(&buf[i2c_pgen->gen.i2c_cpm_gen.alen], i2c_ppara->p_val, i2c_ppara->len);
    
    i2c_switch_msg(msgs, i2c_pgen->gen.i2c_cpm_gen.addr, buf, I2C_WRITE_OP, buf_len);                           
    msgset.msgs = msgs;
    msgset.nmsgs = 1;

    sal_mutex_lock(g_i2c_cpm_mutex.mutex);   
    ret = i2c_transfer(p_i2c_hdl, &msgset);    
    if (ret < 0)
    {
        goto exit;
    }
    
exit:
    sal_mutex_unlock(g_i2c_cpm_mutex.mutex);   
    
    if (buf)
    {
        mem_free(buf);
        buf = NULL;
    }
    
    return ret;
}

int32 i2c_cpm_create_handle(i2c_gen_t *i2c_pgen, i2c_handle_t *p_i2c_hdl)
{
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, i2c_pgen);
    PLATFORM_CTC_CHK_PTR(PLATFORM_BUS_I2C, p_i2c_hdl);

    sal_memcpy((uint8 *)(&(p_i2c_hdl->i2c_gen)), (uint8 *)i2c_pgen, sizeof(i2c_gen_t));

    if (E_I2C_CPM == p_i2c_hdl->i2c_gen.i2c_type)
    {
        p_i2c_hdl->i2c_gen.gen.i2c_cpm_gen.fd = -1;

        p_i2c_hdl->open = i2c_cpm_open;
        p_i2c_hdl->close = i2c_cpm_close;
        p_i2c_hdl->read = i2c_cpm_read;
        p_i2c_hdl->write = i2c_cpm_write;
    }
    else 
    {
        mem_free(p_i2c_hdl);
        p_i2c_hdl = NULL;
    }

    return 0;
}

int32 i2c_cpm_module_init(void)
{
    sal_mutex_create(&(g_i2c_cpm_mutex.mutex));
    return 0;
}

int32 i2c_cpm_module_exit(void)
{
    sal_mutex_destroy(g_i2c_cpm_mutex.mutex);
    return 0;
}
