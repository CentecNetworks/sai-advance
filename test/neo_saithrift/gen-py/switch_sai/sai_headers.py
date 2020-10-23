'''Wrapper for saiacl.h

Generated with:
/opt/Python-2.7.13/bin/ctypesgen.py -I/usr/include -I/data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc --include /usr/include/linux/limits.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiacl.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saibfd.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saibridge.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saibuffer.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saicounter.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saidebugcounter.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saidtel.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saies.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saifdb.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sai.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saihash.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saihostif.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiipmcgroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiipmc.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiisolationgroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sail2mcgroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sail2mc.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sailag.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saimcastfdb.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saimirror.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saimonitor.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saimpls.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saineighbor.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainexthopgroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainexthop.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainpm.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiobject.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saipolicer.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiport.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiptp.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiqosmap.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiqueue.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairouterinterface.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairpfgroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saisamplepacket.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saischedulergroup.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saischeduler.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saisegmentroute.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saistatus.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saistp.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiswitch.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saisynce.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitam.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitunnel.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitwamp.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiuburst.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiudf.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saivirtualrouter.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saivlan.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiwred.h /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saiy1731.h -o gen-py/switch_sai/sai_headers.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# No libraries

# No modules

sai_status_t = c_int32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 87

sai_switch_profile_id_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 88

sai_vlan_id_t = c_uint16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 89

sai_attr_id_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 90

sai_cos_t = c_uint8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 91

sai_queue_index_t = c_uint8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 92

sai_mac_t = c_uint8 * 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 93

sai_ip4_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 94

sai_ip6_t = c_uint8 * 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 95

sai_switch_hash_seed_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 96

sai_label_id_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 97

sai_stat_id_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 98

sai_uint64_t = c_uint64 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 112

sai_int64_t = c_int64 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 113

sai_uint32_t = c_uint32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 114

sai_int32_t = c_int32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 115

sai_uint16_t = c_uint16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 116

sai_int16_t = c_int16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 117

sai_uint8_t = c_uint8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 118

sai_int8_t = c_int8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 119

sai_size_t = c_size_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 120

sai_object_id_t = c_uint64 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 121

sai_pointer_t = POINTER(None) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 122

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 128
class struct__sai_timespec_t(Structure):
    pass

struct__sai_timespec_t.__slots__ = [
    'tv_sec',
    'tv_nsec',
]
struct__sai_timespec_t._fields_ = [
    ('tv_sec', c_uint64),
    ('tv_nsec', c_uint32),
]

sai_timespec_t = struct__sai_timespec_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 128

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 140
class struct__sai_captured_timespec_t(Structure):
    pass

struct__sai_captured_timespec_t.__slots__ = [
    'timestamp',
    'secquence_id',
    'port_id',
]
struct__sai_captured_timespec_t._fields_ = [
    ('timestamp', sai_timespec_t),
    ('secquence_id', sai_uint16_t),
    ('port_id', sai_object_id_t),
]

sai_captured_timespec_t = struct__sai_captured_timespec_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 140

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 153
class struct__sai_timeoffset_t(Structure):
    pass

struct__sai_timeoffset_t.__slots__ = [
    'flag',
    'value',
]
struct__sai_timeoffset_t._fields_ = [
    ('flag', c_uint8),
    ('value', c_uint32),
]

sai_timeoffset_t = struct__sai_timeoffset_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 153

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 181
class struct__sai_object_list_t(Structure):
    pass

struct__sai_object_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_object_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_object_id_t)),
]

sai_object_list_t = struct__sai_object_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 181

enum__sai_common_api_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_CREATE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_REMOVE = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_SET = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_GET = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_BULK_CREATE = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_BULK_REMOVE = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_BULK_SET = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_BULK_GET = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

SAI_COMMON_API_MAX = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

sai_common_api_t = enum__sai_common_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 197

enum__sai_object_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NULL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_PORT = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_LAG = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_VIRTUAL_ROUTER = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NEXT_HOP = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NEXT_HOP_GROUP = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ROUTER_INTERFACE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_TABLE = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_ENTRY = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_COUNTER = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_RANGE = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_TABLE_GROUP = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_MIRROR_SESSION = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SAMPLEPACKET = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_STP = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_POLICER = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_WRED = 19 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_QOS_MAP = 20 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_QUEUE = 21 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SCHEDULER = 22 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SCHEDULER_GROUP = 23 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_BUFFER_POOL = 24 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_BUFFER_PROFILE = 25 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP = 26 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_LAG_MEMBER = 27 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HASH = 28 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_UDF = 29 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_UDF_MATCH = 30 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_UDF_GROUP = 31 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_FDB_ENTRY = 32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SWITCH = 33 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF_TRAP = 34 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY = 35 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NEIGHBOR_ENTRY = 36 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ROUTE_ENTRY = 37 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_VLAN = 38 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_VLAN_MEMBER = 39 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF_PACKET = 40 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TUNNEL_MAP = 41 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TUNNEL = 42 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY = 43 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_FDB_FLUSH = 44 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER = 45 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_STP_PORT = 46 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_RPF_GROUP = 47 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_RPF_GROUP_MEMBER = 48 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_L2MC_GROUP = 49 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER = 50 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_IPMC_GROUP = 51 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER = 52 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_L2MC_ENTRY = 53 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_IPMC_ENTRY = 54 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_MCAST_FDB_ENTRY = 55 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP = 56 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_BRIDGE = 57 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_BRIDGE_PORT = 58 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY = 59 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM = 60 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SEGMENTROUTE_SIDLIST = 61 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_PORT_POOL = 62 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_INSEG_ENTRY = 63 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DTEL = 64 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DTEL_QUEUE_REPORT = 65 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DTEL_INT_SESSION = 66 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DTEL_REPORT_SESSION = 67 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DTEL_EVENT = 68 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_BFD_SESSION = 69 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ISOLATION_GROUP = 70 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER = 71 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_MATH_FUNC = 72 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_REPORT = 73 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD = 74 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_TEL_TYPE = 75 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_TRANSPORT = 76 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_TELEMETRY = 77 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_COLLECTOR = 78 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_EVENT_ACTION = 79 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_EVENT = 80 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NAT_ZONE_COUNTER = 81 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NAT_ENTRY = 82 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TAM_INT = 83 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_COUNTER = 84 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_DEBUG_COUNTER = 85 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_PORT_SERDES = 86 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_TWAMP = 87 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_NPM = 88 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_ES = 89 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_Y1731_MEG = 90 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_Y1731_SESSION = 91 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_Y1731_REMOTE_MEP = 92 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_PTP_DOMAIN = 93 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_SYNCE = 94 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_MONITOR_BUFFER = 95 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_MONITOR_LATENCY = 96 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

SAI_OBJECT_TYPE_MAX = 97 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

sai_object_type_t = enum__sai_object_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 303

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 309
class struct__sai_bool_list_t(Structure):
    pass

struct__sai_bool_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_bool_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_uint8)),
]

sai_bool_list_t = struct__sai_bool_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 309

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 315
class struct__sai_u8_list_t(Structure):
    pass

struct__sai_u8_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u8_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_uint8)),
]

sai_u8_list_t = struct__sai_u8_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 315

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 326
class struct__sai_s8_list_t(Structure):
    pass

struct__sai_s8_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s8_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_int8)),
]

sai_s8_list_t = struct__sai_s8_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 326

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 332
class struct__sai_u16_list_t(Structure):
    pass

struct__sai_u16_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u16_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_uint16)),
]

sai_u16_list_t = struct__sai_u16_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 332

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 338
class struct__sai_s16_list_t(Structure):
    pass

struct__sai_s16_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s16_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_int16)),
]

sai_s16_list_t = struct__sai_s16_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 338

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 344
class struct__sai_u32_list_t(Structure):
    pass

struct__sai_u32_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u32_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_uint32)),
]

sai_u32_list_t = struct__sai_u32_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 344

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 350
class struct__sai_s32_list_t(Structure):
    pass

struct__sai_s32_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s32_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(c_int32)),
]

sai_s32_list_t = struct__sai_s32_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 350

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 356
class struct__sai_u32_range_t(Structure):
    pass

struct__sai_u32_range_t.__slots__ = [
    'min',
    'max',
]
struct__sai_u32_range_t._fields_ = [
    ('min', c_uint32),
    ('max', c_uint32),
]

sai_u32_range_t = struct__sai_u32_range_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 356

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 362
class struct__sai_s32_range_t(Structure):
    pass

struct__sai_s32_range_t.__slots__ = [
    'min',
    'max',
]
struct__sai_s32_range_t._fields_ = [
    ('min', c_int32),
    ('max', c_int32),
]

sai_s32_range_t = struct__sai_s32_range_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 362

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 375
class struct__sai_vlan_list_t(Structure):
    pass

struct__sai_vlan_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_vlan_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_vlan_id_t)),
]

sai_vlan_list_t = struct__sai_vlan_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 375

enum__sai_ip_addr_family_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 383

SAI_IP_ADDR_FAMILY_IPV4 = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 383

SAI_IP_ADDR_FAMILY_IPV6 = (SAI_IP_ADDR_FAMILY_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 383

sai_ip_addr_family_t = enum__sai_ip_addr_family_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 383

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 395
class union__sai_ip_addr_t(Union):
    pass

union__sai_ip_addr_t.__slots__ = [
    'ip4',
    'ip6',
]
union__sai_ip_addr_t._fields_ = [
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
]

sai_ip_addr_t = union__sai_ip_addr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 395

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 403
class struct__sai_ip_address_t(Structure):
    pass

struct__sai_ip_address_t.__slots__ = [
    'addr_family',
    'addr',
]
struct__sai_ip_address_t._fields_ = [
    ('addr_family', sai_ip_addr_family_t),
    ('addr', sai_ip_addr_t),
]

sai_ip_address_t = struct__sai_ip_address_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 403

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 409
class struct__sai_ip_address_list_t(Structure):
    pass

struct__sai_ip_address_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_ip_address_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_ip_address_t)),
]

sai_ip_address_list_t = struct__sai_ip_address_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 409

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 420
class struct__sai_ip_prefix_t(Structure):
    pass

struct__sai_ip_prefix_t.__slots__ = [
    'addr_family',
    'addr',
    'mask',
]
struct__sai_ip_prefix_t._fields_ = [
    ('addr_family', sai_ip_addr_family_t),
    ('addr', sai_ip_addr_t),
    ('mask', sai_ip_addr_t),
]

sai_ip_prefix_t = struct__sai_ip_prefix_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 420

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 458
class union__sai_acl_field_data_mask_t(Union):
    pass

union__sai_acl_field_data_mask_t.__slots__ = [
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'mac',
    'ip4',
    'ip6',
    'u8list',
]
union__sai_acl_field_data_mask_t._fields_ = [
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('u8list', sai_u8_list_t),
]

sai_acl_field_data_mask_t = union__sai_acl_field_data_mask_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 458

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 509
class union__sai_acl_field_data_data_t(Union):
    pass

union__sai_acl_field_data_data_t.__slots__ = [
    'booldata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'mac',
    'ip4',
    'ip6',
    'oid',
    'objlist',
    'u8list',
]
union__sai_acl_field_data_data_t._fields_ = [
    ('booldata', c_uint8),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('u8list', sai_u8_list_t),
]

sai_acl_field_data_data_t = union__sai_acl_field_data_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 509

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 544
class struct__sai_acl_field_data_t(Structure):
    pass

struct__sai_acl_field_data_t.__slots__ = [
    'enable',
    'mask',
    'data',
]
struct__sai_acl_field_data_t._fields_ = [
    ('enable', c_uint8),
    ('mask', sai_acl_field_data_mask_t),
    ('data', sai_acl_field_data_data_t),
]

sai_acl_field_data_t = struct__sai_acl_field_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 544

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 593
class union__sai_acl_action_parameter_t(Union):
    pass

union__sai_acl_action_parameter_t.__slots__ = [
    'booldata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'mac',
    'ip4',
    'ip6',
    'oid',
    'objlist',
    'ipaddr',
]
union__sai_acl_action_parameter_t._fields_ = [
    ('booldata', c_uint8),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('ipaddr', sai_ip_address_t),
]

sai_acl_action_parameter_t = union__sai_acl_action_parameter_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 593

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 617
class struct__sai_acl_action_data_t(Structure):
    pass

struct__sai_acl_action_data_t.__slots__ = [
    'enable',
    'parameter',
]
struct__sai_acl_action_data_t._fields_ = [
    ('enable', c_uint8),
    ('parameter', sai_acl_action_parameter_t),
]

sai_acl_action_data_t = struct__sai_acl_action_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 617

enum__sai_packet_color_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 639

SAI_PACKET_COLOR_GREEN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 639

SAI_PACKET_COLOR_YELLOW = (SAI_PACKET_COLOR_GREEN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 639

SAI_PACKET_COLOR_RED = (SAI_PACKET_COLOR_YELLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 639

sai_packet_color_t = enum__sai_packet_color_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 639

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 683
class struct__sai_qos_map_params_t(Structure):
    pass

struct__sai_qos_map_params_t.__slots__ = [
    'tc',
    'dscp',
    'dot1p',
    'prio',
    'pg',
    'queue_index',
    'color',
    'mpls_exp',
]
struct__sai_qos_map_params_t._fields_ = [
    ('tc', sai_cos_t),
    ('dscp', sai_uint8_t),
    ('dot1p', sai_uint8_t),
    ('prio', sai_uint8_t),
    ('pg', sai_uint8_t),
    ('queue_index', sai_queue_index_t),
    ('color', sai_packet_color_t),
    ('mpls_exp', sai_uint8_t),
]

sai_qos_map_params_t = struct__sai_qos_map_params_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 683

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 693
class struct__sai_qos_map_t(Structure):
    pass

struct__sai_qos_map_t.__slots__ = [
    'key',
    'value',
]
struct__sai_qos_map_t._fields_ = [
    ('key', sai_qos_map_params_t),
    ('value', sai_qos_map_params_t),
]

sai_qos_map_t = struct__sai_qos_map_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 693

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 703
class struct__sai_qos_map_list_t(Structure):
    pass

struct__sai_qos_map_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_qos_map_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_qos_map_t)),
]

sai_qos_map_list_t = struct__sai_qos_map_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 703

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 713
class struct__sai_map_t(Structure):
    pass

struct__sai_map_t.__slots__ = [
    'key',
    'value',
]
struct__sai_map_t._fields_ = [
    ('key', sai_uint32_t),
    ('value', sai_int32_t),
]

sai_map_t = struct__sai_map_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 713

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 723
class struct__sai_map_list_t(Structure):
    pass

struct__sai_map_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_map_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_map_t)),
]

sai_map_list_t = struct__sai_map_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 723

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 749
class struct__sai_acl_capability_t(Structure):
    pass

struct__sai_acl_capability_t.__slots__ = [
    'is_action_list_mandatory',
    'action_list',
]
struct__sai_acl_capability_t._fields_ = [
    ('is_action_list_mandatory', c_uint8),
    ('action_list', sai_s32_list_t),
]

sai_acl_capability_t = struct__sai_acl_capability_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 749

enum__sai_acl_stage_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 762

SAI_ACL_STAGE_INGRESS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 762

SAI_ACL_STAGE_EGRESS = (SAI_ACL_STAGE_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 762

sai_acl_stage_t = enum__sai_acl_stage_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 762

enum__sai_acl_bind_point_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_LAG = (SAI_ACL_BIND_POINT_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_VLAN = (SAI_ACL_BIND_POINT_TYPE_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE = (SAI_ACL_BIND_POINT_TYPE_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_ROUTER_INTF = SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

SAI_ACL_BIND_POINT_TYPE_SWITCH = (SAI_ACL_BIND_POINT_TYPE_ROUTER_INTF + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

sai_acl_bind_point_type_t = enum__sai_acl_bind_point_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 787

enum__sai_tam_bind_point_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_QUEUE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_PORT = (SAI_TAM_BIND_POINT_TYPE_QUEUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_LAG = (SAI_TAM_BIND_POINT_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_VLAN = (SAI_TAM_BIND_POINT_TYPE_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_SWITCH = (SAI_TAM_BIND_POINT_TYPE_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_IPG = (SAI_TAM_BIND_POINT_TYPE_SWITCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

SAI_TAM_BIND_POINT_TYPE_BSP = (SAI_TAM_BIND_POINT_TYPE_IPG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

sai_tam_bind_point_type_t = enum__sai_tam_bind_point_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 815

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 831
class struct__sai_acl_resource_t(Structure):
    pass

struct__sai_acl_resource_t.__slots__ = [
    'stage',
    'bind_point',
    'avail_num',
]
struct__sai_acl_resource_t._fields_ = [
    ('stage', sai_acl_stage_t),
    ('bind_point', sai_acl_bind_point_type_t),
    ('avail_num', sai_uint32_t),
]

sai_acl_resource_t = struct__sai_acl_resource_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 831

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 847
class struct__sai_acl_resource_list_t(Structure):
    pass

struct__sai_acl_resource_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_acl_resource_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_acl_resource_t)),
]

sai_acl_resource_list_t = struct__sai_acl_resource_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 847

enum__sai_tlv_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

SAI_TLV_TYPE_INGRESS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

SAI_TLV_TYPE_EGRESS = (SAI_TLV_TYPE_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

SAI_TLV_TYPE_OPAQUE = (SAI_TLV_TYPE_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

SAI_TLV_TYPE_HMAC = (SAI_TLV_TYPE_OPAQUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

sai_tlv_type_t = enum__sai_tlv_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 865

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 875
class struct__sai_hmac_t(Structure):
    pass

struct__sai_hmac_t.__slots__ = [
    'key_id',
    'hmac',
]
struct__sai_hmac_t._fields_ = [
    ('key_id', sai_uint32_t),
    ('hmac', sai_uint32_t * 8),
]

sai_hmac_t = struct__sai_hmac_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 875

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 893
class union__sai_tlv_entry_t(Union):
    pass

union__sai_tlv_entry_t.__slots__ = [
    'ingress_node',
    'egress_node',
    'opaque_container',
    'hmac',
]
union__sai_tlv_entry_t._fields_ = [
    ('ingress_node', sai_ip6_t),
    ('egress_node', sai_ip6_t),
    ('opaque_container', sai_uint32_t * 4),
    ('hmac', sai_hmac_t),
]

sai_tlv_entry_t = union__sai_tlv_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 893

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 904
class struct__sai_tlv_t(Structure):
    pass

struct__sai_tlv_t.__slots__ = [
    'tlv_type',
    'entry',
]
struct__sai_tlv_t._fields_ = [
    ('tlv_type', sai_tlv_type_t),
    ('entry', sai_tlv_entry_t),
]

sai_tlv_t = struct__sai_tlv_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 904

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 916
class struct__sai_tlv_list_t(Structure):
    pass

struct__sai_tlv_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_tlv_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_tlv_t)),
]

sai_tlv_list_t = struct__sai_tlv_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 916

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 928
class struct__sai_segment_list_t(Structure):
    pass

struct__sai_segment_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_segment_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_ip6_t)),
]

sai_segment_list_t = struct__sai_segment_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 928

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 941
class struct__sai_port_lane_eye_values_t(Structure):
    pass

struct__sai_port_lane_eye_values_t.__slots__ = [
    'lane',
    'left',
    'right',
    'up',
    'down',
]
struct__sai_port_lane_eye_values_t._fields_ = [
    ('lane', c_uint32),
    ('left', c_int32),
    ('right', c_int32),
    ('up', c_int32),
    ('down', c_int32),
]

sai_port_lane_eye_values_t = struct__sai_port_lane_eye_values_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 941

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 963
class struct__sai_port_eye_values_list_t(Structure):
    pass

struct__sai_port_eye_values_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_eye_values_list_t._fields_ = [
    ('count', c_uint32),
    ('list', POINTER(sai_port_lane_eye_values_t)),
]

sai_port_eye_values_list_t = struct__sai_port_eye_values_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 963

enum__sai_outseg_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 976

SAI_OUTSEG_TYPE_PUSH = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 976

SAI_OUTSEG_TYPE_SWAP = (SAI_OUTSEG_TYPE_PUSH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 976

sai_outseg_type_t = enum__sai_outseg_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 976

enum__sai_outseg_ttl_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 987

SAI_OUTSEG_TTL_MODE_UNIFORM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 987

SAI_OUTSEG_TTL_MODE_PIPE = (SAI_OUTSEG_TTL_MODE_UNIFORM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 987

sai_outseg_ttl_mode_t = enum__sai_outseg_ttl_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 987

enum__sai_outseg_exp_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 998

SAI_OUTSEG_EXP_MODE_UNIFORM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 998

SAI_OUTSEG_EXP_MODE_PIPE = (SAI_OUTSEG_EXP_MODE_UNIFORM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 998

sai_outseg_exp_mode_t = enum__sai_outseg_exp_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 998

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1148
class union__sai_attribute_value_t(Union):
    pass

union__sai_attribute_value_t.__slots__ = [
    'booldata',
    'chardata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'u64',
    's64',
    'ptr',
    'mac',
    'ip4',
    'ip6',
    'ipaddr',
    'ipprefix',
    'oid',
    'objlist',
    'boollist',
    'u8list',
    's8list',
    'u16list',
    's16list',
    'u32list',
    's32list',
    'u32range',
    's32range',
    'vlanlist',
    'qosmap',
    'maplist',
    'aclfield',
    'aclaction',
    'aclcapability',
    'aclresource',
    'tlvlist',
    'segmentlist',
    'ipaddrlist',
    'porteyevalues',
    'timespec',
    'captured_timespec',
    'timeoffset',
]
union__sai_attribute_value_t._fields_ = [
    ('booldata', c_uint8),
    ('chardata', c_char * 32),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('u64', sai_uint64_t),
    ('s64', sai_int64_t),
    ('ptr', sai_pointer_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('ipaddr', sai_ip_address_t),
    ('ipprefix', sai_ip_prefix_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('boollist', sai_bool_list_t),
    ('u8list', sai_u8_list_t),
    ('s8list', sai_s8_list_t),
    ('u16list', sai_u16_list_t),
    ('s16list', sai_s16_list_t),
    ('u32list', sai_u32_list_t),
    ('s32list', sai_s32_list_t),
    ('u32range', sai_u32_range_t),
    ('s32range', sai_s32_range_t),
    ('vlanlist', sai_vlan_list_t),
    ('qosmap', sai_qos_map_list_t),
    ('maplist', sai_map_list_t),
    ('aclfield', sai_acl_field_data_t),
    ('aclaction', sai_acl_action_data_t),
    ('aclcapability', sai_acl_capability_t),
    ('aclresource', sai_acl_resource_list_t),
    ('tlvlist', sai_tlv_list_t),
    ('segmentlist', sai_segment_list_t),
    ('ipaddrlist', sai_ip_address_list_t),
    ('porteyevalues', sai_port_eye_values_list_t),
    ('timespec', sai_timespec_t),
    ('captured_timespec', sai_captured_timespec_t),
    ('timeoffset', sai_timeoffset_t),
]

sai_attribute_value_t = union__sai_attribute_value_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1148

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1160
class struct__sai_attribute_t(Structure):
    pass

struct__sai_attribute_t.__slots__ = [
    'id',
    'value',
]
struct__sai_attribute_t._fields_ = [
    ('id', sai_attr_id_t),
    ('value', sai_attribute_value_t),
]

sai_attribute_t = struct__sai_attribute_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1160

enum__sai_bulk_op_error_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1175

SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1175

SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR = (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1175

sai_bulk_op_error_mode_t = enum__sai_bulk_op_error_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1175

sai_bulk_object_create_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_object_id_t), POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1194

sai_bulk_object_remove_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_object_id_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1215

enum__sai_stats_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1232

SAI_STATS_MODE_READ = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1232

SAI_STATS_MODE_READ_AND_CLEAR = (SAI_STATS_MODE_READ + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1232

sai_stats_mode_t = enum__sai_stats_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1232

enum__sai_acl_ip_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ANY = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IP = (SAI_ACL_IP_TYPE_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IP = (SAI_ACL_IP_TYPE_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IPV4ANY = (SAI_ACL_IP_TYPE_NON_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IPV4 = (SAI_ACL_IP_TYPE_IPV4ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IPV6ANY = (SAI_ACL_IP_TYPE_NON_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IPV6 = (SAI_ACL_IP_TYPE_IPV6ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP = (SAI_ACL_IP_TYPE_NON_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP_REQUEST = (SAI_ACL_IP_TYPE_ARP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP_REPLY = (SAI_ACL_IP_TYPE_ARP_REQUEST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

sai_acl_ip_type_t = enum__sai_acl_ip_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 71

enum__sai_acl_ip_frag_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_ANY = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_FRAG = (SAI_ACL_IP_FRAG_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD = (SAI_ACL_IP_FRAG_NON_FRAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_HEAD = (SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_HEAD = (SAI_ACL_IP_FRAG_HEAD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

sai_acl_ip_frag_t = enum__sai_acl_ip_frag_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 93

enum__sai_acl_dtel_flow_op_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_NOP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_INT = (SAI_ACL_DTEL_FLOW_OP_NOP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_IOAM = (SAI_ACL_DTEL_FLOW_OP_INT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_POSTCARD = (SAI_ACL_DTEL_FLOW_OP_IOAM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

sai_acl_dtel_flow_op_t = enum__sai_acl_dtel_flow_op_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 114

enum__sai_acl_action_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_REDIRECT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_ENDPOINT_IP = (SAI_ACL_ACTION_TYPE_REDIRECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_REDIRECT_LIST = (SAI_ACL_ACTION_TYPE_ENDPOINT_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_PACKET_ACTION = (SAI_ACL_ACTION_TYPE_REDIRECT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_FLOOD = (SAI_ACL_ACTION_TYPE_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_COUNTER = (SAI_ACL_ACTION_TYPE_FLOOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_MIRROR_INGRESS = (SAI_ACL_ACTION_TYPE_COUNTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_MIRROR_EGRESS = (SAI_ACL_ACTION_TYPE_MIRROR_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_POLICER = (SAI_ACL_ACTION_TYPE_MIRROR_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DECREMENT_TTL = (SAI_ACL_ACTION_TYPE_SET_POLICER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_TC = (SAI_ACL_ACTION_TYPE_DECREMENT_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR = (SAI_ACL_ACTION_TYPE_SET_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID = (SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI = (SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID = (SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI = (SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_SRC_MAC = (SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_DST_MAC = (SAI_ACL_ACTION_TYPE_SET_SRC_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_SRC_IP = (SAI_ACL_ACTION_TYPE_SET_DST_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_DST_IP = (SAI_ACL_ACTION_TYPE_SET_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_SRC_IPV6 = (SAI_ACL_ACTION_TYPE_SET_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_DST_IPV6 = (SAI_ACL_ACTION_TYPE_SET_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_DSCP = (SAI_ACL_ACTION_TYPE_SET_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_ECN = (SAI_ACL_ACTION_TYPE_SET_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_L4_SRC_PORT = (SAI_ACL_ACTION_TYPE_SET_ECN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_L4_DST_PORT = (SAI_ACL_ACTION_TYPE_SET_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ACTION_TYPE_SET_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_EGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA = (SAI_ACL_ACTION_TYPE_EGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_EGRESS_BLOCK_PORT_LIST = (SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID = (SAI_ACL_ACTION_TYPE_EGRESS_BLOCK_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN = (SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_ACL_DTEL_FLOW_OP = (SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DTEL_INT_SESSION = (SAI_ACL_ACTION_TYPE_ACL_DTEL_FLOW_OP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DTEL_DROP_REPORT_ENABLE = (SAI_ACL_ACTION_TYPE_DTEL_INT_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DTEL_TAIL_DROP_REPORT_ENABLE = (SAI_ACL_ACTION_TYPE_DTEL_DROP_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DTEL_FLOW_SAMPLE_PERCENT = (SAI_ACL_ACTION_TYPE_DTEL_TAIL_DROP_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_DTEL_REPORT_ALL_PACKETS = (SAI_ACL_ACTION_TYPE_DTEL_FLOW_SAMPLE_PERCENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_NO_NAT = (SAI_ACL_ACTION_TYPE_DTEL_REPORT_ALL_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INT_INSERT = (SAI_ACL_ACTION_TYPE_NO_NAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INT_DELETE = (SAI_ACL_ACTION_TYPE_INT_INSERT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INT_REPORT_FLOW = (SAI_ACL_ACTION_TYPE_INT_DELETE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INT_REPORT_DROPS = (SAI_ACL_ACTION_TYPE_INT_REPORT_FLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_INT_REPORT_TAIL_DROPS = (SAI_ACL_ACTION_TYPE_INT_REPORT_DROPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_TAM_INT_OBJECT = (SAI_ACL_ACTION_TYPE_INT_REPORT_TAIL_DROPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_SET_ISOLATION_GROUP = (SAI_ACL_ACTION_TYPE_TAM_INT_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

SAI_ACL_ACTION_TYPE_MACSEC_FLOW = (SAI_ACL_ACTION_TYPE_SET_ISOLATION_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

sai_acl_action_type_t = enum__sai_acl_action_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 262

enum__sai_acl_table_group_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 275

SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 275

SAI_ACL_TABLE_GROUP_TYPE_PARALLEL = (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 275

sai_acl_table_group_type_t = enum__sai_acl_table_group_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 275

enum__sai_acl_table_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE = SAI_ACL_TABLE_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST = (SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_TYPE = (SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST = (SAI_ACL_TABLE_GROUP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_END = (SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

sai_acl_table_group_attr_t = enum__sai_acl_table_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 353

enum__sai_acl_table_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID = SAI_ACL_TABLE_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_END = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

sai_acl_table_group_member_attr_t = enum__sai_acl_table_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 423

enum__sai_acl_table_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_ACL_STAGE = SAI_ACL_TABLE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST = (SAI_ACL_TABLE_ATTR_ACL_STAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_SIZE = (SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST = (SAI_ACL_TABLE_ATTR_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_START = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6 = SAI_ACL_TABLE_ATTR_FIELD_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC = (SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_DST_MAC = (SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_MAC = (SAI_ACL_TABLE_ATTR_FIELD_DST_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_MAC = (SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_SRC_IP = (SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_DST_IP = (SAI_ACL_TABLE_ATTR_FIELD_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IP = (SAI_ACL_TABLE_ATTR_FIELD_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IP = (SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS = (SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS = (SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IN_PORT = (SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT = (SAI_ACL_TABLE_ATTR_FIELD_IN_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID = (SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI = (SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI = (SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID = (SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI = (SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI = (SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT = (SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_DST_PORT = (SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_ETHER_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL = (SAI_ACL_TABLE_ATTR_FIELD_INNER_ETHER_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_INNER_IP_PROTOCOL = (SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IP_IDENTIFICATION = (SAI_ACL_TABLE_ATTR_FIELD_INNER_IP_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_DSCP = (SAI_ACL_TABLE_ATTR_FIELD_IP_IDENTIFICATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ECN = (SAI_ACL_TABLE_ATTR_FIELD_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TTL = (SAI_ACL_TABLE_ATTR_FIELD_ECN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TOS = (SAI_ACL_TABLE_ATTR_FIELD_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS = (SAI_ACL_TABLE_ATTR_FIELD_TOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS = (SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG = (SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TC = (SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE = (SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE = (SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN = (SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TUNNEL_VNI = (SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG = (SAI_ACL_TABLE_ATTR_FIELD_TUNNEL_VNI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI = (SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_FDB_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_FDB_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ROUTE_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_BTH_OPCODE = (SAI_ACL_TABLE_ATTR_FIELD_ROUTE_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_AETH_SYNDROME = (SAI_ACL_TABLE_ATTR_FIELD_BTH_OPCODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN = (SAI_ACL_TABLE_ATTR_FIELD_AETH_SYNDROME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MAX = (SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN + 255) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE = (SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MAX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER = (SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_TAM_INT_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_FIELD_END = SAI_ACL_TABLE_ATTR_FIELD_TAM_INT_TYPE # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_ENTRY_LIST = (SAI_ACL_TABLE_ATTR_FIELD_END + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY = (SAI_ACL_TABLE_ATTR_ENTRY_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER = (SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_END = (SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

sai_acl_table_attr_t = enum__sai_acl_table_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 1346

enum__sai_acl_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_TABLE_ID = SAI_ACL_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_PRIORITY = (SAI_ACL_ENTRY_ATTR_TABLE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ADMIN_STATE = (SAI_ACL_ENTRY_ATTR_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_START = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6 = SAI_ACL_ENTRY_ATTR_FIELD_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP = (SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_DST_IP = (SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP = (SAI_ACL_ENTRY_ATTR_FIELD_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS = (SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI = (SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_ETHER_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_ETHER_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_INNER_IP_PROTOCOL = (SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION = (SAI_ACL_ENTRY_ATTR_FIELD_INNER_IP_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_DSCP = (SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ECN = (SAI_ACL_ENTRY_ATTR_FIELD_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_ECN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TOS = (SAI_ACL_ENTRY_ATTR_FIELD_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS = (SAI_ACL_ENTRY_ATTR_FIELD_TOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS = (SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG = (SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TC = (SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE = (SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE = (SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN = (SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TUNNEL_VNI = (SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG = (SAI_ACL_ENTRY_ATTR_FIELD_TUNNEL_VNI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI = (SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE = (SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME = (SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN = (SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MAX = (SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN + 255) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE = (SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MAX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER = (SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_TAM_INT_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_FIELD_END = SAI_ACL_ENTRY_ATTR_FIELD_TAM_INT_TYPE # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_START = 8192 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT = SAI_ACL_ENTRY_ATTR_ACTION_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_ENDPOINT_IP = (SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST = (SAI_ACL_ENTRY_ATTR_ACTION_ENDPOINT_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION = (SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_FLOOD = (SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_COUNTER = (SAI_ACL_ENTRY_ATTR_ACTION_FLOOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS = (SAI_ACL_ENTRY_ATTR_ACTION_COUNTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS = (SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER = (SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL = (SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_TC = (SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR = (SAI_ACL_ENTRY_ATTR_ACTION_SET_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC = (SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC = (SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP = (SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP = (SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6 = (SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP = (SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN = (SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA = (SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST = (SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID = (SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN = (SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_ACL_DTEL_FLOW_OP = (SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_INT_SESSION = (SAI_ACL_ENTRY_ATTR_ACTION_ACL_DTEL_FLOW_OP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_DROP_REPORT_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_DTEL_INT_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_TAIL_DROP_REPORT_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_DTEL_DROP_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_FLOW_SAMPLE_PERCENT = (SAI_ACL_ENTRY_ATTR_ACTION_DTEL_TAIL_DROP_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_REPORT_ALL_PACKETS = (SAI_ACL_ENTRY_ATTR_ACTION_DTEL_FLOW_SAMPLE_PERCENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_NO_NAT = (SAI_ACL_ENTRY_ATTR_ACTION_DTEL_REPORT_ALL_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INT_INSERT = (SAI_ACL_ENTRY_ATTR_ACTION_NO_NAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INT_DELETE = (SAI_ACL_ENTRY_ATTR_ACTION_INT_INSERT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_FLOW = (SAI_ACL_ENTRY_ATTR_ACTION_INT_DELETE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_DROPS = (SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_FLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_TAIL_DROPS = (SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_DROPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_TAM_INT_OBJECT = (SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_TAIL_DROPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_SET_ISOLATION_GROUP = (SAI_ACL_ENTRY_ATTR_ACTION_TAM_INT_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_MACSEC_FLOW = (SAI_ACL_ENTRY_ATTR_ACTION_SET_ISOLATION_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_ACTION_END = SAI_ACL_ENTRY_ATTR_ACTION_MACSEC_FLOW # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_END = (SAI_ACL_ENTRY_ATTR_ACTION_END + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

sai_acl_entry_attr_t = enum__sai_acl_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2726

enum__sai_acl_counter_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_TABLE_ID = SAI_ACL_COUNTER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT = (SAI_ACL_COUNTER_ATTR_TABLE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT = (SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_PACKETS = (SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_BYTES = (SAI_ACL_COUNTER_ATTR_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_END = (SAI_ACL_COUNTER_ATTR_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

sai_acl_counter_attr_t = enum__sai_acl_counter_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2802

enum__sai_acl_range_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE = (SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

SAI_ACL_RANGE_TYPE_OUTER_VLAN = (SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

SAI_ACL_RANGE_TYPE_INNER_VLAN = (SAI_ACL_RANGE_TYPE_OUTER_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

SAI_ACL_RANGE_TYPE_PACKET_LENGTH = (SAI_ACL_RANGE_TYPE_INNER_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

sai_acl_range_type_t = enum__sai_acl_range_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2824

enum__sai_acl_range_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_TYPE = SAI_ACL_RANGE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_LIMIT = (SAI_ACL_RANGE_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_END = (SAI_ACL_RANGE_ATTR_LIMIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_STAGE = SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_END = (SAI_ACL_RANGE_ATTR_STAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

sai_acl_range_attr_t = enum__sai_acl_range_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2878

sai_create_acl_table_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2890

sai_remove_acl_table_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2903

sai_set_acl_table_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2914

sai_get_acl_table_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2927

sai_create_acl_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2942

sai_remove_acl_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2955

sai_set_acl_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2966

sai_get_acl_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2979

sai_create_acl_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 2994

sai_remove_acl_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3007

sai_set_acl_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3018

sai_get_acl_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3031

sai_create_acl_range_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3046

sai_remove_acl_range_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3059

sai_set_acl_range_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3070

sai_get_acl_range_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3083

sai_create_acl_table_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3098

sai_remove_acl_table_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3111

sai_set_acl_table_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3122

sai_get_acl_table_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3135

sai_create_acl_table_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3150

sai_remove_acl_table_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3163

sai_set_acl_table_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3174

sai_get_acl_table_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3187

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3221
class struct__sai_acl_api_t(Structure):
    pass

struct__sai_acl_api_t.__slots__ = [
    'create_acl_table',
    'remove_acl_table',
    'set_acl_table_attribute',
    'get_acl_table_attribute',
    'create_acl_entry',
    'remove_acl_entry',
    'set_acl_entry_attribute',
    'get_acl_entry_attribute',
    'create_acl_counter',
    'remove_acl_counter',
    'set_acl_counter_attribute',
    'get_acl_counter_attribute',
    'create_acl_range',
    'remove_acl_range',
    'set_acl_range_attribute',
    'get_acl_range_attribute',
    'create_acl_table_group',
    'remove_acl_table_group',
    'set_acl_table_group_attribute',
    'get_acl_table_group_attribute',
    'create_acl_table_group_member',
    'remove_acl_table_group_member',
    'set_acl_table_group_member_attribute',
    'get_acl_table_group_member_attribute',
]
struct__sai_acl_api_t._fields_ = [
    ('create_acl_table', sai_create_acl_table_fn),
    ('remove_acl_table', sai_remove_acl_table_fn),
    ('set_acl_table_attribute', sai_set_acl_table_attribute_fn),
    ('get_acl_table_attribute', sai_get_acl_table_attribute_fn),
    ('create_acl_entry', sai_create_acl_entry_fn),
    ('remove_acl_entry', sai_remove_acl_entry_fn),
    ('set_acl_entry_attribute', sai_set_acl_entry_attribute_fn),
    ('get_acl_entry_attribute', sai_get_acl_entry_attribute_fn),
    ('create_acl_counter', sai_create_acl_counter_fn),
    ('remove_acl_counter', sai_remove_acl_counter_fn),
    ('set_acl_counter_attribute', sai_set_acl_counter_attribute_fn),
    ('get_acl_counter_attribute', sai_get_acl_counter_attribute_fn),
    ('create_acl_range', sai_create_acl_range_fn),
    ('remove_acl_range', sai_remove_acl_range_fn),
    ('set_acl_range_attribute', sai_set_acl_range_attribute_fn),
    ('get_acl_range_attribute', sai_get_acl_range_attribute_fn),
    ('create_acl_table_group', sai_create_acl_table_group_fn),
    ('remove_acl_table_group', sai_remove_acl_table_group_fn),
    ('set_acl_table_group_attribute', sai_set_acl_table_group_attribute_fn),
    ('get_acl_table_group_attribute', sai_get_acl_table_group_attribute_fn),
    ('create_acl_table_group_member', sai_create_acl_table_group_member_fn),
    ('remove_acl_table_group_member', sai_remove_acl_table_group_member_fn),
    ('set_acl_table_group_member_attribute', sai_set_acl_table_group_member_attribute_fn),
    ('get_acl_table_group_member_attribute', sai_get_acl_table_group_member_attribute_fn),
]

sai_acl_api_t = struct__sai_acl_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3221

enum__sai_bfd_session_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

SAI_BFD_SESSION_TYPE_DEMAND_ACTIVE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

SAI_BFD_SESSION_TYPE_DEMAND_PASSIVE = (SAI_BFD_SESSION_TYPE_DEMAND_ACTIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE = (SAI_BFD_SESSION_TYPE_DEMAND_PASSIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

SAI_BFD_SESSION_TYPE_ASYNC_PASSIVE = (SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

sai_bfd_session_type_t = enum__sai_bfd_session_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 54

enum__sai_bfd_session_offload_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 70

SAI_BFD_SESSION_OFFLOAD_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 70

SAI_BFD_SESSION_OFFLOAD_TYPE_FULL = (SAI_BFD_SESSION_OFFLOAD_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 70

SAI_BFD_SESSION_OFFLOAD_TYPE_SUSTENANCE = (SAI_BFD_SESSION_OFFLOAD_TYPE_FULL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 70

sai_bfd_session_offload_type_t = enum__sai_bfd_session_offload_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 70

enum__sai_bfd_encapsulation_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL = (SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

SAI_BFD_ENCAPSULATION_TYPE_MPLS = (SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

SAI_BFD_ENCAPSULATION_TYPE_NONE = (SAI_BFD_ENCAPSULATION_TYPE_MPLS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

sai_bfd_encapsulation_type_t = enum__sai_bfd_encapsulation_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 97

enum__sai_bfd_mpls_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 110

SAI_BFD_MPLS_TYPE_NORMAL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 110

SAI_BFD_MPLS_TYPE_TP = (SAI_BFD_MPLS_TYPE_NORMAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 110

sai_bfd_mpls_type_t = enum__sai_bfd_mpls_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 110

enum__sai_bfd_session_state_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

SAI_BFD_SESSION_STATE_ADMIN_DOWN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

SAI_BFD_SESSION_STATE_DOWN = (SAI_BFD_SESSION_STATE_ADMIN_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

SAI_BFD_SESSION_STATE_INIT = (SAI_BFD_SESSION_STATE_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

SAI_BFD_SESSION_STATE_UP = (SAI_BFD_SESSION_STATE_INIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

sai_bfd_session_state_t = enum__sai_bfd_session_state_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 129

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 146
class struct__sai_bfd_session_state_notification_t(Structure):
    pass

struct__sai_bfd_session_state_notification_t.__slots__ = [
    'bfd_session_id',
    'session_state',
]
struct__sai_bfd_session_state_notification_t._fields_ = [
    ('bfd_session_id', sai_object_id_t),
    ('session_state', sai_bfd_session_state_t),
]

sai_bfd_session_state_notification_t = struct__sai_bfd_session_state_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 146

enum__sai_bfd_ach_channel_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4 = (SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6 = (SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

SAI_BFD_ACH_CHANNEL_TYPE_TP = (SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

sai_bfd_ach_channel_type_t = enum__sai_bfd_ach_channel_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 165

enum__sai_bfd_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TYPE = SAI_BFD_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID = (SAI_BFD_SESSION_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER = (SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_PORT = (SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR = (SAI_BFD_SESSION_ATTR_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR = (SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_UDP_SRC_PORT = (SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TC = (SAI_BFD_SESSION_ATTR_UDP_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VLAN_TPID = (SAI_BFD_SESSION_ATTR_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VLAN_ID = (SAI_BFD_SESSION_ATTR_VLAN_TPID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VLAN_PRI = (SAI_BFD_SESSION_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VLAN_CFI = (SAI_BFD_SESSION_ATTR_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID = (SAI_BFD_SESSION_ATTR_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE = (SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_IPHDR_VERSION = (SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TOS = (SAI_BFD_SESSION_ATTR_IPHDR_VERSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TTL = (SAI_BFD_SESSION_ATTR_TOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TUNNEL_TOS = (SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TUNNEL_TTL = (SAI_BFD_SESSION_ATTR_TUNNEL_TOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS = (SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_ECHO_ENABLE = (SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MULTIHOP = (SAI_BFD_SESSION_ATTR_ECHO_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_CBIT = (SAI_BFD_SESSION_ATTR_MULTIHOP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MIN_TX = (SAI_BFD_SESSION_ATTR_CBIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MIN_RX = (SAI_BFD_SESSION_ATTR_MIN_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MULTIPLIER = (SAI_BFD_SESSION_ATTR_MIN_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX = (SAI_BFD_SESSION_ATTR_MULTIPLIER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX = (SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_STATE = (SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE = (SAI_BFD_SESSION_ATTR_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_NEGOTIATED_TX = (SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_NEGOTIATED_RX = (SAI_BFD_SESSION_ATTR_NEGOTIATED_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_LOCAL_DIAG = (SAI_BFD_SESSION_ATTR_NEGOTIATED_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_REMOTE_DIAG = (SAI_BFD_SESSION_ATTR_LOCAL_DIAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER = (SAI_BFD_SESSION_ATTR_REMOTE_DIAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE = (SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID = (SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE = (SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL = (SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MPLS_TTL = (SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_MPLS_EXP = (SAI_BFD_SESSION_ATTR_MPLS_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TP_CV_ENABLE = (SAI_BFD_SESSION_ATTR_MPLS_EXP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID = (SAI_BFD_SESSION_ATTR_TP_CV_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID = (SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL = (SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_NEXT_HOP_ID = (SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_END = (SAI_BFD_SESSION_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

sai_bfd_session_attr_t = enum__sai_bfd_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 640

enum__sai_bfd_session_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 656

SAI_BFD_SESSION_STAT_IN_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 656

SAI_BFD_SESSION_STAT_OUT_PACKETS = (SAI_BFD_SESSION_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 656

SAI_BFD_SESSION_STAT_DROP_PACKETS = (SAI_BFD_SESSION_STAT_OUT_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 656

sai_bfd_session_stat_t = enum__sai_bfd_session_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 656

sai_create_bfd_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 669

sai_remove_bfd_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 683

sai_set_bfd_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 695

sai_get_bfd_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 709

sai_get_bfd_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 724

sai_get_bfd_session_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 741

sai_clear_bfd_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 757

sai_bfd_session_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_bfd_session_state_notification_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 772

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 789
class struct__sai_bfd_api_t(Structure):
    pass

struct__sai_bfd_api_t.__slots__ = [
    'create_bfd_session',
    'remove_bfd_session',
    'set_bfd_session_attribute',
    'get_bfd_session_attribute',
    'get_bfd_session_stats',
    'get_bfd_session_stats_ext',
    'clear_bfd_session_stats',
]
struct__sai_bfd_api_t._fields_ = [
    ('create_bfd_session', sai_create_bfd_session_fn),
    ('remove_bfd_session', sai_remove_bfd_session_fn),
    ('set_bfd_session_attribute', sai_set_bfd_session_attribute_fn),
    ('get_bfd_session_attribute', sai_get_bfd_session_attribute_fn),
    ('get_bfd_session_stats', sai_get_bfd_session_stats_fn),
    ('get_bfd_session_stats_ext', sai_get_bfd_session_stats_ext_fn),
    ('clear_bfd_session_stats', sai_clear_bfd_session_stats_fn),
]

sai_bfd_api_t = struct__sai_bfd_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 789

enum__sai_bridge_port_fdb_learning_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DROP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_TRAP = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_LOG = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_TRAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_FDB_NOTIFICATION = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_LOG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

sai_bridge_port_fdb_learning_mode_t = enum__sai_bridge_port_fdb_learning_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 66

enum__sai_bridge_port_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_SUB_PORT = (SAI_BRIDGE_PORT_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_1Q_ROUTER = (SAI_BRIDGE_PORT_TYPE_SUB_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_1D_ROUTER = (SAI_BRIDGE_PORT_TYPE_1Q_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_TUNNEL = (SAI_BRIDGE_PORT_TYPE_1D_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

SAI_BRIDGE_PORT_TYPE_FRR = (SAI_BRIDGE_PORT_TYPE_TUNNEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

sai_bridge_port_type_t = enum__sai_bridge_port_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 91

enum__sai_bridge_port_tagging_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 104

SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 104

SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED = (SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 104

sai_bridge_port_tagging_mode_t = enum__sai_bridge_port_tagging_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 104

enum__sai_bridge_port_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_TYPE = SAI_BRIDGE_PORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_PORT_ID = (SAI_BRIDGE_PORT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = (SAI_BRIDGE_PORT_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_VLAN_ID = (SAI_BRIDGE_PORT_ATTR_TAGGING_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_RIF_ID = (SAI_BRIDGE_PORT_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_TUNNEL_ID = (SAI_BRIDGE_PORT_ATTR_RIF_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = (SAI_BRIDGE_PORT_ATTR_TUNNEL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE = (SAI_BRIDGE_PORT_ATTR_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES = (SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION = (SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = (SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = (SAI_BRIDGE_PORT_ATTR_ADMIN_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = (SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP = (SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT = (SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE = (SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_FRR_NHP_GRP = (SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = (SAI_BRIDGE_PORT_ATTR_FRR_NHP_GRP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID = (SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_END = (SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_END = (SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

sai_bridge_port_attr_t = enum__sai_bridge_port_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 343

enum__sai_bridge_port_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

SAI_BRIDGE_PORT_STAT_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

SAI_BRIDGE_PORT_STAT_IN_PACKETS = (SAI_BRIDGE_PORT_STAT_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

SAI_BRIDGE_PORT_STAT_OUT_OCTETS = (SAI_BRIDGE_PORT_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

SAI_BRIDGE_PORT_STAT_OUT_PACKETS = (SAI_BRIDGE_PORT_STAT_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

sai_bridge_port_stat_t = enum__sai_bridge_port_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 362

sai_create_bridge_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 374

sai_remove_bridge_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 387

sai_set_bridge_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 398

sai_get_bridge_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 411

sai_get_bridge_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 426

sai_get_bridge_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 443

sai_clear_bridge_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 459

enum__sai_bridge_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 478

SAI_BRIDGE_TYPE_1Q = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 478

SAI_BRIDGE_TYPE_1D = (SAI_BRIDGE_TYPE_1Q + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 478

SAI_BRIDGE_TYPE_CROSS_CONNECT = (SAI_BRIDGE_TYPE_1D + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 478

sai_bridge_type_t = enum__sai_bridge_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 478

enum__sai_bridge_flood_control_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

SAI_BRIDGE_FLOOD_CONTROL_TYPE_COMBINED = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

sai_bridge_flood_control_type_t = enum__sai_bridge_flood_control_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 509

enum__sai_bridge_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_TYPE = SAI_BRIDGE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_PORT_LIST = (SAI_BRIDGE_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = (SAI_BRIDGE_ATTR_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_LEARN_DISABLE = (SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_LEARN_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_END = (SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

SAI_BRIDGE_ATTR_CUSTOM_RANGE_END = (SAI_BRIDGE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

sai_bridge_attr_t = enum__sai_bridge_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 662

enum__sai_bridge_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

SAI_BRIDGE_STAT_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

SAI_BRIDGE_STAT_IN_PACKETS = (SAI_BRIDGE_STAT_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

SAI_BRIDGE_STAT_OUT_OCTETS = (SAI_BRIDGE_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

SAI_BRIDGE_STAT_OUT_PACKETS = (SAI_BRIDGE_STAT_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

sai_bridge_stat_t = enum__sai_bridge_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 681

sai_create_bridge_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 693

sai_remove_bridge_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 706

sai_set_bridge_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 717

sai_get_bridge_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 730

sai_get_bridge_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 745

sai_get_bridge_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 762

sai_clear_bridge_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 778

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 802
class struct__sai_bridge_api_t(Structure):
    pass

struct__sai_bridge_api_t.__slots__ = [
    'create_bridge',
    'remove_bridge',
    'set_bridge_attribute',
    'get_bridge_attribute',
    'get_bridge_stats',
    'get_bridge_stats_ext',
    'clear_bridge_stats',
    'create_bridge_port',
    'remove_bridge_port',
    'set_bridge_port_attribute',
    'get_bridge_port_attribute',
    'get_bridge_port_stats',
    'get_bridge_port_stats_ext',
    'clear_bridge_port_stats',
]
struct__sai_bridge_api_t._fields_ = [
    ('create_bridge', sai_create_bridge_fn),
    ('remove_bridge', sai_remove_bridge_fn),
    ('set_bridge_attribute', sai_set_bridge_attribute_fn),
    ('get_bridge_attribute', sai_get_bridge_attribute_fn),
    ('get_bridge_stats', sai_get_bridge_stats_fn),
    ('get_bridge_stats_ext', sai_get_bridge_stats_ext_fn),
    ('clear_bridge_stats', sai_clear_bridge_stats_fn),
    ('create_bridge_port', sai_create_bridge_port_fn),
    ('remove_bridge_port', sai_remove_bridge_port_fn),
    ('set_bridge_port_attribute', sai_set_bridge_port_attribute_fn),
    ('get_bridge_port_attribute', sai_get_bridge_port_attribute_fn),
    ('get_bridge_port_stats', sai_get_bridge_port_stats_fn),
    ('get_bridge_port_stats_ext', sai_get_bridge_port_stats_ext_fn),
    ('clear_bridge_port_stats', sai_clear_bridge_port_stats_fn),
]

sai_bridge_api_t = struct__sai_bridge_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 802

enum__sai_ingress_priority_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE = SAI_INGRESS_PRIORITY_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT = (SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_TAM = (SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX = (SAI_INGRESS_PRIORITY_GROUP_ATTR_TAM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_END = (SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

sai_ingress_priority_group_attr_t = enum__sai_ingress_priority_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 97

enum__sai_ingress_priority_group_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_CURR_OCCUPANCY_BYTES = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_WATERMARK_BYTES = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_CURR_OCCUPANCY_BYTES = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_WATERMARK_BYTES = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_CURR_OCCUPANCY_BYTES = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_WATERMARK_BYTES = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

sai_ingress_priority_group_stat_t = enum__sai_ingress_priority_group_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 134

sai_create_ingress_priority_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 146

sai_remove_ingress_priority_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 159

sai_set_ingress_priority_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 170

sai_get_ingress_priority_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 183

sai_get_ingress_priority_group_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 198

sai_get_ingress_priority_group_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 215

sai_clear_ingress_priority_group_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 231

enum__sai_buffer_pool_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_INGRESS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_EGRESS = (SAI_BUFFER_POOL_TYPE_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_BOTH = (SAI_BUFFER_POOL_TYPE_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 250

sai_buffer_pool_type_t = enum__sai_buffer_pool_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 250

enum__sai_buffer_pool_threshold_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 263

SAI_BUFFER_POOL_THRESHOLD_MODE_STATIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 263

SAI_BUFFER_POOL_THRESHOLD_MODE_DYNAMIC = (SAI_BUFFER_POOL_THRESHOLD_MODE_STATIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 263

sai_buffer_pool_threshold_mode_t = enum__sai_buffer_pool_threshold_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 263

enum__sai_buffer_pool_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_SHARED_SIZE = SAI_BUFFER_POOL_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_TYPE = (SAI_BUFFER_POOL_ATTR_SHARED_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_SIZE = (SAI_BUFFER_POOL_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE = (SAI_BUFFER_POOL_ATTR_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_TAM = (SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_XOFF_SIZE = (SAI_BUFFER_POOL_ATTR_TAM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_WRED_PROFILE_ID = (SAI_BUFFER_POOL_ATTR_XOFF_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_END = (SAI_BUFFER_POOL_ATTR_WRED_PROFILE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_END = (SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

sai_buffer_pool_attr_t = enum__sai_buffer_pool_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 361

enum__sai_buffer_pool_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_CURR_OCCUPANCY_BYTES = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WATERMARK_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_DROPPED_PACKETS = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_PACKETS = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_BYTES = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_BYTES = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_PACKETS = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_BYTES = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_DROPPED_PACKETS = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_DROPPED_BYTES = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_BYTES = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_PACKETS = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_BYTES = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_XOFF_ROOM_CURR_OCCUPANCY_BYTES = 19 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_XOFF_ROOM_WATERMARK_BYTES = 20 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

sai_buffer_pool_stat_t = enum__sai_buffer_pool_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 434

sai_create_buffer_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 446

sai_remove_buffer_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 459

sai_set_buffer_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 470

sai_get_buffer_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 483

sai_get_buffer_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 498

sai_get_buffer_pool_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 515

sai_clear_buffer_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 531

enum__sai_buffer_profile_threshold_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 547

SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 547

SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC = (SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 547

sai_buffer_profile_threshold_mode_t = enum__sai_buffer_profile_threshold_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 547

enum__sai_buffer_profile_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_POOL_ID = SAI_BUFFER_PROFILE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE = (SAI_BUFFER_PROFILE_ATTR_POOL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE = SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE = (SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH = (SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH = (SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XOFF_TH = (SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XON_TH = (SAI_BUFFER_PROFILE_ATTR_XOFF_TH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH = (SAI_BUFFER_PROFILE_ATTR_XON_TH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_END = (SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_END = (SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

sai_buffer_profile_attr_t = enum__sai_buffer_profile_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 681

sai_create_buffer_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 693

sai_remove_buffer_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 706

sai_set_buffer_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 717

sai_get_buffer_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 730

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 758
class struct__sai_buffer_api_t(Structure):
    pass

struct__sai_buffer_api_t.__slots__ = [
    'create_buffer_pool',
    'remove_buffer_pool',
    'set_buffer_pool_attribute',
    'get_buffer_pool_attribute',
    'get_buffer_pool_stats',
    'get_buffer_pool_stats_ext',
    'clear_buffer_pool_stats',
    'create_ingress_priority_group',
    'remove_ingress_priority_group',
    'set_ingress_priority_group_attribute',
    'get_ingress_priority_group_attribute',
    'get_ingress_priority_group_stats',
    'get_ingress_priority_group_stats_ext',
    'clear_ingress_priority_group_stats',
    'create_buffer_profile',
    'remove_buffer_profile',
    'set_buffer_profile_attribute',
    'get_buffer_profile_attribute',
]
struct__sai_buffer_api_t._fields_ = [
    ('create_buffer_pool', sai_create_buffer_pool_fn),
    ('remove_buffer_pool', sai_remove_buffer_pool_fn),
    ('set_buffer_pool_attribute', sai_set_buffer_pool_attribute_fn),
    ('get_buffer_pool_attribute', sai_get_buffer_pool_attribute_fn),
    ('get_buffer_pool_stats', sai_get_buffer_pool_stats_fn),
    ('get_buffer_pool_stats_ext', sai_get_buffer_pool_stats_ext_fn),
    ('clear_buffer_pool_stats', sai_clear_buffer_pool_stats_fn),
    ('create_ingress_priority_group', sai_create_ingress_priority_group_fn),
    ('remove_ingress_priority_group', sai_remove_ingress_priority_group_fn),
    ('set_ingress_priority_group_attribute', sai_set_ingress_priority_group_attribute_fn),
    ('get_ingress_priority_group_attribute', sai_get_ingress_priority_group_attribute_fn),
    ('get_ingress_priority_group_stats', sai_get_ingress_priority_group_stats_fn),
    ('get_ingress_priority_group_stats_ext', sai_get_ingress_priority_group_stats_ext_fn),
    ('clear_ingress_priority_group_stats', sai_clear_ingress_priority_group_stats_fn),
    ('create_buffer_profile', sai_create_buffer_profile_fn),
    ('remove_buffer_profile', sai_remove_buffer_profile_fn),
    ('set_buffer_profile_attribute', sai_set_buffer_profile_attribute_fn),
    ('get_buffer_profile_attribute', sai_get_buffer_profile_attribute_fn),
]

sai_buffer_api_t = struct__sai_buffer_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 758

enum__sai_counter_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 48

SAI_COUNTER_TYPE_REGULAR = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 48

sai_counter_type_t = enum__sai_counter_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 48

enum__sai_counter_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

SAI_COUNTER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

SAI_COUNTER_ATTR_TYPE = SAI_COUNTER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

SAI_COUNTER_ATTR_END = (SAI_COUNTER_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

SAI_COUNTER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

SAI_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_COUNTER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

sai_counter_attr_t = enum__sai_counter_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 83

sai_create_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 95

sai_remove_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 108

sai_set_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 119

sai_get_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 132

enum__sai_counter_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 151

SAI_COUNTER_STAT_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 151

SAI_COUNTER_STAT_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 151

SAI_COUNTER_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 151

sai_counter_stat_t = enum__sai_counter_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 151

sai_get_counter_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 163

sai_get_counter_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 180

sai_clear_counter_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 196

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 214
class struct__sai_counter_api_t(Structure):
    pass

struct__sai_counter_api_t.__slots__ = [
    'create_counter',
    'remove_counter',
    'set_counter_attribute',
    'get_counter_attribute',
    'get_counter_stats',
    'get_counter_stats_ext',
    'clear_counter_stats',
]
struct__sai_counter_api_t._fields_ = [
    ('create_counter', sai_create_counter_fn),
    ('remove_counter', sai_remove_counter_fn),
    ('set_counter_attribute', sai_set_counter_attribute_fn),
    ('get_counter_attribute', sai_get_counter_attribute_fn),
    ('get_counter_stats', sai_get_counter_stats_fn),
    ('get_counter_stats_ext', sai_get_counter_stats_ext_fn),
    ('clear_counter_stats', sai_clear_counter_stats_fn),
]

sai_counter_api_t = struct__sai_counter_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 214

enum__sai_debug_counter_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

sai_debug_counter_type_t = enum__sai_debug_counter_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 67

enum__sai_debug_counter_bind_method_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 77

SAI_DEBUG_COUNTER_BIND_METHOD_AUTOMATIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 77

sai_debug_counter_bind_method_t = enum__sai_debug_counter_bind_method_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 77

enum__sai_in_drop_reason_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_L2_ANY = SAI_IN_DROP_REASON_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SMAC_MULTICAST = (SAI_IN_DROP_REASON_L2_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC = (SAI_IN_DROP_REASON_SMAC_MULTICAST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_DMAC_RESERVED = (SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED = (SAI_IN_DROP_REASON_DMAC_RESERVED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER = (SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_INGRESS_STP_FILTER = (SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_FDB_UC_DISCARD = (SAI_IN_DROP_REASON_INGRESS_STP_FILTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_FDB_MC_DISCARD = (SAI_IN_DROP_REASON_FDB_UC_DISCARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER = (SAI_IN_DROP_REASON_FDB_MC_DISCARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_EXCEEDS_L2_MTU = (SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_L3_ANY = (SAI_IN_DROP_REASON_EXCEEDS_L2_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_EXCEEDS_L3_MTU = (SAI_IN_DROP_REASON_L3_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_TTL = (SAI_IN_DROP_REASON_EXCEEDS_L3_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER = (SAI_IN_DROP_REASON_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_NON_ROUTABLE = (SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_NO_L3_HEADER = (SAI_IN_DROP_REASON_NON_ROUTABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_IP_HEADER_ERROR = (SAI_IN_DROP_REASON_NO_L3_HEADER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_UC_DIP_MC_DMAC = (SAI_IN_DROP_REASON_IP_HEADER_ERROR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_DIP_LOOPBACK = (SAI_IN_DROP_REASON_UC_DIP_MC_DMAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_LOOPBACK = (SAI_IN_DROP_REASON_DIP_LOOPBACK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_MC = (SAI_IN_DROP_REASON_SIP_LOOPBACK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_CLASS_E = (SAI_IN_DROP_REASON_SIP_MC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_UNSPECIFIED = (SAI_IN_DROP_REASON_SIP_CLASS_E + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_MC_DMAC_MISMATCH = (SAI_IN_DROP_REASON_SIP_UNSPECIFIED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_EQUALS_DIP = (SAI_IN_DROP_REASON_MC_DMAC_MISMATCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_BC = (SAI_IN_DROP_REASON_SIP_EQUALS_DIP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_DIP_LOCAL = (SAI_IN_DROP_REASON_SIP_BC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_DIP_LINK_LOCAL = (SAI_IN_DROP_REASON_DIP_LOCAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_SIP_LINK_LOCAL = (SAI_IN_DROP_REASON_DIP_LINK_LOCAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_IPV6_MC_SCOPE0 = (SAI_IN_DROP_REASON_SIP_LINK_LOCAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_IPV6_MC_SCOPE1 = (SAI_IN_DROP_REASON_IPV6_MC_SCOPE0 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_IRIF_DISABLED = (SAI_IN_DROP_REASON_IPV6_MC_SCOPE1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ERIF_DISABLED = (SAI_IN_DROP_REASON_IRIF_DISABLED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_LPM4_MISS = (SAI_IN_DROP_REASON_ERIF_DISABLED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_LPM6_MISS = (SAI_IN_DROP_REASON_LPM4_MISS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_BLACKHOLE_ROUTE = (SAI_IN_DROP_REASON_LPM6_MISS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_BLACKHOLE_ARP = (SAI_IN_DROP_REASON_BLACKHOLE_ROUTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP = (SAI_IN_DROP_REASON_BLACKHOLE_ARP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN = (SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_DECAP_ERROR = (SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_ANY = (SAI_IN_DROP_REASON_DECAP_ERROR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_INGRESS_PORT = (SAI_IN_DROP_REASON_ACL_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_INGRESS_LAG = (SAI_IN_DROP_REASON_ACL_INGRESS_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_INGRESS_VLAN = (SAI_IN_DROP_REASON_ACL_INGRESS_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_INGRESS_RIF = (SAI_IN_DROP_REASON_ACL_INGRESS_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH = (SAI_IN_DROP_REASON_ACL_INGRESS_RIF + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_EGRESS_PORT = (SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_EGRESS_LAG = (SAI_IN_DROP_REASON_ACL_EGRESS_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_EGRESS_VLAN = (SAI_IN_DROP_REASON_ACL_EGRESS_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_EGRESS_RIF = (SAI_IN_DROP_REASON_ACL_EGRESS_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH = (SAI_IN_DROP_REASON_ACL_EGRESS_RIF + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_END = (SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

SAI_IN_DROP_REASON_CUSTOM_RANGE_END = (SAI_IN_DROP_REASON_CUSTOM_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

sai_in_drop_reason_t = enum__sai_in_drop_reason_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 315

enum__sai_out_drop_reason_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_L2_ANY = SAI_OUT_DROP_REASON_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER = (SAI_OUT_DROP_REASON_L2_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_L3_ANY = (SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN = (SAI_OUT_DROP_REASON_L3_ANY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_END = (SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

SAI_OUT_DROP_REASON_CUSTOM_RANGE_END = (SAI_OUT_DROP_REASON_CUSTOM_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

sai_out_drop_reason_t = enum__sai_out_drop_reason_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 354

enum__sai_debug_counter_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_INDEX = SAI_DEBUG_COUNTER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_TYPE = (SAI_DEBUG_COUNTER_ATTR_INDEX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_BIND_METHOD = (SAI_DEBUG_COUNTER_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST = (SAI_DEBUG_COUNTER_ATTR_BIND_METHOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST = (SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_END = (SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

sai_debug_counter_attr_t = enum__sai_debug_counter_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 431

sai_create_debug_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 443

sai_remove_debug_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 456

sai_set_debug_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 467

sai_get_debug_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 480

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 495
class struct__sai_debug_counter_api_t(Structure):
    pass

struct__sai_debug_counter_api_t.__slots__ = [
    'create_debug_counter',
    'remove_debug_counter',
    'set_debug_counter_attribute',
    'get_debug_counter_attribute',
]
struct__sai_debug_counter_api_t._fields_ = [
    ('create_debug_counter', sai_create_debug_counter_fn),
    ('remove_debug_counter', sai_remove_debug_counter_fn),
    ('set_debug_counter_attribute', sai_set_debug_counter_attribute_fn),
    ('get_debug_counter_attribute', sai_get_debug_counter_attribute_fn),
]

sai_debug_counter_api_t = struct__sai_debug_counter_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 495

enum__sai_dtel_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_ENDPOINT_ENABLE = SAI_DTEL_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_TRANSIT_ENABLE = (SAI_DTEL_ATTR_INT_ENDPOINT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_POSTCARD_ENABLE = (SAI_DTEL_ATTR_INT_TRANSIT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_DROP_REPORT_ENABLE = (SAI_DTEL_ATTR_POSTCARD_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_QUEUE_REPORT_ENABLE = (SAI_DTEL_ATTR_DROP_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_SWITCH_ID = (SAI_DTEL_ATTR_QUEUE_REPORT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_FLOW_STATE_CLEAR_CYCLE = (SAI_DTEL_ATTR_SWITCH_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_LATENCY_SENSITIVITY = (SAI_DTEL_ATTR_FLOW_STATE_CLEAR_CYCLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_SINK_PORT_LIST = (SAI_DTEL_ATTR_LATENCY_SENSITIVITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_L4_DSCP = (SAI_DTEL_ATTR_SINK_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_END = (SAI_DTEL_ATTR_INT_L4_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

SAI_DTEL_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

sai_dtel_attr_t = enum__sai_dtel_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 179

enum__sai_dtel_queue_report_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_QUEUE_ID = SAI_DTEL_QUEUE_REPORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_DEPTH_THRESHOLD = (SAI_DTEL_QUEUE_REPORT_ATTR_QUEUE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_LATENCY_THRESHOLD = (SAI_DTEL_QUEUE_REPORT_ATTR_DEPTH_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_BREACH_QUOTA = (SAI_DTEL_QUEUE_REPORT_ATTR_LATENCY_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_TAIL_DROP = (SAI_DTEL_QUEUE_REPORT_ATTR_BREACH_QUOTA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_END = (SAI_DTEL_QUEUE_REPORT_ATTR_TAIL_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

sai_dtel_queue_report_attr_t = enum__sai_dtel_queue_report_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 263

enum__sai_dtel_int_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_MAX_HOP_COUNT = SAI_DTEL_INT_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_ID = (SAI_DTEL_INT_SESSION_ATTR_MAX_HOP_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_PORTS = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_INGRESS_TIMESTAMP = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_EGRESS_TIMESTAMP = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_INGRESS_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_QUEUE_INFO = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_EGRESS_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_END = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_QUEUE_INFO + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

sai_dtel_int_session_attr_t = enum__sai_dtel_int_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 361

enum__sai_dtel_report_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_SRC_IP = SAI_DTEL_REPORT_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_DST_IP_LIST = (SAI_DTEL_REPORT_SESSION_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_VIRTUAL_ROUTER_ID = (SAI_DTEL_REPORT_SESSION_ATTR_DST_IP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_TRUNCATE_SIZE = (SAI_DTEL_REPORT_SESSION_ATTR_VIRTUAL_ROUTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_UDP_DST_PORT = (SAI_DTEL_REPORT_SESSION_ATTR_TRUNCATE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_END = (SAI_DTEL_REPORT_SESSION_ATTR_UDP_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

sai_dtel_report_session_attr_t = enum__sai_dtel_report_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 449

enum__sai_dtel_event_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_STATE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_REPORT_ALL_PACKETS = (SAI_DTEL_EVENT_TYPE_FLOW_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_TCPFLAG = (SAI_DTEL_EVENT_TYPE_FLOW_REPORT_ALL_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_THRESHOLD_BREACH = (SAI_DTEL_EVENT_TYPE_FLOW_TCPFLAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_TAIL_DROP = (SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_THRESHOLD_BREACH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_DROP_REPORT = (SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_TAIL_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_MAX = (SAI_DTEL_EVENT_TYPE_DROP_REPORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

sai_dtel_event_type_t = enum__sai_dtel_event_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 478

enum__sai_dtel_event_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_TYPE = SAI_DTEL_EVENT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_REPORT_SESSION = (SAI_DTEL_EVENT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_DSCP_VALUE = (SAI_DTEL_EVENT_ATTR_REPORT_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_END = (SAI_DTEL_EVENT_ATTR_DSCP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

sai_dtel_event_attr_t = enum__sai_dtel_event_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 541

sai_create_dtel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 555

sai_remove_dtel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 570

sai_set_dtel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 583

sai_get_dtel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 598

sai_create_dtel_queue_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 615

sai_remove_dtel_queue_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 630

sai_set_dtel_queue_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 643

sai_get_dtel_queue_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 658

sai_create_dtel_int_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 675

sai_remove_dtel_int_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 690

sai_set_dtel_int_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 703

sai_get_dtel_int_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 718

sai_create_dtel_report_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 735

sai_remove_dtel_report_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 750

sai_set_dtel_report_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 763

sai_get_dtel_report_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 778

sai_create_dtel_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 795

sai_remove_dtel_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 810

sai_set_dtel_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 823

sai_get_dtel_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 838

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 870
class struct__sai_dtel_api_t(Structure):
    pass

struct__sai_dtel_api_t.__slots__ = [
    'create_dtel',
    'remove_dtel',
    'set_dtel_attribute',
    'get_dtel_attribute',
    'create_dtel_queue_report',
    'remove_dtel_queue_report',
    'set_dtel_queue_report_attribute',
    'get_dtel_queue_report_attribute',
    'create_dtel_int_session',
    'remove_dtel_int_session',
    'set_dtel_int_session_attribute',
    'get_dtel_int_session_attribute',
    'create_dtel_report_session',
    'remove_dtel_report_session',
    'set_dtel_report_session_attribute',
    'get_dtel_report_session_attribute',
    'create_dtel_event',
    'remove_dtel_event',
    'set_dtel_event_attribute',
    'get_dtel_event_attribute',
]
struct__sai_dtel_api_t._fields_ = [
    ('create_dtel', sai_create_dtel_fn),
    ('remove_dtel', sai_remove_dtel_fn),
    ('set_dtel_attribute', sai_set_dtel_attribute_fn),
    ('get_dtel_attribute', sai_get_dtel_attribute_fn),
    ('create_dtel_queue_report', sai_create_dtel_queue_report_fn),
    ('remove_dtel_queue_report', sai_remove_dtel_queue_report_fn),
    ('set_dtel_queue_report_attribute', sai_set_dtel_queue_report_attribute_fn),
    ('get_dtel_queue_report_attribute', sai_get_dtel_queue_report_attribute_fn),
    ('create_dtel_int_session', sai_create_dtel_int_session_fn),
    ('remove_dtel_int_session', sai_remove_dtel_int_session_fn),
    ('set_dtel_int_session_attribute', sai_set_dtel_int_session_attribute_fn),
    ('get_dtel_int_session_attribute', sai_get_dtel_int_session_attribute_fn),
    ('create_dtel_report_session', sai_create_dtel_report_session_fn),
    ('remove_dtel_report_session', sai_remove_dtel_report_session_fn),
    ('set_dtel_report_session_attribute', sai_set_dtel_report_session_attribute_fn),
    ('get_dtel_report_session_attribute', sai_get_dtel_report_session_attribute_fn),
    ('create_dtel_event', sai_create_dtel_event_fn),
    ('remove_dtel_event', sai_remove_dtel_event_fn),
    ('set_dtel_event_attribute', sai_set_dtel_event_attribute_fn),
    ('get_dtel_event_attribute', sai_get_dtel_event_attribute_fn),
]

sai_dtel_api_t = struct__sai_dtel_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 870

enum__sai_es_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

SAI_ES_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

SAI_ES_ATTR_ESI_LABEL = SAI_ES_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

SAI_ES_ATTR_END = (SAI_ES_ATTR_ESI_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

SAI_ES_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

SAI_ES_ATTR_CUSTOM_RANGE_END = (SAI_ES_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

sai_es_attr_t = enum__sai_es_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 66

sai_create_es_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 79

sai_remove_es_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 92

sai_set_es_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 103

sai_get_es_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 116

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 130
class struct__sai_es_api_t(Structure):
    pass

struct__sai_es_api_t.__slots__ = [
    'create_es',
    'remove_es',
    'set_es_attribute',
    'get_es_attribute',
]
struct__sai_es_api_t._fields_ = [
    ('create_es', sai_create_es_fn),
    ('remove_es', sai_remove_es_fn),
    ('set_es_attribute', sai_set_es_attribute_fn),
    ('get_es_attribute', sai_get_es_attribute_fn),
]

sai_es_api_t = struct__sai_es_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 130

enum__sai_fdb_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 47

SAI_FDB_ENTRY_TYPE_DYNAMIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 47

SAI_FDB_ENTRY_TYPE_STATIC = (SAI_FDB_ENTRY_TYPE_DYNAMIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 47

sai_fdb_entry_type_t = enum__sai_fdb_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 47

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 71
class struct__sai_fdb_entry_t(Structure):
    pass

struct__sai_fdb_entry_t.__slots__ = [
    'switch_id',
    'mac_address',
    'bv_id',
]
struct__sai_fdb_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('mac_address', sai_mac_t),
    ('bv_id', sai_object_id_t),
]

sai_fdb_entry_t = struct__sai_fdb_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 71

enum__sai_fdb_event_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

SAI_FDB_EVENT_LEARNED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

SAI_FDB_EVENT_AGED = (SAI_FDB_EVENT_LEARNED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

SAI_FDB_EVENT_MOVE = (SAI_FDB_EVENT_AGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

SAI_FDB_EVENT_FLUSHED = (SAI_FDB_EVENT_MOVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

sai_fdb_event_t = enum__sai_fdb_event_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 90

enum__sai_fdb_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_TYPE = SAI_FDB_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_PACKET_ACTION = (SAI_FDB_ENTRY_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_USER_TRAP_ID = (SAI_FDB_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID = (SAI_FDB_ENTRY_ATTR_USER_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_META_DATA = (SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_ENDPOINT_IP = (SAI_FDB_ENTRY_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_COUNTER_ID = (SAI_FDB_ENTRY_ATTR_ENDPOINT_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_END = (SAI_FDB_ENTRY_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

sai_fdb_entry_attr_t = enum__sai_fdb_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 192

enum__sai_fdb_flush_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 208

SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 208

SAI_FDB_FLUSH_ENTRY_TYPE_STATIC = (SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 208

SAI_FDB_FLUSH_ENTRY_TYPE_ALL = (SAI_FDB_FLUSH_ENTRY_TYPE_STATIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 208

sai_fdb_flush_entry_type_t = enum__sai_fdb_flush_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 208

enum__sai_fdb_flush_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID = SAI_FDB_FLUSH_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_BV_ID = (SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_ENTRY_TYPE = (SAI_FDB_FLUSH_ATTR_BV_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_END = (SAI_FDB_FLUSH_ATTR_ENTRY_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_END = (SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

sai_fdb_flush_attr_t = enum__sai_fdb_flush_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 278

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 334
class struct__sai_fdb_event_notification_data_t(Structure):
    pass

struct__sai_fdb_event_notification_data_t.__slots__ = [
    'event_type',
    'fdb_entry',
    'attr_count',
    'attr',
]
struct__sai_fdb_event_notification_data_t._fields_ = [
    ('event_type', sai_fdb_event_t),
    ('fdb_entry', sai_fdb_entry_t),
    ('attr_count', c_uint32),
    ('attr', POINTER(sai_attribute_t)),
]

sai_fdb_event_notification_data_t = struct__sai_fdb_event_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 334

sai_create_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 345

sai_remove_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 357

sai_set_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 368

sai_get_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 381

sai_flush_fdb_entries_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 395

sai_fdb_event_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_fdb_event_notification_data_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 408

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 423
class struct__sai_fdb_api_t(Structure):
    pass

struct__sai_fdb_api_t.__slots__ = [
    'create_fdb_entry',
    'remove_fdb_entry',
    'set_fdb_entry_attribute',
    'get_fdb_entry_attribute',
    'flush_fdb_entries',
]
struct__sai_fdb_api_t._fields_ = [
    ('create_fdb_entry', sai_create_fdb_entry_fn),
    ('remove_fdb_entry', sai_remove_fdb_entry_fn),
    ('set_fdb_entry_attribute', sai_set_fdb_entry_attribute_fn),
    ('get_fdb_entry_attribute', sai_get_fdb_entry_attribute_fn),
    ('flush_fdb_entries', sai_flush_fdb_entries_fn),
]

sai_fdb_api_t = struct__sai_fdb_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 423

enum__sai_native_hash_field_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_SRC_IP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_DST_IP = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_SRC_IP = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_DST_IP = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_VLAN_ID = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_IP_PROTOCOL = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_ETHERTYPE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_L4_SRC_PORT = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_L4_DST_PORT = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_SRC_MAC = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_DST_MAC = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_IN_PORT = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_INNER_DST_MAC = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

sai_native_hash_field_t = enum__sai_native_hash_field_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 108

enum__sai_hash_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST = SAI_HASH_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_UDF_GROUP_LIST = (SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_END = (SAI_HASH_ATTR_UDF_GROUP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

SAI_HASH_ATTR_CUSTOM_RANGE_END = (SAI_HASH_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

sai_hash_attr_t = enum__sai_hash_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 150

sai_create_hash_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 162

sai_remove_hash_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 175

sai_set_hash_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 186

sai_get_hash_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 199

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 214
class struct__sai_hash_api_t(Structure):
    pass

struct__sai_hash_api_t.__slots__ = [
    'create_hash',
    'remove_hash',
    'set_hash_attribute',
    'get_hash_attribute',
]
struct__sai_hash_api_t._fields_ = [
    ('create_hash', sai_create_hash_fn),
    ('remove_hash', sai_remove_hash_fn),
    ('set_hash_attribute', sai_set_hash_attribute_fn),
    ('get_hash_attribute', sai_get_hash_attribute_fn),
]

sai_hash_api_t = struct__sai_hash_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 214

enum__sai_hostif_trap_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE = SAI_HOSTIF_TRAP_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE = (SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER = (SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_END = (SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

sai_hostif_trap_group_attr_t = enum__sai_hostif_trap_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 103

sai_create_hostif_trap_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 115

sai_remove_hostif_trap_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 128

sai_set_hostif_trap_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 139

sai_get_hostif_trap_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 152

enum__sai_hostif_trap_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_STP = SAI_HOSTIF_TRAP_TYPE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_LACP = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_EAPOL = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_LLDP = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PVRST = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_UDLD = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CDP = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_VTP = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_DTP = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PAGP = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PTP = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PTP_TX_EVENT = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_SWITCH_CUSTOM_RANGE_BASE = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST = 8192 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE = 8193 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_DHCP = 8194 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_OSPF = 8195 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PIM = 8196 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_VRRP = 8197 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_DHCPV6 = 8198 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_OSPFV6 = 8199 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_VRRPV6 = 8200 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY = 8201 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2 = 8202 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT = 8203 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE = 8204 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT = 8205 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST = 8206 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_SNAT_MISS = 8207 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_DNAT_MISS = 8208 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_NAT_HAIRPIN = 8209 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_ROUTER_CUSTOM_RANGE_BASE = 12288 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_IP2ME = 16384 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_SSH = 16385 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_SNMP = 16386 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_BGP = 16387 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_BGPV6 = 16388 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_BFD = 16389 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_BFDV6 = 16390 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_LOCAL_IP_CUSTOM_RANGE_BASE = 20480 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR = 24576 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_TTL_ERROR = 24577 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_STATIC_FDB_MOVE = 24578 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_EGRESS_BUFFER = 28672 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_WRED = 28673 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_ROUTER = 28674 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_RANGE_BASE = 32768 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_DM = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LT = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_DM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LBR = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LMR = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LBR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_CV_FAIL = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LMR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_APS = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_CV_FAIL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DLM = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_APS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DM = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DLM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_MICROBURST_LOG = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_LATENCY_OVERFLOW_LOG = (SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_MICROBURST_LOG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

SAI_HOSTIF_TRAP_TYPE_END = 36864 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

sai_hostif_trap_type_t = enum__sai_hostif_trap_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 471

enum__sai_hostif_trap_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE = SAI_HOSTIF_TRAP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION = (SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY = (SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST = (SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP = (SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION = (SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_COUNTER_ID = (SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_END = (SAI_HOSTIF_TRAP_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

sai_hostif_trap_attr_t = enum__sai_hostif_trap_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 567

sai_create_hostif_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 579

sai_remove_hostif_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 592

sai_set_hostif_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 603

sai_get_hostif_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 616

enum__sai_hostif_user_defined_trap_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER = SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGH = SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_FDB = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_CUSTOM_RANGE_BASE = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_END = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_CUSTOM_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

sai_hostif_user_defined_trap_type_t = enum__sai_hostif_user_defined_trap_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 661

enum__sai_hostif_user_defined_trap_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE = SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_END = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

sai_hostif_user_defined_trap_attr_t = enum__sai_hostif_user_defined_trap_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 714

sai_create_hostif_user_defined_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 726

sai_remove_hostif_user_defined_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 739

sai_set_hostif_user_defined_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 750

sai_get_hostif_user_defined_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 763

enum__sai_hostif_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 782

SAI_HOSTIF_TYPE_NETDEV = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 782

SAI_HOSTIF_TYPE_FD = (SAI_HOSTIF_TYPE_NETDEV + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 782

SAI_HOSTIF_TYPE_GENETLINK = (SAI_HOSTIF_TYPE_FD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 782

sai_hostif_type_t = enum__sai_hostif_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 782

enum__sai_hostif_vlan_tag_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 813

SAI_HOSTIF_VLAN_TAG_STRIP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 813

SAI_HOSTIF_VLAN_TAG_KEEP = (SAI_HOSTIF_VLAN_TAG_STRIP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 813

SAI_HOSTIF_VLAN_TAG_ORIGINAL = (SAI_HOSTIF_VLAN_TAG_KEEP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 813

sai_hostif_vlan_tag_t = enum__sai_hostif_vlan_tag_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 813

enum__sai_hostif_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_TYPE = SAI_HOSTIF_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_OBJ_ID = (SAI_HOSTIF_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_NAME = (SAI_HOSTIF_ATTR_OBJ_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_OPER_STATUS = (SAI_HOSTIF_ATTR_NAME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_QUEUE = (SAI_HOSTIF_ATTR_OPER_STATUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_VLAN_TAG = (SAI_HOSTIF_ATTR_QUEUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_GENETLINK_MCGRP_NAME = (SAI_HOSTIF_ATTR_VLAN_TAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_END = (SAI_HOSTIF_ATTR_GENETLINK_MCGRP_NAME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

SAI_HOSTIF_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

sai_hostif_attr_t = enum__sai_hostif_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 913

sai_create_hostif_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 925

sai_remove_hostif_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 938

sai_set_hostif_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 949

sai_get_hostif_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 962

enum__sai_hostif_table_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG = (SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN = (SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID = (SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

SAI_HOSTIF_TABLE_ENTRY_TYPE_WILDCARD = (SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

sai_hostif_table_entry_type_t = enum__sai_hostif_table_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 987

enum__sai_hostif_table_entry_channel_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_FD = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_FD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_LOGICAL_PORT = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_L3 = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_LOGICAL_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_GENETLINK = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_L3 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

sai_hostif_table_entry_channel_type_t = enum__sai_hostif_table_entry_channel_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1012

enum__sai_hostif_table_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE = SAI_HOSTIF_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID = (SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID = (SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE = (SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF = (SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_END = (SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

sai_hostif_table_entry_attr_t = enum__sai_hostif_table_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1087

sai_create_hostif_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1099

sai_remove_hostif_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1112

sai_set_hostif_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1123

sai_get_hostif_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1136

enum__sai_hostif_tx_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

SAI_HOSTIF_TX_TYPE_PIPELINE_LOOKUP = (SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX = (SAI_HOSTIF_TX_TYPE_PIPELINE_LOOKUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX = (SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

SAI_HOSTIF_TX_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

sai_hostif_tx_type_t = enum__sai_hostif_tx_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1164

enum__sai_hostif_packet_oam_tx_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

SAI_HOSTIF_PACKET_OAM_TX_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM = (SAI_HOSTIF_PACKET_OAM_TX_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM = (SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

SAI_HOSTIF_PACKET_OAM_TX_TYPE_OTHER = (SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

sai_hostif_packet_oam_tx_type_t = enum__sai_hostif_packet_oam_tx_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1186

enum__sai_hostif_packet_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = SAI_HOSTIF_PACKET_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = (SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG = (SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE = (SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG = (SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = (SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = (SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = (SAI_HOSTIF_PACKET_ATTR_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_END = (SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_TX_TYPE = (SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_Y1731_SESSION_ID = (SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_TX_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_CUSTOM_TIMESTAMP_OFFSET = (SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_Y1731_SESSION_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_PACKET_ATTR_CUSTOM_TIMESTAMP_OFFSET + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

sai_hostif_packet_attr_t = enum__sai_hostif_packet_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1326

sai_recv_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_size_t), POINTER(None), POINTER(c_uint32), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1342

sai_send_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, sai_size_t, POINTER(None), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1362

sai_packet_event_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_size_t, POINTER(None), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1383

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1417
class struct__sai_hostif_api_t(Structure):
    pass

struct__sai_hostif_api_t.__slots__ = [
    'create_hostif',
    'remove_hostif',
    'set_hostif_attribute',
    'get_hostif_attribute',
    'create_hostif_table_entry',
    'remove_hostif_table_entry',
    'set_hostif_table_entry_attribute',
    'get_hostif_table_entry_attribute',
    'create_hostif_trap_group',
    'remove_hostif_trap_group',
    'set_hostif_trap_group_attribute',
    'get_hostif_trap_group_attribute',
    'create_hostif_trap',
    'remove_hostif_trap',
    'set_hostif_trap_attribute',
    'get_hostif_trap_attribute',
    'create_hostif_user_defined_trap',
    'remove_hostif_user_defined_trap',
    'set_hostif_user_defined_trap_attribute',
    'get_hostif_user_defined_trap_attribute',
    'recv_hostif_packet',
    'send_hostif_packet',
]
struct__sai_hostif_api_t._fields_ = [
    ('create_hostif', sai_create_hostif_fn),
    ('remove_hostif', sai_remove_hostif_fn),
    ('set_hostif_attribute', sai_set_hostif_attribute_fn),
    ('get_hostif_attribute', sai_get_hostif_attribute_fn),
    ('create_hostif_table_entry', sai_create_hostif_table_entry_fn),
    ('remove_hostif_table_entry', sai_remove_hostif_table_entry_fn),
    ('set_hostif_table_entry_attribute', sai_set_hostif_table_entry_attribute_fn),
    ('get_hostif_table_entry_attribute', sai_get_hostif_table_entry_attribute_fn),
    ('create_hostif_trap_group', sai_create_hostif_trap_group_fn),
    ('remove_hostif_trap_group', sai_remove_hostif_trap_group_fn),
    ('set_hostif_trap_group_attribute', sai_set_hostif_trap_group_attribute_fn),
    ('get_hostif_trap_group_attribute', sai_get_hostif_trap_group_attribute_fn),
    ('create_hostif_trap', sai_create_hostif_trap_fn),
    ('remove_hostif_trap', sai_remove_hostif_trap_fn),
    ('set_hostif_trap_attribute', sai_set_hostif_trap_attribute_fn),
    ('get_hostif_trap_attribute', sai_get_hostif_trap_attribute_fn),
    ('create_hostif_user_defined_trap', sai_create_hostif_user_defined_trap_fn),
    ('remove_hostif_user_defined_trap', sai_remove_hostif_user_defined_trap_fn),
    ('set_hostif_user_defined_trap_attribute', sai_set_hostif_user_defined_trap_attribute_fn),
    ('get_hostif_user_defined_trap_attribute', sai_get_hostif_user_defined_trap_attribute_fn),
    ('recv_hostif_packet', sai_recv_hostif_packet_fn),
    ('send_hostif_packet', sai_send_hostif_packet_fn),
]

sai_hostif_api_t = struct__sai_hostif_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1417

enum__sai_ipmc_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT = SAI_IPMC_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST = (SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_END = (SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

sai_ipmc_group_attr_t = enum__sai_ipmc_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 74

enum__sai_ipmc_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID = SAI_IPMC_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID = (SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_END = (SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

sai_ipmc_group_member_attr_t = enum__sai_ipmc_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 112

sai_create_ipmc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 124

sai_remove_ipmc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 137

sai_set_ipmc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 148

sai_get_ipmc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 161

sai_create_ipmc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 176

sai_remove_ipmc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 189

sai_set_ipmc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 200

sai_get_ipmc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 213

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 232
class struct__sai_ipmc_group_api_t(Structure):
    pass

struct__sai_ipmc_group_api_t.__slots__ = [
    'create_ipmc_group',
    'remove_ipmc_group',
    'set_ipmc_group_attribute',
    'get_ipmc_group_attribute',
    'create_ipmc_group_member',
    'remove_ipmc_group_member',
    'set_ipmc_group_member_attribute',
    'get_ipmc_group_member_attribute',
]
struct__sai_ipmc_group_api_t._fields_ = [
    ('create_ipmc_group', sai_create_ipmc_group_fn),
    ('remove_ipmc_group', sai_remove_ipmc_group_fn),
    ('set_ipmc_group_attribute', sai_set_ipmc_group_attribute_fn),
    ('get_ipmc_group_attribute', sai_get_ipmc_group_attribute_fn),
    ('create_ipmc_group_member', sai_create_ipmc_group_member_fn),
    ('remove_ipmc_group_member', sai_remove_ipmc_group_member_fn),
    ('set_ipmc_group_member_attribute', sai_set_ipmc_group_member_attribute_fn),
    ('get_ipmc_group_member_attribute', sai_get_ipmc_group_member_attribute_fn),
]

sai_ipmc_group_api_t = struct__sai_ipmc_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 232

enum__sai_ipmc_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 47

SAI_IPMC_ENTRY_TYPE_SG = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 47

SAI_IPMC_ENTRY_TYPE_XG = (SAI_IPMC_ENTRY_TYPE_SG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 47

sai_ipmc_entry_type_t = enum__sai_ipmc_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 47

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 76
class struct__sai_ipmc_entry_t(Structure):
    pass

struct__sai_ipmc_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'type',
    'destination',
    'source',
]
struct__sai_ipmc_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('type', sai_ipmc_entry_type_t),
    ('destination', sai_ip_address_t),
    ('source', sai_ip_address_t),
]

sai_ipmc_entry_t = struct__sai_ipmc_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 76

enum__sai_ipmc_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_PACKET_ACTION = SAI_IPMC_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID = (SAI_IPMC_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID = (SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_END = (SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

sai_ipmc_entry_attr_t = enum__sai_ipmc_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 133

sai_create_ipmc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 144

sai_remove_ipmc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 156

sai_set_ipmc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 167

sai_get_ipmc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 180

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 195
class struct__sai_ipmc_api_t(Structure):
    pass

struct__sai_ipmc_api_t.__slots__ = [
    'create_ipmc_entry',
    'remove_ipmc_entry',
    'set_ipmc_entry_attribute',
    'get_ipmc_entry_attribute',
]
struct__sai_ipmc_api_t._fields_ = [
    ('create_ipmc_entry', sai_create_ipmc_entry_fn),
    ('remove_ipmc_entry', sai_remove_ipmc_entry_fn),
    ('set_ipmc_entry_attribute', sai_set_ipmc_entry_attribute_fn),
    ('get_ipmc_entry_attribute', sai_get_ipmc_entry_attribute_fn),
]

sai_ipmc_api_t = struct__sai_ipmc_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 195

enum__sai_l2mc_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = SAI_L2MC_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST = (SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_END = (SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

sai_l2mc_group_attr_t = enum__sai_l2mc_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 74

enum__sai_l2mc_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID = SAI_L2MC_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_END = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

sai_l2mc_group_member_attr_t = enum__sai_l2mc_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 122

sai_create_l2mc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 134

sai_remove_l2mc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 147

sai_set_l2mc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 158

sai_get_l2mc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 171

sai_create_l2mc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 186

sai_remove_l2mc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 199

sai_set_l2mc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 210

sai_get_l2mc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 223

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 242
class struct__sai_l2mc_group_api_t(Structure):
    pass

struct__sai_l2mc_group_api_t.__slots__ = [
    'create_l2mc_group',
    'remove_l2mc_group',
    'set_l2mc_group_attribute',
    'get_l2mc_group_attribute',
    'create_l2mc_group_member',
    'remove_l2mc_group_member',
    'set_l2mc_group_member_attribute',
    'get_l2mc_group_member_attribute',
]
struct__sai_l2mc_group_api_t._fields_ = [
    ('create_l2mc_group', sai_create_l2mc_group_fn),
    ('remove_l2mc_group', sai_remove_l2mc_group_fn),
    ('set_l2mc_group_attribute', sai_set_l2mc_group_attribute_fn),
    ('get_l2mc_group_attribute', sai_get_l2mc_group_attribute_fn),
    ('create_l2mc_group_member', sai_create_l2mc_group_member_fn),
    ('remove_l2mc_group_member', sai_remove_l2mc_group_member_fn),
    ('set_l2mc_group_member_attribute', sai_set_l2mc_group_member_attribute_fn),
    ('get_l2mc_group_member_attribute', sai_get_l2mc_group_member_attribute_fn),
]

sai_l2mc_group_api_t = struct__sai_l2mc_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 242

enum__sai_l2mc_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 47

SAI_L2MC_ENTRY_TYPE_SG = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 47

SAI_L2MC_ENTRY_TYPE_XG = (SAI_L2MC_ENTRY_TYPE_SG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 47

sai_l2mc_entry_type_t = enum__sai_l2mc_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 47

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 76
class struct__sai_l2mc_entry_t(Structure):
    pass

struct__sai_l2mc_entry_t.__slots__ = [
    'switch_id',
    'bv_id',
    'type',
    'destination',
    'source',
]
struct__sai_l2mc_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('bv_id', sai_object_id_t),
    ('type', sai_l2mc_entry_type_t),
    ('destination', sai_ip_address_t),
    ('source', sai_ip_address_t),
]

sai_l2mc_entry_t = struct__sai_l2mc_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 76

enum__sai_l2mc_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_PACKET_ACTION = SAI_L2MC_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID = (SAI_L2MC_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_END = (SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

sai_l2mc_entry_attr_t = enum__sai_l2mc_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 122

sai_create_l2mc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 133

sai_remove_l2mc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 145

sai_set_l2mc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 156

sai_get_l2mc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 169

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 184
class struct__sai_l2mc_api_t(Structure):
    pass

struct__sai_l2mc_api_t.__slots__ = [
    'create_l2mc_entry',
    'remove_l2mc_entry',
    'set_l2mc_entry_attribute',
    'get_l2mc_entry_attribute',
]
struct__sai_l2mc_api_t._fields_ = [
    ('create_l2mc_entry', sai_create_l2mc_entry_fn),
    ('remove_l2mc_entry', sai_remove_l2mc_entry_fn),
    ('set_l2mc_entry_attribute', sai_set_l2mc_entry_attribute_fn),
    ('get_l2mc_entry_attribute', sai_get_l2mc_entry_attribute_fn),
]

sai_l2mc_api_t = struct__sai_l2mc_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 184

enum__sai_lag_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

SAI_LAG_MODE_STATIC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

SAI_LAG_MODE_STATIC_FAILOVER = (SAI_LAG_MODE_STATIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

SAI_LAG_MODE_RR = (SAI_LAG_MODE_STATIC_FAILOVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

SAI_LAG_MODE_DLB = (SAI_LAG_MODE_RR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

SAI_LAG_MODE_RH = (SAI_LAG_MODE_DLB + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

sai_lag_mode_t = enum__sai_lag_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 56

enum__sai_lag_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_PORT_LIST = SAI_LAG_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_INGRESS_ACL = (SAI_LAG_ATTR_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_EGRESS_ACL = (SAI_LAG_ATTR_INGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_PORT_VLAN_ID = (SAI_LAG_ATTR_EGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY = (SAI_LAG_ATTR_PORT_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_DROP_UNTAGGED = (SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_DROP_TAGGED = (SAI_LAG_ATTR_DROP_UNTAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_MODE = (SAI_LAG_ATTR_DROP_TAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_END = (SAI_LAG_ATTR_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM = (SAI_LAG_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

SAI_LAG_ATTR_CUSTOM_RANGE_END = (SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

sai_lag_attr_t = enum__sai_lag_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 200

sai_create_lag_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 212

sai_remove_lag_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 225

sai_set_lag_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 236

sai_get_lag_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 249

enum__sai_lag_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_LAG_ID = SAI_LAG_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_PORT_ID = (SAI_LAG_MEMBER_ATTR_LAG_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE = (SAI_LAG_MEMBER_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE = (SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_END = (SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

sai_lag_member_attr_t = enum__sai_lag_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 311

sai_create_lag_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 323

sai_remove_lag_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 336

sai_set_lag_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 347

sai_get_lag_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 360

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 380
class struct__sai_lag_api_t(Structure):
    pass

struct__sai_lag_api_t.__slots__ = [
    'create_lag',
    'remove_lag',
    'set_lag_attribute',
    'get_lag_attribute',
    'create_lag_member',
    'remove_lag_member',
    'set_lag_member_attribute',
    'get_lag_member_attribute',
    'create_lag_members',
    'remove_lag_members',
]
struct__sai_lag_api_t._fields_ = [
    ('create_lag', sai_create_lag_fn),
    ('remove_lag', sai_remove_lag_fn),
    ('set_lag_attribute', sai_set_lag_attribute_fn),
    ('get_lag_attribute', sai_get_lag_attribute_fn),
    ('create_lag_member', sai_create_lag_member_fn),
    ('remove_lag_member', sai_remove_lag_member_fn),
    ('set_lag_member_attribute', sai_set_lag_member_attribute_fn),
    ('get_lag_member_attribute', sai_get_lag_member_attribute_fn),
    ('create_lag_members', sai_bulk_object_create_fn),
    ('remove_lag_members', sai_bulk_object_remove_fn),
]

sai_lag_api_t = struct__sai_lag_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 380

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 58
class struct__sai_mcast_fdb_entry_t(Structure):
    pass

struct__sai_mcast_fdb_entry_t.__slots__ = [
    'switch_id',
    'mac_address',
    'bv_id',
]
struct__sai_mcast_fdb_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('mac_address', sai_mac_t),
    ('bv_id', sai_object_id_t),
]

sai_mcast_fdb_entry_t = struct__sai_mcast_fdb_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 58

enum__sai_mcast_fdb_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID = SAI_MCAST_FDB_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION = (SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_META_DATA = (SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_END = (SAI_MCAST_FDB_ENTRY_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

sai_mcast_fdb_entry_attr_t = enum__sai_mcast_fdb_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 112

sai_create_mcast_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 123

sai_remove_mcast_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 135

sai_set_mcast_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 146

sai_get_mcast_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 159

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 174
class struct__sai_mcast_fdb_api_t(Structure):
    pass

struct__sai_mcast_fdb_api_t.__slots__ = [
    'create_mcast_fdb_entry',
    'remove_mcast_fdb_entry',
    'set_mcast_fdb_entry_attribute',
    'get_mcast_fdb_entry_attribute',
]
struct__sai_mcast_fdb_api_t._fields_ = [
    ('create_mcast_fdb_entry', sai_create_mcast_fdb_entry_fn),
    ('remove_mcast_fdb_entry', sai_remove_mcast_fdb_entry_fn),
    ('set_mcast_fdb_entry_attribute', sai_set_mcast_fdb_entry_attribute_fn),
    ('get_mcast_fdb_entry_attribute', sai_get_mcast_fdb_entry_attribute_fn),
]

sai_mcast_fdb_api_t = struct__sai_mcast_fdb_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 174

enum__sai_mirror_session_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 50

SAI_MIRROR_SESSION_TYPE_LOCAL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 50

SAI_MIRROR_SESSION_TYPE_REMOTE = (SAI_MIRROR_SESSION_TYPE_LOCAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 50

SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE = (SAI_MIRROR_SESSION_TYPE_REMOTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 50

sai_mirror_session_type_t = enum__sai_mirror_session_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 50

enum__sai_erspan_encapsulation_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 62

SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 62

sai_erspan_encapsulation_type_t = enum__sai_erspan_encapsulation_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 62

enum__sai_mirror_session_congestion_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 75

SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 75

SAI_MIRROR_SESSION_CONGESTION_MODE_CORRELATED = (SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 75

sai_mirror_session_congestion_mode_t = enum__sai_mirror_session_congestion_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 75

enum__sai_mirror_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_TYPE = SAI_MIRROR_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_MONITOR_PORT = (SAI_MIRROR_SESSION_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE = (SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE = (SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_TC = (SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_VLAN_TPID = (SAI_MIRROR_SESSION_ATTR_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_VLAN_ID = (SAI_MIRROR_SESSION_ATTR_VLAN_TPID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_VLAN_PRI = (SAI_MIRROR_SESSION_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_VLAN_CFI = (SAI_MIRROR_SESSION_ATTR_VLAN_PRI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID = (SAI_MIRROR_SESSION_ATTR_VLAN_CFI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE = (SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION = (SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_TOS = (SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_TTL = (SAI_MIRROR_SESSION_ATTR_TOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS = (SAI_MIRROR_SESSION_ATTR_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS = (SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS = (SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS = (SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE = (SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID = (SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_POLICER = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_END = (SAI_MIRROR_SESSION_ATTR_POLICER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

sai_mirror_session_attr_t = enum__sai_mirror_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 335

sai_create_mirror_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 348

sai_remove_mirror_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 362

sai_set_mirror_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 374

sai_get_mirror_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 388

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 403
class struct__sai_mirror_api_t(Structure):
    pass

struct__sai_mirror_api_t.__slots__ = [
    'create_mirror_session',
    'remove_mirror_session',
    'set_mirror_session_attribute',
    'get_mirror_session_attribute',
]
struct__sai_mirror_api_t._fields_ = [
    ('create_mirror_session', sai_create_mirror_session_fn),
    ('remove_mirror_session', sai_remove_mirror_session_fn),
    ('set_mirror_session_attribute', sai_set_mirror_session_attribute_fn),
    ('get_mirror_session_attribute', sai_get_mirror_session_attribute_fn),
]

sai_mirror_api_t = struct__sai_mirror_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 403

enum__sai_inseg_entry_psc_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 46

SAI_INSEG_ENTRY_PSC_TYPE_ELSP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 46

SAI_INSEG_ENTRY_PSC_TYPE_LLSP = (SAI_INSEG_ENTRY_PSC_TYPE_ELSP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 46

sai_inseg_entry_psc_type_t = enum__sai_inseg_entry_psc_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 46

enum__sai_inseg_entry_pop_ttl_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 63

SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 63

SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE = (SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 63

sai_inseg_entry_pop_ttl_mode_t = enum__sai_inseg_entry_pop_ttl_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 63

enum__sai_inseg_entry_pop_qos_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 80

SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 80

SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE = (SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 80

sai_inseg_entry_pop_qos_mode_t = enum__sai_inseg_entry_pop_qos_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 80

enum__sai_inseg_entry_configured_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 93

SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 93

SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY = (SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 93

sai_inseg_entry_configured_role_t = enum__sai_inseg_entry_configured_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 93

enum__sai_inseg_entry_observed_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 106

SAI_INSEG_ENTRY_OBSERVED_ROLE_ACTIVE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 106

SAI_INSEG_ENTRY_OBSERVED_ROLE_INACTIVE = (SAI_INSEG_ENTRY_OBSERVED_ROLE_ACTIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 106

sai_inseg_entry_observed_role_t = enum__sai_inseg_entry_observed_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 106

enum__sai_inseg_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_NUM_OF_POP = SAI_INSEG_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_PACKET_ACTION = (SAI_INSEG_ENTRY_ATTR_NUM_OF_POP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY = (SAI_INSEG_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID = (SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_PSC_TYPE = (SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_QOS_TC = (SAI_INSEG_ENTRY_ATTR_PSC_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP = (SAI_INSEG_ENTRY_ATTR_QOS_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP = (SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE = (SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE = (SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID = (SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP = (SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE = (SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE = (SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD = (SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_END = (SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

sai_inseg_entry_attr_t = enum__sai_inseg_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 290

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 309
class struct__sai_inseg_entry_t(Structure):
    pass

struct__sai_inseg_entry_t.__slots__ = [
    'switch_id',
    'label',
]
struct__sai_inseg_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('label', sai_label_id_t),
]

sai_inseg_entry_t = struct__sai_inseg_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 309

sai_create_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 320

sai_remove_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 332

sai_set_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 343

sai_get_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 356

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 371
class struct__sai_mpls_api_t(Structure):
    pass

struct__sai_mpls_api_t.__slots__ = [
    'create_inseg_entry',
    'remove_inseg_entry',
    'set_inseg_entry_attribute',
    'get_inseg_entry_attribute',
]
struct__sai_mpls_api_t._fields_ = [
    ('create_inseg_entry', sai_create_inseg_entry_fn),
    ('remove_inseg_entry', sai_remove_inseg_entry_fn),
    ('set_inseg_entry_attribute', sai_set_inseg_entry_attribute_fn),
    ('get_inseg_entry_attribute', sai_get_inseg_entry_attribute_fn),
]

sai_mpls_api_t = struct__sai_mpls_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 371

enum__sai_neighbor_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS = SAI_NEIGHBOR_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION = (SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID = (SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE = (SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_META_DATA = (SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID = (SAI_NEIGHBOR_ENTRY_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_END = (SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

sai_neighbor_entry_attr_t = enum__sai_neighbor_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 129

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 155
class struct__sai_neighbor_entry_t(Structure):
    pass

struct__sai_neighbor_entry_t.__slots__ = [
    'switch_id',
    'rif_id',
    'ip_address',
]
struct__sai_neighbor_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('rif_id', sai_object_id_t),
    ('ip_address', sai_ip_address_t),
]

sai_neighbor_entry_t = struct__sai_neighbor_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 155

sai_create_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 168

sai_remove_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 182

sai_set_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 193

sai_get_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 206

sai_remove_all_neighbor_entries_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 218

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 232
class struct__sai_neighbor_api_t(Structure):
    pass

struct__sai_neighbor_api_t.__slots__ = [
    'create_neighbor_entry',
    'remove_neighbor_entry',
    'set_neighbor_entry_attribute',
    'get_neighbor_entry_attribute',
    'remove_all_neighbor_entries',
]
struct__sai_neighbor_api_t._fields_ = [
    ('create_neighbor_entry', sai_create_neighbor_entry_fn),
    ('remove_neighbor_entry', sai_remove_neighbor_entry_fn),
    ('set_neighbor_entry_attribute', sai_set_neighbor_entry_attribute_fn),
    ('get_neighbor_entry_attribute', sai_get_neighbor_entry_attribute_fn),
    ('remove_all_neighbor_entries', sai_remove_all_neighbor_entries_fn),
]

sai_neighbor_api_t = struct__sai_neighbor_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 232

enum__sai_next_hop_group_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 49

SAI_NEXT_HOP_GROUP_TYPE_ECMP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 49

SAI_NEXT_HOP_GROUP_TYPE_PROTECTION = (SAI_NEXT_HOP_GROUP_TYPE_ECMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 49

sai_next_hop_group_type_t = enum__sai_next_hop_group_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 49

enum__sai_next_hop_group_member_configured_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 62

SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 62

SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY = (SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 62

sai_next_hop_group_member_configured_role_t = enum__sai_next_hop_group_member_configured_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 62

enum__sai_next_hop_group_member_observed_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 75

SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 75

SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE = (SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 75

sai_next_hop_group_member_observed_role_t = enum__sai_next_hop_group_member_observed_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 75

enum__sai_next_hop_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT = SAI_NEXT_HOP_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST = (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_TYPE = (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER = (SAI_NEXT_HOP_GROUP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID = (SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_END = (SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

sai_next_hop_group_attr_t = enum__sai_next_hop_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 147

enum__sai_next_hop_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID = SAI_NEXT_HOP_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_END = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

sai_next_hop_group_member_attr_t = enum__sai_next_hop_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 233

sai_create_next_hop_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 245

sai_remove_next_hop_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 258

sai_set_next_hop_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 269

sai_get_next_hop_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 282

sai_create_next_hop_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 297

sai_remove_next_hop_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 310

sai_set_next_hop_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 321

sai_get_next_hop_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 334

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 354
class struct__sai_next_hop_group_api_t(Structure):
    pass

struct__sai_next_hop_group_api_t.__slots__ = [
    'create_next_hop_group',
    'remove_next_hop_group',
    'set_next_hop_group_attribute',
    'get_next_hop_group_attribute',
    'create_next_hop_group_member',
    'remove_next_hop_group_member',
    'set_next_hop_group_member_attribute',
    'get_next_hop_group_member_attribute',
    'create_next_hop_group_members',
    'remove_next_hop_group_members',
]
struct__sai_next_hop_group_api_t._fields_ = [
    ('create_next_hop_group', sai_create_next_hop_group_fn),
    ('remove_next_hop_group', sai_remove_next_hop_group_fn),
    ('set_next_hop_group_attribute', sai_set_next_hop_group_attribute_fn),
    ('get_next_hop_group_attribute', sai_get_next_hop_group_attribute_fn),
    ('create_next_hop_group_member', sai_create_next_hop_group_member_fn),
    ('remove_next_hop_group_member', sai_remove_next_hop_group_member_fn),
    ('set_next_hop_group_member_attribute', sai_set_next_hop_group_member_attribute_fn),
    ('get_next_hop_group_member_attribute', sai_get_next_hop_group_member_attribute_fn),
    ('create_next_hop_group_members', sai_bulk_object_create_fn),
    ('remove_next_hop_group_members', sai_bulk_object_remove_fn),
]

sai_next_hop_group_api_t = struct__sai_next_hop_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 354

enum__sai_next_hop_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

SAI_NEXT_HOP_TYPE_IP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

SAI_NEXT_HOP_TYPE_MPLS = (SAI_NEXT_HOP_TYPE_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP = (SAI_NEXT_HOP_TYPE_MPLS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

SAI_NEXT_HOP_TYPE_SEGMENTROUTE_SIDLIST = (SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

SAI_NEXT_HOP_TYPE_SEGMENTROUTE_ENDPOINT = (SAI_NEXT_HOP_TYPE_SEGMENTROUTE_SIDLIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

sai_next_hop_type_t = enum__sai_next_hop_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 56

enum__sai_next_hop_endpoint_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_E = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_X = (SAI_NEXT_HOP_ENDPOINT_TYPE_E + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_T = (SAI_NEXT_HOP_ENDPOINT_TYPE_X + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_DX2 = (SAI_NEXT_HOP_ENDPOINT_TYPE_T + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_DX6 = (SAI_NEXT_HOP_ENDPOINT_TYPE_DX2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_DX4 = (SAI_NEXT_HOP_ENDPOINT_TYPE_DX6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_DT6 = (SAI_NEXT_HOP_ENDPOINT_TYPE_DX4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_DT4 = (SAI_NEXT_HOP_ENDPOINT_TYPE_DT6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

SAI_NEXT_HOP_ENDPOINT_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

sai_next_hop_endpoint_type_t = enum__sai_next_hop_endpoint_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 90

enum__sai_next_hop_endpoint_pop_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 103

SAI_NEXT_HOP_ENDPOINT_POP_TYPE_PSP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 103

SAI_NEXT_HOP_ENDPOINT_POP_TYPE_USP = (SAI_NEXT_HOP_ENDPOINT_POP_TYPE_PSP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 103

sai_next_hop_endpoint_pop_type_t = enum__sai_next_hop_endpoint_pop_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 103

enum__sai_next_hop_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_TYPE = SAI_NEXT_HOP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_IP = (SAI_NEXT_HOP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID = (SAI_NEXT_HOP_ATTR_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_TUNNEL_ID = (SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_TUNNEL_VNI = (SAI_NEXT_HOP_ATTR_TUNNEL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_TUNNEL_MAC = (SAI_NEXT_HOP_ATTR_TUNNEL_VNI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID = (SAI_NEXT_HOP_ATTR_TUNNEL_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_TYPE = (SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_POP_TYPE = (SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_LABELSTACK = (SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_POP_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_COUNTER_ID = (SAI_NEXT_HOP_ATTR_LABELSTACK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_DECREMENT_TTL = (SAI_NEXT_HOP_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_OUTSEG_TYPE = (SAI_NEXT_HOP_ATTR_DECREMENT_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE = (SAI_NEXT_HOP_ATTR_OUTSEG_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE = (SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE = (SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE = (SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP = (SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID = (SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID = (SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_END = (SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

sai_next_hop_attr_t = enum__sai_next_hop_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 328

sai_create_next_hop_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 342

sai_remove_next_hop_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 355

sai_set_next_hop_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 366

sai_get_next_hop_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 379

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 394
class struct__sai_next_hop_api_t(Structure):
    pass

struct__sai_next_hop_api_t.__slots__ = [
    'create_next_hop',
    'remove_next_hop',
    'set_next_hop_attribute',
    'get_next_hop_attribute',
]
struct__sai_next_hop_api_t._fields_ = [
    ('create_next_hop', sai_create_next_hop_fn),
    ('remove_next_hop', sai_remove_next_hop_fn),
    ('set_next_hop_attribute', sai_set_next_hop_attribute_fn),
    ('get_next_hop_attribute', sai_get_next_hop_attribute_fn),
]

sai_next_hop_api_t = struct__sai_next_hop_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 394

enum__sai_route_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION = SAI_ROUTE_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID = (SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID = (SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_META_DATA = (SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY = (SAI_ROUTE_ENTRY_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_COUNTER_ID = (SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_END = (SAI_ROUTE_ENTRY_ATTR_COUNTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

sai_route_entry_attr_t = enum__sai_route_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 142

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 168
class struct__sai_route_entry_t(Structure):
    pass

struct__sai_route_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'destination',
]
struct__sai_route_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('destination', sai_ip_prefix_t),
]

sai_route_entry_t = struct__sai_route_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 168

sai_create_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 181

sai_remove_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 195

sai_set_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 206

sai_get_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 219

sai_bulk_create_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_route_entry_t), POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 241

sai_bulk_remove_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_route_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 263

sai_bulk_set_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_route_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 284

sai_bulk_get_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_route_entry_t), POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 308

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 331
class struct__sai_route_api_t(Structure):
    pass

struct__sai_route_api_t.__slots__ = [
    'create_route_entry',
    'remove_route_entry',
    'set_route_entry_attribute',
    'get_route_entry_attribute',
    'create_route_entries',
    'remove_route_entries',
    'set_route_entries_attribute',
    'get_route_entries_attribute',
]
struct__sai_route_api_t._fields_ = [
    ('create_route_entry', sai_create_route_entry_fn),
    ('remove_route_entry', sai_remove_route_entry_fn),
    ('set_route_entry_attribute', sai_set_route_entry_attribute_fn),
    ('get_route_entry_attribute', sai_get_route_entry_attribute_fn),
    ('create_route_entries', sai_bulk_create_route_entry_fn),
    ('remove_route_entries', sai_bulk_remove_route_entry_fn),
    ('set_route_entries_attribute', sai_bulk_set_route_entry_attribute_fn),
    ('get_route_entries_attribute', sai_bulk_get_route_entry_attribute_fn),
]

sai_route_api_t = struct__sai_route_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 331

enum__sai_nat_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

SAI_NAT_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

SAI_NAT_TYPE_SOURCE_NAT = (SAI_NAT_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

SAI_NAT_TYPE_DESTINATION_NAT = (SAI_NAT_TYPE_SOURCE_NAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

SAI_NAT_TYPE_DOUBLE_NAT = (SAI_NAT_TYPE_DESTINATION_NAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

SAI_NAT_TYPE_DESTINATION_NAT_POOL = (SAI_NAT_TYPE_DOUBLE_NAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

sai_nat_type_t = enum__sai_nat_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 56

enum__sai_nat_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_NAT_TYPE = SAI_NAT_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_SRC_IP = (SAI_NAT_ENTRY_ATTR_NAT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_SRC_IP_MASK = (SAI_NAT_ENTRY_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_VR_ID = (SAI_NAT_ENTRY_ATTR_SRC_IP_MASK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_DST_IP = (SAI_NAT_ENTRY_ATTR_VR_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_DST_IP_MASK = (SAI_NAT_ENTRY_ATTR_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_L4_SRC_PORT = (SAI_NAT_ENTRY_ATTR_DST_IP_MASK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_L4_DST_PORT = (SAI_NAT_ENTRY_ATTR_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT = (SAI_NAT_ENTRY_ATTR_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_PACKET_COUNT = (SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT = (SAI_NAT_ENTRY_ATTR_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_BYTE_COUNT = (SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_HIT_BIT_COR = (SAI_NAT_ENTRY_ATTR_BYTE_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_HIT_BIT = (SAI_NAT_ENTRY_ATTR_HIT_BIT_COR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_END = (SAI_NAT_ENTRY_ATTR_HIT_BIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_CUSTOM_DNAT_REROUTE = (SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_NAT_ENTRY_ATTR_CUSTOM_DNAT_REROUTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

sai_nat_entry_attr_t = enum__sai_nat_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 234

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 269
class struct__sai_nat_entry_key_t(Structure):
    pass

struct__sai_nat_entry_key_t.__slots__ = [
    'src_ip',
    'dst_ip',
    'proto',
    'l4_src_port',
    'l4_dst_port',
]
struct__sai_nat_entry_key_t._fields_ = [
    ('src_ip', sai_ip4_t),
    ('dst_ip', sai_ip4_t),
    ('proto', sai_uint8_t),
    ('l4_src_port', sai_uint16_t),
    ('l4_dst_port', sai_uint16_t),
]

sai_nat_entry_key_t = struct__sai_nat_entry_key_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 269

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 301
class struct__sai_nat_entry_mask_t(Structure):
    pass

struct__sai_nat_entry_mask_t.__slots__ = [
    'src_ip',
    'dst_ip',
    'proto',
    'l4_src_port',
    'l4_dst_port',
]
struct__sai_nat_entry_mask_t._fields_ = [
    ('src_ip', sai_ip4_t),
    ('dst_ip', sai_ip4_t),
    ('proto', sai_uint8_t),
    ('l4_src_port', sai_uint16_t),
    ('l4_dst_port', sai_uint16_t),
]

sai_nat_entry_mask_t = struct__sai_nat_entry_mask_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 301

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 315
class struct__sai_nat_entry_data_t(Structure):
    pass

struct__sai_nat_entry_data_t.__slots__ = [
    'key',
    'mask',
]
struct__sai_nat_entry_data_t._fields_ = [
    ('key', sai_nat_entry_key_t),
    ('mask', sai_nat_entry_mask_t),
]

sai_nat_entry_data_t = struct__sai_nat_entry_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 315

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 341
class struct__sai_nat_entry_t(Structure):
    pass

struct__sai_nat_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'data',
]
struct__sai_nat_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('data', sai_nat_entry_data_t),
]

sai_nat_entry_t = struct__sai_nat_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 341

sai_create_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 352

sai_remove_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 364

sai_set_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 375

sai_get_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 388

sai_bulk_create_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_nat_entry_t), POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 410

sai_bulk_remove_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_nat_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 432

sai_bulk_set_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_nat_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 453

sai_bulk_get_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), c_uint32, POINTER(sai_nat_entry_t), POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 477

enum__sai_nat_zone_counter_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_NAT_TYPE = SAI_NAT_ZONE_COUNTER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_ZONE_ID = (SAI_NAT_ZONE_COUNTER_ATTR_NAT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_DISCARD = (SAI_NAT_ZONE_COUNTER_ATTR_ZONE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_DISCARD_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_DISCARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATION_NEEDED = (SAI_NAT_ZONE_COUNTER_ATTR_DISCARD_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATION_NEEDED_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATION_NEEDED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATIONS = (SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATION_NEEDED_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATIONS_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATIONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_END = (SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATIONS_PACKET_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

sai_nat_zone_counter_attr_t = enum__sai_nat_zone_counter_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 578

sai_create_nat_zone_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 590

sai_remove_nat_zone_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 605

sai_set_nat_zone_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 616

sai_get_nat_zone_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 629

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 656
class struct__sai_nat_api_t(Structure):
    pass

struct__sai_nat_api_t.__slots__ = [
    'create_nat_entry',
    'remove_nat_entry',
    'set_nat_entry_attribute',
    'get_nat_entry_attribute',
    'create_nat_entries',
    'remove_nat_entries',
    'set_nat_entries_attribute',
    'get_nat_entries_attribute',
    'create_nat_zone_counter',
    'remove_nat_zone_counter',
    'set_nat_zone_counter_attribute',
    'get_nat_zone_counter_attribute',
]
struct__sai_nat_api_t._fields_ = [
    ('create_nat_entry', sai_create_nat_entry_fn),
    ('remove_nat_entry', sai_remove_nat_entry_fn),
    ('set_nat_entry_attribute', sai_set_nat_entry_attribute_fn),
    ('get_nat_entry_attribute', sai_get_nat_entry_attribute_fn),
    ('create_nat_entries', sai_bulk_create_nat_entry_fn),
    ('remove_nat_entries', sai_bulk_remove_nat_entry_fn),
    ('set_nat_entries_attribute', sai_bulk_set_nat_entry_attribute_fn),
    ('get_nat_entries_attribute', sai_bulk_get_nat_entry_attribute_fn),
    ('create_nat_zone_counter', sai_create_nat_zone_counter_fn),
    ('remove_nat_zone_counter', sai_remove_nat_zone_counter_fn),
    ('set_nat_zone_counter_attribute', sai_set_nat_zone_counter_attribute_fn),
    ('get_nat_zone_counter_attribute', sai_get_nat_zone_counter_attribute_fn),
]

sai_nat_api_t = struct__sai_nat_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 656

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 80
class union__sai_object_key_entry_t(Union):
    pass

union__sai_object_key_entry_t.__slots__ = [
    'object_id',
    'fdb_entry',
    'neighbor_entry',
    'route_entry',
    'mcast_fdb_entry',
    'l2mc_entry',
    'ipmc_entry',
    'inseg_entry',
    'nat_entry',
]
union__sai_object_key_entry_t._fields_ = [
    ('object_id', sai_object_id_t),
    ('fdb_entry', sai_fdb_entry_t),
    ('neighbor_entry', sai_neighbor_entry_t),
    ('route_entry', sai_route_entry_t),
    ('mcast_fdb_entry', sai_mcast_fdb_entry_t),
    ('l2mc_entry', sai_l2mc_entry_t),
    ('ipmc_entry', sai_ipmc_entry_t),
    ('inseg_entry', sai_inseg_entry_t),
    ('nat_entry', sai_nat_entry_t),
]

sai_object_key_entry_t = union__sai_object_key_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 80

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 94
class struct__sai_object_key_t(Structure):
    pass

struct__sai_object_key_t.__slots__ = [
    'key',
]
struct__sai_object_key_t._fields_ = [
    ('key', sai_object_key_entry_t),
]

sai_object_key_t = struct__sai_object_key_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 94

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 115
class struct__sai_attr_capability_t(Structure):
    pass

struct__sai_attr_capability_t.__slots__ = [
    'create_implemented',
    'set_implemented',
    'get_implemented',
]
struct__sai_attr_capability_t._fields_ = [
    ('create_implemented', c_uint8),
    ('set_implemented', c_uint8),
    ('get_implemented', c_uint8),
]

sai_attr_capability_t = struct__sai_attr_capability_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 115

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 126
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_get_maximum_attribute_count'):
        continue
    sai_get_maximum_attribute_count = _lib.sai_get_maximum_attribute_count
    sai_get_maximum_attribute_count.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(c_uint32)]
    sai_get_maximum_attribute_count.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 140
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_get_object_count'):
        continue
    sai_get_object_count = _lib.sai_get_object_count
    sai_get_object_count.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(c_uint32)]
    sai_get_object_count.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 156
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_get_object_key'):
        continue
    sai_get_object_key = _lib.sai_get_object_key
    sai_get_object_key.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(c_uint32), POINTER(sai_object_key_t)]
    sai_get_object_key.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 193
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_bulk_get_attribute'):
        continue
    sai_bulk_get_attribute = _lib.sai_bulk_get_attribute
    sai_bulk_get_attribute.argtypes = [sai_object_id_t, sai_object_type_t, c_uint32, POINTER(sai_object_key_t), POINTER(c_uint32), POINTER(POINTER(sai_attribute_t)), POINTER(sai_status_t)]
    sai_bulk_get_attribute.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 212
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_query_attribute_capability'):
        continue
    sai_query_attribute_capability = _lib.sai_query_attribute_capability
    sai_query_attribute_capability.argtypes = [sai_object_id_t, sai_object_type_t, sai_attr_id_t, POINTER(sai_attr_capability_t)]
    sai_query_attribute_capability.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 228
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_query_attribute_enum_values_capability'):
        continue
    sai_query_attribute_enum_values_capability = _lib.sai_query_attribute_enum_values_capability
    sai_query_attribute_enum_values_capability.argtypes = [sai_object_id_t, sai_object_type_t, sai_attr_id_t, POINTER(sai_s32_list_t)]
    sai_query_attribute_enum_values_capability.restype = sai_status_t
    break

enum__sai_meter_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 50

SAI_METER_TYPE_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 50

SAI_METER_TYPE_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 50

SAI_METER_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 50

sai_meter_type_t = enum__sai_meter_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 50

enum__sai_policer_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

SAI_POLICER_MODE_SR_TCM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

SAI_POLICER_MODE_TR_TCM = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

SAI_POLICER_MODE_STORM_CONTROL = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

SAI_POLICER_MODE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

sai_policer_mode_t = enum__sai_policer_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 69

enum__sai_policer_color_source_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_BLIND = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_AWARE = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 85

sai_policer_color_source_t = enum__sai_policer_color_source_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 85

enum__sai_policer_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_METER_TYPE = SAI_POLICER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_MODE = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_COLOR_SOURCE = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_CBS = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_CIR = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_PBS = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_PIR = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_GREEN_PACKET_ACTION = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_YELLOW_PACKET_ACTION = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_RED_PACKET_ACTION = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_ENABLE_COUNTER_LIST = (SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_END = (SAI_POLICER_ATTR_ENABLE_COUNTER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

SAI_POLICER_ATTR_CUSTOM_RANGE_END = (SAI_POLICER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

sai_policer_attr_t = enum__sai_policer_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 225

enum__sai_policer_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_ATTR_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_GREEN_PACKETS = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_GREEN_BYTES = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_YELLOW_PACKETS = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_YELLOW_BYTES = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_RED_PACKETS = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_RED_BYTES = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

SAI_POLICER_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

sai_policer_stat_t = enum__sai_policer_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 259

sai_create_policer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 271

sai_remove_policer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 284

sai_set_policer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 295

sai_get_policer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 308

sai_get_policer_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 323

sai_get_policer_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 340

sai_clear_policer_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 356

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 374
class struct__sai_policer_api_t(Structure):
    pass

struct__sai_policer_api_t.__slots__ = [
    'create_policer',
    'remove_policer',
    'set_policer_attribute',
    'get_policer_attribute',
    'get_policer_stats',
    'get_policer_stats_ext',
    'clear_policer_stats',
]
struct__sai_policer_api_t._fields_ = [
    ('create_policer', sai_create_policer_fn),
    ('remove_policer', sai_remove_policer_fn),
    ('set_policer_attribute', sai_set_policer_attribute_fn),
    ('get_policer_attribute', sai_get_policer_attribute_fn),
    ('get_policer_stats', sai_get_policer_stats_fn),
    ('get_policer_stats_ext', sai_get_policer_stats_ext_fn),
    ('clear_policer_stats', sai_clear_policer_stats_fn),
]

sai_policer_api_t = struct__sai_policer_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 374

enum__sai_port_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 47

SAI_PORT_TYPE_LOGICAL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 47

SAI_PORT_TYPE_CPU = (SAI_PORT_TYPE_LOGICAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 47

sai_port_type_t = enum__sai_port_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 47

enum__sai_port_oper_status_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

SAI_PORT_OPER_STATUS_UNKNOWN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

SAI_PORT_OPER_STATUS_UP = (SAI_PORT_OPER_STATUS_UNKNOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

SAI_PORT_OPER_STATUS_DOWN = (SAI_PORT_OPER_STATUS_UP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

SAI_PORT_OPER_STATUS_TESTING = (SAI_PORT_OPER_STATUS_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

SAI_PORT_OPER_STATUS_NOT_PRESENT = (SAI_PORT_OPER_STATUS_TESTING + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

sai_port_oper_status_t = enum__sai_port_oper_status_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 69

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 86
class struct__sai_port_oper_status_notification_t(Structure):
    pass

struct__sai_port_oper_status_notification_t.__slots__ = [
    'port_id',
    'port_state',
]
struct__sai_port_oper_status_notification_t._fields_ = [
    ('port_id', sai_object_id_t),
    ('port_state', sai_port_oper_status_t),
]

sai_port_oper_status_notification_t = struct__sai_port_oper_status_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 86

enum__sai_port_flow_control_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

SAI_PORT_FLOW_CONTROL_MODE_DISABLE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY = (SAI_PORT_FLOW_CONTROL_MODE_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY = (SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE = (SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

sai_port_flow_control_mode_t = enum__sai_port_flow_control_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 105

enum__sai_port_internal_loopback_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 121

SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 121

SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY = (SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 121

SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC = (SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 121

sai_port_internal_loopback_mode_t = enum__sai_port_internal_loopback_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 121

enum__sai_port_media_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

SAI_PORT_MEDIA_TYPE_NOT_PRESENT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

SAI_PORT_MEDIA_TYPE_UNKNOWN = (SAI_PORT_MEDIA_TYPE_NOT_PRESENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

SAI_PORT_MEDIA_TYPE_FIBER = (SAI_PORT_MEDIA_TYPE_UNKNOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

SAI_PORT_MEDIA_TYPE_COPPER = (SAI_PORT_MEDIA_TYPE_FIBER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

sai_port_media_type_t = enum__sai_port_media_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 139

enum__sai_port_breakout_mode_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

SAI_PORT_BREAKOUT_MODE_TYPE_2_LANE = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

SAI_PORT_BREAKOUT_MODE_TYPE_MAX = (SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

sai_port_breakout_mode_type_t = enum__sai_port_breakout_mode_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 158

enum__sai_port_fec_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 173

SAI_PORT_FEC_MODE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 173

SAI_PORT_FEC_MODE_RS = (SAI_PORT_FEC_MODE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 173

SAI_PORT_FEC_MODE_FC = (SAI_PORT_FEC_MODE_RS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 173

sai_port_fec_mode_t = enum__sai_port_fec_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 173

enum__sai_port_priority_flow_control_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 186

SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 186

SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE = (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 186

sai_port_priority_flow_control_mode_t = enum__sai_port_priority_flow_control_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 186

enum__sai_port_ptp_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 202

SAI_PORT_PTP_MODE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 202

SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP = (SAI_PORT_PTP_MODE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 202

SAI_PORT_PTP_MODE_TWO_STEP_TIMESTAMP = (SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 202

sai_port_ptp_mode_t = enum__sai_port_ptp_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 202

enum__sai_port_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_TYPE = SAI_PORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_OPER_STATUS = (SAI_PORT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE = (SAI_PORT_ATTR_OPER_STATUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE = (SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES = (SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_QUEUE_LIST = (SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS = (SAI_PORT_ATTR_QOS_QUEUE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST = (SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_SPEED = (SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_FEC_MODE = (SAI_PORT_ATTR_SUPPORTED_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_SUPPORTED_FEC_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE = (SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE = (SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED = (SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS = (SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST = (SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EYE_VALUES = (SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_OPER_SPEED = (SAI_PORT_ATTR_EYE_VALUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_HW_LANE_LIST = (SAI_PORT_ATTR_OPER_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SPEED = (SAI_PORT_ATTR_HW_LANE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_FULL_DUPLEX_MODE = (SAI_PORT_ATTR_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_AUTO_NEG_MODE = (SAI_PORT_ATTR_FULL_DUPLEX_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADMIN_STATE = (SAI_PORT_ATTR_AUTO_NEG_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_MEDIA_TYPE = (SAI_PORT_ATTR_ADMIN_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_SPEED = (SAI_PORT_ATTR_MEDIA_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_FEC_MODE = (SAI_PORT_ATTR_ADVERTISED_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_ADVERTISED_FEC_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE = (SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE = (SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ADVERTISED_OUI_CODE = (SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PORT_VLAN_ID = (SAI_PORT_ATTR_ADVERTISED_OUI_CODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = (SAI_PORT_ATTR_PORT_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_DROP_UNTAGGED = (SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_DROP_TAGGED = (SAI_PORT_ATTR_DROP_UNTAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE = (SAI_PORT_ATTR_DROP_TAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_FEC_MODE = (SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_UPDATE_DSCP = (SAI_PORT_ATTR_FEC_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_MTU = (SAI_PORT_ATTR_UPDATE_DSCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_INGRESS_ACL = (SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EGRESS_ACL = (SAI_PORT_ATTR_INGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_INGRESS_MIRROR_SESSION = (SAI_PORT_ATTR_EGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EGRESS_MIRROR_SESSION = (SAI_PORT_ATTR_INGRESS_MIRROR_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = (SAI_PORT_ATTR_EGRESS_MIRROR_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE = (SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_POLICER_ID = (SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_DEFAULT_TC = (SAI_PORT_ATTR_POLICER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = (SAI_PORT_ATTR_QOS_DEFAULT_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = (SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = (SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = (SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP = (SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = (SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP = (SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP = (SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP = (SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID = (SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST = (SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST = (SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_META_DATA = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST = (SAI_PORT_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_HW_PROFILE_ID = (SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EEE_ENABLE = (SAI_PORT_ATTR_HW_PROFILE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EEE_IDLE_TIME = (SAI_PORT_ATTR_EEE_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_EEE_WAKE_TIME = (SAI_PORT_ATTR_EEE_IDLE_TIME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PORT_POOL_LIST = (SAI_PORT_ATTR_EEE_WAKE_TIME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ISOLATION_GROUP = (SAI_PORT_ATTR_PORT_POOL_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PKT_TX_ENABLE = (SAI_PORT_ATTR_ISOLATION_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_TAM_OBJECT = (SAI_PORT_ATTR_PKT_TX_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SERDES_PREEMPHASIS = (SAI_PORT_ATTR_TAM_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SERDES_IDRIVER = (SAI_PORT_ATTR_SERDES_PREEMPHASIS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_SERDES_IPREDRIVER = (SAI_PORT_ATTR_SERDES_IDRIVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_LINK_TRAINING_ENABLE = (SAI_PORT_ATTR_SERDES_IPREDRIVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PTP_MODE = (SAI_PORT_ATTR_LINK_TRAINING_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY = (SAI_PORT_ATTR_PTP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY = (SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PTP_PATH_DELAY = (SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PTP_DOMAIN_ID = (SAI_PORT_ATTR_PTP_PATH_DELAY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_PORT_SERDES_ID = (SAI_PORT_ATTR_PTP_DOMAIN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_ES = (SAI_PORT_ATTR_PORT_SERDES_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_Y1731_ENABLE = (SAI_PORT_ATTR_ES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_Y1731_LM_ENABLE = (SAI_PORT_ATTR_Y1731_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_Y1731_MIP_ENABLE = (SAI_PORT_ATTR_Y1731_LM_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_MAC_ADDRESS = (SAI_PORT_ATTR_Y1731_MIP_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_END = (SAI_PORT_ATTR_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

SAI_PORT_ATTR_CUSTOM_RANGE_END = (SAI_PORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

sai_port_attr_t = enum__sai_port_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1319

enum__sai_port_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_UCAST_PKTS = (SAI_PORT_STAT_IF_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IF_IN_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_DISCARDS = (SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_ERRORS = (SAI_PORT_STAT_IF_IN_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_UNKNOWN_PROTOS = (SAI_PORT_STAT_IF_IN_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_BROADCAST_PKTS = (SAI_PORT_STAT_IF_IN_UNKNOWN_PROTOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_MULTICAST_PKTS = (SAI_PORT_STAT_IF_IN_BROADCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_IN_VLAN_DISCARDS = (SAI_PORT_STAT_IF_IN_MULTICAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_OCTETS = (SAI_PORT_STAT_IF_IN_VLAN_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_UCAST_PKTS = (SAI_PORT_STAT_IF_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IF_OUT_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_DISCARDS = (SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_ERRORS = (SAI_PORT_STAT_IF_OUT_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_QLEN = (SAI_PORT_STAT_IF_OUT_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS = (SAI_PORT_STAT_IF_OUT_QLEN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS = (SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS = (SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS = (SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS = (SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_UNDERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_FRAGMENTS = (SAI_PORT_STAT_ETHER_STATS_UNDERSIZE_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS = (SAI_PORT_STAT_ETHER_STATS_FRAGMENTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_2048_TO_4095_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_4096_TO_9216_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_PKTS_9217_TO_16383_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_OVERSIZE_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_TX_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_JABBERS = (SAI_PORT_STAT_ETHER_TX_OVERSIZE_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_OCTETS = (SAI_PORT_STAT_ETHER_STATS_JABBERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_PKTS = (SAI_PORT_STAT_ETHER_STATS_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_COLLISIONS = (SAI_PORT_STAT_ETHER_STATS_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS = (SAI_PORT_STAT_ETHER_STATS_COLLISIONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS = (SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS = (SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_IN_RECEIVES = (SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_IN_OCTETS = (SAI_PORT_STAT_IP_IN_RECEIVES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_IN_UCAST_PKTS = (SAI_PORT_STAT_IP_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IP_IN_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_IN_DISCARDS = (SAI_PORT_STAT_IP_IN_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_OUT_OCTETS = (SAI_PORT_STAT_IP_IN_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_OUT_UCAST_PKTS = (SAI_PORT_STAT_IP_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IP_OUT_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IP_OUT_DISCARDS = (SAI_PORT_STAT_IP_OUT_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_RECEIVES = (SAI_PORT_STAT_IP_OUT_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_OCTETS = (SAI_PORT_STAT_IPV6_IN_RECEIVES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_UCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_MCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_IN_DISCARDS = (SAI_PORT_STAT_IPV6_IN_MCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_OUT_OCTETS = (SAI_PORT_STAT_IPV6_IN_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_OUT_UCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_OUT_MCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IPV6_OUT_DISCARDS = (SAI_PORT_STAT_IPV6_OUT_MCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_GREEN_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_IPV6_OUT_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_GREEN_WRED_DROPPED_BYTES = (SAI_PORT_STAT_GREEN_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_YELLOW_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_GREEN_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_YELLOW_WRED_DROPPED_BYTES = (SAI_PORT_STAT_YELLOW_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_RED_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_YELLOW_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_RED_WRED_DROPPED_BYTES = (SAI_PORT_STAT_RED_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_RED_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_WRED_DROPPED_BYTES = (SAI_PORT_STAT_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ECN_MARKED_PACKETS = (SAI_PORT_STAT_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS = (SAI_PORT_STAT_ECN_MARKED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_2048_TO_4095_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_IN_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_4096_TO_9216_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_9217_TO_16383_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_2048_TO_4095_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_ETHER_OUT_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_4096_TO_9216_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_ETHER_OUT_PKTS_9217_TO_16383_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_WATERMARK_BYTES = (SAI_PORT_STAT_IN_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_IN_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_SHARED_WATERMARK_BYTES = (SAI_PORT_STAT_IN_SHARED_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_IN_SHARED_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_WATERMARK_BYTES = (SAI_PORT_STAT_OUT_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_OUT_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_SHARED_WATERMARK_BYTES = (SAI_PORT_STAT_OUT_SHARED_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_DROPPED_PKTS = (SAI_PORT_STAT_OUT_SHARED_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_DROPPED_PKTS = (SAI_PORT_STAT_IN_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PAUSE_RX_PKTS = (SAI_PORT_STAT_OUT_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PAUSE_TX_PKTS = (SAI_PORT_STAT_PAUSE_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_0_RX_PKTS = (SAI_PORT_STAT_PAUSE_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_0_TX_PKTS = (SAI_PORT_STAT_PFC_0_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_1_RX_PKTS = (SAI_PORT_STAT_PFC_0_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_1_TX_PKTS = (SAI_PORT_STAT_PFC_1_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_2_RX_PKTS = (SAI_PORT_STAT_PFC_1_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_2_TX_PKTS = (SAI_PORT_STAT_PFC_2_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_3_RX_PKTS = (SAI_PORT_STAT_PFC_2_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_3_TX_PKTS = (SAI_PORT_STAT_PFC_3_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_4_RX_PKTS = (SAI_PORT_STAT_PFC_3_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_4_TX_PKTS = (SAI_PORT_STAT_PFC_4_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_5_RX_PKTS = (SAI_PORT_STAT_PFC_4_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_5_TX_PKTS = (SAI_PORT_STAT_PFC_5_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_6_RX_PKTS = (SAI_PORT_STAT_PFC_5_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_6_TX_PKTS = (SAI_PORT_STAT_PFC_6_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_7_RX_PKTS = (SAI_PORT_STAT_PFC_6_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_7_TX_PKTS = (SAI_PORT_STAT_PFC_7_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_7_TX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_0_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_1_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_0_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_2_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_1_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_3_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_2_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_4_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_3_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_5_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_4_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_6_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_5_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_PFC_7_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_6_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_ALIGNMENT_ERRORS = (SAI_PORT_STAT_PFC_7_ON2OFF_RX_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_FCS_ERRORS = (SAI_PORT_STAT_DOT3_STATS_ALIGNMENT_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_SINGLE_COLLISION_FRAMES = (SAI_PORT_STAT_DOT3_STATS_FCS_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_MULTIPLE_COLLISION_FRAMES = (SAI_PORT_STAT_DOT3_STATS_SINGLE_COLLISION_FRAMES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_SQE_TEST_ERRORS = (SAI_PORT_STAT_DOT3_STATS_MULTIPLE_COLLISION_FRAMES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_DEFERRED_TRANSMISSIONS = (SAI_PORT_STAT_DOT3_STATS_SQE_TEST_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_LATE_COLLISIONS = (SAI_PORT_STAT_DOT3_STATS_DEFERRED_TRANSMISSIONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_EXCESSIVE_COLLISIONS = (SAI_PORT_STAT_DOT3_STATS_LATE_COLLISIONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_TRANSMIT_ERRORS = (SAI_PORT_STAT_DOT3_STATS_EXCESSIVE_COLLISIONS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_CARRIER_SENSE_ERRORS = (SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_TRANSMIT_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_FRAME_TOO_LONGS = (SAI_PORT_STAT_DOT3_STATS_CARRIER_SENSE_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_RECEIVE_ERRORS = (SAI_PORT_STAT_DOT3_STATS_FRAME_TOO_LONGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_STATS_SYMBOL_ERRORS = (SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_RECEIVE_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_DOT3_CONTROL_IN_UNKNOWN_OPCODES = (SAI_PORT_STAT_DOT3_STATS_SYMBOL_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_EEE_TX_EVENT_COUNT = (SAI_PORT_STAT_DOT3_CONTROL_IN_UNKNOWN_OPCODES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_EEE_RX_EVENT_COUNT = (SAI_PORT_STAT_EEE_TX_EVENT_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_EEE_TX_DURATION = (SAI_PORT_STAT_EEE_RX_EVENT_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_EEE_RX_DURATION = (SAI_PORT_STAT_EEE_TX_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_IN_DROP_REASON_RANGE_END = 8191 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE = 8192 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END = 12287 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

sai_port_stat_t = enum__sai_port_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1886

enum__sai_signal_degrade_status_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1896

SAI_PORT_SD_STATUS_DETECT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1896

SAI_PORT_SD_STATUS_RECOVER = (SAI_PORT_SD_STATUS_DETECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1896

sai_signal_degrade_status_t = enum__sai_signal_degrade_status_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1896

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1913
class struct__sai_port_sd_notification_t(Structure):
    pass

struct__sai_port_sd_notification_t.__slots__ = [
    'port_id',
    'sd_status',
]
struct__sai_port_sd_notification_t._fields_ = [
    ('port_id', sai_object_id_t),
    ('sd_status', sai_signal_degrade_status_t),
]

sai_port_sd_notification_t = struct__sai_port_sd_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1913

sai_signal_degrade_event_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_port_sd_notification_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1921

sai_create_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1935

sai_remove_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1948

sai_set_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1959

sai_get_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1972

sai_get_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1987

sai_get_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2004

sai_clear_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2020

sai_clear_port_all_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2032

sai_port_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_port_oper_status_notification_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2045

enum__sai_port_pool_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_PORT_ID = SAI_PORT_POOL_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_BUFFER_POOL_ID = (SAI_PORT_POOL_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_QOS_WRED_PROFILE_ID = (SAI_PORT_POOL_ATTR_BUFFER_POOL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_END = (SAI_PORT_POOL_ATTR_QOS_WRED_PROFILE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

SAI_PORT_POOL_ATTR_CUSTOM_RANGE_END = (SAI_PORT_POOL_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

sai_port_pool_attr_t = enum__sai_port_pool_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2106

enum__sai_port_pool_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_IF_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_IF_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_RED_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_RED_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_RED_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_RED_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_WRED_DROPPED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_WRED_DROPPED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_WRED_ECN_MARKED_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_CURR_OCCUPANCY_BYTES = (SAI_PORT_POOL_STAT_WRED_ECN_MARKED_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_WATERMARK_BYTES = (SAI_PORT_POOL_STAT_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_POOL_STAT_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_SHARED_WATERMARK_BYTES = (SAI_PORT_POOL_STAT_SHARED_CURR_OCCUPANCY_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

SAI_PORT_POOL_STAT_DROPPED_PKTS = (SAI_PORT_POOL_STAT_SHARED_WATERMARK_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

sai_port_pool_stat_t = enum__sai_port_pool_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2179

sai_create_port_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2191

sai_remove_port_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2204

sai_set_port_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2215

sai_get_port_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2228

sai_get_port_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2243

sai_get_port_pool_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2260

sai_clear_port_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2276

enum__sai_port_serdes_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_PORT_ID = SAI_PORT_SERDES_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_PREEMPHASIS = (SAI_PORT_SERDES_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_IDRIVER = (SAI_PORT_SERDES_ATTR_PREEMPHASIS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_IPREDRIVER = (SAI_PORT_SERDES_ATTR_IDRIVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_PRE1 = (SAI_PORT_SERDES_ATTR_IPREDRIVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_PRE2 = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_PRE3 = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_MAIN = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE3 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_POST1 = (SAI_PORT_SERDES_ATTR_TX_FIR_MAIN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_POST2 = (SAI_PORT_SERDES_ATTR_TX_FIR_POST1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_POST3 = (SAI_PORT_SERDES_ATTR_TX_FIR_POST2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_TX_FIR_ATTN = (SAI_PORT_SERDES_ATTR_TX_FIR_POST3 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_END = (SAI_PORT_SERDES_ATTR_TX_FIR_ATTN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_END = (SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

sai_port_serdes_attr_t = enum__sai_port_serdes_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2454

sai_create_port_serdes_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2466

sai_remove_port_serdes_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2479

sai_set_port_serdes_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2490

sai_get_port_serdes_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2503

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2533
class struct__sai_port_api_t(Structure):
    pass

struct__sai_port_api_t.__slots__ = [
    'create_port',
    'remove_port',
    'set_port_attribute',
    'get_port_attribute',
    'get_port_stats',
    'get_port_stats_ext',
    'clear_port_stats',
    'clear_port_all_stats',
    'create_port_pool',
    'remove_port_pool',
    'set_port_pool_attribute',
    'get_port_pool_attribute',
    'get_port_pool_stats',
    'get_port_pool_stats_ext',
    'clear_port_pool_stats',
    'create_port_serdes',
    'remove_port_serdes',
    'set_port_serdes_attribute',
    'get_port_serdes_attribute',
]
struct__sai_port_api_t._fields_ = [
    ('create_port', sai_create_port_fn),
    ('remove_port', sai_remove_port_fn),
    ('set_port_attribute', sai_set_port_attribute_fn),
    ('get_port_attribute', sai_get_port_attribute_fn),
    ('get_port_stats', sai_get_port_stats_fn),
    ('get_port_stats_ext', sai_get_port_stats_ext_fn),
    ('clear_port_stats', sai_clear_port_stats_fn),
    ('clear_port_all_stats', sai_clear_port_all_stats_fn),
    ('create_port_pool', sai_create_port_pool_fn),
    ('remove_port_pool', sai_remove_port_pool_fn),
    ('set_port_pool_attribute', sai_set_port_pool_attribute_fn),
    ('get_port_pool_attribute', sai_get_port_pool_attribute_fn),
    ('get_port_pool_stats', sai_get_port_pool_stats_fn),
    ('get_port_pool_stats_ext', sai_get_port_pool_stats_ext_fn),
    ('clear_port_pool_stats', sai_clear_port_pool_stats_fn),
    ('create_port_serdes', sai_create_port_serdes_fn),
    ('remove_port_serdes', sai_remove_port_serdes_fn),
    ('set_port_serdes_attribute', sai_set_port_serdes_attribute_fn),
    ('get_port_serdes_attribute', sai_get_port_serdes_attribute_fn),
]

sai_port_api_t = struct__sai_port_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2533

enum__sai_qos_map_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_DOT1P_TO_TC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_DSCP_TO_TC = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_DSCP_TO_COLOR = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_TC_TO_QUEUE = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_TC_TO_PRIORITY_GROUP = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_PRIORITY_GROUP = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_QUEUE = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

SAI_QOS_MAP_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

sai_qos_map_type_t = enum__sai_qos_map_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 83

enum__sai_qos_map_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_TYPE = SAI_QOS_MAP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_END = (SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

SAI_QOS_MAP_ATTR_CUSTOM_RANGE_END = (SAI_QOS_MAP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

sai_qos_map_attr_t = enum__sai_qos_map_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 127

sai_create_qos_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 139

sai_remove_qos_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 152

sai_set_qos_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 163

sai_get_qos_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 176

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 191
class struct__sai_qos_map_api_t(Structure):
    pass

struct__sai_qos_map_api_t.__slots__ = [
    'create_qos_map',
    'remove_qos_map',
    'set_qos_map_attribute',
    'get_qos_map_attribute',
]
struct__sai_qos_map_api_t._fields_ = [
    ('create_qos_map', sai_create_qos_map_fn),
    ('remove_qos_map', sai_remove_qos_map_fn),
    ('set_qos_map_attribute', sai_set_qos_map_attribute_fn),
    ('get_qos_map_attribute', sai_get_qos_map_attribute_fn),
]

sai_qos_map_api_t = struct__sai_qos_map_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 191

enum__sai_queue_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

SAI_QUEUE_TYPE_ALL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

SAI_QUEUE_TYPE_UNICAST = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

SAI_QUEUE_TYPE_MULTICAST = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

SAI_QUEUE_TYPE_SERVICE = (SAI_QUEUE_TYPE_MULTICAST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

SAI_QUEUE_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

sai_queue_type_t = enum__sai_queue_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 56

enum__sai_queue_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_TYPE = SAI_QUEUE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_PORT = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_INDEX = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_WRED_PROFILE_ID = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_BUFFER_PROFILE_ID = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_PAUSE_STATUS = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_ENABLE_PFC_DLDR = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_PFC_DLR_INIT = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_TAM_OBJECT = (SAI_QUEUE_ATTR_PFC_DLR_INIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_END = (SAI_QUEUE_ATTR_TAM_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_SERVICE_ID = SAI_QUEUE_ATTR_CUSTOM_RANGE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

SAI_QUEUE_ATTR_CUSTOM_RANGE_END = (SAI_QUEUE_ATTR_SERVICE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

sai_queue_attr_t = enum__sai_queue_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 213

enum__sai_queue_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_BYTES = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_DROPPED_PACKETS = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_DROPPED_BYTES = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_PACKETS = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_BYTES = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_DROPPED_PACKETS = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_DROPPED_BYTES = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_PACKETS = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_BYTES = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_DROPPED_PACKETS = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_DROPPED_BYTES = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_PACKETS = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_BYTES = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_DROPPED_PACKETS = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_DROPPED_BYTES = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_WRED_DROPPED_PACKETS = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_WRED_DROPPED_BYTES = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_PACKETS = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_BYTES = 19 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_WRED_DROPPED_PACKETS = 20 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_WRED_DROPPED_BYTES = 21 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_WRED_DROPPED_PACKETS = 22 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_WRED_DROPPED_BYTES = 23 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_CURR_OCCUPANCY_BYTES = 24 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_WATERMARK_BYTES = 25 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_SHARED_CURR_OCCUPANCY_BYTES = 26 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_SHARED_WATERMARK_BYTES = 27 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_PACKETS = 28 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_BYTES = 29 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = 30 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_BYTES = 31 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_PACKETS = 32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_BYTES = 33 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_WRED_ECN_MARKED_PACKETS = 34 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_WRED_ECN_MARKED_BYTES = 35 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

SAI_QUEUE_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

sai_queue_stat_t = enum__sai_queue_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 331

enum__sai_queue_pfc_deadlock_event_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 344

SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_DETECTED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 344

SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_RECOVERED = (SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_DETECTED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 344

sai_queue_pfc_deadlock_event_type_t = enum__sai_queue_pfc_deadlock_event_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 344

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 372
class struct__sai_queue_deadlock_notification_data_t(Structure):
    pass

struct__sai_queue_deadlock_notification_data_t.__slots__ = [
    'queue_id',
    'event',
    'app_managed_recovery',
]
struct__sai_queue_deadlock_notification_data_t._fields_ = [
    ('queue_id', sai_object_id_t),
    ('event', sai_queue_pfc_deadlock_event_type_t),
    ('app_managed_recovery', c_uint8),
]

sai_queue_deadlock_notification_data_t = struct__sai_queue_deadlock_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 372

sai_create_queue_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 384

sai_remove_queue_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 397

sai_set_queue_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 408

sai_get_queue_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 421

sai_get_queue_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 436

sai_get_queue_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 453

sai_clear_queue_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 469

sai_queue_pfc_deadlock_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_queue_deadlock_notification_data_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 484

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 501
class struct__sai_queue_api_t(Structure):
    pass

struct__sai_queue_api_t.__slots__ = [
    'create_queue',
    'remove_queue',
    'set_queue_attribute',
    'get_queue_attribute',
    'get_queue_stats',
    'get_queue_stats_ext',
    'clear_queue_stats',
]
struct__sai_queue_api_t._fields_ = [
    ('create_queue', sai_create_queue_fn),
    ('remove_queue', sai_remove_queue_fn),
    ('set_queue_attribute', sai_set_queue_attribute_fn),
    ('get_queue_attribute', sai_get_queue_attribute_fn),
    ('get_queue_stats', sai_get_queue_stats_fn),
    ('get_queue_stats_ext', sai_get_queue_stats_ext_fn),
    ('clear_queue_stats', sai_clear_queue_stats_fn),
]

sai_queue_api_t = struct__sai_queue_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 501

enum__sai_router_interface_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_VLAN = (SAI_ROUTER_INTERFACE_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_LOOPBACK = (SAI_ROUTER_INTERFACE_TYPE_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER = (SAI_ROUTER_INTERFACE_TYPE_LOOPBACK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_SUB_PORT = (SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_BRIDGE = (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT = (SAI_ROUTER_INTERFACE_TYPE_BRIDGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

sai_router_interface_type_t = enum__sai_router_interface_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 62

enum__sai_router_interface_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID = SAI_ROUTER_INTERFACE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_TYPE = (SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_PORT_ID = (SAI_ROUTER_INTERFACE_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID = (SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS = (SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE = (SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE = (SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_MTU = (SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL = (SAI_ROUTER_INTERFACE_ATTR_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL = (SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION = (SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE = (SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE = (SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION = (SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL = (SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID = (SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_END = (SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE = (SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_END = (SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

sai_router_interface_attr_t = enum__sai_router_interface_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 300

enum__sai_router_interface_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_IN_PACKETS = (SAI_ROUTER_INTERFACE_STAT_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS = (SAI_ROUTER_INTERFACE_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS = (SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_IN_ERROR_OCTETS = (SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_IN_ERROR_PACKETS = (SAI_ROUTER_INTERFACE_STAT_IN_ERROR_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_OCTETS = (SAI_ROUTER_INTERFACE_STAT_IN_ERROR_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_PACKETS = (SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

sai_router_interface_stat_t = enum__sai_router_interface_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 331

sai_create_router_interface_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 343

sai_remove_router_interface_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 356

sai_set_router_interface_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 367

sai_get_router_interface_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 380

sai_get_router_interface_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 395

sai_get_router_interface_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 412

sai_clear_router_interface_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 428

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 446
class struct__sai_router_interface_api_t(Structure):
    pass

struct__sai_router_interface_api_t.__slots__ = [
    'create_router_interface',
    'remove_router_interface',
    'set_router_interface_attribute',
    'get_router_interface_attribute',
    'get_router_interface_stats',
    'get_router_interface_stats_ext',
    'clear_router_interface_stats',
]
struct__sai_router_interface_api_t._fields_ = [
    ('create_router_interface', sai_create_router_interface_fn),
    ('remove_router_interface', sai_remove_router_interface_fn),
    ('set_router_interface_attribute', sai_set_router_interface_attribute_fn),
    ('get_router_interface_attribute', sai_get_router_interface_attribute_fn),
    ('get_router_interface_stats', sai_get_router_interface_stats_fn),
    ('get_router_interface_stats_ext', sai_get_router_interface_stats_ext_fn),
    ('clear_router_interface_stats', sai_clear_router_interface_stats_fn),
]

sai_router_interface_api_t = struct__sai_router_interface_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 446

enum__sai_rpf_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT = SAI_RPF_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST = (SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_END = (SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

sai_rpf_group_attr_t = enum__sai_rpf_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 74

enum__sai_rpf_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID = SAI_RPF_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID = (SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_END = (SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

sai_rpf_group_member_attr_t = enum__sai_rpf_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 112

sai_create_rpf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 124

sai_remove_rpf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 137

sai_set_rpf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 148

sai_get_rpf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 161

sai_create_rpf_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 176

sai_remove_rpf_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 189

sai_set_rpf_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 200

sai_get_rpf_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 213

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 232
class struct__sai_rpf_group_api_t(Structure):
    pass

struct__sai_rpf_group_api_t.__slots__ = [
    'create_rpf_group',
    'remove_rpf_group',
    'set_rpf_group_attribute',
    'get_rpf_group_attribute',
    'create_rpf_group_member',
    'remove_rpf_group_member',
    'set_rpf_group_member_attribute',
    'get_rpf_group_member_attribute',
]
struct__sai_rpf_group_api_t._fields_ = [
    ('create_rpf_group', sai_create_rpf_group_fn),
    ('remove_rpf_group', sai_remove_rpf_group_fn),
    ('set_rpf_group_attribute', sai_set_rpf_group_attribute_fn),
    ('get_rpf_group_attribute', sai_get_rpf_group_attribute_fn),
    ('create_rpf_group_member', sai_create_rpf_group_member_fn),
    ('remove_rpf_group_member', sai_remove_rpf_group_member_fn),
    ('set_rpf_group_member_attribute', sai_set_rpf_group_member_attribute_fn),
    ('get_rpf_group_member_attribute', sai_get_rpf_group_member_attribute_fn),
]

sai_rpf_group_api_t = struct__sai_rpf_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 232

enum__sai_samplepacket_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 44

SAI_SAMPLEPACKET_TYPE_SLOW_PATH = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 44

sai_samplepacket_type_t = enum__sai_samplepacket_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 44

enum__sai_samplepacket_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 71

SAI_SAMPLEPACKET_MODE_EXCLUSIVE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 71

SAI_SAMPLEPACKET_MODE_SHARED = (SAI_SAMPLEPACKET_MODE_EXCLUSIVE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 71

sai_samplepacket_mode_t = enum__sai_samplepacket_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 71

enum__sai_samplepacket_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE = SAI_SAMPLEPACKET_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_TYPE = (SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_MODE = (SAI_SAMPLEPACKET_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_END = (SAI_SAMPLEPACKET_ATTR_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_END = (SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

sai_samplepacket_attr_t = enum__sai_samplepacket_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 125

sai_create_samplepacket_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 138

sai_remove_samplepacket_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 152

sai_set_samplepacket_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 164

sai_get_samplepacket_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 178

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 193
class struct__sai_samplepacket_api_t(Structure):
    pass

struct__sai_samplepacket_api_t.__slots__ = [
    'create_samplepacket',
    'remove_samplepacket',
    'set_samplepacket_attribute',
    'get_samplepacket_attribute',
]
struct__sai_samplepacket_api_t._fields_ = [
    ('create_samplepacket', sai_create_samplepacket_fn),
    ('remove_samplepacket', sai_remove_samplepacket_fn),
    ('set_samplepacket_attribute', sai_set_samplepacket_attribute_fn),
    ('get_samplepacket_attribute', sai_get_samplepacket_attribute_fn),
]

sai_samplepacket_api_t = struct__sai_samplepacket_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 193

enum__sai_scheduler_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT = SAI_SCHEDULER_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_PORT_ID = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_LEVEL = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_END = (SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID = SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

sai_scheduler_group_attr_t = enum__sai_scheduler_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 137

sai_create_scheduler_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 149

sai_remove_scheduler_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 162

sai_set_scheduler_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 173

sai_get_scheduler_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 186

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 201
class struct__sai_scheduler_group_api_t(Structure):
    pass

struct__sai_scheduler_group_api_t.__slots__ = [
    'create_scheduler_group',
    'remove_scheduler_group',
    'set_scheduler_group_attribute',
    'get_scheduler_group_attribute',
]
struct__sai_scheduler_group_api_t._fields_ = [
    ('create_scheduler_group', sai_create_scheduler_group_fn),
    ('remove_scheduler_group', sai_remove_scheduler_group_fn),
    ('set_scheduler_group_attribute', sai_set_scheduler_group_attribute_fn),
    ('get_scheduler_group_attribute', sai_get_scheduler_group_attribute_fn),
]

sai_scheduler_group_api_t = struct__sai_scheduler_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 201

enum__sai_scheduling_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_STRICT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_WRR = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_DWRR = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 50

sai_scheduling_type_t = enum__sai_scheduling_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 50

enum__sai_scheduler_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_SCHEDULING_TYPE = SAI_SCHEDULER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_METER_TYPE = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_END = (SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_CUSTOM_RANGE_END = (SAI_SCHEDULER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

sai_scheduler_attr_t = enum__sai_scheduler_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 143

sai_create_scheduler_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 155

sai_remove_scheduler_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 168

sai_set_scheduler_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 179

sai_get_scheduler_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 192

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 207
class struct__sai_scheduler_api_t(Structure):
    pass

struct__sai_scheduler_api_t.__slots__ = [
    'create_scheduler',
    'remove_scheduler',
    'set_scheduler_attribute',
    'get_scheduler_attribute',
]
struct__sai_scheduler_api_t._fields_ = [
    ('create_scheduler', sai_create_scheduler_fn),
    ('remove_scheduler', sai_remove_scheduler_fn),
    ('set_scheduler_attribute', sai_set_scheduler_attribute_fn),
    ('get_scheduler_attribute', sai_get_scheduler_attribute_fn),
]

sai_scheduler_api_t = struct__sai_scheduler_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 207

enum__sai_segmentroute_sidlist_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 50

SAI_SEGMENTROUTE_SIDLIST_TYPE_INSERT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 50

SAI_SEGMENTROUTE_SIDLIST_TYPE_ENCAPS = (SAI_SEGMENTROUTE_SIDLIST_TYPE_INSERT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 50

SAI_SEGMENTROUTE_SIDLIST_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 50

sai_segmentroute_sidlist_type_t = enum__sai_segmentroute_sidlist_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 50

enum__sai_segmentroute_sidlist_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_TYPE = SAI_SEGMENTROUTE_SIDLIST_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_TLV_LIST = (SAI_SEGMENTROUTE_SIDLIST_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_SEGMENT_LIST = (SAI_SEGMENTROUTE_SIDLIST_ATTR_TLV_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_END = (SAI_SEGMENTROUTE_SIDLIST_ATTR_SEGMENT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

SAI_SEGMENTROUTE_SIDLIST_ATTR_CUSTOM_RANGE_END = (SAI_SEGMENTROUTE_SIDLIST_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

sai_segmentroute_sidlist_attr_t = enum__sai_segmentroute_sidlist_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 98

sai_create_segmentroute_sidlist_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 110

sai_remove_segmentroute_sidlist_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 123

sai_set_segmentroute_sidlist_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 134

sai_get_segmentroute_sidlist_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 147

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 163
class struct__sai_segmentroute_api_t(Structure):
    pass

struct__sai_segmentroute_api_t.__slots__ = [
    'create_segmentroute_sidlist',
    'remove_segmentroute_sidlist',
    'set_segmentroute_sidlist_attribute',
    'get_segmentroute_sidlist_attribute',
    'create_segmentroute_sidlists',
    'remove_segmentroute_sidlists',
]
struct__sai_segmentroute_api_t._fields_ = [
    ('create_segmentroute_sidlist', sai_create_segmentroute_sidlist_fn),
    ('remove_segmentroute_sidlist', sai_remove_segmentroute_sidlist_fn),
    ('set_segmentroute_sidlist_attribute', sai_set_segmentroute_sidlist_attribute_fn),
    ('get_segmentroute_sidlist_attribute', sai_get_segmentroute_sidlist_attribute_fn),
    ('create_segmentroute_sidlists', sai_bulk_object_create_fn),
    ('remove_segmentroute_sidlists', sai_bulk_object_remove_fn),
]

sai_segmentroute_api_t = struct__sai_segmentroute_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 163

enum__sai_stp_port_state_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 50

SAI_STP_PORT_STATE_LEARNING = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 50

SAI_STP_PORT_STATE_FORWARDING = (SAI_STP_PORT_STATE_LEARNING + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 50

SAI_STP_PORT_STATE_BLOCKING = (SAI_STP_PORT_STATE_FORWARDING + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 50

sai_stp_port_state_t = enum__sai_stp_port_state_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 50

enum__sai_stp_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_VLAN_LIST = SAI_STP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_BRIDGE_ID = (SAI_STP_ATTR_VLAN_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_PORT_LIST = (SAI_STP_ATTR_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_END = (SAI_STP_ATTR_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

SAI_STP_ATTR_CUSTOM_RANGE_END = (SAI_STP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

sai_stp_attr_t = enum__sai_stp_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 101

enum__sai_stp_port_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_STP = SAI_STP_PORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_BRIDGE_PORT = (SAI_STP_PORT_ATTR_STP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_STATE = (SAI_STP_PORT_ATTR_BRIDGE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_END = (SAI_STP_PORT_ATTR_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

SAI_STP_PORT_ATTR_CUSTOM_RANGE_END = (SAI_STP_PORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

sai_stp_port_attr_t = enum__sai_stp_port_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 150

sai_create_stp_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 163

sai_remove_stp_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 177

sai_set_stp_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 189

sai_get_stp_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 203

sai_create_stp_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 219

sai_remove_stp_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 233

sai_set_stp_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 245

sai_get_stp_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 259

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 279
class struct__sai_stp_api_t(Structure):
    pass

struct__sai_stp_api_t.__slots__ = [
    'create_stp',
    'remove_stp',
    'set_stp_attribute',
    'get_stp_attribute',
    'create_stp_port',
    'remove_stp_port',
    'set_stp_port_attribute',
    'get_stp_port_attribute',
    'create_stp_ports',
    'remove_stp_ports',
]
struct__sai_stp_api_t._fields_ = [
    ('create_stp', sai_create_stp_fn),
    ('remove_stp', sai_remove_stp_fn),
    ('set_stp_attribute', sai_set_stp_attribute_fn),
    ('get_stp_attribute', sai_get_stp_attribute_fn),
    ('create_stp_port', sai_create_stp_port_fn),
    ('remove_stp_port', sai_remove_stp_port_fn),
    ('set_stp_port_attribute', sai_set_stp_port_attribute_fn),
    ('get_stp_port_attribute', sai_get_stp_port_attribute_fn),
    ('create_stp_ports', sai_bulk_object_create_fn),
    ('remove_stp_ports', sai_bulk_object_remove_fn),
]

sai_stp_api_t = struct__sai_stp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 279

enum__sai_switch_oper_status_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_UNKNOWN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_UP = (SAI_SWITCH_OPER_STATUS_UNKNOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_DOWN = (SAI_SWITCH_OPER_STATUS_UP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_FAILED = (SAI_SWITCH_OPER_STATUS_DOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

sai_switch_oper_status_t = enum__sai_switch_oper_status_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 63

enum__sai_packet_action_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_DROP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_FORWARD = (SAI_PACKET_ACTION_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_COPY = (SAI_PACKET_ACTION_FORWARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_COPY_CANCEL = (SAI_PACKET_ACTION_COPY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_TRAP = (SAI_PACKET_ACTION_COPY_CANCEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_LOG = (SAI_PACKET_ACTION_TRAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_DENY = (SAI_PACKET_ACTION_LOG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

SAI_PACKET_ACTION_TRANSIT = (SAI_PACKET_ACTION_DENY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

sai_packet_action_t = enum__sai_packet_action_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 136

enum__sai_packet_vlan_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 166

SAI_PACKET_VLAN_UNTAG = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 166

SAI_PACKET_VLAN_SINGLE_OUTER_TAG = (SAI_PACKET_VLAN_UNTAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 166

SAI_PACKET_VLAN_DOUBLE_TAG = (SAI_PACKET_VLAN_SINGLE_OUTER_TAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 166

sai_packet_vlan_t = enum__sai_packet_vlan_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 166

enum__sai_switch_switching_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 179

SAI_SWITCH_SWITCHING_MODE_CUT_THROUGH = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 179

SAI_SWITCH_SWITCHING_MODE_STORE_AND_FORWARD = (SAI_SWITCH_SWITCHING_MODE_CUT_THROUGH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 179

sai_switch_switching_mode_t = enum__sai_switch_switching_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 179

enum__sai_hash_algorithm_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_CRC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_XOR = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_RANDOM = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_CRC_32LO = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_CRC_32HI = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_CRC_CCITT = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

SAI_HASH_ALGORITHM_CRC_XOR = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

sai_hash_algorithm_t = enum__sai_hash_algorithm_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 208

enum__sai_switch_restart_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 224

SAI_SWITCH_RESTART_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 224

SAI_SWITCH_RESTART_TYPE_PLANNED = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 224

SAI_SWITCH_RESTART_TYPE_ANY = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 224

sai_switch_restart_type_t = enum__sai_switch_restart_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 224

enum__sai_switch_mcast_snooping_capability_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_SG = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG_AND_SG = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

sai_switch_mcast_snooping_capability_t = enum__sai_switch_mcast_snooping_capability_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 243

enum__sai_switch_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS = SAI_SWITCH_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PORT_NUMBER = SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS = (SAI_SWITCH_ATTR_PORT_NUMBER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PORT_LIST = (SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PORT_MAX_MTU = (SAI_SWITCH_ATTR_PORT_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_CPU_PORT = (SAI_SWITCH_ATTR_PORT_MAX_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS = (SAI_SWITCH_ATTR_CPU_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_TABLE_SIZE = (SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE = (SAI_SWITCH_ATTR_FDB_TABLE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE = (SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_MEMBERS = (SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_LAGS = (SAI_SWITCH_ATTR_LAG_MEMBERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_MEMBERS = (SAI_SWITCH_ATTR_NUMBER_OF_LAGS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS = (SAI_SWITCH_ATTR_ECMP_MEMBERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED = (SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_OPER_STATUS = (SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS = (SAI_SWITCH_ATTR_OPER_STATUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TEMP_LIST = (SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_TEMP = (SAI_SWITCH_ATTR_TEMP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVERAGE_TEMP = (SAI_SWITCH_ATTR_MAX_TEMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_AVERAGE_TEMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE = (SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_DEFAULT_VLAN_ID = (SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID = (SAI_SWITCH_ATTR_DEFAULT_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_STP_INSTANCE = (SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID = (SAI_SWITCH_ATTR_MAX_STP_INSTANCE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID = (SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_INGRESS_ACL = (SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_EGRESS_ACL = (SAI_SWITCH_ATTR_INGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES = (SAI_SWITCH_ATTR_EGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM = (SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM = (SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY = (SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE = (SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP = (SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP = (SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_HASH = (SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_HASH = (SAI_SWITCH_ATTR_ECMP_HASH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_RESTART_WARM = (SAI_SWITCH_ATTR_LAG_HASH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_WARM_RECOVER = (SAI_SWITCH_ATTR_RESTART_WARM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_RESTART_TYPE = (SAI_SWITCH_ATTR_WARM_RECOVER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL = (SAI_SWITCH_ATTR_RESTART_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NV_STORAGE_SIZE = (SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT = (SAI_SWITCH_ATTR_NV_STORAGE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT = (SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_CAPABILITY = (SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY = (SAI_SWITCH_ATTR_ACL_CAPABILITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCHING_MODE = (SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE = (SAI_SWITCH_ATTR_SWITCHING_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE = (SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = (SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES = (SAI_SWITCH_ATTR_SRC_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_AGING_TIME = (SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_AGING_TIME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM = (SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED = (SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH = (SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_HASH_IPV4 = (SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4 = (SAI_SWITCH_ATTR_ECMP_HASH_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECMP_HASH_IPV6 = (SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM = (SAI_SWITCH_ATTR_ECMP_HASH_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED = (SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH = (SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_HASH_IPV4 = (SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4 = (SAI_SWITCH_ATTR_LAG_HASH_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_LAG_HASH_IPV6 = (SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL = (SAI_SWITCH_ATTR_LAG_HASH_IPV6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_DEFAULT_TC = (SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = (SAI_SWITCH_ATTR_QOS_DEFAULT_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = (SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = (SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = (SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP = (SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = (SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE = (SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCH_PROFILE_ID = (SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO = (SAI_SWITCH_ATTR_SWITCH_PROFILE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME = (SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_INIT_SWITCH = (SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_INIT_SWITCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY = (SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY = SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY = (SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY = (SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = (SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_FAST_API_ENABLE = (SAI_SWITCH_ATTR_MAX_TWAMP_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MIRROR_TC = (SAI_SWITCH_ATTR_FAST_API_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_STAGE_INGRESS = (SAI_SWITCH_ATTR_MIRROR_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ACL_STAGE_EGRESS = (SAI_SWITCH_ATTR_ACL_STAGE_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SEGMENTROUTE_MAX_SID_DEPTH = (SAI_SWITCH_ATTR_ACL_STAGE_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SEGMENTROUTE_TLV_TYPE = (SAI_SWITCH_ATTR_SEGMENTROUTE_MAX_SID_DEPTH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES = (SAI_SWITCH_ATTR_SEGMENTROUTE_TLV_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY = (SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION = (SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE = (SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL = (SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE = (SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL = (SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE = (SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TPID_OUTER_VLAN = (SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TPID_INNER_VLAN = (SAI_SWITCH_ATTR_TPID_OUTER_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_CRC_CHECK_ENABLE = (SAI_SWITCH_ATTR_TPID_INNER_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE = (SAI_SWITCH_ATTR_CRC_CHECK_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION = (SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_BFD_SESSION = (SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE = (SAI_SWITCH_ATTR_MAX_BFD_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE = (SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MIN_BFD_RX = (SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MIN_BFD_TX = (SAI_SWITCH_ATTR_MIN_BFD_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE = (SAI_SWITCH_ATTR_MIN_BFD_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC = (SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT = (SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_MIRROR_SESSION = (SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION = (SAI_SWITCH_ATTR_MAX_MIRROR_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE = (SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL = (SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TAM_OBJECT_ID = (SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY = (SAI_SWITCH_ATTR_TAM_OBJECT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_PRE_SHUTDOWN = (SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID = (SAI_SWITCH_ATTR_PRE_SHUTDOWN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NAT_ENABLE = (SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY = (SAI_SWITCH_ATTR_NAT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION = (SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MAX_Y1731_SESSION = (SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE = (SAI_SWITCH_ATTR_MAX_Y1731_SESSION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_ECN_ACTION_ENABLE = (SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_NOTIFY = (SAI_SWITCH_ATTR_ECN_ACTION_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_LATENCY_NOTIFY = (SAI_SWITCH_ATTR_MONITOR_BUFFER_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE = (SAI_SWITCH_ATTR_MONITOR_LATENCY_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_QUEUE_PERIODIC_MONITOR_ENABLE = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_QUEUE_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MB_THRESHOLD_MIN = (SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MB_THRESHOLD_MAX = (SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MB_THRESHOLD_MIN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD = (SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MB_THRESHOLD_MAX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL = (SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_SIGNAL_DEGRADE_EVENT_NOTIFY = (SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_END = (SAI_SWITCH_ATTR_SIGNAL_DEGRADE_EVENT_NOTIFY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

SAI_SWITCH_ATTR_CUSTOM_RANGE_END = (SAI_SWITCH_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

sai_switch_attr_t = enum__sai_switch_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2047

enum__sai_switch_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE = 4096 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_END = 8191 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE = 8192 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_END = 12287 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

sai_switch_stat_t = enum__sai_switch_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2110

sai_switch_shutdown_request_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2231

sai_switch_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_switch_oper_status_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2242

sai_create_switch_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2259

sai_remove_switch_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2273

sai_set_switch_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2284

sai_get_switch_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2297

sai_get_switch_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2312

sai_get_switch_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2329

sai_clear_switch_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2345

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2363
class struct__sai_switch_api_t(Structure):
    pass

struct__sai_switch_api_t.__slots__ = [
    'create_switch',
    'remove_switch',
    'set_switch_attribute',
    'get_switch_attribute',
    'get_switch_stats',
    'get_switch_stats_ext',
    'clear_switch_stats',
]
struct__sai_switch_api_t._fields_ = [
    ('create_switch', sai_create_switch_fn),
    ('remove_switch', sai_remove_switch_fn),
    ('set_switch_attribute', sai_set_switch_attribute_fn),
    ('get_switch_attribute', sai_get_switch_attribute_fn),
    ('get_switch_stats', sai_get_switch_stats_fn),
    ('get_switch_stats_ext', sai_get_switch_stats_ext_fn),
    ('clear_switch_stats', sai_clear_switch_stats_fn),
]

sai_switch_api_t = struct__sai_switch_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2363

enum__sai_tam_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST = SAI_TAM_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_EVENT_OBJECTS_LIST = (SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_INT_OBJECTS_LIST = (SAI_TAM_ATTR_EVENT_OBJECTS_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST = (SAI_TAM_ATTR_INT_OBJECTS_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_END = (SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

SAI_TAM_ATTR_CUSTOM_RANGE_END = (SAI_TAM_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

sai_tam_attr_t = enum__sai_tam_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 100

sai_create_tam_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 116

sai_remove_tam_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 131

sai_set_tam_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 142

sai_get_tam_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 155

enum__sai_tam_tel_math_func_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_GEO_MEAN = (SAI_TAM_TEL_MATH_FUNC_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_ALGEBRAIC_MEAN = (SAI_TAM_TEL_MATH_FUNC_TYPE_GEO_MEAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_AVERAGE = (SAI_TAM_TEL_MATH_FUNC_TYPE_ALGEBRAIC_MEAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_MODE = (SAI_TAM_TEL_MATH_FUNC_TYPE_AVERAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_RATE = (SAI_TAM_TEL_MATH_FUNC_TYPE_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

sai_tam_tel_math_func_type_t = enum__sai_tam_tel_math_func_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 183

enum__sai_tam_math_func_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE = SAI_TAM_MATH_FUNC_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_END = (SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_END = (SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

sai_tam_math_func_attr_t = enum__sai_tam_math_func_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 215

sai_create_tam_math_func_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 226

sai_remove_tam_math_func_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 239

sai_get_tam_math_func_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 251

sai_set_tam_math_func_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 264

enum__sai_tam_event_threshold_unit_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_NANOSEC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_USEC = (SAI_TAM_EVENT_THRESHOLD_UNIT_NANOSEC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_MSEC = (SAI_TAM_EVENT_THRESHOLD_UNIT_USEC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_PERCENT = (SAI_TAM_EVENT_THRESHOLD_UNIT_MSEC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_BYTES = (SAI_TAM_EVENT_THRESHOLD_UNIT_PERCENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_PACKETS = (SAI_TAM_EVENT_THRESHOLD_UNIT_BYTES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

SAI_TAM_EVENT_THRESHOLD_UNIT_CELLS = (SAI_TAM_EVENT_THRESHOLD_UNIT_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

sai_tam_event_threshold_unit_t = enum__sai_tam_event_threshold_unit_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 307

enum__sai_tam_event_threshold_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK = SAI_TAM_EVENT_THRESHOLD_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK = (SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY = (SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_RATE = (SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE = (SAI_TAM_EVENT_THRESHOLD_ATTR_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT = (SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_END = (SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

sai_tam_event_threshold_attr_t = enum__sai_tam_event_threshold_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 385

sai_create_tam_event_threshold_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 397

sai_remove_tam_event_threshold_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 410

sai_get_tam_event_threshold_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 422

sai_set_tam_event_threshold_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 435

enum__sai_tam_int_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_IOAM = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_IFA1 = (SAI_TAM_INT_TYPE_IOAM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_IFA2 = (SAI_TAM_INT_TYPE_IFA1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_P4_INT_1 = (SAI_TAM_INT_TYPE_IFA2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_P4_INT_2 = (SAI_TAM_INT_TYPE_P4_INT_1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_DIRECT_EXPORT = (SAI_TAM_INT_TYPE_P4_INT_2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

SAI_TAM_INT_TYPE_IFA1_TAILSTAMP = (SAI_TAM_INT_TYPE_DIRECT_EXPORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

sai_tam_int_type_t = enum__sai_tam_int_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 479

enum__sai_tam_int_presence_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

SAI_TAM_INT_PRESENCE_TYPE_UNDEFINED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

SAI_TAM_INT_PRESENCE_TYPE_PB = (SAI_TAM_INT_PRESENCE_TYPE_UNDEFINED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

SAI_TAM_INT_PRESENCE_TYPE_L3_PROTOCOL = (SAI_TAM_INT_PRESENCE_TYPE_PB + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

SAI_TAM_INT_PRESENCE_TYPE_DSCP = (SAI_TAM_INT_PRESENCE_TYPE_L3_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

sai_tam_int_presence_type_t = enum__sai_tam_int_presence_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 509

enum__sai_tam_int_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_TYPE = SAI_TAM_INT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_DEVICE_ID = (SAI_TAM_INT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_IOAM_TRACE_TYPE = (SAI_TAM_INT_ATTR_DEVICE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INT_PRESENCE_TYPE = (SAI_TAM_INT_ATTR_IOAM_TRACE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INT_PRESENCE_PB1 = (SAI_TAM_INT_ATTR_INT_PRESENCE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INT_PRESENCE_PB2 = (SAI_TAM_INT_ATTR_INT_PRESENCE_PB1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INT_PRESENCE_DSCP_VALUE = (SAI_TAM_INT_ATTR_INT_PRESENCE_PB2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INLINE = (SAI_TAM_INT_ATTR_INT_PRESENCE_DSCP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INT_PRESENCE_L3_PROTOCOL = (SAI_TAM_INT_ATTR_INLINE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_TRACE_VECTOR = (SAI_TAM_INT_ATTR_INT_PRESENCE_L3_PROTOCOL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_ACTION_VECTOR = (SAI_TAM_INT_ATTR_TRACE_VECTOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_P4_INT_INSTRUCTION_BITMAP = (SAI_TAM_INT_ATTR_ACTION_VECTOR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_METADATA_FRAGMENT_ENABLE = (SAI_TAM_INT_ATTR_P4_INT_INSTRUCTION_BITMAP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_REPORT_ALL_PACKETS = (SAI_TAM_INT_ATTR_METADATA_FRAGMENT_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_FLOW_LIVENESS_PERIOD = (SAI_TAM_INT_ATTR_REPORT_ALL_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_LATENCY_SENSITIVITY = (SAI_TAM_INT_ATTR_FLOW_LIVENESS_PERIOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_ACL_GROUP = (SAI_TAM_INT_ATTR_LATENCY_SENSITIVITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_MAX_HOP_COUNT = (SAI_TAM_INT_ATTR_ACL_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_MAX_LENGTH = (SAI_TAM_INT_ATTR_MAX_HOP_COUNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_NAME_SPACE_ID = (SAI_TAM_INT_ATTR_MAX_LENGTH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_NAME_SPACE_ID_GLOBAL = (SAI_TAM_INT_ATTR_NAME_SPACE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = (SAI_TAM_INT_ATTR_NAME_SPACE_ID_GLOBAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_COLLECTOR_LIST = (SAI_TAM_INT_ATTR_INGRESS_SAMPLEPACKET_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_MATH_FUNC = (SAI_TAM_INT_ATTR_COLLECTOR_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_REPORT_ID = (SAI_TAM_INT_ATTR_MATH_FUNC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_END = (SAI_TAM_INT_ATTR_REPORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

SAI_TAM_INT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_INT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

sai_tam_int_attr_t = enum__sai_tam_int_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 798

sai_create_tam_int_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 810

sai_remove_tam_int_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 823

sai_get_tam_int_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 835

sai_set_tam_int_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 848

enum__sai_tam_telemetry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

SAI_TAM_TELEMETRY_TYPE_NE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

SAI_TAM_TELEMETRY_TYPE_SWITCH = (SAI_TAM_TELEMETRY_TYPE_NE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

SAI_TAM_TELEMETRY_TYPE_FABRIC = (SAI_TAM_TELEMETRY_TYPE_SWITCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

SAI_TAM_TELEMETRY_TYPE_FLOW = (SAI_TAM_TELEMETRY_TYPE_FABRIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

SAI_TAM_TELEMETRY_TYPE_INT = (SAI_TAM_TELEMETRY_TYPE_FLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

sai_tam_telemetry_type_t = enum__sai_tam_telemetry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 889

enum__sai_tam_tel_type_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE = SAI_TAM_TEL_TYPE_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_INT_SWITCH_IDENTIFIER = (SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS = (SAI_TAM_TEL_TYPE_ATTR_INT_SWITCH_IDENTIFIER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE = (SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE = (SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC = (SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_REPORT_ID = (SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_END = (SAI_TAM_TEL_TYPE_ATTR_REPORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

sai_tam_tel_type_attr_t = enum__sai_tam_tel_type_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1058

sai_create_tam_tel_type_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1070

sai_remove_tam_tel_type_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1083

sai_get_tam_tel_type_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1095

sai_set_tam_tel_type_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1108

enum__sai_tam_report_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_SFLOW = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_IPFIX = (SAI_TAM_REPORT_TYPE_SFLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_PROTO = (SAI_TAM_REPORT_TYPE_IPFIX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_THRIFT = (SAI_TAM_REPORT_TYPE_PROTO + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_JSON = (SAI_TAM_REPORT_TYPE_THRIFT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_P4_EXTN = (SAI_TAM_REPORT_TYPE_JSON + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_HISTOGRAM = (SAI_TAM_REPORT_TYPE_P4_EXTN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

SAI_TAM_REPORT_TYPE_VENDOR_EXTN = (SAI_TAM_REPORT_TYPE_HISTOGRAM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

sai_tam_report_type_t = enum__sai_tam_report_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1156

enum__sai_tam_report_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1170

SAI_TAM_REPORT_MODE_ALL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1170

SAI_TAM_REPORT_MODE_BULK = (SAI_TAM_REPORT_MODE_ALL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1170

sai_tam_report_mode_t = enum__sai_tam_report_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1170

enum__sai_tam_report_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_TYPE = SAI_TAM_REPORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS = (SAI_TAM_REPORT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY = (SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_QUOTA = (SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_REPORT_MODE = (SAI_TAM_REPORT_ATTR_QUOTA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_REPORT_INTERVAL = (SAI_TAM_REPORT_ATTR_REPORT_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_END = (SAI_TAM_REPORT_ATTR_REPORT_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

sai_tam_report_attr_t = enum__sai_tam_report_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1258

sai_create_tam_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1270

sai_remove_tam_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1283

sai_get_tam_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1295

sai_set_tam_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1308

enum__sai_tam_reporting_unit_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

SAI_TAM_REPORTING_UNIT_SEC = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

SAI_TAM_REPORTING_UNIT_MINUTE = (SAI_TAM_REPORTING_UNIT_SEC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

SAI_TAM_REPORTING_UNIT_HOUR = (SAI_TAM_REPORTING_UNIT_MINUTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

SAI_TAM_REPORTING_UNIT_DAY = (SAI_TAM_REPORTING_UNIT_HOUR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

sai_tam_reporting_unit_t = enum__sai_tam_reporting_unit_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1337

enum__sai_tam_telemetry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST = SAI_TAM_TELEMETRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST = (SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT = (SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL = (SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_END = (SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

sai_tam_telemetry_attr_t = enum__sai_tam_telemetry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1400

sai_create_tam_telemetry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1412

sai_remove_tam_telemetry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1425

sai_get_tam_telemetry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1437

sai_set_tam_telemetry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1450

enum__sai_tam_transport_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

SAI_TAM_TRANSPORT_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

SAI_TAM_TRANSPORT_TYPE_TCP = (SAI_TAM_TRANSPORT_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

SAI_TAM_TRANSPORT_TYPE_UDP = (SAI_TAM_TRANSPORT_TYPE_TCP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

SAI_TAM_TRANSPORT_TYPE_GRPC = (SAI_TAM_TRANSPORT_TYPE_UDP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

sai_tam_transport_type_t = enum__sai_tam_transport_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1480

enum__sai_tam_transport_auth_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1502

SAI_TAM_TRANSPORT_AUTH_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1502

SAI_TAM_TRANSPORT_AUTH_TYPE_SSL = (SAI_TAM_TRANSPORT_AUTH_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1502

SAI_TAM_TRANSPORT_AUTH_TYPE_TLS = (SAI_TAM_TRANSPORT_AUTH_TYPE_SSL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1502

sai_tam_transport_auth_type_t = enum__sai_tam_transport_auth_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1502

enum__sai_tam_transport_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE = SAI_TAM_TRANSPORT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_SRC_PORT = (SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_DST_PORT = (SAI_TAM_TRANSPORT_ATTR_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE = (SAI_TAM_TRANSPORT_ATTR_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_MTU = (SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_END = (SAI_TAM_TRANSPORT_ATTR_MTU + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

sai_tam_transport_attr_t = enum__sai_tam_transport_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1573

sai_create_tam_transport_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1585

sai_remove_tam_transport_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1598

sai_get_tam_transport_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1610

sai_set_tam_transport_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1623

enum__sai_tam_collector_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_SRC_IP = SAI_TAM_COLLECTOR_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_DST_IP = (SAI_TAM_COLLECTOR_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_LOCALHOST = (SAI_TAM_COLLECTOR_ATTR_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID = (SAI_TAM_COLLECTOR_ATTR_LOCALHOST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE = (SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_TRANSPORT = (SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE = (SAI_TAM_COLLECTOR_ATTR_TRANSPORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_END = (SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_END = (SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

sai_tam_collector_attr_t = enum__sai_tam_collector_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1718

sai_create_tam_collector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1730

sai_remove_tam_collector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1743

sai_get_tam_collector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1755

sai_set_tam_collector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1768

enum__sai_tam_event_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_FLOW_STATE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_FLOW_WATCHLIST = (SAI_TAM_EVENT_TYPE_FLOW_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_FLOW_TCPFLAG = (SAI_TAM_EVENT_TYPE_FLOW_WATCHLIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_QUEUE_THRESHOLD = (SAI_TAM_EVENT_TYPE_FLOW_TCPFLAG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_QUEUE_TAIL_DROP = (SAI_TAM_EVENT_TYPE_QUEUE_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_PACKET_DROP = (SAI_TAM_EVENT_TYPE_QUEUE_TAIL_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_RESOURCE_UTILIZATION = (SAI_TAM_EVENT_TYPE_PACKET_DROP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_IPG_SHARED = (SAI_TAM_EVENT_TYPE_RESOURCE_UTILIZATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_IPG_XOFF_ROOM = (SAI_TAM_EVENT_TYPE_IPG_SHARED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

SAI_TAM_EVENT_TYPE_BSP = (SAI_TAM_EVENT_TYPE_IPG_XOFF_ROOM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

sai_tam_event_type_t = enum__sai_tam_event_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1837

enum__sai_tam_event_action_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE = SAI_TAM_EVENT_ACTION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE = (SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_END = (SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

sai_tam_event_action_attr_t = enum__sai_tam_event_action_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1878

sai_create_tam_event_action_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1890

sai_remove_tam_event_action_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1903

sai_get_tam_event_action_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1915

sai_set_tam_event_action_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1928

enum__sai_tam_event_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_TYPE = SAI_TAM_EVENT_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_ACTION_LIST = (SAI_TAM_EVENT_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_COLLECTOR_LIST = (SAI_TAM_EVENT_ATTR_ACTION_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_THRESHOLD = (SAI_TAM_EVENT_ATTR_COLLECTOR_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_DSCP_VALUE = (SAI_TAM_EVENT_ATTR_THRESHOLD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_END = (SAI_TAM_EVENT_ATTR_DSCP_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

sai_tam_event_attr_t = enum__sai_tam_event_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 1999

sai_create_tam_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2011

sai_remove_tam_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2024

sai_get_tam_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2036

sai_set_tam_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2049

sai_tam_event_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_size_t, POINTER(None), c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2067

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2085
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_tam_telemetry_get_data'):
        continue
    sai_tam_telemetry_get_data = _lib.sai_tam_telemetry_get_data
    sai_tam_telemetry_get_data.argtypes = [sai_object_id_t, sai_object_list_t, c_uint8, POINTER(sai_size_t), POINTER(None)]
    sai_tam_telemetry_get_data.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2155
class struct__sai_tam_api_t(Structure):
    pass

struct__sai_tam_api_t.__slots__ = [
    'create_tam',
    'remove_tam',
    'set_tam_attribute',
    'get_tam_attribute',
    'create_tam_math_func',
    'remove_tam_math_func',
    'set_tam_math_func_attribute',
    'get_tam_math_func_attribute',
    'create_tam_report',
    'remove_tam_report',
    'set_tam_report_attribute',
    'get_tam_report_attribute',
    'create_tam_event_threshold',
    'remove_tam_event_threshold',
    'set_tam_event_threshold_attribute',
    'get_tam_event_threshold_attribute',
    'create_tam_int',
    'remove_tam_int',
    'set_tam_int_attribute',
    'get_tam_int_attribute',
    'create_tam_tel_type',
    'remove_tam_tel_type',
    'set_tam_tel_type_attribute',
    'get_tam_tel_type_attribute',
    'create_tam_transport',
    'remove_tam_transport',
    'set_tam_transport_attribute',
    'get_tam_transport_attribute',
    'create_tam_telemetry',
    'remove_tam_telemetry',
    'set_tam_telemetry_attribute',
    'get_tam_telemetry_attribute',
    'create_tam_collector',
    'remove_tam_collector',
    'set_tam_collector_attribute',
    'get_tam_collector_attribute',
    'create_tam_event_action',
    'remove_tam_event_action',
    'set_tam_event_action_attribute',
    'get_tam_event_action_attribute',
    'create_tam_event',
    'remove_tam_event',
    'set_tam_event_attribute',
    'get_tam_event_attribute',
]
struct__sai_tam_api_t._fields_ = [
    ('create_tam', sai_create_tam_fn),
    ('remove_tam', sai_remove_tam_fn),
    ('set_tam_attribute', sai_set_tam_attribute_fn),
    ('get_tam_attribute', sai_get_tam_attribute_fn),
    ('create_tam_math_func', sai_create_tam_math_func_fn),
    ('remove_tam_math_func', sai_remove_tam_math_func_fn),
    ('set_tam_math_func_attribute', sai_set_tam_math_func_attribute_fn),
    ('get_tam_math_func_attribute', sai_get_tam_math_func_attribute_fn),
    ('create_tam_report', sai_create_tam_report_fn),
    ('remove_tam_report', sai_remove_tam_report_fn),
    ('set_tam_report_attribute', sai_set_tam_report_attribute_fn),
    ('get_tam_report_attribute', sai_get_tam_report_attribute_fn),
    ('create_tam_event_threshold', sai_create_tam_event_threshold_fn),
    ('remove_tam_event_threshold', sai_remove_tam_event_threshold_fn),
    ('set_tam_event_threshold_attribute', sai_set_tam_event_threshold_attribute_fn),
    ('get_tam_event_threshold_attribute', sai_get_tam_event_threshold_attribute_fn),
    ('create_tam_int', sai_create_tam_int_fn),
    ('remove_tam_int', sai_remove_tam_int_fn),
    ('set_tam_int_attribute', sai_set_tam_int_attribute_fn),
    ('get_tam_int_attribute', sai_get_tam_int_attribute_fn),
    ('create_tam_tel_type', sai_create_tam_tel_type_fn),
    ('remove_tam_tel_type', sai_remove_tam_tel_type_fn),
    ('set_tam_tel_type_attribute', sai_set_tam_tel_type_attribute_fn),
    ('get_tam_tel_type_attribute', sai_get_tam_tel_type_attribute_fn),
    ('create_tam_transport', sai_create_tam_transport_fn),
    ('remove_tam_transport', sai_remove_tam_transport_fn),
    ('set_tam_transport_attribute', sai_set_tam_transport_attribute_fn),
    ('get_tam_transport_attribute', sai_get_tam_transport_attribute_fn),
    ('create_tam_telemetry', sai_create_tam_telemetry_fn),
    ('remove_tam_telemetry', sai_remove_tam_telemetry_fn),
    ('set_tam_telemetry_attribute', sai_set_tam_telemetry_attribute_fn),
    ('get_tam_telemetry_attribute', sai_get_tam_telemetry_attribute_fn),
    ('create_tam_collector', sai_create_tam_collector_fn),
    ('remove_tam_collector', sai_remove_tam_collector_fn),
    ('set_tam_collector_attribute', sai_set_tam_collector_attribute_fn),
    ('get_tam_collector_attribute', sai_get_tam_collector_attribute_fn),
    ('create_tam_event_action', sai_create_tam_event_action_fn),
    ('remove_tam_event_action', sai_remove_tam_event_action_fn),
    ('set_tam_event_action_attribute', sai_set_tam_event_action_attribute_fn),
    ('get_tam_event_action_attribute', sai_get_tam_event_action_attribute_fn),
    ('create_tam_event', sai_create_tam_event_fn),
    ('remove_tam_event', sai_remove_tam_event_fn),
    ('set_tam_event_attribute', sai_set_tam_event_attribute_fn),
    ('get_tam_event_attribute', sai_get_tam_event_attribute_fn),
]

sai_tam_api_t = struct__sai_tam_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2155

enum__sai_tunnel_map_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

SAI_TUNNEL_MAP_TYPE_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

sai_tunnel_map_type_t = enum__sai_tunnel_map_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 68

enum__sai_tunnel_map_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE = SAI_TUNNEL_MAP_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_END = (SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

sai_tunnel_map_entry_attr_t = enum__sai_tunnel_map_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 219

enum__sai_tunnel_map_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_TYPE = SAI_TUNNEL_MAP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_ENTRY_LIST = (SAI_TUNNEL_MAP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_END = (SAI_TUNNEL_MAP_ATTR_ENTRY_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

sai_tunnel_map_attr_t = enum__sai_tunnel_map_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 259

sai_create_tunnel_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 271

sai_remove_tunnel_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 284

sai_set_tunnel_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 295

sai_get_tunnel_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 308

enum__sai_tunnel_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

SAI_TUNNEL_TYPE_IPINIP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

SAI_TUNNEL_TYPE_IPINIP_GRE = (SAI_TUNNEL_TYPE_IPINIP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

SAI_TUNNEL_TYPE_VXLAN = (SAI_TUNNEL_TYPE_IPINIP_GRE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

SAI_TUNNEL_TYPE_MPLS = (SAI_TUNNEL_TYPE_VXLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

SAI_TUNNEL_TYPE_MPLS_L2 = (SAI_TUNNEL_TYPE_MPLS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

sai_tunnel_type_t = enum__sai_tunnel_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 328

enum__sai_tunnel_ttl_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 355

SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 355

SAI_TUNNEL_TTL_MODE_PIPE_MODEL = (SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 355

sai_tunnel_ttl_mode_t = enum__sai_tunnel_ttl_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 355

enum__sai_tunnel_dscp_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 382

SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 382

SAI_TUNNEL_DSCP_MODE_PIPE_MODEL = (SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 382

sai_tunnel_dscp_mode_t = enum__sai_tunnel_dscp_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 382

enum__sai_tunnel_exp_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 411

SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 411

SAI_TUNNEL_EXP_MODE_PIPE_MODEL = (SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 411

sai_tunnel_exp_mode_t = enum__sai_tunnel_exp_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 411

enum__sai_tunnel_encap_ecn_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 431

SAI_TUNNEL_ENCAP_ECN_MODE_STANDARD = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 431

SAI_TUNNEL_ENCAP_ECN_MODE_USER_DEFINED = (SAI_TUNNEL_ENCAP_ECN_MODE_STANDARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 431

sai_tunnel_encap_ecn_mode_t = enum__sai_tunnel_encap_ecn_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 431

enum__sai_tunnel_decap_ecn_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 455

SAI_TUNNEL_DECAP_ECN_MODE_STANDARD = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 455

SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER = (SAI_TUNNEL_DECAP_ECN_MODE_STANDARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 455

SAI_TUNNEL_DECAP_ECN_MODE_USER_DEFINED = (SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 455

sai_tunnel_decap_ecn_mode_t = enum__sai_tunnel_decap_ecn_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 455

enum__sai_tunnel_mpls_pw_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 471

SAI_TUNNEL_MPLS_PW_MODE_TAGGED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 471

SAI_TUNNEL_MPLS_PW_MODE_RAW = (SAI_TUNNEL_MPLS_PW_MODE_TAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 471

sai_tunnel_mpls_pw_mode_t = enum__sai_tunnel_mpls_pw_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 471

enum__sai_tunnel_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_TYPE = SAI_TUNNEL_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE = (SAI_TUNNEL_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_OVERLAY_INTERFACE = (SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_SRC_IP = (SAI_TUNNEL_ATTR_OVERLAY_INTERFACE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_TTL_MODE = (SAI_TUNNEL_ATTR_ENCAP_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_TTL_VAL = (SAI_TUNNEL_ATTR_ENCAP_TTL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE = (SAI_TUNNEL_ATTR_ENCAP_TTL_VAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL = (SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID = (SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_GRE_KEY = (SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_ECN_MODE = (SAI_TUNNEL_ATTR_ENCAP_GRE_KEY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_MAPPERS = (SAI_TUNNEL_ATTR_ENCAP_ECN_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_ECN_MODE = (SAI_TUNNEL_ATTR_ENCAP_MAPPERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_MAPPERS = (SAI_TUNNEL_ATTR_DECAP_ECN_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_TTL_MODE = (SAI_TUNNEL_ATTR_DECAP_MAPPERS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_DSCP_MODE = (SAI_TUNNEL_ATTR_DECAP_TTL_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST = (SAI_TUNNEL_ATTR_DECAP_DSCP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID = (SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE = (SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = (SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE = (SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW = (SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN = (SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = (SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID = (SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_EXP_MODE = (SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_EXP_MODE = (SAI_TUNNEL_ATTR_DECAP_EXP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_ENCAP_EXP_VAL = (SAI_TUNNEL_ATTR_ENCAP_EXP_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO = (SAI_TUNNEL_ATTR_ENCAP_EXP_VAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_END = (SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

SAI_TUNNEL_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

sai_tunnel_attr_t = enum__sai_tunnel_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 785

enum__sai_tunnel_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

SAI_TUNNEL_STAT_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

SAI_TUNNEL_STAT_IN_PACKETS = (SAI_TUNNEL_STAT_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

SAI_TUNNEL_STAT_OUT_OCTETS = (SAI_TUNNEL_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

SAI_TUNNEL_STAT_OUT_PACKETS = (SAI_TUNNEL_STAT_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

sai_tunnel_stat_t = enum__sai_tunnel_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 804

sai_create_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 816

sai_remove_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 829

sai_set_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 840

sai_get_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 853

sai_get_tunnel_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 868

sai_get_tunnel_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 885

sai_clear_tunnel_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 901

enum__sai_tunnel_term_table_entry_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 917

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 917

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2MP = (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 917

sai_tunnel_term_table_entry_type_t = enum__sai_tunnel_term_table_entry_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 917

enum__sai_tunnel_term_table_entry_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID = SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_END = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

sai_tunnel_term_table_entry_attr_t = enum__sai_tunnel_term_table_entry_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 991

sai_create_tunnel_term_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1003

sai_remove_tunnel_term_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1016

sai_set_tunnel_term_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1027

sai_get_tunnel_term_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1040

sai_create_tunnel_map_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1055

sai_remove_tunnel_map_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1068

sai_set_tunnel_map_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1079

sai_get_tunnel_map_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1092

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1122
class struct__sai_tunnel_api_t(Structure):
    pass

struct__sai_tunnel_api_t.__slots__ = [
    'create_tunnel_map',
    'remove_tunnel_map',
    'set_tunnel_map_attribute',
    'get_tunnel_map_attribute',
    'create_tunnel',
    'remove_tunnel',
    'set_tunnel_attribute',
    'get_tunnel_attribute',
    'get_tunnel_stats',
    'get_tunnel_stats_ext',
    'clear_tunnel_stats',
    'create_tunnel_term_table_entry',
    'remove_tunnel_term_table_entry',
    'set_tunnel_term_table_entry_attribute',
    'get_tunnel_term_table_entry_attribute',
    'create_tunnel_map_entry',
    'remove_tunnel_map_entry',
    'set_tunnel_map_entry_attribute',
    'get_tunnel_map_entry_attribute',
]
struct__sai_tunnel_api_t._fields_ = [
    ('create_tunnel_map', sai_create_tunnel_map_fn),
    ('remove_tunnel_map', sai_remove_tunnel_map_fn),
    ('set_tunnel_map_attribute', sai_set_tunnel_map_attribute_fn),
    ('get_tunnel_map_attribute', sai_get_tunnel_map_attribute_fn),
    ('create_tunnel', sai_create_tunnel_fn),
    ('remove_tunnel', sai_remove_tunnel_fn),
    ('set_tunnel_attribute', sai_set_tunnel_attribute_fn),
    ('get_tunnel_attribute', sai_get_tunnel_attribute_fn),
    ('get_tunnel_stats', sai_get_tunnel_stats_fn),
    ('get_tunnel_stats_ext', sai_get_tunnel_stats_ext_fn),
    ('clear_tunnel_stats', sai_clear_tunnel_stats_fn),
    ('create_tunnel_term_table_entry', sai_create_tunnel_term_table_entry_fn),
    ('remove_tunnel_term_table_entry', sai_remove_tunnel_term_table_entry_fn),
    ('set_tunnel_term_table_entry_attribute', sai_set_tunnel_term_table_entry_attribute_fn),
    ('get_tunnel_term_table_entry_attribute', sai_get_tunnel_term_table_entry_attribute_fn),
    ('create_tunnel_map_entry', sai_create_tunnel_map_entry_fn),
    ('remove_tunnel_map_entry', sai_remove_tunnel_map_entry_fn),
    ('set_tunnel_map_entry_attribute', sai_set_tunnel_map_entry_attribute_fn),
    ('get_tunnel_map_entry_attribute', sai_get_tunnel_map_entry_attribute_fn),
]

sai_tunnel_api_t = struct__sai_tunnel_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1122

enum__sai_udf_base_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 50

SAI_UDF_BASE_L2 = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 50

SAI_UDF_BASE_L3 = (SAI_UDF_BASE_L2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 50

SAI_UDF_BASE_L4 = (SAI_UDF_BASE_L3 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 50

sai_udf_base_t = enum__sai_udf_base_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 50

enum__sai_udf_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_MATCH_ID = SAI_UDF_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_GROUP_ID = (SAI_UDF_ATTR_MATCH_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_BASE = (SAI_UDF_ATTR_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_OFFSET = (SAI_UDF_ATTR_BASE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_HASH_MASK = (SAI_UDF_ATTR_OFFSET + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_END = (SAI_UDF_ATTR_HASH_MASK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

SAI_UDF_ATTR_CUSTOM_RANGE_END = (SAI_UDF_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

sai_udf_attr_t = enum__sai_udf_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 124

enum__sai_udf_match_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_L2_TYPE = SAI_UDF_MATCH_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_L3_TYPE = (SAI_UDF_MATCH_ATTR_L2_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_GRE_TYPE = (SAI_UDF_MATCH_ATTR_L3_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_PRIORITY = (SAI_UDF_MATCH_ATTR_GRE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_END = (SAI_UDF_MATCH_ATTR_PRIORITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM = SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT = (SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT = (SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_END = (SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

sai_udf_match_attr_t = enum__sai_udf_match_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 197

enum__sai_udf_group_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

SAI_UDF_GROUP_TYPE_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

SAI_UDF_GROUP_TYPE_GENERIC = SAI_UDF_GROUP_TYPE_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

SAI_UDF_GROUP_TYPE_HASH = (SAI_UDF_GROUP_TYPE_GENERIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

SAI_UDF_GROUP_TYPE_END = (SAI_UDF_GROUP_TYPE_HASH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

sai_udf_group_type_t = enum__sai_udf_group_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 216

enum__sai_udf_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_UDF_LIST = SAI_UDF_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_TYPE = (SAI_UDF_GROUP_ATTR_UDF_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_LENGTH = (SAI_UDF_GROUP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_END = (SAI_UDF_GROUP_ATTR_LENGTH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

sai_udf_group_attr_t = enum__sai_udf_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 266

sai_create_udf_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 278

sai_remove_udf_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 291

sai_set_udf_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 302

sai_get_udf_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 315

sai_create_udf_match_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 330

sai_remove_udf_match_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 343

sai_set_udf_match_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 354

sai_get_udf_match_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 367

sai_create_udf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 382

sai_remove_udf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 395

sai_set_udf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 406

sai_get_udf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 419

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 442
class struct__sai_udf_api_t(Structure):
    pass

struct__sai_udf_api_t.__slots__ = [
    'create_udf',
    'remove_udf',
    'set_udf_attribute',
    'get_udf_attribute',
    'create_udf_match',
    'remove_udf_match',
    'set_udf_match_attribute',
    'get_udf_match_attribute',
    'create_udf_group',
    'remove_udf_group',
    'set_udf_group_attribute',
    'get_udf_group_attribute',
]
struct__sai_udf_api_t._fields_ = [
    ('create_udf', sai_create_udf_fn),
    ('remove_udf', sai_remove_udf_fn),
    ('set_udf_attribute', sai_set_udf_attribute_fn),
    ('get_udf_attribute', sai_get_udf_attribute_fn),
    ('create_udf_match', sai_create_udf_match_fn),
    ('remove_udf_match', sai_remove_udf_match_fn),
    ('set_udf_match_attribute', sai_set_udf_match_attribute_fn),
    ('get_udf_match_attribute', sai_get_udf_match_attribute_fn),
    ('create_udf_group', sai_create_udf_group_fn),
    ('remove_udf_group', sai_remove_udf_group_fn),
    ('set_udf_group_attribute', sai_set_udf_group_attribute_fn),
    ('get_udf_group_attribute', sai_get_udf_group_attribute_fn),
]

sai_udf_api_t = struct__sai_udf_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 442

enum__sai_virtual_router_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE = SAI_VIRTUAL_ROUTER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE = (SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS = (SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_END = (SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_END = (SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

sai_virtual_router_attr_t = enum__sai_virtual_router_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 120

sai_create_virtual_router_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 134

sai_remove_virtual_router_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 147

sai_set_virtual_router_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 158

sai_get_virtual_router_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 171

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 186
class struct__sai_virtual_router_api_t(Structure):
    pass

struct__sai_virtual_router_api_t.__slots__ = [
    'create_virtual_router',
    'remove_virtual_router',
    'set_virtual_router_attribute',
    'get_virtual_router_attribute',
]
struct__sai_virtual_router_api_t._fields_ = [
    ('create_virtual_router', sai_create_virtual_router_fn),
    ('remove_virtual_router', sai_remove_virtual_router_fn),
    ('set_virtual_router_attribute', sai_set_virtual_router_attribute_fn),
    ('get_virtual_router_attribute', sai_get_virtual_router_attribute_fn),
]

sai_virtual_router_api_t = struct__sai_virtual_router_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 186

enum__sai_vlan_tagging_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_UNTAGGED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_TAGGED = (SAI_VLAN_TAGGING_MODE_UNTAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_PRIORITY_TAGGED = (SAI_VLAN_TAGGING_MODE_TAGGED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 52

sai_vlan_tagging_mode_t = enum__sai_vlan_tagging_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 52

enum__sai_vlan_mcast_lookup_key_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

sai_vlan_mcast_lookup_key_type_t = enum__sai_vlan_mcast_lookup_key_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 67

enum__sai_vlan_flood_control_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_ALL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_NONE = (SAI_VLAN_FLOOD_CONTROL_TYPE_ALL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP = (SAI_VLAN_FLOOD_CONTROL_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_COMBINED = (SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

sai_vlan_flood_control_type_t = enum__sai_vlan_flood_control_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 98

enum__sai_vlan_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_VLAN_ID = SAI_VLAN_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_MEMBER_LIST = (SAI_VLAN_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = (SAI_VLAN_ATTR_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_STP_INSTANCE = (SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_LEARN_DISABLE = (SAI_VLAN_ATTR_STP_INSTANCE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = (SAI_VLAN_ATTR_LEARN_DISABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = (SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_NON_IP_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_IPV4_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_NON_IP_MCAST_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_IPV6_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_IPV4_MCAST_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_LINKLOCAL_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_IPV6_MCAST_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_INGRESS_ACL = (SAI_VLAN_ATTR_UNKNOWN_LINKLOCAL_MCAST_OUTPUT_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_EGRESS_ACL = (SAI_VLAN_ATTR_INGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_META_DATA = (SAI_VLAN_ATTR_EGRESS_ACL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_META_DATA + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP = (SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP = (SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_BROADCAST_FLOOD_GROUP = (SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_PTP_DOMAIN_ID = (SAI_VLAN_ATTR_BROADCAST_FLOOD_GROUP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_END = (SAI_VLAN_ATTR_PTP_DOMAIN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = (SAI_VLAN_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = (SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_TAM_OBJECT = (SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

SAI_VLAN_ATTR_CUSTOM_RANGE_END = (SAI_VLAN_ATTR_TAM_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

sai_vlan_attr_t = enum__sai_vlan_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 442

enum__sai_vlan_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_VLAN_ID = SAI_VLAN_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID = (SAI_VLAN_MEMBER_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE = (SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_END = (SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

sai_vlan_member_attr_t = enum__sai_vlan_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 494

enum__sai_vlan_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_OCTETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_PACKETS = (SAI_VLAN_STAT_IN_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_UCAST_PKTS = (SAI_VLAN_STAT_IN_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_NON_UCAST_PKTS = (SAI_VLAN_STAT_IN_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_DISCARDS = (SAI_VLAN_STAT_IN_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_ERRORS = (SAI_VLAN_STAT_IN_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_IN_UNKNOWN_PROTOS = (SAI_VLAN_STAT_IN_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_OCTETS = (SAI_VLAN_STAT_IN_UNKNOWN_PROTOS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_PACKETS = (SAI_VLAN_STAT_OUT_OCTETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_UCAST_PKTS = (SAI_VLAN_STAT_OUT_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_NON_UCAST_PKTS = (SAI_VLAN_STAT_OUT_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_DISCARDS = (SAI_VLAN_STAT_OUT_NON_UCAST_PKTS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_ERRORS = (SAI_VLAN_STAT_OUT_DISCARDS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

SAI_VLAN_STAT_OUT_QLEN = (SAI_VLAN_STAT_OUT_ERRORS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

sai_vlan_stat_t = enum__sai_vlan_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 516

sai_create_vlan_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 528

sai_remove_vlan_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 541

sai_set_vlan_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 552

sai_get_vlan_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 565

sai_create_vlan_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 580

sai_remove_vlan_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 593

sai_set_vlan_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 604

sai_get_vlan_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 617

sai_get_vlan_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 632

sai_get_vlan_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 649

sai_clear_vlan_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 665

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 689
class struct__sai_vlan_api_t(Structure):
    pass

struct__sai_vlan_api_t.__slots__ = [
    'create_vlan',
    'remove_vlan',
    'set_vlan_attribute',
    'get_vlan_attribute',
    'create_vlan_member',
    'remove_vlan_member',
    'set_vlan_member_attribute',
    'get_vlan_member_attribute',
    'create_vlan_members',
    'remove_vlan_members',
    'get_vlan_stats',
    'get_vlan_stats_ext',
    'clear_vlan_stats',
]
struct__sai_vlan_api_t._fields_ = [
    ('create_vlan', sai_create_vlan_fn),
    ('remove_vlan', sai_remove_vlan_fn),
    ('set_vlan_attribute', sai_set_vlan_attribute_fn),
    ('get_vlan_attribute', sai_get_vlan_attribute_fn),
    ('create_vlan_member', sai_create_vlan_member_fn),
    ('remove_vlan_member', sai_remove_vlan_member_fn),
    ('set_vlan_member_attribute', sai_set_vlan_member_attribute_fn),
    ('get_vlan_member_attribute', sai_get_vlan_member_attribute_fn),
    ('create_vlan_members', sai_bulk_object_create_fn),
    ('remove_vlan_members', sai_bulk_object_remove_fn),
    ('get_vlan_stats', sai_get_vlan_stats_fn),
    ('get_vlan_stats_ext', sai_get_vlan_stats_ext_fn),
    ('clear_vlan_stats', sai_clear_vlan_stats_fn),
]

sai_vlan_api_t = struct__sai_vlan_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 689

enum__sai_ecn_mark_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN = (SAI_ECN_MARK_MODE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_YELLOW = (SAI_ECN_MARK_MODE_GREEN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_RED = (SAI_ECN_MARK_MODE_YELLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN_YELLOW = (SAI_ECN_MARK_MODE_RED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN_RED = (SAI_ECN_MARK_MODE_GREEN_YELLOW + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_YELLOW_RED = (SAI_ECN_MARK_MODE_GREEN_RED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_ALL = (SAI_ECN_MARK_MODE_YELLOW_RED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

sai_ecn_mark_mode_t = enum__sai_ecn_mark_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 65

enum__sai_wred_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_GREEN_ENABLE = SAI_WRED_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_GREEN_MIN_THRESHOLD = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_GREEN_MAX_THRESHOLD = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_GREEN_DROP_PROBABILITY = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_YELLOW_ENABLE = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_RED_ENABLE = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_RED_MIN_THRESHOLD = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_RED_MAX_THRESHOLD = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_RED_DROP_PROBABILITY = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_WEIGHT = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_MARK_MODE = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_GREEN_MIN_THRESHOLD = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_GREEN_MARK_PROBABILITY = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_YELLOW_MIN_THRESHOLD = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_YELLOW_MARK_PROBABILITY = 19 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_RED_MIN_THRESHOLD = 20 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD = 21 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_RED_MARK_PROBABILITY = 22 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MIN_THRESHOLD = 23 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MAX_THRESHOLD = 24 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MARK_PROBABILITY = 25 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_END = (SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MARK_PROBABILITY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

SAI_WRED_ATTR_CUSTOM_RANGE_END = (SAI_WRED_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

sai_wred_attr_t = enum__sai_wred_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 421

sai_create_wred_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 433

sai_remove_wred_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 446

sai_set_wred_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 457

sai_get_wred_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 470

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 485
class struct__sai_wred_api_t(Structure):
    pass

struct__sai_wred_api_t.__slots__ = [
    'create_wred',
    'remove_wred',
    'set_wred_attribute',
    'get_wred_attribute',
]
struct__sai_wred_api_t._fields_ = [
    ('create_wred', sai_create_wred_fn),
    ('remove_wred', sai_remove_wred_fn),
    ('set_wred_attribute', sai_set_wred_attribute_fn),
    ('get_wred_attribute', sai_get_wred_attribute_fn),
]

sai_wred_api_t = struct__sai_wred_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 485

enum__sai_isolation_group_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 47

SAI_ISOLATION_GROUP_TYPE_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 47

SAI_ISOLATION_GROUP_TYPE_BRIDGE_PORT = (SAI_ISOLATION_GROUP_TYPE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 47

sai_isolation_group_type_t = enum__sai_isolation_group_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 47

enum__sai_isolation_group_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_TYPE = SAI_ISOLATION_GROUP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST = (SAI_ISOLATION_GROUP_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_END = (SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

sai_isolation_group_attr_t = enum__sai_isolation_group_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 87

enum__sai_isolation_group_member_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID = SAI_ISOLATION_GROUP_MEMBER_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT = (SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_END = (SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

sai_isolation_group_member_attr_t = enum__sai_isolation_group_member_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 130

sai_create_isolation_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 142

sai_remove_isolation_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 155

sai_set_isolation_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 166

sai_get_isolation_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 179

sai_create_isolation_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 194

sai_remove_isolation_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 207

sai_set_isolation_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 218

sai_get_isolation_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 231

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 250
class struct__sai_isolation_group_api_t(Structure):
    pass

struct__sai_isolation_group_api_t.__slots__ = [
    'create_isolation_group',
    'remove_isolation_group',
    'set_isolation_group_attribute',
    'get_isolation_group_attribute',
    'create_isolation_group_member',
    'remove_isolation_group_member',
    'set_isolation_group_member_attribute',
    'get_isolation_group_member_attribute',
]
struct__sai_isolation_group_api_t._fields_ = [
    ('create_isolation_group', sai_create_isolation_group_fn),
    ('remove_isolation_group', sai_remove_isolation_group_fn),
    ('set_isolation_group_attribute', sai_set_isolation_group_attribute_fn),
    ('get_isolation_group_attribute', sai_get_isolation_group_attribute_fn),
    ('create_isolation_group_member', sai_create_isolation_group_member_fn),
    ('remove_isolation_group_member', sai_remove_isolation_group_member_fn),
    ('set_isolation_group_member_attribute', sai_set_isolation_group_member_attribute_fn),
    ('get_isolation_group_member_attribute', sai_get_isolation_group_member_attribute_fn),
]

sai_isolation_group_api_t = struct__sai_isolation_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 250

enum__sai_twamp_session_auth_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 49

SAI_TWAMP_SESSION_MODE_AUTHENTICATED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 49

SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED = (SAI_TWAMP_SESSION_MODE_AUTHENTICATED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 49

SAI_TWAMP_SESSION_MODE_ENCRYPTED = (SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 49

sai_twamp_session_auth_mode_t = enum__sai_twamp_session_auth_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 49

enum__sai_twamp_session_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 63

SAI_TWAMP_SESSION_SENDER = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 63

SAI_TWAMP_SESSION_REFLECTOR = (SAI_TWAMP_SESSION_SENDER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 63

sai_twamp_session_role_t = enum__sai_twamp_session_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 63

enum__sai_twamp_mode_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 127

SAI_TWAMP_MODE_TWAMP_FULL = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 127

SAI_TWAMP_MODE_TWAMP_LIGHT = (SAI_TWAMP_MODE_TWAMP_FULL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 127

sai_twamp_mode_type_t = enum__sai_twamp_mode_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 127

enum__sai_twamp_pkt_tx_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 141

SAI_TWAMP_TX_MODE_CONTINUOUS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 141

SAI_TWAMP_TX_MODE_PACKET_NUM = (SAI_TWAMP_TX_MODE_CONTINUOUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 141

SAI_TWAMP_TX_MODE_PERIOD = (SAI_TWAMP_TX_MODE_PACKET_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 141

sai_twamp_pkt_tx_mode_t = enum__sai_twamp_pkt_tx_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 141

enum__sai_twamp_timestamp_format_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 158

SAI_TWAMP_MODE_TIMESTAMP_FORMAT_NTP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 158

SAI_TWAMP_MODE_TIMESTAMP_FORMAT_PTP = (SAI_TWAMP_MODE_TIMESTAMP_FORMAT_NTP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 158

sai_twamp_timestamp_format_t = enum__sai_twamp_timestamp_format_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 158

enum__sai_twamp_encapsulation_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 183

SAI_TWAMP_ENCAPSULATION_TYPE_IP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 183

SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI = (SAI_TWAMP_ENCAPSULATION_TYPE_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 183

SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI = (SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 183

sai_twamp_encapsulation_type_t = enum__sai_twamp_encapsulation_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 183

enum__sai_twamp_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TWAMP_PORT = SAI_TWAMP_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT = (SAI_TWAMP_SESSION_ATTR_TWAMP_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_SESSION_ROLE = (SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT = (SAI_TWAMP_SESSION_ATTR_SESSION_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT = (SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_SRC_IP = (SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_DST_IP = (SAI_TWAMP_SESSION_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TC = (SAI_TWAMP_SESSION_ATTR_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TTL = (SAI_TWAMP_SESSION_ATTR_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER = (SAI_TWAMP_SESSION_ATTR_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE = (SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = (SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID = (SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH = (SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_AUTH_MODE = (SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID = (SAI_TWAMP_SESSION_ATTR_AUTH_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TX_RATE = (SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_PKT_TX_MODE = (SAI_TWAMP_SESSION_ATTR_TX_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION = (SAI_TWAMP_SESSION_ATTR_PKT_TX_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT = (SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD = (SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_MODE = (SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT = (SAI_TWAMP_SESSION_ATTR_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_END = (SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

sai_twamp_session_attr_t = enum__sai_twamp_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 414

enum__sai_twamp_session_stats_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_RX_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_RX_BYTE = (SAI_TWAMP_SESSION_STATS_RX_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_TX_PACKETS = (SAI_TWAMP_SESSION_STATS_RX_BYTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_TX_BYTE = (SAI_TWAMP_SESSION_STATS_TX_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_DROP_PACKETS = (SAI_TWAMP_SESSION_STATS_TX_BYTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_MAX_LATENCY = (SAI_TWAMP_SESSION_STATS_DROP_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_MIN_LATENCY = (SAI_TWAMP_SESSION_STATS_MAX_LATENCY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_AVG_LATENCY = (SAI_TWAMP_SESSION_STATS_MIN_LATENCY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_MAX_JITTER = (SAI_TWAMP_SESSION_STATS_AVG_LATENCY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_MIN_JITTER = (SAI_TWAMP_SESSION_STATS_MAX_JITTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_AVG_JITTER = (SAI_TWAMP_SESSION_STATS_MIN_JITTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_FIRST_TS = (SAI_TWAMP_SESSION_STATS_AVG_JITTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_LAST_TS = (SAI_TWAMP_SESSION_STATS_FIRST_TS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

SAI_TWAMP_SESSION_STATS_DURATION_TS = (SAI_TWAMP_SESSION_STATS_LAST_TS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

sai_twamp_session_stats_t = enum__sai_twamp_session_stats_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 463

sai_create_twamp_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 477

sai_remove_twamp_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 491

sai_set_twamp_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 503

sai_get_twamp_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 517

sai_get_twamp_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 533

sai_clear_twamp_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 548

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 565
class struct__sai_twamp_api_t(Structure):
    pass

struct__sai_twamp_api_t.__slots__ = [
    'create_twamp_session',
    'remove_twamp_session',
    'set_twamp_session_attribute',
    'get_twamp_session_attribute',
    'get_twamp_session_stats',
    'clear_twamp_session_stats',
]
struct__sai_twamp_api_t._fields_ = [
    ('create_twamp_session', sai_create_twamp_session_fn),
    ('remove_twamp_session', sai_remove_twamp_session_fn),
    ('set_twamp_session_attribute', sai_set_twamp_session_attribute_fn),
    ('get_twamp_session_attribute', sai_get_twamp_session_attribute_fn),
    ('get_twamp_session_stats', sai_get_twamp_session_stats_fn),
    ('clear_twamp_session_stats', sai_clear_twamp_session_stats_fn),
]

sai_twamp_api_t = struct__sai_twamp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 565

enum__sai_y1731_meg_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

SAI_Y1731_MEG_TYPE_ETHER_VLAN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

SAI_Y1731_MEG_TYPE_L2VPN_VLAN = (SAI_Y1731_MEG_TYPE_ETHER_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

SAI_Y1731_MEG_TYPE_L2VPN_VPLS = (SAI_Y1731_MEG_TYPE_L2VPN_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

SAI_Y1731_MEG_TYPE_L2VPN_VPWS = (SAI_Y1731_MEG_TYPE_L2VPN_VPLS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

SAI_Y1731_MEG_TYPE_MPLS_TP = (SAI_Y1731_MEG_TYPE_L2VPN_VPWS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

sai_y1731_meg_type_t = enum__sai_y1731_meg_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 55

enum__sai_y1731_meg_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_TYPE = SAI_Y1731_MEG_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_NAME = (SAI_Y1731_MEG_ATTR_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_LEVEL = (SAI_Y1731_MEG_ATTR_NAME + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_END = (SAI_Y1731_MEG_ATTR_LEVEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

SAI_Y1731_MEG_ATTR_CUSTOM_RANGE_END = (SAI_Y1731_MEG_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

sai_y1731_meg_attr_t = enum__sai_y1731_meg_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 105

enum__sai_y1731_remote_mep_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID = SAI_Y1731_REMOTE_MEP_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID = (SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS = (SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED = (SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_END = (SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

SAI_Y1731_REMOTE_MEP_ATTR_CUSTOM_RANGE_END = (SAI_Y1731_REMOTE_MEP_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

sai_y1731_remote_mep_attr_t = enum__sai_y1731_remote_mep_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 163

enum__sai_y1731_session_direction_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 179

SAI_Y1731_SESSION_DIR_DOWNMEP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 179

SAI_Y1731_SESSION_DIR_UPMEP = (SAI_Y1731_SESSION_DIR_DOWNMEP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 179

SAI_Y1731_SESSION_DIR_NODEMEP = (SAI_Y1731_SESSION_DIR_UPMEP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 179

sai_y1731_session_direction_t = enum__sai_y1731_session_direction_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 179

enum__sai_y1731_session_ccm_period_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_0 = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_1 = (SAI_Y1731_SESSION_CCM_PERIOD_0 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_2 = (SAI_Y1731_SESSION_CCM_PERIOD_1 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_3 = (SAI_Y1731_SESSION_CCM_PERIOD_2 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_4 = (SAI_Y1731_SESSION_CCM_PERIOD_3 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_5 = (SAI_Y1731_SESSION_CCM_PERIOD_4 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_6 = (SAI_Y1731_SESSION_CCM_PERIOD_5 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

SAI_Y1731_SESSION_CCM_PERIOD_7 = (SAI_Y1731_SESSION_CCM_PERIOD_6 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

sai_y1731_session_ccm_period_t = enum__sai_y1731_session_ccm_period_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 210

enum__sai_y1731_session_performance_monitor_offload_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 232

SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 232

SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL = (SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 232

SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_PARTIAL = (SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 232

sai_y1731_session_performance_monitor_offload_type_t = enum__sai_y1731_session_performance_monitor_offload_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 232

enum__sai_y1731_session_lm_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 245

SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 245

SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED = (SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 245

sai_y1731_session_lm_type_t = enum__sai_y1731_session_lm_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 245

enum__sai_y1731_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_MEG = SAI_Y1731_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_DIR = (SAI_Y1731_SESSION_ATTR_MEG + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_VLAN_ID = (SAI_Y1731_SESSION_ATTR_DIR + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_BRIDGE_ID = (SAI_Y1731_SESSION_ATTR_VLAN_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_PORT_ID = (SAI_Y1731_SESSION_ATTR_BRIDGE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL = (SAI_Y1731_SESSION_ATTR_PORT_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID = (SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_CCM_PERIOD = (SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_CCM_ENABLE = (SAI_Y1731_SESSION_ATTR_CCM_PERIOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST = (SAI_Y1731_SESSION_ATTR_CCM_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE = (SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_LM_ENABLE = (SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_LM_TYPE = (SAI_Y1731_SESSION_ATTR_LM_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE = (SAI_Y1731_SESSION_ATTR_LM_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_DM_ENABLE = (SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_LOCAL_RDI = (SAI_Y1731_SESSION_ATTR_DM_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID = (SAI_Y1731_SESSION_ATTR_LOCAL_RDI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL = (SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_TTL = (SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_EXP_OR_COS = (SAI_Y1731_SESSION_ATTR_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID = (SAI_Y1731_SESSION_ATTR_EXP_OR_COS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_END = (SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

SAI_Y1731_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_Y1731_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

sai_y1731_session_attr_t = enum__sai_y1731_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 468

enum__sai_y1731_lm_stat_id_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

SAI_Y1731_SESSION_LM_STAT_TX_FCF = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

SAI_Y1731_SESSION_LM_STAT_RX_FCB = (SAI_Y1731_SESSION_LM_STAT_TX_FCF + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

SAI_Y1731_SESSION_LM_STAT_TX_FCB = (SAI_Y1731_SESSION_LM_STAT_RX_FCB + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

SAI_Y1731_SESSION_LM_STAT_RX_FCL = (SAI_Y1731_SESSION_LM_STAT_TX_FCB + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

sai_lm_stat_id_t = enum__sai_y1731_lm_stat_id_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 488

enum__sai_y1731_session_notify_event_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_MISMERGE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_LEVEL = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_MISMERGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_MEP = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_LEVEL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_PERIOD = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_MEP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_DLOC = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_PERIOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_SRC_MAC_MISMATCH = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_DLOC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_RX = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_SRC_MAC_MISMATCH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_TX = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_RX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_CONNECTION_ESTABLISHED = (SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_TX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

sai_y1731_session_notify_event_type_t = enum__sai_y1731_session_notify_event_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 524

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 540
class struct__sai_y1731_session_event_notification_t(Structure):
    pass

struct__sai_y1731_session_event_notification_t.__slots__ = [
    'y1731_oid',
    'session_event_list',
]
struct__sai_y1731_session_event_notification_t._fields_ = [
    ('y1731_oid', sai_object_id_t),
    ('session_event_list', sai_s32_list_t),
]

sai_y1731_session_event_notification_t = struct__sai_y1731_session_event_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 540

sai_create_y1731_meg_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 554

sai_remove_y1731_meg_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 568

sai_set_y1731_meg_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 580

sai_get_y1731_meg_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 594

sai_create_y1731_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 610

sai_remove_y1731_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 624

sai_set_y1731_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 636

sai_get_y1731_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 650

sai_create_y1731_remote_mep_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 666

sai_remove_y1731_remote_mep_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 680

sai_set_y1731_remote_mep_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 692

sai_get_y1731_remote_mep_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 706

sai_get_y1731_session_lm_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 722

sai_y1731_session_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_y1731_session_event_notification_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 739

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 765
class struct__sai_y1731_api_t(Structure):
    pass

struct__sai_y1731_api_t.__slots__ = [
    'create_y1731_meg',
    'remove_y1731_meg',
    'set_y1731_meg_attribute',
    'get_y1731_meg_attribute',
    'create_y1731_session',
    'remove_y1731_session',
    'set_y1731_session_attribute',
    'get_y1731_session_attribute',
    'create_y1731_remote_mep',
    'remove_y1731_remote_mep',
    'set_y1731_remote_mep_attribute',
    'get_y1731_remote_mep_attribute',
    'get_y1731_session_lm_stats',
]
struct__sai_y1731_api_t._fields_ = [
    ('create_y1731_meg', sai_create_y1731_meg_fn),
    ('remove_y1731_meg', sai_remove_y1731_meg_fn),
    ('set_y1731_meg_attribute', sai_set_y1731_meg_attribute_fn),
    ('get_y1731_meg_attribute', sai_get_y1731_meg_attribute_fn),
    ('create_y1731_session', sai_create_y1731_session_fn),
    ('remove_y1731_session', sai_remove_y1731_session_fn),
    ('set_y1731_session_attribute', sai_set_y1731_session_attribute_fn),
    ('get_y1731_session_attribute', sai_get_y1731_session_attribute_fn),
    ('create_y1731_remote_mep', sai_create_y1731_remote_mep_fn),
    ('remove_y1731_remote_mep', sai_remove_y1731_remote_mep_fn),
    ('set_y1731_remote_mep_attribute', sai_set_y1731_remote_mep_attribute_fn),
    ('get_y1731_remote_mep_attribute', sai_get_y1731_remote_mep_attribute_fn),
    ('get_y1731_session_lm_stats', sai_get_y1731_session_lm_stats_fn),
]

sai_y1731_api_t = struct__sai_y1731_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 765

enum__sai_ptp_device_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

SAI_PTP_DEVICE_NONE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

SAI_PTP_DEVICE_OC = (SAI_PTP_DEVICE_NONE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

SAI_PTP_DEVICE_BC = (SAI_PTP_DEVICE_OC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

SAI_PTP_DEVICE_E2E_TC = (SAI_PTP_DEVICE_BC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

SAI_PTP_DEVICE_P2P_TC = (SAI_PTP_DEVICE_E2E_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

sai_ptp_device_type_t = enum__sai_ptp_device_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 48

enum__sai_ptp_enable_based_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 64

SAI_PTP_ENABLE_BASED_ON_VLAN = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 64

SAI_PTP_ENABLE_BASED_ON_PORT = (SAI_PTP_ENABLE_BASED_ON_VLAN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 64

sai_ptp_enable_based_type_t = enum__sai_ptp_enable_based_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 64

enum__sai_ptp_tod_interface_format_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 82

SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375 = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 82

SAI_PTP_TOD_INTERFACE_FORMAT_ITUT_G703 = (SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 82

SAI_PTP_TOD_INTERFACE_FORMAT_USER_DEFINE = (SAI_PTP_TOD_INTERFACE_FORMAT_ITUT_G703 + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 82

sai_ptp_tod_interface_format_type_t = enum__sai_ptp_tod_interface_format_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 82

enum__sai_ptp_tod_intf_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 99

SAI_PTP_TOD_INTERFACE_INPUT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 99

SAI_PTP_TOD_INTERFACE_OUTPUT = (SAI_PTP_TOD_INTERFACE_INPUT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 99

SAI_PTP_TOD_INTERFACE_DISABLE = (SAI_PTP_TOD_INTERFACE_OUTPUT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 99

sai_ptp_tod_intf_mode_t = enum__sai_ptp_tod_intf_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 99

enum__sai_ptp_domain_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE = SAI_PTP_DOMAIN_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE = (SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET = (SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET = (SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE = (SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP = (SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP = (SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_END = (SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

SAI_PTP_DOMAIN_ATTR_CUSTOM_RANGE_END = (SAI_PTP_DOMAIN_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

sai_ptp_domain_attr_t = enum__sai_ptp_domain_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 247

sai_create_ptp_domain_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 260

sai_remove_ptp_domain_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 273

sai_set_ptp_domain_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 285

sai_get_ptp_domain_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 298

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 314
class struct__sai_ptp_api_t(Structure):
    pass

struct__sai_ptp_api_t.__slots__ = [
    'create_ptp_domain',
    'remove_ptp_domain',
    'set_ptp_domain_attribute',
    'get_ptp_domain_attribute',
]
struct__sai_ptp_api_t._fields_ = [
    ('create_ptp_domain', sai_create_ptp_domain_fn),
    ('remove_ptp_domain', sai_remove_ptp_domain_fn),
    ('set_ptp_domain_attribute', sai_set_ptp_domain_attribute_fn),
    ('get_ptp_domain_attribute', sai_get_ptp_domain_attribute_fn),
]

sai_ptp_api_t = struct__sai_ptp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 314

enum__sai_synce_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_RECOVERED_PORT = (SAI_SYNCE_ATTR_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_CLOCK_DIVIDER = (SAI_SYNCE_ATTR_RECOVERED_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_END = (SAI_SYNCE_ATTR_CLOCK_DIVIDER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

SAI_SYNCE_ATTR_CUSTOM_RANGE_END = (SAI_SYNCE_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

sai_synce_attr_t = enum__sai_synce_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 70

sai_create_synce_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 83

sai_remove_synce_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 96

sai_set_synce_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 108

sai_get_synce_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 121

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 137
class struct__sai_synce_api_t(Structure):
    pass

struct__sai_synce_api_t.__slots__ = [
    'create_synce',
    'remove_synce',
    'set_synce_attribute',
    'get_synce_attribute',
]
struct__sai_synce_api_t._fields_ = [
    ('create_synce', sai_create_synce_fn),
    ('remove_synce', sai_remove_synce_fn),
    ('set_synce_attribute', sai_set_synce_attribute_fn),
    ('get_synce_attribute', sai_get_synce_attribute_fn),
]

sai_synce_api_t = struct__sai_synce_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 137

enum__sai_npm_session_direction_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 45

SAI_NPM_SESSION_INGRESS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 45

SAI_NPM_SESSION_EGRESS = (SAI_NPM_SESSION_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 45

sai_npm_session_direction_t = enum__sai_npm_session_direction_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 45

enum__sai_npm_session_role_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 58

SAI_NPM_SESSION_SENDER = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 58

SAI_NPM_SESSION_REFLECTOR = (SAI_NPM_SESSION_SENDER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 58

sai_npm_session_role_t = enum__sai_npm_session_role_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 58

enum__sai_npm_session_color_mode_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 68

SAI_NPM_SESSION_COLOR_AWARE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 68

SAI_NPM_SESSION_COLOR_BLIND = (SAI_NPM_SESSION_COLOR_AWARE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 68

sai_npm_session_color_mode_t = enum__sai_npm_session_color_mode_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 68

enum_sai_npm_pkt_tx_mode_e = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 79

SAI_NPM_TX_MODE_CONTINUOUS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 79

SAI_NPM_TX_MODE_PACKET_NUM = (SAI_NPM_TX_MODE_CONTINUOUS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 79

SAI_NPM_TX_MODE_PERIOD = (SAI_NPM_TX_MODE_PACKET_NUM + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 79

sai_npm_pkt_tx_mode_t = enum_sai_npm_pkt_tx_mode_e # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 79

enum__sai_npm_encapsulation_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 103

SAI_NPM_ENCAPSULATION_TYPE_IP = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 103

SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI = (SAI_NPM_ENCAPSULATION_TYPE_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 103

SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI = (SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 103

sai_npm_encapsulation_type_t = enum__sai_npm_encapsulation_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 103

enum__sai_npm_session_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_NPM_PORT = SAI_NPM_SESSION_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_RECEIVE_PORT = (SAI_NPM_SESSION_ATTR_NPM_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_COLOR_MODE = (SAI_NPM_SESSION_ATTR_RECEIVE_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_SESSION_ROLE = (SAI_NPM_SESSION_ATTR_COLOR_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_UDP_SRC_PORT = (SAI_NPM_SESSION_ATTR_SESSION_ROLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_UDP_DST_PORT = (SAI_NPM_SESSION_ATTR_UDP_SRC_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_SRC_IP = (SAI_NPM_SESSION_ATTR_UDP_DST_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_DST_IP = (SAI_NPM_SESSION_ATTR_SRC_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TC = (SAI_NPM_SESSION_ATTR_DST_IP + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TTL = (SAI_NPM_SESSION_ATTR_TC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER = (SAI_NPM_SESSION_ATTR_TTL + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE = (SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = (SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID = (SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_PACKET_LENGTH = (SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_PKT_TX_MODE = (SAI_NPM_SESSION_ATTR_PACKET_LENGTH + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD = (SAI_NPM_SESSION_ATTR_PKT_TX_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TX_RATE = (SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TX_PKT_CNT = (SAI_NPM_SESSION_ATTR_TX_RATE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_TX_PKT_DURATION = (SAI_NPM_SESSION_ATTR_TX_PKT_CNT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_END = (SAI_NPM_SESSION_ATTR_TX_PKT_DURATION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

SAI_NPM_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_NPM_SESSION_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

sai_npm_session_attr_t = enum__sai_npm_session_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 298

enum__sai_npm_session_stats_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

SAI_NPM_SESSION_STATS_RX_PACKETS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

SAI_NPM_SESSION_STATS_RX_BYTE = (SAI_NPM_SESSION_STATS_RX_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

SAI_NPM_SESSION_STATS_TX_PACKETS = (SAI_NPM_SESSION_STATS_RX_BYTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

SAI_NPM_SESSION_STATS_TX_BYTE = (SAI_NPM_SESSION_STATS_TX_PACKETS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

SAI_NPM_SESSION_STATS_DROP_PACKETS = (SAI_NPM_SESSION_STATS_TX_BYTE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

sai_npm_session_stats_t = enum__sai_npm_session_stats_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 320

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 333
class struct_sai_npm_session_status_notification_s(Structure):
    pass

struct_sai_npm_session_status_notification_s.__slots__ = [
    'npm_session_id',
    'session_stats',
]
struct_sai_npm_session_status_notification_s._fields_ = [
    ('npm_session_id', sai_object_id_t),
    ('session_stats', sai_npm_session_stats_t),
]

sai_npm_session_status_notification_t = struct_sai_npm_session_status_notification_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 333

sai_create_npm_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 347

sai_remove_npm_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 361

sai_set_npm_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 373

sai_get_npm_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 387

sai_get_npm_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 403

sai_clear_npm_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_stat_id_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 418

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 435
class struct__sai_npm_api_t(Structure):
    pass

struct__sai_npm_api_t.__slots__ = [
    'create_npm_session',
    'remove_npm_session',
    'set_npm_session_attribute',
    'get_npm_session_attribute',
    'get_npm_session_stats',
    'clear_npm_session_stats',
]
struct__sai_npm_api_t._fields_ = [
    ('create_npm_session', sai_create_npm_session_fn),
    ('remove_npm_session', sai_remove_npm_session_fn),
    ('set_npm_session_attribute', sai_set_npm_session_attribute_fn),
    ('get_npm_session_attribute', sai_get_npm_session_attribute_fn),
    ('get_npm_session_stats', sai_get_npm_session_stats_fn),
    ('clear_npm_session_stats', sai_clear_npm_session_stats_fn),
]

sai_npm_api_t = struct__sai_npm_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 435

enum__sai_monitor_buffer_monitor_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT = SAI_MONITOR_BUFFER_MONITOR_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN = (SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX = (SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE = (SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE = (SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK = (SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK = (SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK = (SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK = (SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_END = (SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

SAI_MONITOR_BUFFER_MONITOR_ATTR_CUSTOM_RANGE_END = (SAI_MONITOR_BUFFER_MONITOR_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

sai_monitor_buffer_monitor_attr_t = enum__sai_monitor_buffer_monitor_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 129

enum__sai_monitor_latency_monitor_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT = SAI_MONITOR_LATENCY_MONITOR_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_MB_ENABLE = (SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_MB_LEVEL_OVERTHRD_EVENT = (SAI_MONITOR_LATENCY_MONITOR_ATTR_MB_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE = (SAI_MONITOR_LATENCY_MONITOR_ATTR_MB_LEVEL_OVERTHRD_EVENT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD = (SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK = (SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_END = (SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

SAI_MONITOR_LATENCY_MONITOR_ATTR_CUSTOM_RANGE_END = (SAI_MONITOR_LATENCY_MONITOR_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

sai_monitor_latency_monitor_attr_t = enum__sai_monitor_latency_monitor_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 205

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 224
class struct_sai_monitor_mburst_stats_s(Structure):
    pass

struct_sai_monitor_mburst_stats_s.__slots__ = [
    'buffer_monitor_microburst_port',
    'buffer_monitor_microburst_threshold_cnt',
]
struct_sai_monitor_mburst_stats_s._fields_ = [
    ('buffer_monitor_microburst_port', sai_object_id_t),
    ('buffer_monitor_microburst_threshold_cnt', c_uint32 * 8),
]

sai_monitor_mburst_stats_t = struct_sai_monitor_mburst_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 224

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 229
class struct_sai_monitor_buffer_event_s(Structure):
    pass

struct_sai_monitor_buffer_event_s.__slots__ = [
    'buffer_monitor_event_port',
    'buffer_monitor_event_total_cnt',
    'buffer_monitor_event_port_unicast_cnt',
    'buffer_monitor_event_port_multicast_cnt',
    'buffer_monitor_event_stats',
]
struct_sai_monitor_buffer_event_s._fields_ = [
    ('buffer_monitor_event_port', sai_object_id_t),
    ('buffer_monitor_event_total_cnt', c_uint32),
    ('buffer_monitor_event_port_unicast_cnt', c_uint32),
    ('buffer_monitor_event_port_multicast_cnt', c_uint32),
    ('buffer_monitor_event_stats', c_uint8),
]

sai_monitor_buffer_event_t = struct_sai_monitor_buffer_event_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 238

enum__sai_buffer_monitor_stats_direction_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 248

SAI_MONITOR_INGRESS = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 248

SAI_MONITOR_EGRESS = (SAI_MONITOR_INGRESS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 248

sai_buffer_monitor_stats_direction_t = enum__sai_buffer_monitor_stats_direction_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 248

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 253
class struct_sai_monitor_buffer_stats_s(Structure):
    pass

struct_sai_monitor_buffer_stats_s.__slots__ = [
    'buffer_monitor_stats_port',
    'buffer_monitor_stats_queue',
    'buffer_monitor_stats_direction',
    'buffer_monitor_stats_port_cnt',
    'buffer_monitor_stats_queue_cnt',
    'buffer_monitor_event_stats',
]
struct_sai_monitor_buffer_stats_s._fields_ = [
    ('buffer_monitor_stats_port', sai_object_id_t),
    ('buffer_monitor_stats_queue', sai_object_id_t),
    ('buffer_monitor_stats_direction', c_uint32),
    ('buffer_monitor_stats_port_cnt', c_uint32),
    ('buffer_monitor_stats_queue_cnt', c_uint32),
    ('buffer_monitor_event_stats', c_uint8),
]

sai_monitor_buffer_stats_t = struct_sai_monitor_buffer_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 264

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 269
class struct_sai_monitor_latency_event_s(Structure):
    pass

struct_sai_monitor_latency_event_s.__slots__ = [
    'latency_monitor_event_port',
    'latency_monitor_event_latency',
    'latency_monitor_event_level',
    'latency_monitor_event_state',
    'latency_monitor_event_source_port',
]
struct_sai_monitor_latency_event_s._fields_ = [
    ('latency_monitor_event_port', sai_object_id_t),
    ('latency_monitor_event_latency', c_uint64),
    ('latency_monitor_event_level', c_uint8),
    ('latency_monitor_event_state', c_uint8),
    ('latency_monitor_event_source_port', c_uint32),
]

sai_monitor_latency_event_t = struct_sai_monitor_latency_event_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 278

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 283
class struct_sai_monitor_latency_stats_s(Structure):
    pass

struct_sai_monitor_latency_stats_s.__slots__ = [
    'latency_monitor_stats_port',
    'latency_monitor_stats_level_cnt',
]
struct_sai_monitor_latency_stats_s._fields_ = [
    ('latency_monitor_stats_port', sai_object_id_t),
    ('latency_monitor_stats_level_cnt', c_uint32 * 8),
]

sai_monitor_latency_stats_t = struct_sai_monitor_latency_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 289

enum__sai_buffer_monitor_message_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 301

SAI_MONITOR_BUFFER_EVENT_MESSAGE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 301

SAI_MONITOR_BUFFER_STATS_MESSAGE = (SAI_MONITOR_BUFFER_EVENT_MESSAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 301

SAI_MONITOR_MICORBURST_STATS_MESSAGE = (SAI_MONITOR_BUFFER_STATS_MESSAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 301

sai_buffer_monitor_message_type_t = enum__sai_buffer_monitor_message_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 301

enum__sai_buffer_monitor_based_on_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 311

SAI_MONITOR_BUFFER_BASED_ON_PORT = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 311

SAI_MONITOR_BUFFER_BASED_ON_TOTAL = (SAI_MONITOR_BUFFER_BASED_ON_PORT + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 311

sai_buffer_monitor_based_on_type_t = enum__sai_buffer_monitor_based_on_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 311

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 329
class union_anon_15(Union):
    pass

union_anon_15.__slots__ = [
    'buffer_event',
    'buffer_stats',
    'microburst_stats',
]
union_anon_15._fields_ = [
    ('buffer_event', sai_monitor_buffer_event_t),
    ('buffer_stats', sai_monitor_buffer_stats_t),
    ('microburst_stats', sai_monitor_mburst_stats_t),
]

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 339
class struct__sai_monitor_buffer_notification_data_t(Structure):
    pass

struct__sai_monitor_buffer_notification_data_t.__slots__ = [
    'monitor_buffer_id',
    'buffer_monitor_message_type',
    'buffer_monitor_based_on_type',
    'u',
]
struct__sai_monitor_buffer_notification_data_t._fields_ = [
    ('monitor_buffer_id', sai_object_id_t),
    ('buffer_monitor_message_type', c_uint32),
    ('buffer_monitor_based_on_type', c_uint32),
    ('u', union_anon_15),
]

sai_monitor_buffer_notification_data_t = struct__sai_monitor_buffer_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 339

enum__sai_latency_monitor_message_type_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 350

SAI_MONITOR_LATENCY_EVENT_MESSAGE = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 350

SAI_MONITOR_LATENCY_STATS_MESSAGE = (SAI_MONITOR_LATENCY_EVENT_MESSAGE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 350

sai_latency_monitor_message_type_t = enum__sai_latency_monitor_message_type_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 350

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 365
class union_anon_16(Union):
    pass

union_anon_16.__slots__ = [
    'latency_event',
    'latency_stats',
]
union_anon_16._fields_ = [
    ('latency_event', sai_monitor_latency_event_t),
    ('latency_stats', sai_monitor_latency_stats_t),
]

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 373
class struct__sai_monitor_latency_notification_data_t(Structure):
    pass

struct__sai_monitor_latency_notification_data_t.__slots__ = [
    'monitor_latency_id',
    'latency_monitor_message_type',
    'u',
]
struct__sai_monitor_latency_notification_data_t._fields_ = [
    ('monitor_latency_id', sai_object_id_t),
    ('latency_monitor_message_type', c_uint32),
    ('u', union_anon_16),
]

sai_monitor_latency_notification_data_t = struct__sai_monitor_latency_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 373

sai_monitor_buffer_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_monitor_buffer_notification_data_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 384

sai_create_monitor_buffer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 399

sai_remove_monitor_buffer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 412

sai_set_monitor_buffer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 424

sai_get_monitor_buffer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 437

sai_monitor_latency_notification_fn = CFUNCTYPE(UNCHECKED(None), c_uint32, POINTER(sai_monitor_latency_notification_data_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 451

sai_create_monitor_latency_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 466

sai_remove_monitor_latency_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 479

sai_set_monitor_latency_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 491

sai_get_monitor_latency_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 504

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 524
class struct__sai_monitor_api_t(Structure):
    pass

struct__sai_monitor_api_t.__slots__ = [
    'create_monitor_buffer',
    'remove_monitor_buffer',
    'set_monitor_buffer_attribute',
    'get_monitor_buffer_attribute',
    'create_monitor_latency',
    'remove_monitor_latency',
    'set_monitor_latency_attribute',
    'get_monitor_latency_attribute',
]
struct__sai_monitor_api_t._fields_ = [
    ('create_monitor_buffer', sai_create_monitor_buffer_fn),
    ('remove_monitor_buffer', sai_remove_monitor_buffer_fn),
    ('set_monitor_buffer_attribute', sai_set_monitor_buffer_attribute_fn),
    ('get_monitor_buffer_attribute', sai_get_monitor_buffer_attribute_fn),
    ('create_monitor_latency', sai_create_monitor_latency_fn),
    ('remove_monitor_latency', sai_remove_monitor_latency_fn),
    ('set_monitor_latency_attribute', sai_set_monitor_latency_attribute_fn),
    ('get_monitor_latency_attribute', sai_get_monitor_latency_attribute_fn),
]

sai_monitor_api_t = struct__sai_monitor_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 524

enum__sai_api_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_UNSPECIFIED = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SWITCH = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_PORT = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_FDB = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_VLAN = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_VIRTUAL_ROUTER = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_ROUTE = 6 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_NEXT_HOP = 7 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_NEXT_HOP_GROUP = 8 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_ROUTER_INTERFACE = 9 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_NEIGHBOR = 10 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_ACL = 11 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_HOSTIF = 12 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_MIRROR = 13 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SAMPLEPACKET = 14 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_STP = 15 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_LAG = 16 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_POLICER = 17 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_WRED = 18 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_QOS_MAP = 19 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_QUEUE = 20 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SCHEDULER = 21 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SCHEDULER_GROUP = 22 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_BUFFER = 23 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_HASH = 24 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_UDF = 25 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_TUNNEL = 26 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_L2MC = 27 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_IPMC = 28 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_RPF_GROUP = 29 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_L2MC_GROUP = 30 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_IPMC_GROUP = 31 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_MCAST_FDB = 32 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_BRIDGE = 33 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_TAM = 34 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SEGMENTROUTE = 35 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_MPLS = 36 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_DTEL = 37 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_BFD = 38 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_ISOLATION_GROUP = 39 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_NAT = 40 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_COUNTER = 41 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_DEBUG_COUNTER = 42 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_TWAMP = 43 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_NPM = 44 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_ES = 45 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_Y1731 = 46 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_PTP = 47 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_SYNCE = 48 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_MONITOR = 49 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

SAI_API_MAX = 50 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

sai_api_t = enum__sai_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 149

enum__sai_log_level_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_DEBUG = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_INFO = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_NOTICE = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_WARN = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_ERROR = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

SAI_LOG_LEVEL_CRITICAL = 5 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

sai_log_level_t = enum__sai_log_level_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 174

sai_profile_get_value_fn = CFUNCTYPE(UNCHECKED(String), sai_switch_profile_id_t, String) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 176

sai_profile_get_next_value_fn = CFUNCTYPE(UNCHECKED(c_int), sai_switch_profile_id_t, POINTER(POINTER(c_char)), POINTER(POINTER(c_char))) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 180

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 204
class struct__sai_service_method_table_t(Structure):
    pass

struct__sai_service_method_table_t.__slots__ = [
    'profile_get_value',
    'profile_get_next_value',
]
struct__sai_service_method_table_t._fields_ = [
    ('profile_get_value', sai_profile_get_value_fn),
    ('profile_get_next_value', sai_profile_get_next_value_fn),
]

sai_service_method_table_t = struct__sai_service_method_table_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 204

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 216
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_api_initialize'):
        continue
    sai_api_initialize = _lib.sai_api_initialize
    sai_api_initialize.argtypes = [c_uint64, POINTER(sai_service_method_table_t)]
    sai_api_initialize.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 230
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_api_query'):
        continue
    sai_api_query = _lib.sai_api_query
    sai_api_query.argtypes = [sai_api_t, POINTER(POINTER(None))]
    sai_api_query.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 240
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_api_uninitialize'):
        continue
    sai_api_uninitialize = _lib.sai_api_uninitialize
    sai_api_uninitialize.argtypes = []
    sai_api_uninitialize.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 252
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_log_set'):
        continue
    sai_log_set = _lib.sai_log_set
    sai_log_set.argtypes = [sai_api_t, sai_log_level_t]
    sai_log_set.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 264
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_object_type_query'):
        continue
    sai_object_type_query = _lib.sai_object_type_query
    sai_object_type_query.argtypes = [sai_object_id_t]
    sai_object_type_query.restype = sai_object_type_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 277
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_switch_id_query'):
        continue
    sai_switch_id_query = _lib.sai_switch_id_query
    sai_switch_id_query.argtypes = [sai_object_id_t]
    sai_switch_id_query.restype = sai_object_id_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 287
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_dbg_generate_dump'):
        continue
    sai_dbg_generate_dump = _lib.sai_dbg_generate_dump
    sai_dbg_generate_dump.argtypes = [String]
    sai_dbg_generate_dump.restype = sai_status_t
    break

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 302
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'sai_object_type_get_availability'):
        continue
    sai_object_type_get_availability = _lib.sai_object_type_get_availability
    sai_object_type_get_availability.argtypes = [sai_object_id_t, sai_object_type_t, c_uint32, POINTER(sai_attribute_t), POINTER(c_uint64)]
    sai_object_type_get_availability.restype = sai_status_t
    break

enum__sai_tam_microburst_stat_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_LAST_DURATION = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_LONGEST_DURATION = 1 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_SHORTEST_DURATION = 2 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_AVERAGE_DURATION = 3 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_NUMBER = 4 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

SAI_TAM_MICROBURST_STAT_CUSTOM_RANGE_BASE = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

sai_tam_microburst_stat_t = enum__sai_tam_microburst_stat_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 59

enum__sai_tam_microburst_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_TAM_ID = SAI_TAM_MICROBURST_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_STATISTIC = (SAI_TAM_MICROBURST_ATTR_TAM_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_LEVEL_A = (SAI_TAM_MICROBURST_ATTR_STATISTIC + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_LEVEL_B = (SAI_TAM_MICROBURST_ATTR_LEVEL_A + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_TRANSPORTER = (SAI_TAM_MICROBURST_ATTR_LEVEL_B + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_STATS = (SAI_TAM_MICROBURST_ATTR_TRANSPORTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_END = (SAI_TAM_MICROBURST_ATTR_STATS + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

SAI_TAM_MICROBURST_ATTR_CUSTOM_RANGE_END = (SAI_TAM_MICROBURST_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

sai_tam_microburst_attr_t = enum__sai_tam_microburst_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 158

enum__sai_tam_histogram_attr_t = c_int # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_START = 0 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_TAM_ID = SAI_TAM_HISTOGRAM_ATTR_START # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_STAT_TYPE = (SAI_TAM_HISTOGRAM_ATTR_TAM_ID + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_BIN_BOUNDARY = (SAI_TAM_HISTOGRAM_ATTR_STAT_TYPE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_RESOLUTION = (SAI_TAM_HISTOGRAM_ATTR_BIN_BOUNDARY + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_CLEAR_MODE = (SAI_TAM_HISTOGRAM_ATTR_RESOLUTION + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_TRANSPORTER = (SAI_TAM_HISTOGRAM_ATTR_CLEAR_MODE + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_END = (SAI_TAM_HISTOGRAM_ATTR_TRANSPORTER + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_CUSTOM_RANGE_START = 268435456 # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

SAI_TAM_HISTOGRAM_ATTR_CUSTOM_RANGE_END = (SAI_TAM_HISTOGRAM_ATTR_CUSTOM_RANGE_START + 1) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

sai_tam_histogram_attr_t = enum__sai_tam_histogram_attr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 257

sai_create_tam_microburst_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 269

sai_remove_tam_microburst_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 282

sai_get_tam_microburst_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 294

sai_set_tam_microburst_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 307

sai_create_tam_histogram_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 325

sai_remove_tam_histogram_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 338

sai_set_tam_histogram_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 349

sai_get_tam_histogram_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, c_uint32, POINTER(sai_attribute_t)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 362

sai_get_tam_histogram_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(c_uint32), POINTER(c_uint64)) # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 379

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 395
class struct__sai_uburst_api_t(Structure):
    pass

struct__sai_uburst_api_t.__slots__ = [
    'create_tam_microburst',
    'remove_tam_microburst',
    'set_tam_microburst_attribute',
    'get_tam_microburst_attribute',
    'create_tam_histogram',
    'remove_tam_histogram',
    'set_tam_histogram_attribute',
    'get_tam_histogram_attribute',
    'get_tam_histogram_stats',
]
struct__sai_uburst_api_t._fields_ = [
    ('create_tam_microburst', sai_create_tam_microburst_fn),
    ('remove_tam_microburst', sai_remove_tam_microburst_fn),
    ('set_tam_microburst_attribute', sai_set_tam_microburst_attribute_fn),
    ('get_tam_microburst_attribute', sai_get_tam_microburst_attribute_fn),
    ('create_tam_histogram', sai_create_tam_histogram_fn),
    ('remove_tam_histogram', sai_remove_tam_histogram_fn),
    ('set_tam_histogram_attribute', sai_set_tam_histogram_attribute_fn),
    ('get_tam_histogram_attribute', sai_get_tam_histogram_attribute_fn),
    ('get_tam_histogram_stats', sai_get_tam_histogram_stats_fn),
]

sai_uburst_api_t = struct__sai_uburst_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 395

# /usr/include/linux/limits.h: 12
try:
    PATH_MAX = 4096
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 159
try:
    SAI_NULL_OBJECT_ID = 0L
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 428
try:
    SAI_ACL_USER_DEFINED_FIELD_ATTR_ID_RANGE = 255
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 30
try:
    SAI_BFD_CV_SIZE = 32
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 46
try:
    SAI_HOSTIF_NAME_SIZE = 16
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 51
try:
    SAI_HOSTIF_GENETLINK_MCGRP_NAME_SIZE = 16
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 43
def SAI_STATUS_CODE(_S_):
    return (-_S_)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 50
try:
    SAI_STATUS_SUCCESS = 0L
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 55
try:
    SAI_STATUS_FAILURE = (SAI_STATUS_CODE (1L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 60
try:
    SAI_STATUS_NOT_SUPPORTED = (SAI_STATUS_CODE (2L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 65
try:
    SAI_STATUS_NO_MEMORY = (SAI_STATUS_CODE (3L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 70
try:
    SAI_STATUS_INSUFFICIENT_RESOURCES = (SAI_STATUS_CODE (4L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 75
try:
    SAI_STATUS_INVALID_PARAMETER = (SAI_STATUS_CODE (5L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 81
try:
    SAI_STATUS_ITEM_ALREADY_EXISTS = (SAI_STATUS_CODE (6L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 87
try:
    SAI_STATUS_ITEM_NOT_FOUND = (SAI_STATUS_CODE (7L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 92
try:
    SAI_STATUS_BUFFER_OVERFLOW = (SAI_STATUS_CODE (8L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 97
try:
    SAI_STATUS_INVALID_PORT_NUMBER = (SAI_STATUS_CODE (9L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 102
try:
    SAI_STATUS_INVALID_PORT_MEMBER = (SAI_STATUS_CODE (10L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 107
try:
    SAI_STATUS_INVALID_VLAN_ID = (SAI_STATUS_CODE (11L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 112
try:
    SAI_STATUS_UNINITIALIZED = (SAI_STATUS_CODE (12L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 117
try:
    SAI_STATUS_TABLE_FULL = (SAI_STATUS_CODE (13L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 122
try:
    SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING = (SAI_STATUS_CODE (14L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 127
try:
    SAI_STATUS_NOT_IMPLEMENTED = (SAI_STATUS_CODE (15L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 132
try:
    SAI_STATUS_ADDR_NOT_FOUND = (SAI_STATUS_CODE (16L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 137
try:
    SAI_STATUS_OBJECT_IN_USE = (SAI_STATUS_CODE (17L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 145
try:
    SAI_STATUS_INVALID_OBJECT_TYPE = (SAI_STATUS_CODE (18L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 154
try:
    SAI_STATUS_INVALID_OBJECT_ID = (SAI_STATUS_CODE (19L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 159
try:
    SAI_STATUS_INVALID_NV_STORAGE = (SAI_STATUS_CODE (20L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 164
try:
    SAI_STATUS_NV_STORAGE_FULL = (SAI_STATUS_CODE (21L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 169
try:
    SAI_STATUS_SW_UPGRADE_VERSION_MISMATCH = (SAI_STATUS_CODE (22L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 174
try:
    SAI_STATUS_NOT_EXECUTED = (SAI_STATUS_CODE (23L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 191
try:
    SAI_STATUS_INVALID_ATTRIBUTE_0 = (SAI_STATUS_CODE (65536L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 196
try:
    SAI_STATUS_INVALID_ATTRIBUTE_MAX = (SAI_STATUS_CODE (131071L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 203
try:
    SAI_STATUS_INVALID_ATTR_VALUE_0 = (SAI_STATUS_CODE (131072L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 208
try:
    SAI_STATUS_INVALID_ATTR_VALUE_MAX = (SAI_STATUS_CODE (196607L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 218
try:
    SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 = (SAI_STATUS_CODE (196608L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 223
try:
    SAI_STATUS_ATTR_NOT_IMPLEMENTED_MAX = (SAI_STATUS_CODE (262143L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 233
try:
    SAI_STATUS_UNKNOWN_ATTRIBUTE_0 = (SAI_STATUS_CODE (262144L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 238
try:
    SAI_STATUS_UNKNOWN_ATTRIBUTE_MAX = (SAI_STATUS_CODE (327679L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 248
try:
    SAI_STATUS_ATTR_NOT_SUPPORTED_0 = (SAI_STATUS_CODE (327680L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 253
try:
    SAI_STATUS_ATTR_NOT_SUPPORTED_MAX = (SAI_STATUS_CODE (393215L))
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 262
def SAI_STATUS_IS_INVALID_ATTRIBUTE(x):
    return ((x & (~65535)) == SAI_STATUS_INVALID_ATTRIBUTE_0)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 267
def SAI_STATUS_IS_INVALID_ATTR_VALUE(x):
    return ((x & (~65535)) == SAI_STATUS_INVALID_ATTR_VALUE_0)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 272
def SAI_STATUS_IS_ATTR_NOT_IMPLEMENTED(x):
    return ((x & (~65535)) == SAI_STATUS_ATTR_NOT_IMPLEMENTED_0)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 277
def SAI_STATUS_IS_UNKNOWN_ATTRIBUTE(x):
    return ((x & (~65535)) == SAI_STATUS_INVALID_ATTRIBUTE_0)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistatus.h: 282
def SAI_STATUS_IS_ATTR_NOT_SUPPORTED(x):
    return ((x & (~65535)) == SAI_STATUS_ATTR_NOT_SUPPORTED_0)

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 39
try:
    SAI_MAX_HARDWARE_ID_LEN = 255
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 44
try:
    SAI_MAX_FIRMWARE_PATH_NAME_LEN = PATH_MAX
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2116
try:
    SAI_SWITCH_ATTR_MAX_KEY_STRING_LEN = 64
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2125
try:
    SAI_SWITCH_ATTR_MAX_KEY_COUNT = 16
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2134
try:
    SAI_KEY_FDB_TABLE_SIZE = 'SAI_FDB_TABLE_SIZE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2139
try:
    SAI_KEY_L3_ROUTE_TABLE_SIZE = 'SAI_L3_ROUTE_TABLE_SIZE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2144
try:
    SAI_KEY_L3_NEIGHBOR_TABLE_SIZE = 'SAI_L3_NEIGHBOR_TABLE_SIZE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2149
try:
    SAI_KEY_NUM_LAG_MEMBERS = 'SAI_NUM_LAG_MEMBERS'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2154
try:
    SAI_KEY_NUM_LAGS = 'SAI_NUM_LAGS'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2159
try:
    SAI_KEY_NUM_ECMP_MEMBERS = 'SAI_NUM_ECMP_MEMBERS'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2164
try:
    SAI_KEY_NUM_ECMP_GROUPS = 'SAI_NUM_ECMP_GROUPS'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2169
try:
    SAI_KEY_NUM_UNICAST_QUEUES = 'SAI_NUM_UNICAST_QUEUES'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2174
try:
    SAI_KEY_NUM_MULTICAST_QUEUES = 'SAI_NUM_MULTICAST_QUEUES'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2179
try:
    SAI_KEY_NUM_QUEUES = 'SAI_NUM_QUEUES'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2184
try:
    SAI_KEY_NUM_CPU_QUEUES = 'SAI_NUM_CPU_QUEUES'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2189
try:
    SAI_KEY_INIT_CONFIG_FILE = 'SAI_INIT_CONFIG_FILE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2199
try:
    SAI_KEY_BOOT_TYPE = 'SAI_BOOT_TYPE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2205
try:
    SAI_KEY_WARM_BOOT_READ_FILE = 'SAI_WARM_BOOT_READ_FILE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2211
try:
    SAI_KEY_WARM_BOOT_WRITE_FILE = 'SAI_WARM_BOOT_WRITE_FILE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2219
try:
    SAI_KEY_HW_PORT_PROFILE_ID_CONFIG_FILE = 'SAI_HW_PORT_PROFILE_ID_CONFIG_FILE'
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 39
try:
    SAI_VLAN_COUNTER_SET_DEFAULT = 0
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 27
try:
    SAI_Y1731_MEG_NAME_SIZE = 16
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 30
try:
    TOD_INTF_DISABLE = 2
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 211
try:
    SAI_MONITOR_LATENCY_THRD_LEVEL = 8
except:
    pass

# /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 212
try:
    SAI_MONITOR_MICROBURST_THRD_LEVEL = 8
except:
    pass

_sai_timespec_t = struct__sai_timespec_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 128

_sai_captured_timespec_t = struct__sai_captured_timespec_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 140

_sai_timeoffset_t = struct__sai_timeoffset_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 153

_sai_object_list_t = struct__sai_object_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 181

_sai_bool_list_t = struct__sai_bool_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 309

_sai_u8_list_t = struct__sai_u8_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 315

_sai_s8_list_t = struct__sai_s8_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 326

_sai_u16_list_t = struct__sai_u16_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 332

_sai_s16_list_t = struct__sai_s16_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 338

_sai_u32_list_t = struct__sai_u32_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 344

_sai_s32_list_t = struct__sai_s32_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 350

_sai_u32_range_t = struct__sai_u32_range_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 356

_sai_s32_range_t = struct__sai_s32_range_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 362

_sai_vlan_list_t = struct__sai_vlan_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 375

_sai_ip_addr_t = union__sai_ip_addr_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 395

_sai_ip_address_t = struct__sai_ip_address_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 403

_sai_ip_address_list_t = struct__sai_ip_address_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 409

_sai_ip_prefix_t = struct__sai_ip_prefix_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 420

_sai_acl_field_data_mask_t = union__sai_acl_field_data_mask_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 458

_sai_acl_field_data_data_t = union__sai_acl_field_data_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 509

_sai_acl_field_data_t = struct__sai_acl_field_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 544

_sai_acl_action_parameter_t = union__sai_acl_action_parameter_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 593

_sai_acl_action_data_t = struct__sai_acl_action_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 617

_sai_qos_map_params_t = struct__sai_qos_map_params_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 683

_sai_qos_map_t = struct__sai_qos_map_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 693

_sai_qos_map_list_t = struct__sai_qos_map_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 703

_sai_map_t = struct__sai_map_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 713

_sai_map_list_t = struct__sai_map_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 723

_sai_acl_capability_t = struct__sai_acl_capability_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 749

_sai_acl_resource_t = struct__sai_acl_resource_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 831

_sai_acl_resource_list_t = struct__sai_acl_resource_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 847

_sai_hmac_t = struct__sai_hmac_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 875

_sai_tlv_entry_t = union__sai_tlv_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 893

_sai_tlv_t = struct__sai_tlv_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 904

_sai_tlv_list_t = struct__sai_tlv_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 916

_sai_segment_list_t = struct__sai_segment_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 928

_sai_port_lane_eye_values_t = struct__sai_port_lane_eye_values_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 941

_sai_port_eye_values_list_t = struct__sai_port_eye_values_list_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 963

_sai_attribute_value_t = union__sai_attribute_value_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1148

_sai_attribute_t = struct__sai_attribute_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/saitypes.h: 1160

_sai_acl_api_t = struct__sai_acl_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiacl.h: 3221

_sai_bfd_session_state_notification_t = struct__sai_bfd_session_state_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 146

_sai_bfd_api_t = struct__sai_bfd_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibfd.h: 789

_sai_bridge_api_t = struct__sai_bridge_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibridge.h: 802

_sai_buffer_api_t = struct__sai_buffer_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saibuffer.h: 758

_sai_counter_api_t = struct__sai_counter_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saicounter.h: 214

_sai_debug_counter_api_t = struct__sai_debug_counter_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidebugcounter.h: 495

_sai_dtel_api_t = struct__sai_dtel_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saidtel.h: 870

_sai_es_api_t = struct__sai_es_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saies.h: 130

_sai_fdb_entry_t = struct__sai_fdb_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 71

_sai_fdb_event_notification_data_t = struct__sai_fdb_event_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 334

_sai_fdb_api_t = struct__sai_fdb_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saifdb.h: 423

_sai_hash_api_t = struct__sai_hash_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihash.h: 214

_sai_hostif_api_t = struct__sai_hostif_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saihostif.h: 1417

_sai_ipmc_group_api_t = struct__sai_ipmc_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmcgroup.h: 232

_sai_ipmc_entry_t = struct__sai_ipmc_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 76

_sai_ipmc_api_t = struct__sai_ipmc_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiipmc.h: 195

_sai_l2mc_group_api_t = struct__sai_l2mc_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mcgroup.h: 242

_sai_l2mc_entry_t = struct__sai_l2mc_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 76

_sai_l2mc_api_t = struct__sai_l2mc_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sail2mc.h: 184

_sai_lag_api_t = struct__sai_lag_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sailag.h: 380

_sai_mcast_fdb_entry_t = struct__sai_mcast_fdb_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 58

_sai_mcast_fdb_api_t = struct__sai_mcast_fdb_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimcastfdb.h: 174

_sai_mirror_api_t = struct__sai_mirror_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimirror.h: 403

_sai_inseg_entry_t = struct__sai_inseg_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 309

_sai_mpls_api_t = struct__sai_mpls_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimpls.h: 371

_sai_neighbor_entry_t = struct__sai_neighbor_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 155

_sai_neighbor_api_t = struct__sai_neighbor_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saineighbor.h: 232

_sai_next_hop_group_api_t = struct__sai_next_hop_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthopgroup.h: 354

_sai_next_hop_api_t = struct__sai_next_hop_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainexthop.h: 394

_sai_route_entry_t = struct__sai_route_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 168

_sai_route_api_t = struct__sai_route_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sairoute.h: 331

_sai_nat_entry_key_t = struct__sai_nat_entry_key_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 269

_sai_nat_entry_mask_t = struct__sai_nat_entry_mask_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 301

_sai_nat_entry_data_t = struct__sai_nat_entry_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 315

_sai_nat_entry_t = struct__sai_nat_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 341

_sai_nat_api_t = struct__sai_nat_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/test/neo_saithrift/../../inc/sainat.h: 656

_sai_object_key_entry_t = union__sai_object_key_entry_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 80

_sai_object_key_t = struct__sai_object_key_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 94

_sai_attr_capability_t = struct__sai_attr_capability_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiobject.h: 115

_sai_policer_api_t = struct__sai_policer_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saipolicer.h: 374

_sai_port_oper_status_notification_t = struct__sai_port_oper_status_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 86

_sai_port_sd_notification_t = struct__sai_port_sd_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 1913

_sai_port_api_t = struct__sai_port_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiport.h: 2533

_sai_qos_map_api_t = struct__sai_qos_map_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqosmap.h: 191

_sai_queue_deadlock_notification_data_t = struct__sai_queue_deadlock_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 372

_sai_queue_api_t = struct__sai_queue_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiqueue.h: 501

_sai_router_interface_api_t = struct__sai_router_interface_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairouterinterface.h: 446

_sai_rpf_group_api_t = struct__sai_rpf_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sairpfgroup.h: 232

_sai_samplepacket_api_t = struct__sai_samplepacket_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisamplepacket.h: 193

_sai_scheduler_group_api_t = struct__sai_scheduler_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischedulergroup.h: 201

_sai_scheduler_api_t = struct__sai_scheduler_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saischeduler.h: 207

_sai_segmentroute_api_t = struct__sai_segmentroute_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisegmentroute.h: 163

_sai_stp_api_t = struct__sai_stp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saistp.h: 279

_sai_switch_api_t = struct__sai_switch_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiswitch.h: 2363

_sai_tam_api_t = struct__sai_tam_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitam.h: 2155

_sai_tunnel_api_t = struct__sai_tunnel_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitunnel.h: 1122

_sai_udf_api_t = struct__sai_udf_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiudf.h: 442

_sai_virtual_router_api_t = struct__sai_virtual_router_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivirtualrouter.h: 186

_sai_vlan_api_t = struct__sai_vlan_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saivlan.h: 689

_sai_wred_api_t = struct__sai_wred_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiwred.h: 485

_sai_isolation_group_api_t = struct__sai_isolation_group_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiisolationgroup.h: 250

_sai_twamp_api_t = struct__sai_twamp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saitwamp.h: 565

_sai_y1731_session_event_notification_t = struct__sai_y1731_session_event_notification_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 540

_sai_y1731_api_t = struct__sai_y1731_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiy1731.h: 765

_sai_ptp_api_t = struct__sai_ptp_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiptp.h: 314

_sai_synce_api_t = struct__sai_synce_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saisynce.h: 137

sai_npm_session_status_notification_s = struct_sai_npm_session_status_notification_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 333

_sai_npm_api_t = struct__sai_npm_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sainpm.h: 435

sai_monitor_mburst_stats_s = struct_sai_monitor_mburst_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 224

sai_monitor_buffer_event_s = struct_sai_monitor_buffer_event_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 229

sai_monitor_buffer_stats_s = struct_sai_monitor_buffer_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 253

sai_monitor_latency_event_s = struct_sai_monitor_latency_event_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 269

sai_monitor_latency_stats_s = struct_sai_monitor_latency_stats_s # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 283

_sai_monitor_buffer_notification_data_t = struct__sai_monitor_buffer_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 339

_sai_monitor_latency_notification_data_t = struct__sai_monitor_latency_notification_data_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 373

_sai_monitor_api_t = struct__sai_monitor_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saimonitor.h: 524

_sai_service_method_table_t = struct__sai_service_method_table_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/sai.h: 204

_sai_uburst_api_t = struct__sai_uburst_api_t # /data01/users/systest/zhanggy/cmodel_sai_trunk/sai/inc/saiuburst.h: 395

# No inserted files

