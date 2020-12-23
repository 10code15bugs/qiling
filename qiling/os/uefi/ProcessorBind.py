import ctypes

bits = 64
psize = bits // 8

dummy_ptr_type = {
	32 : ctypes.c_uint32,
	64 : ctypes.c_uint64
}[bits]

_pointer_type_cache = {}

def PTR(ptype):
	pname = 'c_void' if ptype is None else ptype.__name__

	if pname not in _pointer_type_cache:
		_pointer_type_cache[pname] = type(f'LP_{psize}_{pname}', (dummy_ptr_type,), {})

	return _pointer_type_cache[pname]

VOID = None
INT8  = ctypes.c_byte
INT16 = ctypes.c_int16
INT32 = ctypes.c_int32
INT64 = ctypes.c_int64
INTN  = INT64

UINT8  = ctypes.c_ubyte
UINT16 = ctypes.c_uint16
UINT32 = ctypes.c_uint32
UINT64 = ctypes.c_uint64
UINTN  = UINT64

BOOLEAN = UINT8
CHAR8 = UINT8
CHAR16 = UINT16

FUNCPTR = lambda *args: PTR(ctypes.CFUNCTYPE(*args))
UNION = ctypes.Union
# SIZEOF = lambda t: ctypes.sizeof(t)
# OFFSETOF = lambda cls, fname: getattr(cls, fname).offset

CPU_STACK_ALIGNMENT = 16
PAGE_SIZE = 0x1000

class STRUCT(ctypes.LittleEndianStructure):
	"""An abstract class for C structures.
	"""

	# Structures are packed by default; when needed, padding should be added
	# manually through placeholder fields
	_packed_ = 1

	def __init__(self):
		pass

	def saveTo(self, ql, address : int):
		"""Store self contents to a specified memory address.
		"""

		size = self.sizeof()
		buffer = ctypes.create_string_buffer(size)
		ctypes.memmove(buffer, ctypes.addressof(self), size)
		data = buffer.raw

		ql.mem.write(address, data)

		return address + len(data)

	@classmethod
	def loadFrom(cls, ql, address : int):
		"""Construct an instance from saved contents.
		"""

		size = cls.sizeof()
		data = bytes(ql.mem.read(address, size))
		instance = cls()

		# TODO: use ctypes.cast instead?
		ctypes.memmove(ctypes.addressof(instance), data, size)

		return instance

	@classmethod
	def sizeof(cls):
		"""Get the C structure size in bytes.
		"""

		return ctypes.sizeof(cls)

	@classmethod
	def offsetof(cls, fname):
		"""Get the offset of a field in the C structure.
		"""

		return getattr(cls, fname).offset

class EnumMeta(type(ctypes.c_int)):
	def __getattr__(self, key):
		return self._members_.index(key)

class ENUM(ctypes.c_int, metaclass=EnumMeta):
	"""An abstract class for C enums.
	"""

	_members_ = []

__all__ = [
	'VOID',
	'INT8',
	'INT16',
	'INT32',
	'INT64',
	'INTN',
	'UINT8',
	'UINT16',
	'UINT32',
	'UINT64',
	'UINTN',
	'BOOLEAN',
	'CHAR8',
	'CHAR16',

	'PTR',
	'FUNCPTR',
	'STRUCT',
	'UNION',
	'ENUM',

	'CPU_STACK_ALIGNMENT',
	'PAGE_SIZE'
]