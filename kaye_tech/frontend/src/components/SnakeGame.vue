<template>
<div>
  <head>
    <title></title>
  </head>
  <canvas width="360" height="200" id="game" class="snakeGame"></canvas>
</div>
</template>

<script>
import swal from "sweetalert";
import SnakeApi from "@/apis/SnakeApi";
const snakeApi = new SnakeApi();

export default {
  data() {
    return {
      active: false
    };
  },
  mounted() {
    var canvas = document.getElementById("game");
    var context = canvas.getContext("2d");

    var grid = 8;
    var count = 0;
    var active = false;
    var freezeOverride = false;
    var moved = true;

    var snake = {
      x: 40,
      y: 40,
      dx: grid,
      dy: 0,
      cells: [],
      maxCells: 4
    };
    var apple = {
      x: 40,
      y: 40
    };
    function getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min)) + min;
    }
    function loop() {
      if (active) {
        requestAnimationFrame(loop);
      }
      var score = Math.max(snake.cells.length - 4, 0);
      function die() {
        active = false;
        freezeOverride = true;
        if (score > 0) {
          swal({
            title: "Final Score: " + score,
            text: "Submit your score for the leaderboard.",
            content: "input",
            button: {
              text: "Submit Score"
            }
          }).then(value => {
            if (value) {
              snakeApi.submitScore({
                name: value,
                score: score
              });
            }
            freezeOverride = false;
            return;
          });
        } else {
          freezeOverride = false;
        }
        snake.x = 40;
        snake.y = 40;
        snake.cells = [];
        snake.maxCells = 4;
        snake.dx = 0;
        snake.dy = 0;
        apple.x = getRandomInt(0, 45) * grid;
        apple.y = getRandomInt(0, 25) * grid;
      }
      if (++count < 4) {
        return;
      }
      count = 0;
      context.clearRect(0, 0, canvas.width, canvas.height);
      snake.x += snake.dx;
      snake.y += snake.dy;
      moved = true;
      if (snake.x < 0) {
        die();
      } else if (snake.x >= canvas.width) {
        die();
      }
      if (snake.y < 0) {
        die();
      } else if (snake.y >= canvas.height) {
        die();
      }
      snake.cells.unshift({ x: snake.x, y: snake.y });
      if (snake.cells.length > snake.maxCells) {
        snake.cells.pop();
      }
      context.fillText("Score: " + score, 5, 10);
      context.fillStyle = "red";
      context.fillRect(apple.x, apple.y, grid - 1, grid - 1);
      context.fillStyle = "green";
      snake.cells.forEach(function(cell, index) {
        context.fillRect(cell.x, cell.y, grid - 1, grid - 1);
        if (cell.x === apple.x && cell.y === apple.y) {
          snake.maxCells++;
          apple.x = getRandomInt(0, 45) * grid;
          apple.y = getRandomInt(0, 25) * grid;
        }
        for (var i = index + 1; i < snake.cells.length; i++) {
          if (
            cell.x === snake.cells[i].x &&
            cell.y === snake.cells[i].y &&
            active
          ) {
            die();
          }
        }
      });
    }
    document.addEventListener("keydown", function(e) {
      if ([38, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
      }
      if ((e.key === " ") & !freezeOverride) {
        e.preventDefault();
        active = !active;
        requestAnimationFrame(loop);
      } else if (!active && !freezeOverride) {
        active = true;
        requestAnimationFrame(loop);
      }
      if (moved) {
        if (e.which === 37 && snake.dx === 0) {
          snake.dx = -grid;
          snake.dy = 0;
        } else if (e.which === 38 && snake.dy === 0) {
          snake.dy = -grid;
          snake.dx = 0;
        } else if (e.which === 39 && snake.dx === 0) {
          snake.dx = grid;
          snake.dy = 0;
        } else if (e.which === 40 && snake.dy === 0) {
          snake.dy = grid;
          snake.dx = 0;
        }
        moved = false;
      }
    });
    if (!freezeOverride) requestAnimationFrame(loop);
  }
};
</script>


<style>
.snakeGame {
  border: 1px solid white;
  width: 50%;
  height: 50%;
}
.swal-modal {
  background-color: rgb(31, 124, 7);
  border: 3px solid white;
}
.swal-text {
  font-size: 24px;
  color: white;
}
.swal-title {
  margin: 0px;
  font-size: 40px;
  margin-bottom: 28px;
  color: white;
}
.swal-button {
  padding: 7px 19px;
  border-radius: 2px;
  background-color: #471111;
  font-size: 20px;
}
</style>