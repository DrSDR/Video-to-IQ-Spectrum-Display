import imageio
import numpy as np

# Configuration Flags
video_path = 'pdance.mp4'
output_iq_path = 'output_row_data.iq'
flip_upside_down = True  # Set to True to flip the image vertically, False to keep normal

# Open the video file stream using imageio
reader = imageio.get_reader(video_path, 'ffmpeg')

# Open binary file to stream/write IQ data
with open(output_iq_path, 'wb') as iq_file:
    for frame_count, frame in enumerate(reader):
        
        # 1. Convert frame to grayscale using standard ITU-R 601-2 luma transform
        gray_frame = (0.299 * frame[:, :, 0] + 
                      0.587 * frame[:, :, 1] + 
                      0.114 * frame[:, :, 2]).astype(np.float32)
        
        # 2. Check the flag and flip the frame vertically if True
        if flip_upside_down:
            gray_frame = gray_frame[::-1, :]  # Reverse the row order (y-axis)
        
        # 3. Shift the zero-frequency component along rows only (axis=1)
        shifted_frame = np.fft.ifftshift(gray_frame, axes=1)
        
        # 4. Generate a random phase for every single pixel in the frame
        random_angles = np.random.uniform(0, 2 * np.pi, size=shifted_frame.shape).astype(np.float32)
        random_phase = np.exp(1j * random_angles)
        phased_frame = shifted_frame * random_phase
        
        # 5. Compute the 1D Inverse Fast Fourier Transform along rows only (axis=1)
        ifft_frame = np.fft.ifft(phased_frame, axis=1)
        
        # 6. Flatten and interleave into [I0, Q0, I1, Q1...]
        iq_interleaved = np.empty(ifft_frame.size * 2, dtype=np.float32)
        iq_interleaved[0::2] = ifft_frame.real.flatten()  # In-phase (Real)
        iq_interleaved[1::2] = ifft_frame.imag.flatten()  # Quadrature (Imaginary)
        
        # 7. Peak Normalize the interleaved frame to the range [-1.0, 1.0]
        peak_val = np.max(np.abs(iq_interleaved))
        if peak_val > 0:
            iq_interleaved /= peak_val
        
        # 8. Write raw float32 bytes to the output file
        iq_file.write(iq_interleaved.tobytes())
        
        if (frame_count + 1) % 30 == 0:
            print(f"Processed {frame_count + 1} frames...")

reader.close()
print(f"Finished! IQ file saved to: {output_iq_path}")
