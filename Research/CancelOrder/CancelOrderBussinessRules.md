![](CancelOrder.png)
$$
\begin{aligned}
1.&\begin{aligned}
OrderCancel(\mu,EXT,o)\rightarrow&ReshippingBack(\mu,o,EXT)\\
&CancelPurchase(\mu,o,p)\\
&CancelFulfillment(\mu,o,f)
\end{aligned}\\
2.&CancelPurchase(\mu,o,p)\rightarrow PurchaseUndone(\mu,p,f)\\
3.&ReshippingBack(\mu,o,EXT)\rightarrow ShippingBack(\mu,EXT,f)\\
3.&CancelFulfillment(\mu,o,f)\wedge PurchaseUndone(\mu,p,f)\wedge ShippingBack(\mu,EXP,f)\\
&\rightarrow ShippingUndone(\mu,f,o)\\
4.&ShippingUndone(\mu,f,o)\rightarrow OrderUndone(\mu,o,EXT)\\
5.&OrderUndone(\mu,o,EXT)\rightarrow PaymentCancel(\mu,EXT,p)\\
6.&PaymentCancel(\mu,EXT,p)\rightarrow OrderPaymentUndone(\mu,p,o)\\
7.&OrderPaymentUndone(\mu,p,o)\rightarrow InVoice(\mu,o,e)
\end{aligned}
$$
