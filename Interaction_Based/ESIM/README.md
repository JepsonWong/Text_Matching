# ESIM（Enhanced LSTM for Natural Language Inference）

## 模型结构

* 输入编码（input encoding）
* 局部推理模型（local inference modeling）
* 推理合成（inference composition）

### 输入编码（input encoding）

利用BiLSTM模块作为推理模型的一个基础模块，用它对输入单词（前提和假设）进行编码。这里BiLSTM可以通过学习表征单词和它的上下文信息（因为BiLSTM能够很好的表征局部推理信息和它在上下文中的影响）。

### 局部推理（local inference modeling）

建立前提与假设之间的局部推理模型。

