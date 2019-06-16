# WebPlagdetect

This repository hosts the prototype of a web application for Intrinsic Plagiarism detection.
It was built under Ubuntu 18.04, using Python 2.7 and C++11.
Its usage is very simple from the user perspective.
An user accesses the tool via a web browser, submits their text for analysis, 
then wait a few minutes to get the report. 
The tool will highlight candidate sentences of plagiarism cases detected.

![Tool input](/data/images/plagdetect_input.PNG)

![Tool out](/data/images/plagdetect_output.PNG)

## Install

This section contain Installation Instructions in order to run the tool.
Please note that **commands displayed are meant to be ran on the project root directory**.

### Conda environment

The requirements for the Python part of the tool are listed in  [requirements.txt](requirements.txt)
and can be installed in a brand new environment by running the following command in your terminal,
assuming you have [Anaconda](https://www.anaconda.com/) installed:

```
conda create --name webplagdetect --file requirements.txt
```

If you don't have Anaconda installed, you may download it 
[here](https://www.anaconda.com/distribution/#download-section).


### Setting up Django database

Once the Anaconda environment is created, it should be activated and the initial setup for the Django
app must be made:

```
conda activate webplagdetect
python manage.py makemigrations
python manage.py migrate
```

After running these commands, you should see a database file named `db.sqlite3` in the project
root directory.

### CPLEX

[CPLEX](https://www.ibm.com/analytics/cplex-optimizer) is required in order to run the C++11 
piece of code. It can be acquired for [free for educational purposes
](https://www.ibm.com/developerworks/community/blogs/jfp/entry/CPLEX_Is_Free_For_Students?lang=en).
The version used during the development of this project is 12.8. Once installed, make sure to
update `CPLEXDIR` value in [correlation_clustering/Makefile](correlation_clustering/Makefile)
if needed.

You can build the C++ executable by running the following commands:

```
cd correlation_clustering # changes to the directory contaning the makefile.
make # builds the executable file called by the application.
cd .. # goes back to the project root directory.
```

## Running the application

Once you have followed all the installation steps described above, you main start the tool
by running the following command:

```
python manage.py runserver
```
 
 The tool can accessed via browser in your [locahost](http://127.0.0.1:8000/).
 