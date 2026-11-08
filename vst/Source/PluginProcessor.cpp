#include "PluginProcessor.h"
#include "LedItem.h"
#include <cmath>

EMX::EMX() : foleys::MagicProcessor (
        BusesProperties()
            .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
            .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
    ){

    // Registrar parámetros. Foley's GUI Magic los detecta y puede adjuntar sus controles.    
    addParameter (volume  = new juce::AudioParameterFloat (juce::ParameterID { "volume"     , 1 },"Volume"  , 0.0f, 1.0f, 0.5f));
    addParameter (panning = new juce::AudioParameterFloat (juce::ParameterID { "panning"    , 1 },"Panning" , 0.0f, 1.0f, 0.5f));

    // Permite a Foley's GUI Magic localizar los recursos del proyecto y gestionar el guardado automático de la interfaz.
    FOLEYS_SET_SOURCE_PATH(__FILE__);

    magicState.setGuiValueTree(
        BinaryData::magic_xml,
        BinaryData::magic_xmlSize
    );
}

void EMX::initialiseBuilder( foleys::MagicGUIBuilder& builder){
    builder.registerJUCEFactories();
    builder.registerJUCELookAndFeels();

    builder.registerFactory("LED", &LedItem::factory);
}

void EMX::prepareToPlay (double sampleRate, int samplesPerBlock){
    juce::dsp::ProcessSpec spec;
    spec.sampleRate         = sampleRate;
    spec.maximumBlockSize   = static_cast<juce::uint32> (samplesPerBlock);
    spec.numChannels        = static_cast<juce::uint32> (getTotalNumOutputChannels());

    myOscillator.prepare (spec);
    myOscillator.setFrequency (440.0f);
    myOscillator.initialise ([] (float x) { return std::sin (x); });
}

void EMX::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) {
    juce::ScopedNoDenormals noDenormals;
    const auto totalNumOutputChannels = getTotalNumOutputChannels();

    // magicState pertenece a foleys::MagicProcessor (clase base).
    magicState.processMidiBuffer (midiMessages, buffer.getNumSamples());

    for (auto channel = totalNumOutputChannels; channel < buffer.getNumChannels(); ++channel)
        buffer.clear (channel, 0, buffer.getNumSamples());

    juce::dsp::AudioBlock<float> audioBlock (buffer);
    juce::dsp::ProcessContextReplacing<float> context (audioBlock);
    
    myOscillator.process (context);

    // Leer el parámetro que Foley's GUI Magic modifica directamente.
    const float volume  = (this->volume  != nullptr) ? this->volume->get()  : 0.5f;
    const float panning = (this->panning != nullptr) ? this->panning->get() : 0.5f;

    for (int channel = 0; channel < totalNumOutputChannels; ++channel){
        auto* channelData = buffer.getWritePointer (channel);

        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
            channelData[sample] *= volume;
    }
}

bool EMX::isBusesLayoutSupported (const BusesLayout& layouts) const {
    const auto output = layouts.getMainOutputChannelSet();

    if (output != juce::AudioChannelSet::mono() && output != juce::AudioChannelSet::stereo()) 
        return false;

    if (output != layouts.getMainInputChannelSet())
        return false;

    return true;
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter(){
    return new EMX();
}

void EMX::releaseResources(){

}

EMX::~EMX(){

}
