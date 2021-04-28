# Bon Apetit functionality

To start using the bon apetit app first we must create our user and the role that this user will have (Chef or Employee0) to do so, we execute:

```
curl -X POST "http://localhost:8000/user" -H  "accept: */*" -H  "content-type: application/json" -d '{"email":"mario@gmail.com", "password":"lalelilolu", "person":{"first_name":"mario", "second_name":"guillermo", "last_name":"gomez","email":"mario_personal@gmail.com"}, "role":1}'
```

Here we are creating a new user with his username and password and the role he is going to take, also we are retrieving his personal data to create a person registry. The output of this POST is the following

```
{"id":2,"email":"mario@gmail.com","password":"pbkdf2_sha256$180000$BQzcqy39WquO$vQUacXyFXe6eiv5Tgq24EEpFk2mXZadbN5R2s0ufmh0=","person":{"id":2,"first_name":"mario","second_name":"guillermo","last_name":"gomez","email":"mario_personal@gmail.com"},"role":1}
```

After that we are ready to login with the following endpoint

```
curl -X POST "http://localhost:8000/authenticate" -H  "accept: */*" -H  "content-type: application/json" -d '{"email":"mario@gmail.com", "password":"lalelilolu"}'
```

The system will generate us a token that we will be using in the following endpoints

```
{"success":true,"statusCode":200,"message":"User logged in successfully","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5NjE4NTEyLCJqdGkiOiJjODIwYzcyMmYzOGU0MmFiODU4NDI3ZWNiZGY0MDhhNSIsInVzZXJfaWQiOjJ9.z4Ai6HxbVYknNdBUJFK7JZaqEuok01Lt0IKMwXGlh-c","refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMDgyNzgxMiwianRpIjoiNjcwNzI4ZTY3NmQxNGFhODhhMDYwOThkNjkxNThmNzgiLCJ1c2VyX2lkIjoyfQ.9IwDoILrfQZkTgb8gYWQ9nEeMZ0VQGc6aYQ0MD3-utk","authenticatedUser":{"email":"mario@gmail.com","role":"1"}}
```

So now the chef can create a menu like this

```
curl -X POST "http://localhost:8000/menu" -H  "accept: */*" -H  "content-type: application/json" -H "authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5NjE5MDEwLCJqdGkiOiJmNjIyZWQ0YjA5NGQ0MmY5OWI4Y2Q0MmI2YzcwNGM5MCIsInVzZXJfaWQiOjJ9.-Bx0OT7Xa5vDDcKBjyHb3QQpyCxiT7Pqo1DefL5apUs" -d '{"name":"Especial de navidad", "available_date":"2020-01-01"}
```

an uuid is automatically assigned to the menu, but be careful, because only the chefs are allowed to create new menus, otherwise you will receive the following message

```
{"status_code":403,"message":"Only the chef is authorized to create a Menu"}
```

Now that a menu was created, a chef can add any number of options for that menu, he can set the list of ingredients that he used so the employees can see if an ingredient doesn't fit in his diet

```
curl -X POST "http://localhost:8000/menuoption" -H  "accept: */*" -H  "content-type: application/json" -H "authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5NjIxNzY0LCJqdGkiOiI0OWU5NWJjYzM5YzI0MzQxYjU2NzE1MDdkNGVkYjI5ZCIsInVzZXJfaWQiOjJ9.zh69cenimPptLjclYjOhhghkjFgrzw2YP-HzUPtzdKA" -d '{"name":"Sopa de espinaca", "ingredients":"Espinaca, tomate, caldo", "menu":1}'
{"id":5,"name":"Sopa de espinaca","ingredients":"Espinaca, tomate, caldo","menu":1}
```

So, when the employee receive the message in slack with the url to see the menu, he can do it without a token
```
curl -X GET "http://localhost:8000/menu/2979459e-902b-4838-a714-3b77ae907501" -H  "accept: */*" -H  "content-type: application/json" -d '{"name":"algo", "available_date":"2020-01-01"}'
```

Now when the user has seen the menu he will star making his choices, he can select the options he likes and also it is possible to remove ingredients or ask for more, because who doesn't like a pizza with extra pepperoni but remember orders are taken before 11:00 A.M.
```
curl -X POST "http://localhost:8000/employeemenu" -H  "accept: */*" -H  "content-type: application/json" -H "authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5NDYwODgwLCJqdGkiOiJiNzQzOWM0NmY0ODU0ZGY4OGJiZGY5NWMzYTdlNmFlOCIsInVzZXJfaWQiOjF9.x5ZIA0-isfNcDlOc4Vb070zstwP3yJrXs-hlmERJDbc" -d '{"user_id":1, "option_id":1, "without":"cebolla, aceitunas", "extra":"queso, champiñon"}'
```

The slack reminder will be send at 9:00 A.M. it is necessary that before that hour a menu wit the available_date set to the current date exists in the database

#Notes
I implemented the tasks using celery, but when I tried to do a final test it didn't executed the task, I don't know if I moved something, so trying to fix it I used also cron tab to send the notifications to slack using the following commands
```
python3 manage.py crontab add
python3 manage.py crontab remove
```