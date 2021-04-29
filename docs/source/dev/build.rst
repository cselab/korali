.. _build-process:

********************
Build Process
********************

The following diagram shows the build diagram for Korali's python modules. This process is triggered when running :code:`./install`, for a normal Korali installation. 

.. image:: images/buildProcess.png
   :scale: 20%

The installation procedure first runs the :code:`source/build.py` script, which runs the following procedure (see numbers in the diagram for reference).

Source File Preprocessing
-----------------------------
   
1. The build script will find all ._cpp files within the :code:`modules` folder and its subfolders and run the pre-process each of them.

2. The script creates the deserialization method called :code:`setConfiguration` which will contain the necessary logic to read all settings from a JSON object, guided by the modules' :code:`.config` file. Each setting therein will trigger the creation of a few lines of code to read the setting from the input JSON object into its corresponding class field. It also add logic to check whether a setting is not defined and produce a runtime error in that case. This procedure includes variable settings, which are applied to each of the Experiment's variables.    

3. Similarly, the script creates a serialization method called :code:`getConfiguration` which will read the values of the Module's class fields and save them into a JSON object.    

4. The script creates the :code:`applyModuleDefaults` function which will apply the module defaults (as described in the :code:`.config` file) to the input JSON-based configuration as provided by the users. The defaults will only apply to those fields that have not been defined by the user. This procedure is recursive, which means that, if a non-elemental (number or string) setting is present in both the user-defined configuration and the default configuration, it will recurse within the setting (instead of just skipping over it). The :code:`applyModuleDefaults` function will also apply the defaults of the module's parent classes.

5. The script creates the :code:`applyVariableDefaults` function which will apply the module variable defaults to each of the Experiment's variables.

6. If the module is a of problem-type, the script does the following:

7. Creates the :code:`runOperation` function, which handles incoming samples and run the corresponding named operation.

8. If the module is a of Distribution-type, the script does the following:

9. Creates the :code:`getPropertyPointer` function, which returns a vector will all of the distribution parameters that have been defined by a string representing a variable name (thus making it a conditional property), instead of a fixed number. 

10. After making all these modifications, the script outputs the resulting :code:`.cpp` file.

Header File Preprocessing
-----------------------------

11. The build script will find all :code:`._hpp` files within the :code:`modules` folder and its subfolders and run the pre-process each of them.

12. It creates the *file*, *namespace* and *class* Doxygen headers for automated code documentation.

13. It adds the corresponding declarations for the functions added to the source files.

14. Adds parameter (setting) class member declarations for each of the module settings (configuration, internal, and termination criteria), specified in the JSON file.

15. Adds parameter (setting) class member declarations to hold variable configuration. For this, it keeps a global variable parameter list onto which it adds the cumulative settings, making sure that repeated variable names are not re-declared. After it has processed all the modules, it adds the list of declarations to the base :code:`variable/variable._hpp` to produce :code:`variable/variable.hpp` 

16. It checks whether the module is a leaf, meaning that it is not an abstract module category and it can be selected.

17. If so, it adds a new entry to the selectable module list that is queried in :code:`getModule()`, every time a module is created.  After it has processed all the modules, it adds the list of selectable modules to the base :code:`module/module._cpp` to produce :code:`module/module.cpp` 

18. After making all these modification, the script outputs the resulting :code:`.hpp` file.

Compilation/Linking/Installation
-----------------------------------

19. The Makefile compiles all preprocessed :code:`.cpp` files within the :code:`source/modules` folder using a C++ compiler..

20. The Makefile also detects and compiles all :code:`.cpp` files within the :code:`source/auxiliar` and `source/external` folders and subfolders within.

21. The Makefile links all :code:`.o` files within the :code:`source` folder and subfolders within into the dynamically linked library :code:`libkorali.so`.

22. The :code:`install` script also downloads and installs the prerequisite GSL library.

23. The Pip installation procedure defined in the :code:`setup.py` copies the :code:`libkorali.so` and GSL libraries into the installation folder.

24. It also copies all header files in the :code:`source/` folder as well as Korali C++ compilation tools.

25. Lastly, it copies all python-based tools in the :code:`tools/` folder to create the additional Korali sub-modules.

26. The main Korali Python module and sub-modules are finally installed and ready to be used.


