## Fruit Similar Finder
## Purpose

To find similar images of 5 fruits: Strawberry, Banana, Mango, Apple and Grape

## Overview
Build a HSNW structure to store image features using MobileV2Net backbone to extract then using the storage structure to find most similar image with user's input
Input: a image about one of five fruit: Strawberry, Banana, Mango, Apple and Grape
Output: 5 image similar to the input image

## Usage
- To train and test the models, execute the following from notebook in directory, unless mentioned otherwise
- While training, you can use the notebook to try another feature extractor or storage structure
- The backend.py is an important file in which you can choose your model for predicting module integrating in-app.
### Training
1. Use the notebook to define your own model or feature extractor, choose hyperparameters, and start training!


```
### App Implementing
Run the backend.py to start creating an api for frontend and backend link
```
python backend.py
```
### Results
![GithubInstance/instance.png](GithubInstance/instance.png)
## Appendix
### Prepare Data
1. **Download Fruit dataset**
```shell
# get images
https://www.kaggle.com/datasets/utkarshsaxenadn/fruits-classification
Organize the data as follows:
```shell
FruitSimilar
|-- Fruit_Data
    |-- Apple1.jpeg
    |-- Apple2.jpeg
    |-- Apple3.jpeg
|--static
    |--scripts,js
    |--style.css
|--template
    |--frontend.html
|--backend.py

```
