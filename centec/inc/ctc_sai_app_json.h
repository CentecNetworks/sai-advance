
#ifndef  CTC_APP_PARSE_CJSON__H
#define  CTC_APP_PARSE_CJSON__H

typedef enum app_josn_val_type_e{
    APP_JSON_TYPE_NONE,
    APP_JSON_TYPE_NUMBER,
    APP_JSON_TYPE_STRING,
    APP_JSON_TYPE_ARRAY,
    APP_JSON_TYPE_OBJECT,
    APP_JSON_TYPE_NULL
}app_josn_val_type_t;



typedef struct app_json_obj_s {
    char* key;

    uint8 type ; /*refer to app_josn_val_type_t*/
    uint8 array_len; 

    union {
        char *string;
        uint32 number;
        struct app_json_obj_s* array;
        struct app_json_obj_s* obj;
    }value;
    struct app_json_obj_s *next,*prev;
} app_json_obj_t;

typedef app_json_obj_t cJSON;


app_json_obj_t * ctc_json_get_array_item(app_json_obj_t *array, int8 index);
app_json_obj_t * ctc_json_get_object(app_json_obj_t *object, const char* string);
int32 ctc_json_parse(const char* str_in, app_json_obj_t** p_json);
void ctc_json_free(app_json_obj_t* p_json);

#endif

