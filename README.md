# 4560project
UI Components Classification for UI High-level Semantics

## Train
1. Requirements:
+ Python >= 3.6
+ Tensorflow == 2.0.0
2. Put ReDraw data set under the folder **Dataset**, it should look like this:
```
|——Dataset
   |——Training
      |——Button
      |——CheckBox
      |——ImageButton
      |——ImageView
      |——...
```

Data set: https://zenodo.org/record/2530277#.Yh1-hOhBw7e

3. Change the parameters in **config.py** to choose the kind of model.
4. Run **train.py** to start training.
## Evaluate
Run **evaluate.py** to evaluate the model's performance on the test dataset.
Run **gen.ipynb** to generate NumPy data from the saved model.
Run **eval.ipynb** to evaluate more evaluation data.

## References
1.https://github.com/calmisential/TensorFlow2.0_ResNet
2. The TensorFlow official tutorials: https://tensorflow.google.cn/beta/tutorials/quickstart/advanced
