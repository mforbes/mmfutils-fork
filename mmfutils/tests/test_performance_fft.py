import nose.tools as nt
# from nose.plugins.attrib import attr

from mmfutils.performance import fft
import numpy as np
from nose import SkipTest

# import timeit


class Test_FFT(object):
    def setUp(self):
        np.random.seed(1)

    def rand(self, shape, complex=True):
        X = np.random.random(shape) - 0.5
        if complex:
            X = X + 1j*(np.random.random(shape) - 0.5)
        return X

    def test_fft(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axis in [None, 0, 1, -1, -2]:
                kw = {}
                if axis is not None:
                    kw = dict(axis=axis)
                nt.ok_(np.allclose(fft.fft_numpy(x, **kw),
                                   np.fft.fft(x, **kw)))
                nt.ok_(np.allclose(fft.ifft_numpy(x, **kw),
                                   np.fft.ifft(x, **kw)))

    def test_fftn(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
                kw = {}
                if axes is not None:
                    kw = dict(axes=axes)
                nt.ok_(np.allclose(fft.fftn_numpy(x, **kw),
                                   np.fft.fftn(x, **kw)))
                nt.ok_(np.allclose(fft.ifftn_numpy(x, **kw),
                                   np.fft.ifftn(x, **kw)))


class Test_FFT_pyfftw(Test_FFT):
    def setUp(self):
        if not hasattr(fft, 'pyfftw'):
            raise SkipTest("No pyfftw")

        np.random.seed(1)

    def test_fft_pyfftw(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axis in [None, 0, 1, -1, -2]:
                kw = {}
                if axis is not None:
                    kw = dict(axis=axis)
                nt.ok_(np.allclose(fft.fft_pyfftw(x, **kw),
                                   np.fft.fft(x, **kw)))
                nt.ok_(np.allclose(fft.ifft_pyfftw(x, **kw),
                                   np.fft.ifft(x, **kw)))

    def test_fftn_pyfftw(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
                kw = {}
                if axes is not None:
                    kw = dict(axes=axes)
                nt.ok_(np.allclose(fft.fftn_pyfftw(x, **kw),
                                   np.fft.fftn(x, **kw)))
                nt.ok_(np.allclose(fft.ifftn_pyfftw(x, **kw),
                                   np.fft.ifftn(x, **kw)))

    def test_get_fft_pyfftw(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axis in [None, 0, 1, -1, -2]:
                kw = {}
                if axis is not None:
                    kw = dict(axis=axis)
                nt.ok_(np.allclose(fft.get_fft_pyfftw(x, **kw)(x),
                                   np.fft.fft(x, **kw)))
                nt.ok_(np.allclose(fft.get_ifft_pyfftw(x, **kw)(x),
                                   np.fft.ifft(x, **kw)))

    def test_get_fftn_pyfftw(self):
        shape = (256, 256)
        x = self.rand(shape)

        for threads in [1, 2]:
            fft.set_num_threads(threads)
            for axes in [None, [0], [1], [-1], [-2], [1, 0]]:
                kw = {}
                if axes is not None:
                    kw = dict(axes=axes)
                nt.ok_(np.allclose(fft.get_fftn_pyfftw(x, **kw)(x),
                                   np.fft.fftn(x, **kw)))
                nt.ok_(np.allclose(fft.get_ifftn_pyfftw(x, **kw)(x),
                                   np.fft.ifftn(x, **kw)))
