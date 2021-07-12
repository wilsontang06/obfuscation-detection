# Obfuscation Detection

## How to test on a real script
1. Put the test scripts you want to run inside the directory `test-scripts` in this top-level repo

2. Grab the best model checkpoint from [Sharepoint](https://adobe-my.sharepoint.com/personal/vikrakum_adobe_com1/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fvikrakum%5Fadobe%5Fcom1%2FDocuments%2Ffile%2Dsharing) and place the file in a new directory `models` in this top-level repo.

3. Install the dependencies needed. I used Anaconda with Python 3.8.10.

4. Run `python --model cnn --model_file best-cnn1-128-fc-1024-1024-dropout-80.pth --run`
- 1 is obfuscated, 0 is non-obfuscated
- As of now, it will run the model over all the scripts in the `test-scripts` directory
