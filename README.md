<p align="center">
    <img src="windowicon.png" alt="App Logo" width="289px" height="260px" />
</p>
<h1 align="center">Samurai Sudoku Game & Solver App</h1>

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents">:book: Table of Contents</h2>
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project"> ➤ About The Project</a></li>
        <li><a href="#overview"> ➤ Overview</a></li>
        <li><a href="#howtoinstall"> ➤ How to Install</a></li>
        <li>
            <a href="#project-files-description"> ➤ Project Files Description</a>
        </li>
        <li><a href="#Credits"> ➤ Credits</a></li>
    </ol>
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project">:pencil: About The Project</h2>

<p align="justify">
    As using Python->PyQt5 and Mysql database of bank managing, banking,
    transactions of accounts and storing them in 3NF database.
</p>

<ul>
    <li>
        In order to use the timer, you should press the timer button.If you want to stop the timer press that button again. It will stop and when it starts, it will start again where it stopped.
    </li>
    <li> In order to restart the game, press the restart button.It will clean all sudoku grid and logs and set timer to
        1 hour.
    </li>
    <li>
        All required sudokus is stored in csv file(sukodus.csv).
    </li>
    <li>All performed operations can be viewed via a GUI(Python->PyQt5).</li>
    <li>
        It can be viewed by clicking the sudoku icon on the dist folder(If you convert this app from py to exe with pyinstaller module).
    </li>

</ul>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="overview">:cloud: Overview</h2>

<p align="justify">
    There are 5 threads to solve samurai sudoku and solve own your own with or without timer. All these actions must be
    displayed visually through a designed interface.
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
<h2 id="howtoinstall">⛓️ How to install</h2>

<p align="justify">
    There are two way to deal with it:
<ol>
    <li>Build an executable file with Pylance</li>
    <ul>
        <li> Open the location where all the documents are located.</li>
        <li> Click the right button while pressing the Shift key.</li>
        <li> You can see "Open powershell window here" .</li>
        <li> pyinstaller --onefile -w -i .\windowicon.png .\main.py</li>
        <li> Run this line of code with Shell.</li>
        <li> You can see executable file in dist folder in that folder</li>
    </ul>
    <li>Run Main(main.py) file with IDE</li>
</ol>
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
<!-- PROJECT FILES DESCRIPTION -->
<h2 id="project-files-description">📝: Project Files Description</h2>

<ul>
    <li><b>main.py</b> - Where all the main classes.</li>
    <li>
        <b>sudoku.py</b> - Where sudoku form implementation generated from
        reading ui file manager.ui.
    </li>
    <li>
        <b>requirements.txt</b> - Where all modules need.
    </li>
    <li>
        <b>res_rc_rc.py</b> - Where all resources(icons,backgrounds etc.) object
        code module.
    </li>
    <li><b>assets</b> - Where all icons.</li>
</ul>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- CREDITS -->
<h2 id="Credits">:scroll: Credits</h2>

[![GitHubBadge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/canthearwhatusay)[![LinkedInBadge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deniz-%C3%B6zcan-4aa4a8162/)
