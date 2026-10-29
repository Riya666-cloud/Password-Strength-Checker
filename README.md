# Password Strength Checker

A beginner-friendly cybersecurity project built with **Python Flask**, **HTML** and **CSS**.
It rates a password as **Weak**, **Medium** or **Strong** and gives tips to improve it.

## Features

- Checks length (8+ and 12+ characters)
- Checks for uppercase letters, lowercase letters, numbers and special characters
- Flags very common passwords (like `password123`) and repeated characters (like `aaa`)
- Shows a checklist, a strength meter and improvement suggestions
- Privacy-friendly: passwords are **never stored or logged**

## Project structure

```
password-strength-checker/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How the rating works

Each of these six checks that passes adds 1 point:
8+ characters, 12+ characters, uppercase, lowercase, number, special character.

| Result | Rule |
|--------|------|
| Weak   | Fewer than 8 characters, a common password, or 3 points or fewer |
| Medium | 4 or 5 points, or 6 points but with repeated characters |
| Strong | All 6 points and no repeated characters |

## Run it in VS Code on Windows

1. **Install Python** from https://www.python.org/downloads/ . During setup, tick **"Add python.exe to PATH"**.
2. **Install VS Code** from https://code.visualstudio.com/ and add the **Python** extension (by Microsoft).
3. **Unzip** the project, then in VS Code choose **File > Open Folder** and select `password-strength-checker`.
4. Open a terminal: **Terminal > New Terminal** (it opens PowerShell).
5. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   ```
6. **Activate it:**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   If you see a "running scripts is disabled" error, run this once and try again:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```
   (Or use Command Prompt and run `venv\Scripts\activate.bat` instead.)
   If VS Code asks to use the new environment, click **Yes**.
7. **Install Flask:**
   ```powershell
   pip install -r requirements.txt
   ```
8. **Start the app:**
   ```powershell
   python app.py
   ```
9. Open **http://127.0.0.1:5000** in your browser.
10. Press **Ctrl + C** in the terminal to stop the server.

If `python` is not found, try `py` instead (for example `py -m venv venv`).

## Privacy and security notes

- The form sends the password with **POST**, so it never appears in the URL.
- The server only reads the password to score it. It is not saved, printed or logged.
- The password box is empty again after every check.
- The app runs only on your own computer (`127.0.0.1`).
- Use HTTPS if you ever put an app like this on a real website.

## Ideas to extend it

- Check against a larger list of leaked passwords
- Estimate crack time
- Add a random password generator
- Add tests with `pytest`

## Limitations

This is a learning tool. Real password safety also depends on uniqueness, a password
manager, and two-factor authentication.
