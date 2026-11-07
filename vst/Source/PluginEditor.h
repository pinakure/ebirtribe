#pragma once
#include <JuceHeader.h>
#include "PluginProcessor.h"

class YourVstAudioProcessorEditor  : public juce::AudioProcessorEditor,
                                     public juce::Slider::Listener // Escucha los cambios del slider
{
public:
    YourVstAudioProcessorEditor (YourVstAudioProcessor&);
    ~YourVstAudioProcessorEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;
    void sliderValueChanged (juce::Slider* slider) override; // Se activa al mover el slider

private:
    YourVstAudioProcessor& audioProcessor; // Referencia para enviarle datos al procesador
    juce::Slider volumeSlider; // Nuestro control visual

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (YourVstAudioProcessorEditor)
};
