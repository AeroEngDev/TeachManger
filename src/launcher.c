
/*
This is a launcher-program written in C.
The idea is to start the python Program without
the need to use CLI commands.

 Also it would be good to find a way to include python, so the end-user
 doesnt have to install python manually.
 */

// include Headers, they should be OS independant
#include <stdlib.h>
//#include <conio.h>
//#include <Python.h>


// the main method

int main() {
    system("python3 main.py");
    return 0;

}
