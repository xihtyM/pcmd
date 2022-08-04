#include <stdlib.h>
#include <stdbool.h>

/* Is on Windows System */

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
#define __WIN__f true
#define CurrentOS "win"
#else
#define __WIN__f false
#endif

/* Is on Linux System */

#if defined(__linux__) || defined(__unix__) || defined(__unix)
#define __UNIX__f true
#define CurrentOS "unix"
#else
#define __UNIX__f false
#endif

#ifndef CurrentOS
#define CurrentOS "unregistered"
#endif

#if __WIN__f == true

#define _CRT_INTERNAL_NONSTDC_NAMES true

#include <sys/stat.h>

#if !defined(S_ISREG) && defined(S_IFMT) && defined(S_IFREG)
#define S_ISREG(m) (((m)&S_IFMT) == S_IFREG)
#endif

#if !defined(S_ISDIR) && defined(S_IFMT) && defined(S_IFDIR)
#define S_ISDIR(m) (((m)&S_IFMT) == S_IFDIR)
#endif

#endif

#if __UNIX__f == true

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#endif

void replace(
	char * str,
	char replace,
	char to);
bool os_isdir(
    char * path);
bool os_isfile(
    char * path);
