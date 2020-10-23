#include "ctc_sai_platform.h"
#include "ctc_board_types.h"

/******************************************************************************
 * e550_24t16y
 ******************************************************************************/

#define E550_24T16Y_FIBER_NUM 16
#define E550_24T16Y_LED_MAC_NUM 16

fiber_info_t e550_24t16y_fiber_table[E550_24T16Y_FIBER_NUM] =
{
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 0}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp1/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp1/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 1}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp2/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp2/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 2}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp3/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp3/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 3}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp4/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp4/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 4}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp5/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp5/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 5}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp6/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp6/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 6}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp7/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp7/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x21, 7}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp8/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp8/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 0}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp9/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp9/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 1}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp10/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp10/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 2}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp11/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp11/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 3}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp12/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp12/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 4}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp13/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp13/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 5}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp14/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp14/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 6}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp15/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp15/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_I2CDEV_ASIC,
                              .cs        = {.i2cdev = {0, 0, 1, 0x36, {0x21, 0x20}, 0x20, 7}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp16/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp16/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
};

macled_info_t e550_24t16y_macled_info;

mac_led_api_para_t e550_24t16y_mac_led_default_entry[E550_24T16Y_LED_MAC_NUM] =
{
    /* panel port 1~8 */
    {
      .port_id = 13,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 12,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 15,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 14,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 29,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 28,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 31,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 30,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    /* panel port 9~16 */
    {
      .port_id = 45,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 44,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 47,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 46,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 62,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 63,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 60,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 61,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
};

led2mac_t e550_24t16y_led2mac[E550_24T16Y_LED_MAC_NUM] =
{
    {
      .sysfs = "/sys/class/leds/port25/brightness",
      .para  = {
                 .port_id = 12,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port26/brightness",
      .para  = {
                 .port_id = 13,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port27/brightness",
      .para  = {
                 .port_id = 14,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port28/brightness",
      .para  = {
                 .port_id = 15,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port29/brightness",
      .para  = {
                 .port_id = 28,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port30/brightness",
      .para  = {
                 .port_id = 29,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port31/brightness",
      .para  = {
                 .port_id = 30,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port32/brightness",
      .para  = {
                 .port_id = 31,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port33/brightness",
      .para  = {
                 .port_id = 44,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port34/brightness",
      .para  = {
                 .port_id = 45,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port35/brightness",
      .para  = {
                 .port_id = 46,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port36/brightness",
      .para  = {
                 .port_id = 47,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port37/brightness",
      .para  = {
                 .port_id = 63,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port38/brightness",
      .para  = {
                 .port_id = 62,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port39/brightness",
      .para  = {
                 .port_id = 61,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port40/brightness",
      .para  = {
                 .port_id = 60,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
};

static ctc_chip_phy_mapping_para_t ctc_sai_e550_24t16y_phy_mapping_para;
phy_info_t ctc_sai_e550_24t16y_phy_info_tbl[] = {
    {
      .macid = 9,
      .busid = 0,
      .addr  = 1,
    },    /* Port 1 */
    {
      .macid = 8,
      .busid = 0,
      .addr  = 0,
    },    /* Port 2 */
    {
      .macid = 11,
      .busid = 0,
      .addr  = 3,
    },    /* Port 3 */
    {
      .macid = 10,
      .busid = 0,
      .addr  = 2,
    },    /* Port 4 */
    {
      .macid = 17,
      .busid = 0,
      .addr  = 5,
    },    /* Port 5 */
    {
      .macid = 16,
      .busid = 0,
      .addr  = 4,
    },    /* Port 6 */
    {
      .macid = 19,
      .busid = 0,
      .addr  = 7,
    },    /* Port 7 */
    {
      .macid = 18,
      .busid = 0,
      .addr  = 6,
    },    /* Port 8 */

    {
      .macid = 21,
      .busid = 0,
      .addr  = 9,
    },    /* Port 9 */
    {
      .macid = 20,
      .busid = 0,
      .addr  = 8,
    },    /* Port 10 */
    {
      .macid = 23,
      .busid = 0,
      .addr  = 11,
    },    /* Port 11 */
    {
      .macid = 22,
      .busid = 0,
      .addr  = 10,
    },    /* Port 12 */
    {
      .macid = 25,
      .busid = 1,
      .addr  = 13,
    },    /* Port 13 */
    {
      .macid = 24,
      .busid = 1,
      .addr  = 12,
    },    /* Port 14 */
    {
      .macid = 27,
      .busid = 1,
      .addr  = 15,
    },    /* Port 15 */
    {
      .macid = 26,
      .busid = 1,
      .addr  = 14,
    },    /* Port 16 */

    {
      .macid = 33,
      .busid = 1,
      .addr  = 17,
    },    /* Port 17 */
    {
      .macid = 32,
      .busid = 1,
      .addr  = 16,
    },    /* Port 18 */
    {
      .macid = 35,
      .busid = 1,
      .addr  = 19,
    },    /* Port 19 */
    {
      .macid = 34,
      .busid = 1,
      .addr  = 18,
    },    /* Port 20 */
    {
      .macid = 37,
      .busid = 1,
      .addr  = 21,
    },    /* Port 21 */
    {
      .macid = 36,
      .busid = 1,
      .addr  = 20,
    },    /* Port 22 */
    {
      .macid = 39,
      .busid = 1,
      .addr  = 23,
    },    /* Port 23 */
    {
      .macid = 38,
      .busid = 1,
      .addr  = 22,
    },    /* Port 24 */
};

int32 ctc_sai_e550_24t16y_create_fiber_handle(glb_card_t *p_glb_card)
{
    int idx = 0;

    p_glb_card->fiber_num = E550_24T16Y_FIBER_NUM;
    p_glb_card->fiber_info_table = e550_24t16y_fiber_table;

    for (idx = 0; idx < E550_24T16Y_FIBER_NUM; idx++)
    {
        e550_24t16y_fiber_table[idx].fiber_hdl = fiber_create_handle(&(e550_24t16y_fiber_table[idx].fiber_gen));
    }

    return 0;
}

int32 ctc_sai_e550_24t16y_create_macled_handle(glb_card_t *p_glb_card)
{
    p_glb_card->macled_info = &e550_24t16y_macled_info;

    p_glb_card->macled_info->macled_gen.mac_table_id = 0;
    p_glb_card->macled_info->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(
                                                          MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
    p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_num = E550_24T16Y_LED_MAC_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->slice0_mac_num = E550_24T16Y_LED_MAC_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->polarity = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para = (mac_led_api_para_t **)mem_malloc(
                                                                            MEM_SYSTEM_MODULE,
                                                                            sizeof(mac_led_api_para_t*) *
                                                                            p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num);
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para[0] = e550_24t16y_mac_led_default_entry;

    p_glb_card->macled_info->macled_hdl = macled_create_handle(&(p_glb_card->macled_info->macled_gen));

    if (p_glb_card->macled_info->macled_hdl != NULL)
        p_glb_card->macled_info->macled_hdl->init(p_glb_card->macled_info->macled_hdl);

    p_glb_card->macled_info->led2mac = (led2mac_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(led2mac_t) * E550_24T16Y_LED_MAC_NUM);
    p_glb_card->macled_info->led2mac_size = E550_24T16Y_LED_MAC_NUM;
    sal_memcpy(p_glb_card->macled_info->led2mac, e550_24t16y_led2mac, sizeof(led2mac_t) * E550_24T16Y_LED_MAC_NUM);
    
    return 0;
}

int32 ctc_sai_e550_24t16y_phy_init(glb_card_t *p_glb_card)
{
    ctc_global_panel_ports_t phy_ports;
    uint8 loop = 0;
    uint32 gport = 0;
    uint8 gchip = 0;

    //SAI Mark, TODO, need phy_drv lib
    //extern int32 ctc_app_phy_init(uint8 lchip);
    //ctc_app_phy_init(0);

    sal_memset(&ctc_sai_e550_24t16y_phy_mapping_para, 0xff, sizeof(ctc_chip_phy_mapping_para_t));
    for (loop = 0; loop < sizeof(ctc_sai_e550_24t16y_phy_info_tbl)/sizeof(phy_info_t); loop++)
    {
        ctc_sai_e550_24t16y_phy_mapping_para.port_mdio_mapping_tbl[ctc_sai_e550_24t16y_phy_info_tbl[loop].macid] = ctc_sai_e550_24t16y_phy_info_tbl[loop].busid;
        ctc_sai_e550_24t16y_phy_mapping_para.port_phy_mapping_tbl[ctc_sai_e550_24t16y_phy_info_tbl[loop].macid] = ctc_sai_e550_24t16y_phy_info_tbl[loop].addr;
    }
    ctcs_chip_set_phy_mapping(0, &ctc_sai_e550_24t16y_phy_mapping_para);

    
    sal_memset(&phy_ports, 0, sizeof(phy_ports));
    ctcs_global_ctl_get(0, CTC_GLOBAL_PANEL_PORTS, (void*)&phy_ports);
    for (loop = 0; loop < phy_ports.count; loop++)
    {
        ctcs_get_gchip_id(0, &gchip);
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, phy_ports.lport[loop]);
        ctcs_port_set_property(0, gport, CTC_PORT_PROP_PHY_INIT, 1);
    }
    for (loop = 0; loop < phy_ports.count; loop++)
    {
        ctcs_get_gchip_id(0, &gchip);
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, phy_ports.lport[loop]);
        ctcs_port_set_port_en(0, gport, 0);
    }

    return 0;
}

int32 ctc_sai_e550_24t16y_board_init(glb_card_t *p_glb_card)
{
    int ret = 0;

    ret += ctc_sai_e550_24t16y_create_fiber_handle(p_glb_card);
    ret += ctc_sai_e550_24t16y_create_macled_handle(p_glb_card);
    ret += ctc_sai_e550_24t16y_phy_init(p_glb_card);

    return ret;
}
