# Demo Config

![TEST - PASS](https://img.shields.io/badge/TEST-PASS-green.svg)

A demo with no logical predicates.

## Demo Model

```sequence
participant External as E
participant Sender as S
participant Receiver as R
E ->  S: SIG
S ->  R: MSG
R --> S: REC
S --> E: ACK
```

$$
\begin{aligned}
1. & SIG(\mu, EXT, s) \rightarrow MSG(\mu, s, r) \\
2. & MSG(\mu, s, r) \rightarrow REC(\mu, r, s) \\
3. & REC(\mu, r, s) \rightarrow ACK(\mu, s, EXT) \\
\end{aligned}
$$

Here is the picture for the GFM:

![Demo Model](DemoModelPicForGithub.png "Demo Model")

## Config Content

### Public Part

- Machines Addresses

  ```
  External: http://127.0.0.1:8001
  Sender:   http://127.0.0.1:8002
  Receiver: http://127.0.0.1:8003
  ```

- Messages Paths

  ```python
  {
      'SIG': ('External', 'Sender'),
      'MSG': ('Sender', 'Receiver'),
      'REC': ('Receiver', 'Sender'),
      'ACK': ('Sender', 'External')
  }
  ```

### Private Part

Shown in `.py` files.

