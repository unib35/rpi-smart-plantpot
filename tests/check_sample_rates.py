import sounddevice as sd

def list_supported_sample_rates(device=None):
    if device is None:
        device = sd.default.device[0]  # 기본 입력 장치
    try:
        device_info = sd.query_devices(device, 'input')
        print(f"장치: {device_info['name']}")
        print("지원되는 샘플링 주파수:")
        for rate in [8000, 16000, 22050, 44100, 48000, 96000]:
            try:
                sd.check_input_settings(device=device, samplerate=rate)
                print(f"  - {rate} Hz")
            except Exception:
                pass
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    list_supported_sample_rates()
