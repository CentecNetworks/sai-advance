CXX= /opt/rh/devtoolset-2/root/usr/bin/g++
#CXX= /usr/bin/g++
SAI_PREFIX =  $(PWD)/../..
SAI_HEADER_DIR ?= $(SAI_PREFIX)/inc
SDK_DIR = $(SAI_PREFIX)/sdk
SAI_HEADERS = $(SAI_HEADER_DIR)/sai*.h
CFLAGS = -I$(SAI_HEADER_DIR) -I. -std=c++11 -D_SAL_LINUX_UM -w -fpermissive

#CFLAGS = -I$(SAI_HEADER_DIR) -I.
#CFLAGS = -I$(SAI_HEADER_DIR) -I. -std=gnu++0x
#CFLAGS = -I$(SAI_HEADER_DIR) -I. -std=c++0x
#CFLAGS += -I/opt/thrift/thrift-0.9.2/lib/cpp/src
#CFLAGS += -I/opt/thrift/thrift-0.9.2/lib/cpp/src/thrift

ifndef ARCH
export ARCH = uml
endif

ifeq ($(ARCH),arm64)
CFLAGS += -I/data01/users/systest/shanz/sdk/cmodelsai/wtf/Runtime/include/
CFLAGS += -I/data01/users/systest/shanz/sdk/cmodelsai/wtf/Runtime/include/thrift/
CFLAGS += -I/data01/users/systest/shanz/sdk/cmodelsai/wtf/Code/third_party/libevent-2.1.11-stable/include
else
CFLAGS += -I/systest/systest_pub/wtf/Runtime/include/
CFLAGS += -I/systest/systest_pub/wtf/Runtime/include/thrift/
endif

CFLAGS += -I$(SDK_DIR)/libptkxr/include -I$(SDK_DIR)/sal/include
CFLAGS += -I/systest/systest_pub/wtf/Code/pktswitch
CFLAGS += -I$(PWD)/gen-cpp

#ifeq ($(DEBUG),1)
CFLAGS += -O0 -ggdb
#endif

ifndef CHIPNAME
export CHIPNAME = tsingma
endif


ifeq ($(platform),MLNX)
CDEFS = -DMLNXSAI
else
ifeq ($(platform),BFT)
CDEFS = -DBFTSAI
else
ifeq ($(platform),CAVIUM)
CDEFS = -DCAVIUMSAI
else
CDEFS = -DBRCMSAI
ifeq ($(platform),CTC)
CDEFS = -DCTCSAI
else
CDEFS = -DCTCSAI
endif
endif
endif
endif

ifeq ($(ARCH),arm64)
CXX = aarch64-linux-gnu-g++
CDEFS += -DSDK_WORK_PLATFORM=0
else
CDEFS += -DSDK_WORK_PLATFORM=1
endif

DEPS = switch_sai_constants.h  switch_sai_rpc.h  switch_sai_types.h
OBJS = switch_sai_constants.o  switch_sai_rpc.o  switch_sai_types.o

ifeq ($(ARCH),arm64)
ODIR = ./mycode/arm_obj
else
ODIR = ./mycode/obj
endif
#SAIDIR = /root/sdk_sai/inc
SRC = ./mycode
THRIFT = /systest/systest_pub/wtf/Runtime/bin/thrift

##10.10.25.26 use
#THRIFT = /data01/users/systest/shanz/sdk/cmodelsai/wtf/Runtime/bin/thrift

#THRIFT = /opt/saithrift/bin/thrift
CTYPESGEN = /opt/Python-2.7.13/bin/ctypesgen.py
PYBIN = /systest/systest_pub/wtf/Runtime/bin/python
ifeq ($(ARCH),arm64)
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib.board/$(CHIPNAME)
else
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib/$(CHIPNAME)
endif

ifeq ($(ARCH),arm64)
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib.board/$(CHIPNAME)
#LDFLAGS = -L/systest/systest_pub/wtf/Runtime/lib -lthrift -lthriftnb
LDFLAGS += -Wl,-rpath=./lib/
LIBS += -L$(SAI_LIBRARY_DIR) -lctcsdk  -lsai  -lthrift -lthriftnb

LIBS += -L/data01/users/systest/shanz/myinstall/arm_install/libevent/lib -levent
LIBS += -L/data01/users/systest/shanz/myinstall/arm_install/arm-openssl/lib -lssl -lcrypto

LIBS += -lpthread -ldl -lstdc++

LDFLAGS += 
else
LDFLAGS = -L/systest/systest_pub/wtf/Runtime/lib -lthrift -lthriftnb

LIBS = -lpthread  -lmodelcpp -lcmodel -lcmodelcli  
ifeq ($(CHIPNAME), goldengate)
LIBS += -lmemmodel
endif
LIBS +=  -lcmodel -lctcsdk  -ldb -lsai -lcmodelcli -lpktclnt

LDFLAGS += -L$(SAI_LIBRARY_DIR) -Wl,-rpath=$(SAI_LIBRARY_DIR)
LDFLAGS += -L/usr/lib64/ -levent -lssl -lcrypto -lrt -lpthread -ldl
LDFLAGS += -L/systest/systest_pub/wtf/Code/pktswitch/ 

LIB_LCRYPTO_DIR := /opt/openssl-1.0.2c/usr/local/lib64

LIBS += -L$(LIB_LCRYPTO_DIR) -lcrypto -ldl -lstdc++
endif

IS_GCOV = no

ifeq ($(IS_GCOV),yes)
CFLAGS += -fprofile-arcs -ftest-coverage
LDFLAGS += -fprofile-arcs -ftest-coverage
LIBS += -fprofile-arcs -ftest-coverage
endif

CPP_SOURCES = \
				./gen-cpp/switch_sai_constants.cpp \
				./gen-cpp/switch_sai_constants.h \
				./gen-cpp/switch_sai_rpc.cpp \
				./gen-cpp/switch_sai_rpc.h \
				./gen-cpp/switch_sai_types.cpp \
				./gen-cpp/switch_sai_types.h

PY_SOURCES = \
				./gen-py/__init__.py \
				./gen-py/switch_sai/constants.py \
				./gen-py/switch_sai/__init__.py \
				./gen-py/switch_sai/switch_sai_rpc.py \
				./gen-py/switch_sai/switch_sai_rpc-remote \
				./gen-py/switch_sai/ttypes.py

SAI_PY_HEADERS = \
                ./gen-py/switch_sai/sai_headers.py

MKDIR_P = mkdir -p
INSTALL := /usr/bin/install

all: directories $(CPP_SOURCES) $(PY_SOURCES) $(SAI_PY_HEADERS) $(ODIR)/librpcserver.a saiserver 
#clientlib 

directories:
	$(MKDIR_P) $(ODIR)

$(CPP_SOURCES): $(SRC)/switch_sai.thrift
	$(THRIFT) -o . --gen cpp -r $(SRC)/switch_sai.thrift

$(PY_SOURCES): $(SRC)/switch_sai.thrift
	$(THRIFT) -o . --gen py -r $(SRC)/switch_sai.thrift 

$(SAI_PY_HEADERS): $(SAI_HEADERS)
	$(CTYPESGEN) -I/usr/include -I$(SAI_HEADER_DIR) --include /usr/include/linux/limits.h $^ -o $@

clientlib: $(PY_SOURCES) $(SAI_PY_HEADERS)
	python setup.py sdist

$(ODIR)/%.o: ./gen-cpp/%.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@

$(ODIR)/switch_sai_rpc_server.o: src/switch_sai_rpc_server.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@ $(CFLAGS) -I$(SRC)/gen-cpp

$(ODIR)/saiserver.o: src/saiserver.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@ $(CFLAGS) $(CDEFS) -I$(SRC)/gen-cpp -I$(SRC)

$(ODIR)/server.o: $(SRC)/server.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@ $(CFLAGS) $(CDEFS) -I$(SRC)/gen-cpp -I$(SRC)    

$(ODIR)/librpcserver.a: $(ODIR)/switch_sai_rpc.o $(ODIR)/switch_sai_types.o $(ODIR)/switch_sai_constants.o 
	ar rcs $(ODIR)/librpcserver.a $(ODIR)/switch_sai_rpc.o $(ODIR)/switch_sai_types.o $(ODIR)/switch_sai_constants.o

saiserver: $(ODIR)/server.o $(ODIR)/librpcserver.a
	@echo "bulild saiserver use $(CXX) " && \
	$(CXX) $(LDFLAGS) $(ODIR)/server.o -o $@ \
		   $(ODIR)/librpcserver.a $(LIBS)

install-lib: $(ODIR)/librpcserver.a 
	$(INSTALL) -D $(ODIR)/librpcserver.a $(DESTDIR)/usr/lib/librpcserver.a
	$(INSTALL) -D $(SRC)/switch_sai_rpc_server.h $(DESTDIR)/usr/include/switch_sai_rpc_server.h

install-pylib: $(PY_SOURCES) $(SAI_PY_HEADERS)
	python setup.py install --prefix $(DESTDIR)/usr/local$(prefix)

install: install-lib install-pylib

clean:
	rm -rf $(ODIR) $(SRC)/gen-cpp $(SRC)/gen-py saiserver dist
