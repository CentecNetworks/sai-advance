#include <arpa/inet.h>
#include <byteswap.h>
#include <ctype.h>
#include <errno.h>
#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sai.h>
#include "ctc_sai_meta_db.h"
#include "ctc_sai_data_ser.h"
#include "ctc_sai_data_utils.h"

#define PRIMITIVE_BUFFER_SIZE 128
#define MAX_CHARS_PRINT 25


bool sai_serialize_is_char_allowed(
        _In_ char c)
{
    /*
     * When we will perform deserialize, we allow buffer string to be
     * terminated not only by zero, but also with json characters like:
     *
     * - end of quote
     * - comma, next item in array
     * - end of array
     *
     * This will be handy when performing deserialize.
     */

    return c == 0 || c == '"' || c == ',' || c == ']' || c == '}';
}

int sai_serialize_bool(
        _Out_ char *buffer,
        _In_ bool flag)
{
    return sprintf(buffer, "%s", flag ? "true" : "false");
}

#define SAI_TRUE_LENGTH 4
#define SAI_FALSE_LENGTH 5

int sai_deserialize_bool(
        _In_ char *buffer,
        _Out_ bool *flag)
{
    if (strncmp(buffer, "true", SAI_TRUE_LENGTH) == 0 &&
            sai_serialize_is_char_allowed(buffer[SAI_TRUE_LENGTH]))
    {
        *flag = true;
        return SAI_TRUE_LENGTH;
    }

    if (strncmp(buffer, "false", SAI_FALSE_LENGTH) == 0 &&
            sai_serialize_is_char_allowed(buffer[SAI_FALSE_LENGTH]))
    {
        *flag = false;
        return SAI_FALSE_LENGTH;
    }

    /*
     * Limit printf to maximum "false" length + 1 if there is invalid character
     * after "false" string.
     */
    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as bool",
            SAI_FALSE_LENGTH + 1,
            buffer);

    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_chardata(
        _Out_ char *buffer,
        _In_ char data[SAI_CHARDATA_LENGTH])
{
    int idx;

    for (idx = 0; idx < SAI_CHARDATA_LENGTH; ++idx)
    {
        char c = data[idx];

        if (c == 0)
        {
            break;
        }

        if (isprint(c) && c != '\\' && c != '"')
        {
            buffer[idx] = c;
            continue;
        }

        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid character 0x%x in chardata", c);
        return SAI_SERIALIZE_ERROR;
    }

    buffer[idx] = 0;

    return idx;
}

int sai_deserialize_chardata(
        _In_ char *buffer,
        _Out_ char data[SAI_CHARDATA_LENGTH])
{
    int idx;

    memset(data, 0, SAI_CHARDATA_LENGTH);

    for (idx = 0; idx < SAI_CHARDATA_LENGTH; ++idx)
    {
        char c = buffer[idx];

        if (isprint(c) && c != '\\' && c != '"')
        {
            data[idx] = c;
            continue;
        }

        if (c == 0)
        {
            break;
        }

        if (c == '"')
        {
            /*
             * We allow quote as last char since chardata will be serialized in
             * quotes.
             */

            break;
        }

        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid character 0x%x in chardata", c);
        return SAI_SERIALIZE_ERROR;
    }

    if (sai_serialize_is_char_allowed(buffer[idx]))
    {
        return idx;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid character 0x%x in chardata", buffer[idx]);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_uint8(
        _Out_ char *buffer,
        _In_ uint8_t u8)
{
    return sal_sprintf(buffer, "%u", u8);
}

int sai_deserialize_uint8(
        _In_ char *buffer,
        _Out_ uint8_t *u8)
{
    uint64_t u64;

    int res = sai_deserialize_uint64(buffer, &u64);

    if (res > 0 && u64 <= UCHAR_MAX)
    {
        *u8 = (uint8_t)u64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as uint8", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_int8(
        _Out_ char *buffer,
        _In_ int8_t s8)
{
    return sal_sprintf(buffer, "%d", s8);
}

int sai_deserialize_int8(
        _In_ char *buffer,
        _Out_ int8_t *s8)
{
    int64_t s64;

    int res = sai_deserialize_int64(buffer, &s64);

    if (res > 0 && s64 >= CHAR_MIN && s64 <= CHAR_MAX)
    {
        *s8 = (int8_t)s64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as int8", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_uint16(
        _Out_ char *buffer,
        _In_ uint16_t u16)
{
    return sprintf(buffer, "%u", u16);
}

int sai_deserialize_uint16(
        _In_ char *buffer,
        _Out_ uint16_t *u16)
{
    uint64_t u64;

    int res = sai_deserialize_uint64(buffer, &u64);

    if (res > 0 && u64 <= USHRT_MAX)
    {
        *u16 = (uint16_t)u64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as uint16", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_int16(
        _Out_ char *buffer,
        _In_ int16_t s16)
{
    return sprintf(buffer, "%d", s16);
}

int sai_deserialize_int16(
        _In_ char *buffer,
        _Out_ int16_t *s16)
{
    int64_t s64;

    int res = sai_deserialize_int64(buffer, &s64);

    if (res > 0 && s64 >= SHRT_MIN && s64 <= SHRT_MAX)
    {
        *s16 = (int16_t)s64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as int16", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_hex_uint32(
        _Out_ char *buffer,
        _In_ uint32_t u32)
{
    return sprintf(buffer, "%08X", u32);
}

int sai_serialize_uint32(
        _Out_ char *buffer,
        _In_ uint32_t u32)
{
    return sprintf(buffer, "%u", u32);
}

int sai_deserialize_uint32(
        _In_ char *buffer,
        _Out_ uint32_t *u32)
{
    uint64_t u64;

    int res = sai_deserialize_uint64(buffer, &u64);

    if (res > 0 && u64 <= UINT_MAX)
    {
        *u32 = (uint32_t)u64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as uint32", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_int32(
        _Out_ char *buffer,
        _In_ int32_t s32)
{
    return sprintf(buffer, "%d", s32);
}

int sai_deserialize_int32(
        _In_ char *buffer,
        _Out_ int32_t *s32)
{
    int64_t s64;

    int res = sai_deserialize_int64(buffer, &s64);

    if (res > 0 && s64 >= INT_MIN && s64 <= INT_MAX)
    {
        *s32 = (int32_t)s64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as int32", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_uint64(
        _Out_ char *buffer,
        _In_ uint64_t u64)
{
    return sprintf(buffer, "%"PRIu64, u64);
}

#define SAI_BASE_10 10

int sai_deserialize_uint64(
        _In_ char *buffer,
        _Out_ uint64_t *u64)
{
    int idx = 0;
    uint64_t result = 0;

    while (isdigit(buffer[idx]))
    {
        char c = (char)(buffer[idx] - '0');

        /*
         * Base is 10 we can check, that if result is greater than (2^64-1)/10)
         * then next multiplication with 10 will cause overflow.
         */

        if (result > (ULONG_MAX/SAI_BASE_10) ||
            ((result == ULONG_MAX/SAI_BASE_10) && (c > (char)(ULONG_MAX % SAI_BASE_10))))
        {
            idx = 0;
            break;
        }

        result = result * 10 + (uint64_t)(c);

        idx++;
    }

    if (idx > 0 && sai_serialize_is_char_allowed(buffer[idx]))
    {
        *u64 = result;
        return idx;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s...' as uint64", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_int64(
        _Out_ char *buffer,
        _In_ int64_t s64)
{
    return sprintf(buffer, "%"PRId64, s64);
}

int sai_deserialize_int64(
        _In_ char *buffer,
        _Out_ int64_t *s64)
{
    uint64_t result = 0;
    bool negative = 0;

    if (*buffer == '-')
    {
        buffer++;
        negative = true;
    }

    int res = sai_deserialize_uint64(buffer, &result);

    if (res > 0)
    {
        if (negative)
        {
            if (result <= (uint64_t)(LONG_MIN))
            {
                *s64 = -(int64_t)result;
                return res + 1;
            }
        }
        else
        {
            if (result <= LONG_MAX)
            {
                *s64 = (int64_t)result;
                return res;
            }
        }
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as int64", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_size(
        _Out_ char *buffer,
        _In_ sai_size_t size)
{
    return sprintf(buffer, "%zu", size);
}

int sai_deserialize_size(
        _In_ char *buffer,
        _Out_ sai_size_t *size)
{
    uint64_t u64;

    int res = sai_deserialize_uint64(buffer, &u64);

    if (res > 0)
    {
        *size = (sai_size_t)u64;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s...' as sai_size_t", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_object_id(
        _Out_ char *buffer,
        _In_ sai_object_id_t oid)
{
    return sprintf(buffer, "0x%"PRIx64, oid);
}

int sai_deserialize_object_id(
        _In_ char *buffer,
        _Out_ sai_object_id_t *oid)
{
    int read;

    int n = sscanf(buffer, "oid:0x%16"PRIx64"%n", oid, &read);

    if (n == 1 && sai_serialize_is_char_allowed(buffer[read]))
    {
        return read;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as oid", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_mac(
        _Out_ char *buffer,
        _In_ sai_mac_t mac)
{
    return sprintf(buffer, "%02X:%02X:%02X:%02X:%02X:%02X",
            mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}

#define SAI_MAC_ADDRESS_LENGTH 17

int sai_deserialize_mac(
        _In_ char *buffer,
        _Out_ sai_mac_t mac)
{
    int arr[6];
    int read;

    int n = sscanf(buffer, "%2X:%2X:%2X:%2X:%2X:%2X%n",
            &arr[0], &arr[1], &arr[2], &arr[3], &arr[4], &arr[5], &read);

    if (n == 6 && read == SAI_MAC_ADDRESS_LENGTH && sai_serialize_is_char_allowed(buffer[read]))
    {
        for (n = 0; n < 6; n++)
        {
            mac[n] = (uint8_t)arr[n];
        }

        return SAI_MAC_ADDRESS_LENGTH;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as mac address", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_macsec_sak(
        _Out_ char *buffer,
        _In_ sai_macsec_sak_t sak)
{
    return sprintf(buffer, "%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:\
%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:\
%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:\
%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X",
                   sak[0], sak[1], sak[2], sak[3], sak[4], sak[5],sak[6], sak[7],
                   sak[8], sak[9], sak[10], sak[11], sak[12], sak[13],sak[14], sak[15],
                   sak[16], sak[17], sak[18], sak[19], sak[20], sak[21],sak[22], sak[23],
                   sak[24], sak[25], sak[26], sak[27], sak[28], sak[29],sak[30], sak[31]);
}

int sai_deserialize_macsec_sak(
        _In_ char *buffer,
        _Out_ sai_macsec_sak_t sak)
{
    int arr[32];
    int read;

    int n = sscanf(buffer, "%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:\
%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X%n",
                   &arr[0], &arr[1], &arr[2], &arr[3],
                   &arr[4], &arr[5], &arr[6], &arr[7],
                   &arr[8], &arr[9], &arr[10], &arr[11],
                   &arr[12], &arr[13], &arr[14], &arr[15],
                   &arr[16], &arr[17], &arr[18], &arr[19],
                   &arr[20], &arr[21], &arr[22], &arr[23],
                   &arr[24], &arr[25], &arr[26], &arr[27],
                   &arr[28], &arr[29], &arr[30], &arr[31], &read);

    if (n == 32 && read == (32*3-1))
    {
        for (n = 0; n < 32; n++)
        {
            sak[n] = (uint8_t)arr[n];
        }

        return read;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as macsec_sak", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_macsec_auth_key(
        _Out_ char *buffer,
        _In_ sai_macsec_auth_key_t auth)
{
    return sprintf(buffer, "%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:\
%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X",
                   auth[0], auth[1], auth[2], auth[3], auth[4], auth[5],auth[6], auth[7],
                   auth[8], auth[9], auth[10], auth[11], auth[12], auth[13],auth[14], auth[15]);
}

int sai_deserialize_macsec_auth_key(
        _In_ char *buffer,
        _Out_ sai_macsec_auth_key_t auth)
{
    int arr[16];
    int read;

    int n = sscanf(buffer, "%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X%n",
                   &arr[0], &arr[1], &arr[2], &arr[3],
                   &arr[4], &arr[5], &arr[6], &arr[7],
                   &arr[8], &arr[9], &arr[10], &arr[11],
                   &arr[12], &arr[13], &arr[14], &arr[15], &read);

    if (n == 16 && read == (16*3-1))
    {
       for (n = 0; n < 16; n++)
        {
            auth[n] = (uint8_t)arr[n];
        }

        return read;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as macsec_auth_key", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_macsec_salt(
        _Out_ char *buffer,
        _In_ sai_macsec_salt_t salt)
{
    return sprintf(buffer, "%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X",
                   salt[0], salt[1], salt[2], salt[3], salt[4], salt[5],salt[6], salt[7],
                   salt[8], salt[9], salt[10], salt[11]);
}

int sai_deserialize_macsec_salt(
        _In_ char *buffer,
        _Out_ sai_macsec_salt_t salt)
{
    int arr[32];
    int read;

    int n = sscanf(buffer, "%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:\
%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X:%2X%n",
                   &arr[0], &arr[1], &arr[2], &arr[3],
                   &arr[4], &arr[5], &arr[6], &arr[7],
                   &arr[8], &arr[9], &arr[10], &arr[11],
                   &arr[12], &arr[13], &arr[14], &arr[15],
                   &arr[16], &arr[17], &arr[18], &arr[19],
                   &arr[20], &arr[21], &arr[22], &arr[23],
                   &arr[24], &arr[25], &arr[26], &arr[27],
                   &arr[28], &arr[29], &arr[30], &arr[31], &read);

    if (n == 32 && read == (32*3-1))
    {
        for (n = 0; n < 32; n++)
        {
            salt[n] = (uint8_t)arr[n];
        }

        return read;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as macsec_salt", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_enum(
        _Out_ char *buffer,
        _In_ ctc_sai_enum_metadata_t *meta,
        _In_ int32_t value)
{
    if (meta ==  NULL)
    {
        return sai_serialize_int32(buffer, value);
    }
    size_t i = 0;

    for (; i < meta->valuescount; ++i)
    {
        if (meta->values[i] == value)
        {
            return sal_sprintf(buffer, "%s", meta->valuesnames[i]);
        }
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "enum value %d not found in enum %s", value, meta->name);

    return sai_serialize_int32(buffer, value);
}

int sai_deserialize_enum(
        _In_ char *buffer,
        _In_ ctc_sai_enum_metadata_t *meta,
        _Out_ int32_t *value)
{
    if (meta == NULL)
    {
        return sai_deserialize_int32(buffer, value);
    }

    size_t idx = 0;

    for (; idx < meta->valuescount; ++idx)
    {
        size_t len = strlen(meta->valuesnames[idx]);

        if (strncmp(meta->valuesnames[idx], buffer, len) == 0 &&
            sai_serialize_is_char_allowed(buffer[len]))
        {
            *value = meta->values[idx];
            return (int)len;
        }
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "enum value '%.*s' not found in enum %s", MAX_CHARS_PRINT, buffer, meta->name);

    return sai_deserialize_int32(buffer, value);
}

static int sai_deserialize_ip(
        _In_ char *buffer,
        _In_ int inet,
        _Out_ uint8_t *ip)
{
    /*
     * Since we want relaxed version of deserialize, after ip address there
     * may be '"' (quote), but inet_pton expects '\0' at the end, so copy at
     * most INET6 characters to local buffer.
     */

    char local[INET6_ADDRSTRLEN + 1];

    int idx;

    for (idx = 0; idx < INET6_ADDRSTRLEN; idx++)
    {
        char c = buffer[idx];

        if (isxdigit(c) || c == ':' || c == '.')
        {
            local[idx] = c;
            continue;
        }

        break;
    }

    local[idx] = 0;

    if (inet_pton(inet, local, ip) != 1)
    {
        /*
         * We should not warn here, since we will use this method to
         * deserialize ip4 and ip6 and we will need to guess which one.
         */

        return SAI_SERIALIZE_ERROR;
    }

    if (sai_serialize_is_char_allowed(buffer[idx]) || buffer[idx] == '/')
    {
        return idx;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid char 0x%x at end of ip address", buffer[idx]);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_ip4(
        _Out_ char *buffer,
        _In_ sai_ip4_t ip4)
{
    if (inet_ntop(AF_INET, &ip4, buffer, INET_ADDRSTRLEN) == NULL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to convert ipv4 address, errno: %s", strerror(errno));
        return SAI_SERIALIZE_ERROR;
    }

    return (int)strlen(buffer);
}

int sai_deserialize_ip4(
        _In_ char *buffer,
        _Out_ sai_ip4_t *ip4)
{
    return sai_deserialize_ip(buffer, AF_INET, (uint8_t*)ip4);
}

int sai_serialize_ip6(
        _Out_ char *buffer,
        _In_ sai_ip6_t ip6)
{
    if (inet_ntop(AF_INET6, ip6, buffer, INET6_ADDRSTRLEN) == NULL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to convert ipv6 address, errno: %s", strerror(errno));
        return SAI_SERIALIZE_ERROR;
    }

    return (int)strlen(buffer);
}

int sai_deserialize_ip6(
        _In_ char *buffer,
        _Out_ sai_ip6_t ip6)
{
    return sai_deserialize_ip(buffer, AF_INET6, ip6);
}

int sai_serialize_ip_address(
        _Out_ char *buffer,
        _In_ sai_ip_address_t *ip_address)
{
    switch (ip_address->addr_family)
    {
        case SAI_IP_ADDR_FAMILY_IPV4:

            return sai_serialize_ip4(buffer, ip_address->addr.ip4);

        case SAI_IP_ADDR_FAMILY_IPV6:

            return sai_serialize_ip6(buffer, ip_address->addr.ip6);

        default:

            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid ip address family: %d", ip_address->addr_family);
            return SAI_SERIALIZE_ERROR;
    }
}

int sai_deserialize_ip_address(
        _In_ char *buffer,
        _Out_ sai_ip_address_t *ip_address)
{
    int res;

    /* try first deserialize ip4 then ip6 */

    res = sai_deserialize_ip(buffer, AF_INET, (uint8_t*)&ip_address->addr.ip4);

    if (res > 0)
    {
        ip_address->addr_family = SAI_IP_ADDR_FAMILY_IPV4;
        return res;
    }

    res = sai_deserialize_ip(buffer, AF_INET6, ip_address->addr.ip6);

    if (res > 0)
    {
        ip_address->addr_family = SAI_IP_ADDR_FAMILY_IPV6;
        return res;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as ip address",
            INET6_ADDRSTRLEN, buffer);

    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_ip_prefix(
        _Out_ char *buffer,
        _In_ sai_ip_prefix_t *ip_prefix)
{
    int ret = 0;

    char addr[PRIMITIVE_BUFFER_SIZE];
    char mask[PRIMITIVE_BUFFER_SIZE];

    switch (ip_prefix->addr_family)
    {
        case SAI_IP_ADDR_FAMILY_IPV4:

            ret |= sai_serialize_ip4(addr, ip_prefix->addr.ip4);
            ret |= sai_serialize_ip4_mask(mask, ip_prefix->mask.ip4);

            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize ipv4");
                return SAI_SERIALIZE_ERROR;
            }

            break;

        case SAI_IP_ADDR_FAMILY_IPV6:

            ret |= sai_serialize_ip6(addr, ip_prefix->addr.ip6);
            ret |= sai_serialize_ip6_mask(mask, ip_prefix->mask.ip6);

            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize ipv6");
                return SAI_SERIALIZE_ERROR;
            }

            break;

        default:

            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "invalid ip address family: %d", ip_prefix->addr_family);
            return SAI_SERIALIZE_ERROR;
    }

    return sprintf(buffer, "%s/%s", addr, mask);
}

int sai_deserialize_ip_prefix(
    _In_ char *buffer,
    _Out_ sai_ip_prefix_t *ip_prefix)
{
    /* try first deserialize ip4 then ip6 */

    int res, n;

    while (true)
    {
        res = sai_deserialize_ip(buffer, AF_INET, (uint8_t*)&ip_prefix->addr.ip4);

        if (res > 0)
        {
            ip_prefix->addr_family = SAI_IP_ADDR_FAMILY_IPV4;

            if (buffer[res++] != '/')
            {
                break;
            }

            n = sai_deserialize_ip4_mask(buffer + res, &ip_prefix->mask.ip4);

            if (n > 0)
            {
                return res + n;
            }

            break;
        }

        res = sai_deserialize_ip(buffer, AF_INET6, ip_prefix->addr.ip6);

        if (res > 0)
        {
            if (buffer[res++] != '/')
            {
                break;
            }

            ip_prefix->addr_family = SAI_IP_ADDR_FAMILY_IPV6;

            n = sai_deserialize_ip6_mask(buffer + res, (uint8_t*)&ip_prefix->mask.ip6);

            if (n > 0)
            {
                return res + n;
            }
        }

        break;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as ip prefix", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_ip4_mask(
        _Out_ char *buffer,
        _In_ sai_ip4_t mask)
{
    uint32_t n = 32;
    uint32_t tmp = 0xFFFFFFFF;

    mask = __builtin_bswap32(mask);

    for (; (tmp != mask) && tmp; tmp <<= 1, n--);

    if (tmp == mask)
    {
        return sai_serialize_uint32(buffer, n);
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ipv4 mask 0x%X has holes", htonl(mask));
    return SAI_SERIALIZE_ERROR;
}

int sai_deserialize_ip4_mask(
        _In_ char *buffer,
        _Out_ sai_ip4_t *mask)
{
    uint32_t value;

    int res = sai_deserialize_uint32(buffer, &value);

    if (res < 0 || value > 32)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as ip4 mask", MAX_CHARS_PRINT, buffer);
        return SAI_SERIALIZE_ERROR;
    }

    if (value == 0)
    {
        /* mask is all zeros */
    }
    else if (value == 32)
    {
        value = 0xFFFFFFFF;
    }
    else
    {
        value = 0xFFFFFFFF << (32 - value);
    }

    *mask = __builtin_bswap32(value);

    return res;
}

int sai_serialize_ip6_mask(
        _Out_ char *buffer,
        _In_ sai_ip6_t mask)
{
    uint32_t n = 64;
    uint64_t tmp = UINT64_C(0xFFFFFFFFFFFFFFFF);

    uint64_t high;
    uint64_t low;
    memcpy(&high, (uint8_t*)mask, sizeof(uint64_t));
    memcpy(&low, ((uint8_t*)mask + sizeof(uint64_t)), sizeof(uint64_t));

    high = __builtin_bswap64(high);
    low = __builtin_bswap64(low);

    if (high == tmp)
    {
        for (; (tmp != low) && tmp; tmp <<= 1, n--);

        if (tmp == low)
        {
            return sai_serialize_uint32(buffer, 64 + n);
        }
    }
    else if (low == 0)
    {
        for (; (tmp != high) && tmp; tmp <<= 1, n--);

        if (tmp == high)
        {
            return sai_serialize_uint32(buffer, n);
        }
    }

    char buf[PRIMITIVE_BUFFER_SIZE];

    sai_serialize_ip6(buf, mask);

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "ipv6 mask %s has holes", buf);
    return SAI_SERIALIZE_ERROR;
}

int sai_deserialize_ip6_mask(
        _In_ char *buffer,
        _Out_ sai_ip6_t mask)
{
    uint64_t value;

    int res = sai_deserialize_uint64(buffer, &value);

    if (res < 0 || value > 128)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as ip6 mask", MAX_CHARS_PRINT, buffer);
        return SAI_SERIALIZE_ERROR;
    }

    uint64_t high = UINT64_C(0xFFFFFFFFFFFFFFFF);
    uint64_t low  = UINT64_C(0xFFFFFFFFFFFFFFFF);
    uint64_t tmp;

    if (value == 128)
    {
        /* mask is all ones */
    }
    else if (value == 64)
    {
        low = 0;
    }
    else if (value == 0)
    {
        low = 0;
        high = 0;
    }
    else if (value > 64)
    {
        low = low << (128 - value);
    }
    else
    {
        high = high << (64 - value);
        low = 0;
    }

    tmp = __builtin_bswap64(high);
    memcpy((uint8_t*)mask, &tmp, sizeof(uint64_t));
    tmp = __builtin_bswap64(low);
    memcpy(((uint8_t*)mask + sizeof(uint64_t)), &tmp, sizeof(uint64_t));

    return res;
}

int sai_serialize_pointer(
        _Out_ char *buffer,
        _In_ sai_pointer_t pointer)
{
    return sprintf(buffer, "%p", pointer);
}

int sai_deserialize_pointer(
        _In_ char *buffer,
        _Out_ sai_pointer_t *pointer)
{
    int read;

    int n = sscanf(buffer, "ptr:%p%n", pointer, &read);

    if (n == 1 && sai_serialize_is_char_allowed(buffer[read]))
    {
        return read;
    }

    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize '%.*s' as pointer", MAX_CHARS_PRINT, buffer);
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_enum_list(
        _Out_ char *buf,
        _In_ ctc_sai_enum_metadata_t *meta,
        _In_ sai_s32_list_t *list)
{
    if (meta == NULL)
    {
        return sai_serialize_s32_list(buf, list);
    }

    char *begin_buf = buf;
    int ret;

    if (list->list == NULL || list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }

            ret = sai_serialize_enum(buf, meta, list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize enum_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}

int sai_deserialize_enum_list(
        _In_ char *buffer,
        _In_ ctc_sai_enum_metadata_t *meta,
        _Out_ sai_s32_list_t *list)
{
    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "not implemented");
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_attr_id(
        _Out_ char *buf,
        _In_ ctc_sai_attr_metadata_t *meta,
        _In_ sai_attr_id_t attr_id)
{
    strcpy(buf, meta->attridname);

    return (int)strlen(buf);
}

int sai_deserialize_attr_id(
        _In_ char *buffer,
        _Out_ sai_attr_id_t *attr_id)
{
    CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "not implemented");
    return SAI_SERIALIZE_ERROR;
}

int sai_serialize_attribute(
        _Out_ char *buf,
        _In_ ctc_sai_attr_metadata_t *meta,
        _In_ sai_attribute_t *attribute)
{
    int ret;
    char *begin_buf = buf;
    ctc_sai_object_type_info_t *sai_object_type_info = NULL;

    sai_object_type_info = ctc_sai_data_utils_get_object_type_info(meta->objecttype);

    /* can be auto generated */
    buf += sal_sprintf(buf, "OjectName: %s\n", sai_object_type_info->objecttypename);
    buf += sal_sprintf(buf, "AttrName:  ");

    ret = sai_serialize_attr_id(buf, meta, attribute->id);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize attr id");
        return SAI_SERIALIZE_ERROR;
    }

    buf += ret;
    buf += sal_sprintf(buf, "\n");

    ret = sai_serialize_attribute_value(buf, meta, &attribute->value);
    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize attribute value");
        return SAI_SERIALIZE_ERROR;
    }
    buf += ret;

    return (int)(buf - begin_buf);
}

int sai_deserialize_attribute(
        _In_ char *buffer,
        _In_ ctc_sai_attr_metadata_t *meta,
        _Out_ sai_attribute_t *attribute)
{
    int ret;

    ret = sai_deserialize_attribute_value(buffer, meta, &attribute->value);

    if (ret < 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize attr value");
        return SAI_SERIALIZE_ERROR;
    }

    return 0;
}

int sai_serialize_acl_action_type(
    _Out_ char *buffer,
    _In_ sai_acl_action_type_t acl_action_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_action_type_t, acl_action_type);
}
int sai_serialize_acl_bind_point_type(
    _Out_ char *buffer,
    _In_ sai_acl_bind_point_type_t acl_bind_point_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_bind_point_type_t, acl_bind_point_type);
}
int sai_serialize_acl_dtel_flow_op(
    _Out_ char *buffer,
    _In_ sai_acl_dtel_flow_op_t acl_dtel_flow_op)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_dtel_flow_op_t, acl_dtel_flow_op);
}
int sai_serialize_acl_ip_frag(
    _Out_ char *buffer,
    _In_ sai_acl_ip_frag_t acl_ip_frag)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_ip_frag_t, acl_ip_frag);
}
int sai_serialize_acl_ip_type(
    _Out_ char *buffer,
    _In_ sai_acl_ip_type_t acl_ip_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_ip_type_t, acl_ip_type);
}
int sai_serialize_acl_range_type(
    _Out_ char *buffer,
    _In_ sai_acl_range_type_t acl_range_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_range_type_t, acl_range_type);
}
int sai_serialize_acl_stage(
    _Out_ char *buffer,
    _In_ sai_acl_stage_t acl_stage)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_stage_t, acl_stage);
}
int sai_serialize_acl_table_group_type(
    _Out_ char *buffer,
    _In_ sai_acl_table_group_type_t acl_table_group_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_table_group_type_t, acl_table_group_type);
}
int sai_serialize_attr_value_type(
    _Out_ char *buffer,
    _In_ ctc_sai_attr_value_type_t attr_value_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_ctc_sai_attr_value_type_t, attr_value_type);
}
int sai_serialize_bfd_ach_channel_type(
    _Out_ char *buffer,
    _In_ sai_bfd_ach_channel_type_t bfd_ach_channel_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_ach_channel_type_t, bfd_ach_channel_type);
}
int sai_serialize_bfd_encapsulation_type(
    _Out_ char *buffer,
    _In_ sai_bfd_encapsulation_type_t bfd_encapsulation_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_encapsulation_type_t, bfd_encapsulation_type);
}
int sai_serialize_bfd_mpls_type(
    _Out_ char *buffer,
    _In_ sai_bfd_mpls_type_t bfd_mpls_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_mpls_type_t, bfd_mpls_type);
}
int sai_serialize_bfd_session_offload_type(
    _Out_ char *buffer,
    _In_ sai_bfd_session_offload_type_t bfd_session_offload_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_offload_type_t, bfd_session_offload_type);
}
int sai_serialize_bfd_session_stat(
    _Out_ char *buffer,
    _In_ sai_bfd_session_stat_t bfd_session_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_stat_t, bfd_session_stat);
}
int sai_serialize_bfd_session_state(
    _Out_ char *buffer,
    _In_ sai_bfd_session_state_t bfd_session_state)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_state_t, bfd_session_state);
}
int sai_serialize_bfd_session_type(
    _Out_ char *buffer,
    _In_ sai_bfd_session_type_t bfd_session_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_type_t, bfd_session_type);
}
int sai_serialize_bridge_flood_control_type(
    _Out_ char *buffer,
    _In_ sai_bridge_flood_control_type_t bridge_flood_control_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_flood_control_type_t, bridge_flood_control_type);
}
int sai_serialize_bridge_port_fdb_learning_mode(
    _Out_ char *buffer,
    _In_ sai_bridge_port_fdb_learning_mode_t bridge_port_fdb_learning_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_fdb_learning_mode_t, bridge_port_fdb_learning_mode);
}
int sai_serialize_bridge_port_outgoing_service_vlan_cos_mode(
    _Out_ char *buffer,
    _In_ sai_bridge_port_outgoing_service_vlan_cos_mode_t bridge_port_outgoing_service_vlan_cos_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_outgoing_service_vlan_cos_mode_t, bridge_port_outgoing_service_vlan_cos_mode);
}
int sai_serialize_bridge_port_stat(
    _Out_ char *buffer,
    _In_ sai_bridge_port_stat_t bridge_port_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_stat_t, bridge_port_stat);
}
int sai_serialize_bridge_port_tagging_mode(
    _Out_ char *buffer,
    _In_ sai_bridge_port_tagging_mode_t bridge_port_tagging_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_tagging_mode_t, bridge_port_tagging_mode);
}
int sai_serialize_bridge_port_type(
    _Out_ char *buffer,
    _In_ sai_bridge_port_type_t bridge_port_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_type_t, bridge_port_type);
}
int sai_serialize_bridge_stat(
    _Out_ char *buffer,
    _In_ sai_bridge_stat_t bridge_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_stat_t, bridge_stat);
}
int sai_serialize_bridge_type(
    _Out_ char *buffer,
    _In_ sai_bridge_type_t bridge_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_type_t, bridge_type);
}
int sai_serialize_buffer_monitor_based_on_type(
    _Out_ char *buffer,
    _In_ sai_buffer_monitor_based_on_type_t buffer_monitor_based_on_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_based_on_type_t, buffer_monitor_based_on_type);
}
int sai_serialize_buffer_monitor_message_type(
    _Out_ char *buffer,
    _In_ sai_buffer_monitor_message_type_t buffer_monitor_message_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_message_type_t, buffer_monitor_message_type);
}
int sai_serialize_buffer_monitor_stats_direction(
    _Out_ char *buffer,
    _In_ sai_buffer_monitor_stats_direction_t buffer_monitor_stats_direction)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_stats_direction_t, buffer_monitor_stats_direction);
}
int sai_serialize_buffer_pool_stat(
    _Out_ char *buffer,
    _In_ sai_buffer_pool_stat_t buffer_pool_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_stat_t, buffer_pool_stat);
}
int sai_serialize_buffer_pool_threshold_mode(
    _Out_ char *buffer,
    _In_ sai_buffer_pool_threshold_mode_t buffer_pool_threshold_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_threshold_mode_t, buffer_pool_threshold_mode);
}
int sai_serialize_buffer_pool_type(
    _Out_ char *buffer,
    _In_ sai_buffer_pool_type_t buffer_pool_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_type_t, buffer_pool_type);
}
int sai_serialize_buffer_profile_threshold_mode(
    _Out_ char *buffer,
    _In_ sai_buffer_profile_threshold_mode_t buffer_profile_threshold_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_profile_threshold_mode_t, buffer_profile_threshold_mode);
}
int sai_serialize_bulk_op_error_mode(
    _Out_ char *buffer,
    _In_ sai_bulk_op_error_mode_t bulk_op_error_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_bulk_op_error_mode_t, bulk_op_error_mode);
}
int sai_serialize_common_api(
    _Out_ char *buffer,
    _In_ sai_common_api_t common_api)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_common_api_t, common_api);
}
int sai_serialize_counter_stat(
    _Out_ char *buffer,
    _In_ sai_counter_stat_t counter_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_counter_stat_t, counter_stat);
}
int sai_serialize_counter_type(
    _Out_ char *buffer,
    _In_ sai_counter_type_t counter_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_counter_type_t, counter_type);
}
int sai_serialize_debug_counter_bind_method(
    _Out_ char *buffer,
    _In_ sai_debug_counter_bind_method_t debug_counter_bind_method)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_debug_counter_bind_method_t, debug_counter_bind_method);
}
int sai_serialize_debug_counter_type(
    _Out_ char *buffer,
    _In_ sai_debug_counter_type_t debug_counter_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_debug_counter_type_t, debug_counter_type);
}
int sai_serialize_dtel_event_type(
    _Out_ char *buffer,
    _In_ sai_dtel_event_type_t dtel_event_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_dtel_event_type_t, dtel_event_type);
}
int sai_serialize_ecn_mark_mode(
    _Out_ char *buffer,
    _In_ sai_ecn_mark_mode_t ecn_mark_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ecn_mark_mode_t, ecn_mark_mode);
}
int sai_serialize_erspan_encapsulation_type(
    _Out_ char *buffer,
    _In_ sai_erspan_encapsulation_type_t erspan_encapsulation_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_erspan_encapsulation_type_t, erspan_encapsulation_type);
}
int sai_serialize_fdb_entry_type(
    _Out_ char *buffer,
    _In_ sai_fdb_entry_type_t fdb_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_entry_type_t, fdb_entry_type);
}
int sai_serialize_fdb_event(
    _Out_ char *buffer,
    _In_ sai_fdb_event_t fdb_event)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_event_t, fdb_event);
}
int sai_serialize_fdb_flush_entry_type(
    _Out_ char *buffer,
    _In_ sai_fdb_flush_entry_type_t fdb_flush_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_flush_entry_type_t, fdb_flush_entry_type);
}
int sai_serialize_hash_algorithm(
    _Out_ char *buffer,
    _In_ sai_hash_algorithm_t hash_algorithm)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hash_algorithm_t, hash_algorithm);
}
int sai_serialize_hostif_packet_oam_tx_type(
    _Out_ char *buffer,
    _In_ sai_hostif_packet_oam_tx_type_t hostif_packet_oam_tx_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_packet_oam_tx_type_t, hostif_packet_oam_tx_type);
}
int sai_serialize_hostif_packet_ptp_tx_packet_op_type(
    _Out_ char *buffer,
    _In_ sai_hostif_packet_ptp_tx_packet_op_type_t hostif_packet_ptp_tx_packet_op_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_packet_ptp_tx_packet_op_type_t, hostif_packet_ptp_tx_packet_op_type);
}
int sai_serialize_hostif_table_entry_channel_type(
    _Out_ char *buffer,
    _In_ sai_hostif_table_entry_channel_type_t hostif_table_entry_channel_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_table_entry_channel_type_t, hostif_table_entry_channel_type);
}
int sai_serialize_hostif_table_entry_type(
    _Out_ char *buffer,
    _In_ sai_hostif_table_entry_type_t hostif_table_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_table_entry_type_t, hostif_table_entry_type);
}
int sai_serialize_hostif_trap_type(
    _Out_ char *buffer,
    _In_ sai_hostif_trap_type_t hostif_trap_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_trap_type_t, hostif_trap_type);
}
int sai_serialize_hostif_tx_type(
    _Out_ char *buffer,
    _In_ sai_hostif_tx_type_t hostif_tx_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_tx_type_t, hostif_tx_type);
}
int sai_serialize_hostif_type(
    _Out_ char *buffer,
    _In_ sai_hostif_type_t hostif_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_type_t, hostif_type);
}
int sai_serialize_hostif_user_defined_trap_type(
    _Out_ char *buffer,
    _In_ sai_hostif_user_defined_trap_type_t hostif_user_defined_trap_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_user_defined_trap_type_t, hostif_user_defined_trap_type);
}
int sai_serialize_hostif_vlan_tag(
    _Out_ char *buffer,
    _In_ sai_hostif_vlan_tag_t hostif_vlan_tag)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_vlan_tag_t, hostif_vlan_tag);
}
int sai_serialize_in_drop_reason(
    _Out_ char *buffer,
    _In_ sai_in_drop_reason_t in_drop_reason)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_in_drop_reason_t, in_drop_reason);
}
int sai_serialize_ingress_priority_group_stat(
    _Out_ char *buffer,
    _In_ sai_ingress_priority_group_stat_t ingress_priority_group_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ingress_priority_group_stat_t, ingress_priority_group_stat);
}
int sai_serialize_inseg_entry_configured_role(
    _Out_ char *buffer,
    _In_ sai_inseg_entry_configured_role_t inseg_entry_configured_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_configured_role_t, inseg_entry_configured_role);
}
int sai_serialize_inseg_entry_frr_observed_role(
    _Out_ char *buffer,
    _In_ sai_inseg_entry_frr_observed_role_t inseg_entry_frr_observed_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_frr_observed_role_t, inseg_entry_frr_observed_role);
}
int sai_serialize_inseg_entry_pop_qos_mode(
    _Out_ char *buffer,
    _In_ sai_inseg_entry_pop_qos_mode_t inseg_entry_pop_qos_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_pop_qos_mode_t, inseg_entry_pop_qos_mode);
}
int sai_serialize_inseg_entry_pop_ttl_mode(
    _Out_ char *buffer,
    _In_ sai_inseg_entry_pop_ttl_mode_t inseg_entry_pop_ttl_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_pop_ttl_mode_t, inseg_entry_pop_ttl_mode);
}
int sai_serialize_inseg_entry_psc_type(
    _Out_ char *buffer,
    _In_ sai_inseg_entry_psc_type_t inseg_entry_psc_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_psc_type_t, inseg_entry_psc_type);
}
int sai_serialize_ip_addr_family(
    _Out_ char *buffer,
    _In_ sai_ip_addr_family_t ip_addr_family)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ip_addr_family_t, ip_addr_family);
}
int sai_serialize_ipmc_entry_type(
    _Out_ char *buffer,
    _In_ sai_ipmc_entry_type_t ipmc_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ipmc_entry_type_t, ipmc_entry_type);
}
int sai_serialize_isolation_group_type(
    _Out_ char *buffer,
    _In_ sai_isolation_group_type_t isolation_group_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_isolation_group_type_t, isolation_group_type);
}
int sai_serialize_l2mc_entry_type(
    _Out_ char *buffer,
    _In_ sai_l2mc_entry_type_t l2mc_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_l2mc_entry_type_t, l2mc_entry_type);
}
int sai_serialize_lag_mode(
    _Out_ char *buffer,
    _In_ sai_lag_mode_t lag_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_lag_mode_t, lag_mode);
}
int sai_serialize_latency_monitor_message_type(
    _Out_ char *buffer,
    _In_ sai_latency_monitor_message_type_t latency_monitor_message_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_latency_monitor_message_type_t, latency_monitor_message_type);
}
int sai_serialize_macsec_direction(
    _Out_ char *buffer,
    _In_ sai_macsec_direction_t macsec_direction)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_direction_t, macsec_direction);
}
int sai_serialize_macsec_flow_stat(
    _Out_ char *buffer,
    _In_ sai_macsec_flow_stat_t macsec_flow_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_flow_stat_t, macsec_flow_stat);
}
int sai_serialize_macsec_port_stat(
    _Out_ char *buffer,
    _In_ sai_macsec_port_stat_t macsec_port_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_port_stat_t, macsec_port_stat);
}
int sai_serialize_macsec_sa_stat(
    _Out_ char *buffer,
    _In_ sai_macsec_sa_stat_t macsec_sa_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_sa_stat_t, macsec_sa_stat);
}
int sai_serialize_macsec_sc_stat(
    _Out_ char *buffer,
    _In_ sai_macsec_sc_stat_t macsec_sc_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_sc_stat_t, macsec_sc_stat);
}
int sai_serialize_meter_type(
    _Out_ char *buffer,
    _In_ sai_meter_type_t meter_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_meter_type_t, meter_type);
}
int sai_serialize_mirror_session_congestion_mode(
    _Out_ char *buffer,
    _In_ sai_mirror_session_congestion_mode_t mirror_session_congestion_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_mirror_session_congestion_mode_t, mirror_session_congestion_mode);
}
int sai_serialize_mirror_session_type(
    _Out_ char *buffer,
    _In_ sai_mirror_session_type_t mirror_session_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_mirror_session_type_t, mirror_session_type);
}
int sai_serialize_monitor_event_state(
    _Out_ char *buffer,
    _In_ sai_monitor_event_state_t monitor_event_state)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_monitor_event_state_t, monitor_event_state);
}
int sai_serialize_nat_type(
    _Out_ char *buffer,
    _In_ sai_nat_type_t nat_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_nat_type_t, nat_type);
}
int sai_serialize_native_hash_field(
    _Out_ char *buffer,
    _In_ sai_native_hash_field_t native_hash_field)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_native_hash_field_t, native_hash_field);
}
int sai_serialize_next_hop_endpoint_pop_type(
    _Out_ char *buffer,
    _In_ sai_next_hop_endpoint_pop_type_t next_hop_endpoint_pop_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_endpoint_pop_type_t, next_hop_endpoint_pop_type);
}
int sai_serialize_next_hop_endpoint_type(
    _Out_ char *buffer,
    _In_ sai_next_hop_endpoint_type_t next_hop_endpoint_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_endpoint_type_t, next_hop_endpoint_type);
}
int sai_serialize_next_hop_group_member_configured_role(
    _Out_ char *buffer,
    _In_ sai_next_hop_group_member_configured_role_t next_hop_group_member_configured_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_member_configured_role_t, next_hop_group_member_configured_role);
}
int sai_serialize_next_hop_group_member_observed_role(
    _Out_ char *buffer,
    _In_ sai_next_hop_group_member_observed_role_t next_hop_group_member_observed_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_member_observed_role_t, next_hop_group_member_observed_role);
}
int sai_serialize_next_hop_group_type(
    _Out_ char *buffer,
    _In_ sai_next_hop_group_type_t next_hop_group_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_type_t, next_hop_group_type);
}
int sai_serialize_next_hop_type(
    _Out_ char *buffer,
    _In_ sai_next_hop_type_t next_hop_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_type_t, next_hop_type);
}
int sai_serialize_npm_encapsulation_type(
    _Out_ char *buffer,
    _In_ sai_npm_encapsulation_type_t npm_encapsulation_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_encapsulation_type_t, npm_encapsulation_type);
}
int sai_serialize_npm_pkt_tx_mode(
    _Out_ char *buffer,
    _In_ sai_npm_pkt_tx_mode_t npm_pkt_tx_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_pkt_tx_mode_t, npm_pkt_tx_mode);
}
int sai_serialize_npm_session_role(
    _Out_ char *buffer,
    _In_ sai_npm_session_role_t npm_session_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_session_role_t, npm_session_role);
}
int sai_serialize_npm_session_stats(
    _Out_ char *buffer,
    _In_ sai_npm_session_stats_t npm_session_stats)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_session_stats_t, npm_session_stats);
}
int sai_serialize_object_type(
    _Out_ char *buffer,
    _In_ sai_object_type_t object_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_object_type_t, object_type);
}
int sai_serialize_out_drop_reason(
    _Out_ char *buffer,
    _In_ sai_out_drop_reason_t out_drop_reason)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_out_drop_reason_t, out_drop_reason);
}
int sai_serialize_outseg_exp_mode(
    _Out_ char *buffer,
    _In_ sai_outseg_exp_mode_t outseg_exp_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_exp_mode_t, outseg_exp_mode);
}
int sai_serialize_outseg_ttl_mode(
    _Out_ char *buffer,
    _In_ sai_outseg_ttl_mode_t outseg_ttl_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_ttl_mode_t, outseg_ttl_mode);
}
int sai_serialize_outseg_type(
    _Out_ char *buffer,
    _In_ sai_outseg_type_t outseg_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_type_t, outseg_type);
}
int sai_serialize_packet_action(
    _Out_ char *buffer,
    _In_ sai_packet_action_t packet_action)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_action_t, packet_action);
}
int sai_serialize_packet_color(
    _Out_ char *buffer,
    _In_ sai_packet_color_t packet_color)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_color_t, packet_color);
}
int sai_serialize_packet_vlan(
    _Out_ char *buffer,
    _In_ sai_packet_vlan_t packet_vlan)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_vlan_t, packet_vlan);
}
int sai_serialize_policer_color_source(
    _Out_ char *buffer,
    _In_ sai_policer_color_source_t policer_color_source)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_color_source_t, policer_color_source);
}
int sai_serialize_policer_mode(
    _Out_ char *buffer,
    _In_ sai_policer_mode_t policer_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_mode_t, policer_mode);
}
int sai_serialize_policer_stat(
    _Out_ char *buffer,
    _In_ sai_policer_stat_t policer_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_stat_t, policer_stat);
}
int sai_serialize_port_breakout_mode_type(
    _Out_ char *buffer,
    _In_ sai_port_breakout_mode_type_t port_breakout_mode_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_breakout_mode_type_t, port_breakout_mode_type);
}
int sai_serialize_port_err_status(
    _Out_ char *buffer,
    _In_ sai_port_err_status_t port_err_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_err_status_t, port_err_status);
}
int sai_serialize_port_fec_mode(
    _Out_ char *buffer,
    _In_ sai_port_fec_mode_t port_fec_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_fec_mode_t, port_fec_mode);
}
int sai_serialize_port_flow_control_mode(
    _Out_ char *buffer,
    _In_ sai_port_flow_control_mode_t port_flow_control_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_flow_control_mode_t, port_flow_control_mode);
}
int sai_serialize_port_interface_type(
    _Out_ char *buffer,
    _In_ sai_port_interface_type_t port_interface_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_interface_type_t, port_interface_type);
}
int sai_serialize_port_internal_loopback_mode(
    _Out_ char *buffer,
    _In_ sai_port_internal_loopback_mode_t port_internal_loopback_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_internal_loopback_mode_t, port_internal_loopback_mode);
}
int sai_serialize_port_link_training_failure_status(
    _Out_ char *buffer,
    _In_ sai_port_link_training_failure_status_t port_link_training_failure_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_link_training_failure_status_t, port_link_training_failure_status);
}
int sai_serialize_port_link_training_rx_status(
    _Out_ char *buffer,
    _In_ sai_port_link_training_rx_status_t port_link_training_rx_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_link_training_rx_status_t, port_link_training_rx_status);
}
int sai_serialize_port_media_type(
    _Out_ char *buffer,
    _In_ sai_port_media_type_t port_media_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_media_type_t, port_media_type);
}
int sai_serialize_port_oper_status(
    _Out_ char *buffer,
    _In_ sai_port_oper_status_t port_oper_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_oper_status_t, port_oper_status);
}
int sai_serialize_port_pool_stat(
    _Out_ char *buffer,
    _In_ sai_port_pool_stat_t port_pool_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_pool_stat_t, port_pool_stat);
}
int sai_serialize_port_prbs_config(
    _Out_ char *buffer,
    _In_ sai_port_prbs_config_t port_prbs_config)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_prbs_config_t, port_prbs_config);
}
int sai_serialize_port_priority_flow_control_mode(
    _Out_ char *buffer,
    _In_ sai_port_priority_flow_control_mode_t port_priority_flow_control_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_priority_flow_control_mode_t, port_priority_flow_control_mode);
}
int sai_serialize_port_ptp_mode(
    _Out_ char *buffer,
    _In_ sai_port_ptp_mode_t port_ptp_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_ptp_mode_t, port_ptp_mode);
}
int sai_serialize_port_stat(
    _Out_ char *buffer,
    _In_ sai_port_stat_t port_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_stat_t, port_stat);
}
int sai_serialize_port_type(
    _Out_ char *buffer,
    _In_ sai_port_type_t port_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_type_t, port_type);
}
int sai_serialize_ptp_device_type(
    _Out_ char *buffer,
    _In_ sai_ptp_device_type_t ptp_device_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_device_type_t, ptp_device_type);
}
int sai_serialize_ptp_enable_based_type(
    _Out_ char *buffer,
    _In_ sai_ptp_enable_based_type_t ptp_enable_based_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_enable_based_type_t, ptp_enable_based_type);
}
int sai_serialize_ptp_tod_interface_format_type(
    _Out_ char *buffer,
    _In_ sai_ptp_tod_interface_format_type_t ptp_tod_interface_format_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_tod_interface_format_type_t, ptp_tod_interface_format_type);
}
int sai_serialize_ptp_tod_intf_mode(
    _Out_ char *buffer,
    _In_ sai_ptp_tod_intf_mode_t ptp_tod_intf_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_tod_intf_mode_t, ptp_tod_intf_mode);
}
int sai_serialize_qos_map_type(
    _Out_ char *buffer,
    _In_ sai_qos_map_type_t qos_map_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_qos_map_type_t, qos_map_type);
}
int sai_serialize_queue_pfc_deadlock_event_type(
    _Out_ char *buffer,
    _In_ sai_queue_pfc_deadlock_event_type_t queue_pfc_deadlock_event_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_pfc_deadlock_event_type_t, queue_pfc_deadlock_event_type);
}
int sai_serialize_queue_stat(
    _Out_ char *buffer,
    _In_ sai_queue_stat_t queue_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_stat_t, queue_stat);
}
int sai_serialize_queue_type(
    _Out_ char *buffer,
    _In_ sai_queue_type_t queue_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_type_t, queue_type);
}
int sai_serialize_router_interface_stat(
    _Out_ char *buffer,
    _In_ sai_router_interface_stat_t router_interface_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_router_interface_stat_t, router_interface_stat);
}
int sai_serialize_router_interface_type(
    _Out_ char *buffer,
    _In_ sai_router_interface_type_t router_interface_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_router_interface_type_t, router_interface_type);
}
int sai_serialize_samplepacket_mode(
    _Out_ char *buffer,
    _In_ sai_samplepacket_mode_t samplepacket_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_samplepacket_mode_t, samplepacket_mode);
}
int sai_serialize_samplepacket_type(
    _Out_ char *buffer,
    _In_ sai_samplepacket_type_t samplepacket_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_samplepacket_type_t, samplepacket_type);
}
int sai_serialize_scheduling_type(
    _Out_ char *buffer,
    _In_ sai_scheduling_type_t scheduling_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_scheduling_type_t, scheduling_type);
}
int sai_serialize_segmentroute_sidlist_type(
    _Out_ char *buffer,
    _In_ sai_segmentroute_sidlist_type_t segmentroute_sidlist_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_segmentroute_sidlist_type_t, segmentroute_sidlist_type);
}
int sai_serialize_signal_degrade_status(
    _Out_ char *buffer,
    _In_ sai_signal_degrade_status_t signal_degrade_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_signal_degrade_status_t, signal_degrade_status);
}
int sai_serialize_stats_mode(
    _Out_ char *buffer,
    _In_ sai_stats_mode_t stats_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_stats_mode_t, stats_mode);
}
int sai_serialize_status(
    _Out_ char *buffer,
    _In_ sai_status_t status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_status_t, status);
}
int sai_serialize_stp_port_state(
    _Out_ char *buffer,
    _In_ sai_stp_port_state_t stp_port_state)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_stp_port_state_t, stp_port_state);
}
//int sai_serialize_switch_attr_extensions(
//    _Out_ char *buffer,
//    _In_ sai_switch_attr_extensions_t switch_attr_extensions)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_attr_extensions_t, switch_attr_extensions);
//}
int sai_serialize_switch_firmware_load_method(
    _Out_ char *buffer,
    _In_ sai_switch_firmware_load_method_t switch_firmware_load_method)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_firmware_load_method_t, switch_firmware_load_method);
}
int sai_serialize_switch_firmware_load_type(
    _Out_ char *buffer,
    _In_ sai_switch_firmware_load_type_t switch_firmware_load_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_firmware_load_type_t, switch_firmware_load_type);
}
int sai_serialize_switch_hardware_access_bus(
    _Out_ char *buffer,
    _In_ sai_switch_hardware_access_bus_t switch_hardware_access_bus)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_hardware_access_bus_t, switch_hardware_access_bus);
}
int sai_serialize_switch_mcast_snooping_capability(
    _Out_ char *buffer,
    _In_ sai_switch_mcast_snooping_capability_t switch_mcast_snooping_capability)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_mcast_snooping_capability_t, switch_mcast_snooping_capability);
}
//int sai_serialize_switch_notification_type(
//    _Out_ char *buffer,
//    _In_ sai_switch_notification_type_t switch_notification_type)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_notification_type_t, switch_notification_type);
//}
int sai_serialize_switch_oper_status(
    _Out_ char *buffer,
    _In_ sai_switch_oper_status_t switch_oper_status)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_oper_status_t, switch_oper_status);
}
int sai_serialize_switch_restart_type(
    _Out_ char *buffer,
    _In_ sai_switch_restart_type_t switch_restart_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_restart_type_t, switch_restart_type);
}
int sai_serialize_switch_stat(
    _Out_ char *buffer,
    _In_ sai_switch_stat_t switch_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_stat_t, switch_stat);
}
int sai_serialize_switch_switching_mode(
    _Out_ char *buffer,
    _In_ sai_switch_switching_mode_t switch_switching_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_switching_mode_t, switch_switching_mode);
}
int sai_serialize_switch_type(
    _Out_ char *buffer,
    _In_ sai_switch_type_t switch_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_type_t, switch_type);
}
int sai_serialize_system_port_type(
    _Out_ char *buffer,
    _In_ sai_system_port_type_t system_port_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_system_port_type_t, system_port_type);
}
//int sai_serialize_table_bitmap_classification_entry_action(
//    _Out_ char *buffer,
//    _In_ sai_table_bitmap_classification_entry_action_t table_bitmap_classification_entry_action)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_bitmap_classification_entry_action_t, table_bitmap_classification_entry_action);
//}
//int sai_serialize_table_bitmap_classification_entry_stat(
//    _Out_ char *buffer,
//    _In_ sai_table_bitmap_classification_entry_stat_t table_bitmap_classification_entry_stat)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_bitmap_classification_entry_stat_t, table_bitmap_classification_entry_stat);
//}
//int sai_serialize_table_bitmap_router_entry_action(
//    _Out_ char *buffer,
//    _In_ sai_table_bitmap_router_entry_action_t table_bitmap_router_entry_action)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_bitmap_router_entry_action_t, table_bitmap_router_entry_action);
//}
//int sai_serialize_table_bitmap_router_entry_stat(
//    _Out_ char *buffer,
//    _In_ sai_table_bitmap_router_entry_stat_t table_bitmap_router_entry_stat)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_bitmap_router_entry_stat_t, table_bitmap_router_entry_stat);
//}
//int sai_serialize_table_meta_tunnel_entry_action(
//    _Out_ char *buffer,
//    _In_ sai_table_meta_tunnel_entry_action_t table_meta_tunnel_entry_action)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_meta_tunnel_entry_action_t, table_meta_tunnel_entry_action);
//}
//int sai_serialize_table_meta_tunnel_entry_stat(
//    _Out_ char *buffer,
//    _In_ sai_table_meta_tunnel_entry_stat_t table_meta_tunnel_entry_stat)
//{
//    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_table_meta_tunnel_entry_stat_t, table_meta_tunnel_entry_stat);
//}
int sai_serialize_tam_bind_point_type(
    _Out_ char *buffer,
    _In_ sai_tam_bind_point_type_t tam_bind_point_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_bind_point_type_t, tam_bind_point_type);
}
int sai_serialize_tam_event_threshold_unit(
    _Out_ char *buffer,
    _In_ sai_tam_event_threshold_unit_t tam_event_threshold_unit)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_event_threshold_unit_t, tam_event_threshold_unit);
}
int sai_serialize_tam_event_type(
    _Out_ char *buffer,
    _In_ sai_tam_event_type_t tam_event_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_event_type_t, tam_event_type);
}
int sai_serialize_tam_int_presence_type(
    _Out_ char *buffer,
    _In_ sai_tam_int_presence_type_t tam_int_presence_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_int_presence_type_t, tam_int_presence_type);
}
int sai_serialize_tam_int_type(
    _Out_ char *buffer,
    _In_ sai_tam_int_type_t tam_int_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_int_type_t, tam_int_type);
}
int sai_serialize_tam_report_mode(
    _Out_ char *buffer,
    _In_ sai_tam_report_mode_t tam_report_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_report_mode_t, tam_report_mode);
}
int sai_serialize_tam_report_type(
    _Out_ char *buffer,
    _In_ sai_tam_report_type_t tam_report_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_report_type_t, tam_report_type);
}
int sai_serialize_tam_reporting_unit(
    _Out_ char *buffer,
    _In_ sai_tam_reporting_unit_t tam_reporting_unit)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_reporting_unit_t, tam_reporting_unit);
}
int sai_serialize_tam_tel_math_func_type(
    _Out_ char *buffer,
    _In_ sai_tam_tel_math_func_type_t tam_tel_math_func_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_tel_math_func_type_t, tam_tel_math_func_type);
}
int sai_serialize_tam_telemetry_type(
    _Out_ char *buffer,
    _In_ sai_tam_telemetry_type_t tam_telemetry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_telemetry_type_t, tam_telemetry_type);
}
int sai_serialize_tam_transport_auth_type(
    _Out_ char *buffer,
    _In_ sai_tam_transport_auth_type_t tam_transport_auth_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_transport_auth_type_t, tam_transport_auth_type);
}
int sai_serialize_tam_transport_type(
    _Out_ char *buffer,
    _In_ sai_tam_transport_type_t tam_transport_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_transport_type_t, tam_transport_type);
}
int sai_serialize_tlv_type(
    _Out_ char *buffer,
    _In_ sai_tlv_type_t tlv_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tlv_type_t, tlv_type);
}
int sai_serialize_tunnel_decap_ecn_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_decap_ecn_mode_t tunnel_decap_ecn_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_decap_ecn_mode_t, tunnel_decap_ecn_mode);
}
int sai_serialize_tunnel_dscp_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_dscp_mode_t tunnel_dscp_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_dscp_mode_t, tunnel_dscp_mode);
}
int sai_serialize_tunnel_encap_ecn_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_encap_ecn_mode_t tunnel_encap_ecn_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_encap_ecn_mode_t, tunnel_encap_ecn_mode);
}
int sai_serialize_tunnel_exp_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_exp_mode_t tunnel_exp_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_exp_mode_t, tunnel_exp_mode);
}
int sai_serialize_tunnel_map_type(
    _Out_ char *buffer,
    _In_ sai_tunnel_map_type_t tunnel_map_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_map_type_t, tunnel_map_type);
}
int sai_serialize_tunnel_mpls_pw_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_mpls_pw_mode_t tunnel_mpls_pw_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_mpls_pw_mode_t, tunnel_mpls_pw_mode);
}
int sai_serialize_tunnel_peer_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_peer_mode_t tunnel_peer_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_peer_mode_t, tunnel_peer_mode);
}
int sai_serialize_tunnel_stat(
    _Out_ char *buffer,
    _In_ sai_tunnel_stat_t tunnel_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_stat_t, tunnel_stat);
}
int sai_serialize_tunnel_term_table_entry_type(
    _Out_ char *buffer,
    _In_ sai_tunnel_term_table_entry_type_t tunnel_term_table_entry_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_term_table_entry_type_t, tunnel_term_table_entry_type);
}
int sai_serialize_tunnel_ttl_mode(
    _Out_ char *buffer,
    _In_ sai_tunnel_ttl_mode_t tunnel_ttl_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_ttl_mode_t, tunnel_ttl_mode);
}
int sai_serialize_tunnel_type(
    _Out_ char *buffer,
    _In_ sai_tunnel_type_t tunnel_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_type_t, tunnel_type);
}
int sai_serialize_twamp_encapsulation_type(
    _Out_ char *buffer,
    _In_ sai_twamp_encapsulation_type_t twamp_encapsulation_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_encapsulation_type_t, twamp_encapsulation_type);
}
int sai_serialize_twamp_mode(
    _Out_ char *buffer,
    _In_ sai_twamp_mode_t twamp_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_mode_t, twamp_mode);
}
int sai_serialize_twamp_pkt_tx_mode(
    _Out_ char *buffer,
    _In_ sai_twamp_pkt_tx_mode_t twamp_pkt_tx_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_pkt_tx_mode_t, twamp_pkt_tx_mode);
}
int sai_serialize_twamp_session_auth_mode(
    _Out_ char *buffer,
    _In_ sai_twamp_session_auth_mode_t twamp_session_auth_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_auth_mode_t, twamp_session_auth_mode);
}
int sai_serialize_twamp_session_role(
    _Out_ char *buffer,
    _In_ sai_twamp_session_role_t twamp_session_role)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_role_t, twamp_session_role);
}
int sai_serialize_twamp_session_stats(
    _Out_ char *buffer,
    _In_ sai_twamp_session_stats_t twamp_session_stats)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_stats_t, twamp_session_stats);
}
int sai_serialize_twamp_timestamp_format(
    _Out_ char *buffer,
    _In_ sai_twamp_timestamp_format_t twamp_timestamp_format)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_timestamp_format_t, twamp_timestamp_format);
}
int sai_serialize_udf_base(
    _Out_ char *buffer,
    _In_ sai_udf_base_t udf_base)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_udf_base_t, udf_base);
}
int sai_serialize_udf_group_type(
    _Out_ char *buffer,
    _In_ sai_udf_group_type_t udf_group_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_udf_group_type_t, udf_group_type);
}
int sai_serialize_vlan_flood_control_type(
    _Out_ char *buffer,
    _In_ sai_vlan_flood_control_type_t vlan_flood_control_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_flood_control_type_t, vlan_flood_control_type);
}
int sai_serialize_vlan_mcast_lookup_key_type(
    _Out_ char *buffer,
    _In_ sai_vlan_mcast_lookup_key_type_t vlan_mcast_lookup_key_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_mcast_lookup_key_type_t, vlan_mcast_lookup_key_type);
}
int sai_serialize_vlan_stat(
    _Out_ char *buffer,
    _In_ sai_vlan_stat_t vlan_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_stat_t, vlan_stat);
}
int sai_serialize_vlan_tagging_mode(
    _Out_ char *buffer,
    _In_ sai_vlan_tagging_mode_t vlan_tagging_mode)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_tagging_mode_t, vlan_tagging_mode);
}
int sai_serialize_y1731_meg_type(
    _Out_ char *buffer,
    _In_ sai_y1731_meg_type_t y1731_meg_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_meg_type_t, y1731_meg_type);
}
int sai_serialize_y1731_session_ccm_period(
    _Out_ char *buffer,
    _In_ sai_y1731_session_ccm_period_t y1731_session_ccm_period)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_ccm_period_t, y1731_session_ccm_period);
}
int sai_serialize_y1731_session_direction(
    _Out_ char *buffer,
    _In_ sai_y1731_session_direction_t y1731_session_direction)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_direction_t, y1731_session_direction);
}
int sai_serialize_y1731_session_lm_type(
    _Out_ char *buffer,
    _In_ sai_y1731_session_lm_type_t y1731_session_lm_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_lm_type_t, y1731_session_lm_type);
}
int sai_serialize_y1731_session_notify_event_type(
    _Out_ char *buffer,
    _In_ sai_y1731_session_notify_event_type_t y1731_session_notify_event_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_notify_event_type_t, y1731_session_notify_event_type);
}
int sai_serialize_y1731_session_perf_monitor_offload_type(
    _Out_ char *buffer,
    _In_ sai_y1731_session_perf_monitor_offload_type_t y1731_session_perf_monitor_offload_type)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_perf_monitor_offload_type_t, y1731_session_perf_monitor_offload_type);
}
int sai_serialize_y1731_session_stat(
    _Out_ char *buffer,
    _In_ sai_y1731_session_stat_t y1731_session_stat)
{
    return sai_serialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_stat_t, y1731_session_stat);
}

/* Emit macros */

#define EMIT(x)        buf += sprintf(buf, x)
#define EMIT_QUOTE     EMIT("\"")
#define EMIT_KEY(k)    EMIT("" k ":")
#define EMIT_NEXT_KEY(k) { EMIT(","); EMIT_KEY(k); }
#define EMIT_CHECK(expr, suffix) {                                 \
    ret = (expr);                                                  \
    if (ret < 0) {                                                 \
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize " #suffix "");      \
        return SAI_SERIALIZE_ERROR; }                              \
    buf += ret; }
#define EMIT_QUOTE_CHECK(expr, suffix) {\
    EMIT_QUOTE; EMIT_CHECK(expr, suffix); EMIT_QUOTE; }

/* Serialize structs */

int sai_serialize_acl_action_data(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_acl_action_data_t *acl_action_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT_KEY("enable");

    EMIT_CHECK(sai_serialize_bool(buf, acl_action_data->enable), bool);

    if (acl_action_data->enable == true)
    {
        EMIT_NEXT_KEY("parameter");

        EMIT_CHECK(sai_serialize_acl_action_parameter(buf, meta, &acl_action_data->parameter), acl_action_parameter);
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_acl_capability(
    _Out_ char *buf,
    _In_ sai_acl_capability_t *acl_capability)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("is_action_list_mandatory");

    EMIT_CHECK(sai_serialize_bool(buf, acl_capability->is_action_list_mandatory), bool);

    EMIT_NEXT_KEY("action_list");

    EMIT_CHECK(sai_serialize_enum_list(buf, &ctc_sai_metadata_enum_sai_acl_action_type_t, &acl_capability->action_list), enum_list);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_acl_field_data(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_acl_field_data_t *acl_field_data)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "enable:");

    ret = sai_serialize_bool(buf, acl_field_data->enable);
    buf += ret;

    if (acl_field_data->enable == true)
    {
        buf += sal_sprintf(buf, ", data:");
        ret = sai_serialize_acl_field_data_data(buf, meta, &acl_field_data->data);
        buf += ret;
    }
    if (acl_field_data->enable == true)
    {
        buf += sal_sprintf(buf, ", mask:");
        ret = sai_serialize_acl_field_data_mask(buf, meta, &acl_field_data->mask);
        buf += ret;
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_acl_resource_list(
    _Out_ char *buf,
    _In_ sai_acl_resource_list_t *acl_resource_list)
{
#if 0
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "ListCount: %u\n", acl_resource_list->count);
    if (acl_resource_list->list == NULL || acl_resource_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        buf += sal_sprintf(buf, "ListData:  [");
        for (idx = 0; idx < acl_resource_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            EMIT_CHECK(sai_serialize_acl_resource(buf, &acl_resource_list->list[idx]), acl_resource);
        }
        buf += sal_sprintf(buf, "]");
    }
    buf += sal_sprintf(buf, "\n");

    return (int)(buf - begin_buf);
#endif
    return 0;
}
int sai_serialize_acl_resource(
    _Out_ char *buf,
    _In_ sai_acl_resource_t *acl_resource)
{
#if 0
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("stage");

    EMIT_QUOTE_CHECK(sai_serialize_acl_stage(buf, acl_resource->stage), acl_stage);

    EMIT_NEXT_KEY("bind_point");

    EMIT_QUOTE_CHECK(sai_serialize_acl_bind_point_type(buf, acl_resource->bind_point), acl_bind_point_type);

    EMIT_NEXT_KEY("avail_num");

    EMIT_CHECK(sai_serialize_uint32(buf, acl_resource->avail_num), uint32);

    EMIT("}");

    return (int)(buf - begin_buf);
#endif
    return 0;
}
int sai_serialize_attr_capability(
    _Out_ char *buf,
    _In_ sai_attr_capability_t *attr_capability)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("create_implemented");

    EMIT_CHECK(sai_serialize_bool(buf, attr_capability->create_implemented), bool);

    EMIT_NEXT_KEY("set_implemented");

    EMIT_CHECK(sai_serialize_bool(buf, attr_capability->set_implemented), bool);

    EMIT_NEXT_KEY("get_implemented");

    EMIT_CHECK(sai_serialize_bool(buf, attr_capability->get_implemented), bool);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_bfd_session_state_notification(
    _Out_ char *buf,
    _In_ sai_bfd_session_state_notification_t *bfd_session_state_notification)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("bfd_session_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, bfd_session_state_notification->bfd_session_id), object_id);

    EMIT_NEXT_KEY("session_state");

    EMIT_QUOTE_CHECK(sai_serialize_bfd_session_state(buf, bfd_session_state_notification->session_state), bfd_session_state);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_bool_list(
    _Out_ char *buf,
    _In_ sai_bool_list_t *bool_list)
{
    char *begin_buf = buf;
    int ret;

    if (bool_list->list == NULL || bool_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < bool_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_bool(buf, bool_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_captured_timespec(
    _Out_ char *buf,
    _In_ sai_captured_timespec_t *captured_timespec)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "%s", "timestamp:");
    EMIT_CHECK(sai_serialize_timespec(buf, &captured_timespec->timestamp), timespec);

    buf += sal_sprintf(buf, "%s", ", secquence_id:");
    EMIT_CHECK(sai_serialize_uint16(buf, captured_timespec->secquence_id), uint16);

    buf += sal_sprintf(buf, "%s", ", port_id:");
    EMIT_CHECK(sai_serialize_uint64(buf, captured_timespec->port_id), uint64);

    return (int)(buf - begin_buf);
}
int sai_serialize_fabric_port_reachability(
    _Out_ char *buf,
    _In_ sai_fabric_port_reachability_t *fabric_port_reachability)
{
    char *begin_buf = buf;
    int ret;

    EMIT_KEY("switch_id:");

    EMIT_CHECK(sai_serialize_uint32(buf, fabric_port_reachability->switch_id), uint32);

    EMIT_NEXT_KEY("reachable:");

    EMIT_CHECK(sai_serialize_bool(buf, fabric_port_reachability->reachable), bool);

    return (int)(buf - begin_buf);
}
int sai_serialize_fdb_entry(
    _Out_ char *buf,
    _In_ sai_fdb_entry_t *fdb_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, fdb_entry->switch_id), object_id);

    EMIT_NEXT_KEY("mac_address");

    EMIT_QUOTE_CHECK(sai_serialize_mac(buf, fdb_entry->mac_address), mac);

    EMIT_NEXT_KEY("bv_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, fdb_entry->bv_id), object_id);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_fdb_event_notification_data(
    _Out_ char *buf,
    _In_ sai_fdb_event_notification_data_t *fdb_event_notification_data)
{
#if 0
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("event_type");

    EMIT_QUOTE_CHECK(sai_serialize_fdb_event(buf, fdb_event_notification_data->event_type), fdb_event);

    EMIT_NEXT_KEY("fdb_entry");

    EMIT_CHECK(sai_serialize_fdb_entry(buf, &fdb_event_notification_data->fdb_entry), fdb_entry);

    EMIT_NEXT_KEY("attr_count");

    EMIT_CHECK(sai_serialize_uint32(buf, fdb_event_notification_data->attr_count), uint32);

    EMIT_NEXT_KEY("attr");

    if (fdb_event_notification_data->attr == NULL || fdb_event_notification_data->attr_count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < fdb_event_notification_data->attr_count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            ctc_sai_attr_metadata_t *meta =
                sai_metadata_get_attr_metadata(SAI_OBJECT_TYPE_FDB_ENTRY, fdb_event_notification_data->attr[idx].id);

            EMIT_CHECK(sai_serialize_attribute(buf, meta, &fdb_event_notification_data->attr[idx]), attribute);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
#endif

    return 0;
}
int sai_serialize_hmac(
    _Out_ char *buf,
    _In_ sai_hmac_t *hmac)
{
    char *begin_buf = buf;
    int ret;

    EMIT_KEY("key_id");

    EMIT_CHECK(sai_serialize_uint32(buf, hmac->key_id), uint32);

    EMIT_NEXT_KEY("hmac");

    if (hmac->hmac == NULL || 8 == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_hex_uint32(buf, hmac->hmac[idx]), uint32);
        }

        EMIT("]");
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_inseg_entry(
    _Out_ char *buf,
    _In_ sai_inseg_entry_t *inseg_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, inseg_entry->switch_id), object_id);

    EMIT_NEXT_KEY("label");

    EMIT_CHECK(sai_serialize_uint32(buf, inseg_entry->label), uint32);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_ip_address_list(
    _Out_ char *buf,
    _In_ sai_ip_address_list_t *ip_address_list)
{
    char *begin_buf = buf;
    int ret;

    if (ip_address_list->list == NULL || ip_address_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < ip_address_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_ip_address(buf, &ip_address_list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize ip_address_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_ipmc_entry(
    _Out_ char *buf,
    _In_ sai_ipmc_entry_t *ipmc_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, ipmc_entry->switch_id), object_id);

    EMIT_NEXT_KEY("vr_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, ipmc_entry->vr_id), object_id);

    EMIT_NEXT_KEY("type");

    EMIT_QUOTE_CHECK(sai_serialize_ipmc_entry_type(buf, ipmc_entry->type), ipmc_entry_type);

    EMIT_NEXT_KEY("destination");

    EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &ipmc_entry->destination), ip_address);

    EMIT_NEXT_KEY("source");

    EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &ipmc_entry->source), ip_address);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_l2mc_entry(
    _Out_ char *buf,
    _In_ sai_l2mc_entry_t *l2mc_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, l2mc_entry->switch_id), object_id);

    EMIT_NEXT_KEY("bv_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, l2mc_entry->bv_id), object_id);

    EMIT_NEXT_KEY("type");

    EMIT_QUOTE_CHECK(sai_serialize_l2mc_entry_type(buf, l2mc_entry->type), l2mc_entry_type);

    EMIT_NEXT_KEY("destination");

    EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &l2mc_entry->destination), ip_address);

    EMIT_NEXT_KEY("source");

    EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &l2mc_entry->source), ip_address);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_map_list(
    _Out_ char *buf,
    _In_ sai_map_list_t *map_list)
{
    char *begin_buf = buf;
    int ret;

    if (map_list->list == NULL || map_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < map_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_map(buf, &map_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_map(
    _Out_ char *buf,
    _In_ sai_map_t *map)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("key");

    EMIT_CHECK(sai_serialize_uint32(buf, map->key), uint32);

    EMIT_NEXT_KEY("value");

    EMIT_CHECK(sai_serialize_int32(buf, map->value), int32);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_mcast_fdb_entry(
    _Out_ char *buf,
    _In_ sai_mcast_fdb_entry_t *mcast_fdb_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, mcast_fdb_entry->switch_id), object_id);

    EMIT_NEXT_KEY("mac_address");

    EMIT_QUOTE_CHECK(sai_serialize_mac(buf, mcast_fdb_entry->mac_address), mac);

    EMIT_NEXT_KEY("bv_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, mcast_fdb_entry->bv_id), object_id);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_buffer_event(
    _Out_ char *buf,
    _In_ sai_monitor_buffer_event_t *monitor_buffer_event)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("buffer_monitor_event_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_buffer_event->buffer_monitor_event_port), object_id);

    EMIT_NEXT_KEY("buffer_monitor_event_total_cnt");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_buffer_event->buffer_monitor_event_total_cnt), uint32);

    EMIT_NEXT_KEY("buffer_monitor_event_port_unicast_cnt");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_buffer_event->buffer_monitor_event_port_unicast_cnt), uint32);

    EMIT_NEXT_KEY("buffer_monitor_event_port_multicast_cnt");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_buffer_event->buffer_monitor_event_port_multicast_cnt), uint32);

    EMIT_NEXT_KEY("buffer_monitor_event_state");

    EMIT_CHECK(sai_serialize_uint8(buf, monitor_buffer_event->buffer_monitor_event_state), uint8);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_buffer_notification_data(
    _Out_ char *buf,
    _In_ sai_monitor_buffer_notification_data_t *monitor_buffer_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("monitor_buffer_monitor_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_buffer_notification_data->monitor_buffer_monitor_id), object_id);

    EMIT_NEXT_KEY("buffer_monitor_message_type");

    EMIT_QUOTE_CHECK(sai_serialize_buffer_monitor_message_type(buf, monitor_buffer_notification_data->buffer_monitor_message_type), buffer_monitor_message_type);

    EMIT_NEXT_KEY("buffer_monitor_based_on_type");

    EMIT_QUOTE_CHECK(sai_serialize_buffer_monitor_based_on_type(buf, monitor_buffer_notification_data->buffer_monitor_based_on_type), buffer_monitor_based_on_type);

    EMIT_NEXT_KEY("u");

    EMIT_CHECK(sai_serialize_monitor_buffer_data(buf, monitor_buffer_notification_data->buffer_monitor_message_type, &monitor_buffer_notification_data->u), monitor_buffer_data);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_buffer_stats(
    _Out_ char *buf,
    _In_ sai_monitor_buffer_stats_t *monitor_buffer_stats)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("buffer_monitor_stats_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_buffer_stats->buffer_monitor_stats_port), object_id);

    EMIT_NEXT_KEY("buffer_monitor_stats_direction");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_buffer_stats->buffer_monitor_stats_direction), uint32);

    EMIT_NEXT_KEY("buffer_monitor_stats_port_cnt");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_buffer_stats->buffer_monitor_stats_port_cnt), uint32);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_latency_event(
    _Out_ char *buf,
    _In_ sai_monitor_latency_event_t *monitor_latency_event)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("latency_monitor_event_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_latency_event->latency_monitor_event_port), object_id);

    EMIT_NEXT_KEY("latency_monitor_event_latency");

    EMIT_CHECK(sai_serialize_uint64(buf, monitor_latency_event->latency_monitor_event_latency), uint64);

    EMIT_NEXT_KEY("latency_monitor_event_level");

    EMIT_CHECK(sai_serialize_uint8(buf, monitor_latency_event->latency_monitor_event_level), uint8);

    EMIT_NEXT_KEY("latency_monitor_event_state");

    EMIT_CHECK(sai_serialize_uint8(buf, monitor_latency_event->latency_monitor_event_state), uint8);

    EMIT_NEXT_KEY("latency_monitor_event_source_port");

    EMIT_CHECK(sai_serialize_uint32(buf, monitor_latency_event->latency_monitor_event_source_port), uint32);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_latency_notification_data(
    _Out_ char *buf,
    _In_ sai_monitor_latency_notification_data_t *monitor_latency_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("monitor_latency_monitor_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_latency_notification_data->monitor_latency_monitor_id), object_id);

    EMIT_NEXT_KEY("latency_monitor_message_type");

    EMIT_QUOTE_CHECK(sai_serialize_latency_monitor_message_type(buf, monitor_latency_notification_data->latency_monitor_message_type), latency_monitor_message_type);

    EMIT_NEXT_KEY("u");

    EMIT_CHECK(sai_serialize_monitor_latency_data(buf, monitor_latency_notification_data->latency_monitor_message_type, &monitor_latency_notification_data->u), monitor_latency_data);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_latency_stats(
    _Out_ char *buf,
    _In_ sai_monitor_latency_stats_t *monitor_latency_stats)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("latency_monitor_stats_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_latency_stats->latency_monitor_stats_port), object_id);

    EMIT_NEXT_KEY("latency_monitor_stats_level_cnt");

    if (monitor_latency_stats->latency_monitor_stats_level_cnt == NULL || 8 == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_uint32(buf, monitor_latency_stats->latency_monitor_stats_level_cnt[idx]), uint32);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_mburst_stats(
    _Out_ char *buf,
    _In_ sai_monitor_mburst_stats_t *monitor_mburst_stats)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("buffer_monitor_microburst_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, monitor_mburst_stats->buffer_monitor_microburst_port), object_id);

    EMIT_NEXT_KEY("buffer_monitor_microburst_threshold_cnt");

    if (monitor_mburst_stats->buffer_monitor_microburst_threshold_cnt == NULL || 8 == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_uint32(buf, monitor_mburst_stats->buffer_monitor_microburst_threshold_cnt[idx]), uint32);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_nat_entry_data(
    _Out_ char *buf,
    _In_ sai_nat_entry_data_t *nat_entry_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("key");

    EMIT_CHECK(sai_serialize_nat_entry_key(buf, &nat_entry_data->key), nat_entry_key);

    EMIT_NEXT_KEY("mask");

    EMIT_CHECK(sai_serialize_nat_entry_mask(buf, &nat_entry_data->mask), nat_entry_mask);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_nat_entry_key(
    _Out_ char *buf,
    _In_ sai_nat_entry_key_t *nat_entry_key)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("src_ip");

    EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, nat_entry_key->src_ip), ip4);

    EMIT_NEXT_KEY("dst_ip");

    EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, nat_entry_key->dst_ip), ip4);

    EMIT_NEXT_KEY("proto");

    EMIT_CHECK(sai_serialize_uint8(buf, nat_entry_key->proto), uint8);

    EMIT_NEXT_KEY("l4_src_port");

    EMIT_CHECK(sai_serialize_uint16(buf, nat_entry_key->l4_src_port), uint16);

    EMIT_NEXT_KEY("l4_dst_port");

    EMIT_CHECK(sai_serialize_uint16(buf, nat_entry_key->l4_dst_port), uint16);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_nat_entry_mask(
    _Out_ char *buf,
    _In_ sai_nat_entry_mask_t *nat_entry_mask)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("src_ip");

    EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, nat_entry_mask->src_ip), ip4);

    EMIT_NEXT_KEY("dst_ip");

    EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, nat_entry_mask->dst_ip), ip4);

    EMIT_NEXT_KEY("proto");

    EMIT_CHECK(sai_serialize_uint8(buf, nat_entry_mask->proto), uint8);

    EMIT_NEXT_KEY("l4_src_port");

    EMIT_CHECK(sai_serialize_uint16(buf, nat_entry_mask->l4_src_port), uint16);

    EMIT_NEXT_KEY("l4_dst_port");

    EMIT_CHECK(sai_serialize_uint16(buf, nat_entry_mask->l4_dst_port), uint16);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_nat_entry(
    _Out_ char *buf,
    _In_ sai_nat_entry_t *nat_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, nat_entry->switch_id), object_id);

    EMIT_NEXT_KEY("vr_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, nat_entry->vr_id), object_id);

    EMIT_NEXT_KEY("nat_type");

    EMIT_QUOTE_CHECK(sai_serialize_nat_type(buf, nat_entry->nat_type), nat_type);

    EMIT_NEXT_KEY("data");

    EMIT_CHECK(sai_serialize_nat_entry_data(buf, &nat_entry->data), nat_entry_data);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_neighbor_entry(
    _Out_ char *buf,
    _In_ sai_neighbor_entry_t *neighbor_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, neighbor_entry->switch_id), object_id);

    EMIT_NEXT_KEY("rif_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, neighbor_entry->rif_id), object_id);

    EMIT_NEXT_KEY("ip_address");

    EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &neighbor_entry->ip_address), ip_address);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_object_key(
    _Out_ char *buf,
    _In_ sai_object_type_t object_type,
    _In_ sai_object_key_t *object_key)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("key");

    EMIT_CHECK(sai_serialize_object_key_entry(buf, object_type, &object_key->key), object_key_entry);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_object_list(
    _Out_ char *buf,
    _In_ sai_object_list_t *object_list)
{
    char *begin_buf = buf;
    int ret;

    if (object_list->list == NULL || object_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < object_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            if (0 == idx%4 && 0 != idx)
            {
                buf += sal_sprintf(buf, "\n            ");
            }
            ret = sai_serialize_object_id(buf, object_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}

int sai_serialize_object_meta_key(
    _Out_ char *buf,
    _In_ ctc_sai_object_meta_key_t *object_meta_key)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("objecttype");

    EMIT_QUOTE_CHECK(sai_serialize_object_type(buf, object_meta_key->objecttype), object_type);

    EMIT_NEXT_KEY("objectkey");

    EMIT_CHECK(sai_serialize_object_key(buf, object_meta_key->objecttype, &object_meta_key->objectkey), object_key);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_packet_event_ptp_tx_notification_data(
    _Out_ char *buf,
    _In_ sai_packet_event_ptp_tx_notification_data_t *packet_event_ptp_tx_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("tx_port");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, packet_event_ptp_tx_notification_data->tx_port), object_id);

    EMIT_NEXT_KEY("msg_type");

    EMIT_CHECK(sai_serialize_uint8(buf, packet_event_ptp_tx_notification_data->msg_type), uint8);

    EMIT_NEXT_KEY("ptp_seq_id");

    EMIT_CHECK(sai_serialize_uint16(buf, packet_event_ptp_tx_notification_data->ptp_seq_id), uint16);

    EMIT_NEXT_KEY("tx_timestamp");

    EMIT_CHECK(sai_serialize_timespec(buf, &packet_event_ptp_tx_notification_data->tx_timestamp), timespec);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_port_err_status_list(
    _Out_ char *buf,
    _In_ sai_port_err_status_list_t *port_err_status_list)
{
    char *begin_buf = buf;
    int ret;

    if (port_err_status_list->list == NULL || port_err_status_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < port_err_status_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_port_err_status(buf, port_err_status_list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize port_err_status_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_port_eye_values_list(
    _Out_ char *buf,
    _In_ sai_port_eye_values_list_t *port_eye_values_list)
{
    char *begin_buf = buf;
    int ret;

    if (port_eye_values_list->list == NULL || port_eye_values_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < port_eye_values_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_port_lane_eye_values(buf, &port_eye_values_list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize port_eye_values_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_port_lane_eye_values(
    _Out_ char *buf,
    _In_ sai_port_lane_eye_values_t *port_lane_eye_values)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("lane");

    EMIT_CHECK(sai_serialize_uint32(buf, port_lane_eye_values->lane), uint32);

    EMIT_NEXT_KEY("left");

    EMIT_CHECK(sai_serialize_int32(buf, port_lane_eye_values->left), int32);

    EMIT_NEXT_KEY("right");

    EMIT_CHECK(sai_serialize_int32(buf, port_lane_eye_values->right), int32);

    EMIT_NEXT_KEY("up");

    EMIT_CHECK(sai_serialize_int32(buf, port_lane_eye_values->up), int32);

    EMIT_NEXT_KEY("down");

    EMIT_CHECK(sai_serialize_int32(buf, port_lane_eye_values->down), int32);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_port_oper_status_notification(
    _Out_ char *buf,
    _In_ sai_port_oper_status_notification_t *port_oper_status_notification)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("port_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, port_oper_status_notification->port_id), object_id);

    EMIT_NEXT_KEY("port_state");

    EMIT_QUOTE_CHECK(sai_serialize_port_oper_status(buf, port_oper_status_notification->port_state), port_oper_status);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_port_sd_notification(
    _Out_ char *buf,
    _In_ sai_port_sd_notification_t *port_sd_notification)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("port_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, port_sd_notification->port_id), object_id);

    EMIT_NEXT_KEY("sd_status");

    EMIT_QUOTE_CHECK(sai_serialize_signal_degrade_status(buf, port_sd_notification->sd_status), signal_degrade_status);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_qos_map_list(
    _Out_ char *buf,
    _In_ sai_qos_map_list_t *qos_map_list)
{
    char *begin_buf = buf;
    int ret;

    if (qos_map_list->list == NULL || qos_map_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < qos_map_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_qos_map(buf, &qos_map_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_qos_map_params(
    _Out_ char *buf,
    _In_ sai_qos_map_params_t *qos_map_params)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("tc");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->tc), uint8);

    EMIT_NEXT_KEY("dscp");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->dscp), uint8);

    EMIT_NEXT_KEY("dot1p");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->dot1p), uint8);

    EMIT_NEXT_KEY("prio");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->prio), uint8);

    EMIT_NEXT_KEY("pg");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->pg), uint8);

    EMIT_NEXT_KEY("queue_index");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->queue_index), uint8);

    EMIT_NEXT_KEY("color");

    EMIT_QUOTE_CHECK(sai_serialize_packet_color(buf, qos_map_params->color), packet_color);

    EMIT_NEXT_KEY("mpls_exp");

    EMIT_CHECK(sai_serialize_uint8(buf, qos_map_params->mpls_exp), uint8);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_qos_map(
    _Out_ char *buf,
    _In_ sai_qos_map_t *qos_map)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("key");

    EMIT_CHECK(sai_serialize_qos_map_params(buf, &qos_map->key), qos_map_params);

    EMIT_NEXT_KEY("value");

    EMIT_CHECK(sai_serialize_qos_map_params(buf, &qos_map->value), qos_map_params);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_queue_deadlock_notification_data(
    _Out_ char *buf,
    _In_ sai_queue_deadlock_notification_data_t *queue_deadlock_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("queue_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, queue_deadlock_notification_data->queue_id), object_id);

    EMIT_NEXT_KEY("event");

    EMIT_QUOTE_CHECK(sai_serialize_queue_pfc_deadlock_event_type(buf, queue_deadlock_notification_data->event), queue_pfc_deadlock_event_type);

    EMIT_NEXT_KEY("app_managed_recovery");

    EMIT_CHECK(sai_serialize_bool(buf, queue_deadlock_notification_data->app_managed_recovery), bool);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_route_entry(
    _Out_ char *buf,
    _In_ sai_route_entry_t *route_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, route_entry->switch_id), object_id);

    EMIT_NEXT_KEY("vr_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, route_entry->vr_id), object_id);

    EMIT_NEXT_KEY("destination");

    EMIT_QUOTE_CHECK(sai_serialize_ip_prefix(buf, &route_entry->destination), ip_prefix);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_s16_list(
    _Out_ char *buf,
    _In_ sai_s16_list_t *s16_list)
{
    char *begin_buf = buf;
    int ret;

    if (s16_list->list == NULL || s16_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < s16_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            if (0 == idx%10 && 0 != idx)
            {
                buf += sal_sprintf(buf, "\n            ");
            }
            ret = sai_serialize_int16(buf, s16_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_s32_list(
    _Out_ char *buf,
    _In_ sai_s32_list_t *s32_list)
{
    char *begin_buf = buf;
    int ret;

    if (s32_list->list == NULL || s32_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < s32_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            if (0 == idx%10 && 0 != idx)
            {
                buf += sal_sprintf(buf, "\n            ");
            }
            ret = sai_serialize_int32(buf, s32_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_s32_range(
    _Out_ char *buf,
    _In_ sai_s32_range_t *s32_range)
{
    char *begin_buf = buf;
    int ret;

    ret = sai_serialize_int32(buf, s32_range->min);
    buf += ret;
    buf += sal_sprintf(buf, ",");
    ret = sai_serialize_int32(buf, s32_range->max);
    buf += ret;

    return (int)(buf - begin_buf);
}
int sai_serialize_s8_list(
    _Out_ char *buf,
    _In_ sai_s8_list_t *s8_list)
{
    char *begin_buf = buf;
    int ret;

    if (s8_list->list == NULL || s8_list->count == 0)
    {
        EMIT("null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < s8_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_int8(buf, s8_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_segment_list(
    _Out_ char *buf,
    _In_ sai_segment_list_t *segment_list)
{
    char *begin_buf = buf;
    int ret;

    if (segment_list->list == NULL || segment_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < segment_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_ip6(buf, segment_list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize segment_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_system_port_config_list(
    _Out_ char *buf,
    _In_ sai_system_port_config_list_t *system_port_config_list)
{
    char *begin_buf = buf;
    int ret;

    if (system_port_config_list->list == NULL || system_port_config_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        sal_sprintf(buf, "%s", "[");
        for (idx = 0; idx < system_port_config_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, "\n            [");
            }
            ret = sai_serialize_system_port_config(buf, &system_port_config_list->list[idx]);
            if (ret < 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to serialize system_port_config_list");
                return SAI_SERIALIZE_ERROR;
            }
            buf += ret;
            if (idx != system_port_config_list->count-1)
            {
                sal_sprintf(buf, "%s", "],");
            }
            else
            {
                sal_sprintf(buf, "%s", "]");
            }
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_system_port_config(
    _Out_ char *buf,
    _In_ sai_system_port_config_t *system_port_config)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "%s", "port_id:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->port_id), uint32);

    buf += sal_sprintf(buf, "%s", ", attached_switch_id:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->attached_switch_id), uint32);

    buf += sal_sprintf(buf, "%s", ", attached_core_index:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->attached_core_index), uint32);

    buf += sal_sprintf(buf, "%s", ", attached_core_port_index:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->attached_core_port_index), uint32);

    buf += sal_sprintf(buf, "%s", ", speed:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->speed), uint32);

    buf += sal_sprintf(buf, "%s", ", num_voq:");
    EMIT_CHECK(sai_serialize_uint32(buf, system_port_config->num_voq), uint32);

    return (int)(buf - begin_buf);
}
int sai_serialize_timeoffset(
    _Out_ char *buf,
    _In_ sai_timeoffset_t *timeoffset)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "%s", "flag:");
    EMIT_CHECK(sai_serialize_uint8(buf, timeoffset->flag), uint8);

    buf += sal_sprintf(buf, "%s", "value:");
    EMIT_CHECK(sai_serialize_uint32(buf, timeoffset->value), uint32);

    return (int)(buf - begin_buf);
}
int sai_serialize_timespec(
    _Out_ char *buf,
    _In_ sai_timespec_t *timespec)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "%s", "tv_sec:");
    EMIT_CHECK(sai_serialize_uint64(buf, timespec->tv_sec), uint64);

    buf += sal_sprintf(buf, "%s", ", tv_nsec:");
    EMIT_CHECK(sai_serialize_uint32(buf, timespec->tv_nsec), uint32);

    return (int)(buf - begin_buf);
}
int sai_serialize_tlv_list(
    _Out_ char *buf,
    _In_ sai_tlv_list_t *tlv_list)
{
    char *begin_buf = buf;
    int ret;

    if (tlv_list->list == NULL || tlv_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        buf += sal_sprintf(buf, "%s", "[");
        for (idx = 0; idx < tlv_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, "\n            [");
            }
            ret = sai_serialize_tlv(buf, &tlv_list->list[idx]);
            buf += ret;
            if (idx != tlv_list->count-1)
            {
                buf += sal_sprintf(buf, "%s", "],");
            }
            else
            {
                buf += sal_sprintf(buf, "%s", "]");
            }
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_tlv(
    _Out_ char *buf,
    _In_ sai_tlv_t *tlv)
{
    char *begin_buf = buf;
    int ret;

    buf += sal_sprintf(buf, "tlv_type:");
    ret = sai_serialize_tlv_type(buf, tlv->tlv_type);
    buf += ret;

    buf += sal_sprintf(buf, ", entry:");
    ret = sai_serialize_tlv_entry(buf, tlv->tlv_type, &tlv->entry);
    buf += ret;

    return (int)(buf - begin_buf);
}
int sai_serialize_u16_list(
    _Out_ char *buf,
    _In_ sai_u16_list_t *u16_list)
{
    char *begin_buf = buf;
    int ret;

    if (u16_list->list == NULL || u16_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < u16_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_uint16(buf, u16_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_u32_list(
    _Out_ char *buf,
    _In_ sai_u32_list_t *u32_list)
{
    char *begin_buf = buf;
    int ret;

    if (u32_list->list == NULL || u32_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < u32_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_uint32(buf, u32_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_u32_range(
    _Out_ char *buf,
    _In_ sai_u32_range_t *u32_range)
{
    char *begin_buf = buf;
    int ret;

    ret = sai_serialize_uint32(buf, u32_range->min);
    buf += ret;
    buf += sal_sprintf(buf, ",");
    ret = sai_serialize_uint32(buf, u32_range->max);
    buf += ret;

    return (int)(buf - begin_buf);
}
int sai_serialize_u8_list(
    _Out_ char *buf,
    _In_ sai_u8_list_t *u8_list)
{
    char *begin_buf = buf;
    int ret;

    if (u8_list->list == NULL || u8_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < u8_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            ret = sai_serialize_uint8(buf, u8_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_vlan_list(
    _Out_ char *buf,
    _In_ sai_vlan_list_t *vlan_list)
{
    char *begin_buf = buf;
    int ret;

    if (vlan_list->list == NULL || vlan_list->count == 0)
    {
        buf += sal_sprintf(buf, "null");
    }
    else
    {
        uint32_t idx;

        for (idx = 0; idx < vlan_list->count; idx++)
        {
            if (idx != 0)
            {
                buf += sal_sprintf(buf, ",");
            }
            if (0 == idx%10 && 0 != idx)
            {
                buf += sal_sprintf(buf, "\n            ");
            }
            ret = sai_serialize_uint16(buf, vlan_list->list[idx]);
            buf += ret;
        }
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_y1731_session_event_notification(
    _Out_ char *buf,
    _In_ sai_y1731_session_event_notification_t *y1731_session_event_notification)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("y1731_oid");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, y1731_session_event_notification->y1731_oid), object_id);

    EMIT_NEXT_KEY("session_event_list");

    EMIT_CHECK(sai_serialize_s32_list(buf, &y1731_session_event_notification->session_event_list), s32_list);

    EMIT("}");

    return (int)(buf - begin_buf);
}

/* Serialize notifications */

int sai_serialize_bfd_session_state_change_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_bfd_session_state_notification_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_bfd_session_state_notification(buf, &data[idx]), bfd_session_state_notification);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_fdb_event_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_fdb_event_notification_data_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_fdb_event_notification_data(buf, &data[idx]), fdb_event_notification_data);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_buffer_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_monitor_buffer_notification_data_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_monitor_buffer_notification_data(buf, &data[idx]), monitor_buffer_notification_data);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_latency_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_monitor_latency_notification_data_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_monitor_latency_notification_data(buf, &data[idx]), monitor_latency_notification_data);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_packet_event_notification(
    _Out_ char *buf,
    _In_ sai_object_id_t switch_id,
    _In_ sai_size_t buffer_size,
    _In_ void * buffer,
    _In_ uint32_t attr_count,
    _In_ sai_attribute_t * attr_list)
{
#if 0
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, switch_id), object_id);

    EMIT_NEXT_KEY("buffer_size");

    EMIT_CHECK(sai_serialize_size(buf, buffer_size), size);

    EMIT_NEXT_KEY("buffer");

    if (((uint8_t*)buffer) == NULL || buffer_size == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        sai_size_t idx;

        for (idx = 0; idx < buffer_size; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_uint8(buf, ((uint8_t*)buffer)[idx]), uint8);
        }

        EMIT("]");
    }

    EMIT_NEXT_KEY("attr_count");

    EMIT_CHECK(sai_serialize_uint32(buf, attr_count), uint32);

    EMIT_NEXT_KEY("attr_list");

    if (attr_list == NULL || attr_count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < attr_count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            ctc_sai_attr_metadata_t *meta =
                sai_metadata_get_attr_metadata(SAI_OBJECT_TYPE_HOSTIF_PACKET, attr_list[idx].id);

            EMIT_CHECK(sai_serialize_attribute(buf, meta, &attr_list[idx]), attribute);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
#endif

    return 0;
}
int sai_serialize_packet_event_ptp_tx_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_packet_event_ptp_tx_notification_data_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_packet_event_ptp_tx_notification_data(buf, &data[idx]), packet_event_ptp_tx_notification_data);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_port_state_change_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_port_oper_status_notification_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_port_oper_status_notification(buf, &data[idx]), port_oper_status_notification);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_queue_pfc_deadlock_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_queue_deadlock_notification_data_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_queue_deadlock_notification_data(buf, &data[idx]), queue_deadlock_notification_data);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_signal_degrade_event_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_port_sd_notification_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_port_sd_notification(buf, &data[idx]), port_sd_notification);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_switch_shutdown_request_notification(
    _Out_ char *buf,
    _In_ sai_object_id_t switch_id)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, switch_id), object_id);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_switch_state_change_notification(
    _Out_ char *buf,
    _In_ sai_object_id_t switch_id,
    _In_ sai_switch_oper_status_t switch_oper_status)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("switch_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, switch_id), object_id);

    EMIT_NEXT_KEY("switch_oper_status");

    EMIT_QUOTE_CHECK(sai_serialize_switch_oper_status(buf, switch_oper_status), switch_oper_status);

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_tam_event_notification(
    _Out_ char *buf,
    _In_ sai_object_id_t tam_event_id,
    _In_ sai_size_t buffer_size,
    _In_ void * buffer,
    _In_ uint32_t attr_count,
    _In_ sai_attribute_t * attr_list)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("tam_event_id");

    EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, tam_event_id), object_id);

    EMIT_NEXT_KEY("buffer_size");

    EMIT_CHECK(sai_serialize_size(buf, buffer_size), size);

    EMIT_NEXT_KEY("buffer");

    if (((uint8_t*)buffer) == NULL || buffer_size == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        sai_size_t idx;

        for (idx = 0; idx < buffer_size; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_uint8(buf, ((uint8_t*)buffer)[idx]), uint8);
        }

        EMIT("]");
    }

    EMIT_NEXT_KEY("attr_count");

    EMIT_CHECK(sai_serialize_uint32(buf, attr_count), uint32);

    EMIT_NEXT_KEY("attr_list");

    if (attr_list == NULL || attr_count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < attr_count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }
            ctc_sai_attr_metadata_t *meta = ctc_sai_data_utils_get_attr_metadata(SAI_OBJECT_TYPE_TAM_EVENT_ACTION, attr_list[idx].id);
            EMIT_CHECK(sai_serialize_attribute(buf, meta, &attr_list[idx]), attribute);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_y1731_session_state_change_notification(
    _Out_ char *buf,
    _In_ uint32_t count,
    _In_ sai_y1731_session_event_notification_t * data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    EMIT_KEY("count");

    EMIT_CHECK(sai_serialize_uint32(buf, count), uint32);

    EMIT_NEXT_KEY("data");

    if (data == NULL || count == 0)
    {
        EMIT("null");
    }
    else
    {
        EMIT("[");

        uint32_t idx;

        for (idx = 0; idx < count; idx++)
        {
            if (idx != 0)
            {
                EMIT(",");
            }

            EMIT_CHECK(sai_serialize_y1731_session_event_notification(buf, &data[idx]), y1731_session_event_notification);
        }

        EMIT("]");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}

/* Serialize unions */

int sai_serialize_acl_action_parameter(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_acl_action_parameter_t *acl_action_parameter)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_BOOL)
    {
        EMIT_KEY("booldata");

        EMIT_CHECK(sai_serialize_bool(buf, acl_action_parameter->booldata), bool);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT8)
    {
        EMIT_KEY("u8");

        EMIT_CHECK(sai_serialize_uint8(buf, acl_action_parameter->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT8)
    {
        EMIT_KEY("s8");

        EMIT_CHECK(sai_serialize_int8(buf, acl_action_parameter->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT16)
    {
        EMIT_KEY("u16");

        EMIT_CHECK(sai_serialize_uint16(buf, acl_action_parameter->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT16)
    {
        EMIT_KEY("s16");

        EMIT_CHECK(sai_serialize_int16(buf, acl_action_parameter->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT32)
    {
        EMIT_KEY("u32");

        EMIT_CHECK(sai_serialize_uint32(buf, acl_action_parameter->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT32)
    {
        EMIT_KEY("s32");

        EMIT_CHECK(sai_serialize_enum(buf, meta->enummetadata, acl_action_parameter->s32), enum);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_MAC)
    {
        EMIT_KEY("mac");

        EMIT_QUOTE_CHECK(sai_serialize_mac(buf, acl_action_parameter->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV4)
    {
        EMIT_KEY("ip4");

        EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, acl_action_parameter->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV6)
    {
        EMIT_KEY("ip6");

        EMIT_QUOTE_CHECK(sai_serialize_ip6(buf, acl_action_parameter->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_ID)
    {
        EMIT_KEY("oid");

        EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, acl_action_parameter->oid), object_id);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST)
    {
        EMIT_KEY("objlist");

        EMIT_CHECK(sai_serialize_object_list(buf, &acl_action_parameter->objlist), object_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IP_ADDRESS)
    {
        EMIT_KEY("ipaddr");

        EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &acl_action_parameter->ipaddr), ip_address);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_acl_action_parameter_t', bad condition?");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_acl_field_data_data(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_acl_field_data_data_t *acl_field_data_data)
{
    char *begin_buf = buf;
    int ret;

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_BOOL)
    {
        EMIT_KEY("booldata");

        ret = sai_serialize_bool(buf, acl_field_data_data->booldata);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8)
    {
        EMIT_KEY("u8");

        ret = sai_serialize_uint8(buf, acl_field_data_data->u8);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8)
    {
        EMIT_KEY("s8");

        ret = sai_serialize_int8(buf, acl_field_data_data->s8);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16)
    {
        EMIT_KEY("u16");

        ret = sai_serialize_uint16(buf, acl_field_data_data->u16);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16)
    {
        EMIT_KEY("s16");

        ret = sai_serialize_int16(buf, acl_field_data_data->s16);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32)
    {
        EMIT_KEY("u32");

        ret = sai_serialize_uint32(buf, acl_field_data_data->u32);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32)
    {
        EMIT_KEY("s32");

        ret = sai_serialize_enum(buf, meta->enummetadata, acl_field_data_data->s32);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64)
    {
        EMIT_KEY("u64");

        ret = sai_serialize_uint64(buf, acl_field_data_data->u64);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC)
    {
        EMIT_KEY("mac");

        ret = sai_serialize_mac(buf, acl_field_data_data->mac);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4)
    {
        EMIT_KEY("ip4");

        ret = sai_serialize_ip4(buf, acl_field_data_data->ip4);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6)
    {
        EMIT_KEY("ip6");

        ret = sai_serialize_ip6(buf, acl_field_data_data->ip6);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_ID)
    {
        EMIT_KEY("oid");

        ret = sai_serialize_object_id(buf, acl_field_data_data->oid);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST)
    {
        EMIT_KEY("objlist");

        ret = sai_serialize_object_list(buf, &acl_field_data_data->objlist);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
    {
        EMIT_KEY("u8list");

        ret = sai_serialize_u8_list(buf, &acl_field_data_data->u8list);
        buf += ret;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_acl_field_data_data_t', bad condition?");
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_acl_field_data_mask(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_acl_field_data_mask_t *acl_field_data_mask)
{
    char *begin_buf = buf;
    int ret;

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8)
    {
        EMIT_KEY("u8");

        ret = sai_serialize_uint8(buf, acl_field_data_mask->u8);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8)
    {
        EMIT_KEY("s8");

        ret = sai_serialize_int8(buf, acl_field_data_mask->s8);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16)
    {
        EMIT_KEY("u16");

        ret = sai_serialize_uint16(buf, acl_field_data_mask->u16);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16)
    {
        EMIT_KEY("s16");

        ret = sai_serialize_int16(buf, acl_field_data_mask->s16);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32)
    {
        EMIT_KEY("u32");

        ret = sai_serialize_uint32(buf, acl_field_data_mask->u32);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32)
    {
        EMIT_KEY("s32");

        ret = sai_serialize_int32(buf, acl_field_data_mask->s32);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64)
    {
        EMIT_KEY("u64");

        ret = sai_serialize_uint64(buf, acl_field_data_mask->u64);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC)
    {
        EMIT_KEY("mac");
        ret = sai_serialize_mac(buf, acl_field_data_mask->mac);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4)
    {
        EMIT_KEY("ip4");
        ret = sai_serialize_ip4(buf, acl_field_data_mask->ip4);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6)
    {
        EMIT_KEY("ip6");
        ret = sai_serialize_ip6(buf, acl_field_data_mask->ip6);
        buf += ret;
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
    {
        EMIT_KEY("u8list");
        ret = sai_serialize_u8_list(buf, &acl_field_data_mask->u8list);
        buf += ret;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_acl_field_data_mask_t', bad condition?");
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_attribute_value(
    _Out_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _In_ sai_attribute_value_t *attribute_value)
{
    char *begin_buf = buf;
    int ret;

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_BOOL)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  booldata");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_bool(buf, attribute_value->booldata), bool);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_CHARDATA)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  chardata");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_chardata(buf, attribute_value->chardata), chardata);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT8)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u8");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_uint8(buf, attribute_value->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT8)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s8");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_int8(buf, attribute_value->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT16)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u16");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_uint16(buf, attribute_value->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT16)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s16");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_int16(buf, attribute_value->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u32");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_uint32(buf, attribute_value->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s32");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_enum(buf, meta->enummetadata, attribute_value->s32), enum);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT64)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u64");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_uint64(buf, attribute_value->u64), uint64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT64)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s64");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_CHECK(sai_serialize_int64(buf, attribute_value->s64), int64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_POINTER)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ptr");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_pointer(buf, attribute_value->ptr), pointer);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MAC)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  mac");
        buf += sal_sprintf(buf, "%s",   "Datavalue: ");
        EMIT_QUOTE_CHECK(sai_serialize_mac(buf, attribute_value->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IPV4)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ip4");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, attribute_value->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IPV6)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ip6");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_ip6(buf, attribute_value->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ipaddr");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_ip_address(buf, &attribute_value->ipaddr), ip_address);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_PREFIX)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ipprefix");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_ip_prefix(buf, &attribute_value->ipprefix), ip_prefix);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_OBJECT_ID)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  oid");
        buf += sal_sprintf(buf, "%s",   "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, attribute_value->oid), object_id);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  objlist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->objlist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_object_list(buf, &attribute_value->objlist), object_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  boollist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->boollist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_bool_list(buf, &attribute_value->boollist), bool_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u8list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->u8list.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_u8_list(buf, &attribute_value->u8list), u8_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s8list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->s8list.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_s8_list(buf, &attribute_value->s8list), s8_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u16list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->u16list.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_u16_list(buf, &attribute_value->u16list), u16_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s16list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->s16list.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_s16_list(buf, &attribute_value->s16list), s16_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u32list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->u32list.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_u32_list(buf, &attribute_value->u32list), u32_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s32list");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->s32list.count);
        buf += sal_sprintf(buf, "%s", "ListData:  {");
        EMIT_CHECK(sai_serialize_enum_list(buf, meta->enummetadata, &attribute_value->s32list), enum_list);
        buf += sal_sprintf(buf, "%s", "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32_RANGE)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  u32range");
        buf += sal_sprintf(buf, "RangeData: {");
        EMIT_CHECK(sai_serialize_u32_range(buf, &attribute_value->u32range), u32_range);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32_RANGE)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  s32range");
        buf += sal_sprintf(buf, "RangeData: {");
        EMIT_CHECK(sai_serialize_s32_range(buf, &attribute_value->s32range), s32_range);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  vlanlist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->vlanlist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_vlan_list(buf, &attribute_value->vlanlist), vlan_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  qosmap");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->qosmap.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_qos_map_list(buf, &attribute_value->qosmap), qos_map_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  maplist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->maplist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_map_list(buf, &attribute_value->maplist), map_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->isaclfield == true)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  aclfield");

        if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST)
        {
            buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->aclfield.data.objlist.count);
            buf += sal_sprintf(buf, "ListData:  {");
        }
        else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
        {
            buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->aclfield.data.u8list.count);
            buf += sal_sprintf(buf, "ListData:  {");
        }
        else
        {
            buf += sal_sprintf(buf, "%s",   "DataValue: ");
        }

        EMIT_CHECK(sai_serialize_acl_field_data(buf, meta, &attribute_value->aclfield), acl_field_data);

        if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST
           || meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
        {
            buf += sal_sprintf(buf, "}");
        }
    }
    else if (meta->isaclaction == true)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  aclaction");
        if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST)
        {
            buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->objlist.count);
            buf += sal_sprintf(buf, "ListData:  {");
        }
        else
        {
            buf += sal_sprintf(buf, "%s",   "DataValue: ");
        }

        EMIT_CHECK(sai_serialize_acl_action_data(buf, meta, &attribute_value->aclaction), acl_action_data);

        if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST)
        {
            buf += sal_sprintf(buf, "}");
        }
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_CAPABILITY)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  aclcapability");
        EMIT_CHECK(sai_serialize_acl_capability(buf, &attribute_value->aclcapability), acl_capability);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  aclresource");
        EMIT_CHECK(sai_serialize_acl_resource_list(buf, &attribute_value->aclresource), acl_resource_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  tlvlist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->tlvlist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_tlv_list(buf, &attribute_value->tlvlist), tlv_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  segmentlist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->segmentlist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_segment_list(buf, &attribute_value->segmentlist), segment_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  ipaddrlist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->ipaddrlist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_ip_address_list(buf, &attribute_value->ipaddrlist), ip_address_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  porteyevalues");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->porteyevalues.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_port_eye_values_list(buf, &attribute_value->porteyevalues), port_eye_values_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TIMESPEC)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  timespec");
        buf += sal_sprintf(buf, "DataValue: ");
        EMIT_CHECK(sai_serialize_timespec(buf, &attribute_value->timespec), timespec);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SAK)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  macsecsak");
        buf += sal_sprintf(buf, "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_macsec_sak(buf, attribute_value->macsecsak), macsec_sak);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_AUTH_KEY)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  macsecauthkey");
        buf += sal_sprintf(buf, "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_macsec_auth_key(buf, attribute_value->macsecauthkey), macsec_auth_key);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SALT)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  macsecsalt");
        buf += sal_sprintf(buf, "DataValue: ");
        EMIT_QUOTE_CHECK(sai_serialize_macsec_salt(buf, attribute_value->macsecsalt), macsec_salt);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  sysportconfig");
        buf += sal_sprintf(buf, "DataValue: [");
        EMIT_CHECK(sai_serialize_system_port_config(buf, &attribute_value->sysportconfig), system_port_config);
        buf += sal_sprintf(buf, "]");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  sysportconfiglist");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->sysportconfiglist.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_system_port_config_list(buf, &attribute_value->sysportconfiglist), system_port_config_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_FABRIC_PORT_REACHABILITY)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  reachability");
        buf += sal_sprintf(buf, "DataValue: [");
        EMIT_CHECK(sai_serialize_fabric_port_reachability(buf, &attribute_value->reachability), fabric_port_reachability);
        buf += sal_sprintf(buf, "]");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  porterror");
        buf += sal_sprintf(buf, "ListCount: %u\n", attribute_value->porterror.count);
        buf += sal_sprintf(buf, "ListData:  {");
        EMIT_CHECK(sai_serialize_port_err_status_list(buf, &attribute_value->porterror), port_err_status_list);
        buf += sal_sprintf(buf, "}");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_CAPTURED_TIMESPEC)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  captured_timespec");
        buf += sal_sprintf(buf, "DataValue: [");
        EMIT_CHECK(sai_serialize_captured_timespec(buf, &attribute_value->captured_timespec), captured_timespec);
        buf += sal_sprintf(buf, "]");
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TIMEOFFSET)
    {
        buf += sal_sprintf(buf, "%s\n", "DataType:  timeoffset");
        buf += sal_sprintf(buf, "DataValue: [");
        EMIT_CHECK(sai_serialize_timeoffset(buf, &attribute_value->timeoffset), timeoffset);
        buf += sal_sprintf(buf, "]");
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_attribute_value_t', bad condition?");
    }

    return (int)(buf - begin_buf);
}
int sai_serialize_ip_addr(
    _Out_ char *buf,
    _In_ sai_ip_addr_family_t addr_family,
    _In_ sai_ip_addr_t *ip_addr)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    if (addr_family == SAI_IP_ADDR_FAMILY_IPV4)
    {
        EMIT_KEY("ip4");

        EMIT_QUOTE_CHECK(sai_serialize_ip4(buf, ip_addr->ip4), ip4);
    }
    else if (addr_family == SAI_IP_ADDR_FAMILY_IPV6)
    {
        EMIT_KEY("ip6");

        EMIT_QUOTE_CHECK(sai_serialize_ip6(buf, ip_addr->ip6), ip6);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_ip_addr_t', bad condition?");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_buffer_data(
    _Out_ char *buf,
    _In_ sai_buffer_monitor_message_type_t buffer_monitor_message_type,
    _In_ sai_monitor_buffer_data_t *monitor_buffer_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE)
    {
        EMIT_KEY("buffer_event");

        EMIT_CHECK(sai_serialize_monitor_buffer_event(buf, &monitor_buffer_data->buffer_event), monitor_buffer_event);
    }
    else if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_STATS_MESSAGE)
    {
        EMIT_KEY("buffer_stats");

        EMIT_CHECK(sai_serialize_monitor_buffer_stats(buf, &monitor_buffer_data->buffer_stats), monitor_buffer_stats);
    }
    else if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_MICORBURST_STATS_MESSAGE)
    {
        EMIT_KEY("microburst_stats");

        EMIT_CHECK(sai_serialize_monitor_mburst_stats(buf, &monitor_buffer_data->microburst_stats), monitor_mburst_stats);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_monitor_buffer_data_t', bad condition?");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_monitor_latency_data(
    _Out_ char *buf,
    _In_ sai_latency_monitor_message_type_t latency_monitor_message_type,
    _In_ sai_monitor_latency_data_t *monitor_latency_data)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    if (latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE)
    {
        EMIT_KEY("latency_event");

        EMIT_CHECK(sai_serialize_monitor_latency_event(buf, &monitor_latency_data->latency_event), monitor_latency_event);
    }
    else if (latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_STATS_MESSAGE)
    {
        EMIT_KEY("latency_stats");

        EMIT_CHECK(sai_serialize_monitor_latency_stats(buf, &monitor_latency_data->latency_stats), monitor_latency_stats);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_monitor_latency_data_t', bad condition?");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_object_key_entry(
    _Out_ char *buf,
    _In_ sai_object_type_t object_type,
    _In_ sai_object_key_entry_t *object_key_entry)
{
    char *begin_buf = buf;
    int ret;

    EMIT("{");

    if (ctc_sai_data_utils_is_object_type_oid(object_type) == true)
    {
        EMIT_KEY("object_id");

        EMIT_QUOTE_CHECK(sai_serialize_object_id(buf, object_key_entry->object_id), object_id);
    }
    else if (object_type == SAI_OBJECT_TYPE_FDB_ENTRY)
    {
        EMIT_KEY("fdb_entry");

        EMIT_CHECK(sai_serialize_fdb_entry(buf, &object_key_entry->fdb_entry), fdb_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_NEIGHBOR_ENTRY)
    {
        EMIT_KEY("neighbor_entry");

        EMIT_CHECK(sai_serialize_neighbor_entry(buf, &object_key_entry->neighbor_entry), neighbor_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_ROUTE_ENTRY)
    {
        EMIT_KEY("route_entry");

        EMIT_CHECK(sai_serialize_route_entry(buf, &object_key_entry->route_entry), route_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_MCAST_FDB_ENTRY)
    {
        EMIT_KEY("mcast_fdb_entry");

        EMIT_CHECK(sai_serialize_mcast_fdb_entry(buf, &object_key_entry->mcast_fdb_entry), mcast_fdb_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_L2MC_ENTRY)
    {
        EMIT_KEY("l2mc_entry");

        EMIT_CHECK(sai_serialize_l2mc_entry(buf, &object_key_entry->l2mc_entry), l2mc_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_IPMC_ENTRY)
    {
        EMIT_KEY("ipmc_entry");

        EMIT_CHECK(sai_serialize_ipmc_entry(buf, &object_key_entry->ipmc_entry), ipmc_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_INSEG_ENTRY)
    {
        EMIT_KEY("inseg_entry");

        EMIT_CHECK(sai_serialize_inseg_entry(buf, &object_key_entry->inseg_entry), inseg_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_NAT_ENTRY)
    {
        EMIT_KEY("nat_entry");

        EMIT_CHECK(sai_serialize_nat_entry(buf, &object_key_entry->nat_entry), nat_entry);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_object_key_entry_t', bad condition?");
    }

    EMIT("}");

    return (int)(buf - begin_buf);
}
int sai_serialize_tlv_entry(
    _Out_ char *buf,
    _In_ sai_tlv_type_t tlv_type,
    _In_ sai_tlv_entry_t *tlv_entry)
{
    char *begin_buf = buf;
    int ret;

    if (tlv_type == SAI_TLV_TYPE_INGRESS)
    {
        buf += sal_sprintf(buf, "ingress_node:");
        buf += sai_serialize_ip6(buf, tlv_entry->ingress_node);
    }
    else if (tlv_type == SAI_TLV_TYPE_EGRESS)
    {
        buf += sal_sprintf(buf, "egress_node:");
        buf += sai_serialize_ip6(buf, tlv_entry->egress_node);
    }
    else if (tlv_type == SAI_TLV_TYPE_OPAQUE)
    {
        buf += sal_sprintf(buf, "opaque_container:");

        if (tlv_entry->opaque_container == NULL || 4 == 0)
        {
            EMIT("null");
        }
        else
        {
            buf += sal_sprintf(buf, "[");

            uint32_t idx;

            for (idx = 0; idx < 4; idx++)
            {
                if (idx != 0)
                {
                    buf += sal_sprintf(buf, ",");
                }
                EMIT_CHECK(sai_serialize_hex_uint32(buf, tlv_entry->opaque_container[idx]), uint32);
            }
            buf += sal_sprintf(buf, "]");
        }
    }
    else if (tlv_type == SAI_TLV_TYPE_HMAC)
    {
        buf += sal_sprintf(buf, "hmac:");
        EMIT_CHECK(sai_serialize_hmac(buf, &tlv_entry->hmac), hmac);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was serialized for 'sai_tlv_entry_t', bad condition?");
    }

    return (int)(buf - begin_buf);
}

/* Enum deserialize methods */

int sai_deserialize_acl_action_type(
    _In_ char *buffer,
    _Out_ sai_acl_action_type_t *acl_action_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_action_type_t, (int*)acl_action_type);
}
int sai_deserialize_acl_bind_point_type(
    _In_ char *buffer,
    _Out_ sai_acl_bind_point_type_t *acl_bind_point_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_bind_point_type_t, (int*)acl_bind_point_type);
}
int sai_deserialize_acl_dtel_flow_op(
    _In_ char *buffer,
    _Out_ sai_acl_dtel_flow_op_t *acl_dtel_flow_op)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_dtel_flow_op_t, (int*)acl_dtel_flow_op);
}
int sai_deserialize_acl_ip_frag(
    _In_ char *buffer,
    _Out_ sai_acl_ip_frag_t *acl_ip_frag)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_ip_frag_t, (int*)acl_ip_frag);
}
int sai_deserialize_acl_ip_type(
    _In_ char *buffer,
    _Out_ sai_acl_ip_type_t *acl_ip_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_ip_type_t, (int*)acl_ip_type);
}
int sai_deserialize_acl_range_type(
    _In_ char *buffer,
    _Out_ sai_acl_range_type_t *acl_range_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_range_type_t, (int*)acl_range_type);
}
int sai_deserialize_acl_stage(
    _In_ char *buffer,
    _Out_ sai_acl_stage_t *acl_stage)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_stage_t, (int*)acl_stage);
}
int sai_deserialize_acl_table_group_type(
    _In_ char *buffer,
    _Out_ sai_acl_table_group_type_t *acl_table_group_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_acl_table_group_type_t, (int*)acl_table_group_type);
}
//int sai_deserialize_api_extensions(
//    _In_ char *buffer,
//    _Out_ sai_api_extensions_t *api_extensions)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_api_extensions_t, (int*)api_extensions);
//}
//int sai_deserialize_api(
//    _In_ char *buffer,
//    _Out_ sai_api_t *api)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_api_t, (int*)api);
//}
//int sai_deserialize_attr_condition_type(
//    _In_ char *buffer,
//    _Out_ sai_attr_condition_type_t *attr_condition_type)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_attr_condition_type_t, (int*)attr_condition_type);
//}
//int sai_deserialize_attr_flags(
//    _In_ char *buffer,
//    _Out_ sai_attr_flags_t *attr_flags)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_attr_flags_t, (int*)attr_flags);
//}
int sai_deserialize_attr_value_type(
    _In_ char *buffer,
    _Out_ ctc_sai_attr_value_type_t *attr_value_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_ctc_sai_attr_value_type_t, (int*)attr_value_type);
}
int sai_deserialize_bfd_ach_channel_type(
    _In_ char *buffer,
    _Out_ sai_bfd_ach_channel_type_t *bfd_ach_channel_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_ach_channel_type_t, (int*)bfd_ach_channel_type);
}
int sai_deserialize_bfd_encapsulation_type(
    _In_ char *buffer,
    _Out_ sai_bfd_encapsulation_type_t *bfd_encapsulation_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_encapsulation_type_t, (int*)bfd_encapsulation_type);
}
int sai_deserialize_bfd_mpls_type(
    _In_ char *buffer,
    _Out_ sai_bfd_mpls_type_t *bfd_mpls_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_mpls_type_t, (int*)bfd_mpls_type);
}
int sai_deserialize_bfd_session_offload_type(
    _In_ char *buffer,
    _Out_ sai_bfd_session_offload_type_t *bfd_session_offload_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_offload_type_t, (int*)bfd_session_offload_type);
}
int sai_deserialize_bfd_session_stat(
    _In_ char *buffer,
    _Out_ sai_bfd_session_stat_t *bfd_session_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_stat_t, (int*)bfd_session_stat);
}
int sai_deserialize_bfd_session_state(
    _In_ char *buffer,
    _Out_ sai_bfd_session_state_t *bfd_session_state)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_state_t, (int*)bfd_session_state);
}
int sai_deserialize_bfd_session_type(
    _In_ char *buffer,
    _Out_ sai_bfd_session_type_t *bfd_session_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bfd_session_type_t, (int*)bfd_session_type);
}
int sai_deserialize_bridge_flood_control_type(
    _In_ char *buffer,
    _Out_ sai_bridge_flood_control_type_t *bridge_flood_control_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_flood_control_type_t, (int*)bridge_flood_control_type);
}
int sai_deserialize_bridge_port_fdb_learning_mode(
    _In_ char *buffer,
    _Out_ sai_bridge_port_fdb_learning_mode_t *bridge_port_fdb_learning_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_fdb_learning_mode_t, (int*)bridge_port_fdb_learning_mode);
}
int sai_deserialize_bridge_port_outgoing_service_vlan_cos_mode(
    _In_ char *buffer,
    _Out_ sai_bridge_port_outgoing_service_vlan_cos_mode_t *bridge_port_outgoing_service_vlan_cos_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_outgoing_service_vlan_cos_mode_t, (int*)bridge_port_outgoing_service_vlan_cos_mode);
}
int sai_deserialize_bridge_port_stat(
    _In_ char *buffer,
    _Out_ sai_bridge_port_stat_t *bridge_port_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_stat_t, (int*)bridge_port_stat);
}
int sai_deserialize_bridge_port_tagging_mode(
    _In_ char *buffer,
    _Out_ sai_bridge_port_tagging_mode_t *bridge_port_tagging_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_tagging_mode_t, (int*)bridge_port_tagging_mode);
}
int sai_deserialize_bridge_port_type(
    _In_ char *buffer,
    _Out_ sai_bridge_port_type_t *bridge_port_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_port_type_t, (int*)bridge_port_type);
}
int sai_deserialize_bridge_stat(
    _In_ char *buffer,
    _Out_ sai_bridge_stat_t *bridge_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_stat_t, (int*)bridge_stat);
}
int sai_deserialize_bridge_type(
    _In_ char *buffer,
    _Out_ sai_bridge_type_t *bridge_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bridge_type_t, (int*)bridge_type);
}
int sai_deserialize_buffer_monitor_based_on_type(
    _In_ char *buffer,
    _Out_ sai_buffer_monitor_based_on_type_t *buffer_monitor_based_on_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_based_on_type_t, (int*)buffer_monitor_based_on_type);
}
int sai_deserialize_buffer_monitor_message_type(
    _In_ char *buffer,
    _Out_ sai_buffer_monitor_message_type_t *buffer_monitor_message_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_message_type_t, (int*)buffer_monitor_message_type);
}
int sai_deserialize_buffer_monitor_stats_direction(
    _In_ char *buffer,
    _Out_ sai_buffer_monitor_stats_direction_t *buffer_monitor_stats_direction)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_monitor_stats_direction_t, (int*)buffer_monitor_stats_direction);
}
int sai_deserialize_buffer_pool_stat(
    _In_ char *buffer,
    _Out_ sai_buffer_pool_stat_t *buffer_pool_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_stat_t, (int*)buffer_pool_stat);
}
int sai_deserialize_buffer_pool_threshold_mode(
    _In_ char *buffer,
    _Out_ sai_buffer_pool_threshold_mode_t *buffer_pool_threshold_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_threshold_mode_t, (int*)buffer_pool_threshold_mode);
}
int sai_deserialize_buffer_pool_type(
    _In_ char *buffer,
    _Out_ sai_buffer_pool_type_t *buffer_pool_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_pool_type_t, (int*)buffer_pool_type);
}
int sai_deserialize_buffer_profile_threshold_mode(
    _In_ char *buffer,
    _Out_ sai_buffer_profile_threshold_mode_t *buffer_profile_threshold_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_buffer_profile_threshold_mode_t, (int*)buffer_profile_threshold_mode);
}
int sai_deserialize_bulk_op_error_mode(
    _In_ char *buffer,
    _Out_ sai_bulk_op_error_mode_t *bulk_op_error_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_bulk_op_error_mode_t, (int*)bulk_op_error_mode);
}
int sai_deserialize_common_api(
    _In_ char *buffer,
    _Out_ sai_common_api_t *common_api)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_common_api_t, (int*)common_api);
}
int sai_deserialize_counter_stat(
    _In_ char *buffer,
    _Out_ sai_counter_stat_t *counter_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_counter_stat_t, (int*)counter_stat);
}
int sai_deserialize_counter_type(
    _In_ char *buffer,
    _Out_ sai_counter_type_t *counter_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_counter_type_t, (int*)counter_type);
}
int sai_deserialize_debug_counter_bind_method(
    _In_ char *buffer,
    _Out_ sai_debug_counter_bind_method_t *debug_counter_bind_method)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_debug_counter_bind_method_t, (int*)debug_counter_bind_method);
}
int sai_deserialize_debug_counter_type(
    _In_ char *buffer,
    _Out_ sai_debug_counter_type_t *debug_counter_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_debug_counter_type_t, (int*)debug_counter_type);
}
#if 0
int sai_deserialize_default_value_type(
    _In_ char *buffer,
    _Out_ sai_default_value_type_t *default_value_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_default_value_type_t, (int*)default_value_type);
}
#endif
int sai_deserialize_dtel_event_type(
    _In_ char *buffer,
    _Out_ sai_dtel_event_type_t *dtel_event_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_dtel_event_type_t, (int*)dtel_event_type);
}
int sai_deserialize_ecn_mark_mode(
    _In_ char *buffer,
    _Out_ sai_ecn_mark_mode_t *ecn_mark_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ecn_mark_mode_t, (int*)ecn_mark_mode);
}
int sai_deserialize_erspan_encapsulation_type(
    _In_ char *buffer,
    _Out_ sai_erspan_encapsulation_type_t *erspan_encapsulation_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_erspan_encapsulation_type_t, (int*)erspan_encapsulation_type);
}
int sai_deserialize_fdb_entry_type(
    _In_ char *buffer,
    _Out_ sai_fdb_entry_type_t *fdb_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_entry_type_t, (int*)fdb_entry_type);
}
int sai_deserialize_fdb_event(
    _In_ char *buffer,
    _Out_ sai_fdb_event_t *fdb_event)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_event_t, (int*)fdb_event);
}
int sai_deserialize_fdb_flush_entry_type(
    _In_ char *buffer,
    _Out_ sai_fdb_flush_entry_type_t *fdb_flush_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_fdb_flush_entry_type_t, (int*)fdb_flush_entry_type);
}
int sai_deserialize_hash_algorithm(
    _In_ char *buffer,
    _Out_ sai_hash_algorithm_t *hash_algorithm)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hash_algorithm_t, (int*)hash_algorithm);
}
int sai_deserialize_hostif_packet_oam_tx_type(
    _In_ char *buffer,
    _Out_ sai_hostif_packet_oam_tx_type_t *hostif_packet_oam_tx_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_packet_oam_tx_type_t, (int*)hostif_packet_oam_tx_type);
}
int sai_deserialize_hostif_packet_ptp_tx_packet_op_type(
    _In_ char *buffer,
    _Out_ sai_hostif_packet_ptp_tx_packet_op_type_t *hostif_packet_ptp_tx_packet_op_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_packet_ptp_tx_packet_op_type_t, (int*)hostif_packet_ptp_tx_packet_op_type);
}
int sai_deserialize_hostif_table_entry_channel_type(
    _In_ char *buffer,
    _Out_ sai_hostif_table_entry_channel_type_t *hostif_table_entry_channel_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_table_entry_channel_type_t, (int*)hostif_table_entry_channel_type);
}
int sai_deserialize_hostif_table_entry_type(
    _In_ char *buffer,
    _Out_ sai_hostif_table_entry_type_t *hostif_table_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_table_entry_type_t, (int*)hostif_table_entry_type);
}
int sai_deserialize_hostif_trap_type(
    _In_ char *buffer,
    _Out_ sai_hostif_trap_type_t *hostif_trap_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_trap_type_t, (int*)hostif_trap_type);
}
int sai_deserialize_hostif_tx_type(
    _In_ char *buffer,
    _Out_ sai_hostif_tx_type_t *hostif_tx_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_tx_type_t, (int*)hostif_tx_type);
}
int sai_deserialize_hostif_type(
    _In_ char *buffer,
    _Out_ sai_hostif_type_t *hostif_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_type_t, (int*)hostif_type);
}
int sai_deserialize_hostif_user_defined_trap_type(
    _In_ char *buffer,
    _Out_ sai_hostif_user_defined_trap_type_t *hostif_user_defined_trap_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_user_defined_trap_type_t, (int*)hostif_user_defined_trap_type);
}
int sai_deserialize_hostif_vlan_tag(
    _In_ char *buffer,
    _Out_ sai_hostif_vlan_tag_t *hostif_vlan_tag)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_hostif_vlan_tag_t, (int*)hostif_vlan_tag);
}
int sai_deserialize_in_drop_reason(
    _In_ char *buffer,
    _Out_ sai_in_drop_reason_t *in_drop_reason)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_in_drop_reason_t, (int*)in_drop_reason);
}
int sai_deserialize_ingress_priority_group_stat(
    _In_ char *buffer,
    _Out_ sai_ingress_priority_group_stat_t *ingress_priority_group_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ingress_priority_group_stat_t, (int*)ingress_priority_group_stat);
}
int sai_deserialize_inseg_entry_configured_role(
    _In_ char *buffer,
    _Out_ sai_inseg_entry_configured_role_t *inseg_entry_configured_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_configured_role_t, (int*)inseg_entry_configured_role);
}
int sai_deserialize_inseg_entry_frr_observed_role(
    _In_ char *buffer,
    _Out_ sai_inseg_entry_frr_observed_role_t *inseg_entry_frr_observed_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_frr_observed_role_t, (int*)inseg_entry_frr_observed_role);
}
int sai_deserialize_inseg_entry_pop_qos_mode(
    _In_ char *buffer,
    _Out_ sai_inseg_entry_pop_qos_mode_t *inseg_entry_pop_qos_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_pop_qos_mode_t, (int*)inseg_entry_pop_qos_mode);
}
int sai_deserialize_inseg_entry_pop_ttl_mode(
    _In_ char *buffer,
    _Out_ sai_inseg_entry_pop_ttl_mode_t *inseg_entry_pop_ttl_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_pop_ttl_mode_t, (int*)inseg_entry_pop_ttl_mode);
}
int sai_deserialize_inseg_entry_psc_type(
    _In_ char *buffer,
    _Out_ sai_inseg_entry_psc_type_t *inseg_entry_psc_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_inseg_entry_psc_type_t, (int*)inseg_entry_psc_type);
}
int sai_deserialize_ip_addr_family(
    _In_ char *buffer,
    _Out_ sai_ip_addr_family_t *ip_addr_family)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ip_addr_family_t, (int*)ip_addr_family);
}
int sai_deserialize_ipmc_entry_type(
    _In_ char *buffer,
    _Out_ sai_ipmc_entry_type_t *ipmc_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ipmc_entry_type_t, (int*)ipmc_entry_type);
}
int sai_deserialize_isolation_group_type(
    _In_ char *buffer,
    _Out_ sai_isolation_group_type_t *isolation_group_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_isolation_group_type_t, (int*)isolation_group_type);
}
int sai_deserialize_l2mc_entry_type(
    _In_ char *buffer,
    _Out_ sai_l2mc_entry_type_t *l2mc_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_l2mc_entry_type_t, (int*)l2mc_entry_type);
}
int sai_deserialize_lag_mode(
    _In_ char *buffer,
    _Out_ sai_lag_mode_t *lag_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_lag_mode_t, (int*)lag_mode);
}
int sai_deserialize_latency_monitor_message_type(
    _In_ char *buffer,
    _Out_ sai_latency_monitor_message_type_t *latency_monitor_message_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_latency_monitor_message_type_t, (int*)latency_monitor_message_type);
}
//int sai_deserialize_log_level(
//    _In_ char *buffer,
//    _Out_ sai_log_level_t *log_level)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_log_level_t, (int*)log_level);
//}
int sai_deserialize_macsec_direction(
    _In_ char *buffer,
    _Out_ sai_macsec_direction_t *macsec_direction)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_direction_t, (int*)macsec_direction);
}
int sai_deserialize_macsec_flow_stat(
    _In_ char *buffer,
    _Out_ sai_macsec_flow_stat_t *macsec_flow_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_flow_stat_t, (int*)macsec_flow_stat);
}
int sai_deserialize_macsec_port_stat(
    _In_ char *buffer,
    _Out_ sai_macsec_port_stat_t *macsec_port_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_port_stat_t, (int*)macsec_port_stat);
}
int sai_deserialize_macsec_sa_stat(
    _In_ char *buffer,
    _Out_ sai_macsec_sa_stat_t *macsec_sa_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_sa_stat_t, (int*)macsec_sa_stat);
}
int sai_deserialize_macsec_sc_stat(
    _In_ char *buffer,
    _Out_ sai_macsec_sc_stat_t *macsec_sc_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_macsec_sc_stat_t, (int*)macsec_sc_stat);
}
int sai_deserialize_meter_type(
    _In_ char *buffer,
    _Out_ sai_meter_type_t *meter_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_meter_type_t, (int*)meter_type);
}
int sai_deserialize_mirror_session_congestion_mode(
    _In_ char *buffer,
    _Out_ sai_mirror_session_congestion_mode_t *mirror_session_congestion_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_mirror_session_congestion_mode_t, (int*)mirror_session_congestion_mode);
}
int sai_deserialize_mirror_session_type(
    _In_ char *buffer,
    _Out_ sai_mirror_session_type_t *mirror_session_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_mirror_session_type_t, (int*)mirror_session_type);
}
int sai_deserialize_monitor_event_state(
    _In_ char *buffer,
    _Out_ sai_monitor_event_state_t *monitor_event_state)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_monitor_event_state_t, (int*)monitor_event_state);
}
int sai_deserialize_nat_type(
    _In_ char *buffer,
    _Out_ sai_nat_type_t *nat_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_nat_type_t, (int*)nat_type);
}
int sai_deserialize_native_hash_field(
    _In_ char *buffer,
    _Out_ sai_native_hash_field_t *native_hash_field)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_native_hash_field_t, (int*)native_hash_field);
}
int sai_deserialize_next_hop_endpoint_pop_type(
    _In_ char *buffer,
    _Out_ sai_next_hop_endpoint_pop_type_t *next_hop_endpoint_pop_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_endpoint_pop_type_t, (int*)next_hop_endpoint_pop_type);
}
int sai_deserialize_next_hop_endpoint_type(
    _In_ char *buffer,
    _Out_ sai_next_hop_endpoint_type_t *next_hop_endpoint_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_endpoint_type_t, (int*)next_hop_endpoint_type);
}
int sai_deserialize_next_hop_group_member_configured_role(
    _In_ char *buffer,
    _Out_ sai_next_hop_group_member_configured_role_t *next_hop_group_member_configured_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_member_configured_role_t, (int*)next_hop_group_member_configured_role);
}
int sai_deserialize_next_hop_group_member_observed_role(
    _In_ char *buffer,
    _Out_ sai_next_hop_group_member_observed_role_t *next_hop_group_member_observed_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_member_observed_role_t, (int*)next_hop_group_member_observed_role);
}
int sai_deserialize_next_hop_group_type(
    _In_ char *buffer,
    _Out_ sai_next_hop_group_type_t *next_hop_group_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_group_type_t, (int*)next_hop_group_type);
}
int sai_deserialize_next_hop_type(
    _In_ char *buffer,
    _Out_ sai_next_hop_type_t *next_hop_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_next_hop_type_t, (int*)next_hop_type);
}
int sai_deserialize_npm_encapsulation_type(
    _In_ char *buffer,
    _Out_ sai_npm_encapsulation_type_t *npm_encapsulation_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_encapsulation_type_t, (int*)npm_encapsulation_type);
}
int sai_deserialize_npm_pkt_tx_mode(
    _In_ char *buffer,
    _Out_ sai_npm_pkt_tx_mode_t *npm_pkt_tx_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_pkt_tx_mode_t, (int*)npm_pkt_tx_mode);
}
int sai_deserialize_npm_session_role(
    _In_ char *buffer,
    _Out_ sai_npm_session_role_t *npm_session_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_session_role_t, (int*)npm_session_role);
}
int sai_deserialize_npm_session_stats(
    _In_ char *buffer,
    _Out_ sai_npm_session_stats_t *npm_session_stats)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_npm_session_stats_t, (int*)npm_session_stats);
}
//int sai_deserialize_object_type_extensions(
//    _In_ char *buffer,
//    _Out_ sai_object_type_extensions_t *object_type_extensions)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_object_type_extensions_t, (int*)object_type_extensions);
//}
int sai_deserialize_object_type(
    _In_ char *buffer,
    _Out_ sai_object_type_t *object_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_object_type_t, (int*)object_type);
}
int sai_deserialize_out_drop_reason(
    _In_ char *buffer,
    _Out_ sai_out_drop_reason_t *out_drop_reason)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_out_drop_reason_t, (int*)out_drop_reason);
}
int sai_deserialize_outseg_exp_mode(
    _In_ char *buffer,
    _Out_ sai_outseg_exp_mode_t *outseg_exp_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_exp_mode_t, (int*)outseg_exp_mode);
}
int sai_deserialize_outseg_ttl_mode(
    _In_ char *buffer,
    _Out_ sai_outseg_ttl_mode_t *outseg_ttl_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_ttl_mode_t, (int*)outseg_ttl_mode);
}
int sai_deserialize_outseg_type(
    _In_ char *buffer,
    _Out_ sai_outseg_type_t *outseg_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_outseg_type_t, (int*)outseg_type);
}
int sai_deserialize_packet_action(
    _In_ char *buffer,
    _Out_ sai_packet_action_t *packet_action)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_action_t, (int*)packet_action);
}
int sai_deserialize_packet_color(
    _In_ char *buffer,
    _Out_ sai_packet_color_t *packet_color)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_color_t, (int*)packet_color);
}
int sai_deserialize_packet_vlan(
    _In_ char *buffer,
    _Out_ sai_packet_vlan_t *packet_vlan)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_packet_vlan_t, (int*)packet_vlan);
}
int sai_deserialize_policer_color_source(
    _In_ char *buffer,
    _Out_ sai_policer_color_source_t *policer_color_source)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_color_source_t, (int*)policer_color_source);
}
int sai_deserialize_policer_mode(
    _In_ char *buffer,
    _Out_ sai_policer_mode_t *policer_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_mode_t, (int*)policer_mode);
}
int sai_deserialize_policer_stat(
    _In_ char *buffer,
    _Out_ sai_policer_stat_t *policer_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_policer_stat_t, (int*)policer_stat);
}
int sai_deserialize_port_breakout_mode_type(
    _In_ char *buffer,
    _Out_ sai_port_breakout_mode_type_t *port_breakout_mode_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_breakout_mode_type_t, (int*)port_breakout_mode_type);
}
int sai_deserialize_port_err_status(
    _In_ char *buffer,
    _Out_ sai_port_err_status_t *port_err_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_err_status_t, (int*)port_err_status);
}
int sai_deserialize_port_fec_mode(
    _In_ char *buffer,
    _Out_ sai_port_fec_mode_t *port_fec_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_fec_mode_t, (int*)port_fec_mode);
}
int sai_deserialize_port_flow_control_mode(
    _In_ char *buffer,
    _Out_ sai_port_flow_control_mode_t *port_flow_control_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_flow_control_mode_t, (int*)port_flow_control_mode);
}
int sai_deserialize_port_interface_type(
    _In_ char *buffer,
    _Out_ sai_port_interface_type_t *port_interface_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_interface_type_t, (int*)port_interface_type);
}
int sai_deserialize_port_internal_loopback_mode(
    _In_ char *buffer,
    _Out_ sai_port_internal_loopback_mode_t *port_internal_loopback_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_internal_loopback_mode_t, (int*)port_internal_loopback_mode);
}
int sai_deserialize_port_link_training_failure_status(
    _In_ char *buffer,
    _Out_ sai_port_link_training_failure_status_t *port_link_training_failure_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_link_training_failure_status_t, (int*)port_link_training_failure_status);
}
int sai_deserialize_port_link_training_rx_status(
    _In_ char *buffer,
    _Out_ sai_port_link_training_rx_status_t *port_link_training_rx_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_link_training_rx_status_t, (int*)port_link_training_rx_status);
}
int sai_deserialize_port_media_type(
    _In_ char *buffer,
    _Out_ sai_port_media_type_t *port_media_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_media_type_t, (int*)port_media_type);
}
int sai_deserialize_port_oper_status(
    _In_ char *buffer,
    _Out_ sai_port_oper_status_t *port_oper_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_oper_status_t, (int*)port_oper_status);
}
int sai_deserialize_port_pool_stat(
    _In_ char *buffer,
    _Out_ sai_port_pool_stat_t *port_pool_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_pool_stat_t, (int*)port_pool_stat);
}
int sai_deserialize_port_prbs_config(
    _In_ char *buffer,
    _Out_ sai_port_prbs_config_t *port_prbs_config)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_prbs_config_t, (int*)port_prbs_config);
}
int sai_deserialize_port_priority_flow_control_mode(
    _In_ char *buffer,
    _Out_ sai_port_priority_flow_control_mode_t *port_priority_flow_control_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_priority_flow_control_mode_t, (int*)port_priority_flow_control_mode);
}
int sai_deserialize_port_ptp_mode(
    _In_ char *buffer,
    _Out_ sai_port_ptp_mode_t *port_ptp_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_ptp_mode_t, (int*)port_ptp_mode);
}
int sai_deserialize_port_stat(
    _In_ char *buffer,
    _Out_ sai_port_stat_t *port_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_stat_t, (int*)port_stat);
}
int sai_deserialize_port_type(
    _In_ char *buffer,
    _Out_ sai_port_type_t *port_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_port_type_t, (int*)port_type);
}
int sai_deserialize_ptp_device_type(
    _In_ char *buffer,
    _Out_ sai_ptp_device_type_t *ptp_device_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_device_type_t, (int*)ptp_device_type);
}
int sai_deserialize_ptp_enable_based_type(
    _In_ char *buffer,
    _Out_ sai_ptp_enable_based_type_t *ptp_enable_based_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_enable_based_type_t, (int*)ptp_enable_based_type);
}
int sai_deserialize_ptp_tod_interface_format_type(
    _In_ char *buffer,
    _Out_ sai_ptp_tod_interface_format_type_t *ptp_tod_interface_format_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_tod_interface_format_type_t, (int*)ptp_tod_interface_format_type);
}
int sai_deserialize_ptp_tod_intf_mode(
    _In_ char *buffer,
    _Out_ sai_ptp_tod_intf_mode_t *ptp_tod_intf_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_ptp_tod_intf_mode_t, (int*)ptp_tod_intf_mode);
}
int sai_deserialize_qos_map_type(
    _In_ char *buffer,
    _Out_ sai_qos_map_type_t *qos_map_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_qos_map_type_t, (int*)qos_map_type);
}
int sai_deserialize_queue_pfc_deadlock_event_type(
    _In_ char *buffer,
    _Out_ sai_queue_pfc_deadlock_event_type_t *queue_pfc_deadlock_event_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_pfc_deadlock_event_type_t, (int*)queue_pfc_deadlock_event_type);
}
int sai_deserialize_queue_stat(
    _In_ char *buffer,
    _Out_ sai_queue_stat_t *queue_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_stat_t, (int*)queue_stat);
}
int sai_deserialize_queue_type(
    _In_ char *buffer,
    _Out_ sai_queue_type_t *queue_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_queue_type_t, (int*)queue_type);
}
int sai_deserialize_router_interface_stat(
    _In_ char *buffer,
    _Out_ sai_router_interface_stat_t *router_interface_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_router_interface_stat_t, (int*)router_interface_stat);
}
int sai_deserialize_router_interface_type(
    _In_ char *buffer,
    _Out_ sai_router_interface_type_t *router_interface_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_router_interface_type_t, (int*)router_interface_type);
}
int sai_deserialize_samplepacket_mode(
    _In_ char *buffer,
    _Out_ sai_samplepacket_mode_t *samplepacket_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_samplepacket_mode_t, (int*)samplepacket_mode);
}
int sai_deserialize_samplepacket_type(
    _In_ char *buffer,
    _Out_ sai_samplepacket_type_t *samplepacket_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_samplepacket_type_t, (int*)samplepacket_type);
}
int sai_deserialize_scheduling_type(
    _In_ char *buffer,
    _Out_ sai_scheduling_type_t *scheduling_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_scheduling_type_t, (int*)scheduling_type);
}
int sai_deserialize_segmentroute_sidlist_type(
    _In_ char *buffer,
    _Out_ sai_segmentroute_sidlist_type_t *segmentroute_sidlist_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_segmentroute_sidlist_type_t, (int*)segmentroute_sidlist_type);
}
int sai_deserialize_signal_degrade_status(
    _In_ char *buffer,
    _Out_ sai_signal_degrade_status_t *signal_degrade_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_signal_degrade_status_t, (int*)signal_degrade_status);
}
int sai_deserialize_stats_mode(
    _In_ char *buffer,
    _Out_ sai_stats_mode_t *stats_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_stats_mode_t, (int*)stats_mode);
}
int sai_deserialize_status(
    _In_ char *buffer,
    _Out_ sai_status_t *status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_status_t, (int*)status);
}
int sai_deserialize_stp_port_state(
    _In_ char *buffer,
    _Out_ sai_stp_port_state_t *stp_port_state)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_stp_port_state_t, (int*)stp_port_state);
}
//int sai_deserialize_switch_attr_extensions(
//    _In_ char *buffer,
//    _Out_ sai_switch_attr_extensions_t *switch_attr_extensions)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_attr_extensions_t, (int*)switch_attr_extensions);
//}
int sai_deserialize_switch_firmware_load_method(
    _In_ char *buffer,
    _Out_ sai_switch_firmware_load_method_t *switch_firmware_load_method)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_firmware_load_method_t, (int*)switch_firmware_load_method);
}
int sai_deserialize_switch_firmware_load_type(
    _In_ char *buffer,
    _Out_ sai_switch_firmware_load_type_t *switch_firmware_load_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_firmware_load_type_t, (int*)switch_firmware_load_type);
}
int sai_deserialize_switch_hardware_access_bus(
    _In_ char *buffer,
    _Out_ sai_switch_hardware_access_bus_t *switch_hardware_access_bus)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_hardware_access_bus_t, (int*)switch_hardware_access_bus);
}
int sai_deserialize_switch_mcast_snooping_capability(
    _In_ char *buffer,
    _Out_ sai_switch_mcast_snooping_capability_t *switch_mcast_snooping_capability)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_mcast_snooping_capability_t, (int*)switch_mcast_snooping_capability);
}
//int sai_deserialize_switch_notification_type(
//    _In_ char *buffer,
//    _Out_ sai_switch_notification_type_t *switch_notification_type)
//{
//    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_notification_type_t, (int*)switch_notification_type);
//}
int sai_deserialize_switch_oper_status(
    _In_ char *buffer,
    _Out_ sai_switch_oper_status_t *switch_oper_status)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_oper_status_t, (int*)switch_oper_status);
}
int sai_deserialize_switch_restart_type(
    _In_ char *buffer,
    _Out_ sai_switch_restart_type_t *switch_restart_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_restart_type_t, (int*)switch_restart_type);
}
int sai_deserialize_switch_stat(
    _In_ char *buffer,
    _Out_ sai_switch_stat_t *switch_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_stat_t, (int*)switch_stat);
}
int sai_deserialize_switch_switching_mode(
    _In_ char *buffer,
    _Out_ sai_switch_switching_mode_t *switch_switching_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_switching_mode_t, (int*)switch_switching_mode);
}
int sai_deserialize_switch_type(
    _In_ char *buffer,
    _Out_ sai_switch_type_t *switch_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_switch_type_t, (int*)switch_type);
}
int sai_deserialize_system_port_type(
    _In_ char *buffer,
    _Out_ sai_system_port_type_t *system_port_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_system_port_type_t, (int*)system_port_type);
}
int sai_deserialize_tam_bind_point_type(
    _In_ char *buffer,
    _Out_ sai_tam_bind_point_type_t *tam_bind_point_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_bind_point_type_t, (int*)tam_bind_point_type);
}
int sai_deserialize_tam_event_threshold_unit(
    _In_ char *buffer,
    _Out_ sai_tam_event_threshold_unit_t *tam_event_threshold_unit)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_event_threshold_unit_t, (int*)tam_event_threshold_unit);
}
int sai_deserialize_tam_event_type(
    _In_ char *buffer,
    _Out_ sai_tam_event_type_t *tam_event_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_event_type_t, (int*)tam_event_type);
}
int sai_deserialize_tam_int_presence_type(
    _In_ char *buffer,
    _Out_ sai_tam_int_presence_type_t *tam_int_presence_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_int_presence_type_t, (int*)tam_int_presence_type);
}
int sai_deserialize_tam_int_type(
    _In_ char *buffer,
    _Out_ sai_tam_int_type_t *tam_int_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_int_type_t, (int*)tam_int_type);
}
int sai_deserialize_tam_report_mode(
    _In_ char *buffer,
    _Out_ sai_tam_report_mode_t *tam_report_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_report_mode_t, (int*)tam_report_mode);
}
int sai_deserialize_tam_report_type(
    _In_ char *buffer,
    _Out_ sai_tam_report_type_t *tam_report_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_report_type_t, (int*)tam_report_type);
}
int sai_deserialize_tam_reporting_unit(
    _In_ char *buffer,
    _Out_ sai_tam_reporting_unit_t *tam_reporting_unit)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_reporting_unit_t, (int*)tam_reporting_unit);
}
int sai_deserialize_tam_tel_math_func_type(
    _In_ char *buffer,
    _Out_ sai_tam_tel_math_func_type_t *tam_tel_math_func_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_tel_math_func_type_t, (int*)tam_tel_math_func_type);
}
int sai_deserialize_tam_telemetry_type(
    _In_ char *buffer,
    _Out_ sai_tam_telemetry_type_t *tam_telemetry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_telemetry_type_t, (int*)tam_telemetry_type);
}
int sai_deserialize_tam_transport_auth_type(
    _In_ char *buffer,
    _Out_ sai_tam_transport_auth_type_t *tam_transport_auth_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_transport_auth_type_t, (int*)tam_transport_auth_type);
}
int sai_deserialize_tam_transport_type(
    _In_ char *buffer,
    _Out_ sai_tam_transport_type_t *tam_transport_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tam_transport_type_t, (int*)tam_transport_type);
}
int sai_deserialize_tlv_type(
    _In_ char *buffer,
    _Out_ sai_tlv_type_t *tlv_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tlv_type_t, (int*)tlv_type);
}
int sai_deserialize_tunnel_decap_ecn_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_decap_ecn_mode_t *tunnel_decap_ecn_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_decap_ecn_mode_t, (int*)tunnel_decap_ecn_mode);
}
int sai_deserialize_tunnel_dscp_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_dscp_mode_t *tunnel_dscp_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_dscp_mode_t, (int*)tunnel_dscp_mode);
}
int sai_deserialize_tunnel_encap_ecn_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_encap_ecn_mode_t *tunnel_encap_ecn_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_encap_ecn_mode_t, (int*)tunnel_encap_ecn_mode);
}
int sai_deserialize_tunnel_exp_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_exp_mode_t *tunnel_exp_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_exp_mode_t, (int*)tunnel_exp_mode);
}
int sai_deserialize_tunnel_map_type(
    _In_ char *buffer,
    _Out_ sai_tunnel_map_type_t *tunnel_map_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_map_type_t, (int*)tunnel_map_type);
}
int sai_deserialize_tunnel_mpls_pw_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_mpls_pw_mode_t *tunnel_mpls_pw_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_mpls_pw_mode_t, (int*)tunnel_mpls_pw_mode);
}
int sai_deserialize_tunnel_peer_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_peer_mode_t *tunnel_peer_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_peer_mode_t, (int*)tunnel_peer_mode);
}
int sai_deserialize_tunnel_stat(
    _In_ char *buffer,
    _Out_ sai_tunnel_stat_t *tunnel_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_stat_t, (int*)tunnel_stat);
}
int sai_deserialize_tunnel_term_table_entry_type(
    _In_ char *buffer,
    _Out_ sai_tunnel_term_table_entry_type_t *tunnel_term_table_entry_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_term_table_entry_type_t, (int*)tunnel_term_table_entry_type);
}
int sai_deserialize_tunnel_ttl_mode(
    _In_ char *buffer,
    _Out_ sai_tunnel_ttl_mode_t *tunnel_ttl_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_ttl_mode_t, (int*)tunnel_ttl_mode);
}
int sai_deserialize_tunnel_type(
    _In_ char *buffer,
    _Out_ sai_tunnel_type_t *tunnel_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_tunnel_type_t, (int*)tunnel_type);
}
int sai_deserialize_twamp_encapsulation_type(
    _In_ char *buffer,
    _Out_ sai_twamp_encapsulation_type_t *twamp_encapsulation_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_encapsulation_type_t, (int*)twamp_encapsulation_type);
}
int sai_deserialize_twamp_mode(
    _In_ char *buffer,
    _Out_ sai_twamp_mode_t *twamp_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_mode_t, (int*)twamp_mode);
}
int sai_deserialize_twamp_pkt_tx_mode(
    _In_ char *buffer,
    _Out_ sai_twamp_pkt_tx_mode_t *twamp_pkt_tx_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_pkt_tx_mode_t, (int*)twamp_pkt_tx_mode);
}
int sai_deserialize_twamp_session_auth_mode(
    _In_ char *buffer,
    _Out_ sai_twamp_session_auth_mode_t *twamp_session_auth_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_auth_mode_t, (int*)twamp_session_auth_mode);
}
int sai_deserialize_twamp_session_role(
    _In_ char *buffer,
    _Out_ sai_twamp_session_role_t *twamp_session_role)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_role_t, (int*)twamp_session_role);
}
int sai_deserialize_twamp_session_stats(
    _In_ char *buffer,
    _Out_ sai_twamp_session_stats_t *twamp_session_stats)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_session_stats_t, (int*)twamp_session_stats);
}
int sai_deserialize_twamp_timestamp_format(
    _In_ char *buffer,
    _Out_ sai_twamp_timestamp_format_t *twamp_timestamp_format)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_twamp_timestamp_format_t, (int*)twamp_timestamp_format);
}
int sai_deserialize_udf_base(
    _In_ char *buffer,
    _Out_ sai_udf_base_t *udf_base)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_udf_base_t, (int*)udf_base);
}
int sai_deserialize_udf_group_type(
    _In_ char *buffer,
    _Out_ sai_udf_group_type_t *udf_group_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_udf_group_type_t, (int*)udf_group_type);
}
int sai_deserialize_vlan_flood_control_type(
    _In_ char *buffer,
    _Out_ sai_vlan_flood_control_type_t *vlan_flood_control_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_flood_control_type_t, (int*)vlan_flood_control_type);
}
int sai_deserialize_vlan_mcast_lookup_key_type(
    _In_ char *buffer,
    _Out_ sai_vlan_mcast_lookup_key_type_t *vlan_mcast_lookup_key_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_mcast_lookup_key_type_t, (int*)vlan_mcast_lookup_key_type);
}
int sai_deserialize_vlan_stat(
    _In_ char *buffer,
    _Out_ sai_vlan_stat_t *vlan_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_stat_t, (int*)vlan_stat);
}
int sai_deserialize_vlan_tagging_mode(
    _In_ char *buffer,
    _Out_ sai_vlan_tagging_mode_t *vlan_tagging_mode)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_vlan_tagging_mode_t, (int*)vlan_tagging_mode);
}
int sai_deserialize_y1731_meg_type(
    _In_ char *buffer,
    _Out_ sai_y1731_meg_type_t *y1731_meg_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_meg_type_t, (int*)y1731_meg_type);
}
int sai_deserialize_y1731_session_ccm_period(
    _In_ char *buffer,
    _Out_ sai_y1731_session_ccm_period_t *y1731_session_ccm_period)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_ccm_period_t, (int*)y1731_session_ccm_period);
}
int sai_deserialize_y1731_session_direction(
    _In_ char *buffer,
    _Out_ sai_y1731_session_direction_t *y1731_session_direction)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_direction_t, (int*)y1731_session_direction);
}
int sai_deserialize_y1731_session_lm_type(
    _In_ char *buffer,
    _Out_ sai_y1731_session_lm_type_t *y1731_session_lm_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_lm_type_t, (int*)y1731_session_lm_type);
}
int sai_deserialize_y1731_session_notify_event_type(
    _In_ char *buffer,
    _Out_ sai_y1731_session_notify_event_type_t *y1731_session_notify_event_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_notify_event_type_t, (int*)y1731_session_notify_event_type);
}
int sai_deserialize_y1731_session_perf_monitor_offload_type(
    _In_ char *buffer,
    _Out_ sai_y1731_session_perf_monitor_offload_type_t *y1731_session_perf_monitor_offload_type)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_perf_monitor_offload_type_t, (int*)y1731_session_perf_monitor_offload_type);
}
int sai_deserialize_y1731_session_stat(
    _In_ char *buffer,
    _Out_ sai_y1731_session_stat_t *y1731_session_stat)
{
    return sai_deserialize_enum(buffer, &ctc_sai_metadata_enum_sai_y1731_session_stat_t, (int*)y1731_session_stat);
}

/* Expect macros */

#define EXPECT(x) { \
    if (strncmp(buf, x, sizeof(x) - 1) == 0) { buf += sizeof(x) - 1; } \
    else { \
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "expected '%s' but got '%.*s...'", x, (int)sizeof(x), buf); \
        return SAI_SERIALIZE_ERROR; } }
#define EXPECT_QUOTE     EXPECT("\"")
#define EXPECT_KEY(k)    EXPECT("\"" k "\":")
#define EXPECT_NEXT_KEY(k) { EXPECT(","); EXPECT_KEY(k); }
#define EXPECT_CHECK(expr, suffix) {                                 \
    ret = (expr);                                                  \
    if (ret < 0) {                                                 \
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "failed to deserialize " #suffix "");      \
        return SAI_SERIALIZE_ERROR; }                              \
    buf += ret; }
#define EXPECT_QUOTE_CHECK(expr, suffix) {\
    EXPECT_QUOTE; EXPECT_CHECK(expr, suffix); EXPECT_QUOTE; }

/* Deserialize structs */

int sai_deserialize_acl_action_data(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_acl_action_data_t *acl_action_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("enable");

    EXPECT_CHECK(sai_deserialize_bool(buf, &acl_action_data->enable), bool);

    if (acl_action_data->enable == true)
    {
        EXPECT_NEXT_KEY("parameter");

        EXPECT_CHECK(sai_deserialize_acl_action_parameter(buf, meta, &acl_action_data->parameter), acl_action_parameter);
    }
    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_capability(
    _In_ char *buf,
    _Out_ sai_acl_capability_t *acl_capability)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("is_action_list_mandatory");

    EXPECT_CHECK(sai_deserialize_bool(buf, &acl_capability->is_action_list_mandatory), bool);

    EXPECT_NEXT_KEY("action_list");

    EXPECT_CHECK(sai_deserialize_enum_list(buf, &ctc_sai_metadata_enum_sai_acl_action_type_t, &acl_capability->action_list), enum_list);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_field_data(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_acl_field_data_t *acl_field_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("enable");

    EXPECT_CHECK(sai_deserialize_bool(buf, &acl_field_data->enable), bool);

    if (acl_field_data->enable == true)
    {
        EXPECT_NEXT_KEY("mask");

        EXPECT_CHECK(sai_deserialize_acl_field_data_mask(buf, meta, &acl_field_data->mask), acl_field_data_mask);
    }
    if (acl_field_data->enable == true)
    {
        EXPECT_NEXT_KEY("data");

        EXPECT_CHECK(sai_deserialize_acl_field_data_data(buf, meta, &acl_field_data->data), acl_field_data_data);
    }
    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_resource_list(
    _In_ char *buf,
    _Out_ sai_acl_resource_list_t *acl_resource_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &acl_resource_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        acl_resource_list->list = NULL;

        buf += 4;
    }
    else
    {
        acl_resource_list->list = calloc((acl_resource_list->count), sizeof(sai_acl_resource_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < acl_resource_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_acl_resource(buf, &acl_resource_list->list[idx]), acl_resource);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_resource(
    _In_ char *buf,
    _Out_ sai_acl_resource_t *acl_resource)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("stage");

    EXPECT_QUOTE_CHECK(sai_deserialize_acl_stage(buf, &acl_resource->stage), acl_stage);

    EXPECT_NEXT_KEY("bind_point");

    EXPECT_QUOTE_CHECK(sai_deserialize_acl_bind_point_type(buf, &acl_resource->bind_point), acl_bind_point_type);

    EXPECT_NEXT_KEY("avail_num");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &acl_resource->avail_num), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_attr_capability(
    _In_ char *buf,
    _Out_ sai_attr_capability_t *attr_capability)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("create_implemented");

    EXPECT_CHECK(sai_deserialize_bool(buf, &attr_capability->create_implemented), bool);

    EXPECT_NEXT_KEY("set_implemented");

    EXPECT_CHECK(sai_deserialize_bool(buf, &attr_capability->set_implemented), bool);

    EXPECT_NEXT_KEY("get_implemented");

    EXPECT_CHECK(sai_deserialize_bool(buf, &attr_capability->get_implemented), bool);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_bfd_session_state_notification(
    _In_ char *buf,
    _Out_ sai_bfd_session_state_notification_t *bfd_session_state_notification)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("bfd_session_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &bfd_session_state_notification->bfd_session_id), object_id);

    EXPECT_NEXT_KEY("session_state");

    EXPECT_QUOTE_CHECK(sai_deserialize_bfd_session_state(buf, &bfd_session_state_notification->session_state), bfd_session_state);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_bool_list(
    _In_ char *buf,
    _Out_ sai_bool_list_t *bool_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &bool_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        bool_list->list = NULL;

        buf += 4;
    }
    else
    {
        bool_list->list = calloc((bool_list->count), sizeof(bool));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < bool_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_bool(buf, &bool_list->list[idx]), bool);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_captured_timespec(
    _In_ char *buf,
    _Out_ sai_captured_timespec_t *captured_timespec)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("timestamp");

    EXPECT_CHECK(sai_deserialize_timespec(buf, &captured_timespec->timestamp), timespec);

    EXPECT_NEXT_KEY("secquence_id");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &captured_timespec->secquence_id), uint16);

    EXPECT_NEXT_KEY("port_id");

    EXPECT_CHECK(sai_deserialize_uint64(buf, &captured_timespec->port_id), uint64);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_fabric_port_reachability(
    _In_ char *buf,
    _Out_ sai_fabric_port_reachability_t *fabric_port_reachability)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &fabric_port_reachability->switch_id), uint32);

    EXPECT_NEXT_KEY("reachable");

    EXPECT_CHECK(sai_deserialize_bool(buf, &fabric_port_reachability->reachable), bool);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_fdb_entry(
    _In_ char *buf,
    _Out_ sai_fdb_entry_t *fdb_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &fdb_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("mac_address");

    EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, fdb_entry->mac_address), mac);

    EXPECT_NEXT_KEY("bv_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &fdb_entry->bv_id), object_id);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_fdb_event_notification_data(
    _In_ char *buf,
    _Out_ sai_fdb_event_notification_data_t *fdb_event_notification_data)
{
#if 0
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("event_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_fdb_event(buf, &fdb_event_notification_data->event_type), fdb_event);

    EXPECT_NEXT_KEY("fdb_entry");

    EXPECT_CHECK(sai_deserialize_fdb_entry(buf, &fdb_event_notification_data->fdb_entry), fdb_entry);

    EXPECT_NEXT_KEY("attr_count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &fdb_event_notification_data->attr_count), uint32);

    EXPECT_NEXT_KEY("attr");

    if (strncmp(buf, "null", 4) == 0)
    {
        fdb_event_notification_data->attr = NULL;

        buf += 4;
    }
    else
    {
        fdb_event_notification_data->attr = calloc((fdb_event_notification_data->attr_count), sizeof(sai_attribute_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < fdb_event_notification_data->attr_count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_attribute(buf, &fdb_event_notification_data->attr[idx]), attribute);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
#endif

    return 0;
}
int sai_deserialize_hmac(
    _In_ char *buf,
    _Out_ sai_hmac_t *hmac)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("key_id");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &hmac->key_id), uint32);

    EXPECT_NEXT_KEY("hmac");

    {
        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint32(buf, &hmac->hmac[idx]), uint32);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_inseg_entry(
    _In_ char *buf,
    _Out_ sai_inseg_entry_t *inseg_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &inseg_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("label");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &inseg_entry->label), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_ip_address_list(
    _In_ char *buf,
    _Out_ sai_ip_address_list_t *ip_address_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &ip_address_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        ip_address_list->list = NULL;

        buf += 4;
    }
    else
    {
        ip_address_list->list = calloc((ip_address_list->count), sizeof(sai_ip_address_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < ip_address_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &ip_address_list->list[idx]), ip_address);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_ipmc_entry(
    _In_ char *buf,
    _Out_ sai_ipmc_entry_t *ipmc_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &ipmc_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("vr_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &ipmc_entry->vr_id), object_id);

    EXPECT_NEXT_KEY("type");

    EXPECT_QUOTE_CHECK(sai_deserialize_ipmc_entry_type(buf, &ipmc_entry->type), ipmc_entry_type);

    EXPECT_NEXT_KEY("destination");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &ipmc_entry->destination), ip_address);

    EXPECT_NEXT_KEY("source");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &ipmc_entry->source), ip_address);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_l2mc_entry(
    _In_ char *buf,
    _Out_ sai_l2mc_entry_t *l2mc_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &l2mc_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("bv_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &l2mc_entry->bv_id), object_id);

    EXPECT_NEXT_KEY("type");

    EXPECT_QUOTE_CHECK(sai_deserialize_l2mc_entry_type(buf, &l2mc_entry->type), l2mc_entry_type);

    EXPECT_NEXT_KEY("destination");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &l2mc_entry->destination), ip_address);

    EXPECT_NEXT_KEY("source");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &l2mc_entry->source), ip_address);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_map_list(
    _In_ char *buf,
    _Out_ sai_map_list_t *map_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &map_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        map_list->list = NULL;

        buf += 4;
    }
    else
    {
        map_list->list = calloc((map_list->count), sizeof(sai_map_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < map_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_map(buf, &map_list->list[idx]), map);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_map(
    _In_ char *buf,
    _Out_ sai_map_t *map)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("key");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &map->key), uint32);

    EXPECT_NEXT_KEY("value");

    EXPECT_CHECK(sai_deserialize_int32(buf, &map->value), int32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_mcast_fdb_entry(
    _In_ char *buf,
    _Out_ sai_mcast_fdb_entry_t *mcast_fdb_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &mcast_fdb_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("mac_address");

    EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, mcast_fdb_entry->mac_address), mac);

    EXPECT_NEXT_KEY("bv_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &mcast_fdb_entry->bv_id), object_id);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_buffer_event(
    _In_ char *buf,
    _Out_ sai_monitor_buffer_event_t *monitor_buffer_event)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("buffer_monitor_event_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_buffer_event->buffer_monitor_event_port), object_id);

    EXPECT_NEXT_KEY("buffer_monitor_event_total_cnt");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_buffer_event->buffer_monitor_event_total_cnt), uint32);

    EXPECT_NEXT_KEY("buffer_monitor_event_port_unicast_cnt");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_buffer_event->buffer_monitor_event_port_unicast_cnt), uint32);

    EXPECT_NEXT_KEY("buffer_monitor_event_port_multicast_cnt");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_buffer_event->buffer_monitor_event_port_multicast_cnt), uint32);

    EXPECT_NEXT_KEY("buffer_monitor_event_state");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &monitor_buffer_event->buffer_monitor_event_state), uint8);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_buffer_notification_data(
    _In_ char *buf,
    _Out_ sai_monitor_buffer_notification_data_t *monitor_buffer_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("monitor_buffer_monitor_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_buffer_notification_data->monitor_buffer_monitor_id), object_id);

    EXPECT_NEXT_KEY("buffer_monitor_message_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_buffer_monitor_message_type(buf, &monitor_buffer_notification_data->buffer_monitor_message_type), buffer_monitor_message_type);

    EXPECT_NEXT_KEY("buffer_monitor_based_on_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_buffer_monitor_based_on_type(buf, &monitor_buffer_notification_data->buffer_monitor_based_on_type), buffer_monitor_based_on_type);

    EXPECT_NEXT_KEY("u");

    EXPECT_CHECK(sai_deserialize_monitor_buffer_data(buf, monitor_buffer_notification_data->buffer_monitor_message_type, &monitor_buffer_notification_data->u), monitor_buffer_data);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_buffer_stats(
    _In_ char *buf,
    _Out_ sai_monitor_buffer_stats_t *monitor_buffer_stats)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("buffer_monitor_stats_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_buffer_stats->buffer_monitor_stats_port), object_id);

    EXPECT_NEXT_KEY("buffer_monitor_stats_direction");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_buffer_stats->buffer_monitor_stats_direction), uint32);

    EXPECT_NEXT_KEY("buffer_monitor_stats_port_cnt");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_buffer_stats->buffer_monitor_stats_port_cnt), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_latency_event(
    _In_ char *buf,
    _Out_ sai_monitor_latency_event_t *monitor_latency_event)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("latency_monitor_event_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_latency_event->latency_monitor_event_port), object_id);

    EXPECT_NEXT_KEY("latency_monitor_event_latency");

    EXPECT_CHECK(sai_deserialize_uint64(buf, &monitor_latency_event->latency_monitor_event_latency), uint64);

    EXPECT_NEXT_KEY("latency_monitor_event_level");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &monitor_latency_event->latency_monitor_event_level), uint8);

    EXPECT_NEXT_KEY("latency_monitor_event_state");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &monitor_latency_event->latency_monitor_event_state), uint8);

    EXPECT_NEXT_KEY("latency_monitor_event_source_port");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_latency_event->latency_monitor_event_source_port), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_latency_notification_data(
    _In_ char *buf,
    _Out_ sai_monitor_latency_notification_data_t *monitor_latency_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("monitor_latency_monitor_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_latency_notification_data->monitor_latency_monitor_id), object_id);

    EXPECT_NEXT_KEY("latency_monitor_message_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_latency_monitor_message_type(buf, &monitor_latency_notification_data->latency_monitor_message_type), latency_monitor_message_type);

    EXPECT_NEXT_KEY("u");

    EXPECT_CHECK(sai_deserialize_monitor_latency_data(buf, monitor_latency_notification_data->latency_monitor_message_type, &monitor_latency_notification_data->u), monitor_latency_data);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_latency_stats(
    _In_ char *buf,
    _Out_ sai_monitor_latency_stats_t *monitor_latency_stats)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("latency_monitor_stats_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_latency_stats->latency_monitor_stats_port), object_id);

    EXPECT_NEXT_KEY("latency_monitor_stats_level_cnt");

    {
        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_latency_stats->latency_monitor_stats_level_cnt[idx]), uint32);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_mburst_stats(
    _In_ char *buf,
    _Out_ sai_monitor_mburst_stats_t *monitor_mburst_stats)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("buffer_monitor_microburst_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &monitor_mburst_stats->buffer_monitor_microburst_port), object_id);

    EXPECT_NEXT_KEY("buffer_monitor_microburst_threshold_cnt");

    {
        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < 8; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint32(buf, &monitor_mburst_stats->buffer_monitor_microburst_threshold_cnt[idx]), uint32);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_nat_entry_data(
    _In_ char *buf,
    _Out_ sai_nat_entry_data_t *nat_entry_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("key");

    EXPECT_CHECK(sai_deserialize_nat_entry_key(buf, &nat_entry_data->key), nat_entry_key);

    EXPECT_NEXT_KEY("mask");

    EXPECT_CHECK(sai_deserialize_nat_entry_mask(buf, &nat_entry_data->mask), nat_entry_mask);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_nat_entry_key(
    _In_ char *buf,
    _Out_ sai_nat_entry_key_t *nat_entry_key)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("src_ip");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &nat_entry_key->src_ip), ip4);

    EXPECT_NEXT_KEY("dst_ip");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &nat_entry_key->dst_ip), ip4);

    EXPECT_NEXT_KEY("proto");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &nat_entry_key->proto), uint8);

    EXPECT_NEXT_KEY("l4_src_port");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &nat_entry_key->l4_src_port), uint16);

    EXPECT_NEXT_KEY("l4_dst_port");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &nat_entry_key->l4_dst_port), uint16);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_nat_entry_mask(
    _In_ char *buf,
    _Out_ sai_nat_entry_mask_t *nat_entry_mask)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("src_ip");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &nat_entry_mask->src_ip), ip4);

    EXPECT_NEXT_KEY("dst_ip");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &nat_entry_mask->dst_ip), ip4);

    EXPECT_NEXT_KEY("proto");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &nat_entry_mask->proto), uint8);

    EXPECT_NEXT_KEY("l4_src_port");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &nat_entry_mask->l4_src_port), uint16);

    EXPECT_NEXT_KEY("l4_dst_port");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &nat_entry_mask->l4_dst_port), uint16);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_nat_entry(
    _In_ char *buf,
    _Out_ sai_nat_entry_t *nat_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &nat_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("vr_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &nat_entry->vr_id), object_id);

    EXPECT_NEXT_KEY("nat_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_nat_type(buf, &nat_entry->nat_type), nat_type);

    EXPECT_NEXT_KEY("data");

    EXPECT_CHECK(sai_deserialize_nat_entry_data(buf, &nat_entry->data), nat_entry_data);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_neighbor_entry(
    _In_ char *buf,
    _Out_ sai_neighbor_entry_t *neighbor_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &neighbor_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("rif_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &neighbor_entry->rif_id), object_id);

    EXPECT_NEXT_KEY("ip_address");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &neighbor_entry->ip_address), ip_address);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_object_key(
    _In_ char *buf,
    _In_ sai_object_type_t object_type,
    _Out_ sai_object_key_t *object_key)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("key");

    EXPECT_CHECK(sai_deserialize_object_key_entry(buf, object_type, &object_key->key), object_key_entry);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_object_list(
    _In_ char *buf,
    _Out_ sai_object_list_t *object_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &object_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        object_list->list = NULL;

        buf += 4;
    }
    else
    {
        object_list->list = calloc((object_list->count), sizeof(sai_object_id_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < object_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &object_list->list[idx]), object_id);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_object_meta_key(
    _In_ char *buf,
    _Out_ ctc_sai_object_meta_key_t *object_meta_key)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("objecttype");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_type(buf, &object_meta_key->objecttype), object_type);

    EXPECT_NEXT_KEY("objectkey");

    EXPECT_CHECK(sai_deserialize_object_key(buf, object_meta_key->objecttype, &object_meta_key->objectkey), object_key);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_packet_event_ptp_tx_notification_data(
    _In_ char *buf,
    _Out_ sai_packet_event_ptp_tx_notification_data_t *packet_event_ptp_tx_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("tx_port");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &packet_event_ptp_tx_notification_data->tx_port), object_id);

    EXPECT_NEXT_KEY("msg_type");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &packet_event_ptp_tx_notification_data->msg_type), uint8);

    EXPECT_NEXT_KEY("ptp_seq_id");

    EXPECT_CHECK(sai_deserialize_uint16(buf, &packet_event_ptp_tx_notification_data->ptp_seq_id), uint16);

    EXPECT_NEXT_KEY("tx_timestamp");

    EXPECT_CHECK(sai_deserialize_timespec(buf, &packet_event_ptp_tx_notification_data->tx_timestamp), timespec);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_port_err_status_list(
    _In_ char *buf,
    _Out_ sai_port_err_status_list_t *port_err_status_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &port_err_status_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        port_err_status_list->list = NULL;

        buf += 4;
    }
    else
    {
        port_err_status_list->list = calloc((port_err_status_list->count), sizeof(sai_port_err_status_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < port_err_status_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_QUOTE_CHECK(sai_deserialize_port_err_status(buf, &port_err_status_list->list[idx]), port_err_status);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_port_eye_values_list(
    _In_ char *buf,
    _Out_ sai_port_eye_values_list_t *port_eye_values_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &port_eye_values_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        port_eye_values_list->list = NULL;

        buf += 4;
    }
    else
    {
        port_eye_values_list->list = calloc((port_eye_values_list->count), sizeof(sai_port_lane_eye_values_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < port_eye_values_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_port_lane_eye_values(buf, &port_eye_values_list->list[idx]), port_lane_eye_values);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_port_lane_eye_values(
    _In_ char *buf,
    _Out_ sai_port_lane_eye_values_t *port_lane_eye_values)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("lane");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &port_lane_eye_values->lane), uint32);

    EXPECT_NEXT_KEY("left");

    EXPECT_CHECK(sai_deserialize_int32(buf, &port_lane_eye_values->left), int32);

    EXPECT_NEXT_KEY("right");

    EXPECT_CHECK(sai_deserialize_int32(buf, &port_lane_eye_values->right), int32);

    EXPECT_NEXT_KEY("up");

    EXPECT_CHECK(sai_deserialize_int32(buf, &port_lane_eye_values->up), int32);

    EXPECT_NEXT_KEY("down");

    EXPECT_CHECK(sai_deserialize_int32(buf, &port_lane_eye_values->down), int32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_port_oper_status_notification(
    _In_ char *buf,
    _Out_ sai_port_oper_status_notification_t *port_oper_status_notification)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("port_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &port_oper_status_notification->port_id), object_id);

    EXPECT_NEXT_KEY("port_state");

    EXPECT_QUOTE_CHECK(sai_deserialize_port_oper_status(buf, &port_oper_status_notification->port_state), port_oper_status);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_port_sd_notification(
    _In_ char *buf,
    _Out_ sai_port_sd_notification_t *port_sd_notification)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("port_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &port_sd_notification->port_id), object_id);

    EXPECT_NEXT_KEY("sd_status");

    EXPECT_QUOTE_CHECK(sai_deserialize_signal_degrade_status(buf, &port_sd_notification->sd_status), signal_degrade_status);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_qos_map_list(
    _In_ char *buf,
    _Out_ sai_qos_map_list_t *qos_map_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &qos_map_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        qos_map_list->list = NULL;

        buf += 4;
    }
    else
    {
        qos_map_list->list = calloc((qos_map_list->count), sizeof(sai_qos_map_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < qos_map_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_qos_map(buf, &qos_map_list->list[idx]), qos_map);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_qos_map_params(
    _In_ char *buf,
    _Out_ sai_qos_map_params_t *qos_map_params)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("tc");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->tc), uint8);

    EXPECT_NEXT_KEY("dscp");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->dscp), uint8);

    EXPECT_NEXT_KEY("dot1p");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->dot1p), uint8);

    EXPECT_NEXT_KEY("prio");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->prio), uint8);

    EXPECT_NEXT_KEY("pg");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->pg), uint8);

    EXPECT_NEXT_KEY("queue_index");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->queue_index), uint8);

    EXPECT_NEXT_KEY("color");

    EXPECT_QUOTE_CHECK(sai_deserialize_packet_color(buf, &qos_map_params->color), packet_color);

    EXPECT_NEXT_KEY("mpls_exp");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &qos_map_params->mpls_exp), uint8);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_qos_map(
    _In_ char *buf,
    _Out_ sai_qos_map_t *qos_map)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("key");

    EXPECT_CHECK(sai_deserialize_qos_map_params(buf, &qos_map->key), qos_map_params);

    EXPECT_NEXT_KEY("value");

    EXPECT_CHECK(sai_deserialize_qos_map_params(buf, &qos_map->value), qos_map_params);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_queue_deadlock_notification_data(
    _In_ char *buf,
    _Out_ sai_queue_deadlock_notification_data_t *queue_deadlock_notification_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("queue_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &queue_deadlock_notification_data->queue_id), object_id);

    EXPECT_NEXT_KEY("event");

    EXPECT_QUOTE_CHECK(sai_deserialize_queue_pfc_deadlock_event_type(buf, &queue_deadlock_notification_data->event), queue_pfc_deadlock_event_type);

    EXPECT_NEXT_KEY("app_managed_recovery");

    EXPECT_CHECK(sai_deserialize_bool(buf, &queue_deadlock_notification_data->app_managed_recovery), bool);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_route_entry(
    _In_ char *buf,
    _Out_ sai_route_entry_t *route_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("switch_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &route_entry->switch_id), object_id);

    EXPECT_NEXT_KEY("vr_id");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &route_entry->vr_id), object_id);

    EXPECT_NEXT_KEY("destination");

    EXPECT_QUOTE_CHECK(sai_deserialize_ip_prefix(buf, &route_entry->destination), ip_prefix);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_s16_list(
    _In_ char *buf,
    _Out_ sai_s16_list_t *s16_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &s16_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        s16_list->list = NULL;

        buf += 4;
    }
    else
    {
        s16_list->list = calloc((s16_list->count), sizeof(int16_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < s16_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_int16(buf, &s16_list->list[idx]), int16);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_s32_list(
    _In_ char *buf,
    _Out_ sai_s32_list_t *s32_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &s32_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        s32_list->list = NULL;

        buf += 4;
    }
    else
    {
        s32_list->list = calloc((s32_list->count), sizeof(int32_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < s32_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_int32(buf, &s32_list->list[idx]), int32);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_s32_range(
    _In_ char *buf,
    _Out_ sai_s32_range_t *s32_range)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("min");

    EXPECT_CHECK(sai_deserialize_int32(buf, &s32_range->min), int32);

    EXPECT_NEXT_KEY("max");

    EXPECT_CHECK(sai_deserialize_int32(buf, &s32_range->max), int32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_s8_list(
    _In_ char *buf,
    _Out_ sai_s8_list_t *s8_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &s8_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        s8_list->list = NULL;

        buf += 4;
    }
    else
    {
        s8_list->list = calloc((s8_list->count), sizeof(int8_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < s8_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_int8(buf, &s8_list->list[idx]), int8);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_segment_list(
    _In_ char *buf,
    _Out_ sai_segment_list_t *segment_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &segment_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        segment_list->list = NULL;

        buf += 4;
    }
    else
    {
        segment_list->list = calloc((segment_list->count), sizeof(sai_ip6_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < segment_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, segment_list->list[idx]), ip6);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_system_port_config_list(
    _In_ char *buf,
    _Out_ sai_system_port_config_list_t *system_port_config_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        system_port_config_list->list = NULL;

        buf += 4;
    }
    else
    {
        system_port_config_list->list = calloc((system_port_config_list->count), sizeof(sai_system_port_config_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < system_port_config_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_system_port_config(buf, &system_port_config_list->list[idx]), system_port_config);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_system_port_config(
    _In_ char *buf,
    _Out_ sai_system_port_config_t *system_port_config)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("port_id");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->port_id), uint32);

    EXPECT_NEXT_KEY("attached_switch_id");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->attached_switch_id), uint32);

    EXPECT_NEXT_KEY("attached_core_index");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->attached_core_index), uint32);

    EXPECT_NEXT_KEY("attached_core_port_index");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->attached_core_port_index), uint32);

    EXPECT_NEXT_KEY("speed");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->speed), uint32);

    EXPECT_NEXT_KEY("num_voq");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &system_port_config->num_voq), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_timeoffset(
    _In_ char *buf,
    _Out_ sai_timeoffset_t *timeoffset)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("flag");

    EXPECT_CHECK(sai_deserialize_uint8(buf, &timeoffset->flag), uint8);

    EXPECT_NEXT_KEY("value");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &timeoffset->value), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_timespec(
    _In_ char *buf,
    _Out_ sai_timespec_t *timespec)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("tv_sec");

    EXPECT_CHECK(sai_deserialize_uint64(buf, &timespec->tv_sec), uint64);

    EXPECT_NEXT_KEY("tv_nsec");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &timespec->tv_nsec), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_tlv_list(
    _In_ char *buf,
    _Out_ sai_tlv_list_t *tlv_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &tlv_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        tlv_list->list = NULL;

        buf += 4;
    }
    else
    {
        tlv_list->list = calloc((tlv_list->count), sizeof(sai_tlv_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < tlv_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_tlv(buf, &tlv_list->list[idx]), tlv);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_tlv(
    _In_ char *buf,
    _Out_ sai_tlv_t *tlv)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("tlv_type");

    EXPECT_QUOTE_CHECK(sai_deserialize_tlv_type(buf, &tlv->tlv_type), tlv_type);

    EXPECT_NEXT_KEY("entry");

    EXPECT_CHECK(sai_deserialize_tlv_entry(buf, tlv->tlv_type, &tlv->entry), tlv_entry);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_u16_list(
    _In_ char *buf,
    _Out_ sai_u16_list_t *u16_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &u16_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        u16_list->list = NULL;

        buf += 4;
    }
    else
    {
        u16_list->list = calloc((u16_list->count), sizeof(uint16_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < u16_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint16(buf, &u16_list->list[idx]), uint16);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_u32_list(
    _In_ char *buf,
    _Out_ sai_u32_list_t *u32_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &u32_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        u32_list->list = NULL;

        buf += 4;
    }
    else
    {
        u32_list->list = calloc((u32_list->count), sizeof(uint32_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < u32_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint32(buf, &u32_list->list[idx]), uint32);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_u32_range(
    _In_ char *buf,
    _Out_ sai_u32_range_t *u32_range)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("min");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &u32_range->min), uint32);

    EXPECT_NEXT_KEY("max");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &u32_range->max), uint32);

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_u8_list(
    _In_ char *buf,
    _Out_ sai_u8_list_t *u8_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &u8_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        u8_list->list = NULL;

        buf += 4;
    }
    else
    {
        u8_list->list = calloc((u8_list->count), sizeof(uint8_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < u8_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint8(buf, &u8_list->list[idx]), uint8);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_vlan_list(
    _In_ char *buf,
    _Out_ sai_vlan_list_t *vlan_list)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("count");

    EXPECT_CHECK(sai_deserialize_uint32(buf, &vlan_list->count), uint32);

    EXPECT_NEXT_KEY("list");

    if (strncmp(buf, "null", 4) == 0)
    {
        vlan_list->list = NULL;

        buf += 4;
    }
    else
    {
        vlan_list->list = calloc((vlan_list->count), sizeof(sai_vlan_id_t));

        EXPECT("[");

        uint32_t idx;

        for (idx = 0; idx < vlan_list->count; idx++)
        {
            if (idx != 0)
            {
                EXPECT(",");
            }

            EXPECT_CHECK(sai_deserialize_uint16(buf, &vlan_list->list[idx]), uint16);
        }

        EXPECT("]");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_y1731_session_event_notification(
    _In_ char *buf,
    _Out_ sai_y1731_session_event_notification_t *y1731_session_event_notification)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    EXPECT_KEY("y1731_oid");

    EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &y1731_session_event_notification->y1731_oid), object_id);

    EXPECT_NEXT_KEY("session_event_list");

    EXPECT_CHECK(sai_deserialize_s32_list(buf, &y1731_session_event_notification->session_event_list), s32_list);

    EXPECT("}");

    return (int)(buf - begin_buf);
}

/* Deserialize unions */

int sai_deserialize_acl_action_parameter(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_acl_action_parameter_t *acl_action_parameter)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_BOOL)
    {
        EXPECT_KEY("booldata");

        EXPECT_CHECK(sai_deserialize_bool(buf, &acl_action_parameter->booldata), bool);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT8)
    {
        EXPECT_KEY("u8");

        EXPECT_CHECK(sai_deserialize_uint8(buf, &acl_action_parameter->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT8)
    {
        EXPECT_KEY("s8");

        EXPECT_CHECK(sai_deserialize_int8(buf, &acl_action_parameter->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT16)
    {
        EXPECT_KEY("u16");

        EXPECT_CHECK(sai_deserialize_uint16(buf, &acl_action_parameter->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT16)
    {
        EXPECT_KEY("s16");

        EXPECT_CHECK(sai_deserialize_int16(buf, &acl_action_parameter->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT32)
    {
        EXPECT_KEY("u32");

        EXPECT_CHECK(sai_deserialize_uint32(buf, &acl_action_parameter->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT32)
    {
        EXPECT_KEY("s32");

        EXPECT_CHECK(sai_deserialize_enum(buf, meta->enummetadata, &acl_action_parameter->s32), enum);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_MAC)
    {
        EXPECT_KEY("mac");

        EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, acl_action_parameter->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV4)
    {
        EXPECT_KEY("ip4");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &acl_action_parameter->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV6)
    {
        EXPECT_KEY("ip6");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, acl_action_parameter->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_ID)
    {
        EXPECT_KEY("oid");

        EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &acl_action_parameter->oid), object_id);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST)
    {
        EXPECT_KEY("objlist");

        EXPECT_CHECK(sai_deserialize_object_list(buf, &acl_action_parameter->objlist), object_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IP_ADDRESS)
    {
        EXPECT_KEY("ipaddr");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &acl_action_parameter->ipaddr), ip_address);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_acl_action_parameter_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_field_data_data(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_acl_field_data_data_t *acl_field_data_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_BOOL)
    {
        EXPECT_KEY("booldata");

        EXPECT_CHECK(sai_deserialize_bool(buf, &acl_field_data_data->booldata), bool);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8)
    {
        EXPECT_KEY("u8");

        EXPECT_CHECK(sai_deserialize_uint8(buf, &acl_field_data_data->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8)
    {
        EXPECT_KEY("s8");

        EXPECT_CHECK(sai_deserialize_int8(buf, &acl_field_data_data->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16)
    {
        EXPECT_KEY("u16");

        EXPECT_CHECK(sai_deserialize_uint16(buf, &acl_field_data_data->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16)
    {
        EXPECT_KEY("s16");

        EXPECT_CHECK(sai_deserialize_int16(buf, &acl_field_data_data->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32)
    {
        EXPECT_KEY("u32");

        EXPECT_CHECK(sai_deserialize_uint32(buf, &acl_field_data_data->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32)
    {
        EXPECT_KEY("s32");

        EXPECT_CHECK(sai_deserialize_enum(buf, meta->enummetadata, &acl_field_data_data->s32), enum);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64)
    {
        EXPECT_KEY("u64");

        EXPECT_CHECK(sai_deserialize_uint64(buf, &acl_field_data_data->u64), uint64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC)
    {
        EXPECT_KEY("mac");

        EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, acl_field_data_data->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4)
    {
        EXPECT_KEY("ip4");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &acl_field_data_data->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6)
    {
        EXPECT_KEY("ip6");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, acl_field_data_data->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_ID)
    {
        EXPECT_KEY("oid");

        EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &acl_field_data_data->oid), object_id);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST)
    {
        EXPECT_KEY("objlist");

        EXPECT_CHECK(sai_deserialize_object_list(buf, &acl_field_data_data->objlist), object_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
    {
        EXPECT_KEY("u8list");

        EXPECT_CHECK(sai_deserialize_u8_list(buf, &acl_field_data_data->u8list), u8_list);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_acl_field_data_data_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_acl_field_data_mask(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_acl_field_data_mask_t *acl_field_data_mask)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8)
    {
        EXPECT_KEY("u8");

        EXPECT_CHECK(sai_deserialize_uint8(buf, &acl_field_data_mask->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8)
    {
        EXPECT_KEY("s8");

        EXPECT_CHECK(sai_deserialize_int8(buf, &acl_field_data_mask->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16)
    {
        EXPECT_KEY("u16");

        EXPECT_CHECK(sai_deserialize_uint16(buf, &acl_field_data_mask->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16)
    {
        EXPECT_KEY("s16");

        EXPECT_CHECK(sai_deserialize_int16(buf, &acl_field_data_mask->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32)
    {
        EXPECT_KEY("u32");

        EXPECT_CHECK(sai_deserialize_uint32(buf, &acl_field_data_mask->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32)
    {
        EXPECT_KEY("s32");

        EXPECT_CHECK(sai_deserialize_int32(buf, &acl_field_data_mask->s32), int32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64)
    {
        EXPECT_KEY("u64");

        EXPECT_CHECK(sai_deserialize_uint64(buf, &acl_field_data_mask->u64), uint64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC)
    {
        EXPECT_KEY("mac");

        EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, acl_field_data_mask->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4)
    {
        EXPECT_KEY("ip4");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &acl_field_data_mask->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6)
    {
        EXPECT_KEY("ip6");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, acl_field_data_mask->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST)
    {
        EXPECT_KEY("u8list");

        EXPECT_CHECK(sai_deserialize_u8_list(buf, &acl_field_data_mask->u8list), u8_list);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_acl_field_data_mask_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_attribute_value(
    _In_ char *buf,
    _In_ ctc_sai_attr_metadata_t *meta,
    _Out_ sai_attribute_value_t *attribute_value)
{
    char *begin_buf = buf;
    int ret;

    //EXPECT("{");

    if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_BOOL)
    {
        //EXPECT_KEY("booldata");

        EXPECT_CHECK(sai_deserialize_bool(buf, &attribute_value->booldata), bool);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_CHARDATA)
    {
        //EXPECT_KEY("chardata");

        EXPECT_QUOTE_CHECK(sai_deserialize_chardata(buf, attribute_value->chardata), chardata);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT8)
    {
        //EXPECT_KEY("u8");

        EXPECT_CHECK(sai_deserialize_uint8(buf, &attribute_value->u8), uint8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT8)
    {
        //EXPECT_KEY("s8");

        EXPECT_CHECK(sai_deserialize_int8(buf, &attribute_value->s8), int8);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT16)
    {
        //EXPECT_KEY("u16");

        EXPECT_CHECK(sai_deserialize_uint16(buf, &attribute_value->u16), uint16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT16)
    {
        //EXPECT_KEY("s16");

        EXPECT_CHECK(sai_deserialize_int16(buf, &attribute_value->s16), int16);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32)
    {
        //EXPECT_KEY("u32");

        EXPECT_CHECK(sai_deserialize_uint32(buf, &attribute_value->u32), uint32);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32)
    {
        //EXPECT_KEY("s32");

        EXPECT_CHECK(sai_deserialize_enum(buf, meta->enummetadata, &attribute_value->s32), enum);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT64)
    {
        //EXPECT_KEY("u64");

        EXPECT_CHECK(sai_deserialize_uint64(buf, &attribute_value->u64), uint64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT64)
    {
        //EXPECT_KEY("s64");

        EXPECT_CHECK(sai_deserialize_int64(buf, &attribute_value->s64), int64);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_POINTER)
    {
        //EXPECT_KEY("ptr");

        EXPECT_QUOTE_CHECK(sai_deserialize_pointer(buf, &attribute_value->ptr), pointer);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MAC)
    {
        //EXPECT_KEY("mac");

        EXPECT_QUOTE_CHECK(sai_deserialize_mac(buf, attribute_value->mac), mac);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IPV4)
    {
        //EXPECT_KEY("ip4");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &attribute_value->ip4), ip4);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IPV6)
    {
        //EXPECT_KEY("ip6");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, attribute_value->ip6), ip6);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS)
    {
        //EXPECT_KEY("ipaddr");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip_address(buf, &attribute_value->ipaddr), ip_address);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_PREFIX)
    {
        //EXPECT_KEY("ipprefix");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip_prefix(buf, &attribute_value->ipprefix), ip_prefix);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_OBJECT_ID)
    {
        //EXPECT_KEY("oid");

        EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &attribute_value->oid), object_id);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST)
    {
        //EXPECT_KEY("objlist");

        EXPECT_CHECK(sai_deserialize_object_list(buf, &attribute_value->objlist), object_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST)
    {
        //EXPECT_KEY("boollist");

        EXPECT_CHECK(sai_deserialize_bool_list(buf, &attribute_value->boollist), bool_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST)
    {
        //EXPECT_KEY("u8list");

        EXPECT_CHECK(sai_deserialize_u8_list(buf, &attribute_value->u8list), u8_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST)
    {
        //EXPECT_KEY("s8list");

        EXPECT_CHECK(sai_deserialize_s8_list(buf, &attribute_value->s8list), s8_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST)
    {
        //EXPECT_KEY("u16list");

        EXPECT_CHECK(sai_deserialize_u16_list(buf, &attribute_value->u16list), u16_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST)
    {
        //EXPECT_KEY("s16list");

        EXPECT_CHECK(sai_deserialize_s16_list(buf, &attribute_value->s16list), s16_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST)
    {
        //EXPECT_KEY("u32list");

        EXPECT_CHECK(sai_deserialize_u32_list(buf, &attribute_value->u32list), u32_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST)
    {
        //EXPECT_KEY("s32list");

        EXPECT_CHECK(sai_deserialize_enum_list(buf, meta->enummetadata, &attribute_value->s32list), enum_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_UINT32_RANGE)
    {
        //EXPECT_KEY("u32range");

        EXPECT_CHECK(sai_deserialize_u32_range(buf, &attribute_value->u32range), u32_range);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_INT32_RANGE)
    {
        //EXPECT_KEY("s32range");

        EXPECT_CHECK(sai_deserialize_s32_range(buf, &attribute_value->s32range), s32_range);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST)
    {
        //EXPECT_KEY("vlanlist");

        EXPECT_CHECK(sai_deserialize_vlan_list(buf, &attribute_value->vlanlist), vlan_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST)
    {
        //EXPECT_KEY("qosmap");

        EXPECT_CHECK(sai_deserialize_qos_map_list(buf, &attribute_value->qosmap), qos_map_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST)
    {
        //EXPECT_KEY("maplist");

        EXPECT_CHECK(sai_deserialize_map_list(buf, &attribute_value->maplist), map_list);
    }
    else if (meta->isaclfield == true)
    {
        //EXPECT_KEY("aclfield");

        EXPECT_CHECK(sai_deserialize_acl_field_data(buf, meta, &attribute_value->aclfield), acl_field_data);
    }
    else if (meta->isaclaction == true)
    {
        //EXPECT_KEY("aclaction");

        EXPECT_CHECK(sai_deserialize_acl_action_data(buf, meta, &attribute_value->aclaction), acl_action_data);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_CAPABILITY)
    {
        //EXPECT_KEY("aclcapability");

        EXPECT_CHECK(sai_deserialize_acl_capability(buf, &attribute_value->aclcapability), acl_capability);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST)
    {
        //EXPECT_KEY("aclresource");

        EXPECT_CHECK(sai_deserialize_acl_resource_list(buf, &attribute_value->aclresource), acl_resource_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST)
    {
        //EXPECT_KEY("tlvlist");

        EXPECT_CHECK(sai_deserialize_tlv_list(buf, &attribute_value->tlvlist), tlv_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST)
    {
        //EXPECT_KEY("segmentlist");

        EXPECT_CHECK(sai_deserialize_segment_list(buf, &attribute_value->segmentlist), segment_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST)
    {
        //EXPECT_KEY("ipaddrlist");

        EXPECT_CHECK(sai_deserialize_ip_address_list(buf, &attribute_value->ipaddrlist), ip_address_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST)
    {
        //EXPECT_KEY("porteyevalues");

        EXPECT_CHECK(sai_deserialize_port_eye_values_list(buf, &attribute_value->porteyevalues), port_eye_values_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TIMESPEC)
    {
        //EXPECT_KEY("timespec");

        EXPECT_CHECK(sai_deserialize_timespec(buf, &attribute_value->timespec), timespec);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SAK)
    {
        //EXPECT_KEY("macsecsak");

        EXPECT_QUOTE_CHECK(sai_deserialize_macsec_sak(buf, attribute_value->macsecsak), macsec_sak);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_AUTH_KEY)
    {
        //EXPECT_KEY("macsecauthkey");

        EXPECT_QUOTE_CHECK(sai_deserialize_macsec_auth_key(buf, attribute_value->macsecauthkey), macsec_auth_key);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SALT)
    {
        //EXPECT_KEY("macsecsalt");

        EXPECT_QUOTE_CHECK(sai_deserialize_macsec_salt(buf, attribute_value->macsecsalt), macsec_salt);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG)
    {
        //EXPECT_KEY("sysportconfig");

        EXPECT_CHECK(sai_deserialize_system_port_config(buf, &attribute_value->sysportconfig), system_port_config);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST)
    {
        //EXPECT_KEY("sysportconfiglist");

        EXPECT_CHECK(sai_deserialize_system_port_config_list(buf, &attribute_value->sysportconfiglist), system_port_config_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_FABRIC_PORT_REACHABILITY)
    {
        //EXPECT_KEY("reachability");

        EXPECT_CHECK(sai_deserialize_fabric_port_reachability(buf, &attribute_value->reachability), fabric_port_reachability);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST)
    {
        //EXPECT_KEY("porterror");

        EXPECT_CHECK(sai_deserialize_port_err_status_list(buf, &attribute_value->porterror), port_err_status_list);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_CAPTURED_TIMESPEC)
    {
        //EXPECT_KEY("captured_timespec");

        EXPECT_CHECK(sai_deserialize_captured_timespec(buf, &attribute_value->captured_timespec), captured_timespec);
    }
    else if (meta->attrvaluetype == CTC_SAI_ATTR_VALUE_TYPE_TIMEOFFSET)
    {
        //EXPECT_KEY("timeoffset");

        EXPECT_CHECK(sai_deserialize_timeoffset(buf, &attribute_value->timeoffset), timeoffset);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_attribute_value_t', bad condition?");
    }

    //EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_ip_addr(
    _In_ char *buf,
    _In_ sai_ip_addr_family_t addr_family,
    _Out_ sai_ip_addr_t *ip_addr)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (addr_family == SAI_IP_ADDR_FAMILY_IPV4)
    {
        EXPECT_KEY("ip4");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip4(buf, &ip_addr->ip4), ip4);
    }
    else if (addr_family == SAI_IP_ADDR_FAMILY_IPV6)
    {
        EXPECT_KEY("ip6");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, ip_addr->ip6), ip6);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_ip_addr_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_buffer_data(
    _In_ char *buf,
    _In_ sai_buffer_monitor_message_type_t buffer_monitor_message_type,
    _Out_ sai_monitor_buffer_data_t *monitor_buffer_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE)
    {
        EXPECT_KEY("buffer_event");

        EXPECT_CHECK(sai_deserialize_monitor_buffer_event(buf, &monitor_buffer_data->buffer_event), monitor_buffer_event);
    }
    else if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_STATS_MESSAGE)
    {
        EXPECT_KEY("buffer_stats");

        EXPECT_CHECK(sai_deserialize_monitor_buffer_stats(buf, &monitor_buffer_data->buffer_stats), monitor_buffer_stats);
    }
    else if (buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_MICORBURST_STATS_MESSAGE)
    {
        EXPECT_KEY("microburst_stats");

        EXPECT_CHECK(sai_deserialize_monitor_mburst_stats(buf, &monitor_buffer_data->microburst_stats), monitor_mburst_stats);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_monitor_buffer_data_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_monitor_latency_data(
    _In_ char *buf,
    _In_ sai_latency_monitor_message_type_t latency_monitor_message_type,
    _Out_ sai_monitor_latency_data_t *monitor_latency_data)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE)
    {
        EXPECT_KEY("latency_event");

        EXPECT_CHECK(sai_deserialize_monitor_latency_event(buf, &monitor_latency_data->latency_event), monitor_latency_event);
    }
    else if (latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_STATS_MESSAGE)
    {
        EXPECT_KEY("latency_stats");

        EXPECT_CHECK(sai_deserialize_monitor_latency_stats(buf, &monitor_latency_data->latency_stats), monitor_latency_stats);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_monitor_latency_data_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_object_key_entry(
    _In_ char *buf,
    _In_ sai_object_type_t object_type,
    _Out_ sai_object_key_entry_t *object_key_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (ctc_sai_data_utils_is_object_type_oid(object_type) == true)
    {
        EXPECT_KEY("object_id");

        EXPECT_QUOTE_CHECK(sai_deserialize_object_id(buf, &object_key_entry->object_id), object_id);
    }
    else if (object_type == SAI_OBJECT_TYPE_FDB_ENTRY)
    {
        EXPECT_KEY("fdb_entry");

        EXPECT_CHECK(sai_deserialize_fdb_entry(buf, &object_key_entry->fdb_entry), fdb_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_NEIGHBOR_ENTRY)
    {
        EXPECT_KEY("neighbor_entry");

        EXPECT_CHECK(sai_deserialize_neighbor_entry(buf, &object_key_entry->neighbor_entry), neighbor_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_ROUTE_ENTRY)
    {
        EXPECT_KEY("route_entry");

        EXPECT_CHECK(sai_deserialize_route_entry(buf, &object_key_entry->route_entry), route_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_MCAST_FDB_ENTRY)
    {
        EXPECT_KEY("mcast_fdb_entry");

        EXPECT_CHECK(sai_deserialize_mcast_fdb_entry(buf, &object_key_entry->mcast_fdb_entry), mcast_fdb_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_L2MC_ENTRY)
    {
        EXPECT_KEY("l2mc_entry");

        EXPECT_CHECK(sai_deserialize_l2mc_entry(buf, &object_key_entry->l2mc_entry), l2mc_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_IPMC_ENTRY)
    {
        EXPECT_KEY("ipmc_entry");

        EXPECT_CHECK(sai_deserialize_ipmc_entry(buf, &object_key_entry->ipmc_entry), ipmc_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_INSEG_ENTRY)
    {
        EXPECT_KEY("inseg_entry");

        EXPECT_CHECK(sai_deserialize_inseg_entry(buf, &object_key_entry->inseg_entry), inseg_entry);
    }
    else if (object_type == SAI_OBJECT_TYPE_NAT_ENTRY)
    {
        EXPECT_KEY("nat_entry");

        EXPECT_CHECK(sai_deserialize_nat_entry(buf, &object_key_entry->nat_entry), nat_entry);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_object_key_entry_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
int sai_deserialize_tlv_entry(
    _In_ char *buf,
    _In_ sai_tlv_type_t tlv_type,
    _Out_ sai_tlv_entry_t *tlv_entry)
{
    char *begin_buf = buf;
    int ret;

    EXPECT("{");

    if (tlv_type == SAI_TLV_TYPE_INGRESS)
    {
        EXPECT_KEY("ingress_node");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, tlv_entry->ingress_node), ip6);
    }
    else if (tlv_type == SAI_TLV_TYPE_EGRESS)
    {
        EXPECT_KEY("egress_node");

        EXPECT_QUOTE_CHECK(sai_deserialize_ip6(buf, tlv_entry->egress_node), ip6);
    }
    else if (tlv_type == SAI_TLV_TYPE_OPAQUE)
    {
        EXPECT_KEY("opaque_container");

        {
            EXPECT("[");

            uint32_t idx;

            for (idx = 0; idx < 4; idx++)
            {
                if (idx != 0)
                {
                    EXPECT(",");
                }

                EXPECT_CHECK(sai_deserialize_uint32(buf, &tlv_entry->opaque_container[idx]), uint32);
            }

            EXPECT("]");
        }
    }
    else if (tlv_type == SAI_TLV_TYPE_HMAC)
    {
        EXPECT_KEY("hmac");

        EXPECT_CHECK(sai_deserialize_hmac(buf, &tlv_entry->hmac), hmac);
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "nothing was deserialized for 'sai_tlv_entry_t', bad condition?");
    }

    EXPECT("}");

    return (int)(buf - begin_buf);
}
