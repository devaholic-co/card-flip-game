# FastAPI backend for Card Flip Game!

## Usage

### New Game API
```http
POST /new-game
```

| RequestBody | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Player Name |

Response
```javascript
true (always success)
```

### Play API
```http
POST /play
```

| RequestBody | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Player Name |
| `pos` | `int` | **Required**. Click Card Position (0-11) |

Response
```javascript
{
  "is_victory" : bool,
  "count" : int,
  "my_best" : int,
  "card_value": list of int
}
```
The `is_victory` attribute describes if game ended or not.

The `count` attribute contains counter of user clicks in this game.

The `my_best` attribute contains user best score.

The `card_value` attribute contains all card number (0 = closed).

### Get Global Best Score Socket API
```http
SOCKET /global_best_score
```
Return real time global best score as string

## Deployment

### For run service first time:
```yml
docker build -t cardgame . && docker run -d --name cardgamecon -p 80:80 cardgame
```

### For Automated CD script:
```yml
docker rm $(docker stop $(docker ps -a -q --filter ancestor="cardgame" --format="{{.ID}}")) && docker build -t cardgame . && docker run -d --name cardgamecon -p 80:80 cardgame
```

### Sample Github Action: 
```yml
name: Game Backend CD

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: copy file via ssh password
        uses: appleboy/scp-action@master
        with:
          host: XXX.XXX.XXX.XX
          username: root
          password: ****************
          port: 22
          source: '.'
          target: '/root/backend'
      - name: Remove Old Docker Container
        uses: appleboy/ssh-action@master
        with:
          host: XXX.XXX.XXX.XX
          username: root
          password: ****************
          port: 22
          script: cd backend && docker rm $(docker stop $(docker ps -a -q --filter ancestor="cardgame" --format="{{.ID}}"))
      - name: Run Docker
        uses: appleboy/ssh-action@master
        with:
          host: XXX.XXX.XXX.XX
          username: root
          password: ****************
          port: 22
          script: cd backend && docker build -t cardgame . && docker run -d --name cardgamecon -p 80:80 cardgame
```

## Run Test
```yml
python3 test/game_service_test.py
```
