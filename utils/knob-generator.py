#------------------------------------------------------------------------------
import os           ; os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import warnings     ; warnings.filterwarnings("ignore", category=UserWarning, message=".*pkg_resources is deprecated as an API.*")
#------------------------------------------------------------------------------
import argparse
import math
import pygame
from colorama import init, Back, Fore, Style

init()

def extract_frame(atlas, index, frame_size, vertical):
    """Extrae un frame del atlas original."""

    frame = pygame.Surface(
        (frame_size, frame_size),
        pygame.SRCALPHA
    )

    if vertical:
        x = 0
        y = index * frame_size
    else:
        x = index * frame_size
        y = 0

    frame.blit(
        atlas,
        (0, 0),
        area=(x, y, frame_size, frame_size)
    )

    return frame


def generate_frame(current, following, fraction, frame_size):
    """Aplica el algoritmo original de interpolación y rotación."""

    degrees_per_frame = 360.0 / INPUT_FRAMES

    # Ángulo de interpolación dentro del intervalo.
    fine_rotation = fraction * degrees_per_frame

    # Alpha del frame siguiente.
    alpha = int(fraction * 255)

    # Frame actual: base opaca.
    surface_current = current.copy()

    # Frame siguiente.
    raw_next = following.copy()

    # Pre-rotación del siguiente frame.
    rotated_next = pygame.transform.rotate(
        raw_next,
        degrees_per_frame
    )

    surface_next = pygame.Surface(
        (frame_size, frame_size),
        pygame.SRCALPHA
    )

    rect = rotated_next.get_rect()
    rect.center = (frame_size // 2, frame_size // 2)

    surface_next.blit(rotated_next, rect.topleft)
    surface_next.set_alpha(alpha)

    # Composición.
    combined = pygame.Surface(
        (frame_size, frame_size),
        pygame.SRCALPHA
    )

    combined.blit(surface_current, (0, 0))
    combined.blit(surface_next, (0, 0))

    # Rotación fina definitiva.
    return pygame.transform.rotate(
        combined,
        -fine_rotation
    )


def generate_atlas(input_path, input_frames, vertical, output_path):

    global INPUT_FRAMES
    INPUT_FRAMES = input_frames

    atlas = pygame.image.load(input_path)

    width, height = atlas.get_size()

    # Calcular tamaño de cada frame.
    if vertical:
        if height % input_frames != 0:
            raise ValueError(
                "La altura del atlas no es divisible "
                "por el número de frames."
            )

        frame_size = height // input_frames

        if width != frame_size:
            raise ValueError(
                "Los frames deben ser cuadrados."
            )

    else:
        if width % input_frames != 0:
            raise ValueError(
                "La anchura del atlas no es divisible "
                "por el número de frames."
            )

        frame_size = width // input_frames

        if height != frame_size:
            raise ValueError(
                "Los frames deben ser cuadrados."
            )

    print(f"Atlas de entrada: {width}x{height}")
    print(f"Tamaño de frame: {frame_size}x{frame_size}")

    # Cargar todos los frames originales.
    frames = [
        extract_frame(atlas, i, frame_size, vertical)
        for i in range(input_frames)
    ]

    # Diez frames de salida por cada frame de entrada.
    output_frames = input_frames * 10

    # Tamaño de celda: suficiente para evitar recortes
    # durante cualquier rotación.
    output_size = math.ceil(frame_size * math.sqrt(2))

    # Distribución automática del atlas.
    columns = math.ceil(math.sqrt(output_frames))
    rows = math.ceil(output_frames / columns)

    output_atlas = pygame.Surface(
        (
            columns * output_size,
            rows * output_size
        ),
        pygame.SRCALPHA
    )

    print(f"Frames de salida: {output_frames}")
    print(f"Celda de salida: {output_size}x{output_size}")
    print(f"Atlas final: {columns}x{rows} frames")
    print("Generando...")

    frame_index = 0

    for i in range(input_frames):

        current = frames[i]

        # Conexión circular con el primer frame.
        following = frames[(i + 1) % input_frames]

        for subframe in range(10):

            fraction = subframe / 10.0

            rendered = generate_frame(
                current,
                following,
                fraction,
                frame_size
            )

            # Posición en el atlas de salida.
            column = frame_index % columns
            row = frame_index // columns

            cell_x = column * output_size
            cell_y = row * output_size

            # Centrar el resultado en su celda.
            rect = rendered.get_rect()
            rect.center = (
                cell_x + output_size // 2,
                cell_y + output_size // 2
            )

            output_atlas.blit(
                rendered,
                rect.topleft
            )

            frame_index += 1

        print(
            f"\rProcesados: {frame_index}/{output_frames}",
            end=""
        )

    pygame.image.save(output_atlas, output_path)

    print()
    print(f"¡Atlas generado!: {output_path}")
    print(
        f"Resolución final: "
        f"{output_atlas.get_width()}x"
        f"{output_atlas.get_height()}"
    )


def main():

    parser = argparse.ArgumentParser(
        description = (
            Fore.CYAN + Style.BRIGHT +
            "KNOB GENERATOR" + Style.RESET_ALL + "\n"
            + Fore.WHITE +
            "A graphical processing tool that converts an original rotational sprite "
            "frame atlas into a high-resolution animation atlas with 10x the original "
            "frame count.\n\n"
            + Fore.YELLOW + Style.BRIGHT +
            "PROCESSING PIPELINE\n" + Style.RESET_ALL
            + Fore.GREEN +
            "  1. " + Style.RESET_ALL + "Loads a sprite atlas containing discrete rotation frames.\n"
            + Fore.GREEN +
            "  2. " + Style.RESET_ALL + "Extracts individual frames from horizontal or vertical layouts.\n"
            + Fore.GREEN +
            "  3. " + Style.RESET_ALL + "Interpolates each frame interval using alpha blending.\n"
            + Fore.GREEN +
            "  4. " + Style.RESET_ALL + "Pre-rotates the next frame to align consecutive sprite positions.\n"
            + Fore.GREEN +
            "  5. " + Style.RESET_ALL + "Applies fine software rotation to generate intermediate orientations.\n"
            + Fore.GREEN +
            "  6. " + Style.RESET_ALL + "Wraps the final frame back to the first for seamless 360-degree rotation.\n"
            + Fore.GREEN +
            "  7. " + Style.RESET_ALL + "Packs all generated frames into a new PNG sprite atlas.\n\n"
            + Fore.YELLOW + Style.BRIGHT +
            "TECHNICAL DETAILS\n" + Style.RESET_ALL
            + Fore.WHITE +
            "  - Generates 10 output frames per original frame interval.\n"
            "  - Uses per-frame alpha compositing and pygame software transformations.\n"
            "  - Preserves sprite transparency (RGBA).\n"
            "  - Automatically calculates frame dimensions from the source atlas.\n"
            "  - Supports horizontal and vertical source atlases.\n"
            "  - Centers rotated frames inside uniform output cells to prevent clipping.\n"
            "  - Produces a pre-rendered atlas, eliminating runtime interpolation and rotation.\n\n"
            + Fore.MAGENTA + Style.BRIGHT +
            "Designed for bitmap filmstrip controls and frame-based rotary knob animations."
            + Style.RESET_ALL
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "input",
        help="Atlas original PNG"
    )

    parser.add_argument(
        "frames",
        type=int,
        help="Número de frames del atlas original"
    )

    parser.add_argument(
        "--vertical",
        action="store_true",
        help="El atlas de entrada está organizado verticalmente"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Nombre del atlas de salida"
    )

    args = parser.parse_args()

    if args.frames < 1:
        parser.error("El número de frames debe ser mayor que cero.")

    if not os.path.isfile(args.input):
        parser.error("No se encuentra el atlas de entrada.")

    output_path = args.output

    if output_path is None:
        base, _ = os.path.splitext(args.input)
        output_path = f"{base}_generated.png"

    generate_atlas(
        args.input,
        args.frames,
        args.vertical,
        output_path
    )


if __name__ == "__main__":
    pygame.init()
    print()
    main()
    print()    
    pygame.quit()
