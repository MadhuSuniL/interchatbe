
This project is a Django application that supports WebSocket connections using Django Channels.

## Getting Started

Follow these instructions to set up and run the Django server locally.

### Prerequisites

Ensure you have the following installed:

- **Python**: [Download Python](https://www.python.org/downloads/) (v3.7+ recommended)
- **pip**: Package installer for Python
- **Redis**: A message broker required for Django Channels

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MadhuSuniL/interchatbe.git
   ```
2. **Navigate to the project directory**:

   ```bash
   cd interchatbe
   ```
3. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
5. **Install Django Channels**:

   You must install Django Channels using the following command to ensure the built-in `runserver` command will run the server as ASGI:

   ```bash
   python -m pip install -U 'channels[daphne]'
   ```
6. **Install Redis**:

   - **Windows**: Follow the instructions from [this link](https://github.com/tporadowski/redis/releases) to download and install Redis on Windows.
   - **Linux and macOS**: You can install Redis using your package manager. For example, on Ubuntu:

     ```bash
     sudo apt update
     sudo apt install redis-server
     ```

   For other distributions and OS, follow the respective Redis installation methods.

### Running the Server

Once you have installed the required dependencies and Redis:

1. **Run Redis** (if not already running):

   ```bash
   redis-server
   ```
2. **Run Django development server**:

   ```bash
   python manage.py runserver
   ```

### API Documentation

You can explore the API endpoints using the Postman documentation:

- **APIs**: [InterChat API Documentation](https://documenter.getpostman.com/view/23753014/2sA3s9Eokv)

### WebSocket Documentation

To interact with specific chat messages, use the following WebSocket (WS) connection:

- **WebSocket URL**:

  ```plaintext
  ws://localhost:8000/ws/messages/{{chat_id}}?token={{token}}
  ```

  Replace `{{chat_id}}` with the ID of the chat you want to connect to, and `{{token}}` with the user’s authentication token.
- **To Create a Message**:

  After connecting to the WebSocket, send a message in the following format to create a new message in the specified chat:

  ```json
  {
      "event_type": "create",
      "event_data": {
          "message": "<Message>"
      }
  }
  ```

  Replace `"<Message>"` with the actual message content you want to send.

### Resources

- [Django Channels Documentation](https://channels.readthedocs.io/en/stable/)
- [Redis Documentation](https://redis.io/documentation)

### License

This project is licensed under the [MIT License](LICENSE).

```

This version includes the WebSocket URL for accessing specific chat messages and the data format for creating a new message.
```
