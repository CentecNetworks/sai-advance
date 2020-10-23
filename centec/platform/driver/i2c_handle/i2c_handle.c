#include "sal.h"
#include "ctc_sai.h"
#include "platform_debug.h"
#include "i2c_handle.h"
#include "i2c_cpm.h"

i2c_handle_t *i2c_create_handle(i2c_gen_t *i2c_pgen)
{
    i2c_handle_t *p_i2c_hdl = NULL;

    PLATFORM_LOG_INFO(PLATFORM_BUS_I2C, "i2c_create_handle");

    PLATFORM_CTC_CHK_PTR_NULL(PLATFORM_BUS_I2C, i2c_pgen);

    p_i2c_hdl = (i2c_handle_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(i2c_handle_t));
    PLATFORM_CTC_CHK_PTR_NULL(PLATFORM_BUS_I2C, p_i2c_hdl);
    sal_memset(p_i2c_hdl, 0, sizeof(i2c_handle_t));

    switch (i2c_pgen->i2c_type)
    {
        case E_I2C_CPM:
            i2c_cpm_create_handle(i2c_pgen, p_i2c_hdl);
            break;
        default:
            PLATFORM_LOG_ERR(PLATFORM_BUS_I2C, "i2c_create_bus_handle don't support this type!\n");
            mem_free(p_i2c_hdl);
            p_i2c_hdl = NULL;
            break;
    }

    PLATFORM_CTC_CHK_PTR_NULL(PLATFORM_BUS_I2C, p_i2c_hdl);

    p_i2c_hdl->open(p_i2c_hdl);

    return p_i2c_hdl;
}

int32 i2c_handle_module_init(void)
{
    int32 ret = 0;

    ret += i2c_cpm_module_init();

    return ret;
}

int32 i2c_handle_module_exit(void)
{
    int32 ret = 0;

    ret += i2c_cpm_module_exit();

    return ret;
}
