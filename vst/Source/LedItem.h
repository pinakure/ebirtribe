/*
  ==============================================================================

    LedItem.h
    Created: 7 Nov 2026 10:26:48pm
    Author:  smiker

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include <foleys_gui_magic/foleys_gui_magic.h>

#include "LedComponent.h"

class LedItem : public foleys::GuiItem{
public:
    FOLEYS_DECLARE_GUI_FACTORY(LedItem)

    LedItem(foleys::MagicGUIBuilder& builder,const juce::ValueTree& node);
    juce::Component*                        getWrappedComponent() override;
    std::vector<foleys::SettableProperty>   getSettableProperties() const override;
    void                                    update() override;

private:
    static const juce::Identifier   pKind;
    static const juce::Identifier   pState;
    static juce::StringArray        getLedTypes();
    static juce::StringArray        getStates();
    static int getLedTypeFromName   (const juce::String& name);
    static int getStateFromName     (const juce::String& name);
    static juce::Image loadAtlas    ();

    LedComponent led;
};
