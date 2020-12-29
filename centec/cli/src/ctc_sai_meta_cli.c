#include "ctc_sai_meta_db.h"
#include "ctc_sai_data_utils.h"
#include "ctc_sai_data_ser.h"
#include "ctc_sai_meta_cli.h"
#include "ctc_error.h"
#include "ctc_cli.h"
#include "ctc_cli_common.h"

sai_api_query_fn ctc_sai_api_query_fn;
sai_apis_t apis;
char buf[4096] = {0};

CTC_CLI(cli_sai_data_get,
        cli_sai_data_get_cmd,
        "sai get OID ATTR",
        "sai cmd",
        "sai get cmd",
        "sai object oid",
        "sai object attribute")
{
    int32 ret = 0;
    sai_object_id_t oid = 0;
    ctc_object_id_t ctc_object_id = {0};
    sai_attribute_t sai_attribute;
    ctc_sai_attr_metadata_t* attr_metadata = NULL;
    ctc_sai_object_meta_key_t meta_key;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    CTC_CLI_GET_UINT64("OID", oid, argv[0]);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_object_id);
    if (!ctc_sai_is_object_type_valid(ctc_object_id.type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return CLI_ERROR;
    }

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(ctc_object_id.type, argv[1]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = ctc_object_id.type;
    meta_key.objectkey.key.object_id = oid;
    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_object_get_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    sai_serialize_attribute(buf, attr_metadata, &sai_attribute);
    ctc_cli_out("%s\n", buf);

    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

CTC_CLI(cli_sai_data_set,
        cli_sai_data_set_cmd,
        "sai set OID ATTR STR",
        "sai cmd",
        "sai set cmd",
        "sai object oid",
        "sai object attribute",
        "sai attribute set str")
{
    int32 ret = 0;
    sai_object_id_t oid = 0;
    ctc_object_id_t ctc_object_id = {0};
    sai_attribute_t sai_attribute;
    ctc_sai_attr_metadata_t* attr_metadata = NULL;
    ctc_sai_object_meta_key_t meta_key;

    sal_memset(&meta_key, 0, sizeof(ctc_sai_object_meta_key_t));
    sal_memset(buf, 0, sizeof(buf));

    CTC_CLI_GET_UINT64("OID", oid, argv[0]);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_object_id);
    if (!ctc_sai_is_object_type_valid(ctc_object_id.type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "OID type is invalid!");
        return CLI_ERROR;
    }

    attr_metadata = ctc_sai_data_utils_object_get_attr_by_name(ctc_object_id.type, argv[1]);
    if (NULL == attr_metadata)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ATTR name is invalid!");
        return CLI_ERROR;
    }
    sai_attribute.id = attr_metadata->attrid;
    ret = ctc_sai_data_utils_attr_alloc_mem(attr_metadata->attrvaluetype, &sai_attribute);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Fail alloc attr memory!");
        return CLI_ERROR;
    }

    meta_key.objecttype = ctc_object_id.type;
    meta_key.objectkey.key.object_id = oid;

    sal_strncpy(buf, argv[2], sal_strlen(argv[2]));
    sai_deserialize_attribute(buf, attr_metadata, &sai_attribute);
    ret = ctc_sai_data_utils_object_set_attr(&meta_key, &sai_attribute);
    if (ret != SAI_STATUS_SUCCESS)
    {
        return CLI_ERROR;
    }
    ctc_sai_data_utils_attr_free_mem(attr_metadata->attrvaluetype, &sai_attribute);

    return CLI_SUCCESS;
}

int32
ctc_sai_cli_init(void)
{
    ctc_sai_metadata_apis_query(sai_api_query, &apis);

    /* sai cli under sdk mode */
    install_element(CTC_SDK_MODE, &cli_sai_data_set_cmd);
    install_element(CTC_SDK_MODE, &cli_sai_data_get_cmd);

    return CLI_SUCCESS;
}

