# Exercise 7 - Create a Microservice

1. Create a new Notification API project in a new folder with a `main.py` file and other related files.

2. The Notification API will have one endpoint: `/notify` which will receive the following JSON structured message.

```json
{
  "recipient_email": "user@somedomain.com",
  "message": "some message",
}
```

3. When the `/notify` endpoint receives a request, the message is written to a database table, and responds with the following JSON.

```json
{
  "status": "received"
}
```

4. Update the Cars API to call the Notification API's `/notify` endpoint when a new car is added or a car is deleted. The `recipient_email` value should be `broker@somedomain.com`. The message will indicate which car was added or removed.

5. Verify the two services are working together by calling the Cars API to add/remove a car, then verify the database table storing the messages in the Notification API.

## When Done

Send me an email [eric@cloudcontraptions.com](mailto:eric@cloudcontraptions.com) when you are done.
