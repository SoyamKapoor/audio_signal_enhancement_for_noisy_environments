# 🎤 Speech Enhancement using Spectral Subtraction

This project applies **Spectral Subtraction** to enhance noisy speech signals using Python. It removes background noise by estimating and subtracting the noise spectrum from the speech signal, improving the Signal-to-Noise Ratio (SNR). The implementation includes audio processing, visualization, and output comparison.

---

## 📌 Project Overview

### Objectives:
- Load and process noisy `.wav` audio files
- Apply windowing and spectral subtraction techniques
- Estimate noise profile from initial frames
- Perform frame-by-frame FFT and reconstruct clean signal
- Save enhanced audio output
- Visualize spectrograms before and after enhancement
- Calculate SNR before and after enhancement

---

## 🧰 Tools & Libraries Used

- Python 3.x
- NumPy
- SciPy (for FFT, signal processing, and WAV handling)
- Matplotlib (for spectrogram visualization)
  
## 📊 Key Steps in the Enhancement Process

1. **Audio Loading & Normalization**
   - Mono conversion and normalization of amplitude values

2. **Noise Estimation**
   - Estimated from the first few frames using magnitude averaging

3. **Spectral Subtraction**
   - FFT applied to each frame
   - Magnitude spectrum adjusted using estimated noise
   - Clean spectrum reconstructed and signal reassembled using overlap-add method

4. **Output & Visualization**
   - Enhanced signal saved as `.wav`
   - Spectrograms plotted for comparison
   - SNR before and after enhancement printed for evaluation

## 🚀 How to Run the Notebook

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/audio_signal_enhancement_for_noisy_environments.git
   cd audio_signal_enhancement_for_noisy_environments
   ```

2. **Install Required Packages**
   Make sure you have Python 3.12.8 and Jupyter Notebook installed. You can install the required libraries using pip:

   ```bash
   pip install numpy scipy matplotlib
   ```

3. **Run the script**
   ```bash
   main.ipynb
   ```
## 📌 Conclusion

This project demonstrates a simple yet effective noise reduction technique for real-world audio enhancement.  
The improvement in **SNR** and clearer **spectrograms** show that **Spectral Subtraction** can be a useful preprocessing step in **speech recognition systems** and **audio communication platforms**.
