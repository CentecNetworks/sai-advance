#include "ctc_sai_platform.h"
#include "ctc_board_types.h"

/******************************************************************************
 * e530_48t4x_p
 ******************************************************************************/

#define E530_48T4X_P_FIBER_NUM 4
#define E530_48T4X_P_LED_MAC_NUM 4

fiber_info_t e530_48t4x_p_fiber_table[E530_48T4X_P_FIBER_NUM] =
{
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 0}},
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
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 1}},
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
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 2}},
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
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 3}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp4/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp4/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
};

macled_info_t e530_48t4x_p_macled_info;

mac_led_api_para_t e530_48t4x_p_mac_led_default_entry[E530_48T4X_P_LED_MAC_NUM] =
{
    /* panel port 49-52 */
    {
      .port_id = 14,
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
      .port_id = 12,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 13,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
};

led2mac_t e530_48t4x_p_led2mac[E530_48T4X_P_LED_MAC_NUM] =
{
    /* panel port 49-52 */
    {
      .sysfs = "/sys/class/leds/port49/brightness",
      .para  = {
                 .port_id = 13,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port50/brightness",
      .para  = {
                 .port_id = 12,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port51/brightness",
      .para  = {
                 .port_id = 15,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port52/brightness",
      .para  = {
                 .port_id = 14,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
};

static ctc_chip_phy_mapping_para_t ctc_sai_e530_48t4x_p_phy_mapping_para;
phy_info_t ctc_sai_e530_48t4x_phy_info_tbl[] = {
    {
      .macid = 1,
      .busid = 0,
      .addr  = 1,
    },    /* Port 1 */
    {
      .macid = 0,
      .busid = 0,
      .addr  = 0,
    },    /* Port 2 */
    {
      .macid = 3,
      .busid = 0,
      .addr  = 3,
    },    /* Port 3 */
    {
      .macid = 2,
      .busid = 0,
      .addr  = 2,
    },    /* Port 4 */
    {
      .macid = 5,
      .busid = 0,
      .addr  = 5,
    },    /* Port 5 */
    {
      .macid = 4,
      .busid = 0,
      .addr  = 4,
    },    /* Port 6 */
    {
      .macid = 7,
      .busid = 0,
      .addr  = 7,
    },    /* Port 7 */
    {
      .macid = 6,
      .busid = 0,
      .addr  = 6,
    },    /* Port 8 */

    {
      .macid = 17,
      .busid = 0,
      .addr  = 9,
    },    /* Port 9 */
    {
      .macid = 16,
      .busid = 0,
      .addr  = 8
    },    /* Port 10 */
    {
      .macid = 19,
      .busid = 0,
      .addr  = 11
    },    /* Port 11 */
    {
      .macid = 18,
      .busid = 0,
      .addr  = 10
    },    /* Port 12 */
    {
      .macid = 21,
      .busid = 0,
      .addr  = 13
    },    /* Port 13 */
    {
      .macid = 20,
      .busid = 0,
      .addr  = 12
    },    /* Port 14 */
    {
      .macid = 23,
      .busid = 0,
      .addr  = 15
    },    /* Port 15 */
    {
      .macid = 22,
      .busid = 0,
      .addr  = 14
    },    /* Port 16 */

    {
      .macid = 9,
      .busid = 1,
      .addr  = 1
    },    /* Port 17 */
    {
      .macid = 8,
      .busid = 1,
      .addr  = 0
    },    /* Port 18 */
    {
      .macid = 11,
      .busid = 1,
      .addr  = 3
    },    /* Port 19 */
    {
      .macid = 10,
      .busid = 1,
      .addr  = 2
    },    /* Port 20 */
    {
      .macid = 33,
      .busid = 1,
      .addr  = 5
    },    /* Port 21 */
    {
      .macid = 32,
      .busid = 1,
      .addr  = 4
    },    /* Port 22 */
    {
      .macid = 35,
      .busid = 1,
      .addr  = 7
    },    /* Port 23 */
    {
      .macid = 34,
      .busid = 1,
      .addr  = 6
    },    /* Port 24 */

    {
      .macid = 37,
      .busid = 1,
      .addr  = 9
    },    /* Port 25 */
    {
      .macid = 36,
      .busid = 1,
      .addr  = 8
    },    /* Port 26 */
    {
      .macid = 39,
      .busid = 1,
      .addr  = 11
    },    /* Port 27 */
    {
      .macid = 38,
      .busid = 1,
      .addr  = 10
    },    /* Port 28 */
    {
      .macid = 41,
      .busid = 1,
      .addr  = 13
    },    /* Port 29 */
    {
      .macid = 40,
      .busid = 1,
      .addr  = 12
    },    /* Port 30 */
    {
      .macid = 43,
      .busid = 1,
      .addr  = 15
    },    /* Port 31 */
    {
      .macid = 42,
      .busid = 1,
      .addr  = 14
    },    /* Port 32 */

    {
      .macid = 25,
      .busid = 2,
      .addr  = 1
    },    /* Port 33 */
    {
      .macid = 24,
      .busid = 2,
      .addr  = 0
    },    /* Port 34 */
    {
      .macid = 27,
      .busid = 2,
      .addr  = 3
    },    /* Port 35 */
    {
      .macid = 26,
      .busid = 2,
      .addr  = 2
    },    /* Port 36 */
    {
      .macid = 49,
      .busid = 2,
      .addr  = 5
    },    /* Port 37 */
    {
      .macid = 48,
      .busid = 2,
      .addr  = 4
    },    /* Port 38 */
    {
      .macid = 51,
      .busid = 2,
      .addr  = 7
    },    /* Port 39 */
    {
      .macid = 50,
      .busid = 2,
      .addr  = 6
    },    /* Port 40 */

    {
      .macid = 53,
      .busid = 3,
      .addr  = 1
    },    /* Port 41 */
    {
      .macid = 52,
      .busid = 3,
      .addr  = 0
    },    /* Port 42 */
    {
      .macid = 55,
      .busid = 3,
      .addr  = 3
    },    /* Port 43 */
    {
      .macid = 54,
      .busid = 3,
      .addr  = 2
    },    /* Port 44 */
    {
      .macid = 57,
      .busid = 3,
      .addr  = 5
    },    /* Port 45 */
    {
      .macid = 56,
      .busid = 3,
      .addr  = 4
    },    /* Port 46 */
    {
      .macid = 59,
      .busid = 3,
      .addr  = 7
    },    /* Port 47 */
    {
      .macid = 58,
      .busid = 3,
      .addr  = 6
    },    /* Port 48 */
};


int32 ctc_sai_e530_48t4x_p_create_fiber_handle(glb_card_t *p_glb_card)
{
    int idx = 0;

    p_glb_card->fiber_num = E530_48T4X_P_FIBER_NUM;
    p_glb_card->fiber_info_table = e530_48t4x_p_fiber_table;

    for (idx = 0; idx < E530_48T4X_P_FIBER_NUM; idx++)
    {
        e530_48t4x_p_fiber_table[idx].fiber_hdl = fiber_create_handle(&(e530_48t4x_p_fiber_table[idx].fiber_gen));
    }

    return 0;
}

int32 ctc_sai_e530_48t4x_p_create_macled_handle(glb_card_t *p_glb_card)
{
    p_glb_card->macled_info = &e530_48t4x_p_macled_info;

    p_glb_card->macled_info->macled_gen.mac_table_id = 0;
    p_glb_card->macled_info->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(
                                                          MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
    p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_num = E530_48T4X_P_LED_MAC_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->slice0_mac_num = E530_48T4X_P_LED_MAC_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->polarity = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para = (mac_led_api_para_t **)mem_malloc(
                                                                            MEM_SYSTEM_MODULE,
                                                                            sizeof(mac_led_api_para_t*) *
                                                                            p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num);
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para[0] = e530_48t4x_p_mac_led_default_entry;

    
    p_glb_card->macled_info->macled_hdl = macled_create_handle(&(p_glb_card->macled_info->macled_gen));


    if (p_glb_card->macled_info->macled_hdl != NULL)
        p_glb_card->macled_info->macled_hdl->init(p_glb_card->macled_info->macled_hdl);

    e530_48t4x_p_macled_info.led2mac = (led2mac_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(led2mac_t) * E530_48T4X_P_LED_MAC_NUM);
    e530_48t4x_p_macled_info.led2mac_size = E530_48T4X_P_LED_MAC_NUM;
    sal_memcpy(p_glb_card->macled_info->led2mac, e530_48t4x_p_led2mac, sizeof(led2mac_t) * E530_48T4X_P_LED_MAC_NUM);
    
    return 0;
}

int32 ctc_sai_e530_48t4x_p_phy_init(glb_card_t *p_glb_card)
{
    ctc_global_panel_ports_t phy_ports;
    uint8 loop = 0;
    uint32 gport = 0;
    uint8 gchip = 0;

    //SAI Mark, TODO, need phy_drv lib
    //extern int32 ctc_app_phy_init(uint8 lchip);
    //ctc_app_phy_init(0);

    sal_memset(&ctc_sai_e530_48t4x_p_phy_mapping_para, 0xff, sizeof(ctc_chip_phy_mapping_para_t));
    for (loop = 0; loop < sizeof(ctc_sai_e530_48t4x_phy_info_tbl)/sizeof(phy_info_t); loop++)
    {
        ctc_sai_e530_48t4x_p_phy_mapping_para.port_mdio_mapping_tbl[ctc_sai_e530_48t4x_phy_info_tbl[loop].macid] = ctc_sai_e530_48t4x_phy_info_tbl[loop].busid;
        ctc_sai_e530_48t4x_p_phy_mapping_para.port_phy_mapping_tbl[ctc_sai_e530_48t4x_phy_info_tbl[loop].macid] = ctc_sai_e530_48t4x_phy_info_tbl[loop].addr;
    }
    ctcs_chip_set_phy_mapping(0, &ctc_sai_e530_48t4x_p_phy_mapping_para);

    
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

void ctc_sai_e530_48t4x_p_platform_callback(void)
{
    int32 temp = -1000;
    FILE *fp = NULL;

    ctcs_get_chip_sensor(0, CTC_CHIP_SENSOR_TEMP, (uint32 *)&temp);

    if (temp >= -40 && temp <= 125)
    {
        fp = sal_fopen("/sys/class/hwmon/hwmon0/temp1_input", "w");
        if (fp == NULL)
        {
            return;
        }
        fprintf(fp, "%d", temp * 1000);
        sal_fclose(fp);
    }

    return;
}

int32 ctc_sai_e530_48t4x_p_board_init(glb_card_t *p_glb_card)
{
    int ret = 0;

    ret += ctc_sai_e530_48t4x_p_create_fiber_handle(p_glb_card);
    ret += ctc_sai_e530_48t4x_p_create_macled_handle(p_glb_card);
    ret += ctc_sai_e530_48t4x_p_phy_init(p_glb_card);
    p_glb_card->platform_callback = ctc_sai_e530_48t4x_p_platform_callback;

    return ret;
}
