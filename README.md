# Rankings web application - Back-end side
Project created with Django and Django Rest Framework showing back-end side of my personal rankings application.

![Fronted_1](https://user-images.githubusercontent.com/50465266/99562204-18ba6980-29c8-11eb-8a91-b8f84e93bac8.png)

## Presentation
Full presentation youtube video under link: https://youtu.be/T1WMRNu-UBM

## Built with:
- Django
- Django Rest Framework

And other additional packages aveilable in 'requirements.txt' file.

## Database:
- PostgreSQL

## REST API Overview

> ### Authentication
Authentication works with Tokens by ensuring that each request that needs authorization to a server is accompanied by signed token which the server verifies for authenticity and only then responds the request. Users can login and register with username, email and password. Before returning the Token server validates the data by checking uniqueness of username and some special requirements like `@` in the email or correct password.

> ### Permissions
Not authenticated users are only allowed to browse rankings, profiles, comments and search database. Creating own ranks, activity and integration with others by follows, likes, comments etc. requires Token otherwise server returns `401 Unauthorized`

> ### Rankings system
Rankings are the main feature of application. Each of them has its own `status` which can be set to `private` (access only for author) or `public` and collection of `positions` which are sorted in user specified order. Author of ranking is able to edit, delete, add positions and change their placement. There are two ways of exploring rankings. Newest - recently created and Hottest with specified timestamp - rankings are filtered and sorted by `rating` (total difference between likes and dislikes) to determine the most popular ones from recent days.

## API Endpoints

| HTTP method | URI path | Description |
| :--- | :--- | :--- |
| **====** | **Authentication** | **====** |
| POST | /api/auth/register | Registration with email, username, password and optional profile picture. Returns authenticated user with token |
| POST | /api/auth/login | Authenticate through username or email and password. Returns user with token |
| POST | /api/users/logout | Deletes the token from the system. Token can no longer be used to authenticate user |
| **====** | **Users** | **====** |
| GET | /api/users | Retrieves paginated list of all users |
| GET, PUT, DELETE | /api/currentuser | Retrives, deletes, updates current user if authenticated |
| GET | /api/users/**_:username_** | Retrives user's details with given **username** if any exist |
| POST | /api/users/**_:username_** | Sets/deletes 'follow' realtion between current user and user with given **username** |
| GET | /api/users/**_:username_**/rankings | Retrives given user's paginated list of public rankings |
| GET | /api/users/search/**_:query_** | Searches users with trigram based search. Returns users ordered by largest similarity |
| **====** | **Rankings** | **====** |
| GET | /api/rankings/**_:uuid_** | Retrives ranking's details with given **uuid** |
| GET | /api/rankings/private | Retrives paginated list of all current user's rankings both private and public |
| GET | /api/rankings/public | Retrives paginated list of all public rankings |
| GET | /api/rankings/followed | Retrives paginated list of all followed user's public rankings |
| GET | /api/rankings/hottest/**_:days_** | Retrives paginated list of public rankings ordered by the highest 'rating' of last **days** |
| GET | /api/rankings/newest/**_:days_** | Retrives paginated list of recently created public rankings of last **days** |
| POST | /api/rankings/create | Creates ranking if user is authenticated |
| DELETE | /api/rankings/**_:uuid_**/delete | Deletes ranking with given **uuid** if current user has permission (is the author) |
| PUT | /api/rankings/**_:uuid_**/edit | Updates ranking with given **uuid** |
| POST | /api/rankings/**_:uuid_**/create-rp | Creates position of ranking with given **uuid** if user has permission |
| DELETE | /api/rankings/**_:uuid_**/delete-rp/**_:id_** | Deletes given position of ranking |
| PUT | /api/rankings/**_:uuid_**/update-rp/**_:id_** | Updates given position of ranking |
| POST | /api/rankings/**_:uuid_**/like | Sets/deletes 'like' relation between current user and ranking with given **uuid** |
| POST | /api/rankings/**_:uuid_**/dislike | Sets/deletes 'dislike' relation between current user and ranking |
| GET | /api/rankings/search/**_:query_** | Retrives paginated list of searched rankings |

### Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 204 | `NO CONTENT` |
| 400 | `BAD REQUEST` |
| 401 | `UNAUTHORIZED` |
| 500 | `INTERNAL SERVER ERROR` |

### Front-end side
https://github.com/NPilis/rankingsAppFrontend
