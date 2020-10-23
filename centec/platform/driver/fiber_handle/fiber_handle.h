#ifndef _FIBER_HANDLE_H_
#define _FIBER_HANDLE_H_

#include "i2c_handle.h"

typedef enum
{
    E_FIBER_SFP = 1,
    E_FIBER_XFP,           
    E_FIBER_SFP_P,
    E_FIBER_QSFP_P,
    E_FIBER_SNAP12
} fiber_device_t;

#define FIBER_DEV_ADDR1   0x50
#define FIBER_DEV_ADDR2   0x51
#define FIBER_DEV_ADDR3   0x56

/******************************************************************************/

/* define the structure including fiber operation paramaters */
struct fiber_para_s {
    uint32 subdev;                   /* I2C address. For XFP, memory map at 50, for SFP, memory map at 50,51 */
    uint32 offset;                   /* the address of the fiber dev register */
    uint32 len;                      /* the length of read/write */
    uint8* val;                      /* value pointer */
};
typedef struct fiber_para_s  fiber_para_t;

/******************************************************************************/

typedef enum
{
    E_FIBER_ASIC_ASIC,       /* Fiber chip select and access by Centec chip i2c Master */
    E_FIBER_I2CDEV_ASIC,     /* Fiber chip select by i2c device and access by Centec chip i2c Master */
    E_FIBER_BRIDGE_I2C,      /* Fiber chip select by i2c bridge and access by CPU i2c Master */
} fiber_access_mode_t;

struct fiber_cs_asic_s
{
    uint8   lchip;
    uint8   ctl_id;

    uint32  slave_bitmap;
};
typedef struct fiber_cs_asic_s fiber_cs_asic_t;

#define CS_I2CDEV_REGS_MAX 4
struct fiber_cs_i2cdev_s
{
    uint8     lchip;
    uint8     ctl_id;

    uint8     cs_bus;
    uint8     cs_dev;
    uint8     cs_regs[CS_I2CDEV_REGS_MAX];
    uint8     cs_reg;
    uint8     cs_no;
};
typedef struct fiber_cs_i2cdev_s fiber_cs_i2cdev_t;

struct fiber_cs_bridge_s
{
    uint8   cs_bus;
};
typedef struct fiber_cs_bridge_s fiber_cs_bridge_t;

/******************************************************************************/

typedef enum
{
    E_FIBER_EN_I2CDEV,       /* Fiber enable by i2cdev */
    E_FIBER_EN_SYSFS,        /* Fiber enable by sysfs */
    E_FIBER_EN_QSFP,         /* QSFP enable by read/write */
} fiber_enable_mode_t;

struct fiber_en_i2cdev_s
{
    uint8 en_bus;
    uint8 en_dev;
    uint8 en_reg;
    uint8 en_no;

};
typedef struct fiber_en_i2cdev_s fiber_en_i2cdev_t;

struct fiber_en_sysfs_s
{
    char sysfs_path[64];
};
typedef struct fiber_en_sysfs_s fiber_en_sysfs_t;

struct fiber_en_qsfp_s
{
    uint8 reserved;
};
typedef struct fiber_en_qsfp_s fiber_en_qsfp_t;

/******************************************************************************/

struct fiber_gen_s {
    int8 fiber_flg;                   /* -1 mean not fiber, other get from fiber_device_t */
    fiber_access_mode_t mode;         /* fiber select and fiber access */
    union
    {
        fiber_cs_asic_t asic;
        fiber_cs_i2cdev_t i2cdev;
        fiber_cs_bridge_t bridge;
    }cs;
    fiber_enable_mode_t en_mode;      /* fiber enable mode */
    union
    {
        fiber_en_i2cdev_t en_i2cdev;
        fiber_en_sysfs_t en_sysfs;
        fiber_en_qsfp_t en_qsfp;
    }en;
};
typedef struct fiber_gen_s fiber_gen_t;

/******************************************************************************/

typedef struct fiber_handle_s fiber_handle_t;
struct fiber_handle_s
{
    int32 (*read)(fiber_handle_t *, fiber_para_t* );    
    int32 (*write)(fiber_handle_t *, fiber_para_t* );
    int32 (*fiber_present)(fiber_handle_t *, uint32 *);
    int32 (*fiber_enable)(fiber_handle_t *, uint32);
    int32 (*fiber_get_info)(fiber_handle_t *, uint8 *, uint32);
    fiber_gen_t fiber_gen;

    i2c_handle_t* phdl_dev1;     /* The hdl of i2c bus or 10G phy, access A0 */  
    i2c_handle_t* phdl_dev2;     /* The hdl of i2c bus or 10G phy, access A2 */  
    i2c_handle_t* phdl_dev3;     /* The hdl of i2c bus or 10G phy, access AC */  
    i2c_handle_t* phdl_dev4;     /* The hdl of 1G phy hdl */ 
    i2c_handle_t* phdl_dev5;      /* The hdl for i2cdev cs */
    i2c_handle_t* phdl_dev6;      /* The hdl for i2cdev en */
};

fiber_handle_t *fiber_create_handle(fiber_gen_t *fiber_pgen);
int32 fiber_handle_module_init(void);
int32 fiber_handle_module_exit(void);

#endif
