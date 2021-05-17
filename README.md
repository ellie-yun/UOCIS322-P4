# UOCIS322 - Project 4 #
> **Author: Ellie Yun, yyun@uoregon.edu**

Brevet time calculator.

## Overview

Implement the RUSA ACP controle time calculator with Flask and AJAX.

### ACP controle times

That's *"controle"* with an *e*, because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.

The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders).  

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data.  

### Algorithms implemented in acp_times.py

> Open Time

The calculation of a control's opening time is based on the maximum speed as it's shown here https://rusa.org/pages/acp-brevet-control-times-calculator. 
First, the function needs to assert that the control distance is positive (including zero) and the control distance is not over 20% longer than the brevet distance.
When the control distance is greater than the brevet distance and is not over 20% longer than the brevet distance, the control distance has to be set to brevet distance by the rule.

Since the maximum speed depends on the range of the control location, the dictionary ```control_max_speed``` is used to store the range as its key and the speed as the value associated with that key. This dictionary will be iterated through until the function finds the range that includes the control distance passed into the function.  

There are two cases that needs to be considered for calculating the opening time:

1. When the control distance is within the range; Since time for the distance below the lower bound of the control location range is already added on the second case, it just need to add time for the difference on the distance between lower bound of the range and control distance.

2. When the control distance is longer than the higher bound of the range; Add time based on the range of the control location, which can be calculated by the difference between the lower bound and the upper bound of the range divided by the maximum speed associated with that range. 

```Note. The case when the control distance is shorter than the lower bound of the range is not considered because the lower bound of the very first range is zero and the function asserts the control distance is at least zero.``` 

> Close Time

The algorithm for calculating the closing time is pretty similar to the algorithm for calculating the opening time. The following might be the differences: 
* The calculation of a control's closing time is based on the minimum speed as it's shown here https://rusa.org/pages/acp-brevet-control-times-calculator. The information is stored in a dictionary ```control_min_speed```.
* When the control distance is greater than equal to the brevet distance but not over 20% longer than the brevet distance, the time has to be set to the set time limits by the rule.
    - There is a dictionary ```set_time_limit``` that store the brevet distance as its key and the set time limit as its value associated with the key.
* Oddities: When the control distance is less than or equal to 60 km, the maximum time limit for a control within the first 60km is based on 20 km/hr, plus 1 hour. 


## Getting started

In a nutshell, you will:

* Implement the logic in `acp_times.py` based on the algorithm linked above.

* Edit the template and Flask app so that the required remaining arugments are passed along.

* Create test cases using the website, and write test suites for your project.

* Update this file (`README`).

### AJAX and Flask reimplementation

The implementation that you will do will fill in times as the input fields are filled using AJAX and Flask. Currently the miles to kilometers (and some other basic stuff) is implemented with AJAX. The remainder is left to you.

### Testing

A suite of nose test cases is a requirement of this project. Design the test cases based on an interpretation of rules here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Be sure to test your test cases: You can use the current brevet time calculator [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html) to check that your expected test outputs are correct. While checking these values once is a manual operation, re-running your test cases should be automated in the usual manner as a Nose test suite.

To make automated testing more practical, your open and close time calculations should be in a separate module. Because I want to be able to use my test suite as well as yours, I will require that module be named `acp_times.py` and contain the two functions I have included in the skeleton code (though revised, of course, to return correct results).

We should be able to run your test suite by changing to the `brevets` directory and typing `nosetests`. All tests should pass. You should have at least 5 test cases, and more importantly, your test cases should be chosen to distinguish between an implementation that correctly interprets the ACP rules and one that does not.

## Tasks

The code under `brevets` can serve as a starting point. It illustrates a very simple AJAX transaction between the Flask server and JavaScript on the web page. Presently, the server does not calculate times (just returns the current time). Other things may be missing; add them as needed. As always, you should fork and then clone this repository, make your changes, and test on the specified server at least once before you submit.

As always you'll turn in your `credentials.ini` using Canvas, which will point to your repository on GitHub, which should contain:

* Dockerfile

* The working application.

* A `README.md` file that includes not only identifying information (your name, email, etc.) but but also a revised, clear specification of the brevet controle time calculation rules.

* An automated 'nose' test suite.

## Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.