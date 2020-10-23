#include "macled_handle.h"
#include "sal.h"
#include "ctc_sai.h"

int32 _macled_set_mode(mac_led_api_para_t *port_led)
{
    int32 ret = 0;
    ctc_chip_led_para_t led_para;
    ctc_chip_mac_led_type_t led_type = CTC_CHIP_USING_ONE_LED;

    led_para.ctl_id = port_led->ctl_id;
#ifdef TSINGMA
    led_para.lport_en = 0;
#endif
    led_para.lchip = port_led->lchip;
    led_para.op_flag = CTC_CHIP_LED_MODE_SET_OP;
    led_para.port_id = port_led->port_id;
    if(port_led->mode == LED_MODE_2_RXLNK_BIACT)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_RXLINK_MODE;
        led_para.sec_mode = CTC_CHIP_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_1_RXLNK_BIACT)
    {
        led_type = CTC_CHIP_USING_ONE_LED;
        led_para.first_mode = CTC_CHIP_RXLINK_BIACTIVITY_MODE;
    }     
    else if (port_led->mode == LED_MODE_2_OFF_RXLNKBIACT)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
        led_para.sec_mode = CTC_CHIP_RXLINK_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_2_RXLNKBIACT_OFF)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_RXLINK_BIACTIVITY_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    else if(port_led->mode == LED_MODE_2_FORCE_OFF)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    else if(port_led->mode == LED_MODE_1_FORCE_ON)
    {
        led_type = CTC_CHIP_USING_ONE_LED;
        led_para.first_mode = CTC_CHIP_FORCE_ON_MODE;
    }
    else if(port_led->mode == LED_MODE_1_FORCE_OFF)
    {
        led_type = CTC_CHIP_USING_ONE_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    else if(port_led->mode == LED_MODE_2_OFF_BIACT)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
        led_para.sec_mode = CTC_CHIP_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_2_BIACT_OFF)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_BIACTIVITY_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    else if(port_led->mode == LED_MODE_1_BIACT)
    {
        led_type = CTC_CHIP_USING_ONE_LED;
        led_para.first_mode = CTC_CHIP_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_2_OFF_ON)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_ON_MODE;
    }
    else if(port_led->mode == LED_MODE_2_ON_OFF)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_ON_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    else if(port_led->mode == LED_MODE_2_TXLNK_RXLNKBIACT)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_RXLINK_BIACTIVITY_MODE;
        led_para.sec_mode = CTC_CHIP_TXLINK_MODE;
    }
    else if(port_led->mode == LED_MODE_2_TXLNK_BIACT)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_BIACTIVITY_MODE;
        led_para.sec_mode = CTC_CHIP_TXLINK_MODE;
    }
    else if(port_led->mode == LED_MODE_2_TXLNK_OFF)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_FORCE_OFF_MODE;
        led_para.sec_mode = CTC_CHIP_TXLINK_MODE;
    }
    else if(port_led->mode == LED_MODE_2_RXLNKBIACT_TXLNK)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_TXLINK_MODE;
        led_para.sec_mode = CTC_CHIP_RXLINK_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_2_BIACT_TXLNK)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_TXLINK_MODE;
        led_para.sec_mode = CTC_CHIP_BIACTIVITY_MODE;
    }
    else if(port_led->mode == LED_MODE_2_OFF_TXLNK)
    {
        led_type = CTC_CHIP_USING_TWO_LED;
        led_para.first_mode = CTC_CHIP_TXLINK_MODE;
        led_para.sec_mode = CTC_CHIP_FORCE_OFF_MODE;
    }
    ret = ctcs_chip_set_mac_led_mode(led_para.lchip, &led_para, led_type);    
    return ret;
}

int32 _macled_choose_one_table(macled_handle_t *p_macled_hdl, int32 table_idx)
{
    mac_led_api_para_t *pp_mac_led_api_para;
    uint16 mac_idx = 0;
    uint8 lchip_idx, ctlid_idx;
    ctc_chip_mac_led_mapping_t led_map[2][2];
    uint8 idx = 0;

    sal_memset(&led_map, 0, sizeof(ctc_chip_mac_led_mapping_t) * 2 * 2);

    if (!p_macled_hdl || !p_macled_hdl->macled_gen.p_mac_led_info)
    {
        return -1;
    }

    pp_mac_led_api_para = p_macled_hdl->macled_gen.p_mac_led_info->mac_led_api_para[table_idx];
    for (mac_idx = 0; mac_idx < p_macled_hdl->macled_gen.p_mac_led_info->mac_num; mac_idx++)
    {
        if (pp_mac_led_api_para[mac_idx].lchip > 1 || pp_mac_led_api_para[mac_idx].ctl_id > 1)
            continue;
        led_map[pp_mac_led_api_para[mac_idx].lchip][pp_mac_led_api_para[mac_idx].ctl_id].mac_led_num++;
    }
    for (lchip_idx = 0; lchip_idx < 2; lchip_idx++)
    {
        for (ctlid_idx = 0; ctlid_idx < 2; ctlid_idx++)
        {
            led_map[lchip_idx][ctlid_idx].lchip = lchip_idx;
            led_map[lchip_idx][ctlid_idx].ctl_id = ctlid_idx;
            led_map[lchip_idx][ctlid_idx].p_mac_id = mem_malloc(MEM_SYSTEM_MODULE, sizeof(uint8) * led_map[lchip_idx][ctlid_idx].mac_led_num);
            led_map[lchip_idx][ctlid_idx].mac_led_num = 0;
        }
    }
    for (mac_idx = 0; mac_idx < p_macled_hdl->macled_gen.p_mac_led_info->mac_num; mac_idx++)
    {
        _macled_set_mode(&pp_mac_led_api_para[mac_idx]);
        if (pp_mac_led_api_para[mac_idx].lchip > 1 || pp_mac_led_api_para[mac_idx].ctl_id > 1)
            continue;
        idx = led_map[pp_mac_led_api_para[mac_idx].lchip][pp_mac_led_api_para[mac_idx].ctl_id].mac_led_num;
        led_map[pp_mac_led_api_para[mac_idx].lchip][pp_mac_led_api_para[mac_idx].ctl_id].mac_led_num++;
        led_map[pp_mac_led_api_para[mac_idx].lchip][pp_mac_led_api_para[mac_idx].ctl_id].p_mac_id[idx] = pp_mac_led_api_para[mac_idx].port_id;
    }
    for (lchip_idx = 0; lchip_idx < 2; lchip_idx++)
    {
        for (ctlid_idx = 0; ctlid_idx < 2; ctlid_idx++)
        {
            ctcs_chip_set_mac_led_mapping(lchip_idx, &led_map[lchip_idx][ctlid_idx]);
            mem_free(led_map[lchip_idx][ctlid_idx].p_mac_id);
        }
    }
    
    return 0;
}

int32 _macled_set_polarity(uint8 lchip, uint8 polarity)
{
    ctc_chip_led_para_t led_para;

    /* set mac led polarity */
    led_para.lchip = lchip;
    led_para.ctl_id = 0;
#ifdef TSINGMA     
    led_para.lport_en = 0;
#endif
    led_para.op_flag = CTC_CHIP_LED_POLARITY_SET_OP;
    led_para.polarity = polarity;
    ctcs_chip_set_mac_led_mode(led_para.lchip, &led_para, CTC_CHIP_USING_ONE_LED);//One led or two led here both ok, it not use
#ifndef TSINGMA     
    led_para.ctl_id = 1;   
    ctcs_chip_set_mac_led_mode(led_para.lchip, &led_para, CTC_CHIP_USING_ONE_LED);//One led or two led here both ok, it not use
#endif

    return 0;
}

int32 _macled_set_enable(uint8 lchip, uint8 enable)
{
    //ctcs_chip_set_property(lchip, CTC_CHIP_MAC_LED_EN, (uint32*)&enable);
    ctcs_chip_set_mac_led_en(lchip, enable);
    return 0;
}

int32 macled_init(macled_handle_t *p_macled_hdl)
{
    uint8 lchip_init[2] = {0, 0};
    uint8 mac_idx = 0;
    uint8 idx = 0;
    mac_led_api_para_t *pp_mac_led_api_para;

    if (!p_macled_hdl || !p_macled_hdl->macled_gen.p_mac_led_info)
    {
        return -1;
    }

    pp_mac_led_api_para = p_macled_hdl->macled_gen.p_mac_led_info->mac_led_api_para[0];
    for (mac_idx = 0; mac_idx < p_macled_hdl->macled_gen.p_mac_led_info->mac_num; mac_idx++)
    {
        if (pp_mac_led_api_para[mac_idx].lchip == 0)
        {
            lchip_init[0] = 1;
        }
        else if (pp_mac_led_api_para[mac_idx].lchip == 1)
        {
            lchip_init[1] = 1;
        }
    }

    /* 1. choose table 0 */
    _macled_choose_one_table(p_macled_hdl, 0);

    /* 2. set polarity */
    for (idx = 0; idx < sizeof(lchip_init); idx++)
    {
        if (lchip_init[idx])
        {
            _macled_set_polarity(idx, p_macled_hdl->macled_gen.p_mac_led_info->polarity);
        }
    }

    /* 3. set enable */
    for (idx = 0; idx < sizeof(lchip_init); idx++)
    {
        if (lchip_init[idx])
        {
            _macled_set_enable(idx, 1);
        }
    }
    
    return 0;
}

int32 macled_update_table_info(macled_handle_t *p_macled_hdl, mac_led_api_para_t *port_led)
{
    int32 ret = 0;
    uint8 table_idx, mac_idx;
    mac_led_api_para_t *pp_mac_led_api_para;

    if (!p_macled_hdl || !p_macled_hdl->macled_gen.p_mac_led_info)
    {
        return -1;
    }

    ret = _macled_set_mode(port_led);
    if (ret)
    {
        return -1;
    }

    for(table_idx = 0; table_idx < p_macled_hdl->macled_gen.p_mac_led_info->table_num; table_idx++)
    {
        pp_mac_led_api_para = p_macled_hdl->macled_gen.p_mac_led_info->mac_led_api_para[table_idx];
        for (mac_idx = 0; mac_idx < p_macled_hdl->macled_gen.p_mac_led_info->mac_num; mac_idx++)
        {
            if ((pp_mac_led_api_para[mac_idx].port_id == port_led->port_id)
             && (pp_mac_led_api_para[mac_idx].lchip == port_led->lchip)
             && (pp_mac_led_api_para[mac_idx].ctl_id == port_led->ctl_id))
            {
                pp_mac_led_api_para[mac_idx].mode = port_led->mode;
                break;
            }
        }
    }
    
    return 0;
}

int32 macled_choose_next_table(macled_handle_t *p_macled_hdl)
{
    int32 ret = 0;

    mac_led_api_para_t *p_mac_led_api_para = NULL;

    if (!p_macled_hdl || !p_macled_hdl->macled_gen.p_mac_led_info)
    {
        return -1;
    }

    p_macled_hdl->macled_gen.mac_table_id++;
    p_macled_hdl->macled_gen.mac_table_id %= p_macled_hdl->macled_gen.p_mac_led_info->table_num;
    p_mac_led_api_para = p_macled_hdl->macled_gen.p_mac_led_info->mac_led_api_para[p_macled_hdl->macled_gen.mac_table_id];
    if (p_mac_led_api_para == NULL)
    {
        return -1;
    }

    ret = _macled_choose_one_table(p_macled_hdl, p_macled_hdl->macled_gen.mac_table_id);

    return ret;
}

macled_handle_t *macled_create_handle(macled_gen_t *macled_pgen)
{
    uint8 table_idx = 0;
    uint8 idx = 0;
    uint8 table_num = 0;
    uint8 mac_num = 0;
    mac_led_api_para_t **mac_led_api_para = NULL;
    macled_handle_t *p_macled_hdl;

    /* 1. basic check */
    if (!macled_pgen || !macled_pgen->p_mac_led_info)
    {
        return NULL;
    }

    /* 2. get memory size and basic check */
    table_num = macled_pgen->p_mac_led_info->table_num;
    mac_num = macled_pgen->p_mac_led_info->mac_num;
    if (table_num == 0)
    {
        return NULL;
    }

    /* 3. alloc memory for macled_handle and init */
    p_macled_hdl = (macled_handle_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(macled_handle_t));
    if (!p_macled_hdl)
    {
        return NULL;
    }
    sal_memset(p_macled_hdl, 0, sizeof(macled_handle_t));

    p_macled_hdl->macled_gen.mac_table_id = 0;

    /* 4. alloc memory for p_mac_led_info and init */
    p_macled_hdl->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
    if (!p_macled_hdl->macled_gen.p_mac_led_info)
    {
        mem_free(p_macled_hdl);
        return NULL;
    }
    sal_memset(p_macled_hdl->macled_gen.p_mac_led_info, 0, sizeof(mac_led_info_t));

    p_macled_hdl->macled_gen.p_mac_led_info->polarity = macled_pgen->p_mac_led_info->polarity;
    p_macled_hdl->macled_gen.p_mac_led_info->mac_num = macled_pgen->p_mac_led_info->mac_num;
    p_macled_hdl->macled_gen.p_mac_led_info->table_num = macled_pgen->p_mac_led_info->table_num;
    p_macled_hdl->macled_gen.p_mac_led_info->slice0_mac_num = macled_pgen->p_mac_led_info->slice0_mac_num;

    /* 5. alloc memory for mac_led_api_para */
    mac_led_api_para = (mac_led_api_para_t **)mem_malloc(MEM_SYSTEM_MODULE, sizeof(mac_led_api_para_t *) * table_num);
    if (!mac_led_api_para)
    {
        mem_free(p_macled_hdl->macled_gen.p_mac_led_info);
        mem_free(p_macled_hdl);
        return NULL;
    }

    /* 6. alloc memory for table and init */
    for (table_idx = 0; table_idx < table_num; table_idx++)
    {
        mac_led_api_para[table_idx] = (mac_led_api_para_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(mac_led_api_para_t) * mac_num);
        if (!mac_led_api_para[table_idx])
        {
            for (idx = 0; idx < table_idx; idx++)
            {
                mem_free(mac_led_api_para[idx]);
            }
            mem_free(mac_led_api_para);
            mem_free(p_macled_hdl->macled_gen.p_mac_led_info);
            mem_free(p_macled_hdl);
            return NULL;
        }

        sal_memcpy(mac_led_api_para[table_idx], macled_pgen->p_mac_led_info->mac_led_api_para[table_idx], sizeof(mac_led_api_para_t) * mac_num);
    }

    p_macled_hdl->macled_gen.p_mac_led_info->mac_led_api_para = mac_led_api_para;

    p_macled_hdl->init = macled_init;
    p_macled_hdl->update_table_info = macled_update_table_info;
    p_macled_hdl->choose_next_table = macled_choose_next_table;
    
    return p_macled_hdl;
}

int32 macled_handle_module_init(void)
{
    return 0;
}

int32 macled_handle_module_exit(void)
{
    return 0;
}

