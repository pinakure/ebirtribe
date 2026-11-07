#include "PluginProcessor.h"
#include "PluginEditor.h"

YourVstAudioProcessorEditor::YourVstAudioProcessorEditor (YourVstAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // Configurar el slider de volumen
    volumeSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    volumeSlider.setRange(0.0, 1.0, 0.01);
    volumeSlider.setValue(0.5);
    volumeSlider.addListener(this);
    addAndMakeVisible(&volumeSlider);

    setSize (400, 200); // Tamaño de la ventana del VST
}

YourVstAudioProcessorEditor::~YourVstAudioProcessorEditor() {}

void YourVstAudioProcessorEditor::paint (juce::Graphics& g)
{
    g.fillAll (juce::Colours::darkgrey); // Fondo del VST
    g.setColour (juce::Colours::white);
    g.setFont (15.0f);
    g.drawFittedText ("Mi Prototipo VST", getLocalBounds(), juce::Justification::centredTop, 1);
}

void YourVstAudioProcessorEditor::resized()
{
    // Posición del slider en la ventana
    volumeSlider.setBounds (50, 80, 300, 40);
}

// Conexión: Cuando el usuario mueve el slider, actualiza el procesador de audio
void YourVstAudioProcessorEditor::sliderValueChanged (juce::Slider* slider)
{
    if (slider == &volumeSlider)
    {
        audioProcessor.setVolume(volumeSlider.getValue());
    }
}
