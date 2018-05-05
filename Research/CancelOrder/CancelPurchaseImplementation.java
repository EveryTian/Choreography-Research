// This is not a java source file, use `.java` to color the code.

class Order {
    // Data:
    id orderId;
    // Relationship:
    id[] purchaseIds;
    id[] fulfillmentIds;
    // Running:
    public void listen(data) {
        switch (data) {
            case orderCancel:
                isOrderCancelGot = true;
                if (isOrderCancelGot) {
                    reshippingBack();
                    cancelPurchase();
                    cancelFulfillment();
                }
                break;
            case shippingUndone:
                isShippingUndoneGot = true;
                if (isShippingUndoneGot) {
                    orderUndone();
                }
                break;
            case orderPaymentUndone:
                isOrderPaymentUndoneGot = true;
                if (isOrderPaymentUndoneGot) {
                    inVoice();
                }
                break;
            default:
                break;
        }
    }
    // Interface:
    private void reshippingBack();    // To External
    private void cancelPurchase();    // To Purchase
    private void cancelFulfillment(); // To Fulfillment
    private void orderUndone();       // To External
    private void inVoice();           // To External
    // Snapshot:
    boolean isOrderCancelGot;
    boolean isShippingUndoneGot;
    boolean isOrderPaymentUndoneGot;
}

class Purchase {
    // Data:
    id purchaseId;
    // Relationship:
    id orderId;
    // Running:
    public void listen(data) {
        switch (data) {
            case cancelPurchase:
                isCancelPurchaseGot = true;
                purchaseUndone();
                break;
            default:
                break;
        }
    }
    // Interface:
    private purchaseUndone();
    // Snapshot:
    boolean isCancelPurchaseGot;
}

class Fulfillment {
    // Data:
    id fulfillmentId;
    // Relationship:
    id orderId;
    // Running:
    public void listen(data) {
        switch (data) {
            case cancelFulfillment:
                isCancelFulfillmentGot = true;
                if (isCancelFulfillmentGot && isPurchaseUndoneGot && isShippingBackGot) {
                    shippingUndone();
                }
                break;
            case purchaseUndone:
                isPurchaseUndoneGot = true;
                if (isCancelFulfillmentGot && isPurchaseUndoneGot && isShippingBackGot) {
                    shippingUndone();
                }
                break;
            case shippingBack:
                isShippingBackGot = true;
                if (isCancelFulfillmentGot && isPurchaseUndoneGot && isShippingBackGot) {
                    shippingUndone();
                }
                break;
            default:
                break;
        }
    }
    // Interface:
    private void shippingUndone();
    // Snapshot:
    boolean isCancelFulfillmentGot;
    boolean isPurchaseUndoneGot;
    boolean isShippingBackGot;
}

class Payment {
    // Data:
    id paymentId;
    // Relationship:
    id orderId;
    // Running:
    public listen(data) {
        switch (data) {
            case paymentCancel:
                isPaymentCancelGot = true;
                if (isPaymentCancelGot) {
                    orderPaymentUndone();
                }
            default:
                break;
        }
    }
    // Interface:
    private void orderPaymentUndone();
    // Snapshot:
    boolean isPaymentCancelGot;
}
