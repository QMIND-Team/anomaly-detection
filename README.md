# Google Street-View Appraiser
Our goal: "To predict housing rebuild cost from limited attributes with deep learning."

By <b>Levi Stringer, Colin Cumming, Jacob Laframboise,</b> and <b>Nic Merz.</b> <br/>
At <u>Queen's Machine Intelligence Neuroevolution Design</u> (<b>QMIND</b>)<br/>
In collaboration with <u>Cooperators Insurance Group</u>.

### The Problem
Home owners often want to purchase short temp insurance form their insurance provider, 
so they can rent out their home on services like airbnb. for this to happen, they must 
fill out a multiple hour long survey with detailed information about their home and/or
have an appraiser come to appraise the value fo the home. having a professional appraiser
appraise your house can be a costly process, while potentially taking a substantial amount of time 
to setup. these costs and delays are good for neither the insuring party or the customer.

### Our Solution
A model which requires input of an address and minimal supplemental information and can
output an estimation of the rebuild cost of the house. 
our solution will:

1. Use google cloud api's to get the geo coordinates from the address.
2. Use google cloud api's to get a satalite and a street view image for the house. 
3. Use a google cloud api to get all of the points of interest nearby the house. 
4. Use an API from Open Data Kingston which contains all the neighbourhood boundaries to get the name of the neighbourhood.
5. Use a deep learning model to crop the images to focus on the houses. 
6. Combine the images, and put the images and metadata through a multilayer perceptron and a convolutional neural network. 
7. Output a prediction of value from the saved training weights of the model. 

### Future Implementations
This work could be deployed as a mobile app that can be integrated with the insurance provider's mobile app.
The user would enter the address they want appraised and input some metadata, and then they would get an estimate for the 
rebuild cost of their house. This would save time and money for both the insurance company and for the customer. 



