# Instructions for Running the College Cafeteria App

Follow these steps to run the College Cafeteria application on your computer:

## Prerequisites

1. **Install Python**: 
   - Download and install Python 3.7 or newer from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Verify Python installation**:
   Open Command Prompt (Windows) or Terminal (Mac/Linux) and type:
   ```
   python --version
   ```
   You should see something like `Python 3.9.5`

## Option A: If I sent you a ZIP file

1. **Extract the ZIP file** to a folder on your computer

2. **Open Command Prompt or Terminal**

3. **Navigate to the extracted folder**:
   ```
   cd path/to/college-cafeteria
   ```

4. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```
   python app.py
   ```

6. **Open your web browser** and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Option B: If I shared a GitHub repository

1. **Install Git** from [git-scm.com](https://git-scm.com/downloads) if you don't have it

2. **Open Command Prompt or Terminal**

3. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/college-cafeteria.git
   ```

4. **Navigate to the project folder**:
   ```
   cd college-cafeteria
   ```

5. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```
   python app.py
   ```

7. **Open your web browser** and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Troubleshooting

- **"Python not found" error**: Make sure Python is installed and added to your PATH
- **Package installation errors**: Try running `pip install --upgrade pip` first
- **Port already in use**: If port 5000 is already in use, edit app.py and change the port number

## Using the Application

1. **Browse the menu** by clicking on the Menu link
2. **Add items to your cart** by selecting quantities and clicking "Add to Cart"
3. **View your cart** and proceed to checkout
4. **Enter your student ID and pickup time** to complete your order

Need help? Contact me at [your contact information]