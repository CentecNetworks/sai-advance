
#include "sal.h"
#include "ctc_sai_app_json.h"

#define CTC_ERROR -1;

#define MALLOC_NODE(node) \
    node = mem_malloc(MEM_APP_MODULE, sizeof(app_json_obj_t)); \
    if (NULL == node) \
        return NULL; \
    memset(node,0,sizeof(app_json_obj_t)); 

const char* _ctc_json_get_val_string(const char* str_in, app_json_obj_t* p_obj);
const char* _ctc_json_get_val_number(const char* str_in, app_json_obj_t* p_obj);
const char* _ctc_json_get_val_object(const char* str_in, app_json_obj_t* p_obj);
const char* _ctc_json_get_val_arrary(const char* str_in, app_json_obj_t* p_obj);

static const char* __skip(const char* in) 
{
    while (in && *in)
    {
        if(*in<=32)
        {
            in++; 
        }
        else if(*in == '#')
        {
            while(*(++in) !='\0' && *in != '#');
            in++;
        }
        else
        {
            break;
        }
    }
    return in;
}


const char* _ctc_json_get_key(const char* str, app_json_obj_t* p_obj)
{
    const char* ptr=str+1;
    char *key;
    int32 len=0;

    while (*ptr!='\"' && *ptr )
    {
        len++;
        ptr++;
    }

    key=(char* )mem_malloc(MEM_APP_MODULE, len+1);
    if (!key) 
        return NULL;

    ptr=str+1;
    while (*ptr!='\"' && *ptr)
    {
        *key++=*ptr++;
    }
    *key = '\0';
    if (*ptr=='\"') 
        ptr++;
    p_obj->key = key-len;
    
    //printf("parse key val is: [%s] ", p_obj->key);
    return ptr;
}

const char* _ctc_json_get_value(const char* str_in, app_json_obj_t* p_obj)
{

    if (*str_in>='0' && *str_in<='9')
    { 
        return _ctc_json_get_val_number(str_in, p_obj); 
    }
    switch(*str_in)
    {
        case '\"' : 
            return _ctc_json_get_val_string(str_in, p_obj);
        case '[' :
            return _ctc_json_get_val_arrary(str_in, p_obj);
        case '{' :
            return _ctc_json_get_val_object(str_in, p_obj);
        default:
            return NULL;
    }
}


const char* _ctc_json_get_val_string(const char* str_in, app_json_obj_t* p_obj)
{
    const char* ptr= str_in+1;
    char* string;
    int len=0;

    while (*ptr!='\"' && *ptr )
    {
        len++;
        ptr++;
    }

    string=(char* )mem_malloc(MEM_APP_MODULE, len+1);
    if (!string) 
        return NULL;

    ptr=str_in+1;
    while (*ptr!='\"' && *ptr)
    {
        *string++=*ptr++;
    }
    *string = '\0';
    if (*ptr=='\"') 
        ptr++;
    p_obj->value.string = string - len;
    p_obj->type = APP_JSON_TYPE_STRING;

    //printf("parse string val is: [%s].\n", p_obj->value.string);
    return ptr;
}


const char* _ctc_json_get_val_number(const char* str_in, app_json_obj_t* p_obj)
{
    const char* ptr = str_in;
    int32 num=0;

    if (*ptr=='0') ptr++;
    if (*ptr>='1' && *ptr<='9')
    do{
        num=(num*10)+(*ptr++ -'0');
    }
    while (*ptr>='0' && *ptr<='9');


    p_obj->value.number=(int)num;
    p_obj->type = APP_JSON_TYPE_NUMBER;
    //printf("parse number val is: [%d].\n", p_obj->value.number);
    return ptr;
}



const char* _ctc_json_get_val_arrary(const char* str_in, app_json_obj_t* p_obj)
{
    app_json_obj_t *tmp;
    const char* prt = __skip(str_in + 1);

    p_obj->type = APP_JSON_TYPE_ARRAY;
    if (*prt==']') 
        return prt+1;
        
    MALLOC_NODE(tmp);
    p_obj->value.array = tmp;
    prt=__skip(_ctc_json_get_value(__skip(prt), tmp));
    if (!prt) 
        return NULL;
    p_obj->array_len = 1;

    while (*prt ==',')
    {
        app_json_obj_t *next;
        prt++;        
        MALLOC_NODE(next);
        tmp->next = next;
        next->prev = tmp;
        tmp = next;
        prt=__skip(_ctc_json_get_value(__skip(prt), next));
        if (!prt) 
            return NULL;
        p_obj->array_len++;
    }

    if (*prt==']') 
        return prt+1;
    return NULL;
}

const char* _ctc_json_get_key_value(const char* str_in, app_json_obj_t* p_json)
{
    const char* ptr = str_in;
    if (*ptr=='\"')     /*fix key*/
    { 
        ptr = __skip(_ctc_json_get_key(__skip(ptr), p_json)); 
    }
    else
    {
        return NULL;
    }
    if(*ptr++ == ':')   /*fix value*/
    {
       return __skip(_ctc_json_get_value(__skip(ptr), p_json));
    }
    else
    {
        return NULL;
    }
}


const char* _ctc_json_get_val_object(const char* str_in, app_json_obj_t* p_obj)
{
    app_json_obj_t *child;
    const char* ptr = __skip(str_in+1);

    p_obj->type=APP_JSON_TYPE_OBJECT;
    if (*ptr=='}') 
        return ptr+1;
    
    MALLOC_NODE(child);

    p_obj->value.obj = child;
    ptr=__skip(_ctc_json_get_key_value(__skip(ptr), child));
    if (!ptr) 
        return NULL;

    while (*ptr ==',')
    {
        app_json_obj_t *next;
        ptr++;
        MALLOC_NODE(next);
        child->next=next;
        next->prev=child;
        child=next;
        
        
        ptr=__skip(_ctc_json_get_key_value(__skip(ptr), child));
        if (!ptr) 
            return NULL;
    }
    
    if (*ptr=='}') 
        return ptr+1;
    return NULL;
}



void ctc_json_free(app_json_obj_t* p_json)
{
    app_json_obj_t *next;
    while (p_json)
    {
        next = p_json->next;
        if (p_json->type == APP_JSON_TYPE_OBJECT) ctc_json_free(p_json->value.obj);
        if (p_json->type == APP_JSON_TYPE_STRING) mem_free(p_json->value.string);
        if (p_json->type == APP_JSON_TYPE_ARRAY) ctc_json_free(p_json->value.array);
        mem_free(p_json->key);
        mem_free(p_json);
        p_json = next;
    }
    return;
}


int32 ctc_json_parse(const char* str_in, app_json_obj_t** p_json)
{
    app_json_obj_t *p_obj = NULL;
    p_obj = mem_malloc(MEM_APP_MODULE, sizeof(app_json_obj_t));
    if (!p_obj || !str_in) 
        return CTC_ERROR;

    sal_memset(p_obj, 0, sizeof(app_json_obj_t));
    if (NULL == _ctc_json_get_val_object(__skip(str_in), p_obj))
    {
        ctc_json_free(p_obj);
        sal_printf("### json cfg file error ###\n");
        return CTC_ERROR;
    }
    *p_json = p_obj;
    return 0;
}

app_json_obj_t* ctc_json_get_object(app_json_obj_t *object, const char *string)
{
    app_json_obj_t *p_node = object->value.obj; 
    while (p_node) 
    {
        if(p_node->key && sal_strcmp((char*)string, (char*)p_node->key) == 0)
            return p_node;
        p_node = p_node->next; 
    }
    return NULL;
}

app_json_obj_t * ctc_json_get_array_item(app_json_obj_t *array, int8 index)
{
    app_json_obj_t *p_node = array->value.array;
    if(index >= array->array_len)
    {
        return NULL;
    }
    while (p_node && index > 0) 
        index--, p_node = p_node->next; 
    return p_node;
}

