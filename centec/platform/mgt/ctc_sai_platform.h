#ifndef _CTC_SAI_PLATFORM_H_
#define _CTC_SAI_PLATFORM_H_

#include "sal.h"
#include "ctc_sai.h"
#include "i2c_handle.h"
#include "fiber_handle.h"
#include "macled_handle.h"

#define MACHINE_FILE "/etc/machine.conf"

typedef enum
{
    FIBER_ABSENT,
    FIBER_INIT1,
    FIBER_INIT2,
    FIBER_PRESENT,
} fiber_present_state_t;

struct fiber_info_s
{
    fiber_gen_t fiber_gen;
    /* sfp dir in sysfs */
    char sysfs_path[64];
    /* fiber handler */
    fiber_handle_t *fiber_hdl;
    fiber_present_state_t present;
    uint8 sync_fiber_present;
};
typedef struct fiber_info_s fiber_info_t;

struct led2mac_s
{
    char sysfs[64];
    mac_led_api_para_t para;
};
typedef struct led2mac_s led2mac_t;

struct macled_info_s
{
    macled_gen_t macled_gen;
    macled_handle_t *macled_hdl;
    uint32  led2mac_size;
    led2mac_t *led2mac;
};
typedef struct macled_info_s macled_info_t;

struct phy_info_s
{
    uint8 macid;
    uint8 busid;
    uint8 addr;
};
typedef struct phy_info_s phy_info_t;

struct glb_card_s
{
    int32 fiber_num;
    fiber_info_t *fiber_info_table;

    macled_info_t *macled_info;

    void (*platform_callback)(void);
};
typedef struct glb_card_s glb_card_t;

#endif
