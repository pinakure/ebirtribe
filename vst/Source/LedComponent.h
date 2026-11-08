
#pragma once

#include <JuceHeader.h>
#include "LedTypes.h"

class LedComponent : public juce::Component
{
public:
    enum State
    {
        Off   = 0,
        Red   = 1,
        Amber = 2,
        Green = 3
    };

    LedComponent(const juce::Image& atlas, int kind = LedTypes::TYPE_HUGE);

    void setState(int newState);
    int getState() const;
    void setKind(int newKind);
    int getKind() const;

    void paint(juce::Graphics& g) override;

private:
    juce::Image imageAtlas;

    int ledKind = LedTypes::TYPE_HUGE;
    int state = Off;
};
