#include "PluginProcessor.h"
#include "LedItem.h"
#include <cmath>

YourVstAudioProcessor::YourVstAudioProcessor()
    : foleys::MagicProcessor (BusesProperties()
        .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
        .withOutput ("Output", juce::AudioChannelSet::stereo(), true))
{
    // Registrar el parámetro directamente en AudioProcessor.
    // Foley's GUI Magic lo detecta y puede adjuntar sus controles.
    addParameter (volumeParameter = new juce::AudioParameterFloat (
        juce::ParameterID { "volume", 1 },
        "Volume",
        0.0f, 1.0f, 0.5f));

    // Permite a Foley's GUI Magic localizar los recursos del proyecto
    // y gestionar el guardado automático de la interfaz.
    FOLEYS_SET_SOURCE_PATH(__FILE__);

    magicState.setGuiValueTree(
        BinaryData::magic_xml,
        BinaryData::magic_xmlSize
    );
}

YourVstAudioProcessor::~YourVstAudioProcessor(){
}

void YourVstAudioProcessor::initialiseBuilder(
    foleys::MagicGUIBuilder& builder)
{
    builder.registerJUCEFactories();
    builder.registerJUCELookAndFeels();

    builder.registerFactory("LED", &LedItem::factory);
}

void YourVstAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    juce::dsp::ProcessSpec spec;
    spec.sampleRate = sampleRate;
    spec.maximumBlockSize = static_cast<juce::uint32> (samplesPerBlock);
    spec.numChannels = static_cast<juce::uint32> (getTotalNumOutputChannels());

    myOscillator.prepare (spec);
    myOscillator.setFrequency (440.0f);
    myOscillator.initialise ([] (float x) { return std::sin (x); });
}

void YourVstAudioProcessor::releaseResources()
{
}

void YourVstAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer,
                                          juce::MidiBuffer& midiMessages)
{
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
    const float volume = (volumeParameter != nullptr) ? volumeParameter->get() : 0.5f;

    for (int channel = 0; channel < totalNumOutputChannels; ++channel)
    {
        auto* channelData = buffer.getWritePointer (channel);

        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
            channelData[sample] *= volume;
    }
}

bool YourVstAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
    const auto output = layouts.getMainOutputChannelSet();

    if (output != juce::AudioChannelSet::mono()
        && output != juce::AudioChannelSet::stereo())
        return false;

    if (output != layouts.getMainInputChannelSet())
        return false;

    return true;
}

// No definir createEditor() aquí: se utiliza el editor proporcionado por MagicProcessor.

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new YourVstAudioProcessor();
}
