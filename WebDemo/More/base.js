const screenHeight = window.screen.height / 2;
const screenWidth = window.screen.width;

const drawingPad = document.getElementById('drawing-pad');
drawingPad.height = screenHeight;
drawingPad.width = screenWidth;

const drawingContext = drawingPad.getContext('2d');
const whiteBoard = document.getElementById('wb');

function writeWhiteBoard(msg) {
    whiteBoard.value += msg;
    whiteBoard.scrollTo(0, whiteBoard.scrollHeight);
    console.log(msg);
}

function clearPad() {
    drawingPad.height = screenHeight;
}


class Text {

    constructor(x, y, text, size, font) {
        this.x = x;
        this.y = y;
        this.text = text;
        this.size = size;
        this.font = font;
    }

    draw() {
        drawingContext.fillStyle = '#000000';
        drawingContext.font = '' + this.size + 'px ' + this.font;
        drawingContext.strokeText(this.text, this.x, this.y);
    }

}


class Triangle {

    constructor(x, y, l, color) {
        this.x = x;
        this.y = y;
        this.l = l;
        this.color = color;
    }

    draw() {
        drawingContext.fillStyle = this.color;
        drawingContext.beginPath();
        const sin60 = Math.sin(Math.PI / 3);
        const a = this.l / sin60 / 2;
        const b = this.l * sin60 / 2;
        drawingContext.moveTo(this.x, this.y - a);
        drawingContext.lineTo(this.x - a, this.y + b);
        drawingContext.lineTo(this.x + a, this.y + b);
        drawingContext.fill();
    }

}


class Rect {

    constructor(x, y, height, width, color, text) {
        this.x = x;
        this.y = y;
        this.height = height;
        this.width = width;
        this.color = color;
        if (text !== undefined) {
            this.text = new Text(x + 5, y + height - 5, text, 20, "Arial");
        }
    }

    draw() {
        if (this.color !== undefined) {
            drawingContext.fillStyle = this.color;
        }
        drawingContext.fillRect(this.x, this.y, this.width, this.height);
        if (this.text !== undefined) {
            this.text.draw();
        }
    }

}


class Circle {

    constructor(x, y, r, color) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.color = color;
    }

    draw() {
        drawingContext.beginPath();
        drawingContext.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
        if (this.color !== undefined) {
            drawingContext.fillStyle = this.color;
        }
        drawingContext.fill();
        drawingContext.closePath();
    }

}


class Message {

    constructor(from, to, artifact, fn) {
        const speedMulMin = 25;
        const speedMulMax = 75;
        this.fn = fn;
        this.artifact = artifact;
        this.color = artifact.color;
        this.fromX = from.x + from.width / 2;
        this.fromY = from.y + from.height / 2;
        this.toX = to.x + to.width / 2;
        this.toY = to.y + to.height / 2;
        this.curX = this.fromX;
        this.curY = this.fromY;
        this.direct = '';
        if (this.toX > this.fromX) {
            this.direct += 'R';
        } else if (this.toX < this.fromX) {
            this.direct += 'L';
        }
        if (this.toY > this.fromY) {
            this.direct += 'D';
        } else if (this.toY < this.fromY) {
            this.direct += 'U';
        }
        this.alive = true;
        let speedMul = Math.random() * 100;
        if (speedMul < speedMulMin) {
            speedMul = speedMulMin;
        } else if (speedMul > speedMulMax) {
            speedMul = speedMulMax;
        }
        this.speedX = Math.abs(this.toX - this.fromX) * 2 / deltaX * speedMul / 50;
        this.speedY = Math.abs(this.toY - this.fromY) / deltaY * speedMul / 50;
    }

    moveOnce() {
        let speedX = this.speedX;
        let speedY = this.speedY;
        switch (this.direct) {
            case 'U':
                this.curY -= speedY;
                if (this.curY <= this.toY) {
                    this.alive = false;
                }
                break;
            case 'D':
                this.curY += speedY;
                if (this.curY >= this.toY) {
                    this.alive = false;
                }
                break;
            case 'L':
                this.curX -= speedX;
                if (this.curX <= this.toX) {
                    this.alive = false;
                }
                break;
            case 'R':
                this.curX += speedX;
                if (this.curX >= this.toX) {
                    this.alive = false;
                }
                break;
            case 'RU':
                this.curY -= speedY;
                this.curX += speedX;
                if (this.curY <= this.toY || this.curX >= this.toX) {
                    this.alive = false;
                }
                break;
            case 'RD':
                this.curY += speedY;
                this.curX += speedX;
                if (this.curY >= this.toY || this.curX >= this.toX) {
                    this.alive = false;
                }
                break;
            case 'LD':
                this.curY += speedY;
                this.curX -= speedX;
                if (this.curY >= this.toY || this.curX <= this.toX) {
                    this.alive = false;
                }
                break;
            case 'LU':
                this.curY -= speedY;
                this.curX -= speedX;
                if (this.curY <= this.toY || this.curX <= this.toX) {
                    this.alive = false;
                }
                break;
        }
        if (!this.alive) {
            this.fn();
        }
    }

    draw() {
        this.artifact.shapeDraw(this.curX, this.curY);
    }

}


class Artifact {

    constructor(artifactName) {
        this.alive = true;
        this.color = '#' + parseInt('' + Math.random() * 1000000);
        const shapesDrawer = [
            (curX, curY) => {
                new Circle(curX, curY, 10, this.color).draw();
            },
            (curX, curY) => {
                new Rect(curX - 10, curY - 10, 20, 20, this.color).draw();
            },
            (curX, curY) => {
                new Triangle(curX, curY, 20, this.color).draw();
            }
        ];
        switch (artifactName) {
            case 'cancel-order':
                this.shapeDraw = shapesDrawer[1];
                break;
            case 'create-order':
                this.shapeDraw = shapesDrawer[2];
                break;
        }
        this.msgs = [];
    }

    draw() {
        for (let i of this.msgs) {
            if (i.alive) {
                i.draw();
            }
        }
    }

    update() {
        for (let i of this.msgs) {
            if (i.alive) {
                i.moveOnce();
            }
        }
    }

}


const deltaX = 350;
const deltaY = deltaX / 2;
const beginX = 100;
const beginY = 100;
const lenY = 75;
const lenX = 150;

const external = new Rect(beginX, beginY, lenY, lenX, '#3e45ff', 'External');
const order = new Rect(beginX + deltaX, beginY, lenY, lenX, '#7cbcff', 'Order');
const payment = new Rect(beginX + deltaX * 2, beginY, lenY, lenX, '#7cbcff', 'Payment');
const purchase = new Rect(beginX + deltaX, beginY + deltaY, lenY, lenX, '#7cbcff', 'Purchase');
const fulfillment = new Rect(beginX + deltaX * 2, beginY + deltaY, lenY, lenX, '#7cbcff', 'Fulfillment');

const bg = [external, order, payment, purchase, fulfillment];

function drawBg() {
    clearPad();
    for (let pattern of bg) {
        pattern.draw();
    }
}

document.getElementById('pause-control').onclick = () => document.getElementById('pause-control-checkbox').click();

drawBg();

let artifacts = [];

setInterval(() => {
    if (!document.getElementById('pause-control-checkbox').checked) {
        drawBg();
        for (let i of artifacts) {
            if (i.alive) {
                i.draw();
                i.update();
            }
        }
    }
}, 20);
