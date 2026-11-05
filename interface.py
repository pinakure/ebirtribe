from widget     import Knob, Slider, Fader, Button, Pad, Led, Valve, Lcd, Vumeter, JogWheel, LedTypes

class Leds:
    STEP_01             = 0x00
    STEP_02             = 0x01
    STEP_03             = 0x02
    STEP_04             = 0x03
    STEP_05             = 0x04
    STEP_06             = 0x05
    STEP_07             = 0x06
    STEP_08             = 0x07
    STEP_09             = 0x08
    STEP_10             = 0x09
    STEP_11             = 0x0A
    STEP_12             = 0x0B
    STEP_13             = 0x0C
    STEP_14             = 0x0D
    STEP_15             = 0x0E
    STEP_16             = 0x0F
    ERASE_RED           = 0x10
    ERASE_GREEN         = 0x11
    WRITE_RED           = 0x12
    WRITE_GREEN         = 0x13
    STEP_COPY           = 0x14
    STEP_REPLACE        = 0x15
    STEP_INSERT         = 0x16
    STEP_DELETE         = 0x17    
    def get():
        return {
            Leds.STEP_01        : Led('STEP_01'     , 261+(74 * 0x00), 685,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_02        : Led('STEP_02'     , 261+(74 * 0x01), 684,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_03        : Led('STEP_03'     , 262+(74 * 0x02), 684,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_04        : Led('STEP_04'     , 263+(74 * 0x03), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_05        : Led('STEP_05'     , 264+(74 * 0x04), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_06        : Led('STEP_06'     , 262+(74 * 0x05), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_07        : Led('STEP_07'     , 263+(74 * 0x06), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_08        : Led('STEP_08'     , 263+(74 * 0x07), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_09        : Led('STEP_09'     , 263+(74 * 0x08), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_10        : Led('STEP_10'     , 263+(74 * 0x09), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_11        : Led('STEP_11'     , 264+(74 * 0x0A), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_12        : Led('STEP_12'     , 264+(74 * 0x0B), 683,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_13        : Led('STEP_13'     , 265+(74 * 0x0C), 682,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_14        : Led('STEP_14'     , 266+(74 * 0x0D), 682,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_15        : Led('STEP_15'     , 264+(74 * 0x0E), 682,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.STEP_16        : Led('STEP_16'     , 261+(74 * 0x0F), 682,  32,  32, LedTypes.TYPE_BIG    ),
            Leds.ERASE_RED      : Led('ERASE_RED'   ,             421, 474,  32,  32, LedTypes.TYPE_HUGE   ),
            Leds.ERASE_GREEN    : Led('ERASE_GREEN' ,             480, 474,  32,  32, LedTypes.TYPE_HUGE   ),
            Leds.WRITE_RED      : Led('WRITE_RED'   ,             538, 474,  32,  32, LedTypes.TYPE_HUGE   ),
            Leds.WRITE_GREEN    : Led('WRITE_GREEN' ,             599, 474,  32,  32, LedTypes.TYPE_HUGE   ),
            Leds.STEP_COPY      : Led('STEP_COPY'   ,            1199, 484,  24,  24, LedTypes.TYPE_MID    ),
            Leds.STEP_REPLACE   : Led('STEP_REPLACE',            1199, 515,  24,  24, LedTypes.TYPE_MID    ),
            Leds.STEP_INSERT    : Led('STEP_INSERT' ,            1199, 545,  24,  24, LedTypes.TYPE_MID    ),
            Leds.STEP_DELETE    : Led('STEP_DELETE' ,            1199, 577,  24,  24, LedTypes.TYPE_MID    ),
        }

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
            Buttons.FUNCTION_MENU    : Button('MENU'        ,  44, 367,  84,  49, (   0,   0), 0, (  88,  56)),
            Buttons.FUNCTION_F1      : Button('F1'          , 142, 367,  68,  49, ( 256,   0), 0, (  72,  56)),
            Buttons.FUNCTION_F2      : Button('F2'          , 220, 367,  66,  49, ( 328,   0), 0, (  72,  56)),
            Buttons.FUNCTION_F3      : Button('F3'          , 297, 367,  65,  49, ( 400,   0), 0, (  64,  56)),
            Buttons.FUNCTION_ENTER   : Button('ENTER'       , 461, 367,  84,  49, (  88,   0), 0, (  88,  56)),
            Buttons.FUNCTION_EXIT    : Button('EXIT'        , 374, 367,  75,  49, ( 176,   0), 0, (  80,  56)),
            Buttons.PATTERN_PATTERN  : Button('PATTERN'     , 179, 478,  93,  49, (   0, 120), 0, (  96,  56)),
            Buttons.PATTERN_SONG     : Button('SONG'        , 179, 535,  93,  45, (  96, 120), 0, (  96,  56)),
            Buttons.PATTERN_ACCENT   : Button('ACCENT'      ,  60, 587,  98,  41, (  96, 176), 0, (  96,  48)),
            Buttons.PATTERN_SLIDE    : Button('SLIDE'       , 179, 588,  92,  41, (   0, 176), 0, (  96,  48)),
            Buttons.TRANSPORT_STOP   : Button('STOP'        , 325, 522,  86,  81, ( 896,   0), 0, (  88,  88)),
            Buttons.TRANSPORT_PLAY   : Button('PLAY'        , 421, 522,  96,  81, ( 984,   0), 0, (  96,  88)),
            Buttons.TRANSPORT_RECORD : Button('RECORD'      , 528, 522,  89,  81, ( 808,   0), 0, (  88,  88)),
            Buttons.TRANSPORT_TAP    : Button('TAP'         , 628, 522,  83,  81, ( 720,   0), 0, (  88,  88)),
            Buttons.FX_COMPRESSOR    : Button('COMPRESSOR'  , 743, 322,  66,  45, ( 192,  56), 0, (  64,  48)),
            Buttons.FX_DISTORTION    : Button('DISTORTION'  , 814, 322,  63,  45, ( 256,  56), 0, (  64,  48)),
            Buttons.FX_EQUALIZER     : Button('EQUALIZER'   , 880, 322,  63,  45, ( 192, 152), 0, (  64,  48)),
            Buttons.FX_RING_MOD      : Button('RING_MOD'    , 947, 322,  63,  45, ( 256, 152), 0, (  64,  48)),
            Buttons.FX_PITCH         : Button('PITCH'       , 743, 370,  66,  45, ( 192, 104), 0, (  64,  48)),
            Buttons.FX_FILTER        : Button('FILTER'      , 814, 370,  63,  45, ( 256, 104), 0, (  64,  48)),
            Buttons.FX_DELAY         : Button('DELAY'       , 880, 370,  63,  45, ( 192, 200), 0, (  64,  48)),
            Buttons.FX_REVERB        : Button('REVERB'      , 947, 370,  63,  45, ( 256, 200), 0, (  64,  48)),
            Buttons.PART_COMMON_MUTE : Button('COMMON_MUTE' ,1069, 334,  93,  57, (   0,  56), 0, (  96,  64)),
            Buttons.PART_COMMON_SOLO : Button('COMMON_SOLO' ,1177, 334,  98,  57, (  96,  56), 0, (  96,  64)),
            Buttons.PART_SELECT_01   : Button('SELECT_01'   , 753, 476,  62,  57, ( 464,   0), 0, (  64,  56)),
            Buttons.PART_SELECT_02   : Button('SELECT_02'   , 820, 476,  62,  57, ( 528,   0), 0, (  64,  56)),
            Buttons.PART_SELECT_03   : Button('SELECT_03'   , 888, 476,  61,  57, ( 592,   0), 0, (  64,  56)),
            Buttons.PART_SELECT_04   : Button('SELECT_04'   , 953, 476,  62,  57, ( 656,   0), 0, (  64,  56)),
            Buttons.PART_SELECT_05   : Button('SELECT_05'   ,1020, 476,  62,  57, ( 464,  64), 0, (  64,  56)),
            Buttons.PART_SELECT_06   : Button('SELECT_06'   ,1087, 476,  62,  57, ( 528,  64), 0, (  64,  56)),
            Buttons.PART_SELECT_07   : Button('SELECT_07'   , 753, 538,  62,  58, ( 592,  64), 0, (  64,  56)),
            Buttons.PART_SELECT_08   : Button('SELECT_08'   , 820, 538,  62,  58, ( 656,  64), 0, (  64,  56)),
            Buttons.PART_SELECT_09   : Button('SELECT_09'   , 888, 538,  61,  58, ( 464, 128), 0, (  64,  56)),
            Buttons.PART_SELECT_10   : Button('SELECT_10'   , 953, 538,  62,  58, ( 528, 128), 0, (  64,  56)),
            Buttons.PART_SELECT_11   : Button('SELECT_11'   ,1020, 538,  62,  58, ( 592, 128), 0, (  64,  56)),
            Buttons.PART_SELECT_12   : Button('SELECT_12'   ,1087, 538,  62,  58, ( 656, 128), 0, (  64,  56)),
            Buttons.PART_01          : Button('PART_01'     , 242, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_02          : Button('PART_02'     , 317, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_03          : Button('PART_03'     , 392, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_04          : Button('PART_04'     , 466, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_05          : Button('PART_05'     , 540, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_06          : Button('PART_06'     , 614, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_07          : Button('PART_07'     , 688, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_08          : Button('PART_08'     , 762, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_09          : Button('PART_09'     , 836, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_10          : Button('PART_10'     , 910, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_11          : Button('PART_11'     , 984, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_12          : Button('PART_12'     ,1058, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_13          : Button('PART_13'     ,1132, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_14          : Button('PART_14'     ,1206, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_15          : Button('PART_15'     ,1280, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.PART_16          : Button('PART_16'     ,1354, 720,  68,  89, ( 720,  88), 0, (  72,  96)),
            Buttons.AUX_SHIFT        : Button('SHIFT'       , 221, 851,  85,  64, ( 792,  88), 0, (  88,  72)),
            Buttons.AUX_PATTERN_SET  : Button('PATTERN_SET' , 334, 851,  87,  64, ( 968,  88), 0, (  88,  72)),
            Buttons.AUX_KEYBOARD     : Button('KEYBOARD'    , 436, 851,  86,  64, ( 880,  88), 0, (  88,  72)),
            Buttons.AUX_LAST_STEP    : Button('LAST_STEP'   , 535, 851,  72,  64, ( 720, 184), 0, (  72,  72)),
            Buttons.AUX_COPY         : Button('COPY'        , 627, 851,  72,  64, ( 792, 184), 0, (  72,  72)),
            Buttons.AUX_PASTE        : Button('PASTE'       , 717, 850,  73,  64, ( 392, 184), 0, (  72,  64)),
            Buttons.AUX_SCALE        : Button('SCALE'       , 809, 850,  72,  64, ( 320,  56), 0, (  72,  64)),
            Buttons.AUX_GROOVE       : Button('GROOVE'      , 902, 850,  73,  64, ( 392,  56), 0, (  72,  64)),
            Buttons.AUX_MOTION       : Button('MOTION'      , 994, 850,  72,  64, ( 320, 120), 0, (  72,  64)),
            Buttons.AUX_DELAY        : Button('DELAY'       ,1087, 850,  67,  64, ( 464, 192), 0, (  64,  64)),
            Buttons.AUX_REVERB       : Button('REVERB'      ,1173, 850,  74,  64, ( 392, 120), 0, (  72,  64)),
            Buttons.AUX_FX_CHAIN     : Button('FX_CHAIN'    ,1263, 850,  83,  64, ( 528, 192), 0, (  80,  64)),
            Buttons.AUX_BPM_SYNC     : Button('BPM_SYNC'    ,1362, 850,  74,  64, ( 320, 184), 0, (  72,  64)),
        }

class Knobs:
    JOG_WHEEL           = 0x00
    PART_COMMON_LEVEL   = 0x01
    PART_COMMON_PANNING = 0x02
    TUNE_PITCH          = 0x03
    TUNE_BEND           = 0x04
    PATTERN             = 0x05
    STEP_EDIT           = 0x06
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
    GENERAL             = 0x00
    def get():
        return {
            JogWheels.GENERAL           : JogWheel('GENERAL'   , 506, 134),
        }
        
class Faders:
    TEMPO               = 0x00
    def get():
        return {
            Faders.TEMPO                : Fader('TEMPO'     ,  76, 679,  88, 231),
        }

class Valves:
    VALVES              = 0x00
    def get():
        return {
            Valves.VALVES               : Valve('VALVES'    , 741, 161, 273, 154),
        }

class Lcds:
    MAIN                = 0x00
    def get():
        return {
            Lcds.MAIN                   : Lcd('MAIN'      ,  95, 151, 360, 168),
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
