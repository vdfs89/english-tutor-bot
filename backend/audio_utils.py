import io

import numpy as np
import soundfile as sf


def trim_trailing_silence(
    audio_bytes: bytes,
    threshold: float = 0.01,
    frame_ms: int = 30,
) -> bytes:
    """
    Corta o silêncio no final do áudio (bytes WAV) e retorna novos bytes.
    Isso evita que o Whisper alucine repetições em trechos de silêncio.
    """
    try:
        # Lê o áudio a partir dos bytes
        data, sr = sf.read(io.BytesIO(audio_bytes))

        # Garante array 1D (mono)
        if len(data.shape) > 1:
            data = data.mean(axis=1)

        frame_len = int(sr * frame_ms / 1000)
        if frame_len <= 0:
            return audio_bytes

        # Calcula RMS (energia) por frame
        rms = []
        for i in range(0, len(data), frame_len):
            frame = data[i : i + frame_len]
            if len(frame) == 0:
                break
            rms.append(np.sqrt(np.mean(frame**2)))

        # Encontra o último frame com voz acima do threshold
        # Se não achar nada (tudo silêncio), mantém o áudio original ou retorna vazio
        if len(rms) > 0:
            last_voice_idx = len(rms) - 1
            for i in range(len(rms) - 1, -1, -1):
                if rms[i] >= threshold:
                    last_voice_idx = i
                    break

            samples_keep = min(len(data), (last_voice_idx + 1) * frame_len)
            trimmed = data[:samples_keep]

            # Retorna o áudio cortado
            buf = io.BytesIO()
            sf.write(buf, trimmed, sr, format="WAV")
            buf.seek(0)
            return buf.read()

        return audio_bytes
    except Exception as e:
        print(f"Erro ao cortar silêncio: {e}")
        return audio_bytes
