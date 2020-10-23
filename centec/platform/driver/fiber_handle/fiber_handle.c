#include "sal.h"
#include "ctc_sai.h"
#include "fiber_handle.h"
#include "i2c_handle.h"
#include "platform_debug.h"


#define SFP_A0_REG_LEN  95
#define XFP_REG_LEN     221
#define QSFP_STATUS     2
#define QSFP_REG_LEN    95
#define QSFP_BASIC_INFO_BASE                   131


struct fiber_cpm_mutex_s {
    sal_mutex_t* mutex;
};
typedef struct fiber_cpm_mutex_s fiber_cpm_mutex_t;
fiber_cpm_mutex_t g_fiber_mutex = { NULL };


int32 fiber_ctc_chip_read(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    int32 ret = 0;
    uint32 slave_bitmap = 0;
    ctc_chip_i2c_read_t sfp_para;

    if (NULL == p_fiber_hdl || NULL == para || NULL == para->val)
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER read: Invalid parameter");
        return -1;
    }

    sal_memset(&sfp_para, 0, sizeof(ctc_chip_i2c_read_t));
    slave_bitmap = p_fiber_hdl->fiber_gen.cs.asic.slave_bitmap;
    if (slave_bitmap < 0)
    {
        return -1;
    }
#if (defined GOLDENGATE) || (defined DUET2) || (defined TSINGMA)
    sfp_para.slave_dev_id = slave_bitmap;
    sfp_para.slave_bitmap = 0;
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.asic.lchip;
    sfp_para.ctl_id = p_fiber_hdl->fiber_gen.cs.asic.ctl_id;
    sfp_para.dev_addr = para->subdev;        
    sfp_para.offset = para->offset;
    sfp_para.length = para->len;
    sfp_para.buf_length = para->len;
    sfp_para.p_buf = para->val;
    sfp_para.i2c_switch_id = 0xf; /* when access_switch is 1 this no useful */ 
    sfp_para.access_switch = 0;
#else
    sfp_para.slave_bitmap = (1<<slave_bitmap);    
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.asic.lchip;
    sfp_para.dev_addr = para->subdev;        
    sfp_para.offset = para->offset;
    sfp_para.length = para->len;
    sfp_para.p_buf = para->val;
#endif

    sal_mutex_lock(g_fiber_mutex.mutex);
    ret = ctcs_chip_i2c_read(sfp_para.lchip, &sfp_para);
    sal_mutex_unlock(g_fiber_mutex.mutex);
    if (ret < 0)
    {
        return -1;
    }

    return 0;
}

int32 fiber_ctc_chip_write(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    int32 ret = 0;
    uint32 slave_bitmap;
    ctc_chip_i2c_write_t sfp_para;
    uint8 i;

    if (NULL == p_fiber_hdl || NULL == para || NULL == para->val)
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER write: Invalid parameter");
        return -1;
    }

    sal_memset(&sfp_para, 0, sizeof(ctc_chip_i2c_write_t));
    slave_bitmap = p_fiber_hdl->fiber_gen.cs.asic.slave_bitmap;
    if (slave_bitmap < 0)
    {
        return -1;
    }
#if (defined GOLDENGATE) || (defined DUET2) || (defined TSINGMA)
    sfp_para.dev_addr = para->subdev;
    sfp_para.slave_id = slave_bitmap;
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.asic.lchip;
    sfp_para.ctl_id = p_fiber_hdl->fiber_gen.cs.asic.ctl_id;
    sfp_para.i2c_switch_id = 0xf; /* when access_switch is 1 this no useful */   
    sfp_para.access_switch = 0;/* 1 means disable i2c bridge */
#else
    sfp_para.dev_addr = para->subdev;
    sfp_para.slave_id = slave_bitmap;
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.asic.lchip;
#endif
    sal_mutex_lock(g_fiber_mutex.mutex);
    for (i = 0; i < para->len; i++)
    {
        if(sfp_para.dev_addr == FIBER_DEV_ADDR3)
        {
            sfp_para.offset = para->offset;
        }
        else
        {
            sfp_para.offset = para->offset + i;
        }
        sfp_para.data = para->val[i];
        
        ret = ctcs_chip_i2c_write(sfp_para.lchip, &sfp_para);
        if (ret < 0)
        {
            sal_mutex_unlock(g_fiber_mutex.mutex);
            return -1;
        }    
    }
    sal_mutex_unlock(g_fiber_mutex.mutex);

    return 0;
}

int32 fiber_i2c_read(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    i2c_handle_t *p_i2c_hdl = NULL;
    i2c_op_para_t i2c_para;
    int32 i = 0, ret = 0;
    uint8 *tmpval;

    if (!p_fiber_hdl || !para)
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER read: Invalid parameter");
        return -1;
    }

    if (FIBER_DEV_ADDR1 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev1;
    }
    else if (FIBER_DEV_ADDR2 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev2;
    }
    else if (FIBER_DEV_ADDR3 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev3;
    }
    else
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER read: Invalid parameter");
        return -1;
    }

    i2c_para.offset = para->offset;
    i2c_para.len = para->len;
    tmpval = mem_malloc(MEM_SYSTEM_MODULE, i2c_para.len);
    if(!tmpval)
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER read: out of memory");
        return -1;
    }
    i2c_para.p_val = tmpval;
        
    sal_mutex_lock(g_fiber_mutex.mutex);
    ret = p_i2c_hdl->read(p_i2c_hdl, &i2c_para);
    sal_mutex_unlock(g_fiber_mutex.mutex);
    if(ret < 0)
    {
        mem_free(tmpval);
        return -1;
    }
    for(i = 0; i < i2c_para.len; i++)
    {
        para->val[i] = tmpval[i];
    }
    
    mem_free(tmpval);
    
    return 0;
}

int32 fiber_i2c_write(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    i2c_handle_t* p_i2c_hdl = NULL;
    i2c_op_para_t i2c_para;
    int32 ret = 0;
    
    if(!p_fiber_hdl || !para)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER write: Invalid parameter");
        return -1;
    }

    if (FIBER_DEV_ADDR1 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev1;
    }
    else if (FIBER_DEV_ADDR2 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev2;
    }
    else if (FIBER_DEV_ADDR3 == para->subdev)
    {
        p_i2c_hdl = p_fiber_hdl->phdl_dev3;
    }
    else
    {
        PLATFORM_LOG_ERR(PLATFORM_DEVICE_FIBER, "FIBER write: Invalid parameter");
        return -1;
    }

    i2c_para.offset = para->offset;
    i2c_para.len = para->len;   
    i2c_para.p_val = para->val;
        
    sal_mutex_lock(g_fiber_mutex.mutex);
    ret = p_i2c_hdl->write(p_i2c_hdl, &i2c_para);
    sal_mutex_unlock(g_fiber_mutex.mutex);
    if(ret < 0)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER write: i2c write failed");
        return -1;
    }

    return 0;
}

int32 fiber_ctc_chip_i2cdev_read(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    int32 ret = 0;
    ctc_chip_i2c_read_t sfp_para;
    i2c_handle_t *p_i2c_hdl = NULL;
    i2c_op_para_t i2c_para;
    uint8 val = 0;
    int i = 0;

    if(!p_fiber_hdl || !para)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER read: Invalid parameter");
        return -1;
    }

    p_i2c_hdl = p_fiber_hdl->phdl_dev5;
    i2c_para.len = 1;
    i2c_para.p_val = &val;

    sal_memset(&sfp_para, 0, sizeof(ctc_chip_i2c_read_t));
    sfp_para.slave_dev_id = 1;  /* useless */
    sfp_para.slave_bitmap = 0;  /* useless */
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.i2cdev.lchip;
    sfp_para.ctl_id = p_fiber_hdl->fiber_gen.cs.i2cdev.ctl_id;
    sfp_para.dev_addr = para->subdev;        
    sfp_para.offset = para->offset;
    sfp_para.length = para->len;
    sfp_para.buf_length = para->len;
    sfp_para.p_buf = para->val;
    sfp_para.i2c_switch_id = 0; /* when access_switch is 1 this no useful */
    sfp_para.access_switch = 0;

    sal_mutex_lock(g_fiber_mutex.mutex);
    for (i = 0; i < CS_I2CDEV_REGS_MAX; i++)
    {
        i2c_para.offset = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_regs[i];
        if (p_fiber_hdl->fiber_gen.cs.i2cdev.cs_regs[i] == 0)
            continue;
        val = 0;
        p_i2c_hdl->write(p_i2c_hdl, &i2c_para);
    }
    i2c_para.offset = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_reg;
    val = 1 << p_fiber_hdl->fiber_gen.cs.i2cdev.cs_no;
    p_i2c_hdl->write(p_i2c_hdl, &i2c_para);

    ret = ctcs_chip_i2c_read(sfp_para.lchip, &sfp_para);
    if (ret < 0)
    {
        sal_mutex_unlock(g_fiber_mutex.mutex);
        return -1;
    }
    sal_mutex_unlock(g_fiber_mutex.mutex);
    
    return 0;
}

int32 fiber_ctc_chip_i2cdev_write(fiber_handle_t *p_fiber_hdl, fiber_para_t *para)
{
    int32 ret = 0;
    ctc_chip_i2c_write_t sfp_para;
    i2c_handle_t *p_i2c_hdl = NULL;
    i2c_op_para_t i2c_para;
    uint8 val = 0;
    int i = 0;

    if(!p_fiber_hdl || !para)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER write: Invalid parameter");
        return -1;
    }

    p_i2c_hdl = p_fiber_hdl->phdl_dev5;
    i2c_para.len = 1;
    i2c_para.p_val = &val;

    sal_memset(&sfp_para, 0, sizeof(ctc_chip_i2c_write_t));
    sfp_para.dev_addr = para->subdev;
    sfp_para.slave_id = 1;
    sfp_para.lchip = p_fiber_hdl->fiber_gen.cs.i2cdev.lchip;
    sfp_para.ctl_id = p_fiber_hdl->fiber_gen.cs.i2cdev.ctl_id;
    sfp_para.i2c_switch_id = 0; /* when access_switch is 1 this no useful */  
    sfp_para.access_switch = 0;

    sal_mutex_lock(g_fiber_mutex.mutex);
    for (i = 0; i < CS_I2CDEV_REGS_MAX; i++)
    {
        i2c_para.offset = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_regs[i];
        if (p_fiber_hdl->fiber_gen.cs.i2cdev.cs_regs[i] == 0)
            continue;
        val = 0;
        p_i2c_hdl->write(p_i2c_hdl, &i2c_para);
    }
    i2c_para.offset = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_reg;
    val = 1 << p_fiber_hdl->fiber_gen.cs.i2cdev.cs_no;
    p_i2c_hdl->write(p_i2c_hdl, &i2c_para);

    for(i=0; i<para->len; i++)
    {
        /*For SFP internal PHY, write 16 bits need do two i2c write, and addr must be same*/
        if(sfp_para.dev_addr == FIBER_DEV_ADDR3)
        {
            sfp_para.offset = para->offset;
        }
        else
        {
            sfp_para.offset = para->offset + i;
        }
        sfp_para.data = para->val[i];
        
        ret = ctcs_chip_i2c_write(sfp_para.lchip, &sfp_para);
        if (ret < 0)
        {
            sal_mutex_unlock(g_fiber_mutex.mutex);
            return -1;
        }    
    }
    sal_mutex_unlock(g_fiber_mutex.mutex);
    
    return 0;
}

int32 fiber_get_present_info(fiber_handle_t *p_fiber_hdl, uint32 *present)
{
    int ret = 0;
    uint8 val = 0;
    fiber_para_t sfp_para;

    if (!p_fiber_hdl || !present)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER get present: Invalid parameter");
        return -1;
    }

    sfp_para.subdev = FIBER_DEV_ADDR1;   /* Fiber basic information */
    sfp_para.offset = 1;    
    sfp_para.len = 1;
    sfp_para.val = &val;

    ret = p_fiber_hdl->read(p_fiber_hdl, &sfp_para);  
    if(ret < 0)
    {
        *present = 0;
    }
    else
    {
        if(val == 0xff)
        {
            *present = 0;
        }
        else
        {
            *present = 1;
        }
    }
    return 0;
}

int32 fiber_i2cdev_enable(fiber_handle_t *p_fiber_hdl, uint32 enable)
{
    i2c_handle_t *p_i2c_hdl = NULL;
    i2c_op_para_t i2c_para;
    uint8 val = 0;

    if (!p_fiber_hdl)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER enable: Invalid parameter");
        return -1;
    }

    p_i2c_hdl = p_fiber_hdl->phdl_dev6;

    i2c_para.offset = p_fiber_hdl->fiber_gen.en.en_i2cdev.en_reg;
    i2c_para.len = 1;
    i2c_para.p_val = &val;

    if (!enable)
    {
        val |= (1 << p_fiber_hdl->fiber_gen.en.en_i2cdev.en_no);
    }
    else
    {
        val &= ~(1 << p_fiber_hdl->fiber_gen.en.en_i2cdev.en_no);
    }
    p_i2c_hdl->write(p_i2c_hdl, &i2c_para);

    return 0;
}

int32 fiber_ctc_sysfs_enable(fiber_handle_t *p_fiber_hdl, uint32 enable)
{
    FILE *fp = NULL;

    if (!p_fiber_hdl)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER enable: Invalid parameter");
        return -1;
    }

    fp = sal_fopen(p_fiber_hdl->fiber_gen.en.en_sysfs.sysfs_path, "w");
    if (fp == NULL)
    {
        return -1;
    }
    if (enable)
    {
        sal_fprintf(fp, "%d", 1);
    }
    else
    {
        sal_fprintf(fp, "%d", 0);
    }
    sal_fclose(fp);

    return 0;
}

int32 fiber_ctc_qsfp_enable(fiber_handle_t *p_fiber_hdl, uint32 enable)
{
    int ret = 0;
    uint8 val = 0;
    fiber_para_t sfp_para;

    if (!p_fiber_hdl)
    {
        PLATFORM_LOG_ERR(PLATFROM_DEVICE_FIBER, "FIBER enable: Invalid parameter");
        return -1;
    }

    sfp_para.subdev = FIBER_DEV_ADDR1;   /* Fiber basic information */
    sfp_para.offset = 0x56;
    sfp_para.len = 1;
    sfp_para.val = &val;

    ret = p_fiber_hdl->read(p_fiber_hdl, &sfp_para);
    if(ret < 0)
    {
       return -1;
    }

    if(enable)
    {
        val &= 0xf0;
    }
    else
    {
        val |= 0x0f;
    }
    
    sfp_para.subdev = FIBER_DEV_ADDR1;   /* Fiber basic information */
    sfp_para.offset = 0x56;
    sfp_para.len = 1;
    sfp_para.val = &val;
    ret = p_fiber_hdl->write(p_fiber_hdl, &sfp_para);
    if(ret < 0)
    {
       return -1;
    }

    /* delay 40ms according SFF8436 */
    usleep(40000);
    
    return 0;
}

int32 fiber_get_info(fiber_handle_t *p_fiber_hdl, uint8 *buf, uint32 len)
{
    uint8 buf_tmp[256] = {0};
    fiber_para_t fiber_para;
    uint32 offset = 0;

    for (offset = 0; offset < 256; offset += 64)
    {
        fiber_para.subdev = FIBER_DEV_ADDR1;
        fiber_para.offset = offset;
        fiber_para.len = 64;
        fiber_para.val = buf_tmp + offset;
        p_fiber_hdl->read(p_fiber_hdl, &fiber_para);
    }

    if (len > 256)
    {
        sal_memcpy(buf, buf_tmp, 256);
    }
    else
    {
        sal_memcpy(buf, buf_tmp, len);
    }

    return 0;
}

fiber_handle_t *fiber_create_handle(fiber_gen_t *fiber_pgen)
{
    fiber_handle_t *p_fiber_hdl = NULL;
    i2c_gen_t i2c_gen;

    PLATFORM_LOG_INFO(PLATFORM_DEV_FIBER, "fiber_create_handle");

    PLATFORM_CTC_CHK_PTR_NULL(PLATFORM_DEV_FIBER, fiber_pgen);

    p_fiber_hdl = (fiber_handle_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(fiber_handle_t));
    PLATFORM_CTC_CHK_PTR_NULL(PLATFORM_DEV_FIBER, p_fiber_hdl);
    sal_memset(p_fiber_hdl, 0, sizeof(fiber_handle_t));

    sal_memcpy((uint8 *)(&(p_fiber_hdl->fiber_gen)), (uint8 *)fiber_pgen, sizeof(fiber_gen_t));
    
    switch (p_fiber_hdl->fiber_gen.mode)
    {
        case E_FIBER_ASIC_ASIC:
#ifdef GREATBELT
            /* For bitmap 24~31, GB default is gpio mode, need set to SCL mode GB GPIO 4~11 map to SCL 24-31 */
            if(p_fiber_hdl->fiber_gen.cs.asic.slave_bitmap >= 24)
            {
                ctcs_chip_set_gpio_mode(p_fiber_hdl->fiber_gen.cs.asic.lchip,
                                        p_fiber_hdl->fiber_gen.cs.asic.slave_bitmap - 24 + 4,
                                       CTC_CHIP_SPECIAL_MODE);
            }
#endif 
            p_fiber_hdl->read = fiber_ctc_chip_read;
            p_fiber_hdl->write = fiber_ctc_chip_write;
            break;
        case E_FIBER_BRIDGE_I2C:
            sal_memset(&i2c_gen, 0, sizeof(i2c_gen_t));
            i2c_gen.i2c_type = E_I2C_CPM;
            i2c_gen.gen.i2c_cpm_gen.alen = 1;
            i2c_gen.gen.i2c_cpm_gen.bus_idx = p_fiber_hdl->fiber_gen.cs.bridge.cs_bus;
            i2c_gen.gen.i2c_cpm_gen.addr = FIBER_DEV_ADDR1;
            p_fiber_hdl->phdl_dev1 = i2c_create_handle(&i2c_gen);
            i2c_gen.gen.i2c_cpm_gen.addr = FIBER_DEV_ADDR2;
            p_fiber_hdl->phdl_dev2 = i2c_create_handle(&i2c_gen);
            i2c_gen.gen.i2c_cpm_gen.addr = FIBER_DEV_ADDR3;
            p_fiber_hdl->phdl_dev3 = i2c_create_handle(&i2c_gen);
            p_fiber_hdl->phdl_dev4 = NULL;
            if ((!p_fiber_hdl->phdl_dev1)
             || (!p_fiber_hdl->phdl_dev2)
             || (!p_fiber_hdl->phdl_dev3))
            {
                mem_free(p_fiber_hdl);
                p_fiber_hdl = NULL;
                return p_fiber_hdl;
            }
            p_fiber_hdl->read = fiber_i2c_read;
            p_fiber_hdl->write = fiber_i2c_write;
            break;
        case E_FIBER_I2CDEV_ASIC:
            sal_memset(&i2c_gen, 0, sizeof(i2c_gen_t));
            i2c_gen.i2c_type = E_I2C_CPM;
            i2c_gen.gen.i2c_cpm_gen.alen = 1;
            i2c_gen.gen.i2c_cpm_gen.bus_idx = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_bus;
            i2c_gen.gen.i2c_cpm_gen.addr = p_fiber_hdl->fiber_gen.cs.i2cdev.cs_dev;
            p_fiber_hdl->phdl_dev5 = i2c_create_handle(&i2c_gen);
            if ((!p_fiber_hdl->phdl_dev5))
            {
                mem_free(p_fiber_hdl);
                p_fiber_hdl = NULL;
                return p_fiber_hdl;
            }
            p_fiber_hdl->read = fiber_ctc_chip_i2cdev_read;
            p_fiber_hdl->write = fiber_ctc_chip_i2cdev_write;
            break;
        default:
            mem_free(p_fiber_hdl);
            p_fiber_hdl = NULL;
            return p_fiber_hdl;
    }

    switch (p_fiber_hdl->fiber_gen.en_mode)
    {
        case E_FIBER_EN_I2CDEV:
            sal_memset(&i2c_gen, 0, sizeof(i2c_gen_t));
            i2c_gen.i2c_type = E_I2C_CPM;
            i2c_gen.gen.i2c_cpm_gen.alen = 1;
            i2c_gen.gen.i2c_cpm_gen.bus_idx = p_fiber_hdl->fiber_gen.en.en_i2cdev.en_bus;
            i2c_gen.gen.i2c_cpm_gen.addr = p_fiber_hdl->fiber_gen.en.en_i2cdev.en_dev;
            p_fiber_hdl->phdl_dev6 = i2c_create_handle(&i2c_gen);
            if ((!p_fiber_hdl->phdl_dev6))
            {
                mem_free(p_fiber_hdl);
                p_fiber_hdl = NULL;
                return p_fiber_hdl;
            }
            p_fiber_hdl->fiber_enable  = fiber_i2cdev_enable;
            break;
        case E_FIBER_EN_SYSFS:
            p_fiber_hdl->fiber_enable = fiber_ctc_sysfs_enable;
            break;
        case E_FIBER_EN_QSFP:
            p_fiber_hdl->fiber_enable = fiber_ctc_qsfp_enable;
            break;
        default:
            mem_free(p_fiber_hdl);
            p_fiber_hdl = NULL;
            return p_fiber_hdl;
    }

    p_fiber_hdl->fiber_present = fiber_get_present_info;
    p_fiber_hdl->fiber_get_info = fiber_get_info;

    return p_fiber_hdl;
}

int32 fiber_handle_module_init(void)
{
    sal_mutex_create(&(g_fiber_mutex.mutex));

    return 0;
}

int32 fiber_handle_module_exit(void)
{
    sal_mutex_destroy(g_fiber_mutex.mutex);

    return 0;
}
