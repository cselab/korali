.. _contributing:

********************
Contributing
********************

Additional Software
---------------------------

To collaborate in the development of Korali you need the following additional tools:

* `Doxygen <http://www.doxygen.nl/>`_ - For automatic generation of C++ documentation.

* `clang-format <http://clang.llvm.org/docs/ClangFormat.html>`_ - For automatic formatting of C++ code.

* `Sphinx <https://www.sphinx-doc.org/en/master/>`_ - (automatically installed by Korali) For generating module documentation.

Korali will try to install these tools automatically, if you do not have them in your system.

General Design Rules
---------------------------

To allow the growing number of internal and external Korali developers to seamlessly integrate their modules into Korali, while reducing the number of conflicts and potential bugs, we have established a set of collaboration rules:

1. All contributions to the Korali repository should be done by means of pull requests, where at least one member of the developer's group approval.

2. All code should follow a consistent format and variables should have proper human understandable names. Cryptic, badly formatted, and inefficient code can be rejected on those grounds alone.

3. Korali is a high-performance framework, and all new methods should allow for the parallel execution of samples. 

4. All modules should be accompanied by at least one tutorial, showcasing its use and a unit test to validate its statistical/computational correctness.

5. All modules and their configuration should be properly documented.

6. You are not allowed to copy third-party code that is not GPL-licensed source and without proper credit.

Collaboration Steps Checklist
-------------------------------

We require collaborators, both internal and external, to follow these set of steps right before issuing a git pull request. 

* Get the latest commit from the master branch :code:`git checkout master; git pull` or fork it to create your own project based on the latest Korali master commit.

* Branch out to a new local branch: :code:`git checkout -b myBranch`

* (Optional) Follow :ref:`these instructions <module-dev>` to create your new module. 
* If you developed a new module, add a new tutorial in the :code:`tutorials` folder with a simple example of how to use it and the expected results, as well as a test file :code:`.run-tests.sh` for in-depth check corner case and correctness testing.

* Create a detailed description of both your module and its tutorial in their respective README.rst file. You are allowed to cite papers and links. 

* Run the *tools/dev-tools/correct-style* tool to adjust the format of your code. This tool will automatically re-format your code to meet Korali-wide standards.

* Merge the latest changes from the Korali master repository onto your forked/cloned code, so to have the latest updates already in your code.

* Make sure Korali installs correctly from scratch by running :code:`install --rebuild`

* Run the documentation generation, making sure no errors occur: :code:`docs/build.sh`. Any warnings in the generation of the documentation page or README.rst files may trigger an error. 

* Run all tests again, by running :code:`tests/run_all_tests.sh`. This step is crucial to make sure that you did not disrupt other modules and that your documentation is correct.

* Create a new pull request (either from your forked repository, or from your own branch if you are part of the developer team).

* Your pull request will be integrated once it was been reviewed and accepted by at least one Korali developer.
 
Bug Reporting
---------------------------

If you report a bug, please provide following information:

* What version of Korali you are using (including full git commit hash).

* What command(s) / code did you run and its arguments.

* On which system architecture did you execute the command.

* What versions of Python / C++ compiler did you use.

* What results were expected but not delivered.
