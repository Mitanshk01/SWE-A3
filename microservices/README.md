# Instructions for running

## Starting RabbitMQ

```bash
systemctl start rabbitmq-server
```

_NOTE:_ Stop and restart the server if the queues get screwed up

## Running the python files

```bash
clear && python clean_init.py && python booking_request_handler.py
clear && python booking_processor.py
clear && python booking_confirmation.py
clear && python client.py
```
