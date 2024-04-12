# Instructions for running

## Starting RabbitMQ

```bash
systemctl start rabbitmq-server
```

## Running the python files

```bash
clear && python clean_init.py
clear && python python request_subscriber.py 
clear && python python response_subscriber.py 
clear && python message_subscriber.py 
```
