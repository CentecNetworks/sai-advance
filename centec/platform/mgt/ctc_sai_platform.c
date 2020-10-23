/* ctc_sai include file */
#include "ctc_sai_port.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_samplepacket.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_isolation_group.h"
/* sdk include file */
#include "ctcs_api.h"
/* platform include file */
#include "ctc_sai_platform.h"
#include "ctc_board_types.h"

glb_card_t glb_card;

/******************************************************************************
 * board init
 ******************************************************************************/

int32 ctc_sai_board_init(void)
{
    FILE *fp = NULL;
    char buf[256] = "";
    int ret = 0;

    /* 1. get board type */
    fp = sal_fopen(MACHINE_FILE, "r");
    if (fp == NULL)
    {
        CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "open file fail\n");
        return -1;
    }

    while (sal_fgets(buf, 128, fp))
    {
        if (!sal_strncmp(buf, "onie_platform=", strlen("onie_platform=")))
        {
            break;
        }
    }

    sal_memset(&glb_card, 0, sizeof(glb_card));
    CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "board init 0\n");

    /* 2. init board */
    if (!sal_strncmp(buf, "onie_platform=arm64-centec_e550_24t16y-r0",
                     strlen("onie_platform=arm64-centec_e550_24t16y-r0")))
    {
        ret += ctc_sai_e550_24t16y_board_init(&glb_card);
        CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "board init 1\n");
    }
    else if (!sal_strncmp(buf, "onie_platform=arm64-centec_e530_48t4x_p-r0",
                     strlen("onie_platform=arm64-centec_e530_48t4x_p-r0")))
    {
        ret += ctc_sai_e530_48t4x_p_board_init(&glb_card);
        CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "board init 2\n");
    }
    else if (!sal_strncmp(buf, "onie_platform=arm64-centec_e530_24x2c-r0",
                     strlen("onie_platform=arm64-centec_e530_24x2c-r0")))
    {
        ret += ctc_sai_e530_24x2c_board_init(&glb_card);
        CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "board init 3\n");
    }
    else if (!sal_strncmp(buf, "onie_platform=arm64-centec_e530_48s4x-r0",
                     strlen("onie_platform=arm64-centec_e530_48s4x-r0")))
    {
        ret += ctc_sai_e530_48s4x_board_init(&glb_card);
        CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "board init 4\n");
    }
    else
    {
        return -1;
    }

    return ret;
}

/******************************************************************************
 * fiber timer
 ******************************************************************************/

void
_ctc_sai_fiber_get_present(int32 idx, int32 *update_info)
{
    uint32 status = 0;
    *update_info = 0;
    fiber_info_t *fiber_info = NULL;

    if (idx < 0 || idx >= glb_card.fiber_num)
    {
        return;
    }

    fiber_info = &(glb_card.fiber_info_table[idx]);
    
    fiber_info->fiber_hdl->fiber_present(fiber_info->fiber_hdl, &status);
    if (status)
    {
        switch(fiber_info->present)
        {
            case FIBER_ABSENT:
                fiber_info->present = FIBER_INIT1;
                break;
            case FIBER_INIT1:
                fiber_info->present = FIBER_INIT2;
                break;
            case FIBER_INIT2:
                fiber_info->present = FIBER_PRESENT;
                *update_info = 1;
                break;
            case FIBER_PRESENT:
                fiber_info->present = FIBER_PRESENT;
                break;
            default:
                fiber_info->present = FIBER_ABSENT;
                break;                
        }
    }
    else
    {
        switch (fiber_info->present)
        {
            case FIBER_ABSENT:
            case FIBER_INIT1:
            case FIBER_INIT2:
                fiber_info->present = FIBER_ABSENT;
                break;
            case FIBER_PRESENT:
                fiber_info->present = FIBER_ABSENT;
                *update_info = 1;
                break;
            default:
                fiber_info->present = FIBER_ABSENT;
                break;
        }
    }
}

void
_ctc_sai_fiber_polling_thread(void *data)
{
    int idx = 0;
    int fiber_eeprom_fd = -1;
    int fiber_presence_fd = -1;
    int32 update_info = 0;
    uint8 buf[256] = {0};
    uint32 len = 0;
    char sysfs_path[64] = "";
    fiber_info_t *fiber_info = NULL;

    for (;;)
    {
        if (glb_card.fiber_num <= 0)
        {
            sleep(1);
            continue;
        }

        for (idx = 0; idx < glb_card.fiber_num; idx++)
        {
            fiber_info = &(glb_card.fiber_info_table[idx]);
            
            _ctc_sai_fiber_get_present(idx, &update_info);
            if (update_info)
            {
                if (fiber_info->present == FIBER_PRESENT)
                {
                    strncpy(sysfs_path, fiber_info->sysfs_path, 64);
                    strcat(sysfs_path, "sfp_eeprom");

                    fiber_eeprom_fd = open(sysfs_path, O_RDWR);
                    if (fiber_eeprom_fd == -1)
                    {
                        continue;
                    }
                    memset(buf, 0, sizeof(buf));
                    write(fiber_eeprom_fd, buf, sizeof(buf));
                    close(fiber_eeprom_fd);
                    fiber_eeprom_fd = -1;
                    
                    len = sizeof(buf);
                    fiber_info->fiber_hdl->fiber_get_info(fiber_info->fiber_hdl, buf, len);
                    fiber_eeprom_fd = open(sysfs_path, O_RDWR);
                    if (fiber_eeprom_fd == -1)
                    {
                        continue;
                    }
                    write(fiber_eeprom_fd, buf, len);
                    close(fiber_eeprom_fd);
                    fiber_eeprom_fd = -1;
                }

                if (fiber_info->sync_fiber_present)
                {
                    strncpy(sysfs_path, fiber_info->sysfs_path, 64);
                    strcat(sysfs_path, "sfp_presence");

                    fiber_presence_fd = open(sysfs_path, O_RDWR);
                    if (fiber_presence_fd == -1)
                    {
                        continue;
                    }
                    if (fiber_info->present == FIBER_PRESENT)
                    {
                        write(fiber_presence_fd, "1", strlen("1"));
                    }
                    else
                    {
                        write(fiber_presence_fd, "0", strlen("0"));
                    }
                    close(fiber_presence_fd);
                    fiber_presence_fd = -1;
                }

                if (fiber_info->present == FIBER_PRESENT)
                {
                    fiber_info->fiber_hdl->fiber_enable(fiber_info->fiber_hdl, 1);
                }
                else
                {
                    fiber_info->fiber_hdl->fiber_enable(fiber_info->fiber_hdl, 0);
                }
            }
        }
        sleep(1);
    }
}

/******************************************************************************
 * macled timer
 ******************************************************************************/
void
_ctc_sai_macled_polling_thread(void *data)
{
    int i = 0, j = 0;
    macled_info_t *macled_info = NULL;

    while (1)
    {
        if (glb_card.macled_info == NULL)
        {
            sleep(1);
            continue;
        }

        macled_info = glb_card.macled_info;

        for (i = 0; i < macled_info->led2mac_size; i++)
        {
            int brightness = 0;
            FILE *fp = NULL;
            int tableid = 0;
            mac_led_api_para_t para;
            mac_led_info_t *p_mac_led_info = NULL;

            if (macled_info->led2mac[i].sysfs == NULL)
                continue;

            fp = sal_fopen(macled_info->led2mac[i].sysfs, "r");
            if (fp == NULL)
            {
                continue;
            }
            fscanf(fp, "%d", &brightness);
            sal_fclose(fp);
            
            tableid = macled_info->macled_hdl->macled_gen.mac_table_id;
            p_mac_led_info = macled_info->macled_hdl->macled_gen.p_mac_led_info;
            for (j = 0; j < p_mac_led_info->mac_num; j++)
            {
                if (macled_info->led2mac[i].para.port_id == p_mac_led_info->mac_led_api_para[tableid][j].port_id
                 && macled_info->led2mac[i].para.lchip == p_mac_led_info->mac_led_api_para[tableid][j].lchip
                 && macled_info->led2mac[i].para.ctl_id == p_mac_led_info->mac_led_api_para[tableid][j].ctl_id)
                {
                    para = p_mac_led_info->mac_led_api_para[tableid][j];
                    break;
                }
            }
            if (brightness != para.mode)
            {
                para.mode = brightness;
                macled_info->macled_hdl->update_table_info(macled_info->macled_hdl, &para);
            }
        }
        sleep(1);
    }
}

/******************************************************************************
 * platform callback thread
 ******************************************************************************/
void
_ctc_sai_platform_callback_task(void *data)
{
    while (1)
    {
        if (glb_card.platform_callback != NULL)
        {
            glb_card.platform_callback();
        }
        sleep(1);
    }
}

/******************************************************************************
 * sai db init and deinit
 ******************************************************************************/

sai_status_t ctc_sai_platform_db_init(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    if (lchip == 0)
    {
        i2c_handle_module_init();
        fiber_handle_module_init();
        macled_handle_module_init();

        ctc_sai_board_init();

        /*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/
        CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }
        sal_task_create(&p_switch_master->fiber_polling_task, "saiFiberPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_fiber_polling_thread, (void*)(uintptr)lchip);    
        sal_task_create(&p_switch_master->macled_polling_task, "saiMacledPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_macled_polling_thread, (void*)(uintptr)lchip);    
        sal_task_create(&p_switch_master->platform_callback_task, "saiPlatformCallbackThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_platform_callback_task, (void*)(uintptr)lchip);    
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_platform_db_deinit(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    if (lchip == 0)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }
        sal_task_destroy(p_switch_master->macled_polling_task);
        sal_task_destroy(p_switch_master->fiber_polling_task);
        sal_task_destroy(p_switch_master->platform_callback_task);

        macled_handle_module_exit();
        fiber_handle_module_exit();
        i2c_handle_module_exit();
    }

    return SAI_STATUS_SUCCESS;
}

/*SYSTEM MODIFIED by yoush for warm-reboot in 2020-08-12*/
sai_status_t ctc_sai_platform_db_run(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;

    if (lchip == 0)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        if (NULL == p_switch_master)
        {
            return SAI_STATUS_FAILURE;
        }
        
        p_switch_master->fiber_polling_task = NULL;
        sal_task_create(&p_switch_master->fiber_polling_task, "saiFiberPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_fiber_polling_thread, (void*)(uintptr)lchip);    

        p_switch_master->macled_polling_task = NULL;
        sal_task_create(&p_switch_master->macled_polling_task, "saiMacledPollingThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_macled_polling_thread, (void*)(uintptr)lchip);
        
        p_switch_master->platform_callback_task = NULL;
        sal_task_create(&p_switch_master->platform_callback_task, "saiPlatformCallbackThread", SAL_DEF_TASK_STACK_SIZE, 0,
                        _ctc_sai_platform_callback_task, (void*)(uintptr)lchip);    
    }

    return SAI_STATUS_SUCCESS;
}

