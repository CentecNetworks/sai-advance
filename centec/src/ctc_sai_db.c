#include "ctc_sai_db.h"
#include "ctc_sai_oid.h"

ctc_sai_db_t* g_sai_db[CTC_SAI_MAX_CHIP_NUM] = {NULL};
ctc_sai_master_t g_ctc_sai_master = {0, NULL};

#define SAI_DB_INIT_CHECK()            \
    do                                   \
    {                                    \
        if(lchip>=CTC_SAI_MAX_CHIP_NUM){\
            return SAI_STATUS_INVALID_PARAMETER;} \
        if (NULL == g_sai_db[lchip]){      \
            return SAI_STATUS_UNINITIALIZED; }     \
    }                                    \
    while (0)

extern sai_status_t ctc_sai_bridge_get_fid(sai_object_id_t bv_id, uint16 *fid);
static uint32
_ctc_sai_db_oid_hash_make(void* p_oid_property)
{
    return ctc_hash_caculate(sizeof(sai_object_id_t), &(((ctc_sai_oid_property_t*)p_oid_property)->oid));
}
static bool
_ctc_sai_db_oid_hash_cmp(void* p_data0, void* p_data1)
{
    if (((ctc_sai_oid_property_t*)p_data0)->oid == ((ctc_sai_oid_property_t*)p_data1)->oid)
    {
        return TRUE;
    }
    return FALSE;
}

static uint32
_ctc_sai_db_entry_hash_make(void* p_entry_property)
{
    uint32 length = 0;
    length = CTC_OFFSET_OF(ctc_sai_entry_property_t, calc_key_len);
    return ctc_hash_caculate(length, (uint8*)p_entry_property);
}
static bool
_ctc_sai_db_entry_hash_cmp(void* p_data0, void* p_data1)
{
    uint32 length = 0;
    length = CTC_OFFSET_OF(ctc_sai_entry_property_t, calc_key_len);
    if (0 == sal_memcmp(p_data0, p_data1, length))
    {
        return TRUE;
    }
    return FALSE;
}
static sai_status_t
_ctc_sai_db_entry_mapping_key(ctc_sai_db_entry_type_t type, void* key, ctc_sai_entry_property_t* entry_property)
{
    ctc_object_id_t ctc_object_id;

    entry_property->entry_type = type;
    if (CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR == type)
    {
        sai_neighbor_entry_t* neighbor_entry = (sai_neighbor_entry_t*)key;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, neighbor_entry->rif_id, &ctc_object_id);
        entry_property->key.neighbor.l3if_id = ctc_object_id.value;
        entry_property->key.neighbor.sai_rif_type = ctc_object_id.sub_type;
        entry_property->key.neighbor.ip_ver = neighbor_entry->ip_address.addr_family;
        if (SAI_IP_ADDR_FAMILY_IPV4 == neighbor_entry->ip_address.addr_family)
        {
            sal_memcpy(&(entry_property->key.neighbor.addr.ip4), &(neighbor_entry->ip_address.addr.ip4), sizeof(sai_ip4_t));
        }
        else
        {
            sal_memcpy(&(entry_property->key.neighbor.addr.ip6), &(neighbor_entry->ip_address.addr.ip6), sizeof(sai_ip6_t));
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ROUTE == type)
    {
        sai_route_entry_t* route_entry = (sai_route_entry_t*)key;
        ipv6_addr_t mask;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, route_entry->vr_id, &ctc_object_id);
        entry_property->key.route.vrf_id = ctc_object_id.value;
        entry_property->key.route.ip_ver = route_entry->destination.addr_family;
        sal_memcpy(mask, &(route_entry->destination.mask), sizeof(ipv6_addr_t));
        CTC_SAI_NTOH_V6(mask);
        if (SAI_IP_ADDR_FAMILY_IPV4 == route_entry->destination.addr_family)
        {
            sal_memcpy(&(entry_property->key.route.addr.ip4), &(route_entry->destination.addr.ip4), sizeof(sai_ip4_t));
            IPV4_MASK_TO_LEN(mask[0], entry_property->key.route.mask_len);
        }
        else
        {
            sal_memcpy(&(entry_property->key.route.addr.ip6), &(route_entry->destination.addr.ip6), sizeof(sai_ip6_t));
            IPV6_MASK_TO_LEN(mask, entry_property->key.route.mask_len);
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC == type)
    {
        sai_object_type_t oid_type = SAI_OBJECT_TYPE_NULL;
        sai_l2mc_entry_t* l2mc_entry = (sai_l2mc_entry_t*)key;
        oid_type = sai_object_type_query(l2mc_entry->bv_id);
        CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(l2mc_entry->bv_id, &entry_property->key.mcast_ip.vrf_id));
        entry_property->key.mcast_ip.is_bridge = (SAI_OBJECT_TYPE_BRIDGE == oid_type)?1:0;
        entry_property->key.mcast_ip.is_l2mc = 1;
        entry_property->key.mcast_ip.ip_ver = l2mc_entry->destination.addr_family;
        if (entry_property->key.mcast_ip.ip_ver == SAI_IP_ADDR_FAMILY_IPV4)
        {
            entry_property->key.mcast_ip.src_mask_len = (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG) ? 32 : 0;
            sal_memcpy(&(entry_property->key.mcast_ip.dst), &(l2mc_entry->destination.addr), sizeof(sai_ip4_t));
            if (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(entry_property->key.mcast_ip.src), &(l2mc_entry->source.addr), sizeof(sai_ip4_t));
            }
        }
        else
        {
            entry_property->key.mcast_ip.src_mask_len = (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG) ? 128 : 0;
            sal_memcpy(&(entry_property->key.mcast_ip.dst), &(l2mc_entry->destination.addr), sizeof(sai_ip6_t));
            if (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(entry_property->key.mcast_ip.src), &(l2mc_entry->source.addr), sizeof(sai_ip6_t));
            }
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC == type)
    {
        sai_ipmc_entry_t* ipmc_entry = (sai_ipmc_entry_t*)key;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, ipmc_entry->vr_id, &ctc_object_id);
        entry_property->key.mcast_ip.vrf_id = ctc_object_id.value;
        entry_property->key.mcast_ip.is_l2mc = 0;
        entry_property->key.mcast_ip.ip_ver = ipmc_entry->destination.addr_family;
        if (entry_property->key.mcast_ip.ip_ver == SAI_IP_ADDR_FAMILY_IPV4)
        {
            entry_property->key.mcast_ip.src_mask_len = (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG) ? 32 : 0;
            sal_memcpy(&(entry_property->key.mcast_ip.dst), &(ipmc_entry->destination.addr), sizeof(sai_ip4_t));
            if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(entry_property->key.mcast_ip.src), &(ipmc_entry->source.addr), sizeof(sai_ip4_t));
            }
        }
        else
        {
            entry_property->key.mcast_ip.src_mask_len = (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG) ? 128 : 0;
            sal_memcpy(&(entry_property->key.mcast_ip.dst), &(ipmc_entry->destination.addr), sizeof(sai_ip6_t));
            if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(entry_property->key.mcast_ip.src), &(ipmc_entry->source.addr), sizeof(sai_ip6_t));
            }
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB == type)
    {
       sai_object_type_t oid_type = SAI_OBJECT_TYPE_NULL;
        sai_mcast_fdb_entry_t* mcast_fdb_entry = (sai_mcast_fdb_entry_t*)key;
        oid_type = sai_object_type_query(mcast_fdb_entry->bv_id);
        CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(mcast_fdb_entry->bv_id, &entry_property->key.mcast_fdb.fid));
        entry_property->key.mcast_fdb.is_bridge = (SAI_OBJECT_TYPE_BRIDGE == oid_type)?1:0;
        sal_memcpy(&(entry_property->key.mcast_fdb.mac), &(mcast_fdb_entry->mac_address), sizeof(mac_addr_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL == type)
    {
        sal_memcpy(&(entry_property->key.hardware_id), key, sizeof(uint64));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS == type)
    {
        sal_memcpy(&(entry_property->key.oid), key, sizeof(sai_object_id_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS == type)
    {
        sal_memcpy(&(entry_property->key.oid), key, sizeof(sai_object_id_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MPLS == type)
    {
        sai_inseg_entry_t* mpls_entry = (sai_inseg_entry_t*)key;
        entry_property->key.mpls.label = mpls_entry->label;
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_NAT == type)
    {
        sai_nat_entry_t* nat_entry = (sai_nat_entry_t*)key;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, nat_entry->vr_id, &ctc_object_id);
        entry_property->key.nat.vrf_id = ctc_object_id.value;
        entry_property->key.nat.ip_ver = CTC_IP_VER_4;
        sal_memcpy(&(entry_property->key.nat.src_ip), &(nat_entry->data.key.src_ip), sizeof(sai_ip4_t));
        sal_memcpy(&(entry_property->key.nat.dst_ip), &(nat_entry->data.key.dst_ip), sizeof(sai_ip4_t));
        entry_property->key.nat.proto = nat_entry->data.key.proto;
        entry_property->key.nat.l4_src_port = nat_entry->data.key.l4_src_port;
        entry_property->key.nat.l4_dst_port = nat_entry->data.key.l4_dst_port;
        entry_property->key.nat.nat_type = nat_entry->nat_type;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_entry_unmapping_key(uint8 lchip, ctc_sai_db_entry_type_t type, ctc_sai_entry_property_t* entry_property, void* key)
{
    uint8 gchip = 0;

	ctcs_get_gchip_id(lchip, &gchip);
    if (CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR == type)
    {
        sai_neighbor_entry_t* neighbor_entry = (sai_neighbor_entry_t*)key;
        neighbor_entry->switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        neighbor_entry->rif_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip,
                                                    entry_property->key.neighbor.sai_rif_type, 0, entry_property->key.neighbor.l3if_id);
        neighbor_entry->ip_address.addr_family = entry_property->key.neighbor.ip_ver;
        if (SAI_IP_ADDR_FAMILY_IPV4 == neighbor_entry->ip_address.addr_family)
        {
            sal_memcpy(&(neighbor_entry->ip_address.addr.ip4), &(entry_property->key.neighbor.addr.ip4), sizeof(sai_ip4_t));
        }
        else
        {
            sal_memcpy(&(neighbor_entry->ip_address.addr.ip6), &(entry_property->key.neighbor.addr.ip6), sizeof(sai_ip6_t));
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ROUTE == type)
    {
        sai_route_entry_t* route_entry = (sai_route_entry_t*)key;
        ipv6_addr_t mask;
        route_entry->switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        route_entry->vr_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, entry_property->key.route.vrf_id);
        route_entry->destination.addr_family = entry_property->key.route.ip_ver;
        if (SAI_IP_ADDR_FAMILY_IPV4 == route_entry->destination.addr_family)
        {
            sal_memcpy(&(route_entry->destination.addr.ip4), &(entry_property->key.route.addr.ip4), sizeof(sai_ip4_t));
            IPV4_LEN_TO_MASK(mask[0], entry_property->key.route.mask_len);
        }
        else
        {
            sal_memcpy(&(route_entry->destination.addr.ip6), &(entry_property->key.route.addr.ip6), sizeof(sai_ip6_t));
            IPV6_LEN_TO_MASK(mask, entry_property->key.route.mask_len)
        }
        CTC_SAI_HTON_V6(mask);
        sal_memcpy(&(route_entry->destination.mask), mask, sizeof(ipv6_addr_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC == type)
    {
        sai_object_type_t oid_type = SAI_OBJECT_TYPE_NULL;
        sai_l2mc_entry_t* l2mc_entry = (sai_l2mc_entry_t*)key;
        l2mc_entry->switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        oid_type = entry_property->key.mcast_ip.is_bridge? SAI_OBJECT_TYPE_BRIDGE : SAI_OBJECT_TYPE_VLAN;
        l2mc_entry->bv_id = ctc_sai_create_object_id(oid_type, lchip, 0, 0, entry_property->key.mcast_ip.vrf_id);
        l2mc_entry->type = ((entry_property->key.mcast_ip.src_mask_len == 32)||(entry_property->key.mcast_ip.src_mask_len == 128))?
                                               SAI_L2MC_ENTRY_TYPE_SG : SAI_L2MC_ENTRY_TYPE_XG;
        l2mc_entry->destination.addr_family = entry_property->key.mcast_ip.ip_ver;
        if (l2mc_entry->destination.addr_family == SAI_IP_ADDR_FAMILY_IPV4)
        {
           sal_memcpy(&(l2mc_entry->destination.addr), &(entry_property->key.mcast_ip.dst), sizeof(sai_ip4_t));
           if (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG)
           {
               sal_memcpy(&(l2mc_entry->source.addr), &(entry_property->key.mcast_ip.src), sizeof(sai_ip4_t));
           }
        }
        else
        {
           sal_memcpy(&(l2mc_entry->destination.addr), &(entry_property->key.mcast_ip.dst), sizeof(sai_ip6_t));
           if (l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG)
           {
               sal_memcpy(&(l2mc_entry->source.addr), &(entry_property->key.mcast_ip.src), sizeof(sai_ip6_t));
           }
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC == type)
    {
        sai_ipmc_entry_t* ipmc_entry = (sai_ipmc_entry_t*)key;

        ipmc_entry->vr_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, entry_property->key.mcast_ip.vrf_id);
        ipmc_entry->type = ((entry_property->key.mcast_ip.src_mask_len == 32)||(entry_property->key.mcast_ip.src_mask_len == 128))?
                                               SAI_L2MC_ENTRY_TYPE_SG : SAI_L2MC_ENTRY_TYPE_XG;
        ipmc_entry->destination.addr_family = entry_property->key.mcast_ip.ip_ver;
        if (entry_property->key.mcast_ip.ip_ver == SAI_IP_ADDR_FAMILY_IPV4)
        {
            sal_memcpy(&(ipmc_entry->destination.addr), &(entry_property->key.mcast_ip.dst), sizeof(sai_ip4_t));
            if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(ipmc_entry->source.addr), &(entry_property->key.mcast_ip.src), sizeof(sai_ip4_t));
            }
        }
        else
        {
            sal_memcpy(&(ipmc_entry->destination.addr), &(entry_property->key.mcast_ip.dst), sizeof(sai_ip6_t));
            if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
            {
                sal_memcpy(&(ipmc_entry->source.addr), &(entry_property->key.mcast_ip.src), sizeof(sai_ip6_t));
            }
        }
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB == type)
    {
        sai_object_type_t oid_type = SAI_OBJECT_TYPE_NULL;
        sai_mcast_fdb_entry_t* mcast_fdb_entry = (sai_mcast_fdb_entry_t*)key;
        oid_type = entry_property->key.mcast_fdb.is_bridge? SAI_OBJECT_TYPE_BRIDGE : SAI_OBJECT_TYPE_VLAN;
        mcast_fdb_entry->bv_id = ctc_sai_create_object_id(oid_type, lchip, 0, 0, entry_property->key.mcast_fdb.fid);
        sal_memcpy(&(mcast_fdb_entry->mac_address), &(entry_property->key.mcast_fdb.mac), sizeof(mac_addr_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL == type)
    {
        sal_memcpy(key, &(entry_property->key.hardware_id), sizeof(uint64));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS == type)
    {
        sal_memcpy(key, &(entry_property->key.oid), sizeof(sai_object_id_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS == type)
    {
        sal_memcpy(key, &(entry_property->key.oid), sizeof(sai_object_id_t));
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_MPLS == type)
    {
        sai_inseg_entry_t* mpls_entry = (sai_inseg_entry_t*)key;
        mpls_entry->label = entry_property->key.mpls.label;
    }
    else if (CTC_SAI_DB_ENTRY_TYPE_NAT == type)
    {
        sai_nat_entry_t* nat_entry = (sai_nat_entry_t*)key;
        nat_entry->switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        nat_entry->vr_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, entry_property->key.nat.vrf_id);

        sal_memcpy(&(nat_entry->data.key.src_ip), &(entry_property->key.nat.src_ip), sizeof(sai_ip4_t));
        sal_memcpy(&(nat_entry->data.key.dst_ip), &(entry_property->key.nat.dst_ip), sizeof(sai_ip4_t));
        nat_entry->data.key.proto = entry_property->key.nat.proto;
        nat_entry->data.key.l4_src_port = entry_property->key.nat.l4_src_port;
        nat_entry->data.key.l4_dst_port = entry_property->key.nat.l4_dst_port;

        nat_entry->data.mask.src_ip = 0xFFFFFFFF;
        nat_entry->data.mask.dst_ip = 0xFFFFFFFF;
        nat_entry->data.mask.proto = 0xFF;
        nat_entry->data.mask.l4_src_port = 0xFFFF;
        nat_entry->data.mask.l4_dst_port = 0xFFFF;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_db_init_id(uint8 lchip)
{
    uint8  chip_type = 0;
    uint32 lchip_num = 0;
    uint8 id_type;
    ctc_opf_t opf;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = { 0 };
    sal_memset(&opf, 0 , sizeof(opf));

    ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability);
    lchip_num = capability[CTC_GLOBAL_CAPABILITY_MAX_LCHIP_NUM];
    opf.pool_index = lchip;
    for (id_type = CTC_SAI_DB_ID_TYPE_COMMON; id_type < CTC_SAI_DB_ID_TYPE_MAX; id_type++)
    {
        ctc_opf_init(id_type, lchip_num);
    }

    chip_type = ctcs_get_chip_type(lchip);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_COMMON;
    ctc_opf_init_offset(&opf, 1, 0xFFFFFFFE);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_VLAN;
    ctc_opf_init_offset(&opf, 1, capability[CTC_GLOBAL_CAPABILITY_VLAN_NUM] - 2);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_VSI;
    ctc_opf_init_offset(&opf, capability[CTC_GLOBAL_CAPABILITY_VLAN_NUM], capability[CTC_GLOBAL_CAPABILITY_MAX_FID] - capability[CTC_GLOBAL_CAPABILITY_VLAN_NUM]);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_VPWS;
    ctc_opf_init_offset(&opf, 1, 4095);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_LOGIC_PORT;
    ctc_opf_init_offset(&opf, 1, capability[CTC_GLOBAL_CAPABILITY_LOGIC_PORT_NUM] - 1);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_VRF;
    ctc_opf_init_offset(&opf, 1, capability[CTC_GLOBAL_CAPABILITY_MAX_VRFID]);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_L3IF;
    ctc_opf_init_offset(&opf, MIN_CTC_L3IF_ID, capability[CTC_GLOBAL_CAPABILITY_L3IF_NUM] - 1);

    /* SDK no max_num limit check,
    when arp_id bind tunnel will write hw table,
    when arp_id bind route only write software table,
    so create arp_id no limit,temporarily limited to 65535 */
    opf.pool_type = CTC_SAI_DB_ID_TYPE_ARP;
    ctc_opf_init_offset(&opf, 1, 0xFFFF);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_NEXTHOP;
    ctc_opf_init_offset(&opf, 3, capability[CTC_GLOBAL_CAPABILITY_EXTERNAL_NEXTHOP_NUM] - 3);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_TUNNEL_ID;
    ctc_opf_init_offset(&opf, 1, capability[CTC_GLOBAL_CAPABILITY_MPLS_TUNNEL_NUM]-1);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER;
    ctc_opf_init_offset(&opf, 0, 0xFFFF);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_APS;
    ctc_opf_init_offset(&opf, 1, capability[CTC_GLOBAL_CAPABILITY_APS_GROUP_NUM]);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_POLICER;
    ctc_opf_init_offset(&opf, 1, 0xFFFF);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP;
    ctc_opf_init_offset(&opf, 0, capability[CTC_GLOBAL_CAPABILITY_MCAST_GROUP_NUM] - 1);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP;
    ctc_opf_init_offset(&opf, 4096, capability[CTC_GLOBAL_CAPABILITY_MCAST_GROUP_NUM] - 1);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_RPF_GROUP;
    ctc_opf_init_offset(&opf, 0, 512);
    opf.pool_type = CTC_SAI_DB_ID_TYPE_LAG;
    ctc_opf_init_offset(&opf, 0, capability[CTC_GLOBAL_CAPABILITY_LINKAGG_GROUP_NUM]);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_STP;
    ctc_opf_init_offset(&opf, 0, capability[CTC_GLOBAL_CAPABILITY_STP_INSTANCE_NUM]);

    /* SAI ACL Resource */
    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX;
    ctc_opf_init_offset(&opf, 1, 1024);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX;
    ctc_opf_init_offset(&opf, 1, 32 * 1024);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX;
    ctc_opf_init_offset(&opf, 1, 64 * 1024);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX;
    ctc_opf_init_offset(&opf, 1, ((CTC_CHIP_TSINGMA_MX == chip_type) ? 2048 : 1024));

    /* CTC SDK totally only support 12 tiem for port or packet length */
    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX;
    ctc_opf_init_offset(&opf, 1, 12);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX;
    ctc_opf_init_offset(&opf, 32, 63);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX;
    /* tm: ingress parellel acl0/1/2 511*3, sequential acl3 511 and global2 513, switch global3 512, total 3069
           egree parellel global0/1 512*2 and acl0 511, total 1535
           ingress + egress total 4604
       tm2: ingress acl2/3/4/5/6/7/8/9/10/11/12/13/14/15 14*2048, total 28672
            egress acl0/1/2/3 4*1024, total 4096
            ingress + egress total 32768 */
    ctc_opf_init_offset(&opf, 1, (CTC_CHIP_TSINGMA_MX == chip_type) ? 32768: 4604);

    /* SDK ACL Resource */
    opf.pool_type = CTC_SAI_DB_ID_TYPE_SDK_SCL_GROUP_ID;
    ctc_opf_init_offset(&opf, 0, 0x7FFFFFFF);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SDK_SCL_ENTRY_ID;
    ctc_opf_init_offset(&opf, 1, 0x7FFFFFFF - 1);/* rsv 1 for copy entry */

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID;
    ctc_opf_init_offset(&opf, 1, 0xFFFF0000);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID;
    ctc_opf_init_offset(&opf, 8, 0xFFFFFFFF - 8);/* rsv 8 for copy entry */

    opf.pool_type = CTC_SAI_DB_ID_TYPE_MAX_FRAME_SIZE;
    ctc_opf_init_offset(&opf, 0, CTC_FRAME_SIZE_MAX);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP;
    ctc_opf_init_offset(&opf, 1, 32-1);

	opf.pool_type = CTC_SAI_DB_ID_TYPE_VIF;
    ctc_opf_init_offset(&opf, 1, 8192);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_COUNTER;
    ctc_opf_init_offset(&opf, 1, 0xFFFFFFFE);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_IN_INDEX;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_OUT_INDEX;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_BFD;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_TWAMP;
    ctc_opf_init_offset(&opf, 0, ((CTC_CHIP_TSINGMA_MX == chip_type) ? 512 : 4));

    opf.pool_type = CTC_SAI_DB_ID_TYPE_NPM;
    ctc_opf_init_offset(&opf, 0, 4);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_Y1731_MEG;
    ctc_opf_init_offset(&opf, 1, 8192);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_Y1731_SESSION;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP;
    ctc_opf_init_offset(&opf, 1, 4096);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_ES;
    ctc_opf_init_offset(&opf, 1, 255);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_PTP;
    ctc_opf_init_offset(&opf, 1, 2);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SYNCE;
    ctc_opf_init_offset(&opf, 1, 2);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_UDF_MATCH;
    ctc_opf_init_offset(&opf, 0, (CTC_CHIP_TSINGMA_MX == chip_type) ? 511 : 16);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_UDF_ENTRY;
    ctc_opf_init_offset(&opf, 0, (CTC_CHIP_TSINGMA_MX == chip_type) ? 511*8 : 16*4);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_UDF_GROUP;
    ctc_opf_init_offset(&opf, 0, (CTC_CHIP_TSINGMA_MX == chip_type) ? 511*8: 16*4);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SDK_UDF_MAPPED_ID;
    if (CTC_CHIP_TSINGMA == chip_type)
    {
        ctc_opf_init_offset(&opf, 0, 16);
    }
    else if (CTC_CHIP_TSINGMA_MX == chip_type)
    {
        ctc_opf_init_offset(&opf, 1, 511);
    }

    opf.pool_type = CTC_SAI_DB_ID_TYPE_WRED;
    ctc_opf_init_offset(&opf, 1, 31);

    opf.pool_type = CTC_SAI_DB_ID_TYPE_SCHEDULER_GROUP;
    ctc_opf_init_offset(&opf, 0, 3072);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_db_deinit_id(uint8 lchip)
{
    uint8 id_type;
    for (id_type = CTC_SAI_DB_ID_TYPE_COMMON; id_type < CTC_SAI_DB_ID_TYPE_MAX; id_type++)
    {
        ctc_opf_free(id_type, lchip);
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_db_deinit_cb(void* bucket_data, void* user_data)
{
    ctc_sai_oid_property_t* p_object_property = bucket_data;
    ctc_sai_entry_property_t* p_entry_property = bucket_data;
    if (NULL == bucket_data)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (NULL != user_data)
    {
        uint32 hash_type = *((uint32*)user_data);
        if (0 == hash_type)
        {
            if (p_object_property->data)
            {
                mem_free(p_object_property->data);
            }
        }
        else if (1 == hash_type)
        {
            if (p_entry_property->data)
            {
                mem_free(p_entry_property->data);
            }
        }
    }
    mem_free(bucket_data);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_alloc_id(uint8 lchip, ctc_sai_db_id_type_t type, uint32 *id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_opf_t opf;
    SAI_DB_INIT_CHECK();
    sal_memset(&opf, 0 , sizeof(opf));
    opf.pool_type = type;
    opf.pool_index = lchip;
    status = ctc_opf_alloc_offset(&opf, 1, id);
    return ctc_sai_mapping_error_ctc(status);
}
sai_status_t
ctc_sai_db_free_id(uint8 lchip, ctc_sai_db_id_type_t type, uint32 id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_opf_t opf;
    SAI_DB_INIT_CHECK();
    sal_memset(&opf, 0 , sizeof(opf));
    opf.pool_type = type;
    opf.pool_index = lchip;
    status = ctc_opf_free_offset(&opf, 1, id);
    return ctc_sai_mapping_error_ctc(status);
}

sai_status_t
ctc_sai_db_opf_get_count(uint8 lchip, ctc_sai_db_id_type_t type, uint32* count)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_opf_t opf;
    uint32 forward_bound = 0;
    uint32 reverse_bound = 0;

    SAI_DB_INIT_CHECK();
    sal_memset(&opf, 0 , sizeof(opf));
    opf.pool_type = type;
    opf.pool_index = lchip;
    status = ctc_opf_get_bound(&opf, &forward_bound, &reverse_bound);
    *count = forward_bound;

    return ctc_sai_mapping_error_ctc(status);
}

sai_status_t
ctc_sai_db_alloc_id_from_position(uint8 lchip, ctc_sai_db_id_type_t type, uint32 id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_opf_t opf;
    SAI_DB_INIT_CHECK();
    sal_memset(&opf, 0 , sizeof(opf));
    opf.pool_type = type;
    opf.pool_index = lchip;
    status = ctc_opf_alloc_offset_from_position(&opf, 1, id);
    return ctc_sai_mapping_error_ctc(status);
}

sai_status_t
ctc_sai_db_lock(uint8 lchip)
{
    if((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip]))
    {
        return SAI_STATUS_UNINITIALIZED;
    }

    sal_mutex_lock(g_sai_db[lchip]->p_mutex);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_unlock(uint8 lchip)
{
    if((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip]))
    {
        return SAI_STATUS_UNINITIALIZED;
    }

    sal_mutex_unlock(g_sai_db[lchip]->p_mutex);

    return SAI_STATUS_SUCCESS;
}

bool
ctc_sai_db_check_object_property_exist(uint8 lchip, sai_object_id_t object_id)
{
    ctc_sai_oid_property_t oid_property;
    ctc_sai_oid_property_t* p_object_property = NULL;
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;

    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip]))
    {
        return NULL;
    }
    ctc_sai_oid_get_type(object_id, &type);
    if (!ctc_sai_is_object_type_valid(type))
    {
        return NULL;
    }
    sal_memset(&oid_property, 0, sizeof(ctc_sai_oid_property_t));
    oid_property.oid = object_id;
    p_object_property = ctc_hash_lookup(g_sai_db[lchip]->oid_hash[type], &oid_property);
    if (NULL == p_object_property)
    {
        return false;
    }

    return true;
}

sai_status_t
ctc_sai_db_get_db_entry_type(sai_object_type_t object_type, ctc_sai_db_entry_type_t* type)
{
    switch (object_type)
    {
        case SAI_OBJECT_TYPE_NEIGHBOR_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR;
            break;
        case SAI_OBJECT_TYPE_ROUTE_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_ROUTE;
            break;
        case SAI_OBJECT_TYPE_L2MC_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC;
            break;
        case SAI_OBJECT_TYPE_IPMC_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC;
            break;
        case SAI_OBJECT_TYPE_MCAST_FDB_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB;
            break;
        case SAI_OBJECT_TYPE_INSEG_ENTRY:
            *type = CTC_SAI_DB_ENTRY_TYPE_MPLS;
            break;
        default:
            return SAI_STATUS_INVALID_PARAMETER;
            break;
    }
    return SAI_STATUS_SUCCESS;
}

void*
ctc_sai_db_get_object_property(uint8 lchip, sai_object_id_t object_id)
{
    ctc_sai_oid_property_t oid_property;
    ctc_sai_oid_property_t* p_object_property = NULL;
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;

    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip]))
    {
        return NULL;
    }
    ctc_sai_oid_get_type(object_id, &type);
    if (!ctc_sai_is_object_type_valid(type))
    {
        return NULL;
    }
    sal_memset(&oid_property, 0, sizeof(ctc_sai_oid_property_t));
    oid_property.oid = object_id;
    p_object_property = ctc_hash_lookup(g_sai_db[lchip]->oid_hash[type], &oid_property);
    if (NULL == p_object_property)
    {
        return NULL;
    }
    return p_object_property->data;
}

bool
ctc_sai_db_check_object_exist(sai_object_id_t object_id)
{
    ctc_sai_oid_property_t oid_property;
    ctc_sai_oid_property_t* p_object_property = NULL;
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(object_id, &lchip);
    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip]))
    {
        return NULL;
    }
    ctc_sai_oid_get_type(object_id, &type);
    if (!ctc_sai_is_object_type_valid(type))
    {
        return NULL;
    }
    sal_memset(&oid_property, 0, sizeof(ctc_sai_oid_property_t));
    oid_property.oid = object_id;
    p_object_property = ctc_hash_lookup(g_sai_db[lchip]->oid_hash[type], &oid_property);
    if (NULL == p_object_property)
    {
        return false;
    }
    return true;
}


sai_status_t
ctc_sai_db_add_object_property(uint8 lchip, sai_object_id_t object_id, void* object_property)
{
    ctc_sai_oid_property_t oid_property;
    ctc_sai_oid_property_t* p_object_property = NULL;
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;

    SAI_DB_INIT_CHECK();
    ctc_sai_oid_get_type(object_id, &type);
    if (!ctc_sai_is_object_type_valid(type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&oid_property, 0, sizeof(ctc_sai_oid_property_t));
    oid_property.oid = object_id;
    p_object_property = ctc_hash_lookup(g_sai_db[lchip]->oid_hash[type], &oid_property);
    if (p_object_property)
    {
        if (NULL == p_object_property->data)
        {
            p_object_property->oid = object_id;
            p_object_property->data = object_property;
            return SAI_STATUS_SUCCESS;
        }
        else
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }
    }
    else
    {
        p_object_property = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_oid_property_t));
        if (NULL == p_object_property)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_object_property, 0, sizeof(ctc_sai_oid_property_t));
        p_object_property->oid = object_id;
        p_object_property->data = object_property;
    }
    ctc_hash_insert(g_sai_db[lchip]->oid_hash[type], p_object_property);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_remove_object_property(uint8 lchip, sai_object_id_t object_id)
{
    ctc_sai_oid_property_t oid_property;
    ctc_sai_oid_property_t* p_object_property = NULL;
    sai_object_type_t type = SAI_OBJECT_TYPE_NULL;

    SAI_DB_INIT_CHECK();
    ctc_sai_oid_get_type(object_id, &type);
    if (!ctc_sai_is_object_type_valid(type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&oid_property, 0, sizeof(ctc_sai_oid_property_t));
    oid_property.oid = object_id;
    p_object_property = ctc_hash_remove(g_sai_db[lchip]->oid_hash[type],  &oid_property);
    if (NULL == p_object_property)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    mem_free(p_object_property);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_traverse_object_property(uint8 lchip, sai_object_type_t object_type, hash_traversal_fn fn, void* data)
{
    SAI_DB_INIT_CHECK();
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_hash_traverse(g_sai_db[lchip]->oid_hash[object_type], fn, data));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_get_object_property_count(uint8 lchip, sai_object_type_t object_type, uint32* count)
{
    SAI_DB_INIT_CHECK();
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    *count = g_sai_db[lchip]->oid_hash[object_type]->count;

    return SAI_STATUS_SUCCESS;
}

void*
ctc_sai_db_entry_property_get_property(uint8 lchip, ctc_sai_db_entry_type_t type, void* key)
{
    ctc_sai_entry_property_t entry_property;
    ctc_sai_entry_property_t* p_entry_property = NULL;
    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip])
        || (type >= CTC_SAI_DB_ENTRY_TYPE_MAX))
    {
        return NULL;
    }
    sal_memset(&entry_property, 0, sizeof(ctc_sai_entry_property_t));
    _ctc_sai_db_entry_mapping_key(type, key, &entry_property);
    p_entry_property = ctc_hash_lookup(g_sai_db[lchip]->entry_hash[type], &entry_property);
    return (void*)p_entry_property;
}

void*
ctc_sai_db_entry_property_get(uint8 lchip, ctc_sai_db_entry_type_t type, void* key)
{
    ctc_sai_entry_property_t entry_property;
    ctc_sai_entry_property_t* p_entry_property = NULL;
    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip])
        || (type >= CTC_SAI_DB_ENTRY_TYPE_MAX))
    {
        return NULL;
    }
    sal_memset(&entry_property, 0, sizeof(ctc_sai_entry_property_t));
    _ctc_sai_db_entry_mapping_key(type, key, &entry_property);
    p_entry_property = ctc_hash_lookup(g_sai_db[lchip]->entry_hash[type], &entry_property);
    if (NULL == p_entry_property)
    {
        return NULL;
    }
    return p_entry_property->data;
}

sai_status_t
ctc_sai_db_entry_property_add(uint8 lchip, ctc_sai_db_entry_type_t type, void* key, void* property)
{
    ctc_sai_entry_property_t entry_property;
    ctc_sai_entry_property_t* p_entry_property = NULL;

    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_ENTRY_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    sal_memset(&entry_property, 0, sizeof(ctc_sai_entry_property_t));
    _ctc_sai_db_entry_mapping_key(type, key, &entry_property);
    p_entry_property = ctc_hash_lookup(g_sai_db[lchip]->entry_hash[type], &entry_property);
    if (p_entry_property)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    else
    {
        p_entry_property = (ctc_sai_entry_property_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_entry_property_t));
        if (NULL == p_entry_property)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_entry_property, 0, sizeof(ctc_sai_entry_property_t));
        sal_memcpy(p_entry_property, &entry_property, sizeof(ctc_sai_entry_property_t));
        p_entry_property->data = property;
    }
    ctc_hash_insert(g_sai_db[lchip]->entry_hash[type], p_entry_property);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_entry_property_remove(uint8 lchip, ctc_sai_db_entry_type_t type, void* key)
{
    ctc_sai_entry_property_t entry_property;
    ctc_sai_entry_property_t* p_entry_property = NULL;

    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_ENTRY_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    sal_memset(&entry_property, 0, sizeof(ctc_sai_entry_property_t));
    _ctc_sai_db_entry_mapping_key(type, key, &entry_property);
    p_entry_property = ctc_hash_remove(g_sai_db[lchip]->entry_hash[type], &entry_property);
    if (NULL == p_entry_property)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    mem_free(p_entry_property);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_entry_property_traverse(uint8 lchip, ctc_sai_db_entry_type_t type, hash_traversal_fn fn, void* data)
{
    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_ENTRY_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_hash_traverse_through(g_sai_db[lchip]->entry_hash[type], fn, data));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_entry_property_get_cnt(uint8 lchip, ctc_sai_db_entry_type_t type, uint32* count)
{
    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_ENTRY_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    *count = g_sai_db[lchip]->entry_hash[type]->count;
    return SAI_STATUS_SUCCESS;
}

void*
ctc_sai_db_vector_get(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index)
{
    ctc_sai_vector_property_t* p_vector_property = NULL;
    if ((lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[lchip])
        || (type >= CTC_SAI_DB_VECTOR_TYPE_MAX))
    {
        return NULL;
    }
    p_vector_property = ctc_vector_get(g_sai_db[lchip]->vector[type], index);
    if (p_vector_property)
    {
        return p_vector_property->data;
    }
    else
    {
        return NULL;
    }
}

sai_status_t
ctc_sai_db_vector_add(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index, void* data)
{
    ctc_sai_vector_property_t vector_property;
    ctc_sai_vector_property_t* p_vector_property = NULL;

    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_VECTOR_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&vector_property, 0, sizeof(vector_property));
    p_vector_property = ctc_vector_get(g_sai_db[lchip]->vector[type], index);
    if (p_vector_property)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    else
    {
        p_vector_property = (ctc_sai_vector_property_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_vector_property_t));
        if (NULL == p_vector_property)
        {
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_vector_property, 0, sizeof(ctc_sai_vector_property_t));
        p_vector_property->index = index;
        p_vector_property->data = data;
    }

    if (FALSE == ctc_vector_add(g_sai_db[lchip]->vector[type], index, p_vector_property))
    {
        mem_free(p_vector_property);
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_vector_remove(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index)
{
    ctc_sai_vector_property_t* p_vector_property = NULL;
    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_VECTOR_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    p_vector_property = ctc_vector_del(g_sai_db[lchip]->vector[type], index);
    if (NULL == p_vector_property)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    mem_free(p_vector_property);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_db_vector_traverse(uint8 lchip, ctc_sai_db_vector_type_t type, vector_traversal_fn fn, void* data)
{
    SAI_DB_INIT_CHECK();
    if (type >= CTC_SAI_DB_VECTOR_TYPE_MAX)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_vector_traverse(g_sai_db[lchip]->vector[type], fn, data));
    return SAI_STATUS_SUCCESS;
}

ctc_sai_switch_master_t*
ctc_sai_get_switch_property(uint8 lchip)
{
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_object_id_t sai_oid;
	uint8 gchip = 0;

	ctcs_get_gchip_id(lchip, &gchip);
    sai_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
    p_switch_master = ctc_sai_db_get_object_property(lchip, sai_oid);

    return p_switch_master;
}

sai_status_t
ctc_sai_db_init(uint8 lchip)
{
    uint8 type = 0;
    uint16 block_num= 0 ;
    uint16 block_size = 0;
    uint32 key_hash_block[CTC_SAI_DB_ENTRY_TYPE_MAX][2] = /*block_num, block_size*/
    {
        {64, 64},/*CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR*/
        {64, 64},/*CTC_SAI_DB_ENTRY_TYPE_ROUTE*/
        {64, 128},/*CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC*/
        {64, 128},/*CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC*/
        {64, 128},/*CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB*/
        {32, 1024},/*CTC_SAI_DB_ENTRY_TYPE_ACL*/
        {4, 1024},/*CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS*/
        {4, 1024},/*CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS*/
        {64, 64},  /*CTC_SAI_DB_ENTRY_TYPE_MPLS*/
        {64, 64} /*CTC_SAI_DB_ENTRY_TYPE_NAT*/
    };
    uint32 vector_block[CTC_SAI_DB_VECTOR_TYPE_MAX][2] = /*block_num, block_size*/
    {
        {CTC_SAI_DB_MIRROR_MAX, CTC_SAI_DB_MIRROR_SESSION_NUM}/*CTC_SAI_DB_VECTOR_TYPE_MIRROR*/
    };

    if(NULL != g_sai_db[lchip])
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    g_sai_db[lchip] = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_db_t));
    if (NULL == g_sai_db[lchip])
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(g_sai_db[lchip], 0, sizeof(ctc_sai_db_t));

    sal_mutex_create(&g_sai_db[lchip]->p_mutex);
    if (NULL == g_sai_db[lchip]->p_mutex)
    {
        mem_free(g_sai_db[lchip]);
        return SAI_STATUS_NOT_EXECUTED;
    }

    for (type = SAI_OBJECT_TYPE_PORT; type < SAI_OBJECT_TYPE_MAX; type++)
    {
        if (SAI_OBJECT_TYPE_NEXT_HOP == type)
        {
            block_num = 32;
            block_size = 128;
        }
        else if(SAI_OBJECT_TYPE_BRIDGE_PORT == type)
        {
            block_num = 64;
            block_size = 64;
        }
        else if (SAI_OBJECT_TYPE_ACL_TABLE == type)
        {
            /* 32K */
            block_num = 32;
            block_size = 1024;
        }
        else if (SAI_OBJECT_TYPE_ACL_ENTRY == type)
        {
            /* 64K */
            block_num = 64;
            block_size = 1024;
        }
        else
        {
            block_num = 32;
            block_size = 32;
        }
        g_sai_db[lchip]->oid_hash[type] = ctc_hash_create(block_num, block_size,
                                                (hash_key_fn)_ctc_sai_db_oid_hash_make,
                                                (hash_cmp_fn)_ctc_sai_db_oid_hash_cmp);
    }
    for (type = CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR; type < CTC_SAI_DB_ENTRY_TYPE_MAX; type++)
    {
        g_sai_db[lchip]->entry_hash[type] = ctc_hash_create(key_hash_block[type][0], key_hash_block[type][1],
                                                             (hash_key_fn)_ctc_sai_db_entry_hash_make,
                                                             (hash_cmp_fn)_ctc_sai_db_entry_hash_cmp);
    }

    for (type = CTC_SAI_DB_VECTOR_TYPE_MIRROR; type < CTC_SAI_DB_VECTOR_TYPE_MAX; type++)
    {
        g_sai_db[lchip]->vector[type] = ctc_vector_init(vector_block[type][0], vector_block[type][1]);
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_db_init_id(lchip));
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_db_deinit(uint8 lchip)
{
    uint8 type = 0;
    uint32 db_type = 0;
    SAI_DB_INIT_CHECK();

    db_type = 0;
    for (type = SAI_OBJECT_TYPE_PORT; type < SAI_OBJECT_TYPE_MAX; type++)
    {
        if (NULL == g_sai_db[lchip]->oid_hash[type])
        {
            continue;
        }
        ctc_hash_traverse(g_sai_db[lchip]->oid_hash[type], (hash_traversal_fn)_ctc_sai_db_deinit_cb, &db_type);
        ctc_hash_free(g_sai_db[lchip]->oid_hash[type]);
    }
    db_type = 1;
    for (type = CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR; type < CTC_SAI_DB_ENTRY_TYPE_MAX; type++)
    {
        if (NULL == g_sai_db[lchip]->entry_hash[type])
        {
            continue;
        }
        ctc_hash_traverse(g_sai_db[lchip]->entry_hash[type], (hash_traversal_fn)_ctc_sai_db_deinit_cb, &db_type);
        ctc_hash_free(g_sai_db[lchip]->entry_hash[type]);
    }

    for (type = CTC_SAI_DB_VECTOR_TYPE_MIRROR; type < CTC_SAI_DB_VECTOR_TYPE_MAX; type++)
    {
        if (NULL == g_sai_db[lchip]->vector[type])
        {
            continue;
        }
        ctc_vector_traverse(g_sai_db[lchip]->vector[type], (vector_traversal_fn)_ctc_sai_db_deinit_cb, NULL);
        ctc_vector_release(g_sai_db[lchip]->vector[type]);
    }

    _ctc_sai_db_deinit_id(lchip);
    mem_free(g_sai_db[lchip]);

    return SAI_STATUS_SUCCESS;
}

