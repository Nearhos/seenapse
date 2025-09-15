# Brain Computer Interface using the CROWN from Neurosity

<img src="https://github.com/user-attachments/assets/d57f8c69-36ca-4bca-b473-5d43506f3a2c" alt="seenapse logo" width="200" height="200">

---

## Description

Seenapse is a BCI software that allows you to think of 3 imagined movements and execute it's workflows. Think and get it done.

---

## Features

- pending

---

## Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nearhos/seenapse.git
   cd seenapse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the required variables (see below).

4. **Run the application**
   ```bash
   streamlit run home.py
   ```
   Or, if using FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

---

## Environment Variables

Create a `.env` file in the project root with:

```env
# Example environment variables
DEBUG=True
SECRET_KEY=your_secret_key
```

Adjust variables as needed for your deployment.

---

## Tech Stack

- Python
- Neurosity SDK
- FastAPI
- ngrok
- MongoDB Vector Database
- Cohere API
- Vapi

---

## Authors
- [Jocelyn Velarde](https://github.com/JocelynVelarde)
- etc

---

## License

This project is licensed under the MIT License.

---

> For questions, suggestions, or contributions, please open an issue or pull request!
