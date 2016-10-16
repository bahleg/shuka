from sdl2 import *

from sys_public import CPU_IDS


def sys_get_processor_id():
    flags = CPU_IDS['CPUID_GENERIC']
    if (SDL_HasMMX()):
        flags |= CPU_IDS['CPUID_MMX']

    if (SDL_Has3DNow()):
        flags |= CPU_IDS['CPUID_3DNOW']

    if (SDL_HasSSE()):
        flags |= CPU_IDS['CPUID_SSE']

    if (SDL_HasSSE2()):
        flags |= CPU_IDS['CPUID_SSE2']
    if (SDL_HasAltiVec()):
        flags |= CPU_IDS['CPUID_ALTIVEC']
    return flags
