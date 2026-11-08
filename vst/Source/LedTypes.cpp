/*
  ==============================================================================

    LedTypes.cpp
    Created: 7 Nov 2026 10:17:20pm
    Author:  smiker

  ==============================================================================
*/

#include "LedTypes.h"

namespace LedTypes{
    int getSize(int type){
        switch (type){
            case TYPE_HUGE:
            case TYPE_BIG:
                return 32;

            case TYPE_MID:
                return 24;

            case TYPE_SMALL:
            case TYPE_TINY:
            case TYPE_FLAT:
                return 8;

            case TYPE_VUH_XL:
            case TYPE_VUV_XL:
            case TYPE_VUH_XS:
            case TYPE_VUV_XS:
                return 4;

            default:
                return 0;
        }
    }

    int getFirstFrame(int type){
        switch (type){
            case TYPE_HUGE:  return HUGE_OFF;
            case TYPE_BIG:   return BIG_OFF;
            case TYPE_MID:   return MID_OFF;
            case TYPE_SMALL: return SMALL_OFF;
            case TYPE_TINY:  return TINY_OFF;
            case TYPE_FLAT:  return FLAT_OFF;

            case TYPE_VUV_XL: return V_BVM_OFF;
            case TYPE_VUH_XL: return H_BVM_OFF;
            case TYPE_VUV_XS: return V_SVM_OFF;
            case TYPE_VUH_XS: return H_SVM_OFF;

            default:
                return -1;
        }
    }

    juce::Rectangle<int> getGeometry(int frame){
        if (frame < 0 || frame >= NUM_FRAMES)
            return {};

        int x = 0;
        int y = 0;
        int size = 0;

        if (frame < 4){
            x = (frame % 4) * 32;
            y = 0;
            size = 32;
        } else if (frame < 8){
            x = ((frame - 4) % 4) * 32;
            y = 32;
            size = 32;
        } else if (frame < 12){
            x = ((frame - 8) % 4) * 24;
            y = 64;
            size = 24;
        } else if (frame < 16){
            x = 96 + (frame - 12) * 8;
            y = 64;
            size = 8;
        } else if (frame < 20){
            x = 96 + (frame - 16) * 8;
            y = 72;
            size = 8;
        } else if (frame < 24){
            x = 96 + (frame - 20) * 8;
            y = 80;
            size = 8;
        } else if (frame < 40){
            x = (frame - 24) * 8;
            y = 88;
            size = 4;
        } else if (frame < 56) {
            x = (frame - 40) * 8;
            y = 96;
            size = 4;
        } else if (frame < 72) {
            x = (frame - 56) * 4;
            y = 104;
            size = 4;
        } else {
            x = (frame - 72) * 4;
            y = 104;
            size = 4;
        }

        return { x, y, size, size };
    }
}
