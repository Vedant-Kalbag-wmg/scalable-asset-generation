import numpy as np
import librosa
import scipy.io.wavfile as wavfile
import math

def filter_data(audio_file_path, framerate, fn='1+x**4', format='disco'):
    # Load audio file
    # sample_rate, data = wavfile.read(audio_file_path)
    raw_data,sample_rate = librosa.load(audio_file_path, sr=None, mono=True)

    # # Average between channels. Take abs so we don't have phase issues (and we eventually want absolute value anyway, for volume).
    # def add_abs_array_elements(a, b):
    #     return np.abs(a) + np.abs(b)

    # channels = np.array([data[:, i] for i in range(data.shape[1])])
    # raw_data = np.apply_along_axis(add_abs_array_elements, 0, channels).mean(axis=0)
    
    samples = int(len(raw_data) / (sample_rate / framerate))+1
    block_size = int(len(raw_data) / samples)
    raw_data = raw_data/max(abs(raw_data))
    filtered_data = []
    for i in range(samples):
        chunk = abs(raw_data[i * block_size:(i + 1) * block_size - 1])
        # chunk=chunk/max(chunk)
        filtered_data.append(np.mean(chunk))
    
    # Normalize
    max_val = max(filtered_data)
    filtered_data = [x / max_val for x in filtered_data]

    # Evaluate expression for each point in filtered data
    filtered_data = [round(eval(fn.replace("x", str(x)).replace("y", str(ind))),2) for ind, x in enumerate(filtered_data)]

    # Format output based on selected format
    if format == "disco":
        output = filtered_data
    elif format == "csv":
        output = "\n".join([str(x) for x in filtered_data])

    return output


if __name__ == "__main__":
    audio_filepath='../resources/drums (3).wav'
    expression = '1+x*(3**2)'
    fps=15
    l=filter_data(audio_filepath, fps, expression, 'disco')
    output=""
    for i in range(len(l)):
        output+=f"{i}:({l[i]}), "
    print(output[:-2])