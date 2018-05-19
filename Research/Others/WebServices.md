# Web Services

*一种`XML` + `HTTP`的实现。*

- Web services are application components
- Web services communicate using open protocols
- Web services are self-contained and self-describing
- Web services can be discovered using UDDI
- Web services can be used by other applications
- HTTP and XML is the basis for Web services

## 元素

- SOAP（简易对象访问协议）
- UDDI（通用描述、发现及整合）
- WSDL（Web services 描述语言）

*除此之外，Web Services还涉及到RDF（Resource Description Framework），RSS（Really Simple Syndication）两个XML描述，不过和UDDI类似，与Web Services核心相关度不高。*

## 实例

一个基于ASP.NET的实例（ASP.NET可以生成相关WSDL和SOAP），方便理解Web Services，简单叙述如下：

假设.NET服务器上存在文件abs.asmx定义了求绝对值的WebMethod（也就是一个函数）Abs，形参为n。

那么可以存在如下关系：

向`http://foo.com/abs.asmx/Abs`POST：

```xml
n=-15
```

会收到：

```xml
<string xmlns="http://foo.com/">15</string>
```

*Web services大概就是这么一个东西。*

# WSDL

## WS-CDL

**注：WS-CDL与WSDL是不同的东西**

- WSDL描述Web Services

- WS-CDL描述Web Services中的Choreography

*WS-CDL的相关见两个W3C官方提供的文档中*

> WS-CDL is a language for specifying peer-to-peer protocols where each party wishes to remain autonomous and in which no party is master over any other.

在WS-CDL Primer的6.1中BPEL和WSDL作为Implementation Considerations & End Point Projections出现。

## Back to WSDL

*WSDL仅是一个XML文档，可**描述**某个Web Service。*

也就是说WSDL仅仅是一个对于Web Service进行描述的XML文档，或者说WSDL即是一个对于Web Service进行描述的模型。

```xml
<wsdl:definitions name="nmtoken"? targetNamespace="uri">

    <import namespace="uri" location="uri"/> *
	
    <wsdl:documentation .... /> ?

    <wsdl:types> ?
        <wsdl:documentation .... /> ?
        <xsd:schema .... /> *
    </wsdl:types>

    <wsdl:message name="ncname"> *
        <wsdl:documentation .... /> ?
        <part name="ncname" element="qname"? type="qname"?/> *
    </wsdl:message>

    <wsdl:portType name="ncname"> *
        <wsdl:documentation .... /> ?
        <wsdl:operation name="ncname"> *
            <wsdl:documentation .... /> ?
            <wsdl:input message="qname"> ?
                <wsdl:documentation .... /> ?
            </wsdl:input>
            <wsdl:output message="qname"> ?
                <wsdl:documentation .... /> ?
            </wsdl:output>
            <wsdl:fault name="ncname" message="qname"> *
                <wsdl:documentation .... /> ?
            </wsdl:fault>
        </wsdl:operation>
    </wsdl:portType>

    <wsdl:serviceType name="ncname"> *
        <wsdl:portType name="qname"/> +
    </wsdl:serviceType>

    <wsdl:binding name="ncname" type="qname"> *
        <wsdl:documentation .... /> ?
        <-- binding details --> *
        <wsdl:operation name="ncname"> *
            <wsdl:documentation .... /> ?
            <-- binding details --> *
            <wsdl:input> ?
                <wsdl:documentation .... /> ?
                <-- binding details -->
            </wsdl:input>
            <wsdl:output> ?
                <wsdl:documentation .... /> ?
                <-- binding details --> *
            </wsdl:output>
            <wsdl:fault name="ncname"> *
                <wsdl:documentation .... /> ?
                <-- binding details --> *
            </wsdl:fault>
        </wsdl:operation>
    </wsdl:binding>

    <wsdl:service name="ncname" serviceType="qname"> *
        <wsdl:documentation .... /> ?
        <wsdl:port name="ncname" binding="qname"> *
            <wsdl:documentation .... /> ?
            <-- address details -->
        </wsdl:port>
    </wsdl:service>

</wsdl:definitions>
```

## WSDL文档结构

| Element      | Definition                               |
| ------------ | ---------------------------------------- |
| `<portType>` | 描述一个web service、可被执行的操作和相关的消息 defines **a web service**, the **operations** that can be performed, and the **messages** that are involved |
| `<message>`  | 定义一个操作的数据元素，每个消息均由一个或多个部件组成              |
| `<types>`    | 使用 XML Schema 语法来定义数据类型                  |
| `<binding>`  | 为每个端口定义消息格式和协议细节                         |

### portType

`portType`中定义了一系列的操作，可以将操作分为四种具体的操作类型：

- One-way

  仅接收消息

- Request-response

  接受请求并响应

- Solicit-response

  发送请求并响应

- Notification

  仅发送消息

### binding

- `binding`元素有两个属性: `name`属性和`type`属性，其中`name`属性定义`binding`的名称，`type`属性指向用于`binding`的端口。
  
- `soap:binding`元素有两个属性: `style`属性和`transport`属性，其中`style`属性可取值`"rpc"`或`"document"`，`transport`属性定义了要使用的SOAP协议。
  
- `operation`元素定义了每个端口提供的操作符。

对于每个操作，相应的 SOAP 行为都需要被定义。

### 实例

以下是一个request-response类型的实例：

```xml
<message name="getTermRequest">
   <part name="term" type="xs:string" />
</message>

<message name="getTermResponse">
   <part name="value" type="xs:string" />
</message>

<portType name="glossaryTerms">
  <operation name="getTerm">
      <input message="getTermRequest" />
      <output message="getTermResponse" />
  </operation>
</portType>

<binding type="glossaryTerms" name="b1">
<soap:binding style="document"
transport="http://schemas.xmlsoap.org/soap/http" />
  <operation>
    <soap:operation
     soapAction="http://example.com/getTerm" />
    <input>
      <soap:body use="literal" />
    </input>
    <output>
      <soap:body use="literal" />
    </output>
  </operation>
</binding>
```

# SOAP

是Web Services的通信协议，构建于HTTP之上

*一个SOAP就是一个XML文档*

```xml
<?xml version="1.0"?>
<soap:Envelope
xmlns:soap="http://www.w3.org/2003/05/soap-envelope/"
soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">
  <soap:Header>
  ...
  </soap:Header>
  <soap:Body>
  ...
    <soap:Fault>
    ...
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
```

## 元素

- 必需的 Envelope 元素，可把此 XML 文档标识为一条 SOAP 消息
- 可选的 Header 元素，包含头部信息
- 必需的 Body 元素，包含所有的调用和响应信息
- 可选的 Fault 元素，提供有关在处理此消息所发生错误的信息

## 实例

请求：

```xml
POST /InStock HTTP/1.1
Host: www.example.org
Content-Type: application/soap+xml; charset=utf-8
Content-Length: nnn

<?xml version="1.0"?>

<soap:Envelope
xmlns:soap="http://www.w3.org/2003/05/soap-envelope/"
soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">

<soap:Body xmlns:m="http://www.example.org/stock">
  <m:GetStockPrice>
    <m:StockName>IBM</m:StockName>
  </m:GetStockPrice>
</soap:Body>

</soap:Envelope>
```

响应：

```xml
HTTP/1.1 200 OK
Content-Type: application/soap+xml; charset=utf-8
Content-Length: nnn

<?xml version="1.0"?>

<soap:Envelope
xmlns:soap="http://www.w3.org/2003/05/soap-envelope/"
soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">

<soap:Body xmlns:m="http://www.example.org/stock">
  <m:GetStockPriceResponse>
    <m:Price>34.5</m:Price>
  </m:GetStockPriceResponse>
</soap:Body>

</soap:Envelope>
```

*SOAP是通过HTTP GET or POST SOAP格式的XML文档，对于HTTP而言，要满足`Content-Type: application/soap+xml`*
