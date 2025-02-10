# Zim-Stock-Dashboard

<h2>Description</h2>
This project continues on from the work done in the Zim-Stock-Project. 
<br />


<h2>Languages and Utilities Used</h2>

<b>![image](https://github.com/user-attachments/assets/da230f44-a9fd-4bc7-b31a-c7c17053d2ea) Python 3.12.7 
</b>
  <h2>Python Packages Used</h2>
  <b>datetime, math, matplotlib, pandas,hvplot, matplotlib, numpy, seaborn, datetime, panel (for dashboard creation), requests, ploomber cloud (for dashboard deployment)
</b>

<h2>Environments Used </h2>

- <b>Jupyter Notebook</b>

<h2>Program walk-through:</h2>

<p align="center">
Accessing Zim Stock json files: <br/>
The project followed the code as described in the py file found in the repo data. 
<img src="https://i.imgur.com/vctkfGU.png" height="80%" width="80%" alt = "Data Collection"/>
<br />
<br />
Fitting linear regression model to au_usd:  <br/>
<img src="https://i.imgur.com/eYYyutt.png" height="80%" width="80%" alt="Trend Removal"/>
<br />
<br />
Checking Residuals of above regression for trend: <br/>
<img src="https://i.imgur.com/YxUavbf.png" height="80%" width="80%" alt="Trend Removal"/>
<br />
<br />
Checking First difference of time series:  <br/>
<img src="https://i.imgur.com/XQZ6lxn.png" height="80%" width="80%" alt="Trend Removal"/>
<br />
<br />
Plotting Autocorrelation function of first difference:  <br/>
<img src="https://i.imgur.com/oh14Ct6.png" height="80%" width="80%" alt="Trend Removal"/>
<br />
<br />
Choosing the best ARIMA setting using auto_arima package from pmdarima.arima:  <br/>
<img src="https://i.imgur.com/59xGyLR.png" height="80%" width="80%" alt="Modelling"/>
<br />
<br />
Plotting price prediction (within predetermined confidence intervals) versus Actual Data:  <br/>
<img src="https://i.imgur.com/alwUH0r.png" height="80%" width="80%" alt="Modelling"/>
</p>

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
