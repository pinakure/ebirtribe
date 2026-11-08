/*
  ==============================================================================

    LedItem.cpp
    Created: 7 Nov 2026 10:26:48pm
    Author:  smiker

  ==============================================================================
*/

#include "LedItem.h"
#include "BinaryData.h"

// identificación de la propiedades y listas de tipos
const juce::Identifier LedItem::pKind { "kind" };
const juce::Identifier LedItem::pState{ "state" };
juce::StringArray LedItem::getLedTypes(){
    return {
        "HUGE",
        "BIG",
        "MID",
        "SMALL",
        "TINY",
        "FLAT",
        "VUH_XL",
        "VUV_XL",
        "VUH_XS",
        "VUV_XS"
    };
}
juce::StringArray LedItem::getStates(){
    return {
        "OFF",
        "RED",
        "AMBER",
        "GREEN",        
    };
}
// conversión del nombre a identificador 
int LedItem::getLedTypeFromName(const juce::String& name){
    if (name == "BIG")    return LedTypes::TYPE_BIG;
    if (name == "MID")    return LedTypes::TYPE_MID;
    if (name == "SMALL")  return LedTypes::TYPE_SMALL;
    if (name == "TINY")   return LedTypes::TYPE_TINY;
    if (name == "FLAT")   return LedTypes::TYPE_FLAT;
    if (name == "VUH_XL") return LedTypes::TYPE_VUH_XL;
    if (name == "VUV_XL") return LedTypes::TYPE_VUV_XL;
    if (name == "VUH_XS") return LedTypes::TYPE_VUH_XS;
    if (name == "VUV_XS") return LedTypes::TYPE_VUV_XS;
    return LedTypes::TYPE_HUGE;
}
int LedItem::getStateFromName(const juce::String& name){
    if (name == "OFF")    return LedTypes::STATE_OFF;
    if (name == "RED")    return LedTypes::STATE_RED;
    if (name == "AMBER")  return LedTypes::STATE_AMBER;
    if (name == "GREEN")  return LedTypes::STATE_GREEN;
    return LedTypes::TYPE_HUGE;
}
// Exponer la propiedad a Foley's
std::vector<foleys::SettableProperty>
LedItem::getSettableProperties() const {
    std::vector<foleys::SettableProperty> props;

    props.push_back({ configNode, pKind       , foleys::SettableProperty::Choice      , "HUGE"        , magicBuilder.createChoicesMenuLambda(getLedTypes()) });
    props.push_back({ configNode, pState      , foleys::SettableProperty::Choice      , "OFF"         , magicBuilder.createChoicesMenuLambda(getStates()) });

    return props;
}

juce::Image LedItem::loadAtlas(){
    return juce::ImageCache::getFromMemory(
        BinaryData::leds_png,
        BinaryData::leds_pngSize
    );
}

LedItem::LedItem(foleys::MagicGUIBuilder& builder, const juce::ValueTree& node) : foleys::GuiItem(builder, node), led(loadAtlas(), LedTypes::TYPE_HUGE){
    const int ledSize = LedTypes::getSize(LedTypes::TYPE_HUGE);

    setSize(ledSize, ledSize);
    led.setBounds(0, 0, ledSize, ledSize);

    addAndMakeVisible(led);
    update();
}

void LedItem::update(){
    const auto  kindName    = configNode.getProperty(pKind      , "HUGE"    ).toString();
    const auto  stateName   = configNode.getProperty(pState     , "OFF"     ).toString();
    const int   kind        = getLedTypeFromName(kindName);
    const int   state       = getStateFromName(stateName);

    led.setKind(kind);
    led.setState(state);
}

juce::Component* LedItem::getWrappedComponent(){
    return &led;
}
