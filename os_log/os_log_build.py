from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_source('_os_log', extra_compile_args=["-std=gnu11"],
                      source=r'''#include <os/log.h>
#define _os_log(log, str) (os_log((log), "%{public}s", (str)))
#define _os_log_info(log, str) (os_log_info((log), "%{public}s", (str)))
#define _os_log_debug(log, str) (os_log_debug((log), "%{public}s", (str)))
#define _os_log_error(log, str) (os_log_error((log), "%{public}s", (str)))
#define _os_log_fault(log, str) (os_log_fault((log), "%{public}s", (str)))
#define _os_log_with_type(log, type, str) (os_log_with_type((log), (type), "%{public}s", (str)))
''')

ffibuilder.cdef(
r'''typedef struct os_log_s *os_log_t;
typedef uint8_t os_log_type_t;
const os_log_t OS_LOG_DEFAULT;
const os_log_type_t OS_LOG_TYPE_DEFAULT, OS_LOG_TYPE_INFO, OS_LOG_TYPE_DEBUG, OS_LOG_TYPE_ERROR, OS_LOG_TYPE_FAULT;
os_log_t os_log_create(const char *subsystem, const char *category);
void _os_log(os_log_t log, const char *str);
void _os_log_info(os_log_t log, const char *str);
void _os_log_debug(os_log_t log, const char *str);
void _os_log_error(os_log_t log, const char *str);
void _os_log_fault(os_log_t log, const char *str);
void _os_log_with_type(os_log_t log, os_log_type_t type, const char *str);
void os_release(void *object);
''')

if __name__ == "__main__":  # not when running with setuptools
    ffibuilder.compile(verbose=True)