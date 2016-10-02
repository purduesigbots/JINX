# Universal C Makefile for MCU targets
# Top-level template file to configure build

# Makefile for IFI VeX Cortex Microcontroller (STM32F103VD series)
DEVICE=VexCortex
# Libraries to include in the link (use -L and -l) e.g. -lm, -lmyLib
LIBRARIES=$(ROOT)/firmware/libccos.a -lgcc -lm
LIBSML=$(ROOT)/firmware/libsml.a
LIBLCD=$(ROOT)/firmware/liblcd.a
# Prefix for ARM tools (must be on the path)
MCUPREFIX=arm-none-eabi-
#Account for Mac users not having arm on $path
#ifeq ($(OS), Windows_NT)
#else
#	UNAME_S := $(shell uname -s)
#    ifeq ($(UNAME_S), Linux)
#    endif
	#Mac
#	ifeq ($(UNAME_S), Darwin)
#        MCUPREFIX = /Applications/PROS_2.0/gcc-arm-none-eabi-4_7-2014q2/ + MCUPREFIX
#    endif
#endif
# Flags for the assembler
MCUAFLAGS=-mthumb -mcpu=cortex-m3 -mlittle-endian
# Flags for the compiler
MCUCFLAGS=-mthumb -mcpu=cortex-m3 -mlittle-endian
# Flags for the linker
MCULFLAGS=-nostartfiles -Wl,-static -Bfirmware -Wl,-u,VectorTable -Wl,-T -Xlinker firmware/cortex.ld
# Prepares the elf file by converting it to a binary that java can write
MCUPREPARE=$(OBJCOPY) $(OUT) -O binary $(BINDIR)/$(OUTBIN)
# Advanced sizing flags
SIZEFLAGS=
# Uploads program using java
UPLOAD=@java -jar firmware/uniflash.jar vex $(BINDIR)/$(OUTBIN)

# Advanced options
ASMEXT=s
CEXT=c
CPPEXT=cpp
HEXT=h
INCLUDE=-I$(ROOT)/include -I$(ROOT)/src
OUTBIN=output.bin
OUTNAME=output.elf

# Flags for programs
AFLAGS:=$(MCUAFLAGS)
ARFLAGS:=$(MCUCFLAGS)
CCFLAGS:=-c -Wall $(MCUCFLAGS) -Os -ffunction-sections -fsigned-char -fomit-frame-pointer -fsingle-precision-constant
CFLAGS:=$(CCFLAGS) -std=gnu99 -Werror=implicit-function-declaration -DVERSION=\"$(GIT_VERSION)\"
CPPFLAGS:=$(CCFLAGS) -fno-exceptions -fno-rtti -felide-constructors
LDFLAGS:=-Wall $(MCUCFLAGS) $(MCULFLAGS) -Wl,--gc-sections

# Tools used in program
AR:=$(MCUPREFIX)ar
AS:=$(MCUPREFIX)as
CC:=$(MCUPREFIX)gcc
CPPCC:=$(MCUPREFIX)g++
OBJCOPY:=$(MCUPREFIX)objcopy
