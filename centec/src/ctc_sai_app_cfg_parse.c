/****************************************************************************
 *
 * Header Files
 *
 ****************************************************************************/

#include "sal.h"
#include "ctc_error.h"
#include "ctc_macro.h"
#include "ctc_sai_app_cfg_parse.h"


/****************************************************************************
 *
 * Defines and Macros
 *
 *****************************************************************************/

#define EMPTY_LINE(C)     ((C) == '\0' || (C) == '\r' || (C) == '\n')
#define WHITE_SPACE(C)    ((C) == '\t' || (C) == ' ')

enum{
    CTC_APP_PARSE_FLAG_GLOBAL = 0x01,
    CTC_APP_PARSE_FLAG_TABLE  = 0x02,
    CTC_APP_PARSE_FLAG_TABLE_ENTER = 0x04,
    CTC_APP_PARSE_FLAG_TABLE_LEAVE = 0x08,
    CTC_APP_PARSE_FLAG_MIX    = 0x10,
};

enum{
    CTC_APP_PARSE_RET_CONTINUE = 0,
    CTC_APP_PARSE_RET_FIND,
    CTC_APP_PARSE_RET_NOT_FIND,
    CTC_APP_PARSE_RET_MAX,
};

typedef struct ctc_app_parse_s
{
    char* field;
    char* field_sub;
    void* value;
    uint8* ret_p_entry_num;
    uint8  cur_entry_num;
    uint8  max_entry_num;
    int32 (*func)(const char*, struct ctc_app_parse_s*);
    int32 parse_flag;
}ctc_app_parse_t;


/****************************************************************************
 *
 * Global and Declaration
 *
 *****************************************************************************/


/****************************************************************************
 *
 * Function
 *
 *****************************************************************************/

#define ___________APP_PARSE_INNER_FUNCTION________________________
#define __1_STRING__
static int32
_ctc_app_string_atrim(char* output, const char* input)
{
    char* p = NULL;

    /*trim left space*/
    while (*input != '\0')
    {
        if (WHITE_SPACE(*input))
        {
            ++input;
        }
        else
        {
            break;
        }
    }

    strcpy(output, input);
    /*trim right space*/
    p = output + strlen(output) - 1;

    while (p >= output)
    {
        /*skip empty line*/
        if (WHITE_SPACE(*p) || ('\r' == (*p)) || ('\n' == (*p)))
        {
            --p;
        }
        else
        {
            break;
        }
    }

    *(++p) = '\0';

    return 0;
}

static int32
_ctc_app_get_interage(const char* string, uint32* integer)
{
    char* ch = NULL;
    uint32 val = 0;

    ch = strstr((char*)string, "=");

    if (NULL == ch)
    {
        return -1;
    }
    else
    {
        ch++;
    }

    while (sal_isspace((int)*ch))
    {
        ch++;
    }
    if(ch[0] == '0' && ch[1] == 'x')
    {
        sscanf((char*)ch, "%x", &val);
    }
    else
    {
        sscanf((char*)ch, "%d", &val);
    }
    *integer = val;

    return 0;
}

static int32
_ctc_app_get_field_interage(const char* string, const char *field, uint32* integer)
{
    char* ch = NULL;
    uint32 val = 0;
    char field_tmp[64];
    uint32 i = 0;

    sal_memset(&field_tmp, 0, sizeof(field_tmp));

    ch = sal_strstr((char*)string, (char*)field);

    if (NULL == ch)
    {
        return -1;
    }
    else
    {
        ch+=sal_strlen(field);
    }

    while (sal_isdigit((int)*ch))
    {
        field_tmp[i++] = *(ch++);
    }

    sal_sscanf((char*)field_tmp, "%d", &val);
    *integer = val;

    return 0;
}

#define __2_MAP_FILE__
#define _ctc_app_parse_file_feof(p_ctc_parsr_file) ((p_ctc_parsr_file)->pos >= (p_ctc_parsr_file)->len ? 1:0)

int32
_ctc_app_parse_file_fseek(ctc_app_parse_file_t* p_ctc_parsr_file, int32 pos, int32 dir)
{
    int32 cur_pos = 0;
    cur_pos = p_ctc_parsr_file->pos;

    switch(dir)
    {
        case 0:
            p_ctc_parsr_file->pos = pos;
            break;
        case 1:
            p_ctc_parsr_file->pos += pos;
            break;
        case 2:
            p_ctc_parsr_file->pos = p_ctc_parsr_file->len - pos;
            break;
    }

    return cur_pos;
}

char*
_ctc_app_parse_file_fgets(char* s, int n, ctc_app_parse_file_t *p_file)
{
    int32 copy_len = 0;
    if(NULL == p_file)
    {
        return NULL;
    }

    if(_ctc_app_parse_file_feof(p_file))
    {
        return NULL;
    }

    while(copy_len < n)
    {
        if(p_file->pos == p_file->len)
        {
            break;
        }

        *(s + copy_len) = *(((char*)p_file->mem_addr) + p_file->pos);
        p_file->pos++;
        copy_len++;

        if('\n' == *(s + copy_len - 1))
        {
            break;
        }
    }

    return s;
}

#define __3_PARSE__
static int32
_ctc_app_do_parse(ctc_app_parse_t* p_app_parse, ctc_app_parse_file_t* p_file)
{
    char string[64] = "";
    char line[64]   = "";

    int  err_map[CTC_APP_PARSE_RET_MAX] = {CTC_E_NOT_EXIST,
                                           CTC_E_NONE,
                                           CTC_E_NOT_EXIST};

    int32 ret = CTC_APP_PARSE_RET_NOT_FIND;

    _ctc_app_parse_file_fseek(p_file, 0, SEEK_SET);

    while (!_ctc_app_parse_file_feof(p_file))
    {
        sal_memset(string, 0, sizeof(string));
        sal_memset(line, 0, sizeof(line));
        _ctc_app_parse_file_fgets(string, sizeof(string), p_file);

        /*comment line*/
        if ('#' == string[0] && '{' != string[1] && '}' != string[1])
        {
            continue;
        }

        if (EMPTY_LINE(string[0]))
        {
            continue;
        }

        _ctc_app_string_atrim(line, string);

        if (EMPTY_LINE(line[0]))
        {
            continue;
        }

        if(ret = p_app_parse->func(line, p_app_parse),ret != CTC_APP_PARSE_RET_CONTINUE)
        {
            break;
        }
    }

    if(p_app_parse->cur_entry_num)
    {
        ret = CTC_APP_PARSE_RET_FIND;
    }

    *p_app_parse->ret_p_entry_num = p_app_parse->cur_entry_num;

    return err_map[ret];
}

static int32
_ctc_app_do_cfg_file(const char* line, struct ctc_app_parse_s* p_app_parse)
{
    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_GLOBAL))
    {
        if(sal_strncmp(line,p_app_parse->field,strlen(p_app_parse->field)) == 0)
        {
            _ctc_app_get_interage(line, p_app_parse->value);

            p_app_parse->cur_entry_num++;

            return CTC_APP_PARSE_RET_FIND;
        }
    }

    return CTC_APP_PARSE_RET_CONTINUE;
}

static int32
_ctc_app_do_table_cfg_file(const char* line, struct ctc_app_parse_s* p_app_parse)
{
    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_LEAVE))
    {
        if(sal_strncmp(line, "#}", strlen("#}")) == 0)
        {
            CTC_UNSET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_LEAVE);
            CTC_SET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_GLOBAL);
        }
        return CTC_APP_PARSE_RET_CONTINUE;
    }

    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_ENTER))
    {
        if(sal_strncmp(line,p_app_parse->field,strlen(p_app_parse->field)) == 0)
        {
            CTC_SET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE);
            CTC_UNSET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_ENTER);
        }else{
            CTC_SET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_LEAVE);
            CTC_UNSET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_ENTER);
        }
        return CTC_APP_PARSE_RET_CONTINUE;
    }

    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_GLOBAL))
    {
        if(sal_strncmp(line, "#{", strlen("#{")) == 0)
        {
            CTC_SET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE_ENTER);
            CTC_UNSET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_GLOBAL);

            return CTC_APP_PARSE_RET_CONTINUE;
        }
    }

    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE))
    {
        if(sal_strncmp(line, "#}", strlen("#}")) == 0)
        {
            CTC_UNSET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_TABLE);
            CTC_SET_FLAG(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_GLOBAL);

            return CTC_APP_PARSE_RET_FIND;
        }

        if(sal_strncmp(line,p_app_parse->field_sub,strlen(p_app_parse->field_sub)) == 0)
        {
            if(p_app_parse->cur_entry_num >= p_app_parse->max_entry_num)
                return CTC_APP_PARSE_RET_NOT_FIND;

            _ctc_app_get_interage(line, ((uint32*)p_app_parse->value) + p_app_parse->cur_entry_num);
            p_app_parse->cur_entry_num++;
        }
    }

    return CTC_APP_PARSE_RET_CONTINUE;
}

static int32
_ctc_app_do_mix_cfg_file(const char* line, struct ctc_app_parse_s* p_app_parse)
{
    char field_tmp[64];
    uint32 val = 0;
    uint8* ret_val = p_app_parse->value;

    if(CTC_FLAG_ISSET(p_app_parse->parse_flag,CTC_APP_PARSE_FLAG_MIX)
        && (p_app_parse->cur_entry_num < p_app_parse->max_entry_num))
    {
        _ctc_app_get_field_interage(line, p_app_parse->field, &val);
        sal_memset(&field_tmp, 0, sizeof(field_tmp));
        sal_sprintf(field_tmp, "[%s%d]", p_app_parse->field, val);

        if(sal_strncmp(line, field_tmp, sal_strlen(field_tmp)) == 0)
        {
            ret_val += val;
            _ctc_app_get_interage(line, &val);
            *ret_val = val;
            p_app_parse->cur_entry_num++;
            return CTC_APP_PARSE_RET_CONTINUE;
        }
    }

    return CTC_APP_PARSE_RET_CONTINUE;
}

#define ___________APP_PARSE_OUTER_FUNCTION________________________
#define __0_APP_PARSE_API__
int32
ctc_app_parse_file(ctc_app_parse_file_t* p_file,
                       const char* field,
                       const char* field_sub,
                       void* value,
                       uint8 *p_entry_num)
{
    char field_tmp[64];
    char field_sub_tmp[64];
    ctc_app_parse_t app_parse;

    CTC_PTR_VALID_CHECK(p_file);
    CTC_PTR_VALID_CHECK(field);
    CTC_PTR_VALID_CHECK(value);
    CTC_PTR_VALID_CHECK(p_entry_num);

    sal_memset(&app_parse, 0, sizeof(ctc_app_parse_t));
    sal_memset(&field_tmp, 0, sizeof(field_tmp));
    sal_memset(&field_sub_tmp, 0, sizeof(field_sub_tmp));

    sal_strcat(field_tmp, "[");
    sal_strcat(field_tmp, field);
    sal_strcat(field_tmp, "]");

    app_parse.parse_flag= CTC_APP_PARSE_FLAG_GLOBAL;
    app_parse.field     = field_tmp;
    app_parse.field_sub = NULL;
    app_parse.value     = value;
    app_parse.cur_entry_num = 0;
    app_parse.max_entry_num = *p_entry_num;
    app_parse.ret_p_entry_num = p_entry_num;

    if (NULL == field_sub)
    {
        app_parse.func = _ctc_app_do_cfg_file;
    }
    else if(sal_strncmp(field_sub, LETTER_NUMBER_MIX, sal_strlen(field_sub)) == 0)
    {
        app_parse.parse_flag = CTC_APP_PARSE_FLAG_MIX;
        sal_memset(&field_tmp, 0, sizeof(field_tmp));
        sal_strcat(field_tmp, field);
        app_parse.field     = field_tmp;
        app_parse.field_sub = NULL;
        app_parse.func = _ctc_app_do_mix_cfg_file;
    }
    else
    {
        sal_strcat(field_sub_tmp, "[");
        sal_strcat(field_sub_tmp, field_sub);
        sal_strcat(field_sub_tmp, "]");
        app_parse.field_sub = field_sub_tmp;
        app_parse.func = _ctc_app_do_table_cfg_file;
    }

    return _ctc_app_do_parse(&app_parse, p_file);
}

int32
ctc_app_parse_open_file(const char* file_name, ctc_app_parse_file_t* p_file)
{
    sal_file_t local_fp = NULL;

    CTC_PTR_VALID_CHECK(p_file);

    local_fp = sal_fopen(file_name, "r");

    if (NULL == local_fp)
    {
        return CTC_E_INVALID_PARAM;
    }

    p_file->p_file = local_fp;

    sal_fseek(p_file->p_file, 0, SEEK_END);
    p_file->len = sal_ftell(p_file->p_file);
    sal_fseek(p_file->p_file, 0, SEEK_SET);

#if defined _SAL_LINUX_UM
    p_file->mem_addr = mmap(NULL, p_file->len, PROT_READ, MAP_PRIVATE, fileno(p_file->p_file), 0);
    if(MAP_FAILED == p_file->mem_addr)
    {
        sal_fclose(p_file->p_file);
        ctc_app_parse_file_init(p_file);

        return CTC_E_NO_MEMORY;
    }
#elif defined _SAL_LINUX_KM || defined (_SAL_VXWORKS)
    p_file->mem_addr = sal_malloc(p_file->len);

    if(!p_file->mem_addr)
    {
        sal_fclose(p_file->p_file);
        ctc_app_parse_file_init(p_file);

        return CTC_E_NO_MEMORY;
    }
    sal_memset(p_file->mem_addr, 0, p_file->len);
    sal_fread(p_file->mem_addr, p_file->len, 1, p_file->p_file);
#endif


    return CTC_E_NONE;
}

int32
ctc_app_parse_close_file(ctc_app_parse_file_t* p_file)
{
    CTC_PTR_VALID_CHECK(p_file);

    if(p_file->mem_addr)
    {
#if defined _SAL_LINUX_UM
        munmap(p_file->mem_addr, p_file->len);
#elif defined _SAL_LINUX_KM || defined (_SAL_VXWORKS)
        sal_free(p_file->mem_addr);
#endif
        p_file->mem_addr = NULL;
    }

    if(p_file->p_file)
    {
        sal_fclose(p_file->p_file);
        p_file->p_file = NULL;
    }

    return CTC_E_NONE;
}

