#pragma once

#include <JuceHeader.h>
#include <foleys_gui_magic/foleys_gui_magic.h>

class YourVstAudioProcessor : public foleys::MagicProcessor
{
public:
    // MagicProcessor ya proporciona magicState. No declararlo aquí otra vez.

    // Parámetro JUCE visible y conectable desde Foley's GUI Magic.
    juce::AudioParameterFloat* volumeParameter = nullptr;

    // Motor de audio
    juce::dsp::Oscillator<float> myOscillator;

    YourVstAudioProcessor();
    ~YourVstAudioProcessor() override;

    // Ciclo de vida y procesamiento de audio
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    // Propiedades generales del plugin
    const juce::String getName() const override { return "MiPrimerVST"; }
    bool acceptsMidi() const override { return true; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 0.0; }

    // Presets / programas
    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram (int index) override {}
    const juce::String getProgramName (int index) override { return {}; }
    void changeProgramName (int index, const juce::String& newName) override {}

    // Buses de audio
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;


private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (YourVstAudioProcessor)
};
