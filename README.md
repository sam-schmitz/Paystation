<h1>Paystation</h1>
<p>This project was developed over the duration of CS225 (Object-Oriented Modeling and Design)</p>
<p>The paystation is a mock parking meter. It allows the user to enter a given "coin" and recive a certain amount of time based on the amount and city. The station then prints the user a recipt. The city can be selected before the transaction is made. The paystation also features a GUI. </p>
<p>Delverable: The project can be viewed by running paystation/gui.py </p>

<h3>Paystaion uses the following programs: </h3>
<ul>
  <li>
    <h3>Paystation</h3>
    <p><b>Description: </b>Implements the buisness logic behind a parking meter. </p>
    <p><b>Location: </b>paystation/domain.py</p>
  </li>
  <li>
    <h3>Recipt</h3>
    <p><b>Description: </b>Stores data and prints itself in the correct format. </p>
    <p><b>Location: </b>paystation/domain.py</p>
  </li>
  <li>
    <h3>Multi-Paystation Model</h3>
    <p><b>Description: </b>Allows the user to switch between different paystations. </p>
    <p><b>Location: </b>paystation/gui.py</p>
  </li>
  <li>
    <h3>GUI</h3>
    <p><b>Description: </b>Uses tkinter to display the paystation. Contains different states for different states in the process. </p>
    <p><b>Location: </b>paystation/gui.py</p>
  </li>
  <li>
    <h3>GUI View</h3>
    <p><b>Description: </b>Builds the GUI in tkinter. Places the components in the window. </p>
    <p><b>Location: </b>paystation/guiview.py</p>
  </li>
  <li>
    <h3>Config</h3>
    <p><b>Description: </b>Contains "factories" that store the configuration for a paystation. </p>
    <p><b>Location: </b>paystation/config.py</p>
  </li>
  <li>
    <h3>Unittest</h3>
    <p><b>Description: </b>Unittest code for the paystation project. Can be run using "make tests"</p>
    <p><b>Location: </b>test/</p>
  </li>
</ul>
