document.getElementById('deliver').onclick = deliverOnce;

let deliveryArtifactNum = 0;

//artifact-03 发货业务流程

function deliverOnce() {
    let artifact = new Artifact('deliver');
    artifacts.push(artifact);
    artifact.id = ++deliveryArtifactNum;
    writeWhiteBoard('#' + artifact.id + ' --- BEGIN ---\n');
    createDelivery(artifact);
}

function createDelivery(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Fulfillment SEND Delivery (Fulfillment -> External)\n');
    let delivery = new Message(fulfillment, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET delivery (Fulfillment -> External)\n');
        if (artifact.id % 2 === 1) {
            writeWhiteBoard('#' + artifact.id + ' Reception Confirmed------------------\n');
            createReceiptConfirm(artifact);
        } else {
            writeWhiteBoard('#' + artifact.id + ' Reception Confirm Failed--------------\n');
            createPaymentConfirmed(artifact);
        }
    });
    artifact.msgs.push(delivery);
}

function createReceiptConfirm(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND createReceiptConfirm (External -> Payment)\n');
    let receiptConfirm = new Message(external, payment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Payment GET createReceiptConfirm (External -> Payment)\n');
        createPaymentConfirm(artifact);
    });
    artifact.msgs.push(receiptConfirm);
}

function createPaymentConfirm(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND createPaymentConfirm (Payment -> External)\n');
    let paymentConfirm = new Message(payment, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET createPaymentConfirm (Payment -> External)\n');
        createPaymentConfirmed(artifact);
    });
    artifact.msgs.push(paymentConfirm);
}

function createPaymentConfirmed(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND createPaymentConfirmed (External -> Payment)\n');
    let paymentConfirmed = new Message(external, payment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Payment GET createPaymentConfirmed (External -> Payment)\n');
        createTradeFinish(artifact);
    });
    artifact.msgs.push(paymentConfirmed);
}

function createTradeFinish(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND  (Payment -> Purchase)\n');
    let tradeFinish = new Message(payment, purchase, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Purchase GET TradeFinish (Payment -> Purchase)\n');
        createOrderFinish(artifact);
    });
    artifact.msgs.push(tradeFinish);
}

function createOrderFinish(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Purchase SEND OrderFinish (Purchase -> Order)\n');
    let orderFinish = new Message(purchase, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET OrderFinish (Purchase -> Order)\n');
        createOrderFinishConfirm(artifact);
    });
    artifact.msgs.push(orderFinish);
}

function createOrderFinishConfirm(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND OrderFinishConfirm (Order -> External)\n');
    let orderFinishConfirm = new Message(order, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET OrderFinishConfirm (Order -> External)\n');
        createOrderFinishConfirmed(artifact);
    });
    artifact.msgs.push(orderFinishConfirm);
}

function createOrderFinishConfirmed(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND OrderFinishConfirmed (External -> Order)\n');
    let orderFinishConfirmed = new Message(external, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET OrderFinishConfirmed (External -> Order)\n');
        createFinish(artifact);
    });
    artifact.msgs.push(orderFinishConfirmed);
}

function createFinish(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND Finish (Order -> External)\n');
    let finish = new Message(order, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' external GET Finish (Order -> External)\n');
        writeWhiteBoard('#' + artifact.id + ' --- END ---\n');
        artifact.alive = false;
    });
    artifact.msgs.push(finish);
}
