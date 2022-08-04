#include "c_os.h"
#include <Python.h>

void replace(
	char * str,
	char replace,
	char to
	)
{
	for (int i = 0; (str[i] = (str[i] == replace ? to : str[i])) != '\0'; i++);
}

bool os_isdir(char * path) {
   char * folder = path;
   replace(folder, '/', '\\');

	/* Create stat struct */

	struct stat sb;

	/* If it is a folder */

	if (stat(folder, &sb) == false && S_ISDIR(sb.st_mode)) {
		free(folder);
		return true;
	}
	/* If it is not a folder */
	else {
		free(folder);
		return false;
	}
}

bool os_isfile(char * path) {
	char * file = path;
    replace(file, '/', '\\');

	/* Create stat struct */

	struct stat sb;

	/* If it is a file */

	if (stat(file, &sb) == false && S_ISREG(sb.st_mode)) {
		free(file);
		return true;
	}
	/* If it is not a file */
	else {
		free(file);
		return false;
	}
}

static PyObject * wrap_isdir(PyObject * self, PyObject * args) {
	char * directory;
	PyArg_ParseTuple(args, "s", &directory);

	bool ret = os_isdir(directory);

	return ret ? Py_True : Py_False;
}

static PyObject * wrap_isfile(PyObject * self, PyObject * args) {
	char * directory;
	PyArg_ParseTuple(args, "s", &directory);

	bool ret = os_isfile(directory);

	return ret ? Py_True : Py_False;
}

static PyMethodDef OS_Methods[] = {
	{"is_true_dir", wrap_isdir, METH_VARARGS, "Returns true if path is a true directory."},
	{"is_true_file", wrap_isfile, METH_VARARGS, "Returns true if path is a true file."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef OS_Module = {
	PyModuleDef_HEAD_INIT,
	"ospath",
	"Adds 2 functions, is_true_dir and is_true_file.",
	-1,
	OS_Methods
};

PyMODINIT_FUNC PyInit_COS(void) {
	return PyModule_create(&OS_Module);
}
