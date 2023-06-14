from mmfutils.performance import fft
import numpy as np

import pytest

# import timeit


class Test_FFT(object):
    @classmethod
    def setup_class(cls):
        np.random.seed(1)

    def rand(self, shape, complex=True, writeable=False):
        X = np.random.random(shape) - 0.5
        if complex:
            X = X + 1j * (np.random.random(shape) - 0.5)

        # The default builders should respect this.  See issue #32.
        X.flags["WRITEABLE"] = writeable
        return X

    def test_fft(self, threads):
        shape = (256, 256)
        x = self.rand(shape)

        fft.set_num_threads(threads)
        for axis in [None, 0, 1, -1, -2]:
            kw = {}
            if axis is not None:
                kw = dict(axis=axis)
            assert np.allclose(fft.fft_numpy(x, **kw), np.fft.fft(x, **kw))
            assert np.allclose(fft.ifft_numpy(x, **kw), np.fft.ifft(x, **kw))

    def test_fftn(self, threads):
        shape = (256, 256)
        x = self.rand(shape)
        fft.set_num_threads(threads)
        for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
            kw = {}
            if axes is not None:
                kw = dict(axes=axes)
            assert np.allclose(fft.fftn_numpy(x, **kw), np.fft.fftn(x, **kw))
            assert np.allclose(fft.ifftn_numpy(x, **kw), np.fft.ifftn(x, **kw))


@pytest.mark.skipif(not hasattr(fft, "pyfftw"), reason="requires pyfftw")
class Test_FFT_pyfftw(Test_FFT):
    @classmethod
    def setup_class(cls):
        np.random.seed(1)

    def test_fft_pyfftw(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=False)

        fft.set_num_threads(threads)
        for axis in [None, 0, 1, -1, -2]:
            kw = {}
            if axis is not None:
                kw = dict(axis=axis)
            assert np.allclose(fft.fft_pyfftw(x, **kw), np.fft.fft(x, **kw))
            assert np.allclose(fft.ifft_pyfftw(x, **kw), np.fft.ifft(x, **kw))

    def test_fftn_pyfftw(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=False)

        fft.set_num_threads(threads)
        for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
            kw = {}
            if axes is not None:
                kw = dict(axes=axes)
            assert np.allclose(fft.fftn_pyfftw(x, **kw), np.fft.fftn(x, **kw))
            assert np.allclose(fft.ifftn_pyfftw(x, **kw), np.fft.ifftn(x, **kw))

    def test_get_fft_pyfftw(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=True)

        fft.set_num_threads(threads)
        for axis in [None, 0, 1, -1, -2]:
            kw = {}
            if axis is not None:
                kw = dict(axis=axis)
            assert np.allclose(fft.get_fft_pyfftw(x, **kw)(x), np.fft.fft(x, **kw))
            assert np.allclose(fft.get_ifft_pyfftw(x, **kw)(x), np.fft.ifft(x, **kw))

    def test_get_fftn_pyfftw(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=True)

        fft.set_num_threads(threads)
        for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
            kw = {}
            if axes is not None:
                kw = dict(axes=axes)
            assert np.allclose(fft.get_fftn_pyfftw(x, **kw)(x), np.fft.fftn(x, **kw))
            assert np.allclose(fft.get_ifftn_pyfftw(x, **kw)(x), np.fft.ifftn(x, **kw))

    def test_get_fft(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=True)

        fft.set_num_threads(threads)
        for axis in [None, 0, 1, -1, -2]:
            kw = {}
            if axis is not None:
                kw = dict(axis=axis)
            assert np.allclose(fft.get_fft(x, **kw)(x), np.fft.fft(x, **kw))
            assert np.allclose(fft.get_ifft(x, **kw)(x), np.fft.ifft(x, **kw))

    def test_get_fftn(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=True)

        fft.set_num_threads(threads)
        for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
            kw = {}
            if axes is not None:
                kw = dict(axes=axes)
            assert np.allclose(fft.get_fftn(x, **kw)(x), np.fft.fftn(x, **kw))
            assert np.allclose(fft.get_ifftn(x, **kw)(x), np.fft.ifftn(x, **kw))

    def test_fft(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=False)

        fft.set_num_threads(threads)
        for axis in [None, 0, 1, -1, -2]:
            kw = {}
            if axis is not None:
                kw = dict(axis=axis)
            for n in range(2):
                assert np.allclose(fft.fft(x, **kw), np.fft.fft(x, **kw))
                assert np.allclose(fft.ifft(x, **kw), np.fft.ifft(x, **kw))

    def test_fftn(self, threads):
        shape = (256, 256)
        x = self.rand(shape, writeable=False)

        fft.set_num_threads(threads)
        for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
            kw = {}
            if axes is not None:
                kw = dict(axes=axes)
            for n in range(2):
                assert np.allclose(fft.fftn(x, **kw), np.fft.fftn(x, **kw))
                assert np.allclose(fft.ifftn(x, **kw), np.fft.ifftn(x, **kw))
