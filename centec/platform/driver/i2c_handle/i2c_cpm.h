#ifndef _I2C_CPM_H_
#define _I2C_CPM_H_

int32 i2c_cpm_create_handle(i2c_gen_t *i2c_pgen, i2c_handle_t *p_i2c_hdl);
int32 i2c_cpm_module_init(void);
int32 i2c_cpm_module_exit(void);
#endif
