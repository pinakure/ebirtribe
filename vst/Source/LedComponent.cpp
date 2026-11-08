
#include "LedComponent.h"

LedComponent::LedComponent(const juce::Image& atlas, int kind) : imageAtlas(atlas), ledKind(kind) {
    if (LedTypes::getSize(ledKind) == 0){
        jassertfalse;
        ledKind = LedTypes::TYPE_HUGE;
    }
    const int size = LedTypes::getSize(ledKind);

    setSize(size, size);
    setInterceptsMouseClicks(false, false);
}

void LedComponent::setKind(int newKind){
    if (ledKind == newKind) return;

    ledKind = newKind;

    const int ledSize = LedTypes::getSize(ledKind);
    setSize(ledSize, ledSize);

    repaint();
}

int LedComponent::getKind() const {
    return ledKind;
}

void LedComponent::setState(int newState){
    newState = juce::jlimit(0, 3, newState);

    if (state != newState)
    {
        state = newState;
        repaint();
    }
}

int LedComponent::getState() const {
    return state;
}

void LedComponent::paint(juce::Graphics& g){
    const int firstFrame = LedTypes::getFirstFrame(ledKind);

    const auto source =
        LedTypes::getGeometry(firstFrame + state);

    if (source.isEmpty() || !imageAtlas.isValid())
        return;

    const auto destination =
        getLocalBounds().withSizeKeepingCentre(
            source.getWidth(),
            source.getHeight()
        );

    g.drawImage(
        imageAtlas,
        destination.getX(),
        destination.getY(),
        destination.getWidth(),
        destination.getHeight(),
        source.getX(),
        source.getY(),
        source.getWidth(),
        source.getHeight()
    );
}
