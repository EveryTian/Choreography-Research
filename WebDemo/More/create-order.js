document.getElementById('create-order').onclick = createOrderOnce;

let createOrderArtifactNum = 0;

//artifact-02 下订单业务流程

function createOrderOnce() {
    let artifact = new Artifact('create-order');
    artifacts.push(artifact);
    artifact.id = ++createOrderArtifactNum;
    writeWhiteBoard('#' + artifact.id + ' --- BEGIN ---\n');
    createCreateOrder(artifact);
}

function createCreateOrder(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND CreateOrder (External -> Order)\n');
    let createOrder = new Message(external, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET CreateOrder (External -> Order)\n');
        createCheckInventory(artifact);
    });
    artifact.msgs.push(createOrder);
}

function createCheckInventory(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND CheckInventory (Order -> Purchase)\n');
    let checkInventory = new Message(order, purchase, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Purchase GET CheckInventory (Order -> Purchase)\n');
        createCreatePayment(artifact);
    });
    artifact.msgs.push(checkInventory);
}

function createCreatePayment(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Purchase SEND CreatePayment (Purchase -> Payment)\n');
    let createPayment = new Message(purchase, payment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Payment GET CreatePayment (Purchase -> Payment)\n');
        createDemandPayment(artifact);
    });
    artifact.msgs.push(createPayment);
}

function createDemandPayment(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND DemandPayment (Payment -> External)\n');
    let demandPayment = new Message(payment, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET DemandPayment (Payment -> External)\n');
        createPaymentForGoods(artifact);
    });
    artifact.msgs.push(demandPayment);
}

function createPaymentForGoods(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND PaymentForGoods (External -> Payment)\n');
    let paymentForGoods = new Message(external, payment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Payment GET PaymentForGoods (External -> Payment)\n');
        //由于前端demo没有输入，这里默认id为奇数的时候用户完成支付，id为偶数的时候未完成支付
        if (artifact.id % 2 === 1) {
            writeWhiteBoard('#' + artifact.id + ' User SUCCEED to complete the payment------------------\n');
            createPrepareShipment(artifact);
        } else {
            writeWhiteBoard('#' + artifact.id + ' User FAIL to complete the payment---------------------\n');
            createCancelOrder(artifact);
        }
    });
    artifact.msgs.push(paymentForGoods);
}

function createPrepareShipment(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND PrepareShipment (Payment -> Fulfillment)\n');
    let prepareShipment = new Message(payment, fulfillment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Fulfillment GET PrepareShipment (Payment -> Fulfillment)\n');
        createInformTakeDelivery(artifact);
    });
    artifact.msgs.push(prepareShipment);
}

function createCancelOrder(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND CancelOrder (Payment -> External)\n');
    let cancelOrder = new Message(payment, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET CancelOrder (Payment -> External)\n');
        writeWhiteBoard('#' + artifact.id + ' --- END ---\n');
        artifact.alive = false;
    });
    artifact.msgs.push(cancelOrder);
}

function createInformTakeDelivery(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Fulfillment SEND InformTakeDelivery (Fulfillment -> External)\n');
    let informTakeDelivery = new Message(fulfillment, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' external GET InformTakeDelivery (Fulfillment -> External)\n');
        writeWhiteBoard('#' + artifact.id + ' --- END ---\n');
        artifact.alive = false;
    });
    artifact.msgs.push(informTakeDelivery);
}
