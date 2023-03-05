# Techno Analytica Project

This project is for collecting publicly available data on a list of instagram users and their followers using the open source instaloader library. We aim to gather this info for market research purposes. 

## Build instructions

We use the pyinstaller library to package up the application as a GUI using TKinter. For the application to run on different Mac platforms we will need to create a build for each one individually.

### Mac w/ Intel Chip

1. Create a new conda environment with the correct architecture. For example, to create an environment with the x86_64 architecture, run:

    ```bash
    conda create --name myenv python=3.8
    conda activate myenv
    arch -x86_64 /bin/bash
    ```
    
    The last command switches the shell to the x86_64 architecture.


2. Install the required packages in the new environment. You can install the packages listed in your requirements.txt file by running:
    ```bash
    pip install -r requirements.txt
    ```
   
3. Once you have installed the required packages, you can build the PyInstaller executable in the same way as before. For example, to build the executable for a script named myscript.py, run:
    ```bash
     pyinstaller --onefile myscript.py
    ```

    This should create an executable file that is compatible with the x86_64 architecture.


4. Finally, you can deactivate the environment and switch back to your original shell by running:

    ```bash
    conda deactivate
    exit
    ```

    This will return you to your original shell and exit the x86_64 shell.

### Mac w/ M1 Chip

1. Create a spec file: A spec file is a configuration file that tells PyInstaller how to package your code. To create a spec file, navigate to your project directory and run the following command:

    ```bash
    pyinstaller --name myapp --onefile main.py
    ```

    Replace myapp with the name of your application and main.py with the name of your main script. This will create a spec file called myapp.spec.


2. Modify the spec file: Open myapp.spec with a text editor and modify it as necessary. You can add data files, exclude modules, and specify runtime options.


3. Build the executable: To build the executable, run the following command:

    ```bash
    pyinstaller myapp.spec
    ```

    This will create a dist directory containing the executable.


4. Test the executable: Test the executable on a Mac with an Intel chip to make sure it works as expected.