import numpy as np
from matplotlib import _api


def window_hanning(x):
    """
    Return *x* times the Hanning (or Hann) window of len(*x*).

    See Also
    --------
    window_none : Another window algorithm.
    """
    return np.hanning(len(x))*x


def window_none(x):
    """
    No window function; simply return *x*.

    See Also
    --------
    window_hanning : Another window algorithm.
    """
    return x


def detrend(x, key=None, axis=None):
    """
    Return *x* with its trend removed.

    Parameters
    ----------
    x : array or sequence
        Array or sequence containing the data.

    key : {'default', 'constant', 'mean', 'linear', 'none'} or function
        The detrending algorithm to use. 'default', 'mean', and 'constant' are
        the same as `detrend_mean`. 'linear' is the same as `detrend_linear`.
        'none' is the same as `detrend_none`. The default is 'mean'. See the
        corresponding functions for more details regarding the algorithms. Can
        also be a function that carries out the detrend operation.

    axis : int
        The axis along which to do the detrending.

    See Also
    --------
    detrend_none : Implementation of the 'none' algorithm.
    """

    if callable(key):
        x = np.asarray(x)
        if axis is not None and axis + 1 > x.ndim:
            raise ValueError(f'axis(={axis}) out of bounds')
        try:
            return key(x, axis=axis)
        except TypeError:
            return np.apply_along_axis(key, axis=axis, arr=x)

def detrend_none(x):
    """
    Return *x*: no detrending.

    Parameters
    ----------
    x : any object
        An object containing the data

    axis : int
        This parameter is ignored.
        It is included for compatibility with detrend_mean

    See Also
    --------
    detrend : A wrapper around all the detrend algorithms.
    """
    return x


def _stride_windows(x, n, noverlap=0, axis=0):
    # np>=1.20 provides sliding_window_view, and we only ever use axis=0.
    if hasattr(np.lib.stride_tricks, "sliding_window_view") and axis == 0:
        if noverlap >= n:
            raise ValueError('noverlap must be less than n')
        return np.lib.stride_tricks.sliding_window_view(
            x, n, axis=0)[::n - noverlap].T

    if noverlap >= n:
        raise ValueError('noverlap must be less than n')
    if n < 1:
        raise ValueError('n cannot be less than 1')

    x = np.asarray(x)

    if n == 1 and noverlap == 0:
        if axis == 0:
            return x[np.newaxis]
        else:
            return x[np.newaxis].T
    if n > x.size:
        raise ValueError('n cannot be greater than the length of x')

    # np.lib.stride_tricks.as_strided easily leads to memory corruption for
    # non integer shape and strides, i.e. noverlap or n. See #3845.
    noverlap = int(noverlap)
    n = int(n)

    step = n - noverlap
    if axis == 0:
        shape = (n, (x.shape[-1]-noverlap)//step)
        strides = (x.strides[0], step*x.strides[0])
    else:
        shape = ((x.shape[-1]-noverlap)//step, n)
        strides = (step*x.strides[0], x.strides[0])
    return np.lib.stride_tricks.as_strided(x, shape=shape, strides=strides)


def _spectral_helper(x, NFFT=None, Fs=None, noverlap=None):
    """
    Private helper implementing the common parts between the psd, csd,
    spectrogram and complex, magnitude, angle, and phase spectrums.
    """

    scale_by_freq = True
    pad_to = NFFT
    detrend_func = detrend_none
    window = window_hanning

    if Fs is None:
        Fs = 2
    if noverlap is None:
        noverlap = 0

    # if NFFT is set to None use the whole signal
    if NFFT is None:
        NFFT = 256

    # Make sure we're dealing with a numpy array. If y and x were the same
    # object to start with, keep them that way
    x = np.asarray(x)

    # zero pad x and y up to NFFT if they are shorter than NFFT
    if len(x) < NFFT:
        n = len(x)
        x = np.resize(x, NFFT)
        x[n:] = 0

    # For real x, ignore the negative frequencies unless told otherwise
    if pad_to % 2:
           numFreqs = (pad_to + 1)//2
    else:
        numFreqs = pad_to//2 + 1
    scaling_factor = 2.

    if not np.iterable(window):
        window = window(np.ones(NFFT, x.dtype))
    if len(window) != NFFT:
        raise ValueError(
            "The window length must match the data's first dimension")

    result = _stride_windows(x, NFFT, noverlap)
    result = detrend(result, detrend_func, axis=0)
    result = result * window.reshape((-1, 1))
    result = np.fft.fft(result, n=pad_to, axis=0)[:numFreqs, :]

    result = np.conj(result) * result


    # Also include scaling factors for one-sided densities and dividing by
    # the sampling frequency, if desired. Scale everything, except the DC
    # component and the NFFT/2 component:
    # if we have a even number of frquencies, don't scale NFFT/2
    if not NFFT % 2:
        slc = slice(1, -1, None)
    # if we have an odd number, just don't scale DC
    else:
        slc = slice(1, None, None)

    result[slc] *= scaling_factor

    # MATLAB divides by the sampling frequency so that density function
    # has units of dB/Hz and can be integrated by the plotted frequency
    # values. Perform the same scaling here.
    if scale_by_freq:
        result /= Fs
        # Scale the spectrum by the norm of the window to compensate for
        # windowing loss; see Bendat & Piersol Sec 11.5.2.
        result /= (window**2).sum()

    result=result.real
    return result

def func_cut(audio_data, sample_rate ,NFFT ,Fs ,noverlap):

    #Freq
    if NFFT % 2:
        numFreqs = (NFFT + 1)//2
    else:
        numFreqs = NFFT//2 + 1

    freq = np.fft.fftfreq(NFFT, 1/sample_rate)[:numFreqs]
    if not NFFT % 2:
        # get the last value correctly, it is negative otherwise
        freq[-1] *= -1

    #Bins
    bins = np.arange(NFFT/2, len(audio_data) - NFFT/2 + 1, NFFT - noverlap)/Fs

    #Pxx
    Pxx=_spectral_helper(x=audio_data, NFFT=NFFT, Fs=Fs, noverlap=noverlap)

    return Pxx, freq, bins