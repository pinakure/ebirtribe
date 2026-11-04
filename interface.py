from widget     import Knob, Slider, Fader, Button, Pad, Led, Valve, Lcd, Vumeter, JogWheel

class Buttons:
    FUNCTION_MENU       = 0x00
    FUNCTION_F1         = 0x01
    FUNCTION_F2         = 0x02
    FUNCTION_F3         = 0x03
    FUNCTION_EXIT       = 0x04
    FUNCTION_ENTER      = 0x05    
    PATTERN_PATTERN     = 0x06
    PATTERN_SONG        = 0x07
    PATTERN_ACCENT      = 0x08
    PATTERN_SLIDE       = 0x09
    TRANSPORT_STOP      = 0x0A
    TRANSPORT_PLAY      = 0x0B
    TRANSPORT_RECORD    = 0x0C
    TRANSPORT_TAP       = 0x0D
    FX_COMPRESSOR       = 0x0E
    FX_DISTORTION       = 0x0F
    FX_EQUALIZER        = 0x10
    FX_RING_MOD         = 0x11
    FX_PITCH            = 0x12
    FX_FILTER           = 0x13
    FX_DELAY            = 0x14
    FX_REVERB           = 0x15
    PART_COMMON_MUTE    = 0x16
    PART_COMMON_SOLO    = 0x17
    PART_SELECT_01      = 0x18
    PART_SELECT_02      = 0x19
    PART_SELECT_03      = 0x1A
    PART_SELECT_04      = 0x1B
    PART_SELECT_05      = 0x1C
    PART_SELECT_06      = 0x1D
    PART_SELECT_07      = 0x1E
    PART_SELECT_08      = 0x1F
    PART_SELECT_09      = 0x20
    PART_SELECT_10      = 0x21
    PART_SELECT_11      = 0x22
    PART_SELECT_12      = 0x23
    PART_01             = 0x24
    PART_02             = 0x25
    PART_03             = 0x26
    PART_04             = 0x27
    PART_05             = 0x28
    PART_06             = 0x29
    PART_07             = 0x2A
    PART_08             = 0x2B
    PART_09             = 0x2C
    PART_10             = 0x2D
    PART_11             = 0x2E
    PART_12             = 0x2F
    PART_13             = 0x30
    PART_14             = 0x31
    PART_15             = 0x32
    PART_16             = 0x33
    AUX_SHIFT           = 0x34
    AUX_PATTERN_SET     = 0x35
    AUX_KEYBOARD        = 0x36
    AUX_LAST_STEP       = 0x37
    AUX_COPY            = 0x38
    AUX_PASTE           = 0x39
    AUX_SCALE           = 0x3A
    AUX_GROOVE          = 0x3B
    AUX_MOTION          = 0x3C
    AUX_DELAY           = 0x3D
    AUX_REVERB          = 0x3E
    AUX_FX_CHAIN        = 0x3F
    AUX_BPM_SYNC        = 0x40
    def get():
        return {
            Buttons.FUNCTION_MENU    : Button('MENU'        ,  45, 366,  84,  49),
            Buttons.FUNCTION_F1      : Button('F1'          , 142, 366,  68,  49),
            Buttons.FUNCTION_F2      : Button('F2'          , 220, 366,  66,  49),
            Buttons.FUNCTION_F3      : Button('F3'          , 297, 366,  65,  49),
            Buttons.FUNCTION_EXIT    : Button('EXIT'        , 373, 366,  75,  49),
            Buttons.FUNCTION_ENTER   : Button('ENTER'       , 461, 366,  84,  49),
            Buttons.PATTERN_PATTERN  : Button('PATTERN'     , 179, 477,  93,  49),
            Buttons.PATTERN_SONG     : Button('SONG'        , 179, 534,  93,  45),
            Buttons.PATTERN_ACCENT   : Button('ACCENT'      ,  60, 587,  98,  41),
            Buttons.PATTERN_SLIDE    : Button('SLIDE'       , 179, 587,  92,  41),
            Buttons.TRANSPORT_STOP   : Button('STOP'        , 325, 521,  86,  81),
            Buttons.TRANSPORT_PLAY   : Button('PLAY'        , 421, 521,  96,  81),
            Buttons.TRANSPORT_RECORD : Button('RECORD'      , 528, 521,  89,  81),
            Buttons.TRANSPORT_TAP    : Button('TAP'         , 627, 521,  83,  81),
            Buttons.FX_COMPRESSOR    : Button('COMPRESSOR'  , 743, 322,  66,  45),
            Buttons.FX_DISTORTION    : Button('DISTORTION'  , 813, 322,  63,  45),
            Buttons.FX_EQUALIZER     : Button('EQUALIZER'   , 879, 322,  63,  45),
            Buttons.FX_RING_MOD      : Button('RING_MOD'    , 945, 322,  63,  45),
            Buttons.FX_PITCH         : Button('PITCH'       , 743, 370,  66,  45),
            Buttons.FX_FILTER        : Button('FILTER'      , 813, 370,  63,  45),
            Buttons.FX_DELAY         : Button('DELAY'       , 879, 370,  63,  45),
            Buttons.FX_REVERB        : Button('REVERB'      , 945, 370,  63,  45),
            Buttons.PART_COMMON_MUTE : Button('COMMON_MUTE' ,1069, 334,  93,  57),
            Buttons.PART_COMMON_SOLO : Button('COMMON_SOLO' ,1177, 334,  98,  57),
            Buttons.PART_SELECT_01   : Button('SELECT_01'   , 753, 476,  62,  57),
            Buttons.PART_SELECT_02   : Button('SELECT_02'   , 820, 476,  62,  57),
            Buttons.PART_SELECT_03   : Button('SELECT_03'   , 887, 476,  61,  57),
            Buttons.PART_SELECT_04   : Button('SELECT_04'   , 953, 476,  62,  57),
            Buttons.PART_SELECT_05   : Button('SELECT_05'   ,1020, 476,  62,  57),
            Buttons.PART_SELECT_06   : Button('SELECT_06'   ,1087, 476,  62,  57),
            Buttons.PART_SELECT_07   : Button('SELECT_07'   , 753, 539,  62,  58),
            Buttons.PART_SELECT_08   : Button('SELECT_08'   , 820, 539,  62,  58),
            Buttons.PART_SELECT_09   : Button('SELECT_09'   , 887, 539,  61,  58),
            Buttons.PART_SELECT_10   : Button('SELECT_10'   , 953, 539,  62,  58),
            Buttons.PART_SELECT_11   : Button('SELECT_11'   ,1020, 539,  62,  58),
            Buttons.PART_SELECT_12   : Button('SELECT_12'   ,1087, 539,  62,  58),
            Buttons.PART_01          : Button('PART_01'     , 242, 719,  68,  89),
            Buttons.PART_02          : Button('PART_02'     , 317, 719,  68,  89),
            Buttons.PART_03          : Button('PART_03'     , 392, 719,  68,  89),
            Buttons.PART_04          : Button('PART_04'     , 466, 719,  68,  89),
            Buttons.PART_05          : Button('PART_05'     , 540, 719,  68,  89),
            Buttons.PART_06          : Button('PART_06'     , 614, 719,  68,  89),
            Buttons.PART_07          : Button('PART_07'     , 688, 719,  68,  89),
            Buttons.PART_08          : Button('PART_08'     , 762, 719,  68,  89),
            Buttons.PART_09          : Button('PART_09'     , 836, 719,  68,  89),
            Buttons.PART_10          : Button('PART_10'     , 910, 719,  68,  89),
            Buttons.PART_11          : Button('PART_11'     , 984, 719,  68,  89),
            Buttons.PART_12          : Button('PART_12'     ,1058, 719,  68,  89),
            Buttons.PART_13          : Button('PART_13'     ,1132, 719,  68,  89),
            Buttons.PART_14          : Button('PART_14'     ,1206, 719,  68,  89),
            Buttons.PART_15          : Button('PART_15'     ,1280, 719,  68,  89),
            Buttons.PART_16          : Button('PART_16'     ,1354, 719,  68,  89),
            Buttons.AUX_SHIFT        : Button('SHIFT'       , 220, 850,  85,  64),
            Buttons.AUX_PATTERN_SET  : Button('PATTERN_SET' , 333, 850,  87,  64),
            Buttons.AUX_KEYBOARD     : Button('KEYBOARD'    , 436, 850,  86,  64),
            Buttons.AUX_LAST_STEP    : Button('LAST_STEP'   , 535, 850,  72,  64),
            Buttons.AUX_COPY         : Button('COPY'        , 626, 850,  72,  64),
            Buttons.AUX_PASTE        : Button('PASTE'       , 717, 850,  73,  64),
            Buttons.AUX_SCALE        : Button('SCALE'       , 809, 850,  72,  64),
            Buttons.AUX_GROOVE       : Button('GROOVE'      , 902, 850,  73,  64),
            Buttons.AUX_MOTION       : Button('MOTION'      , 995, 850,  72,  64),
            Buttons.AUX_DELAY        : Button('DELAY'       ,1087, 850,  67,  64),
            Buttons.AUX_REVERB       : Button('REVERB'      ,1173, 850,  74,  64),
            Buttons.AUX_FX_CHAIN     : Button('FX_CHAIN'    ,1263, 850,  83,  64),
            Buttons.AUX_BPM_SYNC     : Button('BPM_SYNC'    ,1362, 850,  74,  64),
        }

class Knobs:
    JOG_WHEEL           = 0x100
    PART_COMMON_LEVEL   = 0x101
    PART_COMMON_PANNING = 0x102
    TUNE_PITCH          = 0x103
    TUNE_BEND           = 0x104
    PATTERN             = 0x105
    STEP_EDIT           = 0x106
    def get(): 
        return {
            Knobs.PART_COMMON_LEVEL     : Knob('LEVEL'      ,1063, 182),
            Knobs.PART_COMMON_PANNING   : Knob('PANNING'    ,1190, 182),
            Knobs.TUNE_PITCH            : Knob('TUNE_PITCH' ,1343, 171),
            Knobs.TUNE_BEND             : Knob('TUNE_BEND'  ,1343, 299),
            Knobs.PATTERN               : Knob('PATTERN'    ,  58, 475),
            Knobs.STEP_EDIT             : Knob('STEP_EDIT'  ,1346, 479),
        }

class JogWheels:
    GENERAL             = 0x200
    def get():
        return {
            JogWheels.GENERAL           : JogWheel('GENERAL'   , 506, 134),
        }
        
class Faders:
    TEMPO               = 0x300
    def get():
        return {
            Faders.TEMPO                : Fader('TEMPO'     ,  76, 679,  88, 231),
        }

class Valves:
    VALVES             = 0x400
    def get():
        return {
            Valves.VALVES               : Valve('VALVES'    , 741, 161, 273, 154),
        }

class Lcds:
    MAIN                = 0x500
    def get():
        return {
            Lcds.MAIN                   : Lcd('MAIN'      ,  95, 151, 360, 160),
        }

class CallBacks:    
    def nop(widget, event, app): 
        print(event)    
        return True    
    
    def tempo(widget, event, app):
        x_limitada = max(widget.x, min(app.mouse_x, widget.x + widget.width))
        porcentaje_slider = (x_limitada - widget.x) / widget.width
        # app.emx.bpm = w.min + porcentaje_slider * (w.max - w.min)
        return True
    
    def pitch(widget, event, app):
        x_limitada = max(widget.x, min(app.mouse_x, widget.x + widget.width))
        porcentaje_slider = (x_limitada - widget.x) / widget.width
        # app.emx.pitch = int(round(widget.min + porcentaje_slider * (widget.max - widget.min)))
        return True

    def jog_wheel(widget, event, app):
        return True
    
    def bend(widget, event, app):
        return True
    
    def level(widget, event, app):
        return True
    
    def panning(widget, event, app):
        return True
    
    def pattern(widget, event, app):
        return True
    
    def step_edit(widget, event, app):
        return True

RESOURCES = {
    'deck'      : 'resources/deck.png',
    'knob'      : 'resources/knob.png',
    'fader'     : 'resources/fader.png',
    'slider'    : 'resources/slider.png',
    'leds'      : 'resources/leds.png',
    'buttons'   : 'resources/buttons.png',
    'jog_wheel' : 'resources/jog_wheel.png',
    'valve'     : 'resources/valve.png',
}
    
JUMP_TABLE = {
    Faders.TEMPO                : CallBacks.tempo,
    Knobs.TUNE_PITCH            : CallBacks.pitch,
    Knobs.TUNE_BEND             : CallBacks.bend,
    Knobs.JOG_WHEEL             : CallBacks.jog_wheel,
    Knobs.PART_COMMON_LEVEL     : CallBacks.level,
    Knobs.PART_COMMON_PANNING   : CallBacks.panning,
    Knobs.PATTERN               : CallBacks.pattern,
    Knobs.STEP_EDIT             : CallBacks.step_edit,
    Buttons.FUNCTION_MENU       : CallBacks.nop,
    Buttons.FUNCTION_F1         : CallBacks.nop,
    Buttons.FUNCTION_F2         : CallBacks.nop,
    Buttons.FUNCTION_F3         : CallBacks.nop,
    Buttons.FUNCTION_EXIT       : CallBacks.nop,
    Buttons.FUNCTION_ENTER      : CallBacks.nop,
    Buttons.PATTERN_PATTERN     : CallBacks.nop,
    Buttons.PATTERN_SONG        : CallBacks.nop,
    Buttons.PATTERN_ACCENT      : CallBacks.nop,
    Buttons.PATTERN_SLIDE       : CallBacks.nop,
    Buttons.TRANSPORT_STOP      : CallBacks.nop,
    Buttons.TRANSPORT_PLAY      : CallBacks.nop,
    Buttons.TRANSPORT_RECORD    : CallBacks.nop,
    Buttons.TRANSPORT_TAP       : CallBacks.nop,
    Buttons.FX_COMPRESSOR       : CallBacks.nop,
    Buttons.FX_DISTORTION       : CallBacks.nop,
    Buttons.FX_EQUALIZER        : CallBacks.nop,
    Buttons.FX_RING_MOD         : CallBacks.nop,
    Buttons.FX_PITCH            : CallBacks.nop,
    Buttons.FX_FILTER           : CallBacks.nop,
    Buttons.FX_DELAY            : CallBacks.nop,
    Buttons.FX_REVERB           : CallBacks.nop,
    Buttons.PART_COMMON_MUTE    : CallBacks.nop,
    Buttons.PART_COMMON_SOLO    : CallBacks.nop,
    Buttons.PART_SELECT_01      : CallBacks.nop,
    Buttons.PART_SELECT_02      : CallBacks.nop,
    Buttons.PART_SELECT_03      : CallBacks.nop,
    Buttons.PART_SELECT_04      : CallBacks.nop,
    Buttons.PART_SELECT_05      : CallBacks.nop,
    Buttons.PART_SELECT_06      : CallBacks.nop,
    Buttons.PART_SELECT_07      : CallBacks.nop,
    Buttons.PART_SELECT_08      : CallBacks.nop,
    Buttons.PART_SELECT_09      : CallBacks.nop,
    Buttons.PART_SELECT_10      : CallBacks.nop,
    Buttons.PART_SELECT_11      : CallBacks.nop,
    Buttons.PART_SELECT_12      : CallBacks.nop,
    Buttons.PART_01             : CallBacks.nop,
    Buttons.PART_02             : CallBacks.nop,
    Buttons.PART_03             : CallBacks.nop,
    Buttons.PART_04             : CallBacks.nop,
    Buttons.PART_05             : CallBacks.nop,
    Buttons.PART_06             : CallBacks.nop,
    Buttons.PART_07             : CallBacks.nop,
    Buttons.PART_08             : CallBacks.nop,
    Buttons.PART_09             : CallBacks.nop,
    Buttons.PART_10             : CallBacks.nop,
    Buttons.PART_11             : CallBacks.nop,
    Buttons.PART_12             : CallBacks.nop,
    Buttons.PART_13             : CallBacks.nop,
    Buttons.PART_14             : CallBacks.nop,
    Buttons.PART_15             : CallBacks.nop,
    Buttons.PART_16             : CallBacks.nop,
    Buttons.AUX_SHIFT           : CallBacks.nop,
    Buttons.AUX_PATTERN_SET     : CallBacks.nop,
    Buttons.AUX_KEYBOARD        : CallBacks.nop,
    Buttons.AUX_LAST_STEP       : CallBacks.nop,
    Buttons.AUX_COPY            : CallBacks.nop,
    Buttons.AUX_PASTE           : CallBacks.nop,
    Buttons.AUX_SCALE           : CallBacks.nop,
    Buttons.AUX_GROOVE          : CallBacks.nop,
    Buttons.AUX_MOTION          : CallBacks.nop,
    Buttons.AUX_DELAY           : CallBacks.nop,
    Buttons.AUX_REVERB          : CallBacks.nop,
    Buttons.AUX_FX_CHAIN        : CallBacks.nop,
    Buttons.AUX_BPM_SYNC        : CallBacks.nop,
}
