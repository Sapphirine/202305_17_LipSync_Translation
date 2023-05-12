# Replace the below method in original wav2lip
# The latest version of Librosa library takes sr as a named argument as opposed to the previous versions.

def _build_mel_basis():
    assert hp.fmax <= hp.sample_rate // 2
    return librosa.filters.mel(sr=hp.sample_rate, n_fft=hp.n_fft, n_mels=hp.num_mels,
                               fmin=hp.fmin, fmax=hp.fmax)
