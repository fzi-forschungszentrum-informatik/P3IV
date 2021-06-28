### General

 * For which type of application would you recommend p3iv most?
   * This is up to you. No matter if you are developing Dynamic Bayesian networks for prediction or model based planning methods such as mpc-planner, you can use this simulation framework. But if you do reinforcement learning, you may prefer to limit your use to some utility functions.

### Building and Execution

 * I have problems with building Lanelet2 and its dependencies. How to resolve these?
   * Probably some dependencies are missing. Please refer to [Lanelet2 repository](https://github.com/fzi-forschungszentrum-informatik/Lanelet2) and check its `README.md` and open & closed issues.

 * Should build in `Release` or in `Debug`?
   * If you are developing and debugging, `Debug` build is advantageous.

 * How can I set up this simulation framework in VS Code?
    * It's always a good idea to run some Python code in an IDE: adding breakpoints to unclear places helps to reveal the types and to understand the processing. You may add the lines below to your `launch.json` file.
        ```
        "configurations": [
            {
                "name": "DEU_Roundabout_OL_01",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/src/p3iv/p3iv/scripts/main.py",
                "cwd": "${workspaceFolder}/src/p3iv/p3iv/scripts",
                "args": [
                    "--run",
                    "DEU_Roundabout_OL_01"
                ],
                "console": "internalConsole"
            }
        ]
        ```
    * If you want to modify line width of black, you may add the lines below to your `settings.json` file.
        ```
        {
            "python.formatting.provider": "black",
            "python.formatting.blackPath": "<BLACK_INSTALL_DIR>/bin/black",
            "python.formatting.blackArgs": [
                "--line-length",
                "120"
            ]
        }
        ```

### Execution

 * Simulation framework fails to find a package or a module. Why?
   * Please ensure that you have built and sourced your workspace in the terminal you run the simulation environment. In case, refer search for keywords _ros catkin workspace source_ on the internet.

 * Simulation environment fails to find Lanelet2 maps.
   * Please ensure that INTERACTION dataset is located in your workspace below `src/` directory. If the problem persists, check if `interaction_dataset_dir` entry `src/p3iv/p3iv_core/src/p3iv_core/configurations/settings.py` matches the version of your dataset.

### Customization

 * Should I set the settings of my package from the simulation settings file or should I define a settings file in my package?
   * This is up to your specific case. If the settings you define are read and processed by other modules as well, then you should define it centrally. Otherwise, defining algorithm-specific settings inside the package makes more sense.

### Outputs
* Is it possible to create videos from results?
  * Yes, the animation figures are named during saving in such a way that, they can be used to create a video file. For this, ensure that you have installed `ffmpeg` on your computer and then change to the outputs directory you want to create a video. Execute the command `ffmpeg -r 5 -i step_%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4`.