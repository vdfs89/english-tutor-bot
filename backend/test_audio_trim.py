import io
import os
import sys

import numpy as np
import soundfile as sf

# Adiciona o diretório raiz ao path para conseguir importar o backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_utils import trim_trailing_silence


def run_test():
    print("🔊 Gerando áudio sintético para teste...")
    sr = 16000  # Taxa de amostragem

    # 1.0 segundo de som (onda senoidal - "bip")
    t = np.linspace(0, 1.0, sr)
    audio_signal = 0.5 * np.sin(2 * np.pi * 440 * t)

    # 2.0 segundos de silêncio absoluto
    silence = np.zeros(sr * 2)

    # Combina: Som + Silêncio (Total 3s)
    combined = np.concatenate((audio_signal, silence))

    # Converte para bytes (simulando um arquivo WAV)
    buffer = io.BytesIO()
    sf.write(buffer, combined, sr, format="WAV")
    buffer.seek(0)
    original_bytes = buffer.read()

    print(f"   Tamanho original: {len(original_bytes)} bytes (Duração: ~3.0s)")

    # --- TESTE DA FUNÇÃO ---
    print("✂️  Executando trim_trailing_silence...")
    processed_bytes = trim_trailing_silence(original_bytes)

    # Verifica o resultado lendo o arquivo processado
    data, _ = sf.read(io.BytesIO(processed_bytes))
    new_duration = len(data) / sr

    print(f"   Duração final: {new_duration:.2f}s")

    if 0.9 <= new_duration <= 1.1:
        print("✅ SUCESSO: O silêncio final foi removido corretamente!")
    else:
        print(f"❌ FALHA: A duração esperada era ~1.0s, mas obteve {new_duration:.2f}s")


if __name__ == "__main__":
    run_test()
