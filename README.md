Effective waste management is crucial for environmental sustainability and automated waste classification systems plays a vital role in this process. This project focuses on
the development of a waste segregation system utilizing a Raspberry Pi microcontroller along with the VGG16 Convolutional Neural Network (CNN) model for accurately
categorizing waste into paper, plastic, and metal classes. The system utilizes VGG16 model for its high accuracy in distinguishing between different waste materials. The
system begins by IR sensor detecting the presence of waste and capturing the image of waste item using a Pi Camera. The image is then preprocessed which is further
categorized into one of three classes. The highest prediction category is selected and microcontroller sends a signal to the servo motor which rotates the bin according to
the provided signal. This feature eliminates the need for manual sorting of waste. The waste materials were successfully segregated by the system based upon their class to
their respective bins.

The controller detects the presence of waste using IR sensor. A picture of the waste object which needs to be categorized is taken. Before passing the image through the
VGG16 model for classification, the image must go through preprocessing which typically involves resizing the image to a specific size that fits the input size expected by
the model architecture. This is done to ensure consistency in the dimensions of the input images across the entire dataset. The preprocessed result is then sent to a CNN
network that uses the VGG16 algorithm to categorize the input image into one of three classes. The dataset used for this project is taken from Kaggle. The category with the
highest prediction is then selected as the predicted category of the input image. Based on this prediction, an appropriate signal is sent to the main processing unit, which is the
Raspberry Pi. The processing unit then sends a signal to the servo motor which rotates according to the signal given by the processor.
In our model we have two bins in which one of the bin is divided into three compartments which is responsible to categorize three different types of wastes and the second
bin is marked as excess bin in which the user throws the waste in case the first bin is full. If the first bin is full, then the LCD displays ’Bin Full’ message. In this case, the
user must throw the waste in the excess bin.

