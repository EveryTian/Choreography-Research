document.getElementById('cancel-order').onclick = cancelOrderOnce;

let cancelOrderArtifactNum = 0;

function cancelOrderOnce() {
    let artifact = new Artifact('cancel-order');
    artifacts.push(artifact);
    artifact.id = ++cancelOrderArtifactNum;
    writeWhiteBoard('#' + artifact.id + ' --- BEGIN ---\n');
    createOrderCancel(artifact);
}

function createOrderCancel(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND OrderCancel (External -> Order)\n');
    let orderCancel = new Message(external, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET OrderCancel (External -> Order)\n');
        createReshippingBack(artifact);
        createCancelPurchase(artifact);
        createCancelFulfillment(artifact);
    });
    artifact.msgs.push(orderCancel);
}

function createReshippingBack(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND ReshippingBack (Order -> External)\n');
    let reshippingBack = new Message(order, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET ReshippingBack (Order -> External)\n');
        createShippingBack(artifact);
    });
    artifact.msgs.push(reshippingBack);
}

function createShippingBack(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND ShippingBack (External -> Fulfillment)\n');
    let shippingBack = new Message(external, fulfillment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Fulfillment GET ShippingBack (External -> Fulfillment)\n');
        artifact.isShippingBackGot = true;
        if (artifact.isCancelFulfillmentGot && artifact.isPurchaseUndoneGot && artifact.isShippingBackGot) {
            createShippingUndone(artifact);
        }
    });
    artifact.msgs.push(shippingBack);
}

function createShippingUndone(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Fulfillment SEND ShippingUndone (Fulfillment -> Order)\n');
    let shippingUndone = new Message(fulfillment, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET ShippingUndone (Fulfillment -> Order)\n');
        createOrderUndone(artifact);
    });
    artifact.msgs.push(shippingUndone);
}

function createOrderUndone(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND OrderUndone (Order -> External)\n');
    let orderUndone = new Message(order, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET OrderUndone (Order -> External)\n');
        createPaymentCancel(artifact);
    });
    artifact.msgs.push(orderUndone);
}

function createPaymentCancel(artifact) {
    writeWhiteBoard('#' + artifact.id + ' External SEND PaymentCancel (External -> Payment)\n');
    let paymentCancel = new Message(external, payment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Payment GET PaymentCancel (External -> Payment)\n');
        createOrderPaymentUndone(artifact);
    });
    artifact.msgs.push(paymentCancel);
}

function createOrderPaymentUndone(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Payment SEND OrderPaymentUndone (Payment -> Order)\n');
    let orderPaymentUndone = new Message(payment, order, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Order GET OrderPaymentUndone (Payment -> Order)\n');
        createInVoice(artifact);
    });
    artifact.msgs.push(orderPaymentUndone);
}

function createInVoice(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND InVoice (Order -> External)\n');
    let inVoice = new Message(order, external, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' External GET InVoice (Order -> External)\n');
        writeWhiteBoard('#' + artifact.id + ' --- END ---\n');
        artifact.alive = false;
    });
    artifact.msgs.push(inVoice);
}

function createCancelPurchase(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND CancelPurchase (Order -> Purchase)\n');
    let cancelPurchase = new Message(order, purchase, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Purchase GET CancelPurchase (Order -> Purchase)\n');
        createPurchaseUndone(artifact);
    });
    artifact.msgs.push(cancelPurchase);
}

function createPurchaseUndone(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Purchase SEND PurchaseUndone (Purchase -> Fulfillment)\n');
    let purchaseUndone = new Message(purchase, fulfillment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Fulfillment GET PurchaseUndone (Purchase -> Fulfillment)\n');
        artifact.isPurchaseUndoneGot = true;
        if (artifact.isCancelFulfillmentGot && artifact.isPurchaseUndoneGot && artifact.isShippingBackGot) {
            createShippingUndone(artifact);
        }
    });
    artifact.msgs.push(purchaseUndone);
}

function createCancelFulfillment(artifact) {
    writeWhiteBoard('#' + artifact.id + ' Order SEND CancelFulfillment (Order -> Fulfillment)\n');
    let cancelFulfillment = new Message(order, fulfillment, artifact, () => {
        writeWhiteBoard('#' + artifact.id + ' Fulfillment GET CancelFulfillment (Order -> Fulfillment)\n');
        artifact.isCancelFulfillmentGot = true;
        if (artifact.isCancelFulfillmentGot && artifact.isPurchaseUndoneGot && artifact.isShippingBackGot) {
            createShippingUndone(artifact);
        }
    });
    artifact.msgs.push(cancelFulfillment);
}
