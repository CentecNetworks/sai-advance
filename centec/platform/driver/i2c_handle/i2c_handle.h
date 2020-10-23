#ifndef _I2C_HANDLE_H_
#define _I2C_HANDLE_H_

typedef enum
{
    E_I2C_CPM,              /* the I2C interface is implemented by linux kernel i2c driver */
} i2c_type_e;

struct i2c_cpm_gen_s
{
    uint8 bus_idx;          /* i2c bus idx */
    uint8 addr;             /* i2c device address */
    uint32 alen;            /* address length (byte) */

    int32 fd;               /* alloc by linux kernel */
};
typedef struct i2c_cpm_gen_s i2c_cpm_gen_t;

struct i2c_gen_s
{
    i2c_type_e i2c_type;    /* i2c interface type */
    union
    {
        i2c_cpm_gen_t i2c_cpm_gen;
    } gen;
};
typedef struct i2c_gen_s i2c_gen_t;

struct i2c_op_para_s
{    
    uint32 offset;          /* reg offset in the i2c device */    
    uint8 *p_val;           /* pointer of the value buffur */
    uint32 len;             /* data length (byte)*/    
};
typedef struct i2c_op_para_s i2c_op_para_t;

typedef struct i2c_handle_s i2c_handle_t;
struct i2c_handle_s
{
    int32 (*open)(i2c_handle_t *);
    int32 (*close)(i2c_handle_t *);
    int32 (*read)(const i2c_handle_t *, i2c_op_para_t *);
    int32 (*write)(const i2c_handle_t *, i2c_op_para_t *);
    i2c_gen_t i2c_gen;
};

i2c_handle_t* i2c_create_handle(i2c_gen_t *i2c_pgen);
int32 i2c_handle_module_init(void);
int32 i2c_handle_module_exit(void);
#endif
