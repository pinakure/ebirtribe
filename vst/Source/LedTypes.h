/*
  ==============================================================================

    LedTypes.h
    Created: 7 Nov 2026 10:17:20pm
    Author:  smiker

  ==============================================================================
*/
#pragma once

#include <JuceHeader.h>

namespace LedTypes
{
    // Identificadores de los gráficos dentro del atlas.
    enum Frame
    {
        HUGE_OFF = 0x00,
        HUGE_RED = 0x01,
        HUGE_AMBER = 0x02,
        HUGE_GREEN = 0x03,

        BIG_OFF = 0x04,
        BIG_RED = 0x05,
        BIG_AMBER = 0x06,
        BIG_GREEN = 0x07,

        MID_OFF = 0x08,
        MID_RED = 0x09,
        MID_AMBER = 0x0A,
        MID_GREEN = 0x0B,

        SMALL_OFF = 0x0C,
        SMALL_RED = 0x0D,
        SMALL_AMBER = 0x0E,
        SMALL_GREEN = 0x0F,

        TINY_OFF = 0x10,
        TINY_RED = 0x11,
        TINY_AMBER = 0x12,
        TINY_GREEN = 0x13,

        FLAT_OFF = 0x14,
        FLAT_RED = 0x15,
        FLAT_AMBER = 0x16,
        FLAT_GREEN = 0x17,

        V_BVM_OFF = 0x18,
        V_BVM_G00 = 0x19,
        V_BVM_G01 = 0x1A,
        V_BVM_G02 = 0x1B,
        V_BVM_G03 = 0x1C,
        V_BVM_G04 = 0x1D,
        V_BVM_Y00 = 0x1E,
        V_BVM_Y01 = 0x1F,
        V_BVM_Y02 = 0x20,
        V_BVM_Y03 = 0x21,
        V_BVM_Y04 = 0x22,
        V_BVM_R00 = 0x23,
        V_BVM_R01 = 0x24,
        V_BVM_R02 = 0x25,
        V_BVM_R03 = 0x26,
        V_BVM_R04 = 0x27,

        H_BVM_OFF = 0x28,
        H_BVM_G00 = 0x29,
        H_BVM_G01 = 0x2A,
        H_BVM_G02 = 0x2B,
        H_BVM_G03 = 0x2C,
        H_BVM_G04 = 0x2D,
        H_BVM_Y00 = 0x2E,
        H_BVM_Y01 = 0x2F,
        H_BVM_Y02 = 0x30,
        H_BVM_Y03 = 0x31,
        H_BVM_Y04 = 0x32,
        H_BVM_R00 = 0x33,
        H_BVM_R01 = 0x34,
        H_BVM_R02 = 0x35,
        H_BVM_R03 = 0x36,
        H_BVM_R04 = 0x37,

        V_SVM_OFF = 0x38,
        V_SVM_G00 = 0x39,
        V_SVM_G01 = 0x3A,
        V_SVM_G02 = 0x3B,
        V_SVM_G03 = 0x3C,
        V_SVM_G04 = 0x3D,
        V_SVM_Y00 = 0x3E,
        V_SVM_Y01 = 0x3F,
        V_SVM_Y02 = 0x40,
        V_SVM_Y03 = 0x41,
        V_SVM_Y04 = 0x42,
        V_SVM_R00 = 0x43,
        V_SVM_R01 = 0x44,
        V_SVM_R02 = 0x45,
        V_SVM_R03 = 0x46,
        V_SVM_R04 = 0x47,

        H_SVM_OFF = 0x48,
        H_SVM_G00 = 0x49,
        H_SVM_G01 = 0x4A,
        H_SVM_G02 = 0x4B,
        H_SVM_G03 = 0x4C,
        H_SVM_G04 = 0x4D,
        H_SVM_Y00 = 0x4E,
        H_SVM_Y01 = 0x4F,
        H_SVM_Y02 = 0x50,
        H_SVM_Y03 = 0x51,
        H_SVM_Y04 = 0x52,
        H_SVM_R00 = 0x53,
        H_SVM_R01 = 0x54,
        H_SVM_R02 = 0x55,
        H_SVM_R03 = 0x56,
        H_SVM_R04 = 0x57
    };

    // Tipos físicos de componentes.
    enum Type
    {
        TYPE_HUGE   = 0x00,
        TYPE_BIG    = 0x01,
        TYPE_MID    = 0x02,
        TYPE_SMALL  = 0x03,
        TYPE_TINY   = 0x04,
        TYPE_FLAT   = 0x05,
        TYPE_VUH_XL = 0x06,
        TYPE_VUV_XL = 0x07,
        TYPE_VUH_XS = 0x08,
        TYPE_VUV_XS = 0x09
    };
    
    enum State {
        STATE_OFF   = 0x00,
        STATE_RED   = 0x01,
        STATE_AMBER = 0x02,
        STATE_GREEN = 0x03,
    };

    constexpr int NUM_FRAMES = 0x58;

    int getSize(int type);

    int getFirstFrame(int type);

    juce::Rectangle<int> getGeometry(int frame);
}
