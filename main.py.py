import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

def process_audio(file_path, output_file, plot_index):
    # Load Noisy Speech Signal
    Fs, noisy_signal = wavfile.read(file_path)

    # Convert to Mono if Stereo
    if len(noisy_signal.shape) > 1:
        noisy_signal = np.mean(noisy_signal, axis=1)

    # Normalize Signal
    noisy_signal = noisy_signal / np.max(np.abs(noisy_signal))

    # Parameters
    frame_size = 1024
    overlap = frame_size // 2
    window = np.hamming(frame_size)
    noise_reduction_factor = 0.7  # Experiment: 0.4 - 0.7

    # Frame count
    num_frames = int(np.ceil((len(noisy_signal) - overlap) / (frame_size - overlap)))

    # Pad signal
    padded_length = (num_frames * (frame_size - overlap)) + overlap
    noisy_signal = np.pad(noisy_signal, (0, padded_length - len(noisy_signal)), 'constant')

    # Initialize output
    enhanced_signal = np.zeros_like(noisy_signal)

    # Noise estimate (from the first few frames)
    noise_frames = 5
    noise_spectrum = 0
    for i in range(noise_frames):
        start = i * (frame_size - overlap)
        frame = noisy_signal[start:start + frame_size] * window
        spectrum = np.abs(np.fft.rfft(frame))
        noise_spectrum += spectrum
    noise_spectrum /= noise_frames

    # Process each frame
    for i in range(num_frames):
        start = i * (frame_size - overlap)
        frame = noisy_signal[start:start + frame_size] * window

        # FFT
        spectrum = np.fft.rfft(frame)

        # Spectral subtraction
        magnitude = np.abs(spectrum)
        phase = np.angle(spectrum)
        clean_magnitude = np.maximum(magnitude - noise_reduction_factor * noise_spectrum, 0)

        # Reconstruct spectrum
        clean_spectrum = clean_magnitude * np.exp(1j * phase)

        # Inverse FFT
        clean_frame = np.fft.irfft(clean_spectrum)

        # Overlap-add
        enhanced_signal[start:start + frame_size] += clean_frame * window

    # Normalize
    enhanced_signal /= np.max(np.abs(enhanced_signal))

    # Save output
    wavfile.write(output_file, Fs, (enhanced_signal * 32767).astype(np.int16))
    print(f"Processed and saved: {output_file}")

    # SNR Calculation (Before and After)
    snr_before = 10 * np.log10(np.mean(noisy_signal**2) / np.mean(noise_spectrum**2))
    snr_after = 10 * np.log10(np.mean(enhanced_signal**2) / np.mean(noise_spectrum**2))
    print(f"SNR Before Enhancement: {snr_before:.2f} dB")
    print(f"SNR After Enhancement: {snr_after:.2f} dB")

    # Spectrogram Visualization
    plt.figure(figsize=(12, 6))

    # Spectrogram before enhancement
    plt.subplot(2, 1, 1)
    plt.specgram(noisy_signal, NFFT=frame_size, Fs=Fs, noverlap=overlap)
    plt.title(f'Spectrogram - Noisy Signal')

    # Spectrogram after enhancement
    plt.subplot(2, 1, 2)
    plt.specgram(enhanced_signal, NFFT=frame_size, Fs=Fs, noverlap=overlap)
    plt.title(f'Spectrogram - Enhanced Signal')

    plt.tight_layout()
    plot_filename = f'plot{plot_index}.png'
    plt.savefig(plot_filename, dpi=300)
    plt.show()
    print(f"Spectrogram saved as: {plot_filename}")

# List of noisy audio files
noisy_audio_files = ['noisy_audio1.wav', 'noisy_audio2.wav', 'noisy_audio3.wav']

# Process each audio file
for i, noisy_audio in enumerate(noisy_audio_files, start=1):
    output_file = f'enhanced_ss{i}.wav'
    if os.path.exists(noisy_audio):
        process_audio(noisy_audio, output_file, i)
    else:
        print(f"File {noisy_audio} does not exist. Skipping...")