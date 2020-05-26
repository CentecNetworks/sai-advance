ifeq ($(targetbase),linux)
include $(MK_DIR)/sys.mk

OBJ_DIR=$(OBJ_BASE_DIR)/sai

LIB = sai
SRCS = $(shell find src/ -name "*.c")
#SRCS = $(shell find dbclient/ -name "*.c")

ifeq ($(findstring goldengate, $(CHIPNAME)),goldengate)
CPPFLAGS += -DGOLDENGATE
endif

ifeq ($(findstring duet2, $(CHIPNAME)),duet2)
CPPFLAGS += -DDUET2
endif

ifeq ($(findstring tsingma, $(CHIPNAME)),tsingma)
CPPFLAGS += -DTSINGMA
endif

CPPFLAGS += -I$(SAI_SDK_DIR)/dal/include
CPPFLAGS += -I$(SAI_SDK_DIR)/sal/include
CPPFLAGS += -I$(SAI_SDK_DIR)/dkits/
CPPFLAGS += -I$(SAI_SDK_DIR)/core/
CPPFLAGS += -I$(SAI_SDK_DIR)/core/app
CPPFLAGS += -I$(SAI_SDK_DIR)/core/init
CPPFLAGS += -I$(SAI_SDK_DIR)/core/common/include
CPPFLAGS += -I$(SAI_SDK_DIR)/core/api/include
CPPFLAGS += -I$(SAI_DIR)/inc
CPPFLAGS += -I$(SAI_DIR)/centec/inc
#CPPFLAGS += -Wno-unused
CPPFLAGS += -Werror
CPPFLAGS += -O0 -Wall -Werror -g2 -ggdb

include $(MK_DIR)/lib.mk

CFLAGS += -O -Werror -Wall
endif

ifeq ($(targetbase),vxworks)

OBJ_DIR=$(OBJ_BASE_DIR)/sal

all_targets = src libsal

all: $(all_targets) FORCE
clean: $(addprefix clean_,$(all_targets)) FORCE

src: FORCE
	make -C $(SDK_DIR)/sal/src -f Makefile.vx

clean_src: FORCE
	make -C $(SDK_DIR)/sal/src -f Makefile.vx clean

libsal: FORCE
	make -f Makefile_libsal.vx

clean_libsal: FORCE
	make -f Makefile_libsal.vx clean

.PHONY: FORCE
FORCE:
endif
